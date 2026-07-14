"""Merge restarted GROMACS trajectory and energy outputs for one simulation."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import sys
from typing import Callable, Literal, Sequence, TextIO


Runner = Callable[..., subprocess.CompletedProcess]
OutputKind = Literal["xtc", "edr"]

INITIAL_PREFIX = "step7_production"
CONTINUATION_PREFIX = "step8_production_2us"
TRAJECTORY_OUTPUT_PREFIX = "production_combined"

_PART_PATTERN = re.compile(
    rf"^{re.escape(CONTINUATION_PREFIX)}\.part(?P<number>\d+)\."
    r"(?P<extension>xtc|edr)$"
)
_TIME_PATTERN = re.compile(
    r"\b(?:Reading|First|Last)\s+frame\s+-?\d+\s+time\s+"
    r"(?P<time>[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][-+]?\d+)?)",
    flags=re.IGNORECASE,
)


@dataclass(frozen=True)
class DiscoveredGromacsOutputs:
    """Raw XTC and EDR files discovered independently."""

    simulation_dir: Path
    xtc_files: tuple[Path, ...]
    edr_files: tuple[Path, ...]


@dataclass(frozen=True)
class GromacsCheckResult:
    """Result of one checked ``gmx check`` command."""

    kind: OutputKind
    path: Path
    command: tuple[str, ...]
    start_time_ps: float | None
    end_time_ps: float | None
    stdout: str
    stderr: str


@dataclass(frozen=True)
class GromacsMergeCommandResult:
    """Result of one checked ``gmx trjcat`` or ``gmx eneconv`` command."""

    kind: OutputKind
    command: tuple[str, ...]
    input_files: tuple[Path, ...]
    output_path: Path
    stdout: str
    stderr: str


@dataclass(frozen=True)
class GromacsMergeOutputsResult:
    """Structured discovery, command, and validation results."""

    discovered: DiscoveredGromacsOutputs
    trajectory_output: Path
    energy_output: Path
    input_checks: tuple[GromacsCheckResult, ...]
    trajectory_merge: GromacsMergeCommandResult | None
    energy_merge: GromacsMergeCommandResult | None
    output_checks: tuple[GromacsCheckResult, ...]
    energy_skipped_reason: str | None
    dry_run: bool


def _is_excluded(name: str) -> bool:
    return (
        name.startswith("step7_step8")
        or "combined" in name
        or (name.startswith("#") and name.endswith("#"))
    )


def _sort_key(path: Path, extension: OutputKind) -> tuple[int, int, str]:
    if path.name == f"{INITIAL_PREFIX}.{extension}":
        return (0, 0, path.name)
    if path.name == f"{CONTINUATION_PREFIX}.{extension}":
        return (1, 0, path.name)

    match = _PART_PATTERN.fullmatch(path.name)
    if match is None or match.group("extension") != extension:
        raise ValueError(f"Unrecognised raw {extension.upper()} file: {path}")
    return (2, int(match.group("number")), path.name)


def _discover_kind(
    simulation_dir: Path,
    extension: OutputKind,
) -> tuple[Path, ...]:
    recognised: list[Path] = []
    for path in simulation_dir.iterdir():
        if not path.is_file() or _is_excluded(path.name):
            continue
        if path.name in {
            f"{INITIAL_PREFIX}.{extension}",
            f"{CONTINUATION_PREFIX}.{extension}",
        }:
            recognised.append(path)
            continue
        match = _PART_PATTERN.fullmatch(path.name)
        if match is not None and match.group("extension") == extension:
            recognised.append(path)

    return tuple(sorted(recognised, key=lambda path: _sort_key(path, extension)))


def discover_gromacs_outputs(
    simulation_dir: str | Path,
) -> DiscoveredGromacsOutputs:
    """Discover ordered raw XTC and EDR files without inferring their times."""

    directory = Path(simulation_dir)
    if not directory.exists():
        raise FileNotFoundError(f"Simulation directory does not exist: {directory}")
    if not directory.is_dir():
        raise NotADirectoryError(f"Simulation path is not a directory: {directory}")

    return DiscoveredGromacsOutputs(
        simulation_dir=directory,
        xtc_files=_discover_kind(directory, "xtc"),
        edr_files=_discover_kind(directory, "edr"),
    )


def _maximum_part(files: Sequence[Path], extension: OutputKind) -> int:
    """Return the highest continuation number represented by raw files.

    The unnumbered ``step8_production_2us`` file is continuation 1. If only the
    initial step-7 file exists, the returned continuation number is 0.
    """

    maximum_part = 0
    for path in files:
        if path.name == f"{CONTINUATION_PREFIX}.{extension}":
            maximum_part = max(maximum_part, 1)
            continue
        match = _PART_PATTERN.fullmatch(path.name)
        if match is not None and match.group("extension") == extension:
            maximum_part = max(maximum_part, int(match.group("number")))
    return maximum_part


def maximum_trajectory_part(xtc_files: Sequence[Path]) -> int:
    """Return the highest continuation number represented by XTC files."""

    return _maximum_part(xtc_files, "xtc")


def maximum_energy_part(edr_files: Sequence[Path]) -> int:
    """Return the highest continuation number represented by EDR files."""

    return _maximum_part(edr_files, "edr")


def trajectory_output_filename(xtc_files: Sequence[Path]) -> str:
    """Build ``production_combined_00X.xtc`` from the highest XTC part."""

    maximum_part = maximum_trajectory_part(xtc_files)
    return f"{TRAJECTORY_OUTPUT_PREFIX}_{maximum_part:03d}.xtc"


def energy_output_filename(edr_files: Sequence[Path]) -> str:
    """Build ``production_combined_00X.edr`` from the highest EDR part."""

    maximum_part = maximum_energy_part(edr_files)
    return f"{TRAJECTORY_OUTPUT_PREFIX}_{maximum_part:03d}.edr"


def _parse_check_times(output: str) -> tuple[float | None, float | None]:
    times = tuple(float(match.group("time")) for match in _TIME_PATTERN.finditer(output))
    if not times:
        return None, None
    return times[0], times[-1]


def run_gmx_check(
    path: str | Path,
    *,
    kind: OutputKind,
    gmx_command: str = "gmx",
    runner: Runner = subprocess.run,
) -> GromacsCheckResult:
    """Run ``gmx check`` with ``-f`` for XTC or ``-e`` for EDR."""

    input_path = Path(path)
    if not input_path.exists():
        raise FileNotFoundError(f"GROMACS {kind.upper()} file does not exist: {input_path}")

    flag = "-f" if kind == "xtc" else "-e"
    command = [gmx_command, "check", flag, str(input_path)]
    completed = runner(
        command,
        check=True,
        text=True,
        capture_output=True,
        cwd=input_path.parent,
    )
    stdout = completed.stdout or ""
    stderr = completed.stderr or ""
    start_time, end_time = _parse_check_times(f"{stdout}\n{stderr}")
    return GromacsCheckResult(
        kind=kind,
        path=input_path,
        command=tuple(command),
        start_time_ps=start_time,
        end_time_ps=end_time,
        stdout=stdout,
        stderr=stderr,
    )


def _merge_command(
    *,
    kind: OutputKind,
    input_files: tuple[Path, ...],
    output_path: Path,
    simulation_dir: Path,
    gmx_command: str,
    runner: Runner,
) -> GromacsMergeCommandResult:
    subcommand = "trjcat" if kind == "xtc" else "eneconv"
    command = [
        gmx_command,
        subcommand,
        "-f",
        *(str(path) for path in input_files),
        "-o",
        str(output_path),
    ]
    completed = runner(
        command,
        check=True,
        text=True,
        capture_output=True,
        cwd=simulation_dir,
    )
    return GromacsMergeCommandResult(
        kind=kind,
        command=tuple(command),
        input_files=input_files,
        output_path=output_path,
        stdout=completed.stdout or "",
        stderr=completed.stderr or "",
    )


def _print_ordered_files(
    label: str,
    paths: Sequence[Path],
    *,
    stream: TextIO,
) -> None:
    print(f"Ordered {label} inputs:", file=stream)
    if not paths:
        print("  (none)", file=stream)
        return
    for index, path in enumerate(paths, start=1):
        print(f"  {index}. {path}", file=stream)


def _print_check_result(result: GromacsCheckResult, *, stream: TextIO) -> None:
    if result.start_time_ps is None:
        timing = "time range not present in gmx check output"
    else:
        timing = f"{result.start_time_ps:g} to {result.end_time_ps:g} ps"
    print(f"Checked {result.kind.upper()}: {result.path} ({timing})", file=stream)


def _protect_output(
    output_path: Path,
    *,
    will_merge: bool,
    overwrite: bool,
) -> None:
    if will_merge and output_path.exists() and not overwrite:
        raise FileExistsError(
            f"Refusing to overwrite existing output: {output_path}. "
            "Use --overwrite to allow replacement."
        )


def _has_continuation(paths: Sequence[Path], extension: OutputKind) -> bool:
    initial_name = f"{INITIAL_PREFIX}.{extension}"
    return any(path.name != initial_name for path in paths)


def _planned_merge_command(
    kind: OutputKind,
    files: Sequence[Path],
    output_path: Path,
    gmx_command: str,
) -> tuple[str, ...]:
    subcommand = "trjcat" if kind == "xtc" else "eneconv"
    return (
        gmx_command,
        subcommand,
        "-f",
        *(str(path) for path in files),
        "-o",
        str(output_path),
    )


def merge_simulation_outputs(
    simulation_dir: str | Path,
    *,
    dry_run: bool = False,
    trajectory_only: bool = False,
    energy_only: bool = False,
    skip_check: bool = False,
    overwrite: bool = False,
    gmx_command: str = "gmx",
    runner: Runner = subprocess.run,
    stream: TextIO = sys.stdout,
) -> GromacsMergeOutputsResult:
    """Discover, check, merge, and validate one simulation directory."""

    if trajectory_only and energy_only:
        raise ValueError("trajectory_only and energy_only cannot both be enabled.")

    discovered = discover_gromacs_outputs(simulation_dir)
    trajectory_output = discovered.simulation_dir / trajectory_output_filename(
        discovered.xtc_files
    )
    energy_output = discovered.simulation_dir / energy_output_filename(
        discovered.edr_files
    )

    _print_ordered_files("XTC", discovered.xtc_files, stream=stream)
    _print_ordered_files("EDR", discovered.edr_files, stream=stream)

    trajectory_requested = not energy_only
    energy_requested = not trajectory_only
    trajectory_will_merge = trajectory_requested and bool(discovered.xtc_files)
    energy_will_merge = energy_requested and bool(discovered.edr_files)

    energy_skipped_reason: str | None = None
    if (
        energy_will_merge
        and _has_continuation(discovered.xtc_files, "xtc")
        and not _has_continuation(discovered.edr_files, "edr")
    ):
        energy_will_merge = False
        energy_skipped_reason = (
            "Continuation XTC files were found, but no continuation EDR files "
            "were found; energy merging was skipped."
        )
        print(energy_skipped_reason, file=stream)

    if trajectory_requested and not discovered.xtc_files:
        print("No raw XTC inputs were found; trajectory merging was skipped.", file=stream)
    if energy_requested and not discovered.edr_files:
        energy_skipped_reason = "No raw EDR inputs were found; energy merging was skipped."
        print(energy_skipped_reason, file=stream)

    _protect_output(
        trajectory_output,
        will_merge=trajectory_will_merge,
        overwrite=overwrite,
    )
    _protect_output(
        energy_output,
        will_merge=energy_will_merge,
        overwrite=overwrite,
    )

    input_checks: list[GromacsCheckResult] = []
    if skip_check:
        print("Input and output gmx check validation was skipped.", file=stream)
    elif dry_run:
        print("Dry run: gmx check commands were not executed.", file=stream)
    else:
        if trajectory_requested:
            for path in discovered.xtc_files:
                result = run_gmx_check(
                    path,
                    kind="xtc",
                    gmx_command=gmx_command,
                    runner=runner,
                )
                input_checks.append(result)
                _print_check_result(result, stream=stream)
        if energy_requested:
            for path in discovered.edr_files:
                result = run_gmx_check(
                    path,
                    kind="edr",
                    gmx_command=gmx_command,
                    runner=runner,
                )
                input_checks.append(result)
                _print_check_result(result, stream=stream)

    trajectory_merge = None
    energy_merge = None
    if dry_run:
        if trajectory_will_merge:
            command = _planned_merge_command(
                "xtc",
                discovered.xtc_files,
                trajectory_output,
                gmx_command,
            )
            print("Dry run XTC command: " + " ".join(command), file=stream)
        if energy_will_merge:
            command = _planned_merge_command(
                "edr",
                discovered.edr_files,
                energy_output,
                gmx_command,
            )
            print("Dry run EDR command: " + " ".join(command), file=stream)
    else:
        if trajectory_will_merge:
            trajectory_merge = _merge_command(
                kind="xtc",
                input_files=discovered.xtc_files,
                output_path=trajectory_output,
                simulation_dir=discovered.simulation_dir,
                gmx_command=gmx_command,
                runner=runner,
            )
            print(f"Merged trajectory: {trajectory_output}", file=stream)
        if energy_will_merge:
            energy_merge = _merge_command(
                kind="edr",
                input_files=discovered.edr_files,
                output_path=energy_output,
                simulation_dir=discovered.simulation_dir,
                gmx_command=gmx_command,
                runner=runner,
            )
            print(f"Merged energy: {energy_output}", file=stream)

    output_checks: list[GromacsCheckResult] = []
    if not dry_run and not skip_check:
        if trajectory_merge is not None:
            result = run_gmx_check(
                trajectory_output,
                kind="xtc",
                gmx_command=gmx_command,
                runner=runner,
            )
            output_checks.append(result)
            _print_check_result(result, stream=stream)
        if energy_merge is not None:
            result = run_gmx_check(
                energy_output,
                kind="edr",
                gmx_command=gmx_command,
                runner=runner,
            )
            output_checks.append(result)
            _print_check_result(result, stream=stream)

    print(f"Final trajectory path: {trajectory_output}", file=stream)
    if energy_merge is not None or energy_output.exists():
        print(f"Final energy path: {energy_output}", file=stream)

    return GromacsMergeOutputsResult(
        discovered=discovered,
        trajectory_output=trajectory_output,
        energy_output=energy_output,
        input_checks=tuple(input_checks),
        trajectory_merge=trajectory_merge,
        energy_merge=energy_merge,
        output_checks=tuple(output_checks),
        energy_skipped_reason=energy_skipped_reason,
        dry_run=dry_run,
    )


def build_argument_parser() -> argparse.ArgumentParser:
    """Build the command-line parser for the executable module."""

    parser = argparse.ArgumentParser(
        description=(
            "Merge restarted GROMACS XTC and EDR outputs without changing times "
            "or removing raw files."
        )
    )
    parser.add_argument(
        "simulation_directory",
        type=Path,
        nargs="?",
        default=Path("."),
        help="Simulation directory; defaults to the current directory.",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--trajectory-only",
        action="store_true",
        help="Merge only XTC trajectory files.",
    )
    mode.add_argument(
        "--energy-only",
        action="store_true",
        help="Merge only EDR energy files.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned merge commands without running GROMACS.",
    )
    parser.add_argument(
        "--skip-check",
        action="store_true",
        help="Skip input and final-output gmx check validation.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow GROMACS to replace existing combined outputs.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Command-line entry point."""

    parser = build_argument_parser()
    arguments = parser.parse_args(argv)
    try:
        merge_simulation_outputs(
            arguments.simulation_directory,
            dry_run=arguments.dry_run,
            trajectory_only=arguments.trajectory_only,
            energy_only=arguments.energy_only,
            skip_check=arguments.skip_check,
            overwrite=arguments.overwrite,
        )
    except (
        FileExistsError,
        FileNotFoundError,
        NotADirectoryError,
        subprocess.CalledProcessError,
        ValueError,
    ) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
