"""Small, testable wrappers around ``gmx trjconv`` preprocessing commands."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
from typing import Callable, Sequence


Runner = Callable[..., subprocess.CompletedProcess]


@dataclass(frozen=True)
class TrjconvResult:
    """Captured command result for a ``gmx trjconv`` operation."""

    command: tuple[str, ...]
    selections: tuple[str, ...]
    output_path: Path
    returncode: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0


def _selection_input(selections: Sequence[str]) -> str:
    return "\n".join(selections) + "\n"


def run_trjconv(
    *,
    trajectory: str | Path,
    structure: str | Path,
    output: str | Path,
    index: str | Path | None = None,
    selections: Sequence[str] = ("System",),
    trjconv_args: Sequence[str] = (),
    gmx_command: str = "gmx",
    cwd: str | Path | None = None,
    runner: Runner = subprocess.run,
) -> TrjconvResult:
    """Run ``gmx trjconv`` with explicit stdin group selections."""

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    command: list[str] = [
        gmx_command,
        "trjconv",
        "-f",
        str(trajectory),
        "-s",
        str(structure),
    ]
    if index is not None:
        command.extend(["-n", str(index)])
    command.extend(trjconv_args)
    command.extend(["-o", str(output_path)])

    result = runner(
        command,
        input=_selection_input(selections),
        text=True,
        capture_output=True,
        cwd=Path(cwd) if cwd is not None else None,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "gmx trjconv failed with return code "
            f"{result.returncode}: {result.stderr or result.stdout}"
        )

    return TrjconvResult(
        command=tuple(command),
        selections=tuple(selections),
        output_path=output_path,
        returncode=result.returncode,
        stdout=result.stdout,
        stderr=result.stderr,
    )


def center_and_compact_wrap(
    *,
    trajectory: str | Path,
    structure: str | Path,
    index: str | Path,
    output: str | Path,
    center_group: str = "center",
    output_group: str = "System",
    gmx_command: str = "gmx",
    cwd: str | Path | None = None,
    runner: Runner = subprocess.run,
) -> TrjconvResult:
    """Center on ``center_group`` and write the full compact solvated system."""

    return run_trjconv(
        trajectory=trajectory,
        structure=structure,
        index=index,
        output=output,
        selections=(center_group, output_group),
        trjconv_args=("-pbc", "mol", "-ur", "compact", "-center"),
        gmx_command=gmx_command,
        cwd=cwd,
        runner=runner,
    )


def reconstruct_molecules(
    *,
    trajectory: str | Path,
    structure: str | Path,
    index: str | Path,
    output: str | Path,
    output_group: str = "System",
    gmx_command: str = "gmx",
    cwd: str | Path | None = None,
    runner: Runner = subprocess.run,
) -> TrjconvResult:
    """Repair molecules split across periodic boundaries without centering."""

    return run_trjconv(
        trajectory=trajectory,
        structure=structure,
        index=index,
        output=output,
        selections=(output_group,),
        trjconv_args=("-pbc", "mol"),
        gmx_command=gmx_command,
        cwd=cwd,
        runner=runner,
    )


def compact_wrap(
    *,
    trajectory: str | Path,
    structure: str | Path,
    index: str | Path,
    output: str | Path,
    output_group: str = "System",
    gmx_command: str = "gmx",
    cwd: str | Path | None = None,
    runner: Runner = subprocess.run,
) -> TrjconvResult:
    """Wrap the full system into a compact unit-cell representation."""

    return run_trjconv(
        trajectory=trajectory,
        structure=structure,
        index=index,
        output=output,
        selections=(output_group,),
        trjconv_args=("-ur", "compact"),
        gmx_command=gmx_command,
        cwd=cwd,
        runner=runner,
    )


def fit_trajectory(
    *,
    trajectory: str | Path,
    structure: str | Path,
    index: str | Path,
    output: str | Path,
    fit_group: str = "center",
    output_group: str = "System",
    fit: str = "rot+trans",
    gmx_command: str = "gmx",
    cwd: str | Path | None = None,
    runner: Runner = subprocess.run,
) -> TrjconvResult:
    """Fit/alignment wrapper using the centering group as the reference group."""

    return run_trjconv(
        trajectory=trajectory,
        structure=structure,
        index=index,
        output=output,
        selections=(fit_group, output_group),
        trjconv_args=("-fit", fit),
        gmx_command=gmx_command,
        cwd=cwd,
        runner=runner,
    )

