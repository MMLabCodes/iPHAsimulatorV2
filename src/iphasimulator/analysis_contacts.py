"""Stream residue-to-whole-PHA minimum-image distances and sampled contacts.

Distances are in Å, public times in ns, and contact means strictly ``d < cutoff``.
No coordinate fitting, equilibration removal, or inference of binding/catalysis
is performed. MDAnalysis/matplotlib are optional: install ``.[analysis]``.
"""

from __future__ import annotations

import argparse
from collections import Counter
from contextlib import contextmanager
from dataclasses import asdict, dataclass, replace
from datetime import datetime, timezone
import hashlib
from importlib import metadata
import json
from pathlib import Path
import platform
import sys
from tempfile import TemporaryDirectory
from typing import Callable
from uuid import uuid4

import numpy as np
import pandas as pd


MODES = ("all_heavy", "sidechain_heavy")
# Include common PDB, CHARMM, AMBER and GROMACS C-terminal oxygen aliases.
BACKBONE_NAMES = frozenset(("N", "CA", "C", "O", "OXT", "OT1", "OT2",
                            "O1", "O2", "OC1", "OC2", "OCT1", "OCT2"))
TIME_ATOL_NS = 1e-5


@dataclass(frozen=True)
class ContactConfig:
    topology: Path
    trajectory: Path
    output_root: Path
    pha_selection: str  # Explicit: there is no assumed ligand residue name.
    protein_selection: str = "protein"
    start_ns: float | None = None
    end_ns: float | None = None
    sample_interval_ns: float | None = None
    modes: tuple[str, ...] = MODES
    primary_cutoff_A: float = 4.5
    extra_cutoffs_A: tuple[float, ...] = (4.0, 5.0)
    preview_frames: int | None = 31
    label: str = "PHA–enzyme"
    distance_block_size: int = 1024

    @property
    def cutoffs_A(self) -> tuple[float, ...]:
        return tuple(sorted(set((4.0, 5.0, self.primary_cutoff_A, *self.extra_cutoffs_A))))

    def validate(self) -> None:
        if not self.protein_selection.strip() or not self.pha_selection.strip():
            raise ValueError("Both protein_selection and pha_selection must be explicit and nonempty.")
        if not self.modes or len(set(self.modes)) != len(self.modes) or set(self.modes) - set(MODES):
            raise ValueError(f"modes must be a nonempty subset of {MODES} without duplicates.")
        for value in (self.start_ns, self.end_ns):
            if value is not None and not np.isfinite(value):
                raise ValueError("Window boundaries must be finite times in ns or null.")
        if self.start_ns is not None and self.end_ns is not None and self.start_ns > self.end_ns:
            raise ValueError("start_ns must be <= end_ns.")
        if self.sample_interval_ns is not None and (
            not np.isfinite(self.sample_interval_ns) or self.sample_interval_ns <= 0
        ):
            raise ValueError("sample_interval_ns must be positive or null (all stored frames).")
        if any(not np.isfinite(x) or x <= 0 for x in self.cutoffs_A):
            raise ValueError("Cutoffs must be finite and positive, in Å.")
        if self.preview_frames is not None and (
            not isinstance(self.preview_frames, int) or isinstance(self.preview_frames, bool)
            or self.preview_frames < 2
        ):
            raise ValueError("preview_frames must be an integer >= 2 or null for full analysis.")
        if not isinstance(self.distance_block_size, int) or self.distance_block_size < 1:
            raise ValueError("distance_block_size must be a positive integer.")


def load_config(path: str | Path) -> ContactConfig:
    """Load YAML; relative file/output paths are relative to the YAML directory."""
    import yaml

    path = Path(path).expanduser().resolve()
    data = yaml.safe_load(path.read_text())
    if not isinstance(data, dict):
        raise ValueError("The YAML configuration must be a mapping.")
    for key in ("topology", "trajectory", "output_root"):
        value = Path(data[key]).expanduser()
        data[key] = (path.parent / value).resolve() if not value.is_absolute() else value.resolve()
    for key in ("modes", "extra_cutoffs_A"):
        if key in data:
            data[key] = tuple(data[key])
    config = ContactConfig(**data)
    config.validate()
    return config


def _jsonable(value):
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    raise TypeError(type(value).__name__)


def _write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2, default=_jsonable, allow_nan=False) + "\n")


@contextmanager
def open_universe(topology: str | Path, trajectory: str | Path):
    """Open exactly one trajectory, keeping XTC/TRR index sidecars off inputs.

    MDAnalysis writes reader caches next to the supplied trajectory path. A
    temporary symlink directs those caches to scratch without copying the data.
    Neither the simulation files nor their directory is written to.
    """
    import MDAnalysis as mda

    topology, trajectory = Path(topology).expanduser().resolve(), Path(trajectory).expanduser().resolve()
    for path in (topology, trajectory):
        if not path.is_file():
            raise FileNotFoundError(path)
    with TemporaryDirectory(prefix="ipha_contacts_") as temporary:
        link = Path(temporary) / ("trajectory" + trajectory.suffix)
        link.symlink_to(trajectory)
        # Do not override dt, subset/reorder atoms, fit, or attach transformations.
        universe = mda.Universe(str(topology), str(link))
        try:
            if universe.atoms.n_atoms != universe.trajectory.n_atoms:
                raise ValueError("Topology and trajectory atom counts differ.")
            yield universe
        finally:
            universe.trajectory.close()


def valid_box(dimensions) -> np.ndarray:
    """Require a finite, nondegenerate orthorhombic or triclinic periodic cell."""
    from MDAnalysis.lib.mdamath import triclinic_vectors

    box = np.asarray(dimensions, dtype=float)
    if (box.shape != (6,) or not np.all(np.isfinite(box)) or np.any(box[:3] <= 0)
            or np.any(box[3:] <= 0) or np.any(box[3:] >= 180)):
        raise ValueError(f"Missing or invalid periodic box: {dimensions}")
    vectors = triclinic_vectors(box, dtype=np.float64)
    if not np.isfinite(vectors).all() or np.linalg.det(vectors) <= 1e-8:
        raise ValueError(f"Degenerate periodic box: {dimensions}")
    return box


def _optional_attr(group, name, default):
    from MDAnalysis.exceptions import NoDataError

    try:
        return getattr(group, name)
    except (AttributeError, NoDataError):
        return default


def heavy_atom_mask(atoms) -> np.ndarray:
    """Exclude H/D/T and virtual sites using elements, then masses, then names.

    Number-prefixed hydrogens (e.g. 1HB) are excluded in the name fallback.
    Element/mass data take precedence over names such as the heavy atom ND1.
    """
    names = np.char.upper(np.asarray(atoms.names, dtype=str))
    elements = np.char.upper(np.asarray(_optional_attr(atoms, "elements", [""] * len(atoms)), dtype=str))
    masses = np.asarray(_optional_attr(atoms, "masses", [np.nan] * len(atoms)), dtype=float)
    element_known = elements != ""
    mass_known = np.isfinite(masses) & (masses > 0)
    name_heavy = np.array([not n.lstrip("0123456789").startswith(("H", "D", "T")) for n in names])
    mask = np.where(element_known, ~np.isin(elements, ("H", "D", "T")),
                    np.where(mass_known, masses > 3.5, name_heavy))
    # Zero-mass particles/virtual sites are not heavy atoms.
    return mask & ~(np.isfinite(masses) & (masses <= 0))


def residue_metadata(residue) -> dict:
    chains = sorted(set(str(x) for x in _optional_attr(residue.atoms, "chainIDs", []) if str(x)))
    row = {
        "resindex": int(residue.ix), "resid": int(residue.resid), "resname": str(residue.resname),
        "segindex": int(residue.segindex), "segid": str(_optional_attr(residue, "segid", "")),
        "chain_ids": ";".join(chains), "icode": str(_optional_attr(residue, "icode", "")),
    }
    row["label"] = (f"{row['resname']}{row['resid']}{row['icode']} | "
                    f"{row['chain_ids'] or row['segid'] or 'no chain'} | idx {row['resindex']}")
    return row


@dataclass
class AtomSelections:
    protein: object
    pha: object
    heavy: object
    residues: list[dict]
    atom_rows: np.ndarray
    mode_masks: dict[str, np.ndarray]
    counts: dict[str, np.ndarray]


def select_atoms(universe, protein_selection: str, pha_selection: str) -> AtomSelections:
    """Keep selected atom indices; residue.atoms is used only for identity metadata."""
    protein = universe.select_atoms(protein_selection)
    pha_input = universe.select_atoms(pha_selection)
    if not len(protein) or not len(pha_input):
        raise ValueError("Protein and PHA selections must both contain atoms.")
    if np.intersect1d(protein.indices, pha_input.indices).size:
        raise ValueError("Protein and PHA selections overlap.")
    pha = pha_input[heavy_atom_mask(pha_input)]
    heavy = protein[heavy_atom_mask(protein)]
    if not len(pha) or not len(heavy):
        raise ValueError("Protein and PHA must both contain selected heavy atoms.")
    residues = [residue_metadata(r) for r in protein.residues]
    row_by_index = {r["resindex"]: i for i, r in enumerate(residues)}
    atom_rows = np.array([row_by_index[int(i)] for i in heavy.resindices], dtype=int)
    sidechain = ~np.isin(np.char.upper(heavy.names.astype(str)), list(BACKBONE_NAMES))
    sidechain &= np.char.upper(heavy.resnames.astype(str)) != "GLY"
    masks = {"all_heavy": np.ones(len(heavy), dtype=bool), "sidechain_heavy": sidechain}
    counts = {mode: np.bincount(atom_rows[mask], minlength=len(residues)) for mode, mask in masks.items()}
    return AtomSelections(protein, pha, heavy, residues, atom_rows, masks, counts)


def _interval_info(times: np.ndarray) -> dict:
    delta = np.diff(times)
    if not len(delta):
        return {"uniform": None, "min_ns": None, "median_ns": None, "max_ns": None}
    return {"uniform": bool(np.allclose(delta, np.median(delta), rtol=1e-6, atol=TIME_ATOL_NS)),
            "min_ns": float(delta.min()), "median_ns": float(np.median(delta)), "max_ns": float(delta.max())}


def inspect_trajectory(universe, progress: Callable[[str], None] | None = None) -> dict:
    """Stream every stored frame to validate its time, atom count, and box.

    XTC has no atom identities: count compatibility cannot prove atom ordering.
    Supply the corresponding unsliced topology/trajectory from the same system.
    """
    n = len(universe.trajectory)
    if n < 1:
        raise ValueError("Trajectory is empty.")
    times = np.empty(n)
    boxes = np.empty((n, 6))
    for i, ts in enumerate(universe.trajectory):
        times[i] = ts.time / 1000.0
        try:
            boxes[i] = valid_box(ts.dimensions)
        except ValueError as exc:
            raise ValueError(f"Frame {i}: {exc}") from exc
        if ts.n_atoms != universe.atoms.n_atoms:
            raise ValueError(f"Frame {i}: topology/trajectory atom count mismatch.")
        if progress and (i % 1000 == 0 or i == n - 1):
            progress(f"Inspecting timestamps/boxes: {i + 1}/{n} frames")
    if not np.isfinite(times).all() or np.any(np.diff(times) <= 0):
        raise ValueError("Trajectory times must be finite and strictly increasing; duplicate/reversed times found.")
    return {
        "topology_n_atoms": len(universe.atoms), "trajectory_n_atoms": universe.trajectory.n_atoms,
        "n_frames": n, "start_ns": float(times[0]), "end_ns": float(times[-1]),
        "interval": _interval_info(times), "all_frame_boxes_valid": True,
        "box_min_A_degrees": boxes.min(axis=0).tolist(), "box_max_A_degrees": boxes.max(axis=0).tolist(),
        "all_boxes_orthorhombic": bool(np.allclose(boxes[:, 3:], 90)),
        "residue_name_counts": dict(Counter(str(x) for x in universe.residues.resnames)),
        "compatibility": "Atom counts match and all frames decode. XTC does not encode atom identities; ordering relies on the supplied matching topology.",
        "times_ns": times, "boxes_A_degrees": boxes,
    }


def choose_frames(times_ns, config: ContactConfig) -> tuple[np.ndarray, dict]:
    """Select an inclusive window; preview is evenly spread over eligible frames.

    Explicit intervals require a regular native grid and an integer stride, so
    requested sampling is never silently rounded. The grid starts at the first
    stored frame inside the window. All-frame sampling may retain irregular times.
    """
    config.validate()
    times = np.asarray(times_ns, dtype=float)
    if times.ndim != 1 or not len(times) or not np.isfinite(times).all() or np.any(np.diff(times) <= 0):
        raise ValueError("Times must be a finite, strictly increasing nonempty vector.")
    start = times[0] if config.start_ns is None else config.start_ns
    end = times[-1] if config.end_ns is None else config.end_ns
    if start < times[0] - TIME_ATOL_NS or end > times[-1] + TIME_ATOL_NS:
        raise ValueError(f"Requested window {start}–{end} ns exceeds available {times[0]}–{times[-1]} ns.")
    indices = np.flatnonzero((times >= start - TIME_ATOL_NS) & (times <= end + TIME_ATOL_NS))
    if not len(indices):
        raise ValueError("Analysis window contains no stored frames.")
    native = _interval_info(times)
    stride = 1
    if config.sample_interval_ns is not None:
        if native["uniform"] is not True:
            raise ValueError("An explicit sampling interval requires at least two uniformly spaced input frames.")
        stride = int(round(config.sample_interval_ns / native["median_ns"]))
        if stride < 1 or not np.isclose(stride * native["median_ns"], config.sample_interval_ns,
                                        rtol=1e-6, atol=TIME_ATOL_NS):
            raise ValueError("sample_interval_ns must be an integer multiple of the native interval.")
        indices = indices[::stride]
    eligible = len(indices)
    if config.preview_frames is not None and eligible > config.preview_frames:
        indices = indices[np.rint(np.linspace(0, eligible - 1, config.preview_frames)).astype(int)]
    return indices, {
        "kind": "preview" if config.preview_frames is not None else "full",
        "requested_window_ns": [float(start), float(end)],
        "actual_window_ns": [float(times[indices[0]]), float(times[indices[-1]])],
        "requested_interval_ns": config.sample_interval_ns, "native_stride": stride,
        "eligible_frames_before_preview": eligible, "n_analysed_frames": len(indices),
        "actual_interval": _interval_info(times[indices]),
        "window_policy": "Inclusive bounds; null uses the available boundary. No equilibration is discarded.",
        "sampling_policy": "Preview evenly spreads indices across eligible frames; full uses every eligible frame. Explicit interval is anchored at the first frame in the window.",
        "denominator": "All analysed frames; occupancy = 100 * count(distance < cutoff) / n_analysed_frames. Unavailable rows remain NaN. Samples may be correlated and are not independent observations.",
    }


def minimum_atom_distances(reference, pha, box, block_size: int = 1024) -> np.ndarray:
    """Minimum distance from each reference atom to PHA, with bounded pair buffers."""
    from MDAnalysis.lib.distances import distance_array

    box = valid_box(box)
    reference, pha = np.asarray(reference), np.asarray(pha)
    for xyz in (reference, pha):
        if xyz.ndim != 2 or xyz.shape[1] != 3 or not np.isfinite(xyz).all():
            raise ValueError("Coordinates must be finite arrays of shape (n_atoms, 3).")
    if not len(pha) or not isinstance(block_size, int) or block_size < 1:
        raise ValueError("PHA must contain atoms and block_size must be a positive integer.")
    result = np.full(len(reference), np.inf)
    for a in range(0, len(reference), block_size):
        stop = min(a + block_size, len(reference))
        for b in range(0, len(pha), block_size):
            distances = distance_array(reference[a:stop], pha[b:b + block_size], box=box)
            np.minimum(result[a:stop], distances.min(axis=1), out=result[a:stop])
    return result


def residue_minima(atom_distances, atom_rows, n_residues: int) -> np.ndarray:
    result = np.full(n_residues, np.inf)
    np.minimum.at(result, atom_rows, atom_distances)
    result[np.isinf(result)] = np.nan
    return result


def contact_occupancy(distances_A, cutoff_A: float) -> np.ndarray:
    """Residue × frame input; one binary event per frame, strict cutoff, % output.

    Any missing frame makes that row unavailable; the denominator is never
    silently reduced to the number of finite observations.
    """
    distances = np.asarray(distances_A, dtype=float)
    if distances.ndim != 2 or distances.shape[1] < 1:
        raise ValueError("Distances must be a residue × frame matrix with at least one frame.")
    if not np.isfinite(cutoff_A) or cutoff_A <= 0 or np.any(distances < 0) or np.isinf(distances).any():
        raise ValueError("Distances must be nonnegative or NaN; cutoff must be positive and finite.")
    occupancy = 100.0 * np.count_nonzero(distances < cutoff_A, axis=1) / distances.shape[1]
    occupancy[~np.isfinite(distances).all(axis=1)] = np.nan
    return occupancy


@dataclass
class ContactResult:
    times_ns: np.ndarray
    frame_indices: np.ndarray
    boxes_A_degrees: np.ndarray
    residues: list[dict]
    selected_atom_counts: dict[str, np.ndarray]
    distances_A: dict[str, np.ndarray]
    provenance: dict


def calculate_distances(universe, selections: AtomSelections, frame_indices, modes=MODES,
                        block_size=1024, progress=None) -> dict[str, np.ndarray]:
    if getattr(universe.trajectory, "transformations", ()):
        raise ValueError("Use an untransformed trajectory: fitting may invalidate its periodic box.")
    matrices = {m: np.full((len(selections.residues), len(frame_indices)), np.nan) for m in modes}
    for column, frame in enumerate(frame_indices):
        ts = universe.trajectory[int(frame)]
        atom_min = minimum_atom_distances(selections.heavy.positions, selections.pha.positions,
                                          ts.dimensions, block_size)
        for mode in modes:
            mask = selections.mode_masks[mode]
            matrices[mode][:, column] = residue_minima(atom_min[mask], selections.atom_rows[mask], len(selections.residues))
        if progress and (column % 100 == 0 or column == len(frame_indices) - 1):
            progress(f"Distances: {column + 1}/{len(frame_indices)} sampled frames ({ts.time / 1000:g} ns)")
    return matrices


def summarise(result: ContactResult, cutoffs_A=(4.0, 4.5, 5.0)) -> pd.DataFrame:
    tables = []
    for mode, distances in result.distances_A.items():
        table = pd.DataFrame(result.residues)
        table.insert(0, "mode", mode)
        table["selected_atom_count"] = result.selected_atom_counts[mode]
        table["n_analysed_frames"] = len(result.times_ns)
        table["n_valid_frames"] = np.isfinite(distances).sum(axis=1)
        valid = np.isfinite(distances).all(axis=1)
        table["available"] = valid
        table["mean_min_distance_A"] = np.nan
        table["median_min_distance_A"] = np.nan
        table.loc[valid, "mean_min_distance_A"] = distances[valid].mean(axis=1)
        table.loc[valid, "median_min_distance_A"] = np.median(distances[valid], axis=1)
        for cutoff in cutoffs_A:
            table[f"occupancy_lt_{cutoff:g}_A_pct"] = contact_occupancy(distances, cutoff)
        tables.append(table)
    return pd.concat(tables, ignore_index=True)


def save_distances(result: ContactResult, path: str | Path) -> None:
    """Save metadata as JSON strings so loading never requires pickle."""
    arrays = {"times_ns": result.times_ns, "frame_indices": result.frame_indices,
              "boxes_A_degrees": result.boxes_A_degrees,
              "residues_json": np.array(json.dumps(result.residues)),
              "provenance_json": np.array(json.dumps(result.provenance, default=_jsonable, allow_nan=False))}
    for mode, distances in result.distances_A.items():
        arrays[f"distance_{mode}_A"] = distances
        arrays[f"selected_atom_count_{mode}"] = result.selected_atom_counts[mode]
    # Exclusive creation also protects callers outside the fresh-run workflow.
    with Path(path).open("xb") as handle:
        np.savez_compressed(handle, **arrays)


def load_distances(path: str | Path) -> ContactResult:
    with np.load(path, allow_pickle=False) as data:
        modes = [m for m in MODES if f"distance_{m}_A" in data]
        return ContactResult(data["times_ns"], data["frame_indices"], data["boxes_A_degrees"],
                             json.loads(str(data["residues_json"])),
                             {m: data[f"selected_atom_count_{m}"] for m in modes},
                             {m: data[f"distance_{m}_A"] for m in modes},
                             json.loads(str(data["provenance_json"])))


def plot_contacts(result: ContactResult, output_dir: str | Path, cutoffs_A=(4.0, 4.5, 5.0),
                  primary_cutoff_A=4.5, distance_vmax_A=None) -> list[Path]:
    """Regenerate figures from saved matrices; no trajectory access is needed."""
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    paths = []
    nres = len(result.residues)
    ticks = np.unique(np.linspace(0, nres - 1, min(nres, 16)).round().astype(int))
    labels = [result.residues[i]["label"] for i in ticks]
    times = result.times_ns
    if len(times) == 1:
        edges = np.array([times[0] - 0.05, times[0] + 0.05])
    else:
        # Midpoint bins preserve irregular time spacing without interpolation.
        edges = np.r_[times[0] - (times[1] - times[0]) / 2, (times[:-1] + times[1:]) / 2,
                      times[-1] + (times[-1] - times[-2]) / 2]
    finite_maxima = [float(np.nanmax(d)) for d in result.distances_A.values() if np.isfinite(d).any()]
    vmax = distance_vmax_A if distance_vmax_A is not None else max(finite_maxima, default=1)
    if not np.isfinite(vmax) or vmax <= 0:
        raise ValueError("distance_vmax_A must be finite and positive.")
    cutoffs = sorted(set((*cutoffs_A, primary_cutoff_A)))
    kind = result.provenance["sampling"]["kind"].upper()
    title = result.provenance["config"]["label"]
    subtitle = f"{kind} · {len(times)} sampled frames · {times[0]:g}–{times[-1]:g} ns"
    cmap = plt.get_cmap("viridis").copy()
    cmap.set_bad("#dddddd")
    for mode, distances in result.distances_A.items():
        fig, ax = plt.subplots(figsize=(14, 9), layout="constrained")
        mesh = ax.pcolormesh(edges, np.arange(nres + 1) - 0.5, np.ma.masked_invalid(distances),
                             cmap=cmap, vmin=0, vmax=vmax, shading="flat", rasterized=True)
        ax.set(yticks=ticks, yticklabels=labels, ylim=(nres - 0.5, -0.5), xlabel="Trajectory time (ns)",
               ylabel="Enzyme residue (topology identity)", title=f"{title} · {mode.replace('_', ' ')}\n{subtitle}")
        ax.set_xlim((times[0], times[-1]) if len(times) > 1 else (edges[0], edges[-1]))
        ax.tick_params(axis="y", labelsize=8)
        fig.colorbar(mesh, ax=ax, label="Minimum distance to PHA heavy atoms (Å)", extend="max" if distance_vmax_A else "neither")
        fig.supxlabel("Grey = unavailable (e.g. glycine side chain). Colours show sampled distances; gaps are not interpolated.", fontsize=9)
        path = output / f"distance_heatmap_{mode}.png"
        if path.exists():
            plt.close(fig)
            raise FileExistsError(path)
        fig.savefig(path, dpi=180)
        plt.close(fig)
        paths.append(path)
        fig, ax = plt.subplots(figsize=(15, 6), layout="constrained")
        missing = ~np.isfinite(distances).all(axis=1)
        for i in np.flatnonzero(missing):
            ax.axvspan(i - 0.45, i + 0.45, color="#dddddd", zorder=0)
        for cutoff in cutoffs:
            primary = np.isclose(cutoff, primary_cutoff_A)
            ax.plot(np.arange(nres), contact_occupancy(distances, cutoff),
                    linewidth=1.8 if primary else 1, alpha=1 if primary else 0.8,
                    label=f"d < {cutoff:g} Å" + (" (primary)" if primary else ""))
        ax.set(ylim=(0, 100), xlim=(-0.5, nres - 0.5), xticks=ticks, xticklabels=labels,
               xlabel="Enzyme residue (topology identity; selected ticks)", ylabel="Sampled-frame contact occupancy (%)",
               title=f"{title} · {mode.replace('_', ' ')}\n{subtitle}")
        plt.setp(ax.get_xticklabels(), rotation=60, ha="right", fontsize=8)
        handles, legend_labels = ax.get_legend_handles_labels()
        if missing.any():
            handles.append(Patch(color="#dddddd")); legend_labels.append("Unavailable")
        ax.legend(handles, legend_labels, loc="upper right")
        ax.grid(axis="y", alpha=0.25)
        path = output / f"contact_occupancy_{mode}.png"
        if path.exists():
            plt.close(fig)
            raise FileExistsError(path)
        fig.savefig(path, dpi=180)
        plt.close(fig)
        paths.append(path)
    return paths


def _fingerprint(path: Path, full_hash=False) -> dict:
    stat = path.stat()
    info = {"path": str(path.resolve()), "size_bytes": stat.st_size, "mtime_ns": stat.st_mtime_ns}
    if full_hash:
        info["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    return info


def _selection_report(selections: AtomSelections) -> dict:
    return {
        "protein_base_atoms": len(selections.protein), "protein_residues": len(selections.residues),
        "protein_heavy_atoms": len(selections.heavy), "pha_heavy_atoms": len(selections.pha),
        "pha_residues": [residue_metadata(r) for r in selections.pha.residues],
        "selected_atoms_by_mode": {m: int(c.sum()) for m, c in selections.counts.items()},
        "unavailable_residues_by_mode": {m: [r for r, count in zip(selections.residues, c) if count == 0]
                                          for m, c in selections.counts.items()},
        "heavy_atom_policy": "Elements exclude H/D/T; missing elements use mass >3.5 u, then names (leading digits stripped). Zero-mass sites excluded.",
        "sidechain_excluded_names": sorted(BACKBONE_NAMES),
        "glycine_policy": "No side-chain heavy atoms; retain as NaN.",
    }


def _atom_inventory(selections: AtomSelections) -> pd.DataFrame:
    tables = []
    for role, group in (("protein_heavy", selections.heavy), ("pha_heavy", selections.pha)):
        table = pd.DataFrame({"role": role, "atom_index": group.indices, "atom_name": group.names,
                              "resindex": group.resindices, "resid": group.resids, "resname": group.resnames,
                              "segid": group.segids,
                              "element": _optional_attr(group, "elements", [""] * len(group)),
                              "mass_u": _optional_attr(group, "masses", [np.nan] * len(group))})
        table["in_sidechain_mode"] = selections.mode_masks["sidechain_heavy"] if role == "protein_heavy" else False
        tables.append(table)
    return pd.concat(tables, ignore_index=True)


def run_contacts(config: ContactConfig, progress: Callable[[str], None] | None = print) -> Path:
    """Inspect, calculate, and write one fresh, timestamped run; never overwrite."""
    config = replace(config, **{key: Path(getattr(config, key)).expanduser().resolve()
                                for key in ("topology", "trajectory", "output_root")})
    config.validate()
    for path in (config.topology, config.trajectory):
        if not path.is_file():
            raise FileNotFoundError(path)
    kind = "preview" if config.preview_frames is not None else "full"
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    output = config.output_root / f"{stamp}_{kind}_{uuid4().hex[:8]}"
    output.mkdir(parents=True, exist_ok=False)
    _write_json(output / "config.json", asdict(config))
    _write_json(output / "status.json", {"status": "running"})
    try:
        if progress:
            progress(f"Run directory: {output}")
        inputs = {"topology": _fingerprint(config.topology, True), "trajectory": _fingerprint(config.trajectory)}
        with open_universe(config.topology, config.trajectory) as universe:
            selections = select_atoms(universe, config.protein_selection, config.pha_selection)
            selection_report = _selection_report(selections)
            _write_json(output / "selections.json", selection_report)
            pd.DataFrame(selections.residues).to_csv(output / "protein_residues.csv", index=False)
            _atom_inventory(selections).to_csv(output / "selected_atoms.csv", index=False)
            if progress:
                progress(f"Protein: {len(selections.residues)} residues, {len(selections.heavy)} heavy atoms; PHA: {len(selections.pha)} heavy atoms")
            inspection = inspect_trajectory(universe, progress)
            times, boxes = inspection.pop("times_ns"), inspection.pop("boxes_A_degrees")
            _write_json(output / "inspection.json", inspection)
            pd.DataFrame({"frame_index": np.arange(len(times)), "time_ns": times,
                          **{key: boxes[:, i] for i, key in enumerate(("lx_A", "ly_A", "lz_A", "alpha_deg", "beta_deg", "gamma_deg"))}}).to_csv(output / "trajectory_frames.csv", index=False)
            frame_indices, sampling = choose_frames(times, config)
            if progress:
                progress(f"{kind.upper()}: {sampling['n_analysed_frames']} frames, {sampling['actual_window_ns']} ns; available {inspection['start_ns']}–{inspection['end_ns']} ns")
            versions = {"python": platform.python_version()}
            for package in ("iphasimulator", "MDAnalysis", "numpy", "scipy", "pandas", "matplotlib", "PyYAML"):
                try:
                    versions[package] = metadata.version(package)
                except metadata.PackageNotFoundError:
                    versions[package] = "not installed"
            provenance = {
                "schema_version": 1, "created_utc": stamp, "config": asdict(config), "inputs": inputs,
                "inspection": inspection, "sampling": sampling, "selections": selection_report,
                "software_versions": versions, "python_executable": sys.executable,
                "module_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "units": {"time": "ns", "distance": "Å", "occupancy": "%", "box_angles": "degrees"},
                "cutoffs_A": config.cutoffs_A, "matrix_axes": ["residue", "sampled_frame"],
                "method": "Unfitted coordinates; same-frame periodic minimum-image distance_array, minimum over all selected PHA heavy atoms; vectorised residue reduction.",
                "interpretation": "Proximity/contact only; not binding affinity or evidence of catalysis. No convergence claim or independent-sample uncertainty estimate.",
                "fingerprints": "Topology and implementation SHA-256; trajectory path/size/mtime only (no full multi-GB hash).",
            }
            _write_json(output / "provenance.json", provenance)
            matrices = calculate_distances(universe, selections, frame_indices, config.modes,
                                            config.distance_block_size, progress)
            result = ContactResult(times[frame_indices], frame_indices, boxes[frame_indices], selections.residues,
                                   {m: selections.counts[m] for m in config.modes}, matrices, provenance)
        for key, path in (("topology", config.topology), ("trajectory", config.trajectory)):
            current = _fingerprint(path)
            if any(current[k] != inputs[key][k] for k in ("size_bytes", "mtime_ns")):
                raise RuntimeError(f"Input {key} changed during the analysis; results are invalid.")
        save_distances(result, output / "distances.npz")
        summarise(result, config.cutoffs_A).to_csv(output / "residue_summary.csv", index=False, na_rep="NaN")
        plot_contacts(result, output, config.cutoffs_A, config.primary_cutoff_A)
        _write_json(output / "status.json", {"status": "complete", "kind": kind, "n_analysed_frames": len(frame_indices)})
        if progress:
            progress(f"Complete: {output}")
        return output
    except Exception as exc:
        _write_json(output / "status.json", {"status": "failed", "error": f"{type(exc).__name__}: {exc}"})
        raise


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", type=Path, help="YAML configuration; relative paths resolve against its directory")
    choice = parser.add_mutually_exclusive_group()
    choice.add_argument("--full", action="store_true", help="Use every configured sampled frame, disabling preview")
    choice.add_argument("--preview-frames", type=int, help="Preview evenly spread over the configured window")
    parser.add_argument("--start-ns", type=float)
    parser.add_argument("--end-ns", type=float)
    parser.add_argument("--sample-interval-ns", type=float)
    parser.add_argument("--mode", choices=(*MODES, "both"))
    parser.add_argument("--cutoff-A", type=float, dest="primary_cutoff_A")
    parser.add_argument("--output-root", type=Path)
    args = parser.parse_args(argv)
    config = load_config(args.config)
    overrides = {key: getattr(args, key) for key in ("start_ns", "end_ns", "sample_interval_ns", "primary_cutoff_A", "output_root")
                 if getattr(args, key) is not None}
    if args.full:
        overrides["preview_frames"] = None
    elif args.preview_frames is not None:
        overrides["preview_frames"] = args.preview_frames
    if args.mode:
        overrides["modes"] = MODES if args.mode == "both" else (args.mode,)
    run_contacts(replace(config, **overrides), progress=lambda message: print(message, flush=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
