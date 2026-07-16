#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Shared data models for the iPHAsimulatorV2 GUI.
"""

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from src.iphasimulator.pha_filepath_manager import PHAFileManager


@dataclass
class GUIData:
    """
    Shared data used by the GUI tabs.
    """

    paths: PHAFileManager
    available_phas: list[str]
    monomer_smiles: dict[str, str]
    mainchain_df: pd.DataFrame
    md_systems_df: pd.DataFrame


@dataclass
class MDSystemSelection:
    """
    Resolved information for one selected MD system.
    """

    system_name: str
    system_type: str
    number_of_atoms: int | None

    system_dir: Path
    topology_file: Path
    coordinate_file: Path
    simulations_dir: Path

    input_format: str