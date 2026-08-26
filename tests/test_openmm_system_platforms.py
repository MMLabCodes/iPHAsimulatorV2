#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 15:37:23 2026

@author: daniel

Test OpenMM platforms using a real GROMACS molecular system.

This diagnostic:

1. Loads a GROMACS topology and coordinate file.
2. Constructs an OpenMM System.
3. Attempts to create a Simulation using each available platform.
4. Sets positions and requests the potential energy.

This tests whether a platform works with a realistic molecular system rather
than only with a minimal one-particle OpenMM Context.

Run with:

    python tests/test_openmm_system_platforms.py \
        path/to/system.top \
        path/to/system.gro
"""

import argparse
from pathlib import Path

import openmm as mm
from openmm import app
from openmm import unit


def parse_arguments():
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description=(
            "Test OpenMM compute platforms "
            "using a GROMACS topology and GRO file."
        )
    )

    parser.add_argument(
        "topology_file",
        type=Path,
        help="Path to the GROMACS .top file.",
    )

    parser.add_argument(
        "coordinate_file",
        type=Path,
        help="Path to the GROMACS .gro file.",
    )

    return parser.parse_args()


def main():
    """Run platform tests using a real molecular system."""

    args = parse_arguments()

    topology_file = (
        args.topology_file
        .expanduser()
        .resolve()
    )

    coordinate_file = (
        args.coordinate_file
        .expanduser()
        .resolve()
    )

    if not topology_file.exists():

        raise FileNotFoundError(
            f"Topology file not found:\n"
            f"{topology_file}"
        )

    if not coordinate_file.exists():

        raise FileNotFoundError(
            f"Coordinate file not found:\n"
            f"{coordinate_file}"
        )

    print("=" * 80)
    print("OpenMM molecular-system platform diagnostic")
    print("=" * 80)

    print(
        "OpenMM version:",
        mm.__version__,
    )

    print(
        "Topology file:",
        topology_file,
    )

    print(
        "Coordinate file:",
        coordinate_file,
    )

    print()
    print(
        "Loading GROMACS files..."
    )

    gro = app.GromacsGroFile(
        str(
            coordinate_file
        )
    )

    top = app.GromacsTopFile(
        str(
            topology_file
        ),
        periodicBoxVectors=(
            gro.getPeriodicBoxVectors()
        ),
    )

    print(
        "Creating OpenMM system..."
    )

    system = top.createSystem(
        nonbondedMethod=app.PME,
        nonbondedCutoff=(
            1.0
            * unit.nanometer
        ),
        constraints=app.HBonds,
    )

    platform_names = [
        "CUDA",
        "OpenCL",
        "CPU",
        "Reference",
    ]

    results = {}

    for platform_name in platform_names:

        print()
        print("=" * 80)
        print(
            f"Testing platform: "
            f"{platform_name}"
        )
        print("=" * 80)

        integrator = None
        simulation = None

        try:

            platform = (
                mm.Platform.getPlatformByName(
                    platform_name
                )
            )

            if platform_name in {
                "CUDA",
                "OpenCL",
            }:

                try:

                    platform.setPropertyDefaultValue(
                        "Precision",
                        "mixed",
                    )

                except Exception:
                    pass

            integrator = (
                mm.LangevinMiddleIntegrator(
                    300.0
                    * unit.kelvin,
                    1.0
                    / unit.picosecond,
                    0.002
                    * unit.picoseconds,
                )
            )

            simulation = app.Simulation(
                top.topology,
                system,
                integrator,
                platform,
            )

            simulation.context.setPositions(
                gro.positions
            )

            state = (
                simulation.context.getState(
                    getEnergy=True
                )
            )

            potential_energy = (
                state.getPotentialEnergy()
            )

            print(
                "PASS"
            )

            print(
                "Potential energy:",
                potential_energy,
            )

            results[
                platform_name
            ] = True

        except Exception as error:

            print(
                "FAIL"
            )

            print(
                type(error).__name__,
                ":",
                error,
            )

            results[
                platform_name
            ] = False

        finally:

            if simulation is not None:
                del simulation

            if integrator is not None:
                del integrator

    print()
    print("=" * 80)
    print("Summary")
    print("=" * 80)

    for platform_name in platform_names:

        status = (
            "PASS"
            if results[
                platform_name
            ]
            else "FAIL"
        )

        print(
            f"{platform_name:10s}: "
            f"{status}"
        )


if __name__ == "__main__":
    main()