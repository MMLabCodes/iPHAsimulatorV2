#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 16:49:33 2026

@author: daniel

Structural descriptor generation for molecular dynamics analysis.

This module provides utilities for converting molecular structures from
MD trajectories into numerical descriptors suitable for downstream
analysis.

The initial implementation generates pairwise intramolecular heavy-atom
distance descriptors for individual polymer chains.
"""

from __future__ import annotations

from dataclasses import dataclass

import MDAnalysis as mda
import numpy as np
from MDAnalysis.lib.distances import self_distance_array

from .simulation_loader import LoadedSimulation


# =============================================================================
# Descriptor container
# =============================================================================

@dataclass(frozen=True)
class ChainDistanceDescriptors:
    """
    Pairwise intramolecular distance descriptors for one polymer chain.

    Attributes
    ----------
    segment_id : str
        MDAnalysis segment identifier corresponding to the polymer chain.

    frame_indices : numpy.ndarray
        Original trajectory frame indices used to generate descriptors.

    descriptors : numpy.ndarray
        Pairwise heavy-atom distance descriptors.

        Shape::

            (n_sampled_frames, n_pairwise_distances)

    n_heavy_atoms : int
        Number of heavy atoms used to generate each descriptor vector.
    """

    segment_id: str
    frame_indices: np.ndarray
    descriptors: np.ndarray
    n_heavy_atoms: int


# =============================================================================
# Polymer chain discovery
# =============================================================================

def get_polymer_segments(
    simulation: LoadedSimulation,
) -> list[mda.core.groups.Segment]:
    """
    Return polymer segments contained in a loaded simulation.

    In current iPHAsimulator molecular systems, individual polymer chains
    are represented by separate MDAnalysis segments.

    Parameters
    ----------
    simulation : LoadedSimulation
        Loaded molecular dynamics simulation.

    Returns
    -------
    list of MDAnalysis Segment
        Segments present in the molecular system.

    Raises
    ------
    ValueError
        If no segments are present in the loaded topology.
    """

    segments = list(
        simulation.universe.segments
    )

    if not segments:
        raise ValueError(
            "No segments were found in the loaded molecular system."
        )

    return segments


# =============================================================================
# Heavy-atom selection
# =============================================================================

def get_segment_heavy_atoms(
    segment: mda.core.groups.Segment,
) -> mda.core.groups.AtomGroup:
    """
    Select heavy atoms from a polymer segment.

    Hydrogen atoms are excluded using the same atom-name selection
    employed in the original Tg analysis workflow.

    Parameters
    ----------
    segment : MDAnalysis Segment
        Polymer segment from which heavy atoms are selected.

    Returns
    -------
    MDAnalysis AtomGroup
        Heavy atoms belonging to the segment.

    Raises
    ------
    ValueError
        If no heavy atoms are found.
    """

    heavy_atoms = segment.atoms.select_atoms(
        "not name H*"
    )

    if heavy_atoms.n_atoms == 0:
        raise ValueError(
            f"No heavy atoms found for segment '{segment.segid}'."
        )

    return heavy_atoms


# =============================================================================
# Pairwise distance generation
# =============================================================================

def calculate_chain_distance_descriptors(
    simulation: LoadedSimulation,
    segment_id: str,
    stride: int = 1,
) -> ChainDistanceDescriptors:
    """
    Calculate pairwise intramolecular heavy-atom distances for one chain.

    Each sampled trajectory frame is represented by all unique pairwise
    distances between heavy atoms within the selected polymer chain.

    Parameters
    ----------
    simulation : LoadedSimulation
        Loaded molecular dynamics simulation.

    segment_id : str
        Segment identifier corresponding to the polymer chain.

        Example::

            "A"

    stride : int, optional
        Trajectory frame sampling stride.

        A stride of 1 uses every frame, a stride of 10 uses every tenth
        frame, etc.

        Default:
            1

    Returns
    -------
    ChainDistanceDescriptors
        Pairwise distance descriptors and associated metadata.

    Raises
    ------
    ValueError
        If the stride is invalid, the requested segment cannot be found,
        or the segment does not contain sufficient heavy atoms.
    """

    # -------------------------------------------------------------------------
    # Validate stride
    # -------------------------------------------------------------------------

    if stride <= 0:
        raise ValueError(
            "stride must be greater than zero."
        )

    universe = simulation.universe

    # -------------------------------------------------------------------------
    # Find requested polymer segment
    # -------------------------------------------------------------------------

    matching_segments = [
        segment
        for segment in universe.segments
        if segment.segid == segment_id
    ]

    if not matching_segments:
        raise ValueError(
            f"Segment '{segment_id}' was not found."
        )

    if len(matching_segments) > 1:
        raise ValueError(
            f"Multiple segments with ID '{segment_id}' were found."
        )

    segment = matching_segments[0]

    # -------------------------------------------------------------------------
    # Select heavy atoms
    # -------------------------------------------------------------------------

    heavy_atoms = get_segment_heavy_atoms(
        segment
    )

    n_heavy_atoms = heavy_atoms.n_atoms

    if n_heavy_atoms < 2:
        raise ValueError(
            f"Segment '{segment_id}' contains fewer than two heavy atoms."
        )

    # -------------------------------------------------------------------------
    # Determine sampled frames
    # -------------------------------------------------------------------------

    n_frames = len(
        universe.trajectory
    )

    frame_indices = np.arange(
        0,
        n_frames,
        stride,
        dtype=int,
    )

    # Number of unique pairwise distances
    n_distances = (
        n_heavy_atoms
        * (n_heavy_atoms - 1)
        // 2
    )

    # -------------------------------------------------------------------------
    # Allocate descriptor array
    # -------------------------------------------------------------------------

    descriptors = np.empty(
        (
            len(frame_indices),
            n_distances,
        ),
        dtype=np.float64,
    )

    # -------------------------------------------------------------------------
    # Calculate descriptors
    # -------------------------------------------------------------------------

    for output_index, frame_index in enumerate(
        frame_indices
    ):

        universe.trajectory[frame_index]

        descriptors[output_index] = (
            self_distance_array(
                heavy_atoms.positions
            )
        )

    # -------------------------------------------------------------------------
    # Return descriptor container
    # -------------------------------------------------------------------------

    return ChainDistanceDescriptors(
        segment_id=segment_id,
        frame_indices=frame_indices,
        descriptors=descriptors,
        n_heavy_atoms=n_heavy_atoms,
    )

def calculate_all_chain_distance_descriptors(
    simulation: LoadedSimulation,
    stride: int = 1,
) -> dict[str, ChainDistanceDescriptors]:
    """
    Calculate pairwise heavy-atom distance descriptors for all polymer chains.

    Each MDAnalysis segment is treated as an independent polymer chain and
    processed separately.

    Parameters
    ----------
    simulation : LoadedSimulation
        Loaded molecular dynamics simulation.

    stride : int, optional
        Trajectory frame sampling stride.

        A stride of 1 uses every trajectory frame, a stride of 10 uses every
        tenth frame, etc.

        Default:
            1

    Returns
    -------
    dict
        Dictionary mapping segment IDs to ChainDistanceDescriptors objects.

        Example::

            {
                "A": ChainDistanceDescriptors(...),
                "B": ChainDistanceDescriptors(...),
                ...
            }

    Raises
    ------
    ValueError
        If stride is not greater than zero or no polymer segments are found.
    """

    if stride <= 0:
        raise ValueError(
            "stride must be greater than zero."
        )

    segments = get_polymer_segments(
        simulation
    )

    descriptors_by_segment = {}

    for segment in segments:

        segment_id = segment.segid

        descriptors_by_segment[segment_id] = (
            calculate_chain_distance_descriptors(
                simulation=simulation,
                segment_id=segment_id,
                stride=stride,
            )
        )

    return descriptors_by_segment