#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 11:36:49 2026

@author: daniel

Provisional glass-transition response construction.

This module contains diagnostic utilities for converting clustering results
into a temperature-dependent response suitable for preliminary Tg fitting.

The current implementation reproduces the historical cluster-label response
and should not yet be treated as the final Tg observable.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .clustering import ChainClusteringResult


@dataclass(frozen=True)
class TemperatureResponse:
    """Temperature-dependent clustering response."""

    temperatures: np.ndarray
    response: np.ndarray
    counts: np.ndarray


def calculate_historical_cluster_response(
    clustering_results: dict[str, ChainClusteringResult],
    temperature_assignment: pd.DataFrame,
) -> TemperatureResponse:
    """
    Calculate the historical cluster-label response as a function of temperature.

    Cluster labels are associated with their original trajectory frames and
    grouped by nominal temperature. Mean numerical DBSCAN labels are then
    calculated across all chains and sampled conformations.

    Notes
    -----
    This reproduces the historical analysis behaviour for diagnostic purposes.
    DBSCAN cluster labels are categorical identifiers, so this response should
    not yet be interpreted as a physically rigorous order parameter.
    """

    records = []

    frame_to_temperature = dict(
        zip(
            temperature_assignment["Frame"],
            temperature_assignment["Nominal Temperature (K)"],
        )
    )

    for segment_id, result in clustering_results.items():

        for frame_index, label in zip(
            result.frame_indices,
            result.labels,
        ):

            if frame_index not in frame_to_temperature:
                continue

            records.append(
                {
                    "Segment": segment_id,
                    "Frame": frame_index,
                    "Temperature": frame_to_temperature[frame_index],
                    "Cluster Label": label,
                }
            )

    if not records:
        raise ValueError(
            "No clustering observations could be matched to temperatures."
        )

    data = pd.DataFrame(records)

    grouped = (
        data
        .groupby("Temperature")
        ["Cluster Label"]
        .agg(["mean", "count"])
        .sort_index(ascending=False)
    )

    return TemperatureResponse(
        temperatures=grouped.index.to_numpy(dtype=float),
        response=grouped["mean"].to_numpy(dtype=float),
        counts=grouped["count"].to_numpy(dtype=int),
    )

from scipy.optimize import curve_fit


@dataclass(frozen=True)
class TgFitResult:
    """Result of the provisional Tg transition fit."""

    tg: float
    C: float
    s: float
    d: float
    temperatures: np.ndarray
    fitted_response: np.ndarray


def _historical_transition_function(
    temperature,
    C,
    s,
    d,
):
    return (
        C / 2.0
        * (1.0 - np.tanh(s * temperature - d))
        - 1.0
    )


def fit_historical_tg(
    temperature_response: TemperatureResponse,
) -> TgFitResult:
    """
    Fit the historical tanh transition model and estimate Tg.

    This reproduces the fitting procedure used in the original
    Tg analysis workflow.

    Tg is defined as:

        Tg = d / s
    """

    temperatures = np.asarray(
        temperature_response.temperatures,
        dtype=float,
    )

    response = np.asarray(
        temperature_response.response,
        dtype=float,
    )

    if len(temperatures) < 4:
        raise ValueError(
            "At least four temperature points are required for Tg fitting."
        )

    if not np.isfinite(temperatures).all():
        raise ValueError(
            "Temperature values contain non-finite values."
        )

    if not np.isfinite(response).all():
        raise ValueError(
            "Temperature response contains non-finite values."
        )

    # ---------------------------------------------------------------------
    # Historical ordering
    # ---------------------------------------------------------------------

    order = np.argsort(
        temperatures
    )

    temperatures_sorted = temperatures[
        order
    ]

    response_sorted = response[
        order
    ]

    # ---------------------------------------------------------------------
    # Historical initial parameter estimates
    # ---------------------------------------------------------------------

    n_end = max(
        1,
        len(response_sorted) // 5,
    )

    response_low_temperature = np.mean(
        response_sorted[:n_end]
    )

    response_high_temperature = np.mean(
        response_sorted[-n_end:]
    )

    C0 = max(
        0.2,
        abs(
            response_low_temperature
            - response_high_temperature
        ),
    )

    tg0 = np.median(
        temperatures_sorted
    )

    s0 = 0.05

    d0 = s0 * tg0

    initial_guess = [
        C0,
        s0,
        d0,
    ]

    # ---------------------------------------------------------------------
    # Historical parameter bounds
    # ---------------------------------------------------------------------

    bounds = (
        [
            1e-6,   # C > 0
            1e-6,   # s > 0
            -np.inf,
        ],
        [
            np.inf,
            np.inf,
            np.inf,
        ],
    )

    # ---------------------------------------------------------------------
    # Fit transition function
    # ---------------------------------------------------------------------

    parameters, _ = curve_fit(
        _historical_transition_function,
        temperatures_sorted,
        response_sorted,
        p0=initial_guess,
        bounds=bounds,
        maxfev=20000,
    )

    C, s, d = parameters

    tg = d / s

    fitted_response = (
        _historical_transition_function(
            temperatures_sorted,
            C,
            s,
            d,
        )
    )

    return TgFitResult(
        tg=float(tg),
        C=float(C),
        s=float(s),
        d=float(d),
        temperatures=temperatures_sorted,
        fitted_response=fitted_response,
    )