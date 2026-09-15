#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Optimisation utilities for iPHAsimulator analysis.

This module treats PCA dimensionality selection and DBSCAN parameter
selection as two separate optimisation problems.

PCA dimensionality
------------------
PCA dimensionality is assessed directly from the PCA variance spectrum.
DBSCAN clustering is not used to determine the number of principal
components.

Diagnostics include:

- explained variance per principal component;
- cumulative explained variance;
- scree-curve elbow position;
- participation ratio;
- entropy-based effective rank.

A system-level PCA dimensionality is selected from the median scree elbow
across all polymer chains.

DBSCAN optimisation
-------------------
Once the PCA dimensionality has been selected, DBSCAN parameters are
assessed independently.

The neighbour rank used for epsilon estimation follows:

    k = n_components + 1

where n_components is the selected PCA dimensionality.

The DBSCAN min_samples parameter is then evaluated across polymer chains.
Selection is based on clustering stability while also requiring the
clustering to remain non-trivial.

This prevents a high min_samples value from being selected simply because
the clustering has collapsed to one cluster plus noise.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from kneed import KneeLocator
from sklearn.metrics import adjusted_rand_score

from .descriptors import ChainDistanceDescriptors
from .pca import ChainPCAResult, calculate_chain_pca
from .clustering import cluster_chain_pca


# =============================================================================
# PCA result containers
# =============================================================================

@dataclass(frozen=True)
class ChainPCADimensionalityResult:
    """
    PCA dimensionality diagnostics for one polymer chain.
    """

    segment_id: str

    component_numbers: np.ndarray

    explained_variance_ratio: np.ndarray
    cumulative_explained_variance: np.ndarray

    elbow_component: int | None

    participation_ratio: float
    effective_rank: float

    max_components: int


@dataclass(frozen=True)
class PCAOptimisationResult:
    """
    System-level PCA dimensionality optimisation result.
    """

    selected_components: int

    median_elbow: float
    mean_elbow: float

    elbow_q1: float
    elbow_q3: float
    elbow_iqr: float

    fraction_within_one_component: float

    chain_results: dict[
        str,
        ChainPCADimensionalityResult,
    ]

    spectra_dataframe: pd.DataFrame
    dimensionality_dataframe: pd.DataFrame


# =============================================================================
# DBSCAN result containers
# =============================================================================

@dataclass(frozen=True)
class DBSCANParameterResult:
    """
    DBSCAN result for one min_samples value.

    Attributes
    ----------
    segment_id : str
        Polymer-chain segment identifier.

    n_components : int
        PCA dimensionality.

    k : int
        Neighbour rank used for epsilon estimation.

    min_samples : int
        DBSCAN minimum-samples parameter.

    eps : float
        Automatically estimated epsilon.

    n_clusters : int
        Number of non-noise clusters.

    noise_fraction : float
        Fraction of samples assigned to DBSCAN noise.

    labels : np.ndarray
        DBSCAN labels.
    """

    segment_id: str

    n_components: int

    k: int

    min_samples: int

    eps: float

    n_clusters: int

    noise_fraction: float

    labels: np.ndarray


@dataclass(frozen=True)
class DBSCANOptimisationResult:
    """
    System-level DBSCAN optimisation result.
    """

    n_components: int

    k: int

    selected_min_samples: int

    parameter_dataframe: pd.DataFrame

    stability_dataframe: pd.DataFrame

    summary_dataframe: pd.DataFrame


# =============================================================================
# PCA dimensionality utilities
# =============================================================================

def _calculate_scree_elbow(
    explained_variance_ratio: np.ndarray,
) -> int | None:
    """
    Estimate the elbow of a PCA scree curve.

    Parameters
    ----------
    explained_variance_ratio : np.ndarray
        Explained variance ratios ordered from PC1 onwards.

    Returns
    -------
    int or None
        Principal-component number corresponding to the estimated elbow.

        Returns None when no elbow is detected.
    """

    variance = np.asarray(
        explained_variance_ratio,
        dtype=float,
    )

    component_numbers = np.arange(
        1,
        len(variance) + 1,
    )

    knee = KneeLocator(
        component_numbers,
        variance,
        curve="convex",
        direction="decreasing",
        S=1.0,
    )

    if knee.knee is None:
        return None

    return int(
        knee.knee
    )


def _calculate_participation_ratio(
    explained_variance_ratio: np.ndarray,
) -> float:
    """
    Calculate the participation ratio of a PCA spectrum.

    The participation ratio is:

        PR = (sum(lambda_i))^2 / sum(lambda_i^2)

    where lambda_i are the variance contributions of the analysed
    principal components.

    Notes
    -----
    When only the first N principal components are supplied, this is a
    truncated-spectrum participation ratio rather than the full intrinsic
    dimensionality of the original descriptor space.
    """

    variance = np.asarray(
        explained_variance_ratio,
        dtype=float,
    )

    total = np.sum(
        variance
    )

    if total <= 0:
        return np.nan

    denominator = np.sum(
        variance**2
    )

    if denominator <= 0:
        return np.nan

    return float(
        total**2
        / denominator
    )


def _calculate_effective_rank(
    explained_variance_ratio: np.ndarray,
) -> float:
    """
    Calculate entropy-based effective rank of a PCA spectrum.

    The effective rank is:

        exp(-sum(p_i * ln(p_i)))

    where p_i are normalised variance contributions.

    Notes
    -----
    This value refers to the analysed PCA spectrum. If the spectrum is
    truncated to the first N components, the resulting effective rank is
    likewise a truncated-spectrum diagnostic.
    """

    variance = np.asarray(
        explained_variance_ratio,
        dtype=float,
    )

    total = np.sum(
        variance
    )

    if total <= 0:
        return np.nan

    probabilities = (
        variance
        / total
    )

    probabilities = probabilities[
        probabilities > 0
    ]

    entropy = -np.sum(
        probabilities
        * np.log(
            probabilities
        )
    )

    return float(
        np.exp(
            entropy
        )
    )


def analyse_chain_pca_dimensionality(
    chain_descriptors: ChainDistanceDescriptors,
    max_components: int = 20,
) -> ChainPCADimensionalityResult:
    """
    Analyse PCA dimensionality for one polymer chain.

    PCA is calculated once using the requested maximum number of
    components.

    The resulting variance spectrum is then used to estimate dimensionality
    without involving DBSCAN.

    Parameters
    ----------
    chain_descriptors : ChainDistanceDescriptors
        Structural descriptor matrix for one polymer chain.

    max_components : int, optional
        Maximum number of principal components to analyse.

        Default:
            20

    Returns
    -------
    ChainPCADimensionalityResult
        PCA spectrum and dimensionality diagnostics.
    """

    if max_components < 2:
        raise ValueError(
            "max_components must be at least 2."
        )

    n_samples = (
        chain_descriptors
        .descriptors
        .shape[0]
    )

    n_features = (
        chain_descriptors
        .descriptors
        .shape[1]
    )

    available_components = min(
        n_samples,
        n_features,
    )

    n_components = min(
        max_components,
        available_components,
    )

    pca_result = calculate_chain_pca(
        chain_descriptors=chain_descriptors,
        n_components=n_components,
    )

    variance = np.asarray(
        pca_result.explained_variance_ratio,
        dtype=float,
    )

    cumulative = np.asarray(
        pca_result.cumulative_explained_variance,
        dtype=float,
    )

    component_numbers = np.arange(
        1,
        len(variance) + 1,
    )

    elbow_component = (
        _calculate_scree_elbow(
            variance
        )
    )

    participation_ratio = (
        _calculate_participation_ratio(
            variance
        )
    )

    effective_rank = (
        _calculate_effective_rank(
            variance
        )
    )

    return ChainPCADimensionalityResult(
        segment_id=(
            chain_descriptors.segment_id
        ),
        component_numbers=(
            component_numbers
        ),
        explained_variance_ratio=(
            variance
        ),
        cumulative_explained_variance=(
            cumulative
        ),
        elbow_component=(
            elbow_component
        ),
        participation_ratio=(
            participation_ratio
        ),
        effective_rank=(
            effective_rank
        ),
        max_components=(
            n_components
        ),
    )


def analyse_all_chain_pca_dimensionality(
    descriptors_by_segment:
    dict[str, ChainDistanceDescriptors],
    max_components: int = 20,
) -> dict[
    str,
    ChainPCADimensionalityResult,
]:
    """
    Analyse PCA dimensionality independently for every polymer chain.
    """

    if not descriptors_by_segment:
        raise ValueError(
            "No descriptor results were supplied."
        )

    results = {}

    for (
        segment_id,
        chain_descriptors,
    ) in descriptors_by_segment.items():

        results[segment_id] = (
            analyse_chain_pca_dimensionality(
                chain_descriptors=(
                    chain_descriptors
                ),
                max_components=(
                    max_components
                ),
            )
        )

    return results


# =============================================================================
# PCA DataFrames
# =============================================================================

def pca_spectra_to_dataframe(
    results:
    dict[
        str,
        ChainPCADimensionalityResult,
    ],
) -> pd.DataFrame:
    """
    Convert per-chain PCA spectra to a long-form DataFrame.
    """

    records = []

    for (
        segment_id,
        result,
    ) in results.items():

        for (
            component,
            variance,
            cumulative,
        ) in zip(
            result.component_numbers,
            result.explained_variance_ratio,
            result.cumulative_explained_variance,
        ):

            records.append(
                {
                    "Segment":
                        segment_id,

                    "PC":
                        int(
                            component
                        ),

                    "Explained Variance":
                        float(
                            variance
                        ),

                    "Cumulative Variance":
                        float(
                            cumulative
                        ),
                }
            )

    return (
        pd.DataFrame(
            records
        )
        .sort_values(
            [
                "PC",
                "Segment",
            ]
        )
        .reset_index(
            drop=True
        )
    )


def pca_dimensionality_to_dataframe(
    results:
    dict[
        str,
        ChainPCADimensionalityResult,
    ],
) -> pd.DataFrame:
    """
    Convert chain-level dimensionality estimates to a DataFrame.
    """

    records = []

    for (
        segment_id,
        result,
    ) in results.items():

        records.append(
            {
                "Segment":
                    segment_id,

                "Elbow PC":
                    result.elbow_component,

                "Participation Ratio":
                    result.participation_ratio,

                "Effective Rank":
                    result.effective_rank,

                "Analysed PCs":
                    result.max_components,
            }
        )

    return (
        pd.DataFrame(
            records
        )
        .sort_values(
            "Segment"
        )
        .reset_index(
            drop=True
        )
    )


def summarise_pca_spectrum(
    spectra_dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Summarise PCA spectra across polymer chains.

    Median values are used as the central summary because individual
    polymer chains may sample different conformational distributions.
    """

    if spectra_dataframe.empty:
        raise ValueError(
            "PCA spectra DataFrame is empty."
        )

    return (
        spectra_dataframe
        .groupby(
            "PC",
            as_index=False,
        )
        .agg(
            median_explained_variance=(
                "Explained Variance",
                "median",
            ),

            mean_explained_variance=(
                "Explained Variance",
                "mean",
            ),

            median_cumulative_variance=(
                "Cumulative Variance",
                "median",
            ),

            mean_cumulative_variance=(
                "Cumulative Variance",
                "mean",
            ),
        )
    )


def summarise_pca_dimensionality(
    dimensionality_dataframe:
    pd.DataFrame,
) -> dict[str, float]:
    """
    Summarise chain-level PCA dimensionality diagnostics.
    """

    if dimensionality_dataframe.empty:
        raise ValueError(
            "PCA dimensionality DataFrame is empty."
        )

    elbows = (
        dimensionality_dataframe[
            "Elbow PC"
        ]
        .dropna()
        .astype(
            float
        )
    )

    summary = {
        "median_elbow_pc":
            (
                float(
                    elbows.median()
                )
                if not elbows.empty
                else np.nan
            ),

        "mean_elbow_pc":
            (
                float(
                    elbows.mean()
                )
                if not elbows.empty
                else np.nan
            ),

        "median_participation_ratio":
            float(
                dimensionality_dataframe[
                    "Participation Ratio"
                ]
                .median()
            ),

        "median_effective_rank":
            float(
                dimensionality_dataframe[
                    "Effective Rank"
                ]
                .median()
            ),
    }

    return summary


# =============================================================================
# PCA optimisation
# =============================================================================

def optimise_pca_dimensionality(
    descriptors_by_segment:
    dict[str, ChainDistanceDescriptors],
    max_components: int = 20,
) -> PCAOptimisationResult:
    """
    Determine a system-level PCA dimensionality.

    PCA dimensionality is estimated independently for each polymer chain
    using the scree-curve elbow.

    The system-level dimensionality is selected as the rounded median
    chain-level elbow.

    DBSCAN is not involved in this optimisation.

    Parameters
    ----------
    descriptors_by_segment : dict
        Structural descriptors for each polymer chain.

    max_components : int, optional
        Maximum number of PCA components included in the diagnostic.

    Returns
    -------
    PCAOptimisationResult
        System-level PCA dimensionality and supporting diagnostics.
    """

    chain_results = (
        analyse_all_chain_pca_dimensionality(
            descriptors_by_segment=(
                descriptors_by_segment
            ),
            max_components=(
                max_components
            ),
        )
    )

    spectra_dataframe = (
        pca_spectra_to_dataframe(
            chain_results
        )
    )

    dimensionality_dataframe = (
        pca_dimensionality_to_dataframe(
            chain_results
        )
    )

    elbows = (
        dimensionality_dataframe[
            "Elbow PC"
        ]
        .dropna()
        .astype(
            float
        )
        .to_numpy()
    )

    if len(
        elbows
    ) == 0:

        raise RuntimeError(
            "No PCA scree elbows could be identified."
        )

    median_elbow = float(
        np.median(
            elbows
        )
    )

    mean_elbow = float(
        np.mean(
            elbows
        )
    )

    elbow_q1 = float(
        np.percentile(
            elbows,
            25,
        )
    )

    elbow_q3 = float(
        np.percentile(
            elbows,
            75,
        )
    )

    elbow_iqr = (
        elbow_q3
        - elbow_q1
    )

    selected_components = int(
        np.floor(
            median_elbow
            + 0.5
        )
    )

    selected_components = max(
        1,
        selected_components,
    )

    fraction_within_one_component = float(
        np.mean(
            np.abs(
                elbows
                - selected_components
            )
            <= 1
        )
    )

    return PCAOptimisationResult(
        selected_components=(
            selected_components
        ),
        median_elbow=(
            median_elbow
        ),
        mean_elbow=(
            mean_elbow
        ),
        elbow_q1=(
            elbow_q1
        ),
        elbow_q3=(
            elbow_q3
        ),
        elbow_iqr=(
            elbow_iqr
        ),
        fraction_within_one_component=(
            fraction_within_one_component
        ),
        chain_results=(
            chain_results
        ),
        spectra_dataframe=(
            spectra_dataframe
        ),
        dimensionality_dataframe=(
            dimensionality_dataframe
        ),
    )


def calculate_optimised_pca(
    descriptors_by_segment:
    dict[str, ChainDistanceDescriptors],
    optimisation_result:
    PCAOptimisationResult,
) -> dict[
    str,
    ChainPCAResult,
]:
    """
    Calculate PCA for every polymer chain using the selected
    system-level dimensionality.
    """

    if not descriptors_by_segment:
        raise ValueError(
            "No descriptor results were supplied."
        )

    n_components = (
        optimisation_result
        .selected_components
    )

    results = {}

    for (
        segment_id,
        descriptors,
    ) in descriptors_by_segment.items():

        results[segment_id] = (
            calculate_chain_pca(
                chain_descriptors=(
                    descriptors
                ),
                n_components=(
                    n_components
                ),
            )
        )

    return results


# =============================================================================
# DBSCAN utilities
# =============================================================================

def get_dbscan_neighbor_rank(
    n_components: int,
) -> int:
    """
    Determine the neighbour rank used for epsilon estimation.

    The dimensionality-dependent relationship is:

        k = n_components + 1
    """

    if n_components < 1:
        raise ValueError(
            "n_components must be at least 1."
        )

    return (
        n_components
        + 1
    )


def analyse_chain_dbscan_parameters(
    pca_result: ChainPCAResult,
    min_samples_values=range(
        2,
        11,
    ),
    n_temperatures: int = 57,
) -> dict[
    int,
    DBSCANParameterResult,
]:
    """
    Evaluate DBSCAN min_samples values for one fixed PCA representation.

    The PCA dimensionality is not changed during this analysis.

    Epsilon is automatically estimated using:

        k = n_components + 1

    Parameters
    ----------
    pca_result : ChainPCAResult
        PCA representation using an already selected dimensionality.

    min_samples_values : iterable of int
        Candidate DBSCAN minimum-samples values.

    n_temperatures : int
        Number of nominal temperature blocks.

    Returns
    -------
    dict
        Mapping min_samples values to DBSCAN diagnostics.
    """

    n_components = (
        pca_result
        .n_components
    )

    k = (
        get_dbscan_neighbor_rank(
            n_components
        )
    )

    results = {}

    for min_samples in min_samples_values:

        min_samples = int(
            min_samples
        )

        if min_samples < 2:
            raise ValueError(
                "min_samples must be at least 2."
            )

        clustering = (
            cluster_chain_pca(
                pca_result=(
                    pca_result
                ),
                k=(
                    k
                ),
                min_samples=(
                    min_samples
                ),
                n_temperatures=(
                    n_temperatures
                ),
            )
        )

        results[min_samples] = (
            DBSCANParameterResult(
                segment_id=(
                    pca_result.segment_id
                ),
                n_components=(
                    n_components
                ),
                k=(
                    k
                ),
                min_samples=(
                    min_samples
                ),
                eps=(
                    clustering.eps
                ),
                n_clusters=(
                    clustering.n_clusters
                ),
                noise_fraction=(
                    clustering.noise_fraction
                ),
                labels=(
                    clustering.labels.copy()
                ),
            )
        )

    return results


def analyse_all_chain_dbscan_parameters(
    pca_results:
    dict[
        str,
        ChainPCAResult,
    ],
    min_samples_values=range(
        2,
        11,
    ),
    n_temperatures: int = 57,
) -> dict[
    str,
    dict[
        int,
        DBSCANParameterResult,
    ],
]:
    """
    Evaluate DBSCAN min_samples values for every polymer chain.

    PCA dimensionality remains fixed throughout the analysis.
    """

    if not pca_results:
        raise ValueError(
            "No PCA results were supplied."
        )

    results = {}

    for (
        segment_id,
        pca_result,
    ) in pca_results.items():

        results[segment_id] = (
            analyse_chain_dbscan_parameters(
                pca_result=(
                    pca_result
                ),
                min_samples_values=(
                    min_samples_values
                ),
                n_temperatures=(
                    n_temperatures
                ),
            )
        )

    return results


# =============================================================================
# DBSCAN DataFrames
# =============================================================================

def dbscan_parameters_to_dataframe(
    results:
    dict[
        str,
        dict[
            int,
            DBSCANParameterResult,
        ],
    ],
) -> pd.DataFrame:
    """
    Convert DBSCAN parameter results into a DataFrame.
    """

    records = []

    for (
        segment_id,
        chain_results,
    ) in results.items():

        for (
            min_samples,
            result,
        ) in chain_results.items():

            records.append(
                {
                    "Segment":
                        segment_id,

                    "PCs":
                        result.n_components,

                    "k":
                        result.k,

                    "Min Samples":
                        min_samples,

                    "Epsilon":
                        result.eps,

                    "Clusters":
                        result.n_clusters,

                    "Noise Fraction":
                        result.noise_fraction,
                }
            )

    return (
        pd.DataFrame(
            records
        )
        .sort_values(
            [
                "Min Samples",
                "Segment",
            ]
        )
        .reset_index(
            drop=True
        )
    )


# =============================================================================
# DBSCAN adjacent stability
# =============================================================================

def compare_adjacent_min_samples(
    parameter_results:
    dict[
        int,
        DBSCANParameterResult,
    ],
) -> pd.DataFrame:
    """
    Compare DBSCAN solutions for adjacent min_samples values.

    Adjusted Rand Index is used to assess clustering stability while the
    PCA representation, k and epsilon-estimation procedure remain fixed.
    """

    values = sorted(
        parameter_results
    )

    records = []

    for (
        lower,
        upper,
    ) in zip(
        values[:-1],
        values[1:],
    ):

        lower_result = (
            parameter_results[
                lower
            ]
        )

        upper_result = (
            parameter_results[
                upper
            ]
        )

        ari_all = (
            adjusted_rand_score(
                lower_result.labels,
                upper_result.labels,
            )
        )

        common_clustered = (
            (
                lower_result.labels
                != -1
            )
            &
            (
                upper_result.labels
                != -1
            )
        )

        overlap_fraction = float(
            np.mean(
                common_clustered
            )
        )

        if (
            np.sum(
                common_clustered
            )
            >= 2
        ):

            ari_clustered = (
                adjusted_rand_score(
                    lower_result.labels[
                        common_clustered
                    ],
                    upper_result.labels[
                        common_clustered
                    ],
                )
            )

        else:

            ari_clustered = (
                np.nan
            )

        records.append(
            {
                "Min Samples":
                    lower,

                "Next Min Samples":
                    upper,

                "ARI All":
                    float(
                        ari_all
                    ),

                "ARI Clustered":
                    float(
                        ari_clustered
                    ),

                "Clustered Overlap Fraction":
                    overlap_fraction,

                "Noise Fraction":
                    lower_result.noise_fraction,

                "Next Noise Fraction":
                    upper_result.noise_fraction,

                "Clusters":
                    lower_result.n_clusters,

                "Next Clusters":
                    upper_result.n_clusters,

                "Epsilon":
                    lower_result.eps,
            }
        )

    return pd.DataFrame(
        records
    )


def calculate_all_chain_dbscan_stability(
    parameter_results:
    dict[
        str,
        dict[
            int,
            DBSCANParameterResult,
        ],
    ],
) -> pd.DataFrame:
    """
    Calculate adjacent min_samples stability for every polymer chain.
    """

    frames = []

    for (
        segment_id,
        chain_results,
    ) in parameter_results.items():

        stability = (
            compare_adjacent_min_samples(
                chain_results
            )
        )

        stability.insert(
            0,
            "Segment",
            segment_id,
        )

        frames.append(
            stability
        )

    if not frames:
        return pd.DataFrame()

    return pd.concat(
        frames,
        ignore_index=True,
    )


# =============================================================================
# DBSCAN parameter summary
# =============================================================================

def summarise_dbscan_parameters(
    parameter_dataframe: pd.DataFrame,
    high_noise_threshold: float = 0.90,
) -> pd.DataFrame:
    """
    Summarise DBSCAN behaviour across polymer chains for each min_samples.

    Parameters
    ----------
    parameter_dataframe : pd.DataFrame
        Chain-level DBSCAN results produced by
        ``dbscan_parameters_to_dataframe``.

    high_noise_threshold : float, optional
        Noise fraction above which a chain is classified as having a
        high-noise DBSCAN solution.

        Default:
            0.90

    Returns
    -------
    pd.DataFrame
        System-level DBSCAN diagnostics for each min_samples value.

    Notes
    -----
    ``fraction_multicluster`` gives the fraction of polymer chains that
    retain at least two non-noise DBSCAN clusters.

    ``fraction_single_cluster`` gives the fraction of polymer chains with
    exactly one non-noise cluster.

    ``fraction_zero_clusters`` gives the fraction of polymer chains for
    which all sampled conformations are classified as noise.

    ``fraction_high_noise`` gives the fraction of polymer chains whose
    noise fraction exceeds ``high_noise_threshold``.
    """

    if parameter_dataframe.empty:
        raise ValueError(
            "DBSCAN parameter DataFrame is empty."
        )

    records = []

    grouped = (
        parameter_dataframe
        .groupby(
            "Min Samples"
        )
    )

    for (
        min_samples,
        group,
    ) in grouped:

        cluster_counts = (
            group[
                "Clusters"
            ]
            .to_numpy(
                dtype=float
            )
        )

        noise_fractions = (
            group[
                "Noise Fraction"
            ]
            .to_numpy(
                dtype=float
            )
        )

        records.append(
            {
                "Min Samples":
                    int(
                        min_samples
                    ),

                "median_noise_fraction":
                    float(
                        np.median(
                            noise_fractions
                        )
                    ),

                "mean_noise_fraction":
                    float(
                        np.mean(
                            noise_fractions
                        )
                    ),

                "median_clusters":
                    float(
                        np.median(
                            cluster_counts
                        )
                    ),

                "mean_clusters":
                    float(
                        np.mean(
                            cluster_counts
                        )
                    ),

                "fraction_multicluster":
                    float(
                        np.mean(
                            cluster_counts
                            >= 2
                        )
                    ),

                "fraction_single_cluster":
                    float(
                        np.mean(
                            cluster_counts
                            == 1
                        )
                    ),

                "fraction_zero_clusters":
                    float(
                        np.mean(
                            cluster_counts
                            == 0
                        )
                    ),

                "fraction_high_noise":
                    float(
                        np.mean(
                            noise_fractions
                            >= high_noise_threshold
                        )
                    ),
            }
        )

    return (
        pd.DataFrame(
            records
        )
        .sort_values(
            "Min Samples"
        )
        .reset_index(
            drop=True
        )
    )


# =============================================================================
# DBSCAN stability summary
# =============================================================================

def summarise_dbscan_stability(
    stability_dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Summarise adjacent min_samples clustering stability across chains.

    Each row describes the comparison between one min_samples value and
    the next value.

    For example:

        Min Samples = 5

    describes the comparison:

        min_samples = 5
            versus
        min_samples = 6
    """

    if stability_dataframe.empty:
        raise ValueError(
            "DBSCAN stability DataFrame is empty."
        )

    return (
        stability_dataframe
        .groupby(
            "Min Samples",
            as_index=False,
        )
        .agg(
            median_ari_all=(
                "ARI All",
                "median",
            ),

            mean_ari_all=(
                "ARI All",
                "mean",
            ),

            median_ari_clustered=(
                "ARI Clustered",
                "median",
            ),

            median_clustered_overlap=(
                "Clustered Overlap Fraction",
                "median",
            ),

            median_noise_fraction=(
                "Noise Fraction",
                "median",
            ),

            median_next_noise_fraction=(
                "Next Noise Fraction",
                "median",
            ),

            median_clusters=(
                "Clusters",
                "median",
            ),

            median_next_clusters=(
                "Next Clusters",
                "median",
            ),
        )
    )


# =============================================================================
# Combined DBSCAN optimisation summary
# =============================================================================

def build_dbscan_optimisation_summary(
    parameter_dataframe: pd.DataFrame,
    stability_dataframe: pd.DataFrame,
    high_noise_threshold: float = 0.90,
) -> pd.DataFrame:
    """
    Combine DBSCAN structural and stability diagnostics.

    Parameters
    ----------
    parameter_dataframe : pd.DataFrame
        Chain-level DBSCAN parameter results.

    stability_dataframe : pd.DataFrame
        Chain-level adjacent min_samples stability results.

    high_noise_threshold : float, optional
        Chain-level noise fraction above which the result is classified
        as high-noise.

    Returns
    -------
    pd.DataFrame
        Combined system-level DBSCAN optimisation diagnostics.

    Notes
    -----
    The final tested min_samples value has no subsequent value against
    which an adjacent stability comparison can be made.

    Consequently, the final value is not itself a candidate for selection
    through the adjacent-stability criterion.
    """

    parameter_summary = (
        summarise_dbscan_parameters(
            parameter_dataframe=(
                parameter_dataframe
            ),
            high_noise_threshold=(
                high_noise_threshold
            ),
        )
    )

    stability_summary = (
        summarise_dbscan_stability(
            stability_dataframe=(
                stability_dataframe
            )
        )
    )

    summary = (
        stability_summary
        .merge(
            parameter_summary,
            on="Min Samples",
            how="left",
            suffixes=(
                "_stability",
                "_parameter",
            ),
        )
    )

    return (
        summary
        .sort_values(
            "Min Samples"
        )
        .reset_index(
            drop=True
        )
    )


# =============================================================================
# DBSCAN min_samples selection
# =============================================================================

def select_dbscan_min_samples(
    summary_dataframe: pd.DataFrame,
    max_median_noise_fraction: float = 0.95,
    minimum_median_clusters: float = 2.0,
    minimum_next_median_clusters: float = 2.0,
    minimum_multicluster_fraction: float = 0.50,
) -> int:
    """
    Select a stable, non-trivial system-level DBSCAN min_samples value.

    Candidate solutions must first satisfy structural guardrails.

    A candidate is retained only when:

    1. the median noise fraction does not exceed the allowed maximum;
    2. the current median number of non-noise clusters is at least two;
    3. the next min_samples value also retains at least two median
       non-noise clusters;
    4. at least the requested fraction of polymer chains retain two or
       more non-noise clusters.

    Among candidates satisfying those conditions, the value with the
    greatest median adjacent Adjusted Rand Index is selected.

    This prevents a trivially collapsed one-cluster solution from being
    selected simply because its clustering labels are highly stable.

    Parameters
    ----------
    summary_dataframe : pd.DataFrame
        Combined DBSCAN optimisation summary.

    max_median_noise_fraction : float, optional
        Maximum permitted median noise fraction.

        Default:
            0.95

    minimum_median_clusters : float, optional
        Minimum median number of non-noise clusters required for the
        current min_samples value.

        Default:
            2

    minimum_next_median_clusters : float, optional
        Minimum median number of non-noise clusters required after
        increasing min_samples to the next tested value.

        Default:
            2

    minimum_multicluster_fraction : float, optional
        Minimum fraction of polymer chains required to contain at least
        two non-noise clusters.

        Default:
            0.50

    Returns
    -------
    int
        Selected DBSCAN min_samples value.

    Raises
    ------
    RuntimeError
        If no candidate satisfies the non-trivial clustering guardrails.
    """

    if summary_dataframe.empty:
        raise ValueError(
            "DBSCAN optimisation summary is empty."
        )

    required_columns = {
        "Min Samples",
        "median_ari_all",
        "median_noise_fraction_stability",
        "median_clusters_stability",
        "median_next_clusters",
        "fraction_multicluster",
    }

    missing_columns = (
        required_columns
        - set(
            summary_dataframe.columns
        )
    )

    if missing_columns:
        raise ValueError(
            "DBSCAN optimisation summary is missing "
            "required columns: "
            f"{sorted(missing_columns)}"
        )

    candidates = (
        summary_dataframe[
            (
                summary_dataframe[
                    "median_noise_fraction_stability"
                ]
                <= max_median_noise_fraction
            )
            &
            (
                summary_dataframe[
                    "median_clusters_stability"
                ]
                >= minimum_median_clusters
            )
            &
            (
                summary_dataframe[
                    "median_next_clusters"
                ]
                >= minimum_next_median_clusters
            )
            &
            (
                summary_dataframe[
                    "fraction_multicluster"
                ]
                >= minimum_multicluster_fraction
            )
        ]
        .copy()
    )

    if candidates.empty:
        raise RuntimeError(
            "No DBSCAN min_samples candidate satisfied "
            "the non-trivial clustering guardrails. "
            "Inspect the DBSCAN optimisation diagnostics "
            "before continuing."
        )

    best_index = (
        candidates[
            "median_ari_all"
        ]
        .idxmax()
    )

    return int(
        candidates.loc[
            best_index,
            "Min Samples",
        ]
    )


# =============================================================================
# DBSCAN optimisation
# =============================================================================

def optimise_dbscan(
    pca_results:
    dict[
        str,
        ChainPCAResult,
    ],
    min_samples_values=range(
        2,
        11,
    ),
    n_temperatures: int = 57,
    high_noise_threshold: float = 0.90,
    max_median_noise_fraction: float = 0.95,
    minimum_median_clusters: float = 2.0,
    minimum_next_median_clusters: float = 2.0,
    minimum_multicluster_fraction: float = 0.50,
) -> DBSCANOptimisationResult:
    """
    Optimise DBSCAN after PCA dimensionality has been fixed.

    PCA dimensionality is fixed before this function is called.

    The DBSCAN neighbour rank is determined from:

        k = n_components + 1

    Epsilon is estimated independently for each polymer chain using that
    fixed k.

    Candidate min_samples values are then evaluated while PCA
    dimensionality and k remain unchanged.

    Selection favours clustering stability while requiring the DBSCAN
    solution to remain non-trivial.

    Parameters
    ----------
    pca_results : dict
        PCA results for all polymer chains.

        All chains must use the same PCA dimensionality.

    min_samples_values : iterable of int, optional
        DBSCAN min_samples values to evaluate.

        Default:
            range(2, 11)

    n_temperatures : int, optional
        Number of nominal temperature blocks used by the epsilon estimator.

        Default:
            57

    high_noise_threshold : float, optional
        Chain-level noise fraction used to classify a clustering result as
        high-noise.

        Default:
            0.90

    max_median_noise_fraction : float, optional
        Maximum allowed system-level median noise fraction for a candidate
        solution.

        Default:
            0.95

    minimum_median_clusters : float, optional
        Minimum median number of non-noise clusters required for the
        current candidate.

        Default:
            2

    minimum_next_median_clusters : float, optional
        Minimum median number of clusters required for the next tested
        min_samples value.

        This prevents selection immediately before collapse to a
        single-cluster solution.

        Default:
            2

    minimum_multicluster_fraction : float, optional
        Minimum fraction of polymer chains required to contain at least
        two non-noise clusters.

        Default:
            0.50

    Returns
    -------
    DBSCANOptimisationResult
        Selected DBSCAN parameters and all supporting diagnostics.
    """

    if not pca_results:
        raise ValueError(
            "No PCA results were supplied."
        )

    n_components_values = {
        result.n_components
        for result in pca_results.values()
    }

    if len(
        n_components_values
    ) != 1:

        raise ValueError(
            "All polymer chains must use the same "
            "PCA dimensionality."
        )

    n_components = (
        n_components_values.pop()
    )

    k = (
        get_dbscan_neighbor_rank(
            n_components
        )
    )

    # =========================================================================
    # Evaluate DBSCAN parameters for every chain
    # =========================================================================

    parameter_results = (
        analyse_all_chain_dbscan_parameters(
            pca_results=(
                pca_results
            ),
            min_samples_values=(
                min_samples_values
            ),
            n_temperatures=(
                n_temperatures
            ),
        )
    )

    # =========================================================================
    # Convert chain-level parameter results to DataFrame
    # =========================================================================

    parameter_dataframe = (
        dbscan_parameters_to_dataframe(
            parameter_results
        )
    )

    # =========================================================================
    # Calculate adjacent min_samples stability
    # =========================================================================

    stability_dataframe = (
        calculate_all_chain_dbscan_stability(
            parameter_results
        )
    )

    # =========================================================================
    # Build complete system-level diagnostic table
    # =========================================================================

    summary_dataframe = (
        build_dbscan_optimisation_summary(
            parameter_dataframe=(
                parameter_dataframe
            ),
            stability_dataframe=(
                stability_dataframe
            ),
            high_noise_threshold=(
                high_noise_threshold
            ),
        )
    )

    # =========================================================================
    # Select min_samples
    # =========================================================================

    selected_min_samples = (
        select_dbscan_min_samples(
            summary_dataframe=(
                summary_dataframe
            ),
            max_median_noise_fraction=(
                max_median_noise_fraction
            ),
            minimum_median_clusters=(
                minimum_median_clusters
            ),
            minimum_next_median_clusters=(
                minimum_next_median_clusters
            ),
            minimum_multicluster_fraction=(
                minimum_multicluster_fraction
            ),
        )
    )

    return DBSCANOptimisationResult(
        n_components=(
            n_components
        ),
        k=(
            k
        ),
        selected_min_samples=(
            selected_min_samples
        ),
        parameter_dataframe=(
            parameter_dataframe
        ),
        stability_dataframe=(
            stability_dataframe
        ),
        summary_dataframe=(
            summary_dataframe
        ),
    )