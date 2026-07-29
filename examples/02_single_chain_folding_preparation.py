#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
===============================================================================
Example 02

Preparing a Single P3HB Chain for Folding Simulations
===============================================================================

This example demonstrates how to:

1. Build a 50-mer P3HB polymer.
2. Solvate the polymer using TIP3P water.
3. Add 0.15 M KCl.
4. Register the completed molecular dynamics system.

Outputs
-------
• Amber topology (.prmtop)
• Amber coordinates (.rst7)
• PDB structure
• tleap input files
• tleap log files
• Registered molecular dynamics system
"""

from pathlib import Path
import sys

# =============================================================================
# Locate the project
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
STRUCTURE_DATABASE = PROJECT_ROOT / "structure_database"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

print(f"Project root       : {PROJECT_ROOT}")
print(f"Source directory   : {SRC_DIR}")
print(f"Structure database : {STRUCTURE_DATABASE}")

# =============================================================================
# Import iPHAsimulator
# =============================================================================

from iphasimulator.build_pha import PHAPolymerBuilder
from iphasimulator.build_single_PHA_systems import build_solvated_PHA_ions

# =============================================================================
# User settings
# =============================================================================

PHA_TYPE = "3HB"
POLYMER_LENGTH = 50

# =============================================================================
# Build the polymer
# =============================================================================

print("\n===================================================")
print("Building finite polymer")
print("===================================================\n")

builder = PHAPolymerBuilder(
    root_dir=STRUCTURE_DATABASE,
)

polymer = builder.build_PHA_polymer(
    PHA_type=PHA_TYPE,
    length=POLYMER_LENGTH,
)

polymer_name = polymer["built_name"]

# =============================================================================
# Build the solvated system with ions
# =============================================================================

print("\n===================================================")
print("Building solvated system")
print("===================================================\n")

system = build_solvated_PHA_ions(
    polymer_name=polymer_name,
    root_dir=STRUCTURE_DATABASE,
    forcefield="gaff2",
    water_leaprc="water.tip3p",
    water_box="TIP3PBOX",
    box_radius=20.0,
    salt="KCl",
    pos_ion="K+",
    neg_ion="Cl-",
    ion_conc=0.15,
)

# =============================================================================
# Summary
# =============================================================================

print("\n===================================================")
print("Finished")
print("===================================================\n")

print(f"Polymer : {polymer_name}")
print(f"System  : {system['system_name']}")

print("\nGenerated files\n")

for key, value in system.items():
    print(f"{key:20s}: {value}")