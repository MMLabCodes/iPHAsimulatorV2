#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
===============================================================================
Quickstart Guide 04B
Building a Solvated Single-Chain Molecular Dynamics System
===============================================================================

This guide demonstrates how to prepare a solvated molecular dynamics system
containing one previously built polymer chain.

For a more detailed explanation of solvated molecular dynamics systems,
see Tutorial 04B.
"""

from src.iphasimulator.system_builder import PHASystemBuilder


# =============================================================================
# 1. Aim
# =============================================================================

print(
"""
Aim

Prepare a solvated single-chain molecular dynamics system for a P3HB polymer.
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
)

print("\nSolvated molecular dynamics system created.")


# =============================================================================
# 3. What did the code do?
# =============================================================================

print(
"""
The code

• Loaded the previously constructed P3HB polymer.

• Placed the polymer inside a molecular dynamics simulation box.

• Added water molecules around the polymer using the TIP3P water model.

• Added approximately 1.0 nm of solvent padding around the polymer.

• Generated the topology and coordinate files required for molecular
  dynamics simulations.

• Registered the solvated system within the structure database.

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

• Continue to Quickstart Guide 04C to prepare a solvated system containing
  ions.

• See Tutorial 04B for a detailed explanation of solvation, water models,
  simulation boxes, and solvent padding.
"""
)