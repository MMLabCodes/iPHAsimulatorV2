#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
===============================================================================
Quickstart Guide 03
Understanding Molecular Dynamics Systems
===============================================================================

This guide introduces the different molecular dynamics systems that can be
created using iPHAsimulator.

For a more detailed explanation of molecular dynamics systems and their
applications, see Tutorial 03.
"""

from src.iphasimulator.systems import show_available_md_systems


# =============================================================================
# 1. Aim
# =============================================================================

print(
"""
Aim

Display the molecular dynamics system types available in iPHAsimulator.
"""
)


# =============================================================================
# 2. Example Code
# =============================================================================

show_available_md_systems()


# =============================================================================
# 3. What did the code do?
# =============================================================================

print(
"""
The code

• Displayed the molecular dynamics system types available in
  iPHAsimulator.

• Introduced the different environments that can be prepared for
  molecular dynamics simulations.

The available systems include:

  • Dry single-chain systems
  • Solvated single-chain systems
  • Solvated systems containing ions
  • Bulk polymer systems

Each system is designed for a different type of molecular simulation.
"""
)


# =============================================================================
# 4. End
# =============================================================================

print(
"""
Quickstart complete.

Next steps

• Continue to Quickstart Guide 04A to build your first dry
  single-chain molecular dynamics system.

• See Tutorial 03 for a detailed explanation of the different
  molecular dynamics systems and when they should be used.
"""
)