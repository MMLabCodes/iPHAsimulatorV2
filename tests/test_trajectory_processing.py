"""Focused configuration and real, small GROMACS trajectory regression tests."""

from dataclasses import replace
import json
from pathlib import Path
import shutil

import pytest
import yaml

from iphasimulator.trajectory_processing import (
    WORKFLOW, check_output_safety, command_plan, load_config, process_trajectory,
)


def config_file(tmp_path, **changes):
    data = dict(input_trajectory="input.xtc", structure="input.gro", index="input.ndx",
                output_dir="processed", stride=3, output_group="SYSTEM")
    data.update(changes)
    path = tmp_path / "instruction.txt"
    path.write_text(yaml.safe_dump(data))
    return path


@pytest.mark.parametrize("changes", [
    {"strdie": 3}, {"stride": 0}, {"stride": -1}, {"stride": True}, {"stride": 2.5},
    {"center": "false"}, {"center": True}, {"fit": "auto"}, {"fit": "rot+trans"},
    {"pbc": "auto"}, {"pbc": "nojump"}, {"prepare_vmd": 1}, {"overwrite": "yes"},
    {"dry_run": "false"}, {"schema_version": True}, {"custom_groups": []},
    {"output_group": 2}, {"input_trajectory": ""}, {"gmx": None},
])
def test_rejects_invalid_settings(tmp_path, changes):
    with pytest.raises(ValueError):
        load_config(config_file(tmp_path, **changes))


def test_duplicate_and_nonmapping_yaml(tmp_path):
    path = config_file(tmp_path)
    path.write_text(path.read_text() + "stride: 9\n")
    with pytest.raises(ValueError, match="unique"):
        load_config(path)
    path.write_text("- an old instruction\n")
    with pytest.raises(ValueError, match="mapping"):
        load_config(path)


def test_paths_follow_instruction_directory(tmp_path, monkeypatch):
    analysis = tmp_path / "analysis"
    analysis.mkdir()
    path = config_file(analysis, input_trajectory="../raw.xtc")
    monkeypatch.chdir(tmp_path.parent)
    cfg = load_config(path)
    assert cfg.input_trajectory == tmp_path / "raw.xtc"
    assert cfg.output_dir == analysis / "processed"


def test_command_construction_and_separate_fit(tmp_path):
    cfg = load_config(config_file(tmp_path))
    plan = command_plan(cfg, "/bin/gmx")
    assert len(plan) == 1
    assert plan[0]["trjconv_args"] == ["-skip", "3", "-pbc", "none"]
    assert plan[0]["selections"] == ["output"]
    cfg = replace(cfg, center=True, center_group="SOLU", fit="rot+trans", fit_group="CA", pbc="mol")
    plan = command_plan(cfg, "/bin/gmx")
    assert len(plan) == 2
    assert plan[0]["selections"] == ["center", "all_atoms"]
    assert plan[0]["trjconv_args"] == ["-skip", "3", "-pbc", "mol", "-center"]
    assert plan[1]["selections"] == ["fit", "output"]
    assert plan[1]["trjconv_args"] == ["-fit", "rot+trans"]
    assert plan[1]["trajectory"] == plan[0]["output"]


def test_overwrite_and_raw_input_protection(tmp_path):
    cfg = load_config(config_file(tmp_path))
    with pytest.raises(ValueError, match="protected input"):
        check_output_safety(replace(cfg, output_dir=tmp_path))
    cfg.output_dir.mkdir()
    with pytest.raises(FileExistsError):
        check_output_safety(cfg)
    with pytest.raises(ValueError, match="created by"):
        check_output_safety(replace(cfg, overwrite=True))
    (cfg.output_dir / "summary.json").write_text(json.dumps({"workflow": WORKFLOW}))
    check_output_safety(replace(cfg, overwrite=True))


@pytest.fixture
def trajectory(tmp_path):
    mda = pytest.importorskip("MDAnalysis")
    np = pytest.importorskip("numpy")
    if not shutil.which("gmx"):
        pytest.skip("GROMACS is required for the real streaming integration tests")
    from MDAnalysis.lib.formats.libmdaxdr import XTCFile
    u = mda.Universe.empty(4, n_residues=1, atom_resindex=[0, 0, 0, 0], trajectory=True)
    u.add_TopologyAttr("names", ["CA", "N", "C", "O"])
    u.add_TopologyAttr("resnames", ["ALA"])
    u.add_TopologyAttr("resids", [1])
    u.atoms.positions = [[10, 10, 10], [12, 10, 10], [10, 13, 10], [10, 10, 14]]
    u.dimensions = [40, 40, 40, 90, 90, 90]
    u.atoms.write(str(tmp_path / "input.gro"))
    with XTCFile(str(tmp_path / "input.xtc"), "w") as writer:
        for i in range(8):
            writer.write(np.asarray(u.atoms.positions / 10 + i * .03, dtype=np.float32),
                         np.eye(3, dtype=np.float32) * 4, i * 50, 7 + i * 2, 1000)
    (tmp_path / "input.ndx").write_text("[ SYSTEM ]\n1 2 3 4\n[ SOLU ]\n1 2 3\n[ subset ]\n3 1\n")
    return config_file(tmp_path)


def test_dry_run_no_writes_and_missing_tool(trajectory):
    root = trajectory.parent
    before = {p: (p.stat().st_size, p.stat().st_mtime_ns) for p in root.rglob("*")}
    result = process_trajectory(trajectory, dry_run=True)
    assert result["status"] == "dry_run"
    assert {p: (p.stat().st_size, p.stat().st_mtime_ns) for p in root.rglob("*")} == before
    data = yaml.safe_load(trajectory.read_text())
    data["gmx"] = "definitely_missing_gmx"
    trajectory.write_text(yaml.safe_dump(data))
    with pytest.raises(FileNotFoundError, match="executable"):
        process_trajectory(trajectory, dry_run=True)


def test_stride_subset_viewing_and_overwrite_archive(trajectory):
    import MDAnalysis as mda
    import numpy as np
    from MDAnalysis.lib.formats.libmdaxdr import XTCFile
    data = yaml.safe_load(trajectory.read_text())
    data["output_group"] = "subset"
    trajectory.write_text(yaml.safe_dump(data))
    result = process_trajectory(trajectory)
    assert result["processing"]["output_frames"] == 3
    assert result["processing"]["input_frames"] == 8
    output = trajectory.parent / "processed"
    with XTCFile(str(output / "processed.xtc"), "r") as f:
        frames = [(x.time, x.x.copy()) for x in f]
    assert [t for t, _ in frames] == [7, 13, 19]
    gro = mda.Universe(str(output / "viewing.gro"))
    assert list(gro.atoms.names) == ["C", "CA"]
    np.testing.assert_allclose(gro.atoms.positions / 10, frames[0][1], atol=.0002)
    assert "[file join $here processed.xtc]" in (output / "view.vmd").read_text()
    assert not result["visual_inspection_performed"]
    assert not list(trajectory.parent.glob(".*offset*"))
    previous = (output / "processed.xtc").read_bytes()
    with pytest.raises(FileExistsError):
        process_trajectory(trajectory)
    data["overwrite"] = True
    trajectory.write_text(yaml.safe_dump(data))
    replacement = process_trajectory(trajectory)
    assert (Path(replacement["previous_output_archive"]) / "processed.xtc").read_bytes() == previous


def test_real_center_fit_with_subset(trajectory):
    data = yaml.safe_load(trajectory.read_text())
    data.update(center=True, center_group="SOLU", fit="rot+trans", fit_group="SOLU", output_group="subset")
    trajectory.write_text(yaml.safe_dump(data))
    result = process_trajectory(trajectory)
    assert result["processing"]["output_atoms"] == 2
    assert result["processing"]["stride_verified"]
    assert (trajectory.parent / "processed/unfitted.xtc").exists()


@pytest.mark.parametrize("indices", ["0 1", "1 1", "1 5", ""])
def test_invalid_index_rejected_before_outputs(trajectory, indices):
    (trajectory.parent / "input.ndx").write_text(f"[ SYSTEM ]\n{indices}\n")
    with pytest.raises(ValueError, match="atom indices"):
        process_trajectory(trajectory)
    assert not (trajectory.parent / "processed").exists()


def test_missing_selection_and_mismatch(trajectory):
    config_file(trajectory.parent, output_group="not_here")
    with pytest.raises(ValueError, match="Unknown group"):
        process_trajectory(trajectory)
    config_file(trajectory.parent, custom_groups={"nothing": "resname NOT_PRESENT"})
    with pytest.raises(ValueError, match="empty"):
        process_trajectory(trajectory)
    config_file(trajectory.parent)
    gro = trajectory.parent / "input.gro"
    lines = gro.read_text().splitlines()
    lines[1] = "3"
    gro.write_text("\n".join(lines[:5] + lines[-1:]) + "\n")
    (trajectory.parent / "input.ndx").write_text("[ SYSTEM ]\n1 2 3\n")
    with pytest.raises(ValueError, match="atom count mismatch"):
        process_trajectory(trajectory)


def test_failed_replacement_keeps_previous_result_and_logs(trajectory):
    from MDAnalysis.lib.formats.libmdaxdr import XTCFile
    process_trajectory(trajectory)
    root = trajectory.parent
    previous = (root / "processed/processed.xtc").read_bytes()
    data = yaml.safe_load(trajectory.read_text())
    data["overwrite"] = True
    trajectory.write_text(yaml.safe_dump(data))
    # A duplicate time beyond the first-frame preflight is found by final scan.
    with XTCFile(str(root / "input.xtc"), "r") as reader:
        frame = reader.read()
        xyz, box, step, time = frame.x.copy(), frame.box.copy(), frame.step, frame.time
    with XTCFile(str(root / "input.xtc"), "w") as writer:
        writer.write(xyz, box, step, time, 1000)
        writer.write(xyz, box, step + 50, time, 1000)
    with pytest.raises(RuntimeError, match="diagnostic files preserved"):
        process_trajectory(trajectory)
    assert (root / "processed/processed.xtc").read_bytes() == previous
    failures = list(root.glob(".processed-*/summary.json"))
    assert len(failures) == 1
    assert json.loads(failures[0].read_text())["status"] == "failed"
    assert (failures[0].parent / "command_01.stderr.log").exists()
    assert not (root / ".processed.lock").exists()
