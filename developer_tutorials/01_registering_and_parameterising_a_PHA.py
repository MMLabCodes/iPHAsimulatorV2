#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tutorial 01: Registering and parameterising a PHA chemistry.

Purpose
-------
This tutorial explains how a new PHA chemistry is added to iPHAsimulatorV2.

The workflow is:

    PHA name and SMILES
            ↓
    Register the chemistry and residue codes
            ↓
    Create the PHA-type directory structure
            ↓
    Parameterise a trimer
            ↓
    Generate head, mainchain, and tail PREPIN files
            ↓
    Verify the completed parameterisation

This tutorial uses 3HB as the worked example.

Important
---------
Parameterisation can call external AmberTools programs such as:

    antechamber
    parmchk2
    prepgen

The tutorial therefore includes switches controlling whether expensive or
destructive steps are executed.

By default, the script inspects the current database and explains what would
happen. Change the switches in the User settings section when you are ready
to run the parameterisation steps.

Prerequisites
-------------
The following must be available:

- AmberTools
- the iPHAsimulatorV2 source package
- a valid monomer SMILES
- a valid trimer SMILES
- manual PREPGEN definition files for the head, mainchain, and tail residues

Expected manual definition files for this example:

    structure_database/
        PHA_types/
            3HB/
                input/
                    head_P3HB_3.txt
                    mainchain_P3HB_3.txt
                    tail_P3HB_3.txt

Outputs
-------
When all stages are run successfully, the main outputs are:

    structure_database/
        residue_codes.csv

        PHA_types/
            3HB/
                input/
                    head_P3HB_3.txt
                    mainchain_P3HB_3.txt
                    tail_P3HB_3.txt

                trimer/
                    P3HB_3.pdb
                    P3HB_3.mol2
                    P3HB_3.ac
                    P3HB_3.frcmod

                monomer_units/
                    hP3HB.prepin
                    mP3HB.prepin
                    tP3HB.prepin

Notes
-----
The ``# %%`` markers allow this script to be used as:

- a normal Python script
- a Spyder cell-based script
- a VS Code interactive script
- the basis of a Jupyter notebook
"""

# %% 1. Imports

from pathlib import Path
import csv
import sys


# %% 2. Locate the project root

# This tutorial is expected to be saved in:
#
#     iPHAsimulatorV2/tutorials/
#
# Therefore, parents[1] is the project root.

PROJECT_ROOT = Path(__file__).resolve().parents[1]

STRUCTURE_DATABASE = (
    PROJECT_ROOT
    / "structure_database"
)

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT),
    )

from src.iphasimulator.pha_filepath_manager import (
    PHAFileManager,
    PHAResidueCodeManager,
)

from src.iphasimulator.build_pha import (
    PHAPolymerBuilder,
)


# %% 3. User settings

# ----------------------------------------------------------
# PHA identity
# ----------------------------------------------------------

PHA_type = "3HB"

trimer_name = "P3HB_3"


# ----------------------------------------------------------
# Molecular structures
# ----------------------------------------------------------

# The monomer SMILES represents one hydroxyalkanoate repeat-unit precursor.

monomer_smiles = (
    "O[C@H](C)CC(=O)O"
)

# The trimer contains three connected repeat units.
#
# The trimer is used for charge calculation and force-field
# parameter generation.

trimer_smiles = (
    "O[C@H](C)CC(=O)"
    "O[C@H](C)CC(=O)"
    "O[C@H](C)CC(=O)O"
)


# ----------------------------------------------------------
# Parameterisation settings
# ----------------------------------------------------------

forcefield = "gaff2"

charge_model = "abcg2"


# ----------------------------------------------------------
# Execution switches
# ----------------------------------------------------------

# Registration is lightweight and only updates the database.
#
# Set this to True to register the PHA chemistry if it is not
# already present.

RUN_REGISTRATION = False


# Trimer parameterisation can call AmberTools programs.
#
# Set this to True only when you are ready to create or replace
# the trimer parameter files.

RUN_TRIMER_PARAMETERISATION = False


# PREPIN generation requires the manual definition files in:
#
#     PHA_types/<PHA_type>/input/
#
# Set this to True after the trimer parameterisation and manual
# definition files are ready.

RUN_PREPIN_GENERATION = False


# %% 4. Initialise the central manager objects

paths = PHAFileManager(
    root_dir=STRUCTURE_DATABASE
)

residue_manager = PHAResidueCodeManager(
    paths=paths
)

builder = PHAPolymerBuilder(
    root_dir=STRUCTURE_DATABASE
)

print("=" * 80)
print("Tutorial 01: Registering and parameterising a PHA")
print("=" * 80)

print("\nProject root:")
print(PROJECT_ROOT)

print("\nStructure database:")
print(STRUCTURE_DATABASE)

print("\nPHA type:")
print(PHA_type)

print("\nTrimer name:")
print(trimer_name)

print("\nForce field:")
print(forcefield)

print("\nCharge model:")
print(charge_model)


# %% 5. Understand what is being registered

print("\n" + "=" * 80)
print("WHAT IS A REGISTERED PHA TYPE?")
print("=" * 80)

print(
    """
A registered PHA type represents one chemical repeat-unit family.

For this tutorial:

    PHA type:
        3HB

    Human-readable polymer prefix:
        P3HB

Registration does not build a complete polymer.

Instead, it records the identities of four related components:

    trimer
        A three-unit molecule used during parameterisation.

    head
        The first residue in a polymer chain.

    mainchain
        An internal repeat unit.

    tail
        The final residue in a polymer chain.

Each component receives a unique three-letter Amber residue code.
"""
)


# %% 6. Inspect whether the PHA type is already registered

print("\n" + "=" * 80)
print("CURRENT REGISTRATION STATUS")
print("=" * 80)

PHA_already_registered = (
    residue_manager.PHA_type_exists(
        PHA_type
    )
)

print(
    f"Is {PHA_type} already registered? "
    f"{PHA_already_registered}"
)

if PHA_already_registered:
    print(
        "\nThe existing residue-code entries are:"
    )

    for component in [
        "trimer",
        "head",
        "mainchain",
        "tail",
    ]:
        residue_code = residue_manager.get_code(
            PHA_type=PHA_type,
            component=component,
        )

        print(
            f"  {component:<10} "
            f"{residue_code}"
        )

else:
    print(
        "\nThe PHA chemistry is not yet registered."
    )


# %% 7. Preview the names that registration will create

print("\n" + "=" * 80)
print("READABLE COMPONENT NAMES")
print("=" * 80)

component_names = {
    "trimer": trimer_name,
    "head": f"hP{PHA_type}",
    "mainchain": f"mP{PHA_type}",
    "tail": f"tP{PHA_type}",
}

for component, readable_name in (
    component_names.items()
):
    print(
        f"{component:<10} "
        f"{readable_name}"
    )

print(
    """
The readable names describe each residue's role.

For 3HB:

    hP3HB
        Head residue.

    mP3HB
        Mainchain residue.

    tP3HB
        Tail residue.

These readable names are different from the three-letter Amber residue
codes stored in residue_codes.csv.
"""
)


# %% 8. Register the PHA type

print("\n" + "=" * 80)
print("REGISTER THE PHA TYPE")
print("=" * 80)

if not RUN_REGISTRATION:
    print(
        "Registration has not been executed because "
        "RUN_REGISTRATION is False."
    )

    print(
        "\nTo register this chemistry, set:"
    )

    print(
        "    RUN_REGISTRATION = True"
    )

elif PHA_already_registered:
    print(
        f"{PHA_type} is already registered. "
        "No duplicate rows will be added."
    )

else:
    residue_manager.register_PHA_type(
        PHA_type=PHA_type,
        trimer_name=trimer_name,
        trimer_smiles=trimer_smiles,
        monomer_smiles=monomer_smiles,
    )

    print(
        f"\nRegistration completed for {PHA_type}."
    )


# %% 9. Inspect residue_codes.csv

print("\n" + "=" * 80)
print("RESIDUE-CODE DATABASE")
print("=" * 80)

residue_codes_csv = (
    paths.get_residue_codes_csv()
)

print("\nDatabase path:")
print(residue_codes_csv)

if not residue_codes_csv.exists():
    print(
        "\nThe residue-code database does not exist."
    )

else:
    with open(
        residue_codes_csv,
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        reader = csv.DictReader(file)

        registered_rows = [
            row
            for row in reader
            if row.get("PHA_type") == PHA_type
        ]

    if not registered_rows:
        print(
            f"\nNo rows were found for {PHA_type}."
        )

    else:
        print(
            f"\nRows registered for {PHA_type}:"
        )

        for row in registered_rows:
            print(
                "\n"
                f"Component:     {row.get('component', '')}\n"
                f"Readable name: {row.get('readable_name', '')}\n"
                f"Residue code:  {row.get('residue_code', '')}\n"
                f"SMILES:        {row.get('smiles', '')}"
            )


# %% 10. Create the PHA-type directory structure

print("\n" + "=" * 80)
print("CREATE THE PHA-TYPE DIRECTORY STRUCTURE")
print("=" * 80)

# This operation is safe to repeat because mkdir uses exist_ok=True.

PHA_type_dir = paths.create_PHA_type_dir(
    PHA_type
)

print("\nPHA-type directory:")
print(PHA_type_dir)

expected_directories = {
    "Manual inputs": (
        paths.get_PHA_input_dir(
            PHA_type
        )
    ),
    "Trimer parameters": (
        paths.get_PHA_trimer_dir(
            PHA_type
        )
    ),
    "Monomer units": (
        paths.get_PHA_monomer_units_dir(
            PHA_type
        )
    ),
    "TLEaP templates": (
        paths.get_PHA_leap_template_dir(
            PHA_type
        )
    ),
}

for description, directory in (
    expected_directories.items()
):
    print(f"\n{description}")
    print(f"  Path:   {directory}")
    print(f"  Exists: {directory.exists()}")


# %% 11. Understand why a trimer is parameterised

print("\n" + "=" * 80)
print("WHY PARAMETERISE A TRIMER?")
print("=" * 80)

print(
    """
The parameterisation workflow uses a trimer rather than an isolated
monomer because the central repeat unit experiences polymer-like
connections on both sides.

The trimer is used to generate:

    atom types
    partial charges
    bonded parameters
    missing force-field terms

The resulting trimer data are then divided into:

    head residue
    mainchain residue
    tail residue

These three residue types can later be assembled into polymers of
arbitrary length.
"""
)


# %% 12. Display the parameterisation inputs

print("\n" + "=" * 80)
print("TRIMER PARAMETERISATION INPUTS")
print("=" * 80)

print("\nPHA type:")
print(PHA_type)

print("\nTrimer name:")
print(trimer_name)

print("\nMonomer SMILES:")
print(monomer_smiles)

print("\nTrimer SMILES:")
print(trimer_smiles)

print("\nForce field:")
print(forcefield)

print("\nCharge model:")
print(charge_model)


# %% 13. Parameterise the trimer

print("\n" + "=" * 80)
print("PARAMETERISE THE TRIMER")
print("=" * 80)

if not RUN_TRIMER_PARAMETERISATION:
    print(
        "Trimer parameterisation has not been executed because "
        "RUN_TRIMER_PARAMETERISATION is False."
    )

    print(
        "\nTo run this stage, set:"
    )

    print(
        "    RUN_TRIMER_PARAMETERISATION = True"
    )

else:
    parameterisation_result = (
        builder.parameterise_trimer(
            PHA_type=PHA_type,
            trimer_name=trimer_name,
            trimer_smiles=trimer_smiles,
            monomer_smiles=monomer_smiles,
            forcefield=forcefield,
            charge_model=charge_model,
        )
    )

    print(
        "\nTrimer parameterisation completed."
    )

    print(
        "\nReturned result:"
    )

    print(
        parameterisation_result
    )


# %% 14. Inspect the expected trimer files

print("\n" + "=" * 80)
print("EXPECTED TRIMER FILES")
print("=" * 80)

trimer_dir = paths.get_PHA_trimer_dir(
    PHA_type
)

expected_trimer_files = {
    "PDB structure": (
        trimer_dir
        / f"{trimer_name}.pdb"
    ),
    "MOL2 structure and charges": (
        trimer_dir
        / f"{trimer_name}.mol2"
    ),
    "Antechamber AC file": (
        trimer_dir
        / f"{trimer_name}.ac"
    ),
    "Additional force-field parameters": (
        trimer_dir
        / f"{trimer_name}.frcmod"
    ),
}

for description, file_path in (
    expected_trimer_files.items()
):
    print(f"\n{description}")
    print(f"  Path:   {file_path}")
    print(f"  Exists: {file_path.exists()}")


# %% 15. Explain the manual PREPGEN definition files

print("\n" + "=" * 80)
print("MANUAL PREPGEN DEFINITION FILES")
print("=" * 80)

input_dir = paths.get_PHA_input_dir(
    PHA_type
)

definition_files = {
    "Head definition": (
        input_dir
        / f"head_{trimer_name}.txt"
    ),
    "Mainchain definition": (
        input_dir
        / f"mainchain_{trimer_name}.txt"
    ),
    "Tail definition": (
        input_dir
        / f"tail_{trimer_name}.txt"
    ),
}

for description, file_path in (
    definition_files.items()
):
    print(f"\n{description}")
    print(f"  Path:   {file_path}")
    print(f"  Exists: {file_path.exists()}")

print(
    """
These definition files tell PREPGEN which atoms belong to each residue
and which atoms are removed or connected during polymer assembly.

They are chemistry-specific and normally require manual preparation.

The expected files for this tutorial are:

    head_P3HB_3.txt
    mainchain_P3HB_3.txt
    tail_P3HB_3.txt
"""
)


# %% 16. Check whether PREPIN generation is ready

print("\n" + "=" * 80)
print("PREPIN-GENERATION READINESS")
print("=" * 80)

required_prepgen_inputs = [
    expected_trimer_files[
        "Antechamber AC file"
    ],
    definition_files[
        "Head definition"
    ],
    definition_files[
        "Mainchain definition"
    ],
    definition_files[
        "Tail definition"
    ],
]

missing_prepgen_inputs = [
    file_path
    for file_path in required_prepgen_inputs
    if not file_path.exists()
]

if missing_prepgen_inputs:
    print(
        "PREPIN generation is not ready."
    )

    print(
        "\nMissing files:"
    )

    for file_path in missing_prepgen_inputs:
        print(
            f"  {file_path}"
        )

else:
    print(
        "All required PREPGEN inputs were found."
    )


# %% 17. Generate the head, mainchain, and tail PREPIN files

print("\n" + "=" * 80)
print("GENERATE POLYMER RESIDUE PREPIN FILES")
print("=" * 80)

if not RUN_PREPIN_GENERATION:
    print(
        "PREPIN generation has not been executed because "
        "RUN_PREPIN_GENERATION is False."
    )

    print(
        "\nTo run this stage, set:"
    )

    print(
        "    RUN_PREPIN_GENERATION = True"
    )

elif missing_prepgen_inputs:
    print(
        "PREPIN generation cannot start because one or more "
        "required input files are missing."
    )

else:
    prepin_result = (
        builder.generate_polymer_prepins(
            PHA_type
        )
    )

    print(
        "\nPREPIN generation completed."
    )

    print(
        "\nReturned result:"
    )

    print(
        prepin_result
    )


# %% 18. Inspect the expected monomer-unit files

print("\n" + "=" * 80)
print("EXPECTED MONOMER-UNIT FILES")
print("=" * 80)

parameter_files = (
    paths.get_PHA_monomer_unit_files(
        PHA_type
    )
)

for file_role, file_path in (
    parameter_files.items()
):
    print(f"\n{file_role}")
    print(f"  Path:   {file_path}")
    print(f"  Exists: {Path(file_path).exists()}")


# %% 19. Explain the role of each PREPIN file

print("\n" + "=" * 80)
print("ROLE OF THE PREPIN FILES")
print("=" * 80)

print(
    f"""
For {PHA_type}, the expected polymer residues are:

    {parameter_files['head_prepin'].name}
        Used once at the beginning of the chain.

    {parameter_files['mainchain_prepin'].name}
        Repeated for internal monomer units.

    {parameter_files['tail_prepin'].name}
        Used once at the end of the chain.

For a ten-unit polymer, the conceptual sequence is:

    head
    + eight mainchain residues
    + tail

This produces:

    P{PHA_type}_10
"""
)


# %% 20. Verify the completed parameterisation

print("\n" + "=" * 80)
print("FINAL PARAMETERISATION CHECK")
print("=" * 80)

required_final_files = {
    "Head PREPIN": (
        parameter_files["head_prepin"]
    ),
    "Mainchain PREPIN": (
        parameter_files["mainchain_prepin"]
    ),
    "Tail PREPIN": (
        parameter_files["tail_prepin"]
    ),
    "FRCMOD": (
        parameter_files["frcmod"]
    ),
}

all_final_files_exist = True

for description, file_path in (
    required_final_files.items()
):
    file_exists = Path(
        file_path
    ).exists()

    print(
        f"{description:<20} "
        f"{'FOUND' if file_exists else 'MISSING'}"
    )

    print(
        f"  {file_path}"
    )

    if not file_exists:
        all_final_files_exist = False


# %% 21. Report build readiness

print("\n" + "=" * 80)
print("POLYMER-BUILD READINESS")
print("=" * 80)

if all_final_files_exist:
    print(
        f"{PHA_type} is ready for polymer construction."
    )

    print(
        "\nThe next tutorial can use:"
    )

    print(
        f"""
    builder.build_PHA_polymer(
        PHA_type="{PHA_type}",
        length=10,
    )
"""
    )

else:
    print(
        f"{PHA_type} is not yet fully ready for polymer construction."
    )

    print(
        "\nComplete the missing parameterisation stages before "
        "attempting to build a polymer."
    )


# %% 22. Show the expected final directory tree

print("\n" + "=" * 80)
print("EXPECTED FINAL DIRECTORY STRUCTURE")
print("=" * 80)

print(
    f"""
structure_database/
│
├── residue_codes.csv
│
└── PHA_types/
    │
    └── {PHA_type}/
        │
        ├── input/
        │   ├── head_{trimer_name}.txt
        │   ├── mainchain_{trimer_name}.txt
        │   └── tail_{trimer_name}.txt
        │
        ├── trimer/
        │   ├── {trimer_name}.pdb
        │   ├── {trimer_name}.mol2
        │   ├── {trimer_name}.ac
        │   └── {trimer_name}.frcmod
        │
        ├── monomer_units/
        │   ├── hP{PHA_type}.prepin
        │   ├── mP{PHA_type}.prepin
        │   └── tP{PHA_type}.prepin
        │
        └── leap_templates/
"""
)


# %% 23. Tutorial summary

print("\n" + "=" * 80)
print("TUTORIAL SUMMARY")
print("=" * 80)

print(
    """
The key stages in registering and parameterising a PHA are:

1. Define the PHA type, monomer SMILES, and trimer SMILES.

2. Register the PHA type in residue_codes.csv.

3. Assign separate residue codes to the:

       trimer
       head
       mainchain
       tail

4. Create the standard PHA-type directory structure.

5. Parameterise the trimer using the selected force field and
   charge model.

6. Provide the three manual PREPGEN definition files.

7. Generate the head, mainchain, and tail PREPIN files.

8. Confirm that all three PREPIN files and the FRCMOD file exist.

Once these files are available, polymers of different lengths can be
assembled without repeating the chemistry parameterisation.

Next tutorial
-------------
Tutorial 02 will explain how to build finite PHA polymer chains from
the registered head, mainchain, and tail residues.
"""
)

print("\nTutorial 01 complete.")