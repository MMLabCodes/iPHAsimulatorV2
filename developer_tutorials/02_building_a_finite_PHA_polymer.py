#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
===============================================================================
Tutorial 02 - Building Your First PHA Polymer
===============================================================================

Welcome!

In Tutorial 01 we parameterised a PHA chemistry.

That process produced four important files:

    • Head PREPIN
    • Mainchain PREPIN
    • Tail PREPIN
    • FRCMOD

Those files completely describe the chemistry of a repeat unit.

In this tutorial we are NOT creating any new force field parameters.

Instead, we will reuse those existing residue definitions to construct a
polymer of any length.

The workflow looks like this:

        Parameterised chemistry
                  │
                  ▼
        Head/Main/Tail residues
                  │
                  ▼
              TLEaP
                  │
                  ▼
          Amber polymer files
                  │
                  ▼
        GROMACS polymer files

By the end of this tutorial you will understand

• why three residue types are needed
• what TLEaP actually does
• how arbitrary chain lengths are produced
• where every generated file comes from

===============================================================================
"""

# %% ==========================================================================
# Imports
# ==============================================================================

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

STRUCTURE_DATABASE = PROJECT_ROOT / "structure_database"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.iphasimulator.pha_filepath_manager import PHAFileManager
from src.iphasimulator.build_pha import PHAPolymerBuilder


# %% ==========================================================================
# User settings
# ==============================================================================

"""
These are the only settings we need.

PHA_type
    Determines the chemistry.

polymer_length
    Determines how many repeat units should be assembled.
"""

PHA_type = "3HB"

polymer_length = 10

RUN_BUILD = False


# %% ==========================================================================
# Initialise the project
# ==============================================================================

paths = PHAFileManager(
    root_dir=STRUCTURE_DATABASE,
)

builder = PHAPolymerBuilder(
    root_dir=STRUCTURE_DATABASE,
)

polymer_name = paths.get_built_PHA_name(
    PHA_type=PHA_type,
    length=polymer_length,
)

print("=" * 80)
print("Tutorial 02 - Building Your First Polymer")
print("=" * 80)

print(f"\nPHA chemistry : {PHA_type}")
print(f"Polymer name : {polymer_name}")
print(f"Chain length : {polymer_length}")


# %% ==========================================================================
# What are we actually building?
# ==============================================================================

print("\n")
print("=" * 80)
print("WHAT DOES A POLYMER LOOK LIKE?")
print("=" * 80)

print(
"""
Suppose we request

    P3HB_5

Internally the builder does NOT create five identical residues.

Instead it constructs

    HEAD

       ↓

    MAIN

       ↓

    MAIN

       ↓

    MAIN

       ↓

    TAIL

Notice there are only THREE residue types.

The same idea works for every polymer length.

P3HB_10

    HEAD

       ↓

    MAIN × 8

       ↓

    TAIL

P3HB_100

    HEAD

       ↓

    MAIN × 98

       ↓

    TAIL

This is why we generated three PREPIN files during Tutorial 01.

The chemistry never changes.

Only the number of MAIN residues changes.
"""
)


# %% ==========================================================================
# Why are three residues required?
# ==============================================================================

print("\n")
print("=" * 80)
print("WHY DO WE NEED THREE RESIDUES?")
print("=" * 80)

print(
"""
Think about a polymer chain.

The first monomer has

    one free end

The middle monomers have

    two polymer neighbours

The last monomer has

    one free end

These are chemically different environments.

Consequently they require three residue definitions.

Head

    Used exactly once.

Mainchain

    Repeated many times.

Tail

    Used exactly once.

For a polymer containing N repeat units

Head residues

    1

Mainchain residues

    N - 2

Tail residues

    1

For our example

N = 10

therefore

Head       = 1

Mainchain  = 8

Tail       = 1
"""
)


# %% ==========================================================================
# Locate the parameter files
# ==============================================================================

print("\n")
print("=" * 80)
print("LOCATING THE PARAMETER FILES")
print("=" * 80)

parameter_files = paths.get_PHA_monomer_unit_files(
    PHA_type
)

for key, value in parameter_files.items():

    value = Path(value)

    exists = "✓" if value.exists() else "✗"

    print(f"{exists} {key:18s} {value}")


print(
"""

These files were produced during Tutorial 01.

Nothing new will be parameterised during this tutorial.

Instead, these files will simply be reused.

"""
)


# %% ==========================================================================
# Is the chemistry ready?
# ==============================================================================

print("\n")
print("=" * 80)
print("CHEMISTRY READINESS")
print("=" * 80)

required = [
    "head_prepin",
    "mainchain_prepin",
    "tail_prepin",
    "frcmod",
]

ready = True

for file in required:

    path = Path(parameter_files[file])

    if path.exists():

        print(f"✓ {path.name}")

    else:

        ready = False

        print(f"✗ {path.name}")

print()

if ready:

    print(
"""
Excellent!

The chemistry has already been parameterised.

We are ready to build polymers.
"""
    )

else:

    print(
"""
The chemistry is NOT ready.

One or more required parameter files are missing.

Please complete Tutorial 01 before continuing.
"""
    )


# %% ==========================================================================
# Meet PHAPolymerBuilder
# ==============================================================================

print("\n")
print("=" * 80)
print("THE POLYMER BUILDER")
print("=" * 80)

print(
"""
PHAPolymerBuilder is responsible for turning a parameterised chemistry
into a complete polymer.

Internally it performs many operations automatically.

                You

                 │

                 ▼

    build_PHA_polymer()

                 │

                 ▼

      Locate PREPIN files

                 │

                 ▼

      Locate FRCMOD file

                 │

                 ▼

      Generate TLEaP input

                 │

                 ▼

          Execute TLEaP

                 │

                 ▼

      Create Amber topology

                 │

                 ▼

     Convert to GROMACS files

                 │

                 ▼

      Organise output folders

Fortunately we only need a single function call.

The builder handles all of these steps automatically.
"""
)


# %% ==========================================================================
# What happens inside build_PHA_polymer()?
# ==============================================================================

print("\n")
print("=" * 80)
print("WHAT HAPPENS INSIDE THE BUILDER?")
print("=" * 80)

print(
f"""
Suppose we request

    {polymer_name}

The builder first resolves

    hP{PHA_type}

    mP{PHA_type}

    tP{PHA_type}

along with the associated FRCMOD file.

Next it writes a temporary TLEaP script.

Conceptually that script looks something like

    load head residue

            ↓

    load main residue

            ↓

    load tail residue

            ↓

    assemble sequence

            ↓

    save Amber files

TLEaP performs all of the chemistry.

Our Python code simply tells TLEaP

    which residues to use

and

    how many should be connected.
"""
)


# %% ==========================================================================
# Understanding the residue sequence
# ==============================================================================

print("\n")
print("=" * 80)
print("THE RESIDUE SEQUENCE")
print("=" * 80)

sequence = (
    ["HEAD"]
    + ["MAIN"] * (polymer_length - 2)
    + ["TAIL"]
)

print()

for i, residue in enumerate(sequence, start=1):

    print(f"{i:2d}   {residue}")

print(
"""

Notice something interesting.

Only the number of MAIN residues changes.

Everything else remains identical.

That means the same chemistry can be reused for

P3HB_5

P3HB_10

P3HB_20

P3HB_100

without ever repeating the parameterisation stage.

This is one of the biggest advantages of the residue-based approach used
by Amber.
"""
)


# %% ==========================================================================
# Where will the polymer be stored?
# ==============================================================================

print("\n")
print("=" * 80)
print("OUTPUT DIRECTORY")
print("=" * 80)

polymer_directory = paths.get_built_PHA_dir(
    PHA_type,
    polymer_length,
)

print(polymer_directory)

print(
"""

After construction the directory will typically contain

built_PHAs/

    P3HB_10/

        amber/

        gromacs/

        leap/

Each folder has a different purpose.

amber/

    Native Amber files.

gromacs/

    Files converted for GROMACS.

leap/

    Temporary scripts and build logs.
"""
)


# %% ==========================================================================
# Ready to build
# ==============================================================================

print("\n")
print("=" * 80)
print("READY TO BUILD")
print("=" * 80)

if not RUN_BUILD:

    print(
"""
The polymer will NOT be built because

RUN_BUILD = False

This allows us to inspect the workflow safely.

When you are ready simply change

RUN_BUILD = True

The next section will then construct

    {}

using the existing residue definitions.
""".format(polymer_name)
    )

else:

    print(f"Building {polymer_name} ...")

    result = builder.build_PHA_polymer(
        PHA_type=PHA_type,
        length=polymer_length,
    )

    print(result)
    
# %% ==========================================================================
# Inspect the completed build
# ==============================================================================

print("\n")
print("=" * 80)
print("INSPECTING THE COMPLETED BUILD")
print("=" * 80)

print(
"""
Once the polymer has been built, the next step is not simply to assume
that everything worked.

We should inspect the files that were created and confirm that the polymer
can be used by both Amber and GROMACS.

This section will examine:

    Amber files

    GROMACS files

    file sizes

    atom counts

    residue counts

    coordinate records

    basic topology loading

The goal is to distinguish between

    files that merely exist

and

    files that form a valid molecular system.
"""
)


# %% ==========================================================================
# Resolve the built-polymer directories
# ==============================================================================

print("\n")
print("=" * 80)
print("RESOLVING THE OUTPUT DIRECTORIES")
print("=" * 80)

amber_directory = paths.get_built_PHA_amber_dir(
    PHA_type=PHA_type,
    length=polymer_length,
)

gromacs_directory = paths.get_built_PHA_gromacs_dir(
    PHA_type=PHA_type,
    length=polymer_length,
)

leap_directory = paths.get_built_PHA_leap_dir(
    PHA_type=PHA_type,
    length=polymer_length,
)

build_directories = {
    "Polymer root": polymer_directory,
    "Amber": amber_directory,
    "GROMACS": gromacs_directory,
    "TLEaP": leap_directory,
}

for directory_role, directory_path in build_directories.items():

    directory_path = Path(directory_path)

    status = (
        "FOUND"
        if directory_path.exists()
        else "MISSING"
    )

    print(f"\n{directory_role}")
    print(f"  Status: {status}")
    print(f"  Path:   {directory_path}")


# %% ==========================================================================
# Helper function for displaying files
# ==============================================================================

def describe_file(
    file_path,
    description,
):
    """
    Print a concise report for one output file.

    Parameters
    ----------
    file_path : str or pathlib.Path
        File to inspect.

    description : str
        Human-readable explanation of the file.
    """

    file_path = Path(file_path)

    print(f"\n{file_path.name}")
    print(f"  Purpose: {description}")
    print(f"  Path:    {file_path}")
    print(f"  Exists:  {file_path.exists()}")

    if file_path.exists():

        size_bytes = file_path.stat().st_size

        size_kilobytes = (
            size_bytes
            / 1024
        )

        print(
            f"  Size:    "
            f"{size_bytes:,} bytes "
            f"({size_kilobytes:,.2f} KiB)"
        )

        if size_bytes == 0:

            print(
                "  Warning: The file exists but is empty."
            )


# %% ==========================================================================
# Locate the Amber files
# ==============================================================================

print("\n")
print("=" * 80)
print("AMBER FILES")
print("=" * 80)

print(
"""
Amber normally represents the polymer using three principal files.

PDB

    A human-readable structure file.

PRMTOP

    The molecular topology and force-field information.

RST7

    The coordinate file used together with the PRMTOP.

These files describe different parts of the same system.

The PRMTOP does not normally contain the coordinates.

The RST7 does not contain the full force-field description.

They must therefore be used together.
"""
)

try:

    amber_files = paths.get_built_PHA_amber_files(
        polymer_name
    )

except TypeError:

    amber_files = paths.get_built_PHA_amber_files(
        PHA_type=PHA_type,
        length=polymer_length,
    )


# Convert all returned paths into Path objects.

amber_files = {
    key: Path(value)
    for key, value in amber_files.items()
}


# %% ==========================================================================
# Explain and inspect the PDB file
# ==============================================================================

pdb_path = amber_files.get(
    "pdb"
)

if pdb_path is None:

    pdb_path = (
        Path(amber_directory)
        / f"{polymer_name}.pdb"
    )

describe_file(
    pdb_path,
    (
        "Human-readable atomic coordinates, atom names, "
        "residue names, and residue numbers."
    ),
)

print(
"""
The PDB file is particularly useful for:

    visually inspecting the polymer

    checking atom and residue names

    opening the structure in molecular viewers

    confirming that the chain has the expected number of residues

It is convenient for inspection, but the PDB is not usually the main
simulation topology.
"""
)


# %% ==========================================================================
# Explain and inspect the PRMTOP file
# ==============================================================================

prmtop_path = amber_files.get(
    "prmtop"
)

if prmtop_path is None:

    prmtop_path = (
        Path(amber_directory)
        / f"{polymer_name}.prmtop"
    )

describe_file(
    prmtop_path,
    (
        "Amber topology containing atoms, charges, atom types, "
        "bonds, angles, dihedrals, and force-field parameters."
    ),
)

print(
"""
The PRMTOP is one of the most important files in the entire workflow.

It contains information such as:

    atom identities

    partial charges

    atomic masses

    Lennard-Jones parameters

    bond parameters

    angle parameters

    torsional parameters

    residue membership

The PRMTOP is what allows a simulation engine to interpret the polymer as
a force-field model rather than merely a collection of coordinates.
"""
)


# %% ==========================================================================
# Explain and inspect the RST7 file
# ==============================================================================

rst7_path = amber_files.get(
    "rst7"
)

if rst7_path is None:

    rst7_path = (
        Path(amber_directory)
        / f"{polymer_name}.rst7"
    )

describe_file(
    rst7_path,
    (
        "Amber coordinates corresponding to the atoms stored "
        "in the PRMTOP topology."
    ),
)

print(
"""
The RST7 file is normally loaded alongside the PRMTOP.

The atom ordering in both files must agree exactly.

For example:

    PRMTOP atom 1

must correspond to

    RST7 coordinate 1

If the atom counts or ordering differ, the system cannot be interpreted
correctly.
"""
)


# %% ==========================================================================
# Amber file completeness check
# ==============================================================================

print("\n")
print("=" * 80)
print("AMBER COMPLETENESS CHECK")
print("=" * 80)

required_amber_files = {
    "PDB": pdb_path,
    "PRMTOP": prmtop_path,
    "RST7": rst7_path,
}

amber_files_complete = True

for file_label, file_path in required_amber_files.items():

    file_path = Path(file_path)

    if file_path.exists() and file_path.stat().st_size > 0:

        print(
            f"✓ {file_label:<8} "
            f"{file_path.name}"
        )

    else:

        amber_files_complete = False

        print(
            f"✗ {file_label:<8} "
            f"{file_path.name}"
        )

print()

if amber_files_complete:

    print(
        "All expected Amber files were found and are non-empty."
    )

else:

    print(
"""
The Amber output is incomplete.

Possible causes include:

    TLEaP did not finish successfully

    one or more files were moved

    the requested polymer has not yet been built

    the output naming convention differs from the expected convention
"""
    )


# %% ==========================================================================
# Locate the GROMACS files
# ==============================================================================

print("\n")
print("=" * 80)
print("GROMACS FILES")
print("=" * 80)

print(
"""
The Amber polymer may also be converted into GROMACS format.

A typical GROMACS representation contains:

GRO

    Coordinates.

TOP

    The main system topology.

ITP

    The reusable molecule topology.

These files are commonly generated using ACPYPE or a related conversion
workflow.
"""
)

try:

    gromacs_files = paths.get_built_PHA_gromacs_files(
        polymer_name
    )

except (AttributeError, TypeError):

    gromacs_files = {
        "gro": (
            Path(gromacs_directory)
            / f"{polymer_name}.gro"
        ),
        "top": (
            Path(gromacs_directory)
            / f"{polymer_name}.top"
        ),
        "itp": (
            Path(gromacs_directory)
            / f"{polymer_name}.itp"
        ),
    }

gromacs_files = {
    key: Path(value)
    for key, value in gromacs_files.items()
}


# %% ==========================================================================
# Explain and inspect the GRO file
# ==============================================================================

gro_path = gromacs_files.get(
    "gro"
)

if gro_path is None:

    gro_path = (
        Path(gromacs_directory)
        / f"{polymer_name}.gro"
    )

describe_file(
    gro_path,
    (
        "GROMACS coordinate file containing atom positions, "
        "residue names, atom names, and box vectors."
    ),
)

print(
"""
The GRO file is compact and designed for GROMACS.

It normally contains:

    a title line

    the total number of atoms

    one coordinate record per atom

    the simulation box dimensions

Unlike a PDB file, the GRO file often stores coordinates in nanometres.
"""
)


# %% ==========================================================================
# Explain and inspect the TOP file
# ==============================================================================

top_path = gromacs_files.get(
    "top"
)

if top_path is None:

    top_path = (
        Path(gromacs_directory)
        / f"{polymer_name}.top"
    )

describe_file(
    top_path,
    (
        "Main GROMACS system topology, including force-field "
        "includes and the list of molecules in the system."
    ),
)

print(
"""
The TOP file is the main topology read by GROMACS.

It may contain the complete topology directly, or it may include one or
more ITP files.

It normally contains sections such as:

    defaults

    atomtypes

    moleculetype

    system

    molecules

The final [ molecules ] section tells GROMACS how many copies of each
molecule are present.
"""
)


# %% ==========================================================================
# Explain and inspect the ITP file
# ==============================================================================

itp_path = gromacs_files.get(
    "itp"
)

if itp_path is None:

    itp_path = (
        Path(gromacs_directory)
        / f"{polymer_name}.itp"
    )

describe_file(
    itp_path,
    (
        "Reusable molecule-level topology containing atoms "
        "and bonded interactions for the polymer."
    ),
)

print(
"""
The ITP file usually describes one molecular species.

For a single polymer chain, it may contain:

    atom definitions

    bonds

    pairs

    angles

    dihedrals

The TOP file can then include this ITP and state how many copies of that
polymer are present.

This separation becomes especially useful later when constructing systems
containing many copies of the same polymer.
"""
)


# %% ==========================================================================
# GROMACS file completeness check
# ==============================================================================

print("\n")
print("=" * 80)
print("GROMACS COMPLETENESS CHECK")
print("=" * 80)

required_gromacs_files = {
    "GRO": gro_path,
    "TOP": top_path,
    "ITP": itp_path,
}

gromacs_files_complete = True

for file_label, file_path in required_gromacs_files.items():

    file_path = Path(file_path)

    if file_path.exists() and file_path.stat().st_size > 0:

        print(
            f"✓ {file_label:<8} "
            f"{file_path.name}"
        )

    else:

        gromacs_files_complete = False

        print(
            f"✗ {file_label:<8} "
            f"{file_path.name}"
        )

print()

if gromacs_files_complete:

    print(
        "All expected GROMACS files were found and are non-empty."
    )

else:

    print(
"""
The GROMACS representation is incomplete.

This does not necessarily mean the Amber build failed.

It may mean that:

    ACPYPE was not run

    conversion was disabled

    output files use different names

    the converted files are stored in another directory
"""
    )


# %% ==========================================================================
# Inspect the PDB atom and residue records
# ==============================================================================

print("\n")
print("=" * 80)
print("PDB ATOM AND RESIDUE INSPECTION")
print("=" * 80)

pdb_atom_count = None
pdb_residue_count = None

if not Path(pdb_path).exists():

    print(
        "The PDB file is unavailable."
    )

else:

    pdb_lines = Path(pdb_path).read_text(
        encoding="utf-8",
        errors="replace",
    ).splitlines()

    coordinate_records = [
        line
        for line in pdb_lines
        if line.startswith(
            ("ATOM", "HETATM")
        )
    ]

    pdb_atom_count = len(
        coordinate_records
    )

    residue_identifiers = {
        (
            line[21:22],
            line[22:26].strip(),
            line[17:20].strip(),
        )
        for line in coordinate_records
        if len(line) >= 26
    }

    pdb_residue_count = len(
        residue_identifiers
    )

    print(
        f"Coordinate records: "
        f"{pdb_atom_count}"
    )

    print(
        f"Unique residues:     "
        f"{pdb_residue_count}"
    )

    print(
        f"Expected residues:   "
        f"{polymer_length}"
    )

    if pdb_residue_count == polymer_length:

        print(
            "\n✓ The PDB residue count matches the requested chain length."
        )

    else:

        print(
"""
The PDB residue count does not match the requested chain length.

This may indicate:

    residue numbering was repeated

    chain identifiers were reused

    the PDB includes additional residues

    the structure was written using a different residue convention
"""
        )


# %% ==========================================================================
# Display the residue sequence found in the PDB
# ==============================================================================

print("\n")
print("=" * 80)
print("RESIDUE SEQUENCE FOUND IN THE PDB")
print("=" * 80)

if not Path(pdb_path).exists():

    print(
        "The PDB file is unavailable."
    )

else:

    residue_order = []

    seen_residues = set()

    for line in coordinate_records:

        if len(line) < 26:

            continue

        residue_name = line[17:20].strip()
        chain_id = line[21:22]
        residue_number = line[22:26].strip()

        residue_key = (
            chain_id,
            residue_number,
            residue_name,
        )

        if residue_key not in seen_residues:

            seen_residues.add(
                residue_key
            )

            residue_order.append(
                residue_key
            )

    for index, residue_data in enumerate(
        residue_order,
        start=1,
    ):

        chain_id, residue_number, residue_name = (
            residue_data
        )

        displayed_chain = (
            chain_id
            if chain_id.strip()
            else "-"
        )

        print(
            f"{index:3d}  "
            f"Residue name: {residue_name:<4}  "
            f"Residue number: {residue_number:<5}  "
            f"Chain: {displayed_chain}"
        )


# %% ==========================================================================
# Inspect the GRO atom count
# ==============================================================================

print("\n")
print("=" * 80)
print("GRO ATOM COUNT")
print("=" * 80)

gro_atom_count = None

if not Path(gro_path).exists():

    print(
        "The GRO file is unavailable."
    )

else:

    gro_lines = Path(gro_path).read_text(
        encoding="utf-8",
        errors="replace",
    ).splitlines()

    if len(gro_lines) < 2:

        print(
            "The GRO file is too short to contain a valid atom count."
        )

    else:

        try:

            gro_atom_count = int(
                gro_lines[1].strip()
            )

        except ValueError:

            print(
                "The second GRO line could not be interpreted as an atom count."
            )

        else:

            print(
                f"GRO atom count: "
                f"{gro_atom_count}"
            )

            if pdb_atom_count is not None:

                print(
                    f"PDB atom count: "
                    f"{pdb_atom_count}"
                )

                if gro_atom_count == pdb_atom_count:

                    print(
                        "\n✓ PDB and GRO atom counts agree."
                    )

                else:

                    print(
"""
The PDB and GRO atom counts differ.

This should be investigated before simulation.

Possible causes include:

    hydrogen atoms were added or removed

    conversion changed the structure

    the files belong to different builds

    one file is incomplete
"""
                    )


# %% ==========================================================================
# Load the Amber topology using OpenMM
# ==============================================================================

print("\n")
print("=" * 80)
print("LOADING THE AMBER TOPOLOGY")
print("=" * 80)

openmm_prmtop_atom_count = None
openmm_coordinate_count = None

if (
    not Path(prmtop_path).exists()
    or not Path(rst7_path).exists()
):

    print(
        "The PRMTOP and RST7 files are both required for this test."
    )

else:

    try:

        from openmm.app import (
            AmberPrmtopFile,
            AmberInpcrdFile,
        )

    except ImportError:

        print(
"""
OpenMM is not available in the current Python environment.

The files can still exist and be valid, but this particular loading test
cannot be performed.
"""
        )

    else:

        try:

            loaded_prmtop = AmberPrmtopFile(
                str(prmtop_path)
            )

            loaded_coordinates = AmberInpcrdFile(
                str(rst7_path)
            )

        except Exception as error:

            print(
                "OpenMM could not load the Amber files."
            )

            print(
                f"\nError:\n{error}"
            )

        else:

            openmm_prmtop_atom_count = sum(
                1
                for _ in loaded_prmtop.topology.atoms()
            )

            openmm_coordinate_count = len(
                loaded_coordinates.positions
            )

            print(
                "✓ PRMTOP loaded successfully."
            )

            print(
                "✓ RST7 loaded successfully."
            )

            print(
                f"\nPRMTOP atoms:     "
                f"{openmm_prmtop_atom_count}"
            )

            print(
                f"RST7 coordinates: "
                f"{openmm_coordinate_count}"
            )

            if (
                openmm_prmtop_atom_count
                == openmm_coordinate_count
            ):

                print(
                    "\n✓ Amber topology and coordinate counts agree."
                )

            else:

                print(
"""
The PRMTOP and RST7 atom counts do not agree.

The two files must not be used together until this mismatch has been
resolved.
"""
                )


# %% ==========================================================================
# Compare every available atom count
# ==============================================================================

print("\n")
print("=" * 80)
print("ATOM-COUNT COMPARISON")
print("=" * 80)

atom_count_sources = {
    "PDB": pdb_atom_count,
    "GRO": gro_atom_count,
    "PRMTOP via OpenMM": openmm_prmtop_atom_count,
    "RST7 via OpenMM": openmm_coordinate_count,
}

available_atom_counts = {
    source: count
    for source, count in atom_count_sources.items()
    if count is not None
}

for source, count in atom_count_sources.items():

    displayed_count = (
        count
        if count is not None
        else "Unavailable"
    )

    print(
        f"{source:<20} "
        f"{displayed_count}"
    )

if len(available_atom_counts) >= 2:

    unique_atom_counts = set(
        available_atom_counts.values()
    )

    if len(unique_atom_counts) == 1:

        print(
            "\n✓ All available atom counts agree."
        )

    else:

        print(
            "\n✗ The available atom counts do not all agree."
        )

        print(
            "\nThis mismatch should be investigated before simulation."
        )


# %% ==========================================================================
# Check whether the GROMACS topology includes the ITP
# ==============================================================================

print("\n")
print("=" * 80)
print("GROMACS TOPOLOGY INCLUDE CHECK")
print("=" * 80)

if not Path(top_path).exists():

    print(
        "The TOP file is unavailable."
    )

else:

    top_text = Path(top_path).read_text(
        encoding="utf-8",
        errors="replace",
    )

    itp_filename = Path(
        itp_path
    ).name

    if itp_filename in top_text:

        print(
            f"✓ The TOP file references {itp_filename}."
        )

    else:

        print(
            f"The TOP file does not explicitly reference {itp_filename}."
        )

        print(
"""
This is not automatically an error.

Some conversion workflows place the complete molecular topology directly
inside the TOP file rather than including a separate ITP.
"""
        )


# %% ==========================================================================
# Inspect the [ molecules ] section of the TOP file
# ==============================================================================

print("\n")
print("=" * 80)
print("GROMACS [ MOLECULES ] SECTION")
print("=" * 80)

if not Path(top_path).exists():

    print(
        "The TOP file is unavailable."
    )

else:

    top_lines = Path(top_path).read_text(
        encoding="utf-8",
        errors="replace",
    ).splitlines()

    molecules_section = []

    in_molecules_section = False

    for line in top_lines:

        stripped_line = line.strip()

        if stripped_line.lower() == "[ molecules ]":

            in_molecules_section = True
            continue

        if (
            in_molecules_section
            and stripped_line.startswith("[")
        ):

            break

        if in_molecules_section:

            if (
                stripped_line
                and not stripped_line.startswith(";")
            ):

                molecules_section.append(
                    stripped_line
                )

    if molecules_section:

        print(
            "The following molecule entries were found:"
        )

        for line in molecules_section:

            print(
                f"  {line}"
            )

    else:

        print(
            "No populated [ molecules ] section was found."
        )


# %% ==========================================================================
# Inspect the TLEaP build directory
# ==============================================================================

print("\n")
print("=" * 80)
print("TLEAP BUILD FILES")
print("=" * 80)

print(
"""
The leap directory is valuable when debugging a failed build.

It may contain:

    the generated TLEaP input script

    TLEaP output logs

    temporary structures

    intermediate files

These files explain how the final Amber topology was produced.
"""
)

if not Path(leap_directory).exists():

    print(
        "The TLEaP directory does not exist."
    )

else:

    leap_contents = sorted(
        path
        for path in Path(leap_directory).iterdir()
        if path.is_file()
    )

    if not leap_contents:

        print(
            "The TLEaP directory exists but contains no files."
        )

    else:

        for file_path in leap_contents:

            size_bytes = file_path.stat().st_size

            print(
                f"{file_path.name:<35} "
                f"{size_bytes:>10,} bytes"
            )


# %% ==========================================================================
# Final validation summary for Part 2A
# ==============================================================================

print("\n")
print("=" * 80)
print("PART 2A VALIDATION SUMMARY")
print("=" * 80)

validation_checks = {
    "Amber files complete": (
        amber_files_complete
    ),
    "GROMACS files complete": (
        gromacs_files_complete
    ),
    "PDB residue count matches length": (
        pdb_residue_count == polymer_length
        if pdb_residue_count is not None
        else False
    ),
    "PDB and GRO atom counts agree": (
        pdb_atom_count == gro_atom_count
        if (
            pdb_atom_count is not None
            and gro_atom_count is not None
        )
        else False
    ),
    "PRMTOP and RST7 counts agree": (
        openmm_prmtop_atom_count
        == openmm_coordinate_count
        if (
            openmm_prmtop_atom_count is not None
            and openmm_coordinate_count is not None
        )
        else False
    ),
}

for check_name, check_result in validation_checks.items():

    symbol = (
        "✓"
        if check_result
        else "✗"
    )

    print(
        f"{symbol} {check_name}"
    )

print(
"""
A successful polymer build should ideally satisfy all of these checks.

However, an unavailable optional check does not always mean the build failed.

For example:

    OpenMM may not be installed in the active environment

    GROMACS conversion may not have been requested

    a helper method may use a different filename convention

The most important requirement is that each file set is internally
consistent.

At this stage we have:

    inspected the Amber files

    inspected the GROMACS files

    checked file sizes

    counted atoms

    counted residues

    loaded the Amber topology and coordinates

    compared the available atom counts

Part 2B will finish the tutorial by:

    visualising the polymer

    building several chain lengths

    comparing the resulting polymers

    showing the final directory tree

    summarising the complete workflow
"""
)
    
# %% ==========================================================================
# Part 2B - Visualisation, multiple chain lengths, and final summary
# ==============================================================================

print("\n")
print("=" * 80)
print("PART 2B - VISUALISATION AND EXTENDED BUILDING")
print("=" * 80)

print(
"""
In Part 2A we inspected the files created by the polymer build.

We confirmed that the Amber and GROMACS representations were present,
counted atoms and residues, and checked that the topology and coordinate
files were internally consistent.

Part 2B now completes the tutorial by:

    visualising the polymer

    summarising the completed build

    comparing different chain lengths

    optionally building several polymers

    inspecting the built-polymer database

    reviewing the entire workflow
"""
)


# %% ==========================================================================
# User settings for Part 2B
# ==============================================================================

"""
These settings control the optional demonstrations in this section.

RUN_VISUALISATION
    Attempts to display the polymer using py3Dmol.

RUN_ADDITIONAL_BUILDS
    Builds the polymers listed in additional_lengths.

OVERWRITE_EXISTING_BUILDS
    This tutorial does not force deletion or overwriting itself.

    The value is only used to decide whether the tutorial should attempt
    to call the builder for polymers whose output directory already exists.

    The builder's own behaviour remains the final source of truth.
"""

RUN_VISUALISATION = True

RUN_ADDITIONAL_BUILDS = False

OVERWRITE_EXISTING_BUILDS = False

additional_lengths = [
    5,
    20,
    50,
]


# %% ==========================================================================
# Summarise the polymer that was built
# ==============================================================================

print("\n")
print("=" * 80)
print("POLYMER BUILD SUMMARY")
print("=" * 80)

summary_atom_count = None

for possible_count in [
    openmm_prmtop_atom_count,
    openmm_coordinate_count,
    pdb_atom_count,
    gro_atom_count,
]:

    if possible_count is not None:

        summary_atom_count = possible_count
        break


print(f"\nPolymer name:       {polymer_name}")
print(f"PHA chemistry:      {PHA_type}")
print(f"Repeat units:       {polymer_length}")
print(f"Head residues:      1")
print(
    f"Mainchain residues: "
    f"{max(polymer_length - 2, 0)}"
)
print(f"Tail residues:      1")

if summary_atom_count is None:

    print("Number of atoms:    Unavailable")

else:

    print(
        f"Number of atoms:    "
        f"{summary_atom_count}"
    )

print(
    f"Amber complete:     "
    f"{'Yes' if amber_files_complete else 'No'}"
)

print(
    f"GROMACS complete:   "
    f"{'Yes' if gromacs_files_complete else 'No'}"
)

print(f"Output directory:   {polymer_directory}")


# %% ==========================================================================
# Explain why visualisation matters
# ==============================================================================

print("\n")
print("=" * 80)
print("WHY VISUALISE THE POLYMER?")
print("=" * 80)

print(
"""
A successful topology build is not the end of structural validation.

Visual inspection can reveal problems that are difficult to detect from
filenames or atom counts alone.

For example:

    disconnected residues

    unexpected long bonds

    overlapping atoms

    incorrect residue ordering

    missing atoms

    distorted stereochemistry

    unusual terminal groups

A structure can therefore pass a simple file-existence check while still
containing a chemically unreasonable geometry.

Visualisation should be treated as an important validation step.
"""
)


# %% ==========================================================================
# Optional py3Dmol visualisation
# ==============================================================================

print("\n")
print("=" * 80)
print("INTERACTIVE 3D VISUALISATION")
print("=" * 80)

polymer_viewer = None

if not RUN_VISUALISATION:

    print(
        "Visualisation was skipped because "
        "RUN_VISUALISATION is False."
    )

elif not Path(pdb_path).exists():

    print(
        "The polymer cannot be visualised because "
        "the PDB file does not exist."
    )

else:

    try:

        import py3Dmol

    except ImportError:

        print(
"""
py3Dmol is not installed in the active Python environment.

The molecular build is unaffected.

To use this optional visualisation, install py3Dmol in the environment
used to run the tutorial.
"""
        )

    else:

        pdb_text = Path(pdb_path).read_text(
            encoding="utf-8",
            errors="replace",
        )

        polymer_viewer = py3Dmol.view(
            width=950,
            height=550,
        )

        polymer_viewer.addModel(
            pdb_text,
            "pdb",
        )

        polymer_viewer.setStyle(
            {
                "stick": {
                    "radius": 0.18,
                },
            }
        )

        polymer_viewer.setBackgroundColor(
            "white"
        )

        polymer_viewer.zoomTo()

        print(
            f"Displaying {polymer_name} from:"
        )

        print(
            f"  {pdb_path}"
        )

        polymer_viewer.show()


# %% ==========================================================================
# Alternative visualisation styles
# ==============================================================================

print("\n")
print("=" * 80)
print("ALTERNATIVE DISPLAY STYLES")
print("=" * 80)

print(
"""
py3Dmol supports several molecular display styles.

Stick

    Good for inspecting bonds and stereochemistry.

Sphere

    Useful for viewing the occupied molecular volume.

Line

    Lightweight and useful for very long chains.

Cartoon

    Mainly intended for biomolecular secondary structure and is generally
    less useful for a synthetic PHA chain.

Surface

    Useful for viewing the external molecular envelope.

The following examples are not run automatically.

They can be copied into a notebook cell after the PDB structure has been
loaded.
"""
)

print(
r'''
# Stick representation

viewer.setStyle(
    {
        "stick": {}
    }
)


# Sphere representation

viewer.setStyle(
    {
        "sphere": {
            "scale": 0.3
        }
    }
)


# Combined stick and sphere representation

viewer.setStyle(
    {
        "stick": {
            "radius": 0.15
        },
        "sphere": {
            "scale": 0.22
        }
    }
)


# Line representation

viewer.setStyle(
    {
        "line": {}
    }
)


# Molecular surface

viewer.addSurface(
    py3Dmol.VDW,
    {
        "opacity": 0.75
    }
)
'''
)


# %% ==========================================================================
# Lightweight text preview of the first PDB atoms
# ==============================================================================

print("\n")
print("=" * 80)
print("TEXT PREVIEW OF THE PDB")
print("=" * 80)

if not Path(pdb_path).exists():

    print(
        "The PDB file is unavailable."
    )

else:

    pdb_coordinate_lines = [
        line
        for line in Path(pdb_path).read_text(
            encoding="utf-8",
            errors="replace",
        ).splitlines()
        if line.startswith(
            ("ATOM", "HETATM")
        )
    ]

    preview_count = min(
        10,
        len(pdb_coordinate_lines),
    )

    print(
        f"Showing the first {preview_count} "
        f"coordinate records:\n"
    )

    for line in pdb_coordinate_lines[
        :preview_count
    ]:

        print(line)

    print(
"""
Each coordinate record contains information such as:

    atom serial number

    atom name

    residue name

    residue number

    x, y, and z coordinates

    chemical element

This text representation is useful when checking naming conventions.
"""
    )


# %% ==========================================================================
# Compare several possible chain lengths
# ==============================================================================

print("\n")
print("=" * 80)
print("COMPARING POLYMER LENGTHS")
print("=" * 80)

comparison_lengths = sorted(
    set(
        [
            5,
            10,
            20,
            50,
            100,
        ]
    )
)

print(
"""
The same parameterised chemistry can be reused for many polymer lengths.

Only the number of internal mainchain residues changes.
"""
)

print(
    "\n"
    f"{'Polymer':<15}"
    f"{'Head':>8}"
    f"{'Main':>8}"
    f"{'Tail':>8}"
    f"{'Total':>10}"
)

print(
    "-" * 49
)

for comparison_length in comparison_lengths:

    comparison_name = (
        paths.get_built_PHA_name(
            PHA_type=PHA_type,
            length=comparison_length,
        )
    )

    comparison_main_count = max(
        comparison_length - 2,
        0,
    )

    print(
        f"{comparison_name:<15}"
        f"{1:>8}"
        f"{comparison_main_count:>8}"
        f"{1:>8}"
        f"{comparison_length:>10}"
    )


# %% ==========================================================================
# Show the sequence architecture for each chain length
# ==============================================================================

print("\n")
print("=" * 80)
print("CHAIN ARCHITECTURE COMPARISON")
print("=" * 80)

for comparison_length in comparison_lengths:

    comparison_name = (
        paths.get_built_PHA_name(
            PHA_type=PHA_type,
            length=comparison_length,
        )
    )

    comparison_main_count = max(
        comparison_length - 2,
        0,
    )

    if comparison_main_count:

        architecture = (
            f"HEAD → MAIN × "
            f"{comparison_main_count} → TAIL"
        )

    else:

        architecture = (
            "HEAD → TAIL"
        )

    print(
        f"\n{comparison_name}"
    )

    print(
        f"  {architecture}"
    )

print(
"""
All of these polymers use the same:

    head PREPIN

    mainchain PREPIN

    tail PREPIN

    FRCMOD

Parameterisation is performed once.

Polymer assembly is repeated for each requested chain length.
"""
)


# %% ==========================================================================
# Estimate how atom count changes with polymer length
# ==============================================================================

print("\n")
print("=" * 80)
print("APPROXIMATE ATOM-COUNT SCALING")
print("=" * 80)

print(
"""
For polymers built from the same chemistry, atom count usually increases
approximately linearly with chain length.

The exact relationship depends on the number of atoms in the head,
mainchain, and tail residues.

If at least two previously built polymer lengths are available, the scaling
can be measured directly.

This tutorial does not assume a fixed number of atoms per repeat unit,
because terminal residues may contain different atom counts.
"""
)


# %% ==========================================================================
# Find already-built polymers for this PHA type
# ==============================================================================

print("\n")
print("=" * 80)
print("EXISTING BUILT POLYMERS")
print("=" * 80)

built_PHA_root = Path(
    paths.get_built_PHAs_dir()
)

existing_polymer_records = []

if not built_PHA_root.exists():

    print(
        "The built_PHAs directory does not exist."
    )

else:

    for candidate_directory in sorted(
        built_PHA_root.iterdir()
    ):

        if not candidate_directory.is_dir():

            continue

        candidate_name = (
            candidate_directory.name
        )

        try:

            candidate_PHA_type, candidate_length = (
                paths.parse_built_PHA_name(
                    candidate_name
                )
            )

        except Exception:

            continue

        if candidate_PHA_type != PHA_type:

            continue

        existing_polymer_records.append(
            {
                "name": candidate_name,
                "length": candidate_length,
                "directory": candidate_directory,
            }
        )

    if not existing_polymer_records:

        print(
            f"No built polymers were found for "
            f"{PHA_type}."
        )

    else:

        print(
            f"Built polymers found for "
            f"{PHA_type}:"
        )

        for record in sorted(
            existing_polymer_records,
            key=lambda item: item["length"],
        ):

            print(
                f"\n{record['name']}"
            )

            print(
                f"  Length:    "
                f"{record['length']}"
            )

            print(
                f"  Directory: "
                f"{record['directory']}"
            )


# %% ==========================================================================
# Inspect atom counts for existing polymers
# ==============================================================================

print("\n")
print("=" * 80)
print("ATOM COUNTS FOR EXISTING POLYMERS")
print("=" * 80)

existing_atom_counts = []

if not existing_polymer_records:

    print(
        "No existing polymers are available for comparison."
    )

else:

    for record in sorted(
        existing_polymer_records,
        key=lambda item: item["length"],
    ):

        candidate_name = record["name"]
        candidate_length = record["length"]

        try:

            candidate_amber_files = (
                paths.get_built_PHA_amber_files(
                    candidate_name
                )
            )

        except TypeError:

            candidate_amber_files = (
                paths.get_built_PHA_amber_files(
                    PHA_type=PHA_type,
                    length=candidate_length,
                )
            )

        candidate_pdb = Path(
            candidate_amber_files.get(
                "pdb",
                (
                    record["directory"]
                    / "amber"
                    / f"{candidate_name}.pdb"
                ),
            )
        )

        candidate_atom_count = None

        if candidate_pdb.exists():

            candidate_atom_count = sum(
                1
                for line in candidate_pdb.read_text(
                    encoding="utf-8",
                    errors="replace",
                ).splitlines()
                if line.startswith(
                    ("ATOM", "HETATM")
                )
            )

        existing_atom_counts.append(
            {
                "name": candidate_name,
                "length": candidate_length,
                "atoms": candidate_atom_count,
            }
        )

    print(
        f"\n{'Polymer':<18}"
        f"{'Length':>10}"
        f"{'Atoms':>12}"
    )

    print(
        "-" * 40
    )

    for record in existing_atom_counts:

        displayed_atoms = (
            record["atoms"]
            if record["atoms"] is not None
            else "Unavailable"
        )

        print(
            f"{record['name']:<18}"
            f"{record['length']:>10}"
            f"{str(displayed_atoms):>12}"
        )


# %% ==========================================================================
# Calculate atom increments when possible
# ==============================================================================

print("\n")
print("=" * 80)
print("MEASURED ATOM INCREMENTS")
print("=" * 80)

usable_atom_records = [
    record
    for record in existing_atom_counts
    if record["atoms"] is not None
]

usable_atom_records = sorted(
    usable_atom_records,
    key=lambda item: item["length"],
)

if len(usable_atom_records) < 2:

    print(
"""
At least two existing polymer lengths with readable PDB files are needed
to calculate an atom increment.
"""
    )

else:

    for previous_record, current_record in zip(
        usable_atom_records,
        usable_atom_records[1:],
    ):

        repeat_unit_difference = (
            current_record["length"]
            - previous_record["length"]
        )

        atom_difference = (
            current_record["atoms"]
            - previous_record["atoms"]
        )

        atoms_per_added_repeat = (
            atom_difference
            / repeat_unit_difference
        )

        print(
            f"\n{previous_record['name']} "
            f"→ {current_record['name']}"
        )

        print(
            f"  Added repeat units: "
            f"{repeat_unit_difference}"
        )

        print(
            f"  Added atoms:        "
            f"{atom_difference}"
        )

        print(
            f"  Atoms per added "
            f"repeat unit: "
            f"{atoms_per_added_repeat:.2f}"
        )


# %% ==========================================================================
# Optional build of several polymer lengths
# ==============================================================================

print("\n")
print("=" * 80)
print("OPTIONAL MULTIPLE-LENGTH BUILD")
print("=" * 80)

print(
"""
This section demonstrates one of the central ideas of iPHAsimulator:

    parameterise once

    build many chain lengths

The polymers in additional_lengths will only be built when:

    RUN_ADDITIONAL_BUILDS = True
"""
)

if not RUN_ADDITIONAL_BUILDS:

    print(
        "Additional builds were skipped because "
        "RUN_ADDITIONAL_BUILDS is False."
    )

elif not ready:

    print(
        "Additional polymers cannot be built because "
        "the chemistry readiness check failed."
    )

else:

    requested_lengths = sorted(
        set(
            int(length)
            for length in additional_lengths
        )
    )

    for requested_length in requested_lengths:

        if requested_length < 2:

            print(
                f"\nSkipping length "
                f"{requested_length}: "
                f"length must be at least 2."
            )

            continue

        requested_name = (
            paths.get_built_PHA_name(
                PHA_type=PHA_type,
                length=requested_length,
            )
        )

        requested_directory = Path(
            paths.get_built_PHA_dir(
                PHA_type,
                requested_length,
            )
        )

        print(
            "\n" + "-" * 80
        )

        print(
            f"Requested polymer: "
            f"{requested_name}"
        )

        print(
            f"Output directory:  "
            f"{requested_directory}"
        )

        if (
            requested_directory.exists()
            and not OVERWRITE_EXISTING_BUILDS
        ):

            print(
"""
The output directory already exists.

The build was skipped because:

    OVERWRITE_EXISTING_BUILDS = False
"""
            )

            continue

        try:

            requested_result = (
                builder.build_PHA_polymer(
                    PHA_type=PHA_type,
                    length=requested_length,
                )
            )

        except Exception as error:

            print(
                f"✗ Build failed for "
                f"{requested_name}."
            )

            print(
                f"\nError:\n{error}"
            )

        else:

            print(
                f"✓ Build completed for "
                f"{requested_name}."
            )

            print(
                "\nReturned result:"
            )

            print(
                requested_result
            )


# %% ==========================================================================
# Validate the optional builds
# ==============================================================================

print("\n")
print("=" * 80)
print("OPTIONAL BUILD VALIDATION")
print("=" * 80)

for requested_length in sorted(
    set(additional_lengths)
):

    if requested_length < 2:

        continue

    requested_name = (
        paths.get_built_PHA_name(
            PHA_type=PHA_type,
            length=requested_length,
        )
    )

    try:

        requested_amber_files = (
            paths.get_built_PHA_amber_files(
                requested_name
            )
        )

    except TypeError:

        requested_amber_files = (
            paths.get_built_PHA_amber_files(
                PHA_type=PHA_type,
                length=requested_length,
            )
        )

    requested_required_files = {
        "PDB": Path(
            requested_amber_files.get(
                "pdb",
                (
                    paths.get_built_PHA_amber_dir(
                        PHA_type=PHA_type,
                        length=requested_length,
                    )
                    / f"{requested_name}.pdb"
                ),
            )
        ),
        "PRMTOP": Path(
            requested_amber_files.get(
                "prmtop",
                (
                    paths.get_built_PHA_amber_dir(
                        PHA_type=PHA_type,
                        length=requested_length,
                    )
                    / f"{requested_name}.prmtop"
                ),
            )
        ),
        "RST7": Path(
            requested_amber_files.get(
                "rst7",
                (
                    paths.get_built_PHA_amber_dir(
                        PHA_type=PHA_type,
                        length=requested_length,
                    )
                    / f"{requested_name}.rst7"
                ),
            )
        ),
    }

    requested_complete = all(
        file_path.exists()
        and file_path.stat().st_size > 0
        for file_path in requested_required_files.values()
    )

    symbol = (
        "✓"
        if requested_complete
        else "✗"
    )

    print(
        f"{symbol} {requested_name:<15} "
        f"Amber files complete: "
        f"{requested_complete}"
    )


# %% ==========================================================================
# Explain what does and does not change between builds
# ==============================================================================

print("\n")
print("=" * 80)
print("WHAT CHANGES BETWEEN POLYMER LENGTHS?")
print("=" * 80)

print(
"""
When the chain length changes, the following values change:

    polymer name

    number of residues

    number of atoms

    coordinate file size

    topology file size

    number of repeated mainchain residues

The following chemistry inputs do not change:

    monomer identity

    atom types

    partial-charge method

    head PREPIN

    mainchain PREPIN

    tail PREPIN

    FRCMOD

This separation is fundamental.

Parameterisation describes the chemistry.

Polymer construction describes the architecture.
"""
)


# %% ==========================================================================
# Show the final directory tree
# ==============================================================================

print("\n")
print("=" * 80)
print("EXPECTED FINAL DIRECTORY TREE")
print("=" * 80)

head_prepin_name = Path(
    parameter_files["head_prepin"]
).name

mainchain_prepin_name = Path(
    parameter_files["mainchain_prepin"]
).name

tail_prepin_name = Path(
    parameter_files["tail_prepin"]
).name

frcmod_name = Path(
    parameter_files["frcmod"]
).name

print(
f"""
structure_database/
│
├── residue_codes.csv
│
├── PHA_types/
│   │
│   └── {PHA_type}/
│       │
│       ├── input/
│       │   ├── head definition file
│       │   ├── mainchain definition file
│       │   └── tail definition file
│       │
│       ├── trimer/
│       │   └── {frcmod_name}
│       │
│       └── monomer_units/
│           ├── {head_prepin_name}
│           ├── {mainchain_prepin_name}
│           └── {tail_prepin_name}
│
└── built_PHAs/
    │
    └── {polymer_name}/
        │
        ├── leap/
        │   ├── generated TLEaP input
        │   ├── TLEaP output
        │   └── intermediate build files
        │
        ├── amber/
        │   ├── {Path(pdb_path).name}
        │   ├── {Path(prmtop_path).name}
        │   └── {Path(rst7_path).name}
        │
        └── gromacs/
            ├── {Path(gro_path).name}
            ├── {Path(top_path).name}
            └── {Path(itp_path).name}
"""
)


# %% ==========================================================================
# Display the complete workflow
# ==============================================================================

print("\n")
print("=" * 80)
print("COMPLETE POLYMER-BUILDING WORKFLOW")
print("=" * 80)

print(
"""
                    Monomer SMILES
                           │
                           ▼
                     Trimer SMILES
                           │
                           ▼
               Trimer parameterisation
                           │
                           ▼
              Charges and atom typing
                           │
                           ▼
          Head / mainchain / tail PREPINs
                           │
                           ▼
                 Chemistry is reusable
                           │
                           ▼
                Select a chain length
                           │
                           ▼
                build_PHA_polymer()
                           │
                           ▼
                 Generate TLEaP input
                           │
                           ▼
                    Execute TLEaP
                           │
                           ▼
                     Amber polymer
                           │
                  ┌────────┴────────┐
                  ▼                 ▼
                PDB          PRMTOP + RST7
                  │                 │
                  └────────┬────────┘
                           ▼
                    ACPYPE conversion
                           │
                           ▼
                GRO + TOP + ITP files
                           │
                           ▼
                  Polymer ready for
                  system preparation
"""
)


# %% ==========================================================================
# Connect this tutorial to the next stage
# ==============================================================================

print("\n")
print("=" * 80)
print("WHAT HAPPENS NEXT?")
print("=" * 80)

print(
"""
A single finite polymer chain is useful for:

    checking the chemistry

    validating atom names

    inspecting stereochemistry

    testing topology conversion

    studying isolated-chain behaviour

Many condensed-phase simulations require more than one chain.

For example, an amorphous polymer melt may contain:

    25 polymer chains

    50 polymer chains

    chains of different lengths

    a defined density

    a periodic simulation box

The next tutorial will take the finite polymer built here and use it as
the molecular building block for a multi-chain polymer melt.
"""
)


# %% ==========================================================================
# Final knowledge check
# ==============================================================================

print("\n")
print("=" * 80)
print("KNOWLEDGE CHECK")
print("=" * 80)

print(
"""
After completing this tutorial, you should be able to answer the following
questions.

1. Why are separate head, mainchain, and tail residues required?

2. How many mainchain residues are used in a polymer of length N?

3. Does building a new chain length require new force-field
   parameterisation?

4. What information is stored in a PRMTOP file?

5. Why must a PRMTOP and RST7 have matching atom counts?

6. What is the difference between a GROMACS TOP and ITP file?

7. Why is visual inspection still important after the files have been
   generated?

8. Which files are reused when building P3HB_5, P3HB_20, and P3HB_100?

Answers
-------

1. The terminal and internal repeat units have different connection
   environments.

2. N - 2.

3. No. The existing parameterised residues are reused.

4. Atoms, charges, atom types, bonded interactions, and force-field
   parameters.

5. Each coordinate must correspond to exactly one topology atom in the
   same order.

6. TOP is the main system topology, while ITP commonly stores a reusable
   molecule-level topology.

7. File checks cannot always reveal disconnected atoms, overlaps, or
   unreasonable geometry.

8. The same head PREPIN, mainchain PREPIN, tail PREPIN, and FRCMOD files.
"""
)


# %% ==========================================================================
# Tutorial 02 summary
# ==============================================================================

print("\n")
print("=" * 80)
print("TUTORIAL 02 SUMMARY")
print("=" * 80)

print(
f"""
In this tutorial we built and inspected:

    {polymer_name}

The polymer contains:

    1 head residue

    {max(polymer_length - 2, 0)} mainchain residues

    1 tail residue

    {polymer_length} repeat units in total

The most important lessons are:

1. PHA chemistry is parameterised before polymer construction.

2. The parameterisation is reused rather than repeated.

3. Finite chains require chemically distinct head, mainchain, and tail
   residues.

4. PHAPolymerBuilder coordinates the construction workflow.

5. TLEaP assembles the residues and generates the Amber representation.

6. Amber uses PDB, PRMTOP, and RST7 files for different purposes.

7. ACPYPE can convert the Amber polymer into GROMACS GRO, TOP, and ITP
   files.

8. Atom counts and residue counts should be checked before simulation.

9. Visual inspection is an important part of validation.

10. The same residue definitions can generate many polymer lengths.

Complete conceptual summary
---------------------------

    Parameterise one chemistry

                ↓

    Generate reusable residue definitions

                ↓

    Choose a polymer length

                ↓

    Assemble head + mainchain residues + tail

                ↓

    Produce Amber files

                ↓

    Produce GROMACS files

                ↓

    Use the polymer in larger MD systems

Next tutorial
-------------

Tutorial 03 will explain how to pack multiple finite polymer chains into
an amorphous polymer melt.
"""
)

print(
    "\nTutorial 02 complete."
)