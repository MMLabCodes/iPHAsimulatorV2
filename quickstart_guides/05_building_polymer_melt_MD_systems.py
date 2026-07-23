#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
===============================================================================
Quickstart Guide 05
Constructing a Bulk Polymer System
===============================================================================

This guide demonstrates how to construct a bulk polymer system containing
multiple polymer chains for molecular dynamics simulations.

For a more detailed explanation of bulk polymer systems,
see Tutorial 05.
"""

from src.iphasimulator.system_builder import PHASystemBuilder


# =============================================================================
# 1. Aim
# =============================================================================

print(
"""
Aim

Construct a bulk amorphous polymer system containing 25 P3HB polymer chains.
"""
)


# =============================================================================
# 2. Example Code
# =============================================================================

builder = PHASystemBuilder()

builder.build_bulk_system(
    polymer_name="P3HB_10",
    number_of_chains=25,
    target_density=0.75,
    starting_configuration="random",
)

print("\nBulk polymer system created.")


# =============================================================================
# 3. What did the code do?
# =============================================================================

print(
"""
The code

• Loaded the previously constructed P3HB polymer.

• Generated 25 copies of the polymer chain.

• Packed the polymer chains into a periodic simulation box.

• Adjusted the simulation box to achieve an initial density of
  approximately 0.75 g/cm³.

• Generated the topology and coordinate files required for molecular
  dynamics simulations.

• Registered the bulk polymer system within the structure database.

The generated system is now ready for equilibration and molecular
dynamics simulations.
"""
)


# =============================================================================
# 4. End
# =============================================================================

print(
"""
Quickstart complete.

Next steps

• Continue to Quickstart Guide 06 to explore the molecular dynamics
  system registry.

• See Tutorial 05 for a detailed explanation of bulk polymer packing,
  periodic boundary conditions, target density, and system preparation.
"""
)