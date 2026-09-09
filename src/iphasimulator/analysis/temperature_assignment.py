#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 15:24:41 2026

@author: daniel

Temperature assignment utilities for molecular dynamics trajectories.

This module provides methods for associating molecular dynamics
trajectory frames with simulation temperatures.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .simulation_loader import LoadedSimulation


# =============================================================================
# Nominal temperature assignment
# =============================================================================

def assign_nominal_temperatures(
    simulation: LoadedSimulation,
    total_steps: int,
    max_temp: float,
    min_temp: float,
    temp_change: float,
    reporter_freq: int,
) -> pd.DataFrame:
    """
    Assign nominal temperatures to trajectory frames.

    This reproduces the temperature-assignment method used in the
    original Tg analysis workflow.

    The total number of simulation steps is divided equally between
    the requested nominal temperatures. Each trajectory frame is then
    assigned a temperature according to its frame index and reporter
    frequency.

    Parameters
    ----------
    simulation : LoadedSimulation
        Loaded molecular dynamics simulation.

    total_steps : int
        Total number of simulation steps represented by the cooling
        trajectory.

    max_temp : float
        Highest nominal temperature.

    min_temp : float
        Lowest nominal temperature.

    temp_change : float
        Temperature interval between neighbouring nominal temperatures.

    reporter_freq : int
        Number of simulation steps between trajectory frames.

    Returns
    -------
    pandas.DataFrame
        Table containing, for every trajectory frame:

        - frame index
        - nominal step
        - nominal temperature

    Notes
    -----
    This function intentionally reproduces the original temperature
    assignment method, including its use of::

        step = frame_index * reporter_freq

    Therefore, frame zero is assigned nominal step zero even when the
    first recorded simulation frame corresponds to a later simulation
    step.
    """

    # -------------------------------------------------------------------------
    # Validate inputs
    # -------------------------------------------------------------------------

    if total_steps <= 0:
        raise ValueError(
            "total_steps must be greater than zero."
        )

    if reporter_freq <= 0:
        raise ValueError(
            "reporter_freq must be greater than zero."
        )

    if temp_change <= 0:
        raise ValueError(
            "temp_change must be greater than zero."
        )

    if max_temp <= min_temp:
        raise ValueError(
            "max_temp must be greater than min_temp "
            "for a cooling trajectory."
        )

    # -------------------------------------------------------------------------
    # Determine temperature schedule
    # -------------------------------------------------------------------------

    n_temps = (
        int((max_temp - min_temp) / temp_change)
        + 1
    )

    steps_per_temp = total_steps / n_temps

    # -------------------------------------------------------------------------
    # Determine trajectory frames
    # -------------------------------------------------------------------------

    n_frames = len(
        simulation.universe.trajectory
    )

    frame_indices = np.arange(
        n_frames,
        dtype=int,
    )

    # -------------------------------------------------------------------------
    # Reproduce original step assignment
    # -------------------------------------------------------------------------

    nominal_steps = (
        frame_indices * reporter_freq
    )

    # -------------------------------------------------------------------------
    # Assign temperature block
    # -------------------------------------------------------------------------

    temperature_indices = np.floor(
        nominal_steps / steps_per_temp
    ).astype(int)

    nominal_temperatures = (
        max_temp
        - temp_change * temperature_indices
    )

    # -------------------------------------------------------------------------
    # Construct output table
    # -------------------------------------------------------------------------

    assignments = pd.DataFrame(
        {
            "Frame": frame_indices,
            "Nominal Step": nominal_steps,
            "Nominal Temperature (K)": nominal_temperatures,
        }
    )

    return assignments