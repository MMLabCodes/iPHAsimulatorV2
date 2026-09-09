#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 16:46:29 2026

@author: daniel

Tests for nominal trajectory temperature assignment.
"""

from pathlib import Path

import numpy as np
import pytest

from iphasimulator.analysis.simulation_loader import load_simulation
from iphasimulator.analysis.temperature_assignment import (
    assign_nominal_temperatures,
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

TOTAL_STEPS = 200_000_000
MAX_TEMP = 700
MIN_TEMP = 140
TEMP_CHANGE = 10
REPORTER_FREQ = 1000


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture(scope="module")
def loaded_simulation():
    """Load the cooling simulation once for all tests."""

    return load_simulation(
        system_directory=SYSTEM_DIRECTORY,
        simulation_name=SIMULATION_NAME,
        stage=SIMULATION_STAGE,
    )


@pytest.fixture(scope="module")
def nominal_temperatures(loaded_simulation):
    """Assign nominal temperatures using the historical Tg method."""

    return assign_nominal_temperatures(
        simulation=loaded_simulation,
        total_steps=TOTAL_STEPS,
        max_temp=MAX_TEMP,
        min_temp=MIN_TEMP,
        temp_change=TEMP_CHANGE,
        reporter_freq=REPORTER_FREQ,
    )


# =============================================================================
# Basic assignment tests
# =============================================================================

def test_temperature_assignment_has_one_row_per_frame(
    loaded_simulation,
    nominal_temperatures,
):
    """Check that every trajectory frame receives a nominal temperature."""

    assert len(nominal_temperatures) == len(
        loaded_simulation.universe.trajectory
    )


def test_temperature_assignment_contains_expected_columns(
    nominal_temperatures,
):
    """Check that the expected output columns are present."""

    expected_columns = {
        "Frame",
        "Nominal Step",
        "Nominal Temperature (K)",
    }

    assert expected_columns.issubset(
        nominal_temperatures.columns
    )


def test_frame_indices_are_sequential(
    nominal_temperatures,
):
    """Check that frame numbering begins at zero and is sequential."""

    expected_frames = np.arange(
        len(nominal_temperatures)
    )

    np.testing.assert_array_equal(
        nominal_temperatures["Frame"].to_numpy(),
        expected_frames,
    )


def test_nominal_steps_follow_reporter_frequency(
    nominal_temperatures,
):
    """Check that the historical frame-to-step mapping is reproduced."""

    expected_steps = (
        nominal_temperatures["Frame"].to_numpy()
        * REPORTER_FREQ
    )

    np.testing.assert_array_equal(
        nominal_temperatures["Nominal Step"].to_numpy(),
        expected_steps,
    )


# =============================================================================
# Temperature schedule tests
# =============================================================================

def test_first_nominal_temperature_is_maximum(
    nominal_temperatures,
):
    """Check that the cooling schedule begins at the maximum temperature."""

    first_temperature = nominal_temperatures[
        "Nominal Temperature (K)"
    ].iloc[0]

    assert first_temperature == MAX_TEMP


def test_last_nominal_temperature_is_minimum(
    nominal_temperatures,
):
    """Check that the cooling schedule ends at the minimum temperature."""

    last_temperature = nominal_temperatures[
        "Nominal Temperature (K)"
    ].iloc[-1]

    assert last_temperature == MIN_TEMP


def test_expected_number_of_nominal_temperatures(
    nominal_temperatures,
):
    """Check that the expected number of 10 K temperature blocks exists."""

    expected_number = (
        int(
            (MAX_TEMP - MIN_TEMP)
            / TEMP_CHANGE
        )
        + 1
    )

    observed_number = nominal_temperatures[
        "Nominal Temperature (K)"
    ].nunique()

    assert observed_number == expected_number


def test_nominal_temperature_values_are_correct(
    nominal_temperatures,
):
    """Check that the assigned temperature sequence is 700 to 140 K."""

    observed_temperatures = (
        nominal_temperatures[
            "Nominal Temperature (K)"
        ]
        .drop_duplicates()
        .to_numpy()
    )

    expected_temperatures = np.arange(
        MAX_TEMP,
        MIN_TEMP - TEMP_CHANGE,
        -TEMP_CHANGE,
    )

    np.testing.assert_array_equal(
        observed_temperatures,
        expected_temperatures,
    )


def test_nominal_temperature_never_exceeds_requested_range(
    nominal_temperatures,
):
    """Check that assigned temperatures remain within the cooling range."""

    temperatures = nominal_temperatures[
        "Nominal Temperature (K)"
    ]

    assert temperatures.max() == MAX_TEMP
    assert temperatures.min() == MIN_TEMP


# =============================================================================
# Historical implementation behaviour
# =============================================================================

def test_first_frame_uses_historical_step_zero(
    nominal_temperatures,
    loaded_simulation,
):
    """
    Check that the historical assignment behaviour is retained.

    The original Tg analysis assigned frame zero to nominal step zero,
    although the first recorded simulation state corresponds to step 1000.
    """

    nominal_step = nominal_temperatures[
        "Nominal Step"
    ].iloc[0]

    recorded_step = loaded_simulation.data[
        "Step"
    ].iloc[0]

    assert nominal_step == 0
    assert recorded_step == REPORTER_FREQ


# =============================================================================
# Validation against recorded simulation temperature
# =============================================================================

def test_nominal_temperature_matches_mean_recorded_temperature(
    nominal_temperatures,
    loaded_simulation,
):
    """
    Validate nominal temperature blocks against recorded temperatures.

    Mean instantaneous temperature within each nominal temperature block
    should closely reproduce the assigned nominal temperature.
    """

    comparison = nominal_temperatures.copy()

    comparison["Recorded Temperature (K)"] = (
        loaded_simulation.data[
            "Temperature (K)"
        ].to_numpy()
    )

    block_means = (
        comparison
        .groupby("Nominal Temperature (K)")
        ["Recorded Temperature (K)"]
        .mean()
    )

    differences = (
        block_means.index.to_numpy()
        - block_means.to_numpy()
    )

    mean_absolute_block_difference = np.mean(
        np.abs(differences)
    )

    assert mean_absolute_block_difference < 1.0


def test_overall_nominal_temperature_bias_is_small(
    nominal_temperatures,
    loaded_simulation,
):
    """Check that nominal assignment has little systematic temperature bias."""

    nominal = nominal_temperatures[
        "Nominal Temperature (K)"
    ].to_numpy()

    recorded = loaded_simulation.data[
        "Temperature (K)"
    ].to_numpy()

    mean_difference = np.mean(
        recorded - nominal
    )

    assert abs(mean_difference) < 1.0


# =============================================================================
# Invalid input tests
# =============================================================================

def test_zero_total_steps_raises_error(
    loaded_simulation,
):
    """Check that total_steps must be greater than zero."""

    with pytest.raises(ValueError):

        assign_nominal_temperatures(
            simulation=loaded_simulation,
            total_steps=0,
            max_temp=MAX_TEMP,
            min_temp=MIN_TEMP,
            temp_change=TEMP_CHANGE,
            reporter_freq=REPORTER_FREQ,
        )


def test_zero_reporter_frequency_raises_error(
    loaded_simulation,
):
    """Check that reporter frequency must be greater than zero."""

    with pytest.raises(ValueError):

        assign_nominal_temperatures(
            simulation=loaded_simulation,
            total_steps=TOTAL_STEPS,
            max_temp=MAX_TEMP,
            min_temp=MIN_TEMP,
            temp_change=TEMP_CHANGE,
            reporter_freq=0,
        )


def test_zero_temperature_change_raises_error(
    loaded_simulation,
):
    """Check that temperature change must be greater than zero."""

    with pytest.raises(ValueError):

        assign_nominal_temperatures(
            simulation=loaded_simulation,
            total_steps=TOTAL_STEPS,
            max_temp=MAX_TEMP,
            min_temp=MIN_TEMP,
            temp_change=0,
            reporter_freq=REPORTER_FREQ,
        )


def test_invalid_cooling_range_raises_error(
    loaded_simulation,
):
    """Check that maximum temperature must exceed minimum temperature."""

    with pytest.raises(ValueError):

        assign_nominal_temperatures(
            simulation=loaded_simulation,
            total_steps=TOTAL_STEPS,
            max_temp=140,
            min_temp=700,
            temp_change=TEMP_CHANGE,
            reporter_freq=REPORTER_FREQ,
        )