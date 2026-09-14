#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 11:11:24 2026

@author: daniel

Tests for principal component analysis of structural descriptors.
"""

from pathlib import Path

import numpy as np
import pytest

from iphasimulator.analysis.simulation_loader import load_simulation
from iphasimulator.analysis.descriptors import (
    calculate_all_chain_distance_descriptors,
)
from iphasimulator.analysis.pca import (
    calculate_chain_pca,
    calculate_all_chain_pca,
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
N_COMPONENTS = 5


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture(scope="module")
def loaded_simulation():
    """Load the integration-test simulation."""

    return load_simulation(
        system_directory=SYSTEM_DIRECTORY,
        simulation_name=SIMULATION_NAME,
        stage=SIMULATION_STAGE,
    )


@pytest.fixture(scope="module")
def all_descriptors(loaded_simulation):
    """Generate structural descriptors for all polymer chains."""

    return calculate_all_chain_distance_descriptors(
        simulation=loaded_simulation,
        stride=TEST_STRIDE,
    )


@pytest.fixture(scope="module")
def chain_a_pca(all_descriptors):
    """Calculate PCA for polymer segment A."""

    return calculate_chain_pca(
        chain_descriptors=all_descriptors["A"],
        n_components=N_COMPONENTS,
    )


@pytest.fixture(scope="module")
def all_pca_results(all_descriptors):
    """Calculate PCA independently for all polymer chains."""

    return calculate_all_chain_pca(
        descriptors_by_segment=all_descriptors,
        n_components=N_COMPONENTS,
    )


# =============================================================================
# Single-chain PCA
# =============================================================================

def test_pca_retains_requested_number_of_components(chain_a_pca):
    """Check that PCA retains the requested number of components."""

    assert chain_a_pca.n_components == N_COMPONENTS

    assert (
        chain_a_pca.transformed_data.shape[1]
        == N_COMPONENTS
    )


def test_pca_preserves_number_of_samples(
    all_descriptors,
    chain_a_pca,
):
    """Check that PCA does not alter the number of sampled conformations."""

    assert (
        chain_a_pca.transformed_data.shape[0]
        ==
        all_descriptors["A"].descriptors.shape[0]
    )


def test_pca_preserves_frame_indices(
    all_descriptors,
    chain_a_pca,
):
    """Check that PCA results retain their original trajectory frames."""

    np.testing.assert_array_equal(
        chain_a_pca.frame_indices,
        all_descriptors["A"].frame_indices,
    )


def test_pca_values_are_finite(chain_a_pca):
    """Check that PCA does not produce NaN or infinite values."""

    assert np.isfinite(
        chain_a_pca.transformed_data
    ).all()


# =============================================================================
# Explained variance
# =============================================================================

def test_explained_variance_has_one_value_per_component(
    chain_a_pca,
):
    """Check explained-variance output dimensions."""

    assert len(
        chain_a_pca.explained_variance_ratio
    ) == N_COMPONENTS


def test_explained_variance_is_valid(chain_a_pca):
    """Check that explained-variance ratios lie between zero and one."""

    variance = (
        chain_a_pca.explained_variance_ratio
    )

    assert np.all(variance >= 0)
    assert np.all(variance <= 1)


def test_explained_variance_decreases_for_current_system(
    chain_a_pca,
):
    """Check that PCA components are ordered by decreasing variance."""

    variance = (
        chain_a_pca.explained_variance_ratio
    )

    assert np.all(
        np.diff(variance) <= 0
    )


def test_cumulative_variance_is_monotonic(
    chain_a_pca,
):
    """Check that cumulative explained variance cannot decrease."""

    cumulative = (
        chain_a_pca.cumulative_explained_variance
    )

    assert np.all(
        np.diff(cumulative) >= 0
    )


def test_cumulative_variance_matches_component_sum(
    chain_a_pca,
):
    """Check calculation of cumulative explained variance."""

    expected = np.cumsum(
        chain_a_pca.explained_variance_ratio
    )

    np.testing.assert_allclose(
        chain_a_pca.cumulative_explained_variance,
        expected,
    )


# =============================================================================
# Standardisation / PCA properties
# =============================================================================

def test_pca_component_scores_are_centred(chain_a_pca):
    """
    Check that PCA-transformed component scores are centred around zero.
    """

    component_means = (
        chain_a_pca.transformed_data.mean(axis=0)
    )

    np.testing.assert_allclose(
        component_means,
        0.0,
        atol=1e-10,
    )


# =============================================================================
# Current P3HB integration system
# =============================================================================

def test_current_p3hb_pca_shape(chain_a_pca):
    """Preserve the observed PCA dimensions for the development system."""

    assert chain_a_pca.transformed_data.shape == (
        200,
        5,
    )


def test_current_p3hb_variance_is_reasonable(chain_a_pca):
    """
    Check the approximate retained variance observed for the current
    development trajectory.

    This is deliberately a broad range rather than an exact numerical
    regression requirement.
    """

    cumulative_variance = (
        chain_a_pca.cumulative_explained_variance[-1]
    )

    assert 0.50 < cumulative_variance < 0.65


# =============================================================================
# All-chain PCA
# =============================================================================

def test_all_chains_receive_pca_results(
    all_descriptors,
    all_pca_results,
):
    """Check that every descriptor set receives a PCA result."""

    assert set(
        all_pca_results.keys()
    ) == set(
        all_descriptors.keys()
    )


def test_all_chains_have_requested_pca_dimensions(
    all_pca_results,
):
    """Check PCA dimensions across all polymer chains."""

    for result in all_pca_results.values():

        assert (
            result.transformed_data.shape[1]
            == N_COMPONENTS
        )


def test_all_chain_pca_results_are_finite(
    all_pca_results,
):
    """Check all PCA-transformed values are finite."""

    for result in all_pca_results.values():

        assert np.isfinite(
            result.transformed_data
        ).all()


# =============================================================================
# Error handling
# =============================================================================

def test_zero_components_raises_error(all_descriptors):
    """Check that zero PCA components are rejected."""

    with pytest.raises(ValueError):

        calculate_chain_pca(
            chain_descriptors=all_descriptors["A"],
            n_components=0,
        )


def test_negative_components_raises_error(all_descriptors):
    """Check that negative PCA components are rejected."""

    with pytest.raises(ValueError):

        calculate_chain_pca(
            chain_descriptors=all_descriptors["A"],
            n_components=-1,
        )


def test_too_many_components_raises_error(all_descriptors):
    """Check that unsupported PCA dimensionality is rejected."""

    chain = all_descriptors["A"]

    max_components = min(
        chain.descriptors.shape
    )

    with pytest.raises(ValueError):

        calculate_chain_pca(
            chain_descriptors=chain,
            n_components=max_components + 1,
        )


def test_empty_descriptor_dictionary_raises_error():
    """Check that all-chain PCA requires descriptor input."""

    with pytest.raises(ValueError):

        calculate_all_chain_pca(
            descriptors_by_segment={},
            n_components=N_COMPONENTS,
        )
