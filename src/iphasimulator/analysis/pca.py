#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 16:57:41 2026

@author: daniel

Principal component analysis for molecular structural descriptors.

This module provides utilities for standardising structural descriptor
matrices and reducing their dimensionality using principal component
analysis (PCA).

Each polymer chain is processed independently.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from .descriptors import ChainDistanceDescriptors


# =============================================================================
# PCA result container
# =============================================================================

@dataclass(frozen=True)
class ChainPCAResult:
    """
    PCA results for one polymer chain.

    Attributes
    ----------
    segment_id : str
        Segment identifier corresponding to the polymer chain.

    frame_indices : numpy.ndarray
        Original trajectory frame indices represented in the PCA result.

    transformed_data : numpy.ndarray
        PCA-transformed structural descriptors.

        Shape::

            (n_sampled_frames, n_components)

    explained_variance_ratio : numpy.ndarray
        Fraction of total variance explained by each principal component.

    cumulative_explained_variance : numpy.ndarray
        Cumulative fraction of variance explained by the retained
        principal components.

    n_components : int
        Number of principal components retained.
    """

    segment_id: str
    frame_indices: np.ndarray
    transformed_data: np.ndarray
    explained_variance_ratio: np.ndarray
    cumulative_explained_variance: np.ndarray
    n_components: int


# =============================================================================
# Single-chain PCA
# =============================================================================

def calculate_chain_pca(
    chain_descriptors: ChainDistanceDescriptors,
    n_components: int,
) -> ChainPCAResult:
    """
    Standardise and PCA-transform structural descriptors for one chain.

    Structural descriptor features are first independently standardised
    to zero mean and unit variance using StandardScaler. PCA is then
    applied to the standardised descriptor matrix.

    Parameters
    ----------
    chain_descriptors : ChainDistanceDescriptors
        Pairwise intramolecular distance descriptors for one polymer
        chain.

    n_components : int
        Number of principal components to retain.

    Returns
    -------
    ChainPCAResult
        PCA-transformed descriptors and explained-variance information.

    Raises
    ------
    ValueError
        If n_components is invalid or the descriptor matrix cannot
        support the requested number of components.
    """

    if n_components <= 0:
        raise ValueError(
            "n_components must be greater than zero."
        )

    descriptors = chain_descriptors.descriptors

    if descriptors.ndim != 2:
        raise ValueError(
            "Descriptor matrix must be two-dimensional."
        )

    n_samples, n_features = descriptors.shape

    if n_samples < 2:
        raise ValueError(
            "At least two sampled frames are required for PCA."
        )

    max_components = min(
        n_samples,
        n_features,
    )

    if n_components > max_components:
        raise ValueError(
            f"n_components={n_components} exceeds the maximum "
            f"supported value of {max_components}."
        )

    # -------------------------------------------------------------------------
    # Standardise descriptor features
    # -------------------------------------------------------------------------

    scaler = StandardScaler()

    scaled_descriptors = scaler.fit_transform(
        descriptors
    )

    # -------------------------------------------------------------------------
    # Principal component analysis
    # -------------------------------------------------------------------------

    pca = PCA(
        n_components=n_components
    )

    transformed_data = pca.fit_transform(
        scaled_descriptors
    )

    explained_variance_ratio = (
        pca.explained_variance_ratio_.copy()
    )

    cumulative_explained_variance = (
        np.cumsum(
            explained_variance_ratio
        )
    )

    return ChainPCAResult(
        segment_id=chain_descriptors.segment_id,
        frame_indices=chain_descriptors.frame_indices.copy(),
        transformed_data=transformed_data,
        explained_variance_ratio=explained_variance_ratio,
        cumulative_explained_variance=cumulative_explained_variance,
        n_components=n_components,
    )


# =============================================================================
# All-chain PCA
# =============================================================================

def calculate_all_chain_pca(
    descriptors_by_segment: dict[
        str,
        ChainDistanceDescriptors,
    ],
    n_components: int,
) -> dict[str, ChainPCAResult]:
    """
    Perform independent PCA for all polymer chains.

    Each chain is standardised and PCA-transformed separately.

    Parameters
    ----------
    descriptors_by_segment : dict
        Dictionary mapping segment IDs to ChainDistanceDescriptors.

    n_components : int
        Number of principal components retained for each chain.

    Returns
    -------
    dict
        Dictionary mapping segment IDs to ChainPCAResult objects.

    Raises
    ------
    ValueError
        If no descriptor sets are supplied.
    """

    if not descriptors_by_segment:
        raise ValueError(
            "No chain descriptor sets were supplied."
        )

    results = {}

    for segment_id, chain_descriptors in (
        descriptors_by_segment.items()
    ):

        results[segment_id] = (
            calculate_chain_pca(
                chain_descriptors=chain_descriptors,
                n_components=n_components,
            )
        )

    return results