"""Configuration-driven, streaming GROMACS XTC processing for enzyme–PHA systems.

Run ``python -m iphasimulator.trajectory_processing instrcution.txt --dry-run``.
Paths in YAML are relative to that file. No simulation or viewer is launched.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict, dataclass, field, replace
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import uuid

import yaml

from iphasimulator.trajectory_centering import (
    GROUP_HEADER_PATTERN, GromacsIndex, read_index, write_index,
)
from iphasimulator.trajectory_gromacs_trjconv import run_trjconv


WORKFLOW = "iphasimulator.trajectory_processing.v1"


class _UniqueLoader(yaml.SafeLoader):
    pass


def _unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str) or key in result:
            raise ValueError(f"YAML keys must be unique strings: {key!r}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


_UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _unique_mapping)


@dataclass(frozen=True)
class ProcessingConfig:
    """Validated settings; all filesystem paths are absolute after loading."""

    instruction_file: Path
    input_trajectory: Path
    structure: Path
    index: Path
    output_dir: Path
    schema_version: int = 1
    stride: int = 100
    pbc: str = "none"
    center: bool = False
    center_group: str | None = None
    fit: str = "none"
    fit_group: str | None = None
    output_group: str = "SYSTEM"
    prepare_vmd: bool = True
    overwrite: bool = False
    dry_run: bool = False
    gmx: str = "gmx"
    custom_groups: dict[str, str] = field(default_factory=dict)


def load_config(path: str | Path) -> ProcessingConfig:
    """Read strict YAML, rejecting unknown/duplicate keys and invalid values."""
    path = Path(path).expanduser().resolve(strict=True)
    data = yaml.load(path.read_text(), Loader=_UniqueLoader)
    if not isinstance(data, dict):
        raise ValueError("Instruction file must contain a YAML mapping")
    allowed = set(ProcessingConfig.__dataclass_fields__) - {"instruction_file"}
    if set(data) - allowed:
        raise ValueError(f"Unknown settings: {sorted(set(data) - allowed)}")
    for key in ("input_trajectory", "structure", "index", "output_dir"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ValueError(f"{key} must be a nonempty path string")
        value = Path(data[key]).expanduser()
        data[key] = (path.parent / value).resolve()
    cfg = ProcessingConfig(instruction_file=path, **data)
    if type(cfg.schema_version) is not int or cfg.schema_version != 1:
        raise ValueError("schema_version must be 1")
    if type(cfg.stride) is not int or not 1 <= cfg.stride <= 2147483647:
        raise ValueError("stride must be a positive integer <= 2147483647")
    for key in ("center", "prepare_vmd", "overwrite", "dry_run"):
        if type(getattr(cfg, key)) is not bool:
            raise ValueError(f"{key} must be true or false, without quotes")
    if cfg.pbc not in ("none", "mol", "whole", "res", "atom"):
        raise ValueError("pbc must be none, mol, whole, res or atom; nojump/cluster are not supported")
    if cfg.fit not in ("none", "rot+trans", "translation"):
        raise ValueError("fit must be none, rot+trans or translation")
    for key in ("center_group", "fit_group", "output_group"):
        value = getattr(cfg, key)
        if value is not None and (not isinstance(value, str) or not value.strip() or "\n" in value):
            raise ValueError(f"{key} must be an exact group name or null")
    if not cfg.output_group or (cfg.center and not cfg.center_group) or (cfg.fit != "none" and not cfg.fit_group):
        raise ValueError("Explicit output, enabled centring and enabled fitting groups are required")
    if not isinstance(cfg.gmx, str) or not cfg.gmx.strip():
        raise ValueError("gmx must be one executable name or path, not a shell command")
    if "/" in cfg.gmx:
        cfg = replace(cfg, gmx=str((path.parent / Path(cfg.gmx).expanduser()).resolve()))
    if not isinstance(cfg.custom_groups, dict) or any(
        not isinstance(k, str) or not k.strip() or any(c in k for c in "[]\n\r")
        or not isinstance(v, str) or not v.strip() for k, v in cfg.custom_groups.items()
    ):
        raise ValueError("custom_groups must map group names to MDAnalysis selection strings")
    return cfg


def resolved_settings(cfg: ProcessingConfig) -> dict:
    """Return JSON/YAML-serialisable settings, including resolved paths."""
    return {k: str(v) if isinstance(v, Path) else v for k, v in asdict(cfg).items()}


def check_output_safety(cfg: ProcessingConfig) -> None:
    """Refuse raw-input containment and replacement of unowned output folders."""
    for path in (cfg.instruction_file, cfg.input_trajectory, cfg.structure, cfg.index):
        if path.is_relative_to(cfg.output_dir):
            raise ValueError(f"Output directory would contain a protected input: {path}")
    if cfg.output_dir.exists():
        if not cfg.overwrite:
            raise FileExistsError(f"Output already exists: {cfg.output_dir}; choose a new output_dir or set overwrite: true")
        summary = cfg.output_dir / "summary.json"
        if not summary.is_file() or json.loads(summary.read_text()).get("workflow") != WORKFLOW:
            raise ValueError("overwrite only accepts a directory created by this workflow")


def _dependencies():
    try:
        import MDAnalysis as mda
        import numpy as np
        from MDAnalysis.lib.formats.libmdaxdr import XTCFile
    except ImportError as exc:
        raise RuntimeError("Install the analysis extra: python -m pip install -e '.[analysis]'") from exc
    return mda, np, XTCFile


def _check_frame(frame, atom_count, require_box):
    _, np, _ = _dependencies()
    if frame.x.shape != (atom_count, 3):
        raise ValueError("Trajectory/structure atom count mismatch")
    if not np.isfinite(frame.x).all() or not np.isfinite(frame.time):
        raise ValueError("Non-finite trajectory coordinates or time")
    if require_box and (not np.isfinite(frame.box).all() or np.linalg.det(frame.box) <= 0):
        raise ValueError("PBC/centring requires a finite, positive-volume box")


def preflight(cfg: ProcessingConfig):
    """Validate files/tools, topology, named selections and the first XTC frame.

    This is read-only, including in dry-run mode. XTC contains no atom identities:
    its atom count can be checked, but provenance/order must be supplied correctly.
    """
    check_output_safety(cfg)
    for path in (cfg.input_trajectory, cfg.structure, cfg.index):
        if not path.is_file():
            raise FileNotFoundError(path)
    if cfg.input_trajectory.suffix.lower() != ".xtc" or cfg.structure.suffix.lower() not in (".tpr", ".gro"):
        raise ValueError("Supported inputs: XTC trajectory and matching TPR or GRO structure")
    if cfg.pbc in ("mol", "whole") and cfg.structure.suffix.lower() != ".tpr":
        raise ValueError("Molecule reconstruction requires a TPR with molecular topology")
    executable = shutil.which(cfg.gmx)
    if executable is None:
        raise FileNotFoundError(f"GROMACS executable not found: {cfg.gmx}")
    version = subprocess.run([executable, "--version"], capture_output=True, text=True, check=True, timeout=30)
    mda, np, XTCFile = _dependencies()
    universe = mda.Universe(str(cfg.structure))
    n_atoms = len(universe.atoms)
    # Existing parser supplies atom lists; reject duplicate headers first rather
    # than letting its intentionally permissive merge behaviour hide mistakes.
    headers = [m.group(1).strip().casefold() for line in cfg.index.read_text().splitlines()
               if (m := GROUP_HEADER_PATTERN.match(line))]
    if len(headers) != len(set(headers)):
        raise ValueError("Duplicate index group headers")
    groups = dict(read_index(cfg.index).groups)
    for name, selection in cfg.custom_groups.items():
        if name.casefold() in {key.casefold() for key in groups}:
            raise ValueError(f"Custom group collides with index group: {name}")
        groups[name] = tuple(int(i) + 1 for i in universe.select_atoms(selection).indices)
    for name, atoms in groups.items():
        if not atoms or min(atoms) < 1 or max(atoms) > n_atoms or len(set(atoms)) != len(atoms):
            raise ValueError(f"Invalid/empty/duplicate atom indices in group {name!r}")
    for name in (cfg.output_group, cfg.center_group, cfg.fit_group):
        if name is not None and name not in groups:
            raise ValueError(f"Unknown group {name!r}; available exact names: {list(groups)}")
    with XTCFile(str(cfg.input_trajectory), "r") as reader:
        try:
            frame = reader.read()
        except StopIteration as exc:
            raise ValueError("Input trajectory is empty") from exc
        _check_frame(frame, n_atoms, cfg.center or cfg.pbc != "none")
        if cfg.fit == "rot+trans":
            points = frame.x[np.asarray(groups[cfg.fit_group]) - 1]
            if len(points) < 3 or np.linalg.matrix_rank(points - points.mean(axis=0)) < 2:
                raise ValueError("Rotation fitting needs at least three non-collinear atoms")
        first_time = float(frame.time)
    report = {
        "atom_count": n_atoms, "first_time_ps": first_time,
        "groups": {name: {"atoms": len(atoms), "residue_atom_counts": dict(Counter(
            str(r) for r in universe.atoms[np.asarray(atoms) - 1].resnames))}
            for name, atoms in groups.items()},
        "gromacs_version": version.stdout + version.stderr,
        "mdanalysis_version": mda.__version__,
        "compatibility": "TPR/GRO and first XTC atom counts match; XTC cannot prove atom identity/order",
    }
    return universe, groups, executable, report


def command_plan(cfg: ProcessingConfig, executable: str, directory: Path | None = None) -> list[dict]:
    """Construct separate preparation and optional fitting trjconv operations."""
    directory = directory or cfg.output_dir
    fitting = cfg.fit != "none"
    selections = ["center"] if cfg.center else []
    selections.append("all_atoms" if fitting else "output")
    args = ["-skip", str(cfg.stride), "-pbc", cfg.pbc]
    if cfg.center:
        args.append("-center")
    prepared = directory / ("unfitted.xtc" if fitting else "processed.xtc")
    common = {"structure": str(cfg.structure), "index": str(directory / "selections.ndx"),
              "gmx_command": executable}
    plan = [dict(common, trajectory=str(cfg.input_trajectory), output=str(prepared),
                 selections=selections, trjconv_args=args)]
    if fitting:
        plan.append(dict(common, trajectory=str(prepared), output=str(directory / "processed.xtc"),
                         selections=["fit", "output"], trjconv_args=["-fit", cfg.fit]))
    return plan


def _logged_runner(directory):
    counter = 0

    def runner(command, *, input, **kwargs):
        nonlocal counter
        counter += 1
        stem = f"command_{counter:02d}"
        record = {"command": command, "stdin": input,
                  "stdout": stem + ".stdout.log", "stderr": stem + ".stderr.log"}
        (directory / (stem + ".json")).write_text(json.dumps(record, indent=2))
        with (directory / record["stdout"]).open("w") as out, (directory / record["stderr"]).open("w") as err:
            result = subprocess.run(command, input=input, text=True, stdout=out, stderr=err,
                                    cwd=directory)
        record["returncode"] = result.returncode
        (directory / (stem + ".json")).write_text(json.dumps(record, indent=2))
        with (directory / record["stderr"]).open("rb") as log:
            log.seek(max(0, log.seek(0, 2) - 8192))
            tail = log.read().decode(errors="replace")
        return subprocess.CompletedProcess(command, result.returncode, "", tail)

    return runner


def _verify_and_view(cfg, directory, universe, groups):
    """Stream raw/output pairs, verify stride/times and write one matching GRO."""
    import csv
    mda, np, XTCFile = _dependencies()
    atom_indices = np.asarray(groups[cfg.output_group]) - 1
    no_transform = not cfg.center and cfg.pbc == "none" and cfg.fit == "none"
    n_input = n_output = 0
    previous_time = None
    first_time = last_time = None
    with XTCFile(str(cfg.input_trajectory), "r") as source, \
            XTCFile(str(directory / "processed.xtc"), "r") as output, \
            (directory / "frames.csv").open("w", newline="") as mapping:
        writer = csv.writer(mapping)
        writer.writerow(["output_frame", "input_frame", "time_ps", "step"])
        for i, raw in enumerate(source):
            _check_frame(raw, len(universe.atoms), cfg.center or cfg.pbc != "none")
            if previous_time is not None and raw.time <= previous_time:
                raise ValueError("Input times must increase strictly; check merged restart boundaries")
            previous_time = raw.time
            n_input += 1
            if i % cfg.stride:
                continue
            try:
                processed = output.read()
            except StopIteration as exc:
                raise ValueError("Processed trajectory has too few frames") from exc
            _check_frame(processed, len(atom_indices), cfg.center or cfg.pbc != "none")
            if processed.time != raw.time or processed.step != raw.step:
                raise ValueError(f"Frame stride/time/step mismatch at input frame {i}")
            if no_transform and (not np.allclose(processed.x, raw.x[atom_indices], rtol=0, atol=0.002)
                                 or not np.allclose(processed.box, raw.box, rtol=0, atol=1e-5)):
                raise ValueError(f"Unexpected coordinate/box change at input frame {i}")
            if n_output == 0:
                # Low-level XTC coordinates are nm; MDAnalysis writers expect Angstrom.
                view = mda.Merge(universe.atoms[atom_indices])
                view.atoms.positions = processed.x * 10
                view.dimensions = mda.lib.mdamath.triclinic_box(*(processed.box * 10))
                view.atoms.write(str(directory / "viewing.gro"))
                first_time = float(processed.time)
            last_time = float(processed.time)
            writer.writerow([n_output, i, processed.time, processed.step])
            n_output += 1
        if not n_output:
            raise ValueError("No output frames")
        try:
            output.read()
        except StopIteration:
            pass
        else:
            raise ValueError("Processed trajectory has extra frames")
    return {"input_frames": n_input, "output_frames": n_output,
            "output_atoms": len(atom_indices), "first_time_ps": first_time,
            "last_time_ps": last_time, "stride_verified": True,
            "unchanged_coordinates_verified": no_transform}


def _fingerprint(path):
    stat = path.stat()
    return {"path": str(path), "size_bytes": stat.st_size, "mtime_ns": stat.st_mtime_ns}


def process_trajectory(instruction_file: str | Path, *, dry_run: bool | None = None) -> dict:
    """Load, validate and run once; a dry run reads only metadata/first frame.

    Results are assembled in a staging directory and published locally only after
    streaming verification. Explicit overwrite archives the previous owned result.
    Failures retain logs in the staging directory and leave previous results intact.
    """
    cfg = load_config(instruction_file)
    if dry_run is not None:
        if type(dry_run) is not bool:
            raise ValueError("dry_run override must be a boolean")
        cfg = replace(cfg, dry_run=dry_run)
    universe, groups, executable, validation = preflight(cfg)
    summary = {"workflow": WORKFLOW, "settings": resolved_settings(cfg),
               "validation": validation, "plan": command_plan(cfg, executable),
               "status": "dry_run" if cfg.dry_run else "running",
               "visual_inspection_performed": False}
    if cfg.dry_run:
        return summary
    protected = (cfg.input_trajectory, cfg.structure, cfg.index, cfg.instruction_file)
    fingerprints = [_fingerprint(path) for path in protected]
    cfg.output_dir.parent.mkdir(parents=True, exist_ok=True)
    lock = cfg.output_dir.parent / ("." + cfg.output_dir.name + ".lock")
    # Exclusive sibling lock prevents two Run All / CLI calls replacing each other.
    with lock.open("x"):
        pass
    stage = None
    try:
        check_output_safety(cfg)
        stage = Path(tempfile.mkdtemp(prefix="." + cfg.output_dir.name + "-", dir=cfg.output_dir.parent))
        (stage / "settings.yaml").write_text(yaml.safe_dump(resolved_settings(cfg), sort_keys=False))
        shutil.copyfile(cfg.instruction_file, stage / "instruction_used.txt")
        summary["inputs"] = fingerprints
        summary["instruction_sha256"] = hashlib.sha256(cfg.instruction_file.read_bytes()).hexdigest()
        selected = {"all_atoms": tuple(range(1, len(universe.atoms) + 1)),
                    "output": groups[cfg.output_group]}
        if cfg.center:
            selected["center"] = groups[cfg.center_group]
        if cfg.fit != "none":
            selected["fit"] = groups[cfg.fit_group]
        write_index(GromacsIndex(selected), stage / "selections.ndx")
        summary["started_utc"] = datetime.now(timezone.utc).isoformat()
        (stage / "summary.json").write_text(json.dumps(summary, indent=2))
        runner = _logged_runner(stage)
        for operation in command_plan(cfg, executable, stage):
            run_trjconv(**operation, runner=runner)
        summary["processing"] = _verify_and_view(cfg, stage, universe, groups)
        if [_fingerprint(path) for path in protected] != fingerprints:
            raise RuntimeError("An input changed during processing; results have not been installed")
        if cfg.prepare_vmd:
            (stage / "view.vmd").write_text(
                '# Run: vmd -e /absolute/path/to/view.vmd\n'
                'set here [file dirname [file normalize [info script]]]\n'
                'mol new [file join $here viewing.gro] type gro waitfor all\n'
                'mol addfile [file join $here processed.xtc] type xtc waitfor all\n'
                '# The GRO supplies topology and duplicates the first XTC frame.\n'
                'animate delete beg 0 end 0 top\n'
                'mol modselect 0 top all\n'
                'mol modstyle 0 top Lines 1.0\n'
                'display resetview\n')
        summary["status"] = "completed"
        summary["completed_utc"] = datetime.now(timezone.utc).isoformat()
        summary["files"] = sorted(p.name for p in stage.iterdir())
        archive = None
        if cfg.output_dir.exists():
            check_output_safety(cfg)
            archive = cfg.output_dir.with_name(cfg.output_dir.name + ".backup-" + uuid.uuid4().hex[:12])
            summary["previous_output_archive"] = str(archive)
        (stage / "summary.json").write_text(json.dumps(summary, indent=2))
        if archive:
            cfg.output_dir.rename(archive)
        try:
            stage.rename(cfg.output_dir)
        except OSError:
            if archive and not cfg.output_dir.exists():
                archive.rename(cfg.output_dir)
            raise
        return summary
    except Exception as exc:
        if stage is not None and stage.exists():
            summary.update(status="failed", error=str(exc))
            (stage / "summary.json").write_text(json.dumps(summary, indent=2))
            raise RuntimeError(f"Processing failed; diagnostic files preserved in {stage}: {exc}") from exc
        raise
    finally:
        lock.unlink()


def main(argv=None):
    """CLI entry point shared with the notebook."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("instruction_file", type=Path)
    parser.add_argument("--dry-run", action="store_true", help="Read-only validation and plan; overrides YAML")
    args = parser.parse_args(argv)
    try:
        result = process_trajectory(args.instruction_file, dry_run=True if args.dry_run else None)
    except (OSError, ValueError, RuntimeError, yaml.YAMLError) as exc:
        parser.exit(1, f"Error: {exc}\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
