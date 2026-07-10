"""Representative frame extraction helpers for preprocessed trajectories."""

from __future__ import annotations

from pathlib import Path
import subprocess

from iphasimulator.trajectory_gromacs_trjconv import Runner, TrjconvResult, run_trjconv


def extract_frame(
    *,
    trajectory: str | Path,
    structure: str | Path,
    output: str | Path,
    index: str | Path | None = None,
    time_ps: float | int | None = None,
    output_group: str = "System",
    gmx_command: str = "gmx",
    cwd: str | Path | None = None,
    runner: Runner = subprocess.run,
) -> TrjconvResult:
    """Extract a single representative frame using ``gmx trjconv``.

    Pass ``time_ps`` to select the frame nearest that simulation time.
    """

    args: list[str] = []
    if time_ps is not None:
        args.extend(["-dump", str(time_ps)])

    return run_trjconv(
        trajectory=trajectory,
        structure=structure,
        output=output,
        index=index,
        selections=(output_group,),
        trjconv_args=tuple(args),
        gmx_command=gmx_command,
        cwd=cwd,
        runner=runner,
    )


def extract_first_frame(**kwargs) -> TrjconvResult:
    """Extract frame 0 as a lightweight visual sanity check."""

    return extract_frame(time_ps=0, **kwargs)
