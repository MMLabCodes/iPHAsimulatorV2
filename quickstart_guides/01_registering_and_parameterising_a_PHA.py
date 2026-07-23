#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
===============================================================================
Quickstart Guide 01
Registering and Parameterising a PHA
===============================================================================

This guide demonstrates the minimum steps required to register a new PHA and
generate the molecular files required for polymer construction.

For a more detailed explanation of the registration and parameterisation
process, see Tutorial 01.
"""

from src.iphasimulator.pha_builder import PHAPolymerBuilder


# =============================================================================
# 1. Aim
# =============================================================================

print(
"""
Aim

Register the PHA 3HB and parameterise its trimer using the GAFF2 force field.
"""
)


# =============================================================================
# 2. Example Code
# =============================================================================

builder = PHAPolymerBuilder()

builder.parameterise_trimer(
    PHA_type="3HB",
    trimer_name="P3HB_3",
    trimer_smiles="O[C@H](C)CC(=O)O[C@H](C)CC(=O)O[C@H](C)CC(=O)O",
    monomer_smiles="O[C@H](C)CC(=O)O",
    forcefield="gaff2",
    charge_model="abcg2",
)

print("\nParameterisation complete.")


# =============================================================================
# 3. What did the code do?
# =============================================================================

print(
"""
The code

• Registered the PHA type '3HB'.

• Generated the molecular structure of a 3HB trimer.

• Assigned GAFF2 atom types.

• Calculated partial atomic charges using the ABCG2 charge model.

• Generated the files required for polymer construction.
"""
)


# =============================================================================
# 4. End
# =============================================================================

print(
"""
Quickstart complete.

Next steps

• Continue to Quickstart Guide 02 to build your first polymer.

• See Tutorial 01 for a detailed explanation of PHA registration,
  force field parameterisation, residue generation, and molecular files.
"""
)