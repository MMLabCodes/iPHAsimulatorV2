"""End-to-end GROMACS trajectory preprocessing for polymer analysis."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess

from .centering import CenterIndexResult, ensure_center_index
from .frame_extraction import extract_first_frame
from .gromacs_trjconv import Runner, TrjconvResult, center_and_compact_wrap, fit_trajectory


@dataclass(frozen=True)
class TrajectoryPreprocessingOutputs:
    """Files created by the standard preprocessing workflow."""

    system_dir: Path
    raw_dir: Path
    processed_dir: Path
    analysis_ready_dir: Path
    center_index: CenterIndexResult
    raw_trajectory_path: Path
    structure_path: Path
    centered_trajectory_path: Path
    fitted_trajectory_path: Path | None
    representative_frame_path: Path | None
    center_result: TrjconvResult | None
    fit_result: TrjconvResult | None
    frame_result: TrjconvResult | None

    @property
    def analysis_trajectory_path(self) -> Path:
        return self.fitted_trajectory_path or self.centered_trajectory_path


def _resolve_existing_path(system_dir: Path, raw_dir: Path, filename: str | Path) -> Path:
    path = Path(filename)
    if path.is_absolute():
        return path

    raw_path = raw_dir / path
    root_path = system_dir / path
    if raw_path.exists():
        return raw_path
    return root_path


def _default_centered_name(trajectory_path: Path) -> str:
    return trajectory_path.name.replace("_production", "_centered")


def _default_fitted_name(trajectory_path: Path) -> str:
    return trajectory_path.name.replace("_production", "_fitted").replace("_centered", "_fitted")


def preprocess_gromacs_trajectory(
    system_dir: str | Path,
    *,
    trajectory: str | Path = "step7_production.xtc",
    structure: str | Path = "step7_production.tpr",
    index: str | Path = "index.ndx",
    workflow_type: str = "polymer",
    source_groups: tuple[str, ...] | list[str] | None = None,
    fit: bool = True,
    extract_representative_frame: bool = True,
    gmx_command: str = "gmx",
    runner: Runner = subprocess.run,
    dry_run: bool = False,
) -> TrajectoryPreprocessingOutputs:
    """Run the standard GROMACS preprocessing pipeline.

    The output trajectory keeps ``System`` so water and ions remain available for
    downstream analyses, while centering/fitting use the reusable ``center`` group.
    """

    system_path = Path(system_dir)
    raw_dir = system_path / "raw"
    processed_dir = system_path / "processed"
    analysis_ready_dir = system_path / "analysis_ready"
    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)
    analysis_ready_dir.mkdir(parents=True, exist_ok=True)

    source_index = _resolve_existing_path(system_path, raw_dir, index)
    center_index = ensure_center_index(
        source_index,
        system_path / "center.ndx",
        workflow_type=workflow_type,
        source_groups=source_groups,
    )

    raw_trajectory_path = _resolve_existing_path(system_path, raw_dir, trajectory)
    structure_path = _resolve_existing_path(system_path, raw_dir, structure)
    centered_path = processed_dir / _default_centered_name(raw_trajectory_path)
    fitted_path = analysis_ready_dir / _default_fitted_name(raw_trajectory_path)
    frame_path = analysis_ready_dir / "representative_frame.gro"

    if dry_run:
        return TrajectoryPreprocessingOutputs(
            system_dir=system_path,
            raw_dir=raw_dir,
            processed_dir=processed_dir,
            analysis_ready_dir=analysis_ready_dir,
            center_index=center_index,
            raw_trajectory_path=raw_trajectory_path,
            structure_path=structure_path,
            centered_trajectory_path=centered_path,
            fitted_trajectory_path=fitted_path if fit else None,
            representative_frame_path=frame_path if extract_representative_frame else None,
            center_result=None,
            fit_result=None,
            frame_result=None,
        )

    missing_inputs = [
        path for path in (raw_trajectory_path, structure_path) if not path.exists()
    ]
    if missing_inputs:
        missing_text = ", ".join(str(path) for path in missing_inputs)
        raise FileNotFoundError(
            "Cannot preprocess trajectory because required GROMACS outputs are "
            f"missing: {missing_text}"
        )

    center_result = center_and_compact_wrap(
        trajectory=raw_trajectory_path,
        structure=structure_path,
        index=center_index.index_path,
        output=centered_path,
        center_group=center_index.center_group,
        output_group="System",
        gmx_command=gmx_command,
        runner=runner,
    )

    fit_result: TrjconvResult | None = None
    analysis_trajectory = centered_path
    if fit:
        fit_result = fit_trajectory(
            trajectory=centered_path,
            structure=structure_path,
            index=center_index.index_path,
            output=fitted_path,
            fit_group=center_index.center_group,
            output_group="System",
            gmx_command=gmx_command,
            runner=runner,
        )
        analysis_trajectory = fitted_path
    else:
        fitted_path = None

    frame_result: TrjconvResult | None = None
    if extract_representative_frame:
        frame_result = extract_first_frame(
            trajectory=analysis_trajectory,
            structure=structure_path,
            index=center_index.index_path,
            output=frame_path,
            output_group="System",
            gmx_command=gmx_command,
            runner=runner,
        )
    else:
        frame_path = None

    return TrajectoryPreprocessingOutputs(
        system_dir=system_path,
        raw_dir=raw_dir,
        processed_dir=processed_dir,
        analysis_ready_dir=analysis_ready_dir,
        center_index=center_index,
        raw_trajectory_path=raw_trajectory_path,
        structure_path=structure_path,
        centered_trajectory_path=centered_path,
        fitted_trajectory_path=fitted_path,
        representative_frame_path=frame_path,
        center_result=center_result,
        fit_result=fit_result,
        frame_result=frame_result,
    )
