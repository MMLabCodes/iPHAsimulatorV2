#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 11:41:37 2026

@author: daniel

DBSCAN clustering utilities for PCA-reduced polymer conformations.

This module provides automatic DBSCAN epsilon estimation using
nearest-neighbour k-distance curves and knee-point detection.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from kneed import KneeLocator
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors

from ..pca import ChainPCAResult


# =============================================================================
# Result containers
# =============================================================================

@dataclass(frozen=True)
class EpsilonEstimate:
    """
    Automatic DBSCAN epsilon estimate.

    Attributes
    ----------
    eps : float
        Estimated DBSCAN epsilon value.

    neighbor_rank : int
        Nearest-neighbour rank used to construct the k-distance curve.

    distances : numpy.ndarray
        Sorted k-nearest-neighbour distances.

    knee_index : int | None
        Index of the detected knee in the sorted distance curve.
        None if knee detection fails and the percentil fallback is used.
    """

    eps: float
    neighbor_rank: int
    distances: np.ndarray
    knee_index: int | None


@dataclass(frozen=True)
class ChainClusteringResult:
    """
    DBSCAN clustering result for one polymer chain.

    Attributes
    ----------
    segment_id : str
        Segment identifier corresponding to the polymer chain.

    frame_indices : numpy.ndarray
        Original trajectory frame indices represented in the clustering.

    labels : numpy.ndarray
        DBSCAN cluster labels.

        Noise points are labelled -1.

    eps : float
        DBSCAN epsilon value used.

    min_samples : int
        DBSCAN minimum-samples parameter.

    n_clusters : int
        Number of non-noise clusters.

    noise_fraction : float
        Fraction of samples labelled as noise.

    epsilon_estimate : EpsilonEstimate
        Information from the automatic epsilon estimation.
    """

    segment_id: str
    frame_indices: np.ndarray
    labels: np.ndarray
    eps: float
    min_samples: int
    n_clusters: int
    noise_fraction: float
    epsilon_estimate: EpsilonEstimate


# =============================================================================
# Automatic epsilon estimation
# =============================================================================

def estimate_dbscan_eps(
    transformed_data: np.ndarray,
    k: int = 6,
    n_temperatures: int = 57,
) -> EpsilonEstimate:
    """
    Estimate DBSCAN epsilon using the historical k-distance knee method.

    Parameters
    ----------
    transformed_data
        PCA-transformed conformational data.

    k
        Number of nearest neighbours used for the k-distance curve.

    n_temperatures
        Number of nominal temperature blocks in the cooling trajectory.
        Used to reproduce the historical trimming of the lowest portion
        of the sorted k-distance distribution.

    Returns
    -------
    EpsilonEstimate
        Estimated epsilon and diagnostic information.
    """

    transformed_data = np.asarray(
        transformed_data,
        dtype=float,
    )

    if transformed_data.ndim != 2:
        raise ValueError(
            "transformed_data must be a 2D array."
        )

    n_samples = transformed_data.shape[0]

    if n_samples < 2:
        raise ValueError(
            "At least two samples are required."
        )

    if k < 2:
        raise ValueError(
            "k must be at least 2."
        )

    if k > n_samples:
        raise ValueError(
            "k cannot exceed the number of samples."
        )

    if n_temperatures <= 0:
        raise ValueError(
            "n_temperatures must be positive."
        )

    if not np.isfinite(transformed_data).all():
        raise ValueError(
            "transformed_data contains non-finite values."
        )

    # ---------------------------------------------------------
    # Historical k-nearest-neighbour distance calculation
    # ---------------------------------------------------------

    nbrs = NearestNeighbors(
        n_neighbors=k
    ).fit(transformed_data)

    distances, _ = nbrs.kneighbors(
        transformed_data
    )

    # Historical implementation:
    # use the final returned neighbour distance
    k_distances = np.sort(
        distances[:, k - 1]
    )

    # ---------------------------------------------------------
    # Historical trimming
    # ---------------------------------------------------------

    omit_n = int(
        n_samples / n_temperatures
    )

    k_distances_trimmed = k_distances[
        omit_n:
    ]

    if len(k_distances_trimmed) < 2:
        raise ValueError(
            "Too few k-distance values remain after trimming."
        )

    x_trimmed = np.arange(
        len(k_distances_trimmed)
    )

    # ---------------------------------------------------------
    # Historical KneeLocator configuration
    # ---------------------------------------------------------

    kneedle = KneeLocator(
        x_trimmed,
        k_distances_trimmed,
        S=1.0,
        curve="convex",
        direction="increasing",
        online=True,
    )

    eps = kneedle.knee_y

    # Historical fallback
    if eps is None or not np.isfinite(eps):
        eps = float(
            np.percentile(
                k_distances_trimmed,
                90,
            )
        )

        knee_index = None

    else:
        eps = float(eps)

        # Convert knee location back to an integer index
        # within the trimmed array.
        knee_index = (
            int(kneedle.knee)
            if kneedle.knee is not None
            else None
        )

    if eps <= 0:
        raise ValueError(
            "Estimated DBSCAN epsilon must be positive."
        )

    return EpsilonEstimate(
        eps=eps,
        neighbor_rank=k,
        distances=k_distances_trimmed,
        knee_index=knee_index,
    )


# =============================================================================
# Single-chain clustering
# =============================================================================

def cluster_chain_pca(
    pca_result: ChainPCAResult,
    k: int = 6,
    min_samples: int = 6,
    n_temperatures: int = 57,
) -> ChainClusteringResult:

    epsilon_estimate = estimate_dbscan_eps(
        transformed_data=pca_result.transformed_data,
        k=k,
        n_temperatures=n_temperatures,
    )

    dbscan = DBSCAN(
        eps=epsilon_estimate.eps,
        min_samples=min_samples,
    )

    labels = dbscan.fit_predict(
        pca_result.transformed_data
    )

    unique_labels = set(labels)

    n_clusters = len(
        unique_labels - {-1}
    )

    noise_fraction = float(
        np.mean(labels == -1)
    )

    return ChainClusteringResult(
        segment_id=pca_result.segment_id,
        frame_indices=pca_result.frame_indices.copy(),
        labels=labels,
        eps=epsilon_estimate.eps,
        min_samples=min_samples,
        n_clusters=n_clusters,
        noise_fraction=noise_fraction,
        epsilon_estimate=epsilon_estimate,
    )


# =============================================================================
# All-chain clustering
# =============================================================================

def cluster_all_chain_pca(
    pca_results: dict[str, ChainPCAResult],
    k: int = 6,
    min_samples: int = 6,
    n_temperatures: int = 57,
) -> dict[str, ChainClusteringResult]:
    """
    Cluster PCA results independently for all polymer chains.

    Parameters
    ----------
    pca_results : dict
        Dictionary mapping segment IDs to ChainPCAResult objects.

    k : int, optional
        Number of nearest neighbours used to construct the
        k-distance curve for automatic epsilon estimation.

        Default:
            6

    min_samples : int, optional
        DBSCAN minimum-samples parameter.

        Default:
            6

    n_temperatures : int, optional
        Number of nominal temperature blocks represented in the
        trajectory.

        Default:
            57

    Returns
    -------
    dict
        Dictionary mapping segment IDs to ChainClusteringResult objects.

    Raises
    ------
    ValueError
        If no PCA results are supplied.
    """

    if not pca_results:
        raise ValueError(
            "No PCA results were supplied."
        )

    results = {}

    for segment_id, pca_result in pca_results.items():

        results[segment_id] = cluster_chain_pca(
            pca_result=pca_result,
            k=k,
            min_samples=min_samples,
            n_temperatures=n_temperatures,
        )

    return results