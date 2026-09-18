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
        Unique analysis identifier assigned to the polymer chain.

        Example::

            "chain_001"

    segment_index : int
        Zero-based MDAnalysis segment index corresponding to the polymer chain.

    topology_segid : str
        Original segment identifier stored in the topology.

        This value is retained for reference only and is not assumed to be
        unique.

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
    segment_index: int
    topology_segid: str
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

    heavy_atoms = (
        segment.atoms.select_atoms(
            "not name H*"
        )
    )

    if heavy_atoms.n_atoms == 0:
        raise ValueError(
            "No heavy atoms found for segment "
            f"'{segment.segid}'."
        )

    return heavy_atoms


# =============================================================================
# Chain identifiers
# =============================================================================

def get_chain_analysis_id(
    segment_index: int,
) -> str:
    """
    Return a stable analysis identifier for a polymer chain.

    Parameters
    ----------
    segment_index : int
        Zero-based segment index.

    Returns
    -------
    str
        Chain identifier.

        Example::

            0 -> "chain_001"
            1 -> "chain_002"
    """

    if segment_index < 0:
        raise ValueError(
            "segment_index must be greater than or equal to zero."
        )

    return (
        f"chain_{segment_index + 1:03d}"
    )


# =============================================================================
# Pairwise distance generation
# =============================================================================

def calculate_chain_distance_descriptors(
    simulation: LoadedSimulation,
    segment_index: int,
    stride: int = 1,
) -> ChainDistanceDescriptors:
    """
    Calculate pairwise intramolecular heavy-atom distances for one chain.

    Each sampled trajectory frame is represented by all unique pairwise
    distances between heavy atoms within the selected polymer chain.

    Polymer chains are identified using their zero-based MDAnalysis segment
    index rather than their topology segid. This avoids ambiguity when
    topology segment identifiers are reused.

    Parameters
    ----------
    simulation : LoadedSimulation
        Loaded molecular dynamics simulation.

    segment_index : int
        Zero-based index of the polymer segment to analyse.

        Example::

            0

        corresponds to the first segment in::

            simulation.universe.segments

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
        If stride or segment_index is invalid, or the selected segment
        contains insufficient heavy atoms.

    IndexError
        If segment_index is outside the available segment range.
    """

    # -------------------------------------------------------------------------
    # Validate stride
    # -------------------------------------------------------------------------

    if stride <= 0:
        raise ValueError(
            "stride must be greater than zero."
        )


    # -------------------------------------------------------------------------
    # Resolve universe
    # -------------------------------------------------------------------------

    universe = (
        simulation.universe
    )

    segments = (
        universe.segments
    )


    # -------------------------------------------------------------------------
    # Validate segment index
    # -------------------------------------------------------------------------

    if segment_index < 0:
        raise ValueError(
            "segment_index must be greater than or equal to zero."
        )

    if segment_index >= len(
        segments
    ):
        raise IndexError(
            "Segment index is outside the available range:\n"
            f"Requested index:   {segment_index}\n"
            f"Available segments: {len(segments)}"
        )


    # -------------------------------------------------------------------------
    # Select requested segment
    # -------------------------------------------------------------------------

    segment = (
        segments[
            segment_index
        ]
    )

    segment_id = (
        get_chain_analysis_id(
            segment_index
        )
    )

    topology_segid = (
        str(
            segment.segid
        )
    )


    # -------------------------------------------------------------------------
    # Select heavy atoms
    # -------------------------------------------------------------------------

    heavy_atoms = (
        get_segment_heavy_atoms(
            segment
        )
    )

    n_heavy_atoms = (
        heavy_atoms.n_atoms
    )

    if n_heavy_atoms < 2:
        raise ValueError(
            f"{segment_id} "
            f"(topology segid '{topology_segid}') "
            "contains fewer than two heavy atoms."
        )


    # -------------------------------------------------------------------------
    # Determine sampled frames
    # -------------------------------------------------------------------------

    n_frames = (
        len(
            universe.trajectory
        )
    )

    frame_indices = np.arange(
        0,
        n_frames,
        stride,
        dtype=int,
    )


    # -------------------------------------------------------------------------
    # Determine descriptor dimensionality
    # -------------------------------------------------------------------------

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
            len(
                frame_indices
            ),
            n_distances,
        ),
        dtype=np.float64,
    )


    # -------------------------------------------------------------------------
    # Calculate descriptors
    # -------------------------------------------------------------------------

    for (
        output_index,
        frame_index,
    ) in enumerate(
        frame_indices
    ):

        universe.trajectory[
            frame_index
        ]

        descriptors[
            output_index
        ] = (
            self_distance_array(
                heavy_atoms.positions,
                box=universe.dimensions,
            )
        )


    # -------------------------------------------------------------------------
    # Return descriptor container
    # -------------------------------------------------------------------------

    return ChainDistanceDescriptors(
        segment_id=segment_id,
        segment_index=segment_index,
        topology_segid=topology_segid,
        frame_indices=frame_indices,
        descriptors=descriptors,
        n_heavy_atoms=n_heavy_atoms,
    )


# =============================================================================
# All-chain descriptor generation
# =============================================================================

def calculate_all_chain_distance_descriptors(
    simulation: LoadedSimulation,
    stride: int = 1,
) -> dict[str, ChainDistanceDescriptors]:
    """
    Calculate pairwise heavy-atom distance descriptors for all polymer chains.

    Each MDAnalysis segment is treated as an independent polymer chain and
    processed separately.

    Chains are identified internally using stable analysis identifiers such as::

        chain_001
        chain_002
        chain_003

    The original topology segid is retained within each result object but is
    not used as a unique key.

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
        Dictionary mapping unique analysis chain IDs to
        ChainDistanceDescriptors objects.

        Example::

            {
                "chain_001": ChainDistanceDescriptors(...),
                "chain_002": ChainDistanceDescriptors(...),
                ...
            }

    Raises
    ------
    ValueError
        If stride is not greater than zero or no polymer segments are found.
    """

    # -------------------------------------------------------------------------
    # Validate stride
    # -------------------------------------------------------------------------

    if stride <= 0:
        raise ValueError(
            "stride must be greater than zero."
        )


    # -------------------------------------------------------------------------
    # Discover polymer segments
    # -------------------------------------------------------------------------

    segments = (
        get_polymer_segments(
            simulation
        )
    )


    # -------------------------------------------------------------------------
    # Generate descriptors
    # -------------------------------------------------------------------------

    descriptors_by_segment = {}


    for segment_index in range(
        len(
            segments
        )
    ):

        chain_id = (
            get_chain_analysis_id(
                segment_index
            )
        )

        descriptors_by_segment[
            chain_id
        ] = (
            calculate_chain_distance_descriptors(
                simulation=simulation,
                segment_index=segment_index,
                stride=stride,
            )
        )


    # -------------------------------------------------------------------------
    # Return results
    # -------------------------------------------------------------------------

    return descriptors_by_segment