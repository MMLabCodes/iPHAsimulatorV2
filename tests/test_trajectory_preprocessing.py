from pathlib import Path
from types import SimpleNamespace

import pytest

from iphasimulator.trajectory import (
    center_and_compact_wrap,
    ensure_center_index,
    fit_trajectory,
    preprocess_gromacs_trajectory,
    read_index,
)
from iphasimulator.trajectory.frame_extraction import extract_frame


def _write_index(path: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "[ System ]",
                "1 2 3 4 5 6",
                "",
                "[ PHA ]",
                "1 2 3",
                "",
                "[ SOL ]",
                "4 5 6",
                "",
            ]
        )
    )


def test_ensure_center_index_creates_center_from_polymer_group(tmp_path):
    source = tmp_path / "index.ndx"
    output = tmp_path / "center.ndx"
    _write_index(source)

    result = ensure_center_index(source, output, workflow_type="polymer")

    assert result.index_path == output
    assert result.created
    assert result.source_groups == ("PHA",)
    parsed = read_index(output)
    assert parsed.group("center") == (1, 2, 3)
    assert parsed.group("System") == (1, 2, 3, 4, 5, 6)


def test_ensure_center_index_reuses_existing_center(tmp_path):
    source = tmp_path / "index.ndx"
    source.write_text("[ System ]\n1 2 3\n\n[ center ]\n2 3\n")

    result = ensure_center_index(source, source, workflow_type="polymer")

    assert not result.created
    assert result.reused_existing_center
    assert read_index(source).group("center") == (2, 3)


def test_ensure_center_index_merges_custom_source_groups(tmp_path):
    source = tmp_path / "index.ndx"
    source.write_text(
        "[ System ]\n1 2 3 4\n\n[ Protein ]\n1 3\n\n[ PHA ]\n2 4\n"
    )

    ensure_center_index(
        source,
        tmp_path / "center.ndx",
        source_groups=("Protein", "PHA"),
    )

    assert read_index(tmp_path / "center.ndx").group("center") == (1, 2, 3, 4)


def test_ensure_center_index_errors_when_source_group_missing(tmp_path):
    source = tmp_path / "index.ndx"
    source.write_text("[ System ]\n1 2 3\n")

    with pytest.raises(ValueError, match="PHA"):
        ensure_center_index(source, tmp_path / "center.ndx", workflow_type="polymer")


def test_center_and_fit_use_center_then_system_selections(tmp_path):
    calls = []

    def fake_runner(command, **kwargs):
        calls.append((command, kwargs))
        Path(command[command.index("-o") + 1]).write_text("xtc")
        return SimpleNamespace(returncode=0, stdout="ok", stderr="")

    center_and_compact_wrap(
        trajectory="step7_production.xtc",
        structure="step7_production.tpr",
        index="center.ndx",
        output=tmp_path / "step7_centered.xtc",
        runner=fake_runner,
    )
    fit_trajectory(
        trajectory=tmp_path / "step7_centered.xtc",
        structure="step7_production.tpr",
        index="center.ndx",
        output=tmp_path / "step7_fitted.xtc",
        runner=fake_runner,
    )

    center_command, center_kwargs = calls[0]
    assert center_command[:2] == ["gmx", "trjconv"]
    assert center_command[center_command.index("-pbc") + 1] == "mol"
    assert center_command[center_command.index("-ur") + 1] == "compact"
    assert "-center" in center_command
    assert center_kwargs["input"] == "center\nSystem\n"

    fit_command, fit_kwargs = calls[1]
    assert fit_command[fit_command.index("-fit") + 1] == "rot+trans"
    assert fit_kwargs["input"] == "center\nSystem\n"


def test_extract_frame_uses_output_group_only(tmp_path):
    calls = []

    def fake_runner(command, **kwargs):
        calls.append((command, kwargs))
        return SimpleNamespace(returncode=0, stdout="ok", stderr="")

    extract_frame(
        trajectory="step7_fitted.xtc",
        structure="step7_production.tpr",
        output=tmp_path / "representative.gro",
        index="center.ndx",
        time_ps=1000,
        runner=fake_runner,
    )

    command, kwargs = calls[0]
    assert command[command.index("-dump") + 1] == "1000"
    assert kwargs["input"] == "System\n"


def test_preprocess_gromacs_trajectory_dry_run_builds_expected_paths(tmp_path):
    _write_index(tmp_path / "index.ndx")

    outputs = preprocess_gromacs_trajectory(tmp_path, dry_run=True)

    assert outputs.raw_dir == tmp_path / "raw"
    assert outputs.processed_dir == tmp_path / "processed"
    assert outputs.analysis_ready_dir == tmp_path / "analysis_ready"
    assert outputs.center_index.index_path == tmp_path / "center.ndx"
    assert outputs.centered_trajectory_path == tmp_path / "processed" / "step7_centered.xtc"
    assert outputs.fitted_trajectory_path == tmp_path / "analysis_ready" / "step7_fitted.xtc"
    assert outputs.analysis_trajectory_path == tmp_path / "analysis_ready" / "step7_fitted.xtc"
    assert read_index(tmp_path / "center.ndx").group("center") == (1, 2, 3)


def test_preprocess_gromacs_trajectory_reports_missing_inputs(tmp_path):
    _write_index(tmp_path / "index.ndx")

    with pytest.raises(FileNotFoundError, match="step7_production.xtc"):
        preprocess_gromacs_trajectory(tmp_path)
