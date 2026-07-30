#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Application-wide configuration for the iPHAsimulatorV2 GUI.
"""

from pathlib import Path

from src.iphasimulator.pha_filepath_manager import PHAFileManager


# ==========================================================
# Project directories
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

STRUCTURE_DATABASE = PROJECT_ROOT / "structure_database"

RESIDUE_CODES_CSV = (
    STRUCTURE_DATABASE
    / "residue_codes.csv"
)

MD_SYSTEMS_CSV = (
    STRUCTURE_DATABASE
    / "md_systems.csv"
)

MD_SCRIPT_DIR = (
    PROJECT_ROOT
    / "md_simulation_scripts"
)

MD_SCRIPT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ==========================================================
# External scientific environment
# ==========================================================

IPHASIMULATOR_PYTHON = (
    Path.home()
    / "miniconda3"
    / "envs"
    / "iphasimulator"
    / "bin"
    / "python"
)

# Temporary backwards-compatibility alias.
# Existing GUI modules can continue using AMBERTOOLS_PYTHON
# until they are updated.
AMBERTOOLS_PYTHON = IPHASIMULATOR_PYTHON

AMBERTOOLS_PYTHON = IPHASIMULATOR_PYTHON

# ==========================================================
# Shared backend objects
# ==========================================================

paths = PHAFileManager(
    STRUCTURE_DATABASE
)