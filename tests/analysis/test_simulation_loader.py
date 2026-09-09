#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 15:07:59 2026

@author: daniel

Tests for the iPHAsimulator simulation loader.
"""

from pathlib import Path

import pytest

from iphasimulator.analysis.simulation_loader import (
    LoadedSimulation,
    load_simulation,
    validate_frame_data_alignment,
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


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture(scope="module")
def loaded_simulation():
    """Load the test simulation once for all tests in this module."""

    return load_simulation(
        system_directory=SYSTEM_DIRECTORY,
        simulation_name=SIMULATION_NAME,
        stage=SIMULATION_STAGE,
    )


# =============================================================================
# Loading tests
# =============================================================================

def test_load_simulation_returns_loaded_simulation(loaded_simulation):
    """Check that the loader returns the expected container type."""

    assert isinstance(
        loaded_simulation,
        LoadedSimulation,
    )


def test_simulation_files_exist(loaded_simulation):
    """Check that all required simulation files were located."""

    assert loaded_simulation.topology_path.is_file()
    assert loaded_simulation.trajectory_path.is_file()
    assert loaded_simulation.data_path.is_file()


def test_correct_file_types_loaded(loaded_simulation):
    """Check that the expected simulation file types were selected."""

    assert loaded_simulation.topology_path.suffix == ".pdb"
    assert loaded_simulation.trajectory_path.suffix == ".dcd"
    assert loaded_simulation.data_path.suffix == ".txt"


# =============================================================================
# MDAnalysis Universe tests
# =============================================================================

def test_universe_contains_atoms(loaded_simulation):
    """Check that the MDAnalysis Universe contains atoms."""

    universe = loaded_simulation.universe

    assert universe.atoms.n_atoms > 0


def test_universe_contains_residues(loaded_simulation):
    """Check that the MDAnalysis Universe contains residues."""

    universe = loaded_simulation.universe

    assert universe.residues.n_residues > 0


def test_universe_contains_segments(loaded_simulation):
    """Check that the MDAnalysis Universe contains segments."""

    universe = loaded_simulation.universe

    assert universe.segments.n_segments > 0


def test_universe_contains_trajectory_frames(loaded_simulation):
    """Check that trajectory frames were loaded."""

    universe = loaded_simulation.universe

    assert len(universe.trajectory) > 0


# =============================================================================
# State-data tests
# =============================================================================

def test_state_data_not_empty(loaded_simulation):
    """Check that simulation state data were loaded."""

    assert not loaded_simulation.data.empty


def test_state_data_contains_time(loaded_simulation):
    """Check that the state-data file contains simulation time."""

    assert "Time (ps)" in loaded_simulation.data.columns


def test_state_data_contains_temperature(loaded_simulation):
    """Check that the state-data file contains temperature."""

    assert "Temperature (K)" in loaded_simulation.data.columns


# =============================================================================
# Trajectory/data alignment tests
# =============================================================================

def test_frame_and_data_counts_match(loaded_simulation):
    """Check that every trajectory frame has a state-data row."""

    n_frames = len(
        loaded_simulation.universe.trajectory
    )

    n_rows = len(
        loaded_simulation.data
    )

    assert n_frames == n_rows


def test_frame_data_alignment(loaded_simulation):
    """Check that trajectory and state-data times are aligned."""

    validate_frame_data_alignment(
        universe=loaded_simulation.universe,
        data=loaded_simulation.data,
        tolerance_ps=0.01,
    )


# =============================================================================
# Error handling tests
# =============================================================================

def test_missing_system_directory_raises_error(tmp_path):
    """Check that a missing system directory raises FileNotFoundError."""

    missing_directory = (
        tmp_path
        / "this_system_does_not_exist"
    )

    with pytest.raises(FileNotFoundError):

        load_simulation(
            system_directory=missing_directory,
            simulation_name="test_simulation",
            stage="test_stage",
        )


def test_missing_simulation_directory_raises_error(tmp_path):
    """Check that a missing simulation directory raises FileNotFoundError."""

    system_directory = tmp_path / "test_system"
    system_directory.mkdir()

    with pytest.raises(FileNotFoundError):

        load_simulation(
            system_directory=system_directory,
            simulation_name="missing_simulation",
            stage="test_stage",
        )
