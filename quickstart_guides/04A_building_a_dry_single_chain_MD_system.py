#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
===============================================================================
Quickstart Guide 04A
Building a Dry Single-Chain Molecular Dynamics System
===============================================================================

This guide demonstrates how to prepare a dry single-chain molecular dynamics
system for a previously built polymer.

For a more detailed explanation of dry molecular dynamics systems,
see Tutorial 04A.
"""

from src.iphasimulator.system_builder import PHASystemBuilder


# =============================================================================
# 1. Aim
# =============================================================================

print(
"""
Aim

Prepare a dry single-chain molecular dynamics system for a P3HB polymer.
"""
)


# =============================================================================
# 2. Example Code
# =============================================================================

builder = PHASystemBuilder()

builder.build_dry_system(
    polymer_name="P3HB_10",
)

print("\nDry molecular dynamics system created.")


# =============================================================================
# 3. What did the code do?
# =============================================================================

print(
"""
The code

• Loaded the previously constructed P3HB polymer.

• Generated a dry molecular dynamics system containing a single polymer chain.

• Prepared the topology and coordinate files required for molecular dynamics
  simulations.

• Registered the system within the structure database.

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

• Continue to Quickstart Guide 04B to prepare a solvated molecular dynamics
  system.

• See Tutorial 04A for a detailed explanation of dry molecular dynamics
  systems and their applications.
"""
)