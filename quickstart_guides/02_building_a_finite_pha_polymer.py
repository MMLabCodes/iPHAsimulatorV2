#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
===============================================================================
Quickstart Guide 02
Building a Finite Polymer
===============================================================================

This guide demonstrates how to construct a finite PHA polymer from a
previously parameterised PHA.

For a more detailed explanation of polymer construction,
see Tutorial 02.
"""

from src.iphasimulator.build_pha import PHAPolymerBuilder


# =============================================================================
# 1. Aim
# =============================================================================

print(
"""
Aim

Build a finite P3HB polymer containing 10 repeat units.
"""
)


# =============================================================================
# 2. Example Code
# =============================================================================

builder = PHAPolymerBuilder()

builder.build_PHA_polymer(
    PHA_type="3HB",
    length=10,
)

print("\nPolymer construction complete.")


# =============================================================================
# 3. What did the code do?
# =============================================================================

print(
"""
The code

• Loaded the registered 3HB residue library.

• Constructed a polymer containing 10 repeat units.

• Generated the molecular topology and coordinate files.

• Saved the completed polymer to the structure database.

The generated polymer is now ready for molecular dynamics system preparation.
"""
)


# =============================================================================
# 4. End
# =============================================================================

print(
"""
Quickstart complete.

Next steps

• Continue to Quickstart Guide 03 to learn about molecular dynamics systems.

• See Tutorial 02 for a detailed explanation of polymer construction,
  residue connectivity, and generated molecular files.
"""
)