"""Known-coordinate checks independent of the user's simulation files."""

from dataclasses import replace
from itertools import product
from pathlib import Path

import numpy as np
import pytest

mda = pytest.importorskip("MDAnalysis")

from iphasimulator.analysis_contacts import (
    ContactConfig, ContactResult, calculate_distances, choose_frames, contact_occupancy,
    heavy_atom_mask, inspect_trajectory, load_config, load_distances,
    minimum_atom_distances, open_universe, plot_contacts, residue_minima,
    run_contacts, save_distances, select_atoms, summarise, valid_box,
)


BOX = [20, 20, 20, 90, 90, 90]


def small_universe():
    # Nonconsecutive numbers and duplicate resid values across segments expose
    # matrix-index labels and ambiguous joins. Excluded atoms sit closest to PHA.
    names = ["N", "CA", "C", "O", "CB", "1HB", "OT1", "OT2", "OXT", "OC1", "OC2",
             "N", "CA", "C", "O", "HA2", "N", "CA", "CB", "C1", "H1"]
    residue_index = [0] * 11 + [1] * 5 + [2] * 3 + [3] * 2
    u = mda.Universe.empty(len(names), n_residues=4, n_segments=3,
                          atom_resindex=residue_index, residue_segindex=[0, 0, 1, 2], trajectory=True)
    for attr, values in {
        "names": names, "resnames": ["ALA", "GLY", "ALA", "PHA"], "resids": [42, 88, 42, 901],
        "segids": ["ENZA", "ENZB", "POLY"], "chainIDs": ["A"] * 16 + ["B"] * 3 + ["P"] * 2,
        "icodes": ["", "A", "", ""],
        "elements": ["H" if n.lstrip("0123456789").startswith("H") else n[0] for n in names],
    }.items():
        u.add_TopologyAttr(attr, values)
    u.add_TopologyAttr("masses", [1.008 if e == "H" else 12.0 for e in u.atoms.elements])
    u.atoms.positions = np.array([[0.1, 0, 0]] * len(names))
    u.atoms[4].position = [5, 0, 0]
    u.atoms[18].position = [8, 0, 0]
    u.atoms[19].position = [0, 0, 0]
    u.atoms[20].position = [5, 0, 0]  # PHA hydrogen must not make CB distance zero.
    u.dimensions = BOX
    return u


def config(**kwargs):
    return ContactConfig(Path("t.tpr"), Path("t.xtc"), Path("output"), "resname PHA", **kwargs)


def test_minimum_distances_and_block_boundaries():
    # Known 3-4-5 geometry; whole-PHA minimum includes the second ligand atom.
    reference = [[0, 0, 0], [0, 3, 0], [15, 10, 10]]
    pha = [[4, 0, 0], [14, 10, 10]]
    for size in (1, 2, 100):
        np.testing.assert_allclose(minimum_atom_distances(reference, pha, BOX, size), [4, 5, 1], atol=1e-6)
    np.testing.assert_allclose(residue_minima([4, 5, 1], [0, 0, 2], 4), [4, np.nan, 1, np.nan], equal_nan=True)


def test_periodic_minimum_image_same_frame_box():
    a, b = [[0.2, 0, 0]], [[9.8, 0, 0]]
    assert minimum_atom_distances(a, b, [10, 10, 10, 90, 90, 90])[0] == pytest.approx(0.4, abs=1e-6)
    assert minimum_atom_distances(a, b, BOX)[0] == pytest.approx(9.6, abs=1e-6)


def test_triclinic_periodic_boundary_against_explicit_images():
    # Independent lattice geometry, then explicit image enumeration.
    matrix = np.array([[10., 0, 0], [5., np.sqrt(75), 0], [0, 0, 10.]])
    a = np.array([[0.05, 0.05, 0.2]]) @ matrix
    b = np.array([[0.95, 0.95, 0.2]]) @ matrix
    images = np.array(list(product(range(-2, 3), repeat=3))) @ matrix
    expected = np.linalg.norm(a[:, None] - (b + images)[None], axis=-1).min()
    assert minimum_atom_distances(a, b, [10, 10, 10, 90, 90, 60])[0] == pytest.approx(expected, abs=2e-6)


@pytest.mark.parametrize("box", [None, [0, 10, 10, 90, 90, 90], [10, 10, 10, 0, 90, 90],
                                   [10, 10, 10, 170, 10, 10], [10, 10, np.nan, 90, 90, 90]])
def test_invalid_periodic_boxes_rejected(box):
    with pytest.raises(ValueError, match="box"):
        valid_box(box)


def test_atom_exclusions_glycine_and_unambiguous_identity():
    u = small_universe()
    selections = select_atoms(u, "protein", "resname PHA")
    np.testing.assert_array_equal(selections.pha.indices, [19])
    np.testing.assert_array_equal(selections.counts["sidechain_heavy"], [1, 0, 1])
    assert list(selections.heavy[selections.mode_masks["sidechain_heavy"]].names) == ["CB", "CB"]
    matrices = calculate_distances(u, selections, [0])
    np.testing.assert_allclose(matrices["all_heavy"][:, 0], [0.1, 0.1, 0.1], atol=1e-6)
    np.testing.assert_allclose(matrices["sidechain_heavy"][:, 0], [5, np.nan, 8], atol=1e-6)
    assert [r["resid"] for r in selections.residues] == [42, 88, 42]
    assert [r["resindex"] for r in selections.residues] == [0, 1, 2]
    assert [r["chain_ids"] for r in selections.residues] == ["A", "A", "B"]
    assert selections.residues[1]["icode"] == "A"
    assert selections.residues[0]["label"] != selections.residues[2]["label"]


def test_narrow_base_selection_never_expands_back_to_residue_atoms():
    u = small_universe()
    selections = select_atoms(u, "protein and name CB", "resname PHA")
    matrices = calculate_distances(u, selections, [0])
    np.testing.assert_allclose(matrices["all_heavy"][:, 0], [5, 8], atol=1e-6)


def test_hydrogen_mass_and_number_prefixed_name_fallbacks():
    u = mda.Universe.empty(7)
    u.add_TopologyAttr("names", ["1HB", "2HD1", "D1", "T1", "CA", "ND1", "CB"])
    np.testing.assert_array_equal(heavy_atom_mask(u.atoms), [False, False, False, False, True, True, True])
    u.add_TopologyAttr("masses", [1, 1, 2, 3, 12, 14, 0])
    np.testing.assert_array_equal(heavy_atom_mask(u.atoms), [False, False, False, False, True, True, False])


def test_occupancy_strict_threshold_one_event_per_frame_and_nan_denominator():
    d = [[4, 4.5, 5, 3.9], [np.nan] * 4, [3, 3, 3, 3], [1, np.nan, 1, 1]]
    np.testing.assert_allclose(contact_occupancy(d, 4.5), [50, np.nan, 100, np.nan])
    np.testing.assert_allclose(contact_occupancy(d, 4), [25, np.nan, 100, np.nan])
    np.testing.assert_allclose(contact_occupancy(d, 5), [75, np.nan, 100, np.nan])
    with pytest.raises(ValueError):
        contact_occupancy(np.empty((2, 0)), 4.5)


def test_sampling_window_preview_and_no_implicit_equilibration():
    times = np.arange(101) * 0.1
    indices, report = choose_frames(times, config(preview_frames=3))
    assert list(indices) == [0, 50, 100]
    assert report["n_analysed_frames"] == 3
    assert report["actual_window_ns"] == [0, 10]
    indices, report = choose_frames(times, config(start_ns=2, end_ns=3, sample_interval_ns=0.2, preview_frames=None))
    assert list(indices) == [20, 22, 24, 26, 28, 30]
    assert report["kind"] == "full"
    assert report["actual_interval"]["median_ns"] == pytest.approx(0.2)
    # Bounds are explicit; grid is anchored at first stored frame in window.
    indices, _ = choose_frames(times, config(start_ns=2.01, end_ns=2.51, sample_interval_ns=0.2, preview_frames=None))
    assert list(indices) == [21, 23, 25]


def test_irregular_sampling_is_reported_and_never_silently_rounded():
    indices, report = choose_frames([0, 1, 3], config(preview_frames=None))
    assert list(indices) == [0, 1, 2]
    assert report["actual_interval"]["uniform"] is False
    for times, kwargs in [([0, 1, 3], {"sample_interval_ns": 1}),
                          ([0, 1, 2], {"sample_interval_ns": 1.5}),
                          ([0, 1, 1], {}), ([0, 1, 2], {"end_ns": 3}),
                          ([0, 1, 2], {"start_ns": 0.2, "end_ns": 0.3})]:
        with pytest.raises(ValueError):
            choose_frames(times, config(**kwargs))


def test_inspection_checks_every_frame_and_nan_statistics_roundtrip(tmp_path):
    u = small_universe()
    coords = np.repeat(u.atoms.positions[None], 3, axis=0)
    u.load_new(coords, format=mda.coordinates.memory.MemoryReader,
               dimensions=np.tile(BOX, (3, 1)), dt=100)
    info = inspect_trajectory(u)
    np.testing.assert_allclose(info["times_ns"], [0, 0.1, 0.2])
    assert info["all_frame_boxes_valid"]
    selections = select_atoms(u, "protein", "resname PHA")
    result = ContactResult(info["times_ns"], np.arange(3), info["boxes_A_degrees"], selections.residues,
                           selections.counts, calculate_distances(u, selections, [0, 1, 2]),
                           {"sampling": {"kind": "preview"}, "config": {"label": "Known coordinates"}})
    path = tmp_path / "distances.npz"
    save_distances(result, path)
    loaded = load_distances(path)
    np.testing.assert_allclose(loaded.distances_A["sidechain_heavy"], result.distances_A["sidechain_heavy"])
    table = summarise(loaded)
    gly = table[(table["mode"] == "sidechain_heavy") & (table["resname"] == "GLY")].iloc[0]
    assert gly["selected_atom_count"] == 0 and gly["n_analysed_frames"] == 3 and gly["n_valid_frames"] == 0
    assert np.isnan(gly["mean_min_distance_A"]) and np.isnan(gly["occupancy_lt_4.5_A_pct"])
    assert len(plot_contacts(loaded, tmp_path / "plots")) == 4
    with pytest.raises(FileExistsError):
        save_distances(result, path)
    u.trajectory[1]
    u.dimensions = [0, 0, 0, 90, 90, 90]
    with pytest.raises(ValueError, match="Frame 1"):
        inspect_trajectory(u)


def test_full_workflow_input_preservation_output_isolation_and_atom_mismatch(tmp_path):
    u = small_universe()
    topology, trajectory = tmp_path / "test.pdb", tmp_path / "test.xtc"
    with mda.Writer(str(topology), n_atoms=len(u.atoms)) as writer:
        writer.write(u)
    with mda.Writer(str(trajectory), n_atoms=len(u.atoms)) as writer:
        for i in range(3):
            u.trajectory.ts.time = i * 100
            writer.write(u)
    before = {p.name: (p.stat().st_size, p.stat().st_mtime_ns) for p in tmp_path.iterdir()}
    cfg = ContactConfig(topology, trajectory, tmp_path / "output", "resname PHA", preview_frames=None)
    first = run_contacts(cfg, progress=None)
    second = run_contacts(replace(cfg, preview_frames=2), progress=None)
    assert first != second
    assert load_distances(first / "distances.npz").times_ns.tolist() == [0, 0.1, 0.2]
    assert load_distances(second / "distances.npz").times_ns.tolist() == [0, 0.2]
    assert {p.name for p in tmp_path.iterdir()} == {*before, "output"}
    for name, fingerprint in before.items():
        assert (tmp_path / name).stat().st_size == fingerprint[0]
        assert (tmp_path / name).stat().st_mtime_ns == fingerprint[1]
    wrong = tmp_path / "wrong.pdb"
    with mda.Writer(str(wrong), n_atoms=2) as writer:
        writer.write(u.atoms[:2])
    with pytest.raises(ValueError):
        with open_universe(wrong, trajectory):
            pass


def test_config_relative_paths_and_required_selection(tmp_path):
    path = tmp_path / "config.yaml"
    path.write_text("topology: test.tpr\ntrajectory: test.xtc\noutput_root: output\npha_selection: resname PHA\n")
    cfg = load_config(path)
    assert cfg.topology == tmp_path / "test.tpr"
    assert cfg.output_root == tmp_path / "output"
    with pytest.raises(ValueError, match="overlap"):
        select_atoms(small_universe(), "all", "resname PHA")
    with pytest.raises(ValueError):
        replace(cfg, primary_cutoff_A=float("nan")).validate()
