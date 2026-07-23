#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
===============================================================================
Quickstart Guide 00
Understanding the Structure Database
===============================================================================

This guide introduces the iPHAsimulator structure database and shows how to
locate the main directories used throughout the package.

For a more detailed explanation of the structure database and its design,
see Tutorial 00.
"""

from pathlib import Path

from src.iphasimulator.filepaths import PHAFileManager


# =============================================================================
# 1. Aim
# =============================================================================

print(
"""
Aim

Initialise the iPHAsimulator structure database and display the locations of
the main directories used throughout the software.
"""
)


# =============================================================================
# 2. Example Code
# =============================================================================

PROJECT_ROOT = Path.cwd()

file_manager = PHAFileManager(
    project_root=PROJECT_ROOT,
)

print("\nStructure database located successfully.\n")

print(f"Project root      : {file_manager.project_root}")
print(f"Structure database: {file_manager.structure_database_dir}")
print(f"PHA library       : {file_manager.PHA_types_dir}")
print(f"Built PHAs        : {file_manager.built_PHAs_dir}")
print(f"MD systems        : {file_manager.md_systems_csv}")


# =============================================================================
# 3. What did the code do?
# =============================================================================

print(
"""
The code

• Located the iPHAsimulator project.

• Initialised the PHAFileManager.

• Found the structure database.

• Displayed the locations of the main directories used by
  iPHAsimulator.

The PHAFileManager provides a single interface for locating files and
directories used throughout the package. Most tutorials and workflows begin
by creating an instance of this class.
"""
)


# =============================================================================
# 4. End
# =============================================================================

print(
"""
Quickstart complete.

Continue to Quickstart Guide 01 to register and parameterise your first PHA.
"""
)