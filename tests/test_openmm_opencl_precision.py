#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 16:05:18 2026

@author: daniel

Diagnose OpenCL precision support using a real GROMACS system.

Tests the same molecular system with:

- OpenCL default precision
- single precision
- mixed precision
- double precision

This helps determine whether an explicitly requested OpenCL precision mode
is responsible for context-creation failures.
"""

from pathlib import Path

import openmm as mm
from openmm import app
from openmm import unit


# =============================================================================
# Files
# =============================================================================

PROJECT_ROOT = Path(
    "/Users/daniel/projects/iPHAsimulatorV2"
)

SYSTEM_DIR = (
    PROJECT_ROOT
    / "structure_database"
    / "PHA_melts"
    / "25_P3HB_10_melt"
)

TOP_FILE = (
    SYSTEM_DIR
    / "25_P3HB_10_melt.top"
)

GRO_FILE = (
    SYSTEM_DIR
    / "25_P3HB_10_melt.gro"
)


# =============================================================================
# Load system
# =============================================================================

print("=" * 80)
print("OpenCL precision diagnostic")
print("=" * 80)

print(
    "OpenMM:",
    mm.__version__,
)

gro = app.GromacsGroFile(
    str(GRO_FILE)
)

top = app.GromacsTopFile(
    str(TOP_FILE),
    periodicBoxVectors=(
        gro.getPeriodicBoxVectors()
    ),
)

system = top.createSystem(
    nonbondedMethod=app.PME,
    nonbondedCutoff=(
        1.0
        * unit.nanometer
    ),
    constraints=app.HBonds,
)


# =============================================================================
# Inspect OpenCL
# =============================================================================

platform = mm.Platform.getPlatformByName(
    "OpenCL"
)

print()
print("OpenCL platform properties:")

for property_name in platform.getPropertyNames():

    try:

        value = (
            platform.getPropertyDefaultValue(
                property_name
            )
        )

    except Exception:

        value = "<unavailable>"

    print(
        f"  {property_name}: {value}"
    )


# =============================================================================
# Precision tests
# =============================================================================

precision_modes = [
    None,
    "single",
    "mixed",
    "double",
]


for precision in precision_modes:

    print()
    print("=" * 80)

    if precision is None:
        print(
            "Testing OpenCL with DEFAULT precision"
        )

    else:
        print(
            f"Testing OpenCL precision: {precision}"
        )

    print("=" * 80)

    integrator = None
    context = None

    try:

        integrator = mm.LangevinMiddleIntegrator(
            300.0
            * unit.kelvin,
            1.0
            / unit.picosecond,
            0.002
            * unit.picoseconds,
        )

        properties = {}

        if precision is not None:

            properties[
                "Precision"
            ] = precision

        context = mm.Context(
            system,
            integrator,
            platform,
            properties,
        )

        context.setPositions(
            gro.positions
        )

        state = context.getState(
            getEnergy=True
        )

        print(
            "PASS"
        )

        print(
            "Potential energy:",
            state.getPotentialEnergy(),
        )

        if precision is not None:

            try:

                actual_precision = (
                    platform.getPropertyValue(
                        context,
                        "Precision",
                    )
                )

                print(
                    "Actual precision:",
                    actual_precision,
                )

            except Exception:
                pass

    except Exception as error:

        print(
            "FAIL"
        )

        print(
            type(error).__name__,
            ":",
            error,
        )

    finally:

        if context is not None:
            del context

        if integrator is not None:
            del integrator