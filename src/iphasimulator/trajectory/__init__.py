"""Trajectory preprocessing utilities for GROMACS simulation outputs."""

from .centering import (
    CenterIndexResult,
    GromacsIndex,
    ensure_center_index,
    merged_group_atoms,
    read_index,
    resolve_center_source_groups,
    write_index,
)
from .frame_extraction import extract_first_frame, extract_frame
from .gromacs_trjconv import (
    TrjconvResult,
    center_and_compact_wrap,
    compact_wrap,
    fit_trajectory,
    reconstruct_molecules,
    run_trjconv,
)
from .preprocessing import TrajectoryPreprocessingOutputs, preprocess_gromacs_trajectory

__all__ = [
    "CenterIndexResult",
    "GromacsIndex",
    "TrajectoryPreprocessingOutputs",
    "TrjconvResult",
    "center_and_compact_wrap",
    "compact_wrap",
    "ensure_center_index",
    "extract_first_frame",
    "extract_frame",
    "fit_trajectory",
    "merged_group_atoms",
    "preprocess_gromacs_trajectory",
    "read_index",
    "reconstruct_molecules",
    "resolve_center_source_groups",
    "run_trjconv",
    "write_index",
]
