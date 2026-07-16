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
# External environments
# ==========================================================

AMBERTOOLS_PYTHON = (
    Path.home()
    / "miniconda3"
    / "envs"
    / "AmberTools23"
    / "bin"
    / "python"
)


# ==========================================================
# Shared backend objects
# ==========================================================

paths = PHAFileManager(
    STRUCTURE_DATABASE
)