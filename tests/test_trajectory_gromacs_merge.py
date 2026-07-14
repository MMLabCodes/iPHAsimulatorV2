from io import StringIO
from pathlib import Path
from types import SimpleNamespace

import pytest

from iphasimulator.trajectory_gromacs_merge import (
    build_argument_parser,
    discover_gromacs_outputs,
    energy_output_filename,
    maximum_energy_part,
    maximum_trajectory_part,
    merge_simulation_outputs,
    trajectory_output_filename,
)


def _write(path: Path, content: str = "raw") -> Path:
    path.write_text(content)
    return path


def test_discovery_allows_missing_part0001(tmp_path):
    initial = _write(tmp_path / "step7_production.xtc")
    part2 = _write(tmp_path / "step8_production_2us.part0002.xtc")
    part3 = _write(tmp_path / "step8_production_2us.part0003.xtc")

    discovered = discover_gromacs_outputs(tmp_path)

    assert discovered.xtc_files == (initial, part2, part3)


def test_discovery_sorts_parts_numerically(tmp_path):
    part10 = _write(tmp_path / "step8_production_2us.part0010.xtc")
    part2 = _write(tmp_path / "step8_production_2us.part0002.xtc")
    part9 = _write(tmp_path / "step8_production_2us.part0009.xtc")

    discovered = discover_gromacs_outputs(tmp_path)

    assert discovered.xtc_files == (part2, part9, part10)


def test_trajectory_output_name_uses_highest_numeric_part(tmp_path):
    part2 = tmp_path / "step8_production_2us.part0002.xtc"
    part9 = tmp_path / "step8_production_2us.part0009.xtc"
    part10 = tmp_path / "step8_production_2us.part0010.xtc"

    assert maximum_trajectory_part((part2, part9, part10)) == 10
    assert trajectory_output_filename((part2, part9, part10)) == (
        "production_combined_010.xtc"
    )


def test_trajectory_output_name_handles_unnumbered_continuation_and_step7(tmp_path):
    initial = tmp_path / "step7_production.xtc"
    continuation = tmp_path / "step8_production_2us.xtc"

    assert trajectory_output_filename((initial,)) == "production_combined_000.xtc"
    assert trajectory_output_filename((initial, continuation)) == (
        "production_combined_001.xtc"
    )


def test_energy_output_name_uses_highest_edr_part(tmp_path):
    initial = tmp_path / "step7_production.edr"
    part2 = tmp_path / "step8_production_2us.part0002.edr"
    part10 = tmp_path / "step8_production_2us.part0010.edr"

    assert maximum_energy_part((initial, part2, part10)) == 10
    assert energy_output_filename((initial, part2, part10)) == (
        "production_combined_010.edr"
    )


def test_discovery_excludes_existing_merged_files(tmp_path):
    raw_xtc = _write(tmp_path / "step7_production.xtc")
    raw_edr = _write(tmp_path / "step7_production.edr")
    _write(tmp_path / "production_combined.xtc")
    _write(tmp_path / "production_combined.edr")
    _write(tmp_path / "step7_step8_combined.xtc")
    _write(tmp_path / "step7_step8_combined.edr")
    _write(tmp_path / "step8_production_2us_combined.xtc")

    discovered = discover_gromacs_outputs(tmp_path)

    assert discovered.xtc_files == (raw_xtc,)
    assert discovered.edr_files == (raw_edr,)


def test_discovery_excludes_gromacs_backup_files(tmp_path):
    raw = _write(tmp_path / "step8_production_2us.part0002.xtc")
    _write(tmp_path / "#step7_production.xtc#")
    _write(tmp_path / "#step8_production_2us.part0002.xtc#")
    _write(tmp_path / "#step8_production_2us.part0002.edr#")

    discovered = discover_gromacs_outputs(tmp_path)

    assert discovered.xtc_files == (raw,)
    assert discovered.edr_files == ()


def test_xtc_and_edr_discovery_is_independent(tmp_path):
    xtc_initial = _write(tmp_path / "step7_production.xtc")
    xtc_part3 = _write(tmp_path / "step8_production_2us.part0003.xtc")
    edr_unnumbered = _write(tmp_path / "step8_production_2us.edr")
    edr_part2 = _write(tmp_path / "step8_production_2us.part0002.edr")

    discovered = discover_gromacs_outputs(tmp_path)

    assert discovered.xtc_files == (xtc_initial, xtc_part3)
    assert discovered.edr_files == (edr_unnumbered, edr_part2)


def test_existing_output_is_protected_before_any_command(tmp_path):
    _write(tmp_path / "step7_production.xtc")
    _write(tmp_path / "production_combined_000.xtc", "existing output")
    calls = []

    def fake_runner(command, **kwargs):
        calls.append((command, kwargs))
        raise AssertionError("No GROMACS command should run")

    with pytest.raises(FileExistsError, match="--overwrite"):
        merge_simulation_outputs(
            tmp_path,
            trajectory_only=True,
            runner=fake_runner,
            stream=StringIO(),
        )

    assert calls == []


def test_continuation_xtc_without_continuation_edr_skips_energy(tmp_path):
    _write(tmp_path / "step7_production.xtc")
    _write(tmp_path / "step8_production_2us.part0002.xtc")
    _write(tmp_path / "step7_production.edr")
    calls = []
    output = StringIO()

    def fake_runner(command, **kwargs):
        calls.append((command, kwargs))
        if command[1] == "trjcat":
            Path(command[command.index("-o") + 1]).write_text("merged xtc")
        return SimpleNamespace(
            stdout="Reading frame 0 time 0\nLast frame 10 time 10\n",
            stderr="",
        )

    result = merge_simulation_outputs(tmp_path, runner=fake_runner, stream=output)

    assert result.trajectory_merge is not None
    assert result.energy_merge is None
    assert "energy merging was skipped" in result.energy_skipped_reason
    assert "energy merging was skipped" in output.getvalue()
    assert not any(command[1] == "eneconv" for command, _ in calls)


def test_mocked_trjcat_and_eneconv_use_one_checked_command_each(tmp_path):
    xtc_files = (
        _write(tmp_path / "step7_production.xtc", "xtc initial"),
        _write(tmp_path / "step8_production_2us.xtc", "xtc continuation"),
        _write(tmp_path / "step8_production_2us.part0002.xtc", "xtc part2"),
    )
    edr_files = (
        _write(tmp_path / "step7_production.edr", "edr initial"),
        _write(tmp_path / "step8_production_2us.edr", "edr continuation"),
        _write(tmp_path / "step8_production_2us.part0002.edr", "edr part2"),
    )
    original_contents = {
        path: path.read_text() for path in (*xtc_files, *edr_files)
    }
    calls = []

    def fake_runner(command, **kwargs):
        calls.append((command, kwargs))
        assert kwargs["check"] is True
        assert kwargs.get("shell", False) is False
        if command[1] in {"trjcat", "eneconv"}:
            Path(command[command.index("-o") + 1]).write_text("merged")
        return SimpleNamespace(
            stdout="Reading frame 0 time 0\nLast frame 100 time 100\n",
            stderr="",
        )

    result = merge_simulation_outputs(tmp_path, runner=fake_runner, stream=StringIO())

    trjcat_calls = [command for command, _ in calls if command[1] == "trjcat"]
    eneconv_calls = [command for command, _ in calls if command[1] == "eneconv"]
    assert len(trjcat_calls) == 1
    assert len(eneconv_calls) == 1
    assert trjcat_calls[0] == [
        "gmx",
        "trjcat",
        "-f",
        *(str(path) for path in xtc_files),
        "-o",
        str(tmp_path / "production_combined_002.xtc"),
    ]
    assert eneconv_calls[0] == [
        "gmx",
        "eneconv",
        "-f",
        *(str(path) for path in edr_files),
        "-o",
        str(tmp_path / "production_combined_002.edr"),
    ]
    assert "-settime" not in trjcat_calls[0]
    assert "-settime" not in eneconv_calls[0]
    assert len(result.input_checks) == 6
    assert len(result.output_checks) == 2
    assert all(path.read_text() == text for path, text in original_contents.items())


def test_dry_run_prints_commands_without_running_subprocess(tmp_path):
    _write(tmp_path / "step7_production.xtc")
    _write(tmp_path / "step8_production_2us.part0002.xtc")
    calls = []
    output = StringIO()

    def fake_runner(command, **kwargs):
        calls.append((command, kwargs))
        raise AssertionError("Dry run must not execute GROMACS")

    result = merge_simulation_outputs(
        tmp_path,
        dry_run=True,
        trajectory_only=True,
        runner=fake_runner,
        stream=output,
    )

    assert result.dry_run
    assert calls == []
    assert "gmx trjcat" in output.getvalue()
    assert "production_combined_002.xtc" in output.getvalue()
    assert "-settime" not in output.getvalue()


def test_cli_defaults_to_current_directory():
    arguments = build_argument_parser().parse_args([])

    assert arguments.simulation_directory == Path(".")
