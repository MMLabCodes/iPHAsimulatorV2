#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 15:31:19 2026

@author: daniel

Test OpenMM platform availability.

This diagnostic checks:

1. Which OpenMM platforms are registered.
2. Whether each platform can successfully create a minimal OpenMM Context.

This is useful because a platform may appear in the list of registered
OpenMM platforms but still fail when a Context is created.

Run with:

    python tests/test_openmm_platforms.py
"""

import openmm
from openmm import unit


def main():
    """Run the OpenMM platform diagnostics."""

    print("=" * 80)
    print("OpenMM platform diagnostic")
    print("=" * 80)

    print(
        "OpenMM version:",
        openmm.__version__,
    )

    print()
    print("Registered platforms:")

    registered_platforms = []

    for index in range(
        openmm.Platform.getNumPlatforms()
    ):

        platform = openmm.Platform.getPlatform(
            index
        )

        platform_name = platform.getName()

        registered_platforms.append(
            platform_name
        )

        print(
            f"  {index}: "
            f"{platform_name} "
            f"(speed = {platform.getSpeed()})"
        )

    print()
    print("=" * 80)
    print("Context creation tests")
    print("=" * 80)

    platform_names = [
        "CUDA",
        "OpenCL",
        "CPU",
        "Reference",
    ]

    results = {}

    for platform_name in platform_names:

        print()
        print(
            f"Testing {platform_name}..."
        )

        try:

            platform = (
                openmm.Platform.getPlatformByName(
                    platform_name
                )
            )

            system = openmm.System()

            system.addParticle(
                1.0
            )

            integrator = (
                openmm.VerletIntegrator(
                    0.001
                    * unit.picoseconds
                )
            )

            context = openmm.Context(
                system,
                integrator,
                platform,
            )

            print(
                f"PASS: {platform_name} "
                "can create an OpenMM Context."
            )

            results[
                platform_name
            ] = True

            del context
            del integrator

        except Exception as error:

            print(
                f"FAIL: {platform_name}"
            )

            print(
                type(error).__name__,
                ":",
                error,
            )

            results[
                platform_name
            ] = False

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