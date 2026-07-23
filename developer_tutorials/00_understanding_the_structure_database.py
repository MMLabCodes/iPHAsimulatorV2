#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tutorial 00: Understanding the iPHAsimulator structure database.

Purpose
-------
This tutorial introduces the directory and database structure used by
iPHAsimulatorV2.

It demonstrates how PHAFileManager acts as the central source of truth for:

- registered PHA chemistries
- parameter files
- built polymer chains
- prepared molecular-dynamics systems
- polymer melts
- simulation directories
- CSV database files

This tutorial does not build or modify any polymers or MD systems.

Prerequisites
-------------
Run this script from the root of the iPHAsimulatorV2 project.

The project should contain:

    structure_database/
    src/
    gui/

Outputs
-------
This tutorial only prints information.

It does not create a polymer or run a simulation.

Notes
-----
The ``# %%`` headings allow this file to be used as:

- a normal Python script
- a Spyder cell-based script
- a VS Code interactive script
- a source for a Jupyter notebook
"""

# %% 1. Imports

from pathlib import Path
import csv

from src.iphasimulator.pha_filepath_manager import (
    PHAFileManager,
)


# %% 2. User settings

# The structure database is normally located in the project root.
root_dir = Path("structure_database")

# Example PHA chemistry used throughout this tutorial.
example_PHA_type = "3HB"

# Example previously built polymer.
example_polymer_name = "P3HB_10"

# Example melt definition.
example_melt_polymer_names = [
    "P3HB_10",
]

example_melt_polymer_counts = [
    25,
]


# %% 3. Initialise the filepath manager

"""
PHAFileManager is the central path-management object used by the project.

Rather than manually constructing paths such as:

    structure_database/PHA_types/3HB/monomer_units/hP3HB.prepin

the code asks PHAFileManager for the path.

This keeps directory naming consistent across all builder, simulation,
analysis, and GUI modules.
"""

paths = PHAFileManager(
    root_dir=root_dir,
)

print("=" * 80)
print("PHA FILE MANAGER")
print("=" * 80)

print("Structure database root:")
print(paths.get_root_dir())

print("\nTemporary working directory:")
print(paths.get_temp_dir())

print("\nResidue-code database:")
print(paths.get_residue_codes_csv())

print("\nPolymer-SMILES database:")
print(paths.get_polymer_smiles_csv())

print("\nMD-system registry:")
print(paths.get_md_systems_csv())


# %% 4. Inspect the main structure-database directories

"""
The structure database separates different kinds of information.

PHA_types
    Stores chemistry-specific parameterisation files.

built_PHAs
    Stores individual built polymer chains.

PHA_melts
    Stores packed multi-chain polymer melts.

PHA_dry
    Stores dry single-chain MD systems.

PHA_solvated
    Stores solvated single-chain MD systems.

PHA_solvated_ions
    Stores solvated systems containing salt ions.
"""

print("\n" + "=" * 80)
print("MAIN DATABASE DIRECTORIES")
print("=" * 80)

main_directories = {
    "PHA chemistry database": paths.PHA_types_dir,
    "Built polymer database": paths.built_PHAs_dir,
    "Polymer melt database": paths.PHA_melts_dir,
    "Dry MD systems": paths.get_PHA_dry_dir(),
    "Solvated MD systems": paths.get_PHA_solvated_dir(),
    "Solvated + ion systems": paths.get_PHA_solvated_ions_dir(),
    "Temporary files": paths.get_temp_dir(),
}

for description, directory in main_directories.items():
    print(f"\n{description}")
    print(f"  Path:   {directory}")
    print(f"  Exists: {directory.exists()}")


# %% 5. Inspect one registered PHA chemistry

"""
A PHA type represents a chemical repeat-unit family.

For example:

    3HB

is a PHA chemistry.

It is not yet a complete polymer chain.

The chemistry directory stores the files needed to parameterise and assemble
polymers of that chemistry.
"""

print("\n" + "=" * 80)
print(f"PHA CHEMISTRY: {example_PHA_type}")
print("=" * 80)

PHA_type_dir = paths.get_PHA_type_dir(
    example_PHA_type
)

PHA_input_dir = paths.get_PHA_input_dir(
    example_PHA_type
)

PHA_trimer_dir = paths.get_PHA_trimer_dir(
    example_PHA_type
)

PHA_monomer_units_dir = (
    paths.get_PHA_monomer_units_dir(
        example_PHA_type
    )
)

PHA_leap_template_dir = (
    paths.get_PHA_leap_template_dir(
        example_PHA_type
    )
)

PHA_directories = {
    "PHA type directory": PHA_type_dir,
    "Manual parameterisation inputs": PHA_input_dir,
    "Trimer parameter files": PHA_trimer_dir,
    "Head/mainchain/tail residues": PHA_monomer_units_dir,
    "TLEaP templates": PHA_leap_template_dir,
}

for description, directory in PHA_directories.items():
    print(f"\n{description}")
    print(f"  Path:   {directory}")
    print(f"  Exists: {directory.exists()}")


# %% 6. Inspect the monomer-unit parameter files

"""
A polymer is assembled from three residue types:

head
    The first residue in the polymer chain.

mainchain
    The internal repeat-unit residue.

tail
    The final residue in the polymer chain.

For P3HB, the standard files are:

    hP3HB.prepin
    mP3HB.prepin
    tP3HB.prepin

The FRCMOD file contains force-field terms obtained from the parameterised
trimer.
"""

parameter_files = paths.get_PHA_monomer_unit_files(
    example_PHA_type
)

print("\n" + "=" * 80)
print("MONOMER-UNIT PARAMETER FILES")
print("=" * 80)

for file_role, file_path in parameter_files.items():
    print(f"\n{file_role}")
    print(f"  Path:   {file_path}")
    print(f"  Exists: {Path(file_path).exists()}")


required_parameter_keys = [
    "head_prepin",
    "mainchain_prepin",
    "tail_prepin",
    "frcmod",
]

all_parameter_files_exist = all(
    Path(parameter_files[key]).exists()
    for key in required_parameter_keys
)

print("\nParameterisation status:")

if all_parameter_files_exist:
    print(
        f"  {example_PHA_type} has all files required "
        "for polymer construction."
    )

else:
    print(
        f"  {example_PHA_type} is missing one or more files "
        "required for polymer construction."
    )


# %% 7. Inspect the residue-code database

"""
residue_codes.csv links readable PHA names to Amber-compatible residue codes.

A typical PHA chemistry has four entries:

    trimer
    head
    mainchain
    tail

For example:

    3HB,trimer,P3HB_3,AAA,...
    3HB,head,hP3HB,AAB,...
    3HB,mainchain,mP3HB,AAC,...
    3HB,tail,tP3HB,AAD,...

The three-letter codes are used internally by AmberTools.
"""

residue_codes_csv = paths.get_residue_codes_csv()

print("\n" + "=" * 80)
print("RESIDUE-CODE DATABASE")
print("=" * 80)

print("CSV path:")
print(residue_codes_csv)

if not residue_codes_csv.exists():
    print("\nThe residue-code database does not exist.")

else:
    with open(
        residue_codes_csv,
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        reader = csv.DictReader(file)

        matching_rows = [
            row
            for row in reader
            if row.get("PHA_type") == example_PHA_type
        ]

    if not matching_rows:
        print(
            f"\nNo entries were found for {example_PHA_type}."
        )

    else:
        print(
            f"\nEntries for {example_PHA_type}:"
        )

        for row in matching_rows:
            print(
                "  "
                f"{row.get('component', ''):<10} "
                f"{row.get('readable_name', ''):<12} "
                f"{row.get('residue_code', '')}"
            )


# %% 8. Inspect one built polymer

"""
A built polymer is an actual finite polymer chain.

For example:

    P3HB_10

means:

    P       polymer
    3HB     PHA chemistry
    10      ten repeat units

The polymer name can be parsed by PHAFileManager.
"""

print("\n" + "=" * 80)
print(f"BUILT POLYMER: {example_polymer_name}")
print("=" * 80)

PHA_type, polymer_length = (
    paths.parse_built_PHA_name(
        example_polymer_name
    )
)

print("Parsed polymer information:")
print(f"  PHA type: {PHA_type}")
print(f"  Length:   {polymer_length}")

built_polymer_dir = paths.get_built_PHA_dir(
    PHA_type,
    polymer_length,
)

built_leap_dir = paths.get_built_PHA_leap_dir(
    PHA_type,
    polymer_length,
)

built_amber_dir = paths.get_built_PHA_amber_dir(
    PHA_type,
    polymer_length,
)

built_gromacs_dir = paths.get_built_PHA_gromacs_dir(
    PHA_type,
    polymer_length,
)

print("\nBuilt-polymer directories:")

for description, directory in {
    "Polymer root": built_polymer_dir,
    "TLEaP build files": built_leap_dir,
    "Amber files": built_amber_dir,
    "GROMACS files": built_gromacs_dir,
}.items():
    print(f"\n{description}")
    print(f"  Path:   {directory}")
    print(f"  Exists: {directory.exists()}")


# %% 9. Inspect expected Amber files

"""
The standard Amber representation of a built polymer consists of:

PDB
    Human-readable coordinates.

PRMTOP
    Amber topology and force-field information.

RST7
    Amber coordinates and box information.
"""

amber_files = paths.get_built_PHA_amber_files(
    example_polymer_name
)

print("\n" + "=" * 80)
print("BUILT-POLYMER AMBER FILES")
print("=" * 80)

for file_role, file_path in amber_files.items():
    print(f"\n{file_role}")
    print(f"  Path:   {file_path}")
    print(f"  Exists: {Path(file_path).exists()}")


# %% 10. Count atoms in the built polymer, when possible

"""
PHAFileManager can use ParmEd to count atoms in an Amber topology.

This section only runs if the expected PRMTOP file exists.
"""

polymer_prmtop = amber_files["prmtop"]

print("\n" + "=" * 80)
print("BUILT-POLYMER ATOM COUNT")
print("=" * 80)

if polymer_prmtop.exists():
    try:
        number_of_atoms = (
            paths.count_atoms_from_amber_topology(
                polymer_prmtop
            )
        )

        print(
            f"{example_polymer_name} contains "
            f"{number_of_atoms} atoms."
        )

    except Exception as error:
        print(
            "The topology exists, but its atom count "
            "could not be read."
        )

        print(error)

else:
    print(
        "The built-polymer PRMTOP does not exist, "
        "so the atom count was not calculated."
    )


# %% 11. Inspect a polymer-melt path

"""
A polymer melt contains one or more polymer species and a specified number
of chains of each species.

The arguments are lists because mixed melts are supported.

For example:

    polymer_names = ["P3HB_10", "P4HB_10"]
    number_of_polymers = [25, 25]

would produce a mixed melt containing 25 chains of each polymer.
"""

melt_name = paths.get_PHA_melt_name(
    example_melt_polymer_names,
    example_melt_polymer_counts,
)

melt_dir = paths.get_PHA_melt_dir(
    example_melt_polymer_names,
    example_melt_polymer_counts,
)

melt_inputs_dir = paths.get_PHA_melt_inputs_dir(
    example_melt_polymer_names,
    example_melt_polymer_counts,
)

melt_simulations_dir = (
    paths.get_PHA_melt_simulations_dir(
        example_melt_polymer_names,
        example_melt_polymer_counts,
    )
)

print("\n" + "=" * 80)
print("POLYMER MELT")
print("=" * 80)

print(f"Melt name: {melt_name}")

print("\nMelt root:")
print(melt_dir)

print("\nMelt inputs:")
print(melt_inputs_dir)

print("\nMelt simulations:")
print(melt_simulations_dir)

print("\nDoes this melt already exist?")
print(melt_dir.exists())


# %% 12. Inspect single-chain MD-system naming

"""
A built polymer is not automatically an MD system.

The single-chain system builders can prepare:

dry
    The polymer in a simulation box without solvent.

solvated
    The polymer surrounded by water.

solvated with ions
    The polymer surrounded by water and a selected salt concentration.
"""

dry_system_name = paths.get_dry_PHA_system_name(
    example_polymer_name
)

solvated_system_name = (
    paths.get_solvated_PHA_system_name(
        example_polymer_name
    )
)

ionised_system_name = (
    paths.get_solvated_ions_PHA_system_name(
        polymer_name=example_polymer_name,
        salt="KCl",
        ion_concentration=0.15,
    )
)

print("\n" + "=" * 80)
print("SINGLE-CHAIN MD-SYSTEM NAMES")
print("=" * 80)

print(f"Dry system:              {dry_system_name}")
print(f"Solvated system:         {solvated_system_name}")
print(f"Solvated + ion system:   {ionised_system_name}")


# %% 13. Inspect single-chain MD-system directories

dry_system_dir = paths.get_dry_PHA_dir(
    example_polymer_name
)

solvated_system_dir = (
    paths.get_solvated_PHA_dir(
        example_polymer_name
    )
)

ionised_system_dir = (
    paths.get_solvated_ions_PHA_dir(
        polymer_name=example_polymer_name,
        salt="KCl",
        ion_concentration=0.15,
    )
)

print("\n" + "=" * 80)
print("SINGLE-CHAIN MD-SYSTEM DIRECTORIES")
print("=" * 80)

for description, directory in {
    "Dry system": dry_system_dir,
    "Solvated system": solvated_system_dir,
    "Solvated + ion system": ionised_system_dir,
}.items():
    print(f"\n{description}")
    print(f"  Path:   {directory}")
    print(f"  Exists: {directory.exists()}")


# %% 14. Load the MD-system registry

"""
md_systems.csv records prepared systems that can be selected by the GUI
or passed to the OpenMM script builder.

The registry stores:

    system_name
    system_type
    number_of_atoms

It does not need to store paths.

PHAFileManager reconstructs the paths from the system name and type.
"""

print("\n" + "=" * 80)
print("MD-SYSTEM REGISTRY")
print("=" * 80)

registered_systems = paths.load_md_systems()

if not registered_systems:
    print("No MD systems are currently registered.")

else:
    print(
        f"Registered systems: {len(registered_systems)}"
    )

    for row in registered_systems:
        system_name = row.get(
            "system_name",
            "",
        )

        system_type = row.get(
            "system_type",
            "",
        )

        number_of_atoms = row.get(
            "number_of_atoms",
            "",
        )

        if not number_of_atoms:
            number_of_atoms = "unknown"

        print(
            f"  {system_name:<40} "
            f"{system_type:<16} "
            f"{number_of_atoms} atoms"
        )


# %% 15. Resolve files for one registered MD system

"""
This section demonstrates the key registry workflow:

    system name + system type
            ↓
    PHAFileManager
            ↓
    topology and coordinate paths

The first registered system is used as an example.
"""

print("\n" + "=" * 80)
print("RESOLVE A REGISTERED MD SYSTEM")
print("=" * 80)

if not registered_systems:
    print(
        "There is no registered system available "
        "for file resolution."
    )

else:
    selected_system = registered_systems[0]

    selected_system_name = selected_system[
        "system_name"
    ]

    selected_system_type = selected_system[
        "system_type"
    ]

    print("Selected registry entry:")
    print(f"  Name: {selected_system_name}")
    print(f"  Type: {selected_system_type}")

    try:
        system_files = paths.get_md_system_files(
            system_name=selected_system_name,
            system_type=selected_system_type,
        )

        print("\nResolved files:")

        for file_role, file_path in system_files.items():
            print(f"\n{file_role}")
            print(f"  {file_path}")

            if isinstance(
                file_path,
                Path,
            ):
                print(
                    f"  Exists: {file_path.exists()}"
                )

    except Exception as error:
        print(
            "\nThe system entry was found, but its "
            "files could not be resolved."
        )

        print(error)


# %% 16. Validate one registered MD system

"""
validate_md_system_files performs a stricter check.

It raises an exception when required topology or coordinate files are missing.

This is used by the GUI and OpenMM script builder before starting a
simulation.
"""

print("\n" + "=" * 80)
print("VALIDATE A REGISTERED MD SYSTEM")
print("=" * 80)

if not registered_systems:
    print(
        "There is no registered system available "
        "for validation."
    )

else:
    selected_system = registered_systems[0]

    try:
        validated_files = (
            paths.validate_md_system_files(
                system_name=selected_system[
                    "system_name"
                ],
                system_type=selected_system[
                    "system_type"
                ],
            )
        )

        print("The registered system is valid.")

        print("\nTopology:")
        print(
            validated_files["topology_file"]
        )

        print("\nCoordinates:")
        print(
            validated_files["coordinate_file"]
        )

    except Exception as error:
        print(
            "The registered system failed validation."
        )

        print(error)


# %% 17. List files in selected directories

"""
PHAFileManager also provides general file-search helpers.

find_file
    Returns the first matching file.

find_files
    Returns all matching files.
"""

print("\n" + "=" * 80)
print("GENERAL FILE HELPERS")
print("=" * 80)

amber_pdb_files = paths.find_files(
    built_amber_dir,
    "pdb",
)

print(
    f"PDB files found in {built_amber_dir}: "
    f"{len(amber_pdb_files)}"
)

for file_path in amber_pdb_files:
    print(f"  {file_path.name}")


# %% 18. Summary

print("\n" + "=" * 80)
print("TUTORIAL SUMMARY")
print("=" * 80)

print(
    """
The structure database separates the iPHAsimulator workflow into several
layers:

1. PHA chemistry

   PHA_types/<PHA_type>/

   Stores chemistry-specific parameter files.

2. Built polymer chains

   built_PHAs/<polymer_name>/

   Stores finite Amber and GROMACS polymer structures.

3. Prepared MD systems

   PHA_dry/
   PHA_solvated/
   PHA_solvated_ions/
   PHA_melts/

   Stores systems ready for molecular-dynamics simulation.

4. MD-system registry

   md_systems.csv

   Allows the GUI and OpenMM script builder to discover available systems.

The filepath manager should be used whenever a module needs to locate or
create files. Other modules should not reproduce the directory naming logic
manually.
"""
)

print("Tutorial 00 complete.")