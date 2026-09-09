#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 16:54:31 2026

@author: daniel
# -*- coding: utf-8 -*-

Tests for structural descriptor generation.
"""

from pathlib import Path

import numpy as np
import pytest

from iphasimulator.analysis.simulation_loader import load_simulation
from iphasimulator.analysis.descriptors import (
    calculate_chain_distance_descriptors,
    calculate_all_chain_distance_descriptors,
    get_polymer_segments,
    get_segment_heavy_atoms,
)


# =============================================================================
# Test configuration
# =============================================================================

PROJECT_ROOT = Path("/Users/daniel/projects/iPHAsimulatorV2")

SYSTEM_DIRECTORY = (
    PROJECT_ROOT
    / "structure_database"
    / "PHA_melts"
    / "25_P3HB_10_melt"
)

SIMULATION_NAME = "broad_tg_sim_02"
SIMULATION_STAGE = "thermal_ramp_cooling"

TEST_STRIDE = 1000


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture(scope="module")
def loaded_simulation():
    """Load the test simulation once for the descriptor tests."""

    return load_simulation(
        system_directory=SYSTEM_DIRECTORY,
        simulation_name=SIMULATION_NAME,
        stage=SIMULATION_STAGE,
    )


@pytest.fixture(scope="module")
def chain_a_descriptors(loaded_simulation):
    """Generate descriptors for polymer segment A."""

    return calculate_chain_distance_descriptors(
        simulation=loaded_simulation,
        segment_id="A",
        stride=TEST_STRIDE,
    )


@pytest.fixture(scope="module")
def all_chain_descriptors(loaded_simulation):
    """Generate descriptors for every polymer chain."""

    return calculate_all_chain_distance_descriptors(
        simulation=loaded_simulation,
        stride=TEST_STRIDE,
    )


# =============================================================================
# Segment discovery
# =============================================================================

def test_polymer_segments_are_found(loaded_simulation):
    """Check that polymer segments can be obtained from the Universe."""

    segments = get_polymer_segments(
        loaded_simulation
    )

    assert len(segments) > 0


def test_real_system_contains_expected_segments(loaded_simulation):
    """Check the segment IDs of the current integration-test system."""

    segments = get_polymer_segments(
        loaded_simulation
    )

    segment_ids = [
        segment.segid
        for segment in segments
    ]

    expected_ids = list(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    )

    assert segment_ids == expected_ids


# =============================================================================
# Heavy-atom selection
# =============================================================================

def test_heavy_atoms_are_found(loaded_simulation):
    """Check that heavy atoms can be selected from a polymer chain."""

    segment = loaded_simulation.universe.segments[0]

    heavy_atoms = get_segment_heavy_atoms(
        segment
    )

    assert heavy_atoms.n_atoms > 0


def test_hydrogens_are_excluded(loaded_simulation):
    """Check that hydrogen atom names are absent from the selection."""

    segment = loaded_simulation.universe.segments[0]

    heavy_atoms = get_segment_heavy_atoms(
        segment
    )

    assert all(
        not atom.name.startswith("H")
        for atom in heavy_atoms
    )


# =============================================================================
# Single-chain descriptor tests
# =============================================================================

def test_descriptor_frame_count_is_correct(
    loaded_simulation,
    chain_a_descriptors,
):
    """Check that the requested stride gives the expected sampled frames."""

    n_frames = len(
        loaded_simulation.universe.trajectory
    )

    expected_frame_indices = np.arange(
        0,
        n_frames,
        TEST_STRIDE,
    )

    assert len(
        chain_a_descriptors.frame_indices
    ) == len(expected_frame_indices)


def test_descriptor_frame_indices_follow_stride(
    loaded_simulation,
    chain_a_descriptors,
):
    """Check that original trajectory frame indices are retained."""

    n_frames = len(
        loaded_simulation.universe.trajectory
    )

    expected_frame_indices = np.arange(
        0,
        n_frames,
        TEST_STRIDE,
    )

    np.testing.assert_array_equal(
        chain_a_descriptors.frame_indices,
        expected_frame_indices,
    )


def test_descriptor_dimension_matches_pair_count(
    chain_a_descriptors,
):
    """
    Check that the descriptor length equals the number of unique
    heavy-atom pairs.
    """

    n_heavy_atoms = (
        chain_a_descriptors.n_heavy_atoms
    )

    expected_distances = (
        n_heavy_atoms
        * (n_heavy_atoms - 1)
        // 2
    )

    actual_distances = (
        chain_a_descriptors.descriptors.shape[1]
    )

    assert actual_distances == expected_distances


def test_descriptor_matrix_has_correct_number_of_rows(
    chain_a_descriptors,
):
    """Check that one descriptor vector exists per sampled frame."""

    assert (
        chain_a_descriptors.descriptors.shape[0]
        ==
        len(chain_a_descriptors.frame_indices)
    )


def test_descriptor_values_are_finite(
    chain_a_descriptors,
):
    """Check that descriptor generation does not produce NaN or infinity."""

    assert np.isfinite(
        chain_a_descriptors.descriptors
    ).all()


def test_descriptor_distances_are_positive(
    chain_a_descriptors,
):
    """Check that all intramolecular distances are greater than zero."""

    assert (
        chain_a_descriptors.descriptors > 0
    ).all()


# =============================================================================
# Current P3HB integration-test system
# =============================================================================

def test_current_p3hb_chain_has_expected_descriptor_size(
    chain_a_descriptors,
):
    """
    Preserve the descriptor dimensions observed for the current
    P3HB decamer system.
    """

    assert chain_a_descriptors.n_heavy_atoms == 61

    assert (
        chain_a_descriptors.descriptors.shape[1]
        == 1830
    )


# =============================================================================
# All-chain descriptor tests
# =============================================================================

def test_all_segments_receive_descriptors(
    loaded_simulation,
    all_chain_descriptors,
):
    """Check that every segment receives a descriptor object."""

    expected_segments = {
        segment.segid
        for segment in loaded_simulation.universe.segments
    }

    observed_segments = set(
        all_chain_descriptors.keys()
    )

    assert observed_segments == expected_segments


def test_all_chains_have_same_sampled_frames(
    all_chain_descriptors,
):
    """Check that every polymer was sampled at the same trajectory frames."""

    chains = list(
        all_chain_descriptors.values()
    )

    reference_frames = (
        chains[0].frame_indices
    )

    for chain in chains[1:]:

        np.testing.assert_array_equal(
            chain.frame_indices,
            reference_frames,
        )


def test_all_current_p3hb_chains_have_matching_descriptor_shapes(
    all_chain_descriptors,
):
    """Check descriptor consistency across the current P3HB melt."""

    descriptor_shapes = {
        chain.descriptors.shape
        for chain in all_chain_descriptors.values()
    }

    assert len(descriptor_shapes) == 1


def test_current_system_contains_26_descriptor_sets(
    all_chain_descriptors,
):
    """Preserve the chain count of the current integration-test system."""

    assert len(
        all_chain_descriptors
    ) == 26


# =============================================================================
# Error handling
# =============================================================================

def test_invalid_stride_raises_error(
    loaded_simulation,
):
    """Check that zero stride is rejected."""

    with pytest.raises(ValueError):

        calculate_chain_distance_descriptors(
            simulation=loaded_simulation,
            segment_id="A",
            stride=0,
        )


def test_negative_stride_raises_error(
    loaded_simulation,
):
    """Check that negative stride is rejected."""

    with pytest.raises(ValueError):

        calculate_chain_distance_descriptors(
            simulation=loaded_simulation,
            segment_id="A",
            stride=-1,
        )


def test_unknown_segment_raises_error(
    loaded_simulation,
):
    """Check that requesting a missing polymer segment fails cleanly."""

    with pytest.raises(ValueError):

        calculate_chain_distance_descriptors(
            simulation=loaded_simulation,
            segment_id="NOT_A_SEGMENT",
            stride=TEST_STRIDE,
        )


def test_invalid_stride_for_all_chains_raises_error(
    loaded_simulation,
):
    """Check that invalid stride is rejected by the all-chain function."""

    with pytest.raises(ValueError):

        calculate_all_chain_distance_descriptors(
            simulation=loaded_simulation,
            stride=0,
        )