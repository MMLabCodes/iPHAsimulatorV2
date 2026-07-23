#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
===============================================================================
Tutorial 04A - Building a Dry Single-Chain Molecular Dynamics System
Part 1 - Preparing the Polymer and Understanding the Simulation Box
===============================================================================

In Tutorial 02, we built a finite PHA polymer.

In Tutorial 03, we learned that a polymer is not yet a complete molecular
dynamics system. A physical environment and simulation boundaries must also
be defined.

In this tutorial, we will create the simplest MD system supported by
iPHAsimulator:

        One polymer chain

                +

        An empty periodic box

This is called a dry single-chain system.

"Dry" means that the system contains no explicit solvent and no ions. It does
not mean that the system lacks coordinates, topology information, simulation
boundaries, or periodic box vectors.

The complete preparation workflow is

        Built polymer

              │

              ▼

     Validate polymer files

              │

              ▼

      Define box padding

              │

              ▼

     Create periodic box

              │

              ▼

      Write system files

              │

              ▼

       Register system

By the end of Tutorial 04A, we will have created and validated a complete
single-chain system that can later be used to generate molecular dynamics
workflows.

This first part covers

    • what a dry single-chain system represents

    • why a simulation box is required

    • how box padding is defined

    • how to locate the previously built polymer

    • how to verify that the polymer is ready for system preparation

No system is created yet in Part 1. We first establish the inputs and make
sure that the source polymer is valid.

===============================================================================
"""


# %% ==========================================================================
# Imports
# ==============================================================================

from pathlib import Path
import sys


# %% ==========================================================================
# Locate the iPHAsimulator project
# ==============================================================================

# This tutorial is assumed to live inside a tutorials directory:
#
# iPHAsimulatorV2/
# ├── src/
# ├── structure_database/
# └── tutorials/
#     └── tutorial_04a_dry_single_chain.py
#
# Path(__file__).resolve().parents[1] therefore points to the project root.

PROJECT_ROOT = Path(__file__).resolve().parents[1]
STRUCTURE_DATABASE = PROJECT_ROOT / "structure_database"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# Import the central path manager used throughout iPHAsimulator.

from src.iphasimulator.pha_filepath_manager import PHAFileManager


# %% ==========================================================================
# Initialise the project
# ==============================================================================

paths = PHAFileManager(
    root_dir=STRUCTURE_DATABASE,
)

print("=" * 80)
print("Tutorial 04A - Building a Dry Single-Chain MD System")
print("Part 1 - Preparing the Polymer and Understanding the Simulation Box")
print("=" * 80)

print()
print(f"Project root:       {PROJECT_ROOT}")
print(f"Structure database: {STRUCTURE_DATABASE}")


# %% ==========================================================================
# Course progress
# ==============================================================================

print("\n")
print("=" * 80)
print("COURSE PROGRESS")
print("=" * 80)

print(
"""
Completed

✓ Tutorial 00

    Understanding the structure database

✓ Tutorial 01

    Registering and parameterising a PHA

✓ Tutorial 02

    Building a finite PHA polymer

✓ Tutorial 03

    Understanding molecular dynamics systems


Current tutorial

► Tutorial 04A

    Building a dry single-chain molecular dynamics system


Upcoming tutorials

□ Tutorial 04B

    Building a solvated single-chain system

□ Tutorial 04C

    Building a solvated single-chain system with ions

□ Tutorial 05

    Building a polymer melt
"""
)


# %% ==========================================================================
# What are we building?
# ==============================================================================

print("\n")
print("=" * 80)
print("WHAT ARE WE BUILDING?")
print("=" * 80)

print(
"""
We begin with a finite polymer created in Tutorial 02.

For example

        P3HB_10

The polymer already contains

    ✓ atomic coordinates

    ✓ atom types

    ✓ partial charges

    ✓ bonded parameters

    ✓ Amber topology

    ✓ GROMACS topology

We will place this polymer inside a periodic simulation box.

The resulting system contains

        One PHA polymer chain

                  +

        An otherwise empty box

It contains

    no water

    no salt

    no additional polymer chains

This is the smallest environment in which the finite polymer can be prepared
as a registered molecular dynamics system.
"""
)


# %% ==========================================================================
# What does "dry" mean?
# ==============================================================================

print("\n")
print("=" * 80)
print("WHAT DOES DRY MEAN?")
print("=" * 80)

print(
"""
A dry system contains no explicit solvent molecules.

For this tutorial

        Dry system

means

        one polymer

              +

        no water

              +

        no ions

              +

        no neighbouring polymer chains

The word "dry" describes the contents of the simulation box.

It does not mean that the polymer loses its topology or force-field
parameters.

The polymer chemistry remains exactly the same as it was at the end of
Tutorial 02.
"""
)


# %% ==========================================================================
# Why create a dry single-chain system?
# ==============================================================================

print("\n")
print("=" * 80)
print("WHY CREATE A DRY SINGLE-CHAIN SYSTEM?")
print("=" * 80)

print(
"""
A dry single-chain system isolates the behaviour of one polymer from solvent
and neighbouring chains.

It can therefore be useful for investigating

    • intrinsic chain flexibility

    • conformational changes

    • chain folding

    • backbone motion

    • radius of gyration

    • end-to-end distance

    • intramolecular interactions

    • conformational sampling

Because the system contains relatively few atoms, it is also inexpensive
compared with solvated systems and polymer melts.

However, it does not represent bulk polymer behaviour or an aqueous
environment.

The scientific interpretation must therefore match the system that has been
constructed.
"""
)


# %% ==========================================================================
# From a built polymer to a prepared system
# ==============================================================================

print("\n")
print("=" * 80)
print("FROM A BUILT POLYMER TO A PREPARED SYSTEM")
print("=" * 80)

print(
"""
The built polymer and the dry MD system are related, but they are not the
same object.

Built polymer

    Describes the finite molecule.

Dry MD system

    Describes the finite molecule inside a defined simulation environment.

The transformation can be represented as

        Built polymer

              │

              ▼

     Read coordinates

              │

              ▼

   Determine molecular size

              │

              ▼

      Add box padding

              │

              ▼

   Define periodic box vectors

              │

              ▼

    Write prepared system

The force field is reused.

The polymer is not parameterised again.
"""
)


# %% ==========================================================================
# Why is a simulation box required?
# ==============================================================================

print("\n")
print("=" * 80)
print("WHY IS A SIMULATION BOX REQUIRED?")
print("=" * 80)

print(
"""
Molecular dynamics requires a defined region of space.

The simulation box provides that region.

A simple representation is

        +----------------------------------+
        |                                  |
        |                                  |
        |          polymer chain           |
        |                                  |
        |                                  |
        +----------------------------------+

The box defines

    • the dimensions of the simulated region

    • the periodic boundary vectors

    • the volume associated with the system

    • the distance between the polymer and its periodic images

Even though the box contains no solvent, its dimensions still affect the
physical and numerical behaviour of the simulation.
"""
)


# %% ==========================================================================
# Periodic boundary conditions
# ==============================================================================

print("\n")
print("=" * 80)
print("PERIODIC BOUNDARY CONDITIONS")
print("=" * 80)

print(
"""
Under periodic boundary conditions, the simulation box is treated as though
identical copies surround it in every direction.

A two-dimensional illustration looks like this.

    +-------------+-------------+-------------+
    |             |             |             |
    |   image     |   image     |   image     |
    |             |             |             |
    +-------------+-------------+-------------+
    |             |             |             |
    |   image     | simulated   |   image     |
    |             |    box      |             |
    +-------------+-------------+-------------+
    |             |             |             |
    |   image     |   image     |   image     |
    |             |             |             |
    +-------------+-------------+-------------+

Only the central box is explicitly simulated.

The surrounding boxes are periodic images.

This means that a polymer near one side of the box may interact with its
periodic image on the opposite side if the box is too small.
"""
)


# %% ==========================================================================
# Box padding
# ==============================================================================

print("\n")
print("=" * 80)
print("BOX PADDING")
print("=" * 80)

print(
"""
Box padding is the minimum empty distance placed between the polymer and the
edge of the simulation box.

Conceptually

    box edge

        │<------ padding ------>│

        +-----------------------+
        |                       |
        |       polymer         |
        |                       |
        +-----------------------+

Padding is normally added around the polymer in all three dimensions.

If the polymer occupies coordinate ranges

    x_min to x_max

    y_min to y_max

    z_min to z_max

then an orthorhombic box can be estimated using

    Lx = (x_max - x_min) + 2p

    Ly = (y_max - y_min) + 2p

    Lz = (z_max - z_min) + 2p

where

    Lx, Ly and Lz

are the box lengths and

    p

is the chosen padding distance.

The factor of two appears because padding is added to both sides of each
dimension.
"""
)


# %% ==========================================================================
# Why padding matters
# ==============================================================================

print("\n")
print("=" * 80)
print("WHY DOES PADDING MATTER?")
print("=" * 80)

print(
"""
The padding controls the separation between the polymer and its periodic
images.

Too little padding can allow the chain to interact strongly with copies of
itself.

Excessive padding creates a larger box than necessary.

For a dry system, increasing the box size does not add solvent atoms.
However, the choice of box dimensions can still affect

    • periodic image separation

    • nonbonded interactions

    • computational setup

    • later simulation settings

The chosen padding should therefore be recorded as part of the system
preparation procedure.
"""
)


# %% ==========================================================================
# User settings
# ==============================================================================

print("\n")
print("=" * 80)
print("USER SETTINGS")
print("=" * 80)

# Name of the finite polymer created in Tutorial 02.
POLYMER_NAME = "P3HB_10"

# Minimum distance between the polymer and each side of the box.
#
# The exact unit expected by the system-building API must remain consistent
# with the implementation. In many molecular dynamics workflows, box padding
# is supplied in nanometres.
BOX_PADDING = 2.0

# When False, an existing prepared system should not be silently replaced.
OVERWRITE = False

# The actual construction call will be introduced in Part 2.
RUN_SYSTEM_PREPARATION = False

print(f"Polymer name:          {POLYMER_NAME}")
print(f"Requested box padding: {BOX_PADDING}")
print(f"Overwrite outputs:     {OVERWRITE}")
print(f"Run preparation:       {RUN_SYSTEM_PREPARATION}")


# %% ==========================================================================
# Interpreting the settings
# ==============================================================================

print("\n")
print("=" * 80)
print("INTERPRETING THE SETTINGS")
print("=" * 80)

print(
f"""
POLYMER_NAME

    {POLYMER_NAME}

identifies the finite polymer that will be placed inside the box.

The polymer must already have been built successfully.


BOX_PADDING

    {BOX_PADDING}

controls the minimum space added around the polymer.

The system builder uses the polymer coordinates together with this value to
determine the box dimensions.


OVERWRITE

    {OVERWRITE}

controls whether an existing system may be replaced.

Keeping this disabled by default protects previously prepared systems.


RUN_SYSTEM_PREPARATION

    {RUN_SYSTEM_PREPARATION}

is a tutorial safety switch.

The first part of the tutorial can be executed to inspect and validate the
inputs without creating or replacing any molecular files.
"""
)


# %% ==========================================================================
# Locate the built polymer directory
# ==============================================================================

print("\n")
print("=" * 80)
print("LOCATING THE BUILT POLYMER")
print("=" * 80)

# The standard location used by the structure database is
#
# structure_database/
# └── built_PHAs/
#     └── P3HB_10/
#
# We first attempt to obtain the directory through PHAFileManager. The
# fallback keeps this tutorial readable if the public method name differs
# between versions of the package.

try:
    polymer_dir = paths.get_built_polymer_dir(
        polymer_name=POLYMER_NAME,
    )
except (AttributeError, TypeError):
    polymer_dir = (
        STRUCTURE_DATABASE
        / "built_PHAs"
        / POLYMER_NAME
    )

polymer_dir = Path(polymer_dir)

print(f"Polymer directory:\n{polymer_dir}")

if polymer_dir.exists():
    print("\n✓ Built polymer directory found.")
else:
    print("\n✗ Built polymer directory was not found.")


# %% ==========================================================================
# Locate the Amber and GROMACS directories
# ==============================================================================

print("\n")
print("=" * 80)
print("LOCATING THE MOLECULAR FILES")
print("=" * 80)

amber_dir = polymer_dir / "amber"
gromacs_dir = polymer_dir / "gromacs"

# Some existing builds may store GROMACS files directly inside the polymer
# directory rather than in a dedicated gromacs subdirectory. We detect both
# layouts without altering either one.

if not gromacs_dir.exists():
    gromacs_dir = polymer_dir

print(f"Amber directory:   {amber_dir}")
print(f"GROMACS directory: {gromacs_dir}")

print()

print(
    "Amber directory exists:   "
    f"{amber_dir.exists()}"
)

print(
    "GROMACS directory exists: "
    f"{gromacs_dir.exists()}"
)


# %% ==========================================================================
# Search for the required polymer files
# ==============================================================================

print("\n")
print("=" * 80)
print("SEARCHING FOR POLYMER FILES")
print("=" * 80)


def find_first_file(directory: Path, patterns: tuple[str, ...]) -> Path | None:
    """
    Return the first file matching one of the supplied filename patterns.

    The patterns are checked in order so that the preferred naming convention
    is selected before broader fallback patterns.
    """

    if not directory.exists():
        return None

    for pattern in patterns:
        matches = sorted(directory.glob(pattern))

        if matches:
            return matches[0]

    return None


amber_topology_path = find_first_file(
    amber_dir,
    (
        f"{POLYMER_NAME}.prmtop",
        "*.prmtop",
    ),
)

amber_coordinates_path = find_first_file(
    amber_dir,
    (
        f"{POLYMER_NAME}.rst7",
        f"{POLYMER_NAME}.inpcrd",
        "*.rst7",
        "*.inpcrd",
    ),
)

amber_pdb_path = find_first_file(
    amber_dir,
    (
        f"{POLYMER_NAME}.pdb",
        "*.pdb",
    ),
)

gromacs_coordinates_path = find_first_file(
    gromacs_dir,
    (
        f"{POLYMER_NAME}.gro",
        "*.gro",
    ),
)

gromacs_topology_path = find_first_file(
    gromacs_dir,
    (
        f"{POLYMER_NAME}.top",
        "*.top",
    ),
)

gromacs_include_path = find_first_file(
    gromacs_dir,
    (
        f"{POLYMER_NAME}.itp",
        "*.itp",
    ),
)


# %% ==========================================================================
# Display the discovered files
# ==============================================================================

print("\n")
print("=" * 80)
print("DISCOVERED POLYMER FILES")
print("=" * 80)

polymer_files = {
    "Amber topology": amber_topology_path,
    "Amber coordinates": amber_coordinates_path,
    "Amber PDB": amber_pdb_path,
    "GROMACS coordinates": gromacs_coordinates_path,
    "GROMACS topology": gromacs_topology_path,
    "GROMACS include topology": gromacs_include_path,
}

for description, file_path in polymer_files.items():

    if file_path is None:
        status = "NOT FOUND"
    else:
        status = str(file_path)

    print(f"{description:<28}{status}")


# %% ==========================================================================
# Validate the source polymer
# ==============================================================================

print("\n")
print("=" * 80)
print("SOURCE POLYMER VALIDATION")
print("=" * 80)

# Amber requires a topology-coordinate pair.
amber_pair_complete = (
    amber_topology_path is not None
    and amber_coordinates_path is not None
)

# GROMACS requires a topology-coordinate pair. The .top file may reference an
# external .itp file or may contain the molecular definitions directly.
gromacs_pair_complete = (
    gromacs_coordinates_path is not None
    and gromacs_topology_path is not None
)

validation_checks = {
    "Built polymer directory exists": polymer_dir.exists(),
    "Amber directory exists": amber_dir.exists(),
    "Amber topology found": amber_topology_path is not None,
    "Amber coordinates found": amber_coordinates_path is not None,
    "Complete Amber file pair": amber_pair_complete,
    "GROMACS coordinates found": gromacs_coordinates_path is not None,
    "GROMACS topology found": gromacs_topology_path is not None,
    "Complete GROMACS file pair": gromacs_pair_complete,
}

for description, passed in validation_checks.items():
    symbol = "✓" if passed else "✗"
    print(f"{symbol} {description}")


# %% ==========================================================================
# Determine readiness
# ==============================================================================

print("\n")
print("=" * 80)
print("IS THE POLYMER READY?")
print("=" * 80)

# At least one complete topology-coordinate representation is required before
# system preparation can proceed.
polymer_ready = (
    polymer_dir.exists()
    and (
        amber_pair_complete
        or gromacs_pair_complete
    )
)

if polymer_ready:

    print(
f"""
✓ {POLYMER_NAME} is ready for dry-system preparation.

At least one complete topology-coordinate pair was found.

The next stage can

    read the polymer

    determine its spatial dimensions

    apply the requested padding

    create the simulation box

    write the prepared system

    register the result
"""
    )

else:

    print(
f"""
✗ {POLYMER_NAME} is not ready for dry-system preparation.

A complete topology-coordinate pair could not be identified.

Return to Tutorial 02 and confirm that the polymer build completed
successfully before continuing.
"""
    )


# %% ==========================================================================
# Behind the scenes - why validate before building?
# ==============================================================================

print("\n")
print("=" * 80)
print("BEHIND THE SCENES - INPUT VALIDATION")
print("=" * 80)

print(
"""
The dry-system builder should not begin by immediately writing new files.

It must first confirm that the source polymer is internally usable.

At a high level, the validation stage asks

        Does the polymer directory exist?

                      │

                      ▼

          Is a topology available?

                      │

                      ▼

        Are coordinates available?

                      │

                      ▼

       Do those files form a valid pair?

                      │

                      ▼

          Continue system preparation

This separation is important.

A failure discovered before writing outputs is much easier to diagnose than
a partially generated MD system containing incomplete or inconsistent files.
"""
)


# %% ==========================================================================
# Preview the preparation workflow
# ==============================================================================

print("\n")
print("=" * 80)
print("PREVIEW OF PART 2")
print("=" * 80)

print(
f"""
In Part 2, iPHAsimulator will use

    Polymer

        {POLYMER_NAME}

    Box padding

        {BOX_PADDING}

to construct the dry molecular dynamics system.

The high-level workflow will be

        Validate source polymer

                  │

                  ▼

          Read coordinates

                  │

                  ▼

     Measure the polymer bounds

                  │

                  ▼

      Add padding on every side

                  │

                  ▼

       Define periodic box vectors

                  │

                  ▼

       Write Amber and/or GROMACS files

                  │

                  ▼

         Register the new system

No solvent molecules will be added.

No ions will be added.

No force-field parameterisation will be repeated.
"""
)


# %% ==========================================================================
# Part 1 summary
# ==============================================================================

print("\n")
print("=" * 80)
print("PART 1 SUMMARY")
print("=" * 80)

print(
"""
In this section we established the inputs required to create a dry
single-chain molecular dynamics system.

We learned that

✓ A dry system contains one polymer and no explicit solvent or ions.

✓ The polymer chemistry is reused without being parameterised again.

✓ A simulation box defines the region of space and periodic boundaries.

✓ Box padding separates the polymer from its periodic images.

✓ The previously built topology and coordinates must be validated before
  system preparation begins.

The polymer is now ready to be transformed from a finite molecular structure
into a registered molecular dynamics system.

Part 2 will perform that construction and explain each high-level operation
carried out behind the scenes.
"""
)

print("\nTutorial 04A, Part 1 complete.")

# %% ==========================================================================
# Part 2 - Constructing the dry single-chain system
# ==============================================================================

print("\n")
print("=" * 80)
print("TUTORIAL 04A - PART 2")
print("CONSTRUCTING THE DRY SINGLE-CHAIN SYSTEM")
print("=" * 80)

print(
"""
In Part 1, we located and validated the finite polymer created in
Tutorial 02.

We confirmed that the polymer has

    • coordinates

    • topology information

    • force-field parameters

We also introduced the role of the simulation box and box padding.

In this section we will transform that finite polymer into a prepared dry
molecular dynamics system.

The high-level workflow is

        Validated polymer

                │

                ▼

        Read coordinates

                │

                ▼

      Determine molecular bounds

                │

                ▼

         Add box padding

                │

                ▼

      Define periodic box vectors

                │

                ▼

        Write system files

                │

                ▼

         Register the system
"""
)


# %% ==========================================================================
# Import the dry-system preparation class
# ==============================================================================

# Replace this import with the exact public class used by the current backend.
#
# The important design principle is that the tutorial should use the public
# iPHAsimulator API rather than directly copying files or constructing box
# vectors inside the tutorial itself.

try:

    from src.iphasimulator.md_system_builder import MDSystemBuilder

    MD_SYSTEM_BUILDER_AVAILABLE = True

except ImportError:

    MDSystemBuilder = None

    MD_SYSTEM_BUILDER_AVAILABLE = False


print(
    "MD system builder available: "
    f"{MD_SYSTEM_BUILDER_AVAILABLE}"
)


# %% ==========================================================================
# Confirm that Part 1 was completed
# ==============================================================================

print("\n")
print("=" * 80)
print("CONFIRMING THE INPUTS")
print("=" * 80)

required_part_1_variables = (
    "paths",
    "POLYMER_NAME",
    "BOX_PADDING",
    "OVERWRITE",
    "RUN_SYSTEM_PREPARATION",
    "polymer_dir",
    "polymer_ready",
)

missing_variables = [
    variable_name
    for variable_name in required_part_1_variables
    if variable_name not in globals()
]

if missing_variables:

    print("Part 1 variables are missing:")

    for variable_name in missing_variables:
        print(f"    {variable_name}")

    raise RuntimeError(
        "Run Tutorial 04A Part 1 before continuing with Part 2."
    )

print("✓ Part 1 variables are available.")

if not polymer_ready:

    raise RuntimeError(
        f"{POLYMER_NAME} did not pass the source-polymer validation."
    )

print(f"✓ {POLYMER_NAME} passed the source-polymer validation.")


# %% ==========================================================================
# Define the prepared-system name
# ==============================================================================

print("\n")
print("=" * 80)
print("DEFINING THE SYSTEM IDENTITY")
print("=" * 80)

# A prepared system should have a distinct name from the finite polymer.
#
# The polymer name describes the molecule:
#
#     P3HB_10
#
# The system name describes the molecule together with its environment:
#
#     P3HB_10_dry
#
# This distinction allows one polymer to be reused in several environments.

SYSTEM_NAME = f"{POLYMER_NAME}_dry"
SYSTEM_TYPE = "dry"

print(f"Polymer name: {POLYMER_NAME}")
print(f"System name:  {SYSTEM_NAME}")
print(f"System type:  {SYSTEM_TYPE}")


# %% ==========================================================================
# Locate the dry-system output directory
# ==============================================================================

print("\n")
print("=" * 80)
print("LOCATING THE OUTPUT DIRECTORY")
print("=" * 80)

# The exact path-manager method should be used when it exists.
#
# The fallback shown here represents the expected conceptual layout:
#
# structure_database/
# └── MD_systems/
#     └── dry/
#         └── P3HB_10_dry/

try:

    dry_system_dir = paths.get_dry_system_dir(
        system_name=SYSTEM_NAME,
        create=False,
    )

except (AttributeError, TypeError):

    dry_system_dir = (
        STRUCTURE_DATABASE
        / "MD_systems"
        / "dry"
        / SYSTEM_NAME
    )

dry_system_dir = Path(dry_system_dir)

print(f"Proposed output directory:\n{dry_system_dir}")

if dry_system_dir.exists():

    print("\nA directory already exists for this system.")

    if OVERWRITE:
        print("OVERWRITE is enabled.")
    else:
        print("OVERWRITE is disabled.")

else:

    print("\nNo existing output directory was found.")


# %% ==========================================================================
# Decide whether preparation may proceed
# ==============================================================================

print("\n")
print("=" * 80)
print("PREPARATION SAFETY CHECK")
print("=" * 80)

existing_output_blocks_run = (
    dry_system_dir.exists()
    and not OVERWRITE
)

if existing_output_blocks_run:

    print(
f"""
Preparation is currently blocked.

The output directory already exists:

    {dry_system_dir}

and

    OVERWRITE = {OVERWRITE}

This prevents an existing prepared system from being silently replaced.
"""
    )

else:

    print("✓ Output safety check passed.")


# %% ==========================================================================
# Initialise the MD system builder
# ==============================================================================

print("\n")
print("=" * 80)
print("INITIALISING THE SYSTEM BUILDER")
print("=" * 80)

system_builder = None

if MD_SYSTEM_BUILDER_AVAILABLE:

    try:

        system_builder = MDSystemBuilder(
            file_manager=paths,
        )

    except TypeError:

        try:

            system_builder = MDSystemBuilder(
                paths=paths,
            )

        except TypeError:

            system_builder = MDSystemBuilder()

    print("✓ MD system builder initialised.")

else:

    print(
"""
The example import did not match the installed backend.

Update the import near the beginning of Part 2 so that it points to the
public class responsible for preparing MD systems.

The construction logic should remain inside the backend rather than being
reimplemented inside this tutorial.
"""
    )


# %% ==========================================================================
# Preview the construction request
# ==============================================================================

print("\n")
print("=" * 80)
print("CONSTRUCTION REQUEST")
print("=" * 80)

construction_request = {
    "polymer_name": POLYMER_NAME,
    "system_name": SYSTEM_NAME,
    "system_type": SYSTEM_TYPE,
    "box_padding": BOX_PADDING,
    "overwrite": OVERWRITE,
}

for setting, value in construction_request.items():
    print(f"{setting:<20}{value}")


print(
"""

This request contains the information required to identify

    the source polymer

    the new prepared system

    the physical environment

    the box-padding rule

    the output-replacement policy
"""
)


# %% ==========================================================================
# Build the dry system
# ==============================================================================

print("\n")
print("=" * 80)
print("BUILDING THE DRY SYSTEM")
print("=" * 80)

dry_system_result = None

can_run_preparation = (
    RUN_SYSTEM_PREPARATION
    and polymer_ready
    and not existing_output_blocks_run
    and system_builder is not None
)

if can_run_preparation:

    print(
f"""
Preparing

    {SYSTEM_NAME}

from

    {POLYMER_NAME}
"""
    )

    # Adapt this single call to the exact public method exposed by the current
    # backend.
    #
    # A suitable API would look similar to:
    #
    #     system_builder.build_dry_single_chain_system(
    #         polymer_name=POLYMER_NAME,
    #         system_name=SYSTEM_NAME,
    #         box_padding=BOX_PADDING,
    #         overwrite=OVERWRITE,
    #     )
    #
    # The tutorial should not reproduce the internal preparation algorithm.

    dry_system_result = (
        system_builder.build_dry_single_chain_system(
            polymer_name=POLYMER_NAME,
            system_name=SYSTEM_NAME,
            box_padding=BOX_PADDING,
            overwrite=OVERWRITE,
        )
    )

    print("\n✓ Dry-system preparation completed.")

elif not RUN_SYSTEM_PREPARATION:

    print(
"""
System preparation was not run because

    RUN_SYSTEM_PREPARATION = False

This allows the tutorial to be inspected safely.

After confirming the settings and the backend method name, change the switch
to

    RUN_SYSTEM_PREPARATION = True
"""
    )

elif existing_output_blocks_run:

    print(
"""
System preparation was not run because an output directory already exists
and overwriting is disabled.
"""
    )

elif system_builder is None:

    print(
"""
System preparation was not run because the MD system builder could not be
initialised.
"""
    )


# %% ==========================================================================
# Behind the scenes - the complete preparation sequence
# ==============================================================================

print("\n")
print("=" * 80)
print("BEHIND THE SCENES - WHAT DID THE BUILDER DO?")
print("=" * 80)

print(
"""
The high-level function hides several coordinated operations.

It does not simply copy the original polymer files.

The preparation sequence is conceptually

1. Locate the source polymer

        The builder uses the polymer name to locate the validated topology
        and coordinate files created in Tutorial 02.

2. Read the molecular coordinates

        The Cartesian position of every atom is loaded.

3. Determine the molecular bounds

        The minimum and maximum coordinates are measured along x, y and z.

4. Apply box padding

        Empty space is added to both sides of every molecular dimension.

5. Define the periodic box

        Box vectors are written into the prepared coordinate representation.

6. Preserve the force field

        Atom types, charges and bonded parameters are reused directly from
        the source polymer.

7. Write the prepared system

        The topology-coordinate pair is written to the MD-system directory.

8. Register the system

        Metadata describing the prepared environment is added to the system
        registry.

The polymer chemistry is not recalculated during any of these stages.
"""
)


# %% ==========================================================================
# Understanding the molecular bounds
# ==============================================================================

print("\n")
print("=" * 80)
print("UNDERSTANDING THE MOLECULAR BOUNDS")
print("=" * 80)

print(
"""
Before a box can be created, the builder must know how much space the polymer
currently occupies.

Suppose the polymer coordinates span

    x_min to x_max

    y_min to y_max

    z_min to z_max

The molecular dimensions are

    molecular_x = x_max - x_min

    molecular_y = y_max - y_min

    molecular_z = z_max - z_min

If the requested padding is p, the box dimensions become

    box_x = molecular_x + 2p

    box_y = molecular_y + 2p

    box_z = molecular_z + 2p

Padding is added twice because each dimension has two sides.
"""
)


# %% ==========================================================================
# Optional coordinate inspection
# ==============================================================================

print("\n")
print("=" * 80)
print("OPTIONAL COORDINATE INSPECTION")
print("=" * 80)

# The following section independently illustrates how molecular bounds can be
# measured from the Amber coordinate file.
#
# It is for education and inspection only.
#
# The backend remains responsible for constructing the actual system.

try:

    from openmm.app import AmberInpcrdFile

    OPENMM_AVAILABLE = True

except ImportError:

    AmberInpcrdFile = None

    OPENMM_AVAILABLE = False


if (
    OPENMM_AVAILABLE
    and amber_coordinates_path is not None
):

    amber_coordinates = AmberInpcrdFile(
        str(amber_coordinates_path)
    )

    positions = amber_coordinates.positions

    # Convert OpenMM quantities to nanometres.
    from openmm import unit

    xyz_nm = [
        position.value_in_unit(unit.nanometer)
        for position in positions
    ]

    x_values = [position[0] for position in xyz_nm]
    y_values = [position[1] for position in xyz_nm]
    z_values = [position[2] for position in xyz_nm]

    bounds_nm = {
        "x_min": min(x_values),
        "x_max": max(x_values),
        "y_min": min(y_values),
        "y_max": max(y_values),
        "z_min": min(z_values),
        "z_max": max(z_values),
    }

    molecular_dimensions_nm = {
        "x": bounds_nm["x_max"] - bounds_nm["x_min"],
        "y": bounds_nm["y_max"] - bounds_nm["y_min"],
        "z": bounds_nm["z_max"] - bounds_nm["z_min"],
    }

    estimated_box_dimensions_nm = {
        dimension: molecular_size + (2 * BOX_PADDING)
        for dimension, molecular_size
        in molecular_dimensions_nm.items()
    }

    print("Coordinate bounds in nanometres")
    print("-" * 40)

    for name, value in bounds_nm.items():
        print(f"{name:<12}{value:>12.5f}")

    print()
    print("Molecular dimensions in nanometres")
    print("-" * 40)

    for dimension, value in molecular_dimensions_nm.items():
        print(f"{dimension:<12}{value:>12.5f}")

    print()
    print("Estimated padded box dimensions")
    print("-" * 40)

    for dimension, value in estimated_box_dimensions_nm.items():
        print(f"{dimension:<12}{value:>12.5f}")

else:

    print(
"""
Coordinate-bound inspection was skipped.

It requires

    • OpenMM

    • an Amber coordinate file

The backend may use Amber, GROMACS or another molecular representation to
determine the actual box dimensions.
"""
    )


# %% ==========================================================================
# Behind the scenes - coordinate translation
# ==============================================================================

print("\n")
print("=" * 80)
print("BEHIND THE SCENES - POSITIONING THE POLYMER")
print("=" * 80)

print(
"""
Defining box lengths is not always the final geometric step.

The builder may also translate the polymer so that it is positioned inside
the box with the requested padding.

Conceptually

Before translation

    +----------------------------------+
    | polymer                          |
    |                                  |
    |                                  |
    +----------------------------------+

After translation

    +----------------------------------+
    |                                  |
    |          polymer                 |
    |                                  |
    +----------------------------------+

Translation changes every atom by the same displacement vector.

For atom i

    r_i,new = r_i,old + d

where

    r_i

is the atomic position and

    d

is the translation vector.

Because every atom receives the same displacement, internal distances,
angles and molecular geometry remain unchanged.

Only the position of the whole polymer relative to the box changes.
"""
)


# %% ==========================================================================
# Box vectors
# ==============================================================================

print("\n")
print("=" * 80)
print("PERIODIC BOX VECTORS")
print("=" * 80)

print(
"""
An orthorhombic periodic box can be represented by three vectors.

    a = (Lx, 0,  0)

    b = (0,  Ly, 0)

    c = (0,  0,  Lz)

where

    Lx

    Ly

    Lz

are the lengths of the box along each Cartesian axis.

These vectors are stored with the prepared coordinate data so that the
simulation engine knows where the periodic boundaries occur.

The topology describes the molecular interactions.

The coordinates describe the atomic positions.

The box vectors describe the periodic simulation space.
"""
)


# %% ==========================================================================
# What is reused and what is added?
# ==============================================================================

print("\n")
print("=" * 80)
print("WHAT IS REUSED AND WHAT IS ADDED?")
print("=" * 80)

system_components = [
    ("Atom identities", "Reused from polymer"),
    ("Atom types", "Reused from polymer"),
    ("Partial charges", "Reused from polymer"),
    ("Bonded parameters", "Reused from polymer"),
    ("Initial coordinates", "Reused, possibly translated"),
    ("Simulation box", "Added during preparation"),
    ("Periodic box vectors", "Added during preparation"),
    ("Solvent", "Not added"),
    ("Ions", "Not added"),
    ("System registry entry", "Added during preparation"),
]

print(f"{'Component':<30}{'Treatment'}")
print("-" * 80)

for component, treatment in system_components:
    print(f"{component:<30}{treatment}")


# %% ==========================================================================
# Inspect the returned result
# ==============================================================================

print("\n")
print("=" * 80)
print("INSPECTING THE BUILDER RESULT")
print("=" * 80)

if dry_system_result is None:

    print(
"""
No result object is currently available because preparation was not run.

When the builder is executed, it should ideally return a structured result
containing the important generated paths and metadata.
"""
    )

else:

    print(f"Result type: {type(dry_system_result).__name__}")
    print()

    if hasattr(dry_system_result, "__dict__"):

        for field_name, value in vars(dry_system_result).items():
            print(f"{field_name:<30}{value}")

    else:

        print(dry_system_result)


# %% ==========================================================================
# Refresh the expected output directory
# ==============================================================================

print("\n")
print("=" * 80)
print("REFRESHING THE OUTPUT LOCATION")
print("=" * 80)

# A builder may return the output directory directly or as a field on a result
# object. Prefer that authoritative location when available.

result_directory_candidates = (
    "system_dir",
    "output_dir",
    "dry_system_dir",
    "directory",
)

if dry_system_result is not None:

    for attribute_name in result_directory_candidates:

        if hasattr(dry_system_result, attribute_name):

            candidate = getattr(
                dry_system_result,
                attribute_name,
            )

            if candidate is not None:

                dry_system_dir = Path(candidate)
                break


print(f"Dry-system directory:\n{dry_system_dir}")
print(f"\nDirectory exists: {dry_system_dir.exists()}")


# %% ==========================================================================
# Display the generated directory tree
# ==============================================================================

print("\n")
print("=" * 80)
print("GENERATED DIRECTORY TREE")
print("=" * 80)


def print_directory_tree(
    directory: Path,
    prefix: str = "",
) -> None:
    """
    Print a simple recursive directory tree.
    """

    if not directory.exists():
        print(f"{directory.name}/ [not found]")
        return

    entries = sorted(
        directory.iterdir(),
        key=lambda path: (
            path.is_file(),
            path.name.lower(),
        ),
    )

    print(f"{directory.name}/")

    for index, entry in enumerate(entries):

        is_last = index == len(entries) - 1

        connector = "└── " if is_last else "├── "

        print(
            f"{prefix}{connector}{entry.name}"
            f"{'/' if entry.is_dir() else ''}"
        )

        if entry.is_dir():

            child_prefix = (
                prefix
                + ("    " if is_last else "│   ")
            )

            print_directory_tree_contents(
                entry,
                child_prefix,
            )


def print_directory_tree_contents(
    directory: Path,
    prefix: str,
) -> None:
    """
    Print the contents of a directory beneath an existing tree branch.
    """

    entries = sorted(
        directory.iterdir(),
        key=lambda path: (
            path.is_file(),
            path.name.lower(),
        ),
    )

    for index, entry in enumerate(entries):

        is_last = index == len(entries) - 1

        connector = "└── " if is_last else "├── "

        print(
            f"{prefix}{connector}{entry.name}"
            f"{'/' if entry.is_dir() else ''}"
        )

        if entry.is_dir():

            child_prefix = (
                prefix
                + ("    " if is_last else "│   ")
            )

            print_directory_tree_contents(
                entry,
                child_prefix,
            )


if dry_system_dir.exists():

    print_directory_tree(dry_system_dir)

else:

    print(
"""
The generated tree is unavailable because the system directory does not yet
exist.
"""
    )


# %% ==========================================================================
# Search for generated molecular files
# ==============================================================================

print("\n")
print("=" * 80)
print("SEARCHING FOR GENERATED FILES")
print("=" * 80)

generated_files = []

if dry_system_dir.exists():

    generated_files = sorted(
        path
        for path in dry_system_dir.rglob("*")
        if path.is_file()
    )


if generated_files:

    for file_path in generated_files:

        relative_path = file_path.relative_to(
            dry_system_dir
        )

        size_bytes = file_path.stat().st_size

        print(
            f"{str(relative_path):<55}"
            f"{size_bytes:>12,} bytes"
        )

else:

    print("No generated files were found.")


# %% ==========================================================================
# Classify the generated files
# ==============================================================================

print("\n")
print("=" * 80)
print("CLASSIFYING THE GENERATED FILES")
print("=" * 80)

generated_by_suffix = {}

for file_path in generated_files:

    suffix = file_path.suffix.lower()

    generated_by_suffix.setdefault(
        suffix,
        [],
    ).append(file_path)


important_suffixes = {
    ".prmtop": "Amber topology",
    ".rst7": "Amber coordinates",
    ".inpcrd": "Amber coordinates",
    ".pdb": "Portable coordinate structure",
    ".gro": "GROMACS coordinates",
    ".top": "GROMACS topology",
    ".itp": "GROMACS include topology",
    ".csv": "Registry or metadata table",
    ".json": "Structured metadata",
}

for suffix, description in important_suffixes.items():

    matches = generated_by_suffix.get(
        suffix,
        [],
    )

    print(
        f"{description:<35}"
        f"{len(matches)}"
    )


# %% ==========================================================================
# Locate the prepared topology-coordinate pairs
# ==============================================================================

print("\n")
print("=" * 80)
print("LOCATING PREPARED TOPOLOGY-COORDINATE PAIRS")
print("=" * 80)


def first_generated_file(
    suffixes: tuple[str, ...],
) -> Path | None:
    """
    Return the first generated file matching one of the requested suffixes.
    """

    for suffix in suffixes:

        matching_files = generated_by_suffix.get(
            suffix,
            [],
        )

        if matching_files:
            return matching_files[0]

    return None


prepared_prmtop = first_generated_file(
    (".prmtop",)
)

prepared_rst7 = first_generated_file(
    (".rst7", ".inpcrd")
)

prepared_gro = first_generated_file(
    (".gro",)
)

prepared_top = first_generated_file(
    (".top",)
)


prepared_file_summary = {
    "Amber topology": prepared_prmtop,
    "Amber coordinates": prepared_rst7,
    "GROMACS coordinates": prepared_gro,
    "GROMACS topology": prepared_top,
}

for description, file_path in prepared_file_summary.items():

    value = (
        str(file_path)
        if file_path is not None
        else "NOT FOUND"
    )

    print(f"{description:<25}{value}")


# %% ==========================================================================
# Confirm that a prepared representation exists
# ==============================================================================

print("\n")
print("=" * 80)
print("PRELIMINARY OUTPUT CHECK")
print("=" * 80)

prepared_amber_pair = (
    prepared_prmtop is not None
    and prepared_rst7 is not None
)

prepared_gromacs_pair = (
    prepared_gro is not None
    and prepared_top is not None
)

preliminary_output_checks = {
    "Output directory exists": dry_system_dir.exists(),
    "Generated files found": bool(generated_files),
    "Complete Amber pair": prepared_amber_pair,
    "Complete GROMACS pair": prepared_gromacs_pair,
    "At least one complete representation": (
        prepared_amber_pair
        or prepared_gromacs_pair
    ),
}

for description, passed in preliminary_output_checks.items():

    symbol = "✓" if passed else "✗"

    print(f"{symbol} {description}")


# %% ==========================================================================
# Behind the scenes - writing multiple file formats
# ==============================================================================

print("\n")
print("=" * 80)
print("BEHIND THE SCENES - WHY WRITE MULTIPLE FORMATS?")
print("=" * 80)

print(
"""
Amber and GROMACS represent the same molecular system using different file
formats.

Amber commonly uses

    PRMTOP

        topology and force-field information

    RST7 or INPCRD

        coordinates and periodic box information

GROMACS commonly uses

    TOP and ITP

        topology and force-field information

    GRO

        coordinates and box dimensions

Writing both representations allows the prepared system to be inspected or
simulated using different molecular-dynamics tools.

The scientific system should remain equivalent across both formats.

Only the file representation changes.
"""
)


# %% ==========================================================================
# Locate the MD-system registry
# ==============================================================================

print("\n")
print("=" * 80)
print("LOCATING THE MD-SYSTEM REGISTRY")
print("=" * 80)

try:

    md_registry_path = paths.get_md_system_registry_path()

except AttributeError:

    md_registry_path = (
        STRUCTURE_DATABASE
        / "md_systems.csv"
    )

md_registry_path = Path(md_registry_path)

print(f"Registry path:\n{md_registry_path}")
print(f"\nRegistry exists: {md_registry_path.exists()}")


# %% ==========================================================================
# Inspect the registry entry
# ==============================================================================

print("\n")
print("=" * 80)
print("INSPECTING THE REGISTRY ENTRY")
print("=" * 80)

registered_rows = None

if md_registry_path.exists():

    import pandas as pd

    md_registry = pd.read_csv(
        md_registry_path
    )

    print(
        f"Number of registered systems: "
        f"{len(md_registry)}"
    )

    # Search across likely identifier columns. The exact schema can evolve, so
    # the tutorial first discovers which expected columns are present.

    possible_name_columns = (
        "system_name",
        "name",
        "system_id",
        "md_system_name",
    )

    matching_name_column = next(
        (
            column
            for column in possible_name_columns
            if column in md_registry.columns
        ),
        None,
    )

    if matching_name_column is not None:

        registered_rows = md_registry[
            md_registry[matching_name_column].astype(str)
            == SYSTEM_NAME
        ]

        if len(registered_rows) > 0:

            print(
                f"\n✓ Registry entry found for "
                f"{SYSTEM_NAME}."
            )

            print()
            print(registered_rows.to_string(index=False))

        else:

            print(
                f"\nNo registry entry was found for "
                f"{SYSTEM_NAME}."
            )

    else:

        print(
"""
The registry was found, but no recognised system-name column was identified.
"""
        )

        print("\nAvailable columns:")

        for column in md_registry.columns:
            print(f"    {column}")

else:

    print("The registry does not yet exist.")


# %% ==========================================================================
# Behind the scenes - system registration
# ==============================================================================

print("\n")
print("=" * 80)
print("BEHIND THE SCENES - SYSTEM REGISTRATION")
print("=" * 80)

print(
"""
The molecular files contain the information required by a simulation engine.

The registry serves a different purpose.

It records the identity and provenance of the prepared system.

A dry-system entry may describe

    • system name

    • source polymer

    • system type

    • chain count

    • box padding

    • coordinate path

    • topology path

    • creation location

The registry therefore connects

        scientific description

                │

                ▼

          molecular files

                │

                ▼

       later simulation workflows

This allows other parts of iPHAsimulator to select a system without relying
on filename guessing or manual folder navigation.
"""
)


# %% ==========================================================================
# Construction summary
# ==============================================================================

print("\n")
print("=" * 80)
print("CONSTRUCTION SUMMARY")
print("=" * 80)

construction_summary = {
    "Source polymer": POLYMER_NAME,
    "Prepared system": SYSTEM_NAME,
    "System type": SYSTEM_TYPE,
    "Box padding": BOX_PADDING,
    "Preparation requested": RUN_SYSTEM_PREPARATION,
    "Output directory exists": dry_system_dir.exists(),
    "Amber representation found": prepared_amber_pair,
    "GROMACS representation found": prepared_gromacs_pair,
    "Registry exists": md_registry_path.exists(),
}

for property_name, value in construction_summary.items():

    print(f"{property_name:<32}{value}")


# %% ==========================================================================
# What has been achieved?
# ==============================================================================

print("\n")
print("=" * 80)
print("WHAT HAS BEEN ACHIEVED?")
print("=" * 80)

print(
f"""
The finite polymer

    {POLYMER_NAME}

has now been associated with a dry molecular-dynamics environment.

The prepared system is

    {SYSTEM_NAME}

Its conceptual composition is

        one polymer chain

                +

        one periodic box

                +

          no solvent

                +

            no ions

The polymer force field was reused directly.

The major new information introduced during this stage is the periodic box.
"""
)


# %% ==========================================================================
# Preview of Part 3
# ==============================================================================

print("\n")
print("=" * 80)
print("PREVIEW OF PART 3")
print("=" * 80)

print(
"""
Creating files is not sufficient evidence that the system is correct.

In Part 3 we will validate the prepared dry system by checking

    • topology-coordinate compatibility

    • atom counts

    • residue counts

    • chain count

    • absence of solvent

    • absence of ions

    • periodic box vectors

    • consistency between Amber and GROMACS

    • registry information

This validation stage ensures that the system is not merely present on disk,
but is internally consistent and ready for later workflow generation.
"""
)


# %% ==========================================================================
# Part 2 summary
# ==============================================================================

print("\n")
print("=" * 80)
print("PART 2 SUMMARY")
print("=" * 80)

print(
"""
In this section we constructed the dry single-chain molecular dynamics
system.

We learned that the high-level preparation method

✓ locates the validated finite polymer

✓ reads its molecular coordinates

✓ measures the spatial extent of the chain

✓ applies padding around the polymer

✓ defines periodic box vectors

✓ preserves the existing force field

✓ writes the prepared molecular files

✓ registers the completed system

The polymer chemistry has not changed.

The system now differs from the finite polymer because it has a defined
periodic simulation environment.

Part 3 will perform detailed scientific and structural validation of the
generated system.
"""
)

print("\nTutorial 04A, Part 2 complete.")

# %% ==========================================================================
# Part 3 - Validating the Prepared Dry System
# ==============================================================================

print("\n")
print("=" * 80)
print("TUTORIAL 04A - PART 3")
print("VALIDATING THE PREPARED DRY SYSTEM")
print("=" * 80)

print(
"""
At the end of Part 2 we successfully prepared a dry single-chain molecular
dynamics system.

However, before running any molecular dynamics simulation, we should verify
that the generated system is internally consistent.

Validation is one of the most important stages of every molecular modelling
workflow.

Rather than assuming the generated files are correct, we will confirm that

    • the topology can be read

    • the coordinates can be read

    • the atom counts agree

    • the residue counts agree

    • only one polymer chain exists

    • no solvent molecules are present

    • no ions are present

    • periodic box vectors have been written

Only after these checks pass should the system be considered ready for
simulation.
"""
)


# %% ==========================================================================
# Load the prepared Amber system
# ==============================================================================

print("\n")
print("=" * 80)
print("LOADING THE AMBER SYSTEM")
print("=" * 80)

try:

    from openmm.app import AmberPrmtopFile
    from openmm.app import AmberInpcrdFile

    OPENMM_AVAILABLE = True

except ImportError:

    OPENMM_AVAILABLE = False

if (
    OPENMM_AVAILABLE
    and prepared_prmtop is not None
    and prepared_rst7 is not None
):

    prmtop = AmberPrmtopFile(
        str(prepared_prmtop)
    )

    inpcrd = AmberInpcrdFile(
        str(prepared_rst7)
    )

    topology = prmtop.topology

    print("✓ Amber files loaded successfully.")

else:

    topology = None

    print(
"""
Amber validation skipped.

Either

    OpenMM

or

    Amber topology files

were unavailable.
"""
    )


# %% ==========================================================================
# Count atoms
# ==============================================================================

print("\n")
print("=" * 80)
print("COUNTING ATOMS")
print("=" * 80)

if topology is not None:

    atom_count = sum(
        1 for atom in topology.atoms()
    )

    print(f"Total atoms : {atom_count}")

else:

    atom_count = None


# %% ==========================================================================
# Count residues
# ==============================================================================

print("\n")
print("=" * 80)
print("COUNTING RESIDUES")
print("=" * 80)

if topology is not None:

    residues = list(
        topology.residues()
    )

    residue_count = len(residues)

    print(f"Residues : {residue_count}")

else:

    residue_count = None


# %% ==========================================================================
# Count chains
# ==============================================================================

print("\n")
print("=" * 80)
print("COUNTING CHAINS")
print("=" * 80)

if topology is not None:

    chains = list(
        topology.chains()
    )

    chain_count = len(chains)

    print(f"Chains : {chain_count}")

else:

    chain_count = None


# %% ==========================================================================
# Inspect residue sequence
# ==============================================================================

print("\n")
print("=" * 80)
print("RESIDUE SEQUENCE")
print("=" * 80)

if topology is not None:

    residue_names = [
        residue.name
        for residue in residues
    ]

    print("Residues")

    print("-"*40)

    print(" ".join(residue_names))

else:

    print("Residues unavailable.")


# %% ==========================================================================
# Verify a single polymer exists
# ==============================================================================

print("\n")
print("=" * 80)
print("VERIFYING THE POLYMER")
print("=" * 80)

if chain_count == 1:

    print("✓ One polymer chain detected.")

else:

    print(
        f"Unexpected chain count: {chain_count}"
    )


# %% ==========================================================================
# Search for solvent
# ==============================================================================

print("\n")
print("=" * 80)
print("SEARCHING FOR SOLVENT")
print("=" * 80)

solvent_residue_names = {

    "WAT",
    "HOH",
    "SOL",
    "TIP3",
    "TIP3P",

}

water_found = False

if topology is not None:

    for residue in topology.residues():

        if residue.name.upper() in solvent_residue_names:

            water_found = True

            break

if water_found:

    print("Water molecules detected.")

else:

    print("✓ No solvent molecules detected.")


# %% ==========================================================================
# Search for ions
# ==============================================================================

print("\n")
print("=" * 80)
print("SEARCHING FOR IONS")
print("=" * 80)

ion_names = {

    "NA",
    "K",
    "CL",
    "CA",
    "MG",

}

ions_found = False

if topology is not None:

    for residue in topology.residues():

        if residue.name.upper() in ion_names:

            ions_found = True

            break

if ions_found:

    print("Ions detected.")

else:

    print("✓ No ions detected.")


# %% ==========================================================================
# Periodic box vectors
# ==============================================================================

print("\n")
print("=" * 80)
print("PERIODIC BOX")
print("=" * 80)

if (
    OPENMM_AVAILABLE
    and inpcrd is not None
):

    box = inpcrd.boxVectors

    if box is None:

        print("No periodic box vectors.")

    else:

        print("✓ Periodic box vectors found.")

        print()

        print(box)

else:

    print("Box vectors unavailable.")


# %% ==========================================================================
# Compare Amber and GROMACS atom counts
# ==============================================================================

print("\n")
print("=" * 80)
print("COMPARING FILE FORMATS")
print("=" * 80)

gro_atoms = None

if (
    prepared_gro is not None
    and prepared_gro.exists()
):

    with open(prepared_gro) as gro:

        gro.readline()

        gro_atoms = int(
            gro.readline().strip()
        )

    print(
        f"GRO atom count : {gro_atoms}"
    )

if atom_count is not None:

    print(
        f"Amber atoms    : {atom_count}"
    )

if (
    gro_atoms is not None
    and atom_count is not None
):

    if gro_atoms == atom_count:

        print(
            "\n✓ Atom counts agree."
        )

    else:

        print(
            "\nAtom count mismatch."
        )


# %% ==========================================================================
# Overall validation
# ==============================================================================

print("\n")
print("=" * 80)
print("VALIDATION SUMMARY")
print("=" * 80)

validation = {

    "Topology loaded":
        topology is not None,

    "Coordinates loaded":
        inpcrd is not None,

    "One polymer":
        chain_count == 1,

    "No solvent":
        not water_found,

    "No ions":
        not ions_found,

    "Periodic box":
        (
            OPENMM_AVAILABLE
            and
            inpcrd is not None
            and
            inpcrd.boxVectors is not None
        ),

    "Amber/GROMACS agree":
        (
            gro_atoms == atom_count
            if (
                gro_atoms is not None
                and atom_count is not None
            )
            else False
        ),

}

for test, passed in validation.items():

    symbol = "✓" if passed else "✗"

    print(
        f"{symbol} {test}"
    )


# %% ==========================================================================
# Behind the scenes
# ==============================================================================

print("\n")
print("=" * 80)
print("BEHIND THE SCENES - WHY VALIDATE?")
print("=" * 80)

print(
"""
A prepared molecular system can contain hundreds of thousands of atoms.

If an error exists in

    topology

coordinates

box vectors

or atom ordering

the simulation may fail immediately or, even worse, produce incorrect
scientific results.

For this reason experienced molecular modellers never assume a generated
system is correct.

Instead they verify that

        every file

                │

                ▼

        every atom

                │

                ▼

      every coordinate

                │

                ▼

      every topology

is internally consistent before running molecular dynamics.

This validation stage often saves many hours or even days of computational
time.
"""
)


# %% ==========================================================================
# Visualising the prepared system
# ==============================================================================

print("\n")
print("=" * 80)
print("VISUALISING THE SYSTEM")
print("=" * 80)

print(
"""
The final validation step is often visual inspection.

Although numerical checks confirm that the topology is internally
consistent, visualisation allows us to identify

    unusual geometries

    misplaced atoms

    unexpected molecules

    incorrect box placement

Most molecular modelling workflows therefore include both

    numerical validation

and

    visual inspection

before beginning production simulations.

The visualisation tools introduced in previous tutorials can now be used to
inspect the prepared dry system.
"""
)


# %% ==========================================================================
# Part 3 summary
# ==============================================================================

print("\n")
print("=" * 80)
print("PART 3 SUMMARY")
print("=" * 80)

print(
"""
The prepared dry system has now been scientifically validated.

We confirmed

✓ topology integrity

✓ coordinate integrity

✓ atom counts

✓ residue counts

✓ chain count

✓ absence of solvent

✓ absence of ions

✓ periodic box vectors

✓ agreement between Amber and GROMACS

This gives us confidence that the prepared system accurately represents a
single polymer chain inside a periodic simulation box and is suitable for
constructing molecular dynamics workflows.

Part 4 concludes Tutorial 04A by discussing the scientific applications of
dry systems and how they compare with solvated systems and polymer melts.
"""
)

print("\nTutorial 04A Part 3 complete.")

# %% ==========================================================================
# Part 4 - Understanding the Completed Dry Molecular Dynamics System
# ==============================================================================

print("\n")
print("=" * 80)
print("TUTORIAL 04A - PART 4")
print("UNDERSTANDING THE COMPLETED DRY SYSTEM")
print("=" * 80)

print(
"""
The dry molecular dynamics system is now complete.

Rather than thinking of it as a collection of molecular files, it is more
useful to think of it as a complete scientific model.

That model consists of

        One polymer chain

                +

        One periodic simulation box

                +

        A complete molecular force field

                +

        No solvent

                +

        No ions

The chemistry has not changed.

Only the environment surrounding the polymer has changed.
"""
)


# %% ==========================================================================
# What can this system tell us?
# ==============================================================================

print("\n")
print("=" * 80)
print("SCIENTIFIC APPLICATIONS")
print("=" * 80)

applications = [

    (
        "Chain flexibility",
        "Observe how the backbone explores different conformations."
    ),

    (
        "Radius of gyration",
        "Measure the average spatial extent of the polymer."
    ),

    (
        "End-to-end distance",
        "Monitor chain extension during simulation."
    ),

    (
        "Conformational sampling",
        "Explore the accessible conformational landscape."
    ),

    (
        "Backbone dynamics",
        "Investigate intrinsic molecular motion."
    ),

    (
        "Intramolecular hydrogen bonding",
        "Study interactions occurring within a single chain."
    ),

]

for title, description in applications:

    print(f"\n{title}")
    print("-" * len(title))
    print(description)


# %% ==========================================================================
# What can this system NOT tell us?
# ==============================================================================

print("\n")
print("=" * 80)
print("LIMITATIONS OF A DRY SYSTEM")
print("=" * 80)

limitations = [

    "No polymer-water interactions.",

    "No hydration shell.",

    "No dissolved ions.",

    "No polymer-polymer interactions.",

    "No bulk density.",

    "No glass transition temperature.",

    "No oxygen diffusion through bulk material.",

]

for limitation in limitations:

    print(f"• {limitation}")

print(
"""

These properties require more complex simulation environments that will be
introduced in later tutorials.
"""
)


# %% ==========================================================================
# Comparing the available MD systems
# ==============================================================================

print("\n")
print("=" * 80)
print("COMPARING THE AVAILABLE SYSTEMS")
print("=" * 80)

comparison = [

    (
        "Dry",
        "Intrinsic chain behaviour"
    ),

    (
        "Solvated",
        "Polymer-water interactions"
    ),

    (
        "Solvated + ions",
        "Electrolyte environments"
    ),

    (
        "Polymer melt",
        "Bulk material properties"
    ),

]

print(f"{'System':<22}Primary application")
print("-" * 80)

for system, purpose in comparison:

    print(f"{system:<22}{purpose}")


# %% ==========================================================================
# Behind the scenes - what changes next?
# ==============================================================================

print("\n")
print("=" * 80)
print("BEHIND THE SCENES - BUILDING NEW ENVIRONMENTS")
print("=" * 80)

print(
"""
One of the central ideas behind iPHAsimulator is that the polymer itself
does not need to be rebuilt when creating different molecular environments.

The workflow is

        Parameterise polymer

                │

                ▼

         Build polymer

                │

                ▼

      Dry system (this tutorial)

                │

        ┌───────┴────────┐
        │                │
        ▼                ▼

   Add water        Copy many chains

        │                │
        ▼                ▼

 Solvated system   Polymer melt

        │
        ▼

  Add dissolved ions

        │
        ▼

 Solvated ionic system

Notice that every branch starts from exactly the same validated polymer.

The molecular force field never changes.

Only the surrounding environment changes.
"""
)


# %% ==========================================================================
# The complete workflow so far
# ==============================================================================

print("\n")
print("=" * 80)
print("THE COMPLETE WORKFLOW")
print("=" * 80)

print(
"""
Across the first four tutorials we have gradually transformed a simple
chemical description into a complete molecular dynamics system.

        Monomer SMILES

                │

                ▼

     Parameterise chemistry

                │

                ▼

     Generate residue library

                │

                ▼

      Build finite polymer

                │

                ▼

      Prepare dry MD system

                │

                ▼

      Validate the system

At this point the system is ready for simulation workflow generation.
"""
)


# %% ==========================================================================
# Knowledge check
# ==============================================================================

print("\n")
print("=" * 80)
print("KNOWLEDGE CHECK")
print("=" * 80)

print(
"""
1.

Does creating a dry system change the molecular force field?

2.

Why is box padding required?

3.

Can a dry system be used to measure polymer hydration?

4.

Which properties are best investigated using a dry system?

5.

Why should every prepared system be validated before simulation?

Take a few moments to answer these questions before reading the solutions.
"""
)


# %% ==========================================================================
# Knowledge check answers
# ==============================================================================

print("\n")
print("=" * 80)
print("KNOWLEDGE CHECK - ANSWERS")
print("=" * 80)

print(
"""
1.

No.

The polymer chemistry, atom types, charges and bonded parameters are reused
without modification.

2.

Padding separates the polymer from its periodic images and defines the
simulation box dimensions.

3.

No.

Hydration requires explicit solvent molecules.

4.

Examples include

    • chain flexibility

    • radius of gyration

    • backbone motion

    • conformational sampling

5.

Validation confirms that the topology, coordinates and simulation box are
internally consistent before computationally expensive simulations begin.
"""
)


# %% ==========================================================================
# Tutorial summary
# ==============================================================================

print("\n")
print("=" * 80)
print("TUTORIAL 04A SUMMARY")
print("=" * 80)

print(
"""
Congratulations!

You have successfully prepared and validated your first molecular dynamics
system using iPHAsimulator.

During this tutorial you

✓ understood the purpose of a dry molecular dynamics system

✓ introduced a periodic simulation box

✓ prepared a complete dry single-chain system

✓ examined the generated molecular files

✓ validated the topology and coordinates

✓ confirmed the absence of solvent and ions

✓ registered the prepared system

Most importantly, you have now seen the distinction between

        a finite polymer

and

        a simulation-ready molecular system.

Although the chemistry is identical, the prepared system now contains all of
the information required by a molecular dynamics engine.
"""
)


# %% ==========================================================================
# Looking ahead
# ==============================================================================

print("\n")
print("=" * 80)
print("LOOKING AHEAD")
print("=" * 80)

print(
"""
In Tutorial 04B we will revisit exactly the same polymer.

Rather than rebuilding its chemistry, we will simply change its
environment.

Starting with the validated dry system, we will

        Add explicit water

                │

                ▼

     Create a solvated system

We will learn

    • how water molecules are added

    • how the solvent box is generated

    • how solvent molecules are removed when clashes occur

    • how the prepared system is updated and registered

Notice that the polymer itself remains unchanged.

Only the world surrounding it becomes more realistic.

This philosophy—parameterise once, reuse everywhere—underpins the design of
iPHAsimulator.
"""
)

print("\nTutorial 04A complete.")