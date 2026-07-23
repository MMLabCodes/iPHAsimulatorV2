#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
===============================================================================
Quickstart Guide 04C
Building a Solvated Single-Chain Molecular Dynamics System with Ions
===============================================================================

This guide demonstrates how to prepare a solvated molecular dynamics system
containing one previously built polymer chain and a specified concentration
of dissolved ions.

For a more detailed explanation of solvated ionic molecular dynamics systems,
see Tutorial 04C.
"""

from src.iphasimulator.system_builder import PHASystemBuilder


# =============================================================================
# 1. Aim
# =============================================================================

print(
"""
Aim

Prepare a solvated single-chain molecular dynamics system containing
0.15 M KCl for a P3HB polymer.
"""
)


# =============================================================================
# 2. Example Code
# =============================================================================

builder = PHASystemBuilder()

builder.build_solvated_system(
    polymer_name="P3HB_10",
    solvent="water",
    water_model="tip3p",
    padding=1.0,
    ions="KCl",
    ion_concentration=0.15,
)

print("\nSolvated molecular dynamics system with ions created.")


# =============================================================================
# 3. What did the code do?
# =============================================================================

print(
"""
The code

• Loaded the previously constructed P3HB polymer.

• Placed the polymer inside a molecular dynamics simulation box.

• Added water molecules around the polymer using the TIP3P water model.

• Added potassium (K+) and chloride (Cl−) ions to produce a
  0.15 M KCl solution.

• Generated the topology and coordinate files required for molecular
  dynamics simulations.

• Registered the solvated ionic system within the structure database.

The generated system is now ready to be used when creating an OpenMM
simulation workflow.
"""
)


# =============================================================================
# 4. End
# =============================================================================

print(
"""
Quickstart complete.

Next steps

• Continue to Quickstart Guide 05 to construct a bulk polymer system.

• See Tutorial 04C for a detailed explanation of electrolyte solutions,
  ion placement, charge neutrality, and simulation preparation.
"""
)