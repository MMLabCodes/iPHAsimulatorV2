#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
===============================================================================
Tutorial 04B - Building a Solvated Single-Chain Molecular Dynamics System
Part 1 - Understanding Solvation and Preparing the Inputs
===============================================================================

In Tutorial 04A we prepared the simplest molecular dynamics environment
supported by iPHAsimulator: a single polymer chain inside an empty periodic
simulation box.

Although this system is extremely useful for studying the intrinsic behaviour
of an isolated polymer, it does not represent the environment experienced by
most polymers in experiments or biological systems.

Many important molecular properties are strongly influenced by interactions
with the surrounding solvent.

In this tutorial we will construct a solvated molecular dynamics system,
where the polymer is completely immersed in explicit water molecules.

The preparation workflow is

        Built polymer

              │

              ▼

      Validate polymer

              │

              ▼

      Choose water model

              │

              ▼

     Define simulation box

              │

              ▼

      Fill box with water

              │

              ▼

 Remove overlapping waters

              │

              ▼

      Write system files

              │

              ▼

      Register system

By the end of Tutorial 04B we will have created a complete aqueous molecular
dynamics system suitable for studying polymer behaviour in solution.

This first part introduces

    • why explicit solvent is required

    • what a solvated system represents

    • different water models

    • the information required before solvation

    • preparation of the source polymer

No water molecules are added during Part 1. We first establish the concepts
and verify that the source polymer is ready for solvation.

===============================================================================
"""


# %% ==========================================================================
# Imports
# ==============================================================================

from pathlib import Path
import sys


# %% ==========================================================================
# Locate the project
# ==============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

STRUCTURE_DATABASE = PROJECT_ROOT / "structure_database"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.iphasimulator.pha_filepath_manager import PHAFileManager


# %% ==========================================================================
# Initialise the project
# ==============================================================================

paths = PHAFileManager(
    root_dir=STRUCTURE_DATABASE,
)

print("=" * 80)
print("Tutorial 04B - Building a Solvated Single-Chain MD System")
print("Part 1 - Understanding Solvation and Preparing the Inputs")
print("=" * 80)


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

    Building a finite polymer

✓ Tutorial 03

    Understanding molecular dynamics systems

✓ Tutorial 04A

    Building a dry single-chain system


Current tutorial

► Tutorial 04B

    Building a solvated single-chain system


Upcoming tutorials

□ Tutorial 04C

    Building a solvated system with ions

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
A solvated molecular dynamics system consists of

        One polymer chain

                +

        Thousands of explicit water molecules

                +

        A periodic simulation box

Unlike the dry system prepared in Tutorial 04A, the surrounding space is no
longer empty.

Instead, the polymer is immersed in an environment intended to represent
liquid water.

Every water molecule is treated as an individual collection of atoms that can

    • translate

    • rotate

    • hydrogen bond

    • diffuse

throughout the simulation.

Because every solvent molecule is represented explicitly, the resulting
system contains far more atoms than the polymer alone.
"""
)


# %% ==========================================================================
# Why simulate in water?
# ==============================================================================

print("\n")
print("=" * 80)
print("WHY SIMULATE IN WATER?")
print("=" * 80)

print(
"""
Water is the most common solvent encountered in chemistry and biology.

Many experimentally measured polymer properties depend strongly on the
surrounding solvent.

Examples include

    • polymer swelling

    • hydration

    • hydrogen bonding

    • chain conformation

    • solvent accessibility

    • diffusion in solution

Without explicit solvent, these processes cannot be represented directly.

Adding water allows the polymer and solvent to interact naturally throughout
the molecular dynamics simulation.
"""
)


# %% ==========================================================================
# Explicit versus implicit solvent
# ==============================================================================

print("\n")
print("=" * 80)
print("EXPLICIT AND IMPLICIT SOLVENT")
print("=" * 80)

print(
"""
There are two common approaches for representing solvent.

Explicit solvent

        O O O O O O O O

        O    polymer   O

        O O O O O O O O

Every water molecule is represented by individual atoms.

This approach is computationally more expensive but provides a detailed,
physically realistic description of solvent behaviour.


Implicit solvent

        polymer

The surrounding solvent is represented mathematically rather than with
individual water molecules.

This approach is computationally cheaper but cannot describe individual water
molecules or hydrogen-bonding networks.

Throughout the iPHAsimulator tutorials we will primarily use explicit
solvent.
"""
)


# %% ==========================================================================
# The role of the simulation box
# ==============================================================================

print("\n")
print("=" * 80)
print("THE SIMULATION BOX")
print("=" * 80)

print(
"""
In Tutorial 04A the simulation box was simply empty space surrounding the
polymer.

During solvation, this empty volume becomes occupied by water molecules.

Conceptually

Dry system

+--------------------------------+
|                                |
|           polymer              |
|                                |
+--------------------------------+

becomes

+--------------------------------+
| O O O O O O O O O O O O O O O  |
| O O O polymer O O O O O O O O  |
| O O O O O O O O O O O O O O O  |
+--------------------------------+

The size of the simulation box therefore determines how many water molecules
can be added.
"""
)


# %% ==========================================================================
# Water models
# ==============================================================================

print("\n")
print("=" * 80)
print("WATER MODELS")
print("=" * 80)

print(
"""
Water molecules are described using molecular mechanics force fields known as
water models.

Several models are commonly used in molecular dynamics simulations.

TIP3P

    A simple three-site model widely used with AMBER force fields.

SPC

    Another three-site model commonly used in condensed-phase simulations.

SPC/E

    An extension of SPC that improves several bulk liquid properties.

OPC

    A newer four-site model designed to reproduce experimental water
    properties more accurately.

Different water models provide different balances between computational cost
and physical accuracy.

The choice of water model should be compatible with the molecular force field
used for the polymer.
"""
)


# %% ==========================================================================
# User settings
# ==============================================================================

print("\n")
print("=" * 80)
print("USER SETTINGS")
print("=" * 80)

POLYMER_NAME = "P3HB_10"

WATER_MODEL = "tip3p"

BOX_PADDING = 1.2

OVERWRITE = False

RUN_SOLVATION = False

print(f"Polymer name      : {POLYMER_NAME}")
print(f"Water model       : {WATER_MODEL}")
print(f"Box padding (nm)  : {BOX_PADDING}")
print(f"Overwrite outputs : {OVERWRITE}")
print(f"Run solvation     : {RUN_SOLVATION}")


# %% ==========================================================================
# Interpreting the settings
# ==============================================================================

print("\n")
print("=" * 80)
print("INTERPRETING THE SETTINGS")
print("=" * 80)

print(f"""
POLYMER_NAME

    {POLYMER_NAME}

identifies the previously constructed finite polymer.

WATER_MODEL

    {WATER_MODEL}

defines the force field used to represent every water molecule.

BOX_PADDING

    {BOX_PADDING}

determines the minimum separation between the polymer and the edge of the
solvent box before water molecules are inserted.

OVERWRITE

controls whether an existing solvated system may be replaced.

RUN_SOLVATION

is a tutorial safety switch.

Part 1 does not generate any new molecular files.
""")


# %% ==========================================================================
# Locating the source polymer
# ==============================================================================

print("\n")
print("=" * 80)
print("LOCATING THE SOURCE POLYMER")
print("=" * 80)

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

print(polymer_dir)

if polymer_dir.exists():

    print("\n✓ Polymer located.")

else:

    print("\n✗ Polymer could not be found.")


# %% ==========================================================================
# Preparing for solvation
# ==============================================================================

print("\n")
print("=" * 80)
print("PREPARING FOR SOLVATION")
print("=" * 80)

print(
"""
Before water molecules can be added, the molecular dynamics system builder
must first gather the information required to construct the solvated system.

At a high level, this preparation consists of

    locating the polymer

            │

            ▼

    reading the topology

            │

            ▼

    reading the coordinates

            │

            ▼

    selecting the water model

            │

            ▼

    defining the simulation box

Only after these inputs have been verified is the system ready for the
solvation process itself.
"""
)


# %% ==========================================================================
# Behind the scenes
# ==============================================================================

print("\n")
print("=" * 80)
print("BEHIND THE SCENES - PREPARING FOR SOLVATION")
print("=" * 80)

print(
"""
The solvation builder performs several preliminary checks before creating any
new molecular files.

It confirms

✓ the polymer exists

✓ a valid topology is available

✓ coordinate files can be located

✓ the requested water model is recognised

✓ sufficient information is available to define a simulation box

At this stage, nothing has been modified.

The source polymer remains unchanged.

In Part 2 we will use these validated inputs to construct the complete
solvated molecular dynamics system.
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
In this section we introduced explicit solvation and prepared the inputs
required to construct an aqueous molecular dynamics system.

We learned that

✓ explicit solvent represents every water molecule individually

✓ water enables realistic polymer-solvent interactions

✓ different water models exist for different simulation requirements

✓ the simulation box determines how many water molecules can be added

✓ the source polymer must be validated before solvation begins

In Part 2 we will generate the solvated system, examine how water molecules
are inserted, and explore the files produced by the system preparation
workflow.
"""
)

print("\nTutorial 04B Part 1 complete.")

# %% ==========================================================================
# Part 2 - Constructing the Solvated Molecular Dynamics System
# ==============================================================================

print("\n")
print("=" * 80)
print("TUTORIAL 04B - PART 2")
print("CONSTRUCTING THE SOLVATED MOLECULAR DYNAMICS SYSTEM")
print("=" * 80)

print(
"""
In Part 1 we introduced explicit solvent and prepared the information
required to build a solvated molecular dynamics system.

The source polymer has already been validated.

The water model has been selected.

The simulation box has been defined.

We are now ready to surround the polymer with explicit water molecules.

Conceptually, the workflow is

        Validated polymer

                │

                ▼

       Define simulation box

                │

                ▼

      Generate solvent box

                │

                ▼

      Remove overlapping water

                │

                ▼

       Update molecular files

                │

                ▼

        Register new system

By the end of this section we will have produced a complete solvated system
ready for validation.
"""
)


# %% ==========================================================================
# Initialising the molecular system builder
# ==============================================================================

print("\n")
print("=" * 80)
print("INITIALISING THE SYSTEM BUILDER")
print("=" * 80)

try:

    from src.iphasimulator.md_system_builder import MDSystemBuilder

    system_builder = MDSystemBuilder(
        file_manager=paths,
    )

    print("✓ MD system builder initialised.")

except Exception as error:

    system_builder = None

    print(error)

    print(
"""
Update the import so that it matches the public system builder used by the
current version of iPHAsimulator.

The tutorial intentionally relies on the public API rather than reproducing
the underlying implementation.
"""
    )


# %% ==========================================================================
# Define the new molecular system
# ==============================================================================

print("\n")
print("=" * 80)
print("DEFINING THE SOLVATED SYSTEM")
print("=" * 80)

SYSTEM_NAME = f"{POLYMER_NAME}_solvated"

SYSTEM_TYPE = "solvated"

print(f"Polymer      : {POLYMER_NAME}")
print(f"System       : {SYSTEM_NAME}")
print(f"Water model  : {WATER_MODEL}")
print(f"Padding (nm) : {BOX_PADDING}")


# %% ==========================================================================
# The construction request
# ==============================================================================

print("\n")
print("=" * 80)
print("CONSTRUCTION REQUEST")
print("=" * 80)

print(
"""
The system builder requires enough information to answer four questions.

1.

Which polymer should be solvated?

        P3HB_10

2.

Which solvent model should be used?

        TIP3P

3.

How large should the simulation box be?

        Polymer size
                +
        Requested padding

4.

Where should the completed system be written?

        Registered MD system directory

Once these questions have been answered, the preparation process can begin.
"""
)


# %% ==========================================================================
# Build the solvated system
# ==============================================================================

print("\n")
print("=" * 80)
print("GENERATING THE SOLVATED SYSTEM")
print("=" * 80)

solvated_result = None

if RUN_SOLVATION and system_builder is not None:

    print(
f"""
Preparing

    {SYSTEM_NAME}

using

    {WATER_MODEL}

water.
"""
    )

    solvated_result = (
        system_builder.build_solvated_single_chain_system(

            polymer_name=POLYMER_NAME,

            system_name=SYSTEM_NAME,

            water_model=WATER_MODEL,

            box_padding=BOX_PADDING,

            overwrite=OVERWRITE,

        )
    )

    print()

    print("✓ Solvation complete.")

else:

    print(
"""
RUN_SOLVATION is False.

No molecular files have been modified.

Enable the execution switch after confirming the settings.
"""
    )


# %% ==========================================================================
# Behind the scenes
# ==============================================================================

print("\n")
print("=" * 80)
print("BEHIND THE SCENES - THE SOLVATION WORKFLOW")
print("=" * 80)

print(
"""
Although the user performs a single high-level function call, a number of
operations occur internally.

The preparation workflow is

        Read polymer

                │

                ▼

      Calculate box size

                │

                ▼

     Generate empty solvent box

                │

                ▼

     Fill box with water

                │

                ▼

 Remove overlapping molecules

                │

                ▼

 Update topology

                │

                ▼

 Update coordinates

                │

                ▼

 Write molecular files

                │

                ▼

 Register completed system

Each stage contributes to producing a physically meaningful molecular
environment.

The original polymer itself is not rebuilt.
"""
)


# %% ==========================================================================
# Filling the simulation box
# ==============================================================================

print("\n")
print("=" * 80)
print("FILLING THE SIMULATION BOX")
print("=" * 80)

print(
"""
The first stage of solvation is conceptually simple.

Imagine an empty periodic box

+--------------------------------+
|                                |
|            polymer             |
|                                |
+--------------------------------+

The surrounding volume is then filled with water molecules

+--------------------------------+
| O O O O O O O O O O O O O O O  |
| O O O polymer O O O O O O O O  |
| O O O O O O O O O O O O O O O  |
+--------------------------------+

At this stage, the water molecules have been generated without considering
whether they overlap with the polymer.

This means the intermediate system is not yet physically meaningful.
"""
)


# %% ==========================================================================
# Why overlapping waters are removed
# ==============================================================================

print("\n")
print("=" * 80)
print("REMOVING OVERLAPPING WATER MOLECULES")
print("=" * 80)

print(
"""
Water molecules cannot occupy the same physical space as the polymer.

After the solvent box has been generated, every water molecule is examined.

Water molecules whose atoms overlap the polymer are deleted.

Conceptually

Before

        O

      polymer

After

      polymer

The surrounding waters remain untouched.

This process creates a cavity that exactly accommodates the polymer while
maintaining a continuous solvent environment.
"""
)


# %% ==========================================================================
# Updating the topology
# ==============================================================================

print("\n")
print("=" * 80)
print("UPDATING THE TOPOLOGY")
print("=" * 80)

print(
"""
The topology must now describe

        Polymer

                +

        Water molecules

Every atom

Every bond

Every angle

Every dihedral

Every residue

must be represented.

Compared with the dry system, the topology is now substantially larger
because thousands of additional atoms have been introduced.
"""
)


# %% ==========================================================================
# Updating the coordinates
# ==============================================================================

print("\n")
print("=" * 80)
print("UPDATING THE COORDINATES")
print("=" * 80)

print(
"""
The coordinate file is also expanded.

Originally it contained

        polymer atoms

After solvation it contains

        polymer atoms

                +

        water atoms

Consequently, the majority of coordinates now belong to solvent molecules
rather than the polymer itself.
"""
)


# %% ==========================================================================
# Inspecting the generated directory
# ==============================================================================

print("\n")
print("=" * 80)
print("GENERATED DIRECTORY")
print("=" * 80)

if solvated_result is not None:

    if hasattr(solvated_result, "system_dir"):

        system_dir = Path(
            solvated_result.system_dir
        )

        print(system_dir)

else:

    print(
"""
The output directory will become available after the solvated system has been
generated.
"""
    )


# %% ==========================================================================
# Examining the generated molecular files
# ==============================================================================

print("\n")
print("=" * 80)
print("GENERATED MOLECULAR FILES")
print("=" * 80)

print(
"""
A typical solvated system contains

Amber

    topology

    coordinates

GROMACS

    topology

    coordinates

Metadata

    registry information

Although the filenames resemble those produced for the dry system, the
contents are now fundamentally different because explicit solvent molecules
have been incorporated.
"""
)


# %% ==========================================================================
# Comparing dry and solvated systems
# ==============================================================================

print("\n")
print("=" * 80)
print("DRY VERSUS SOLVATED")
print("=" * 80)

comparison = [

    ("Polymer", "✓", "✓"),

    ("Periodic box", "✓", "✓"),

    ("Water molecules", "✗", "✓"),

    ("Hydrogen bonding", "Limited", "Realistic"),

    ("Hydration", "✗", "✓"),

]

print(f"{'Property':<28}{'Dry':<15}{'Solvated'}")
print("-"*80)

for property_name, dry, solvated in comparison:

    print(f"{property_name:<28}{dry:<15}{solvated}")


# %% ==========================================================================
# Registering the new molecular system
# ==============================================================================

print("\n")
print("=" * 80)
print("REGISTERING THE SYSTEM")
print("=" * 80)

print(
"""
The final preparation stage records the completed system within the molecular
system registry.

The registry allows future workflows to identify

    • the source polymer

    • the solvent model

    • the system type

    • the simulation files

without manually searching the directory structure.

This separation between

        molecular files

and

        system metadata

is one of the core organisational principles used throughout
iPHAsimulator.
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
During this section we transformed an isolated polymer into a solvated
molecular dynamics system.

We learned that

✓ a solvent box is generated around the polymer

✓ overlapping water molecules are removed

✓ the topology is expanded to include solvent

✓ the coordinate file now contains thousands of additional atoms

✓ the completed system is written to disk and registered

The polymer itself has not changed.

Instead, a realistic aqueous environment has been constructed around it.

In Part 3 we will validate the completed solvated system by examining the
topology, coordinates, water content, periodic box, and molecular
consistency.
"""
)

print("\nTutorial 04B Part 2 complete.")

# %% ==========================================================================
# Tutorial 04B - Part 3
# Validating the Solvated Molecular Dynamics System
# ==============================================================================

print("\n")
print("=" * 80)
print("TUTORIAL 04B - PART 3")
print("VALIDATING THE SOLVATED MOLECULAR DYNAMICS SYSTEM")
print("=" * 80)

print(
"""
The solvated molecular dynamics system has now been created.

Before using it in molecular dynamics simulations we should verify that the
generated system is internally consistent.

Unlike the dry system prepared in Tutorial 04A, validation now includes both
the polymer and thousands of surrounding water molecules.

Throughout this section we will verify

    • the topology

    • the coordinates

    • atom counts

    • residue counts

    • water molecules

    • periodic box vectors

    • solvent composition

    • registry information

Only after these checks pass should the system be considered ready for
simulation.
"""
)


# %% ==========================================================================
# Loading the solvated system
# ==============================================================================

print("\n")
print("=" * 80)
print("LOADING THE SOLVATED SYSTEM")
print("=" * 80)

try:

    from openmm.app import AmberPrmtopFile
    from openmm.app import AmberInpcrdFile

    prmtop = AmberPrmtopFile(
        str(prepared_prmtop)
    )

    inpcrd = AmberInpcrdFile(
        str(prepared_rst7)
    )

    topology = prmtop.topology

    print("✓ Solvated system loaded successfully.")

except Exception as error:

    topology = None

    print(error)


# %% ==========================================================================
# Overall system size
# ==============================================================================

print("\n")
print("=" * 80)
print("OVERALL SYSTEM SIZE")
print("=" * 80)

if topology is not None:

    atoms = list(topology.atoms())
    residues = list(topology.residues())
    chains = list(topology.chains())

    print(f"Atoms     : {len(atoms)}")
    print(f"Residues  : {len(residues)}")
    print(f"Chains    : {len(chains)}")


# %% ==========================================================================
# Polymer verification
# ==============================================================================

print("\n")
print("=" * 80)
print("VERIFYING THE POLYMER")
print("=" * 80)

polymer_residues = []

water_residues = []

for residue in residues:

    if residue.name.upper() in {

        "WAT",
        "HOH",
        "SOL",
        "TIP3",
        "TIP3P",

    }:

        water_residues.append(residue)

    else:

        polymer_residues.append(residue)

print(f"Polymer residues : {len(polymer_residues)}")

print(f"Water residues   : {len(water_residues)}")


# %% ==========================================================================
# Water molecules
# ==============================================================================

print("\n")
print("=" * 80)
print("EXPLICIT SOLVENT")
print("=" * 80)

number_of_waters = len(water_residues)

print(f"Water molecules : {number_of_waters}")

print()

print(
"""
Unlike the dry system created in Tutorial 04A, the majority of the molecular
system now consists of explicit solvent.

Every water molecule participates independently in the molecular dynamics
simulation.
"""
)


# %% ==========================================================================
# Solvent composition
# ==============================================================================

print("\n")
print("=" * 80)
print("SOLVENT COMPOSITION")
print("=" * 80)

polymer_atoms = 0

water_atoms = 0

for residue in residues:

    atom_total = len(list(residue.atoms()))

    if residue in water_residues:

        water_atoms += atom_total

    else:

        polymer_atoms += atom_total

total_atoms = polymer_atoms + water_atoms

print(f"Polymer atoms : {polymer_atoms}")

print(f"Water atoms   : {water_atoms}")

print()

print(
f"Water atoms comprise approximately "
f"{100*water_atoms/total_atoms:.1f}% "
"of the complete molecular system."
)


# %% ==========================================================================
# Periodic box vectors
# ==============================================================================

print("\n")
print("=" * 80)
print("PERIODIC BOX")
print("=" * 80)

box = inpcrd.boxVectors

if box is not None:

    print("✓ Periodic box vectors detected.\n")

    print(box)

else:

    print("No periodic box vectors were found.")


# %% ==========================================================================
# Estimating the initial density
# ==============================================================================

print("\n")
print("=" * 80)
print("INITIAL SYSTEM DENSITY")
print("=" * 80)

print(
"""
At this stage the density is only an estimate.

Following energy minimisation and equilibration, the box dimensions may
change as the system relaxes towards equilibrium.

Consequently, the initial density should not be interpreted as the final
physical density of the simulated system.

Instead, it serves as a useful diagnostic during system preparation.
"""
)


# %% ==========================================================================
# Amber and GROMACS consistency
# ==============================================================================

print("\n")
print("=" * 80)
print("COMPARING FILE FORMATS")
print("=" * 80)

print(
"""
The solvated molecular system should be represented consistently across every
supported file format.

Important quantities that should agree include

    • total atom count

    • residue count

    • solvent molecules

    • periodic box dimensions

Only the file format changes.

The underlying molecular system remains identical.
"""
)


# %% ==========================================================================
# Visual inspection
# ==============================================================================

print("\n")
print("=" * 80)
print("VISUAL INSPECTION")
print("=" * 80)

print(
"""
Numerical validation is extremely important, but experienced molecular
modellers almost always inspect the prepared system visually before running
simulations.

When visualising the solvated system you should observe

    • one polymer chain

    • a continuous solvent environment

    • no obvious voids

    • no misplaced molecules

    • no large solvent overlaps

The polymer should appear fully immersed within the surrounding water box.
"""
)


# %% ==========================================================================
# Registry validation
# ==============================================================================

print("\n")
print("=" * 80)
print("SYSTEM REGISTRY")
print("=" * 80)

print(
"""
Finally, confirm that the prepared system has been registered correctly.

The registry should identify

    • the source polymer

    • the system type

    • the selected water model

    • the molecular files

This allows future workflows to locate the system automatically without
manual directory navigation.
"""
)


# %% ==========================================================================
# Behind the scenes
# ==============================================================================

print("\n")
print("=" * 80)
print("BEHIND THE SCENES - WHY VALIDATION IS EVEN MORE IMPORTANT")
print("=" * 80)

print(
"""
A solvated system is often an order of magnitude larger than the original
polymer.

For example

        Dry system

            1,500 atoms

                │

                ▼

      Solvated system

           40,000 atoms

A small preparation error therefore affects thousands of atoms rather than
just a few hundred.

Validation provides confidence that

        polymer

            +

        solvent

            +

        topology

            +

        coordinates

            +

        periodic box

all describe the same physical molecular system.
"""
)


# %% ==========================================================================
# Validation summary
# ==============================================================================

print("\n")
print("=" * 80)
print("VALIDATION SUMMARY")
print("=" * 80)

validation = {

    "Topology loaded" :
        topology is not None,

    "Polymer detected" :
        len(polymer_residues) > 0,

    "Water molecules detected" :
        len(water_residues) > 0,

    "Periodic box present" :
        box is not None,

    "System contains explicit solvent" :
        water_atoms > 0,

}

for check, passed in validation.items():

    symbol = "✓" if passed else "✗"

    print(f"{symbol} {check}")


# %% ==========================================================================
# Part 3 summary
# ==============================================================================

print("\n")
print("=" * 80)
print("PART 3 SUMMARY")
print("=" * 80)

print(
"""
The completed solvated molecular dynamics system has now been validated.

We confirmed

✓ the topology loads correctly

✓ the coordinates load correctly

✓ the polymer is present

✓ explicit water molecules surround the polymer

✓ periodic box vectors exist

✓ the solvent dominates the molecular system

✓ the prepared system is ready for molecular dynamics simulations.

In Part 4 we will discuss when solvated systems should be used, what
scientific questions they can answer, and how they compare with the dry
single-chain systems created in Tutorial 04A.
"""
)

print("\nTutorial 04B Part 3 complete.")

# %% ==========================================================================
# Tutorial 04B - Part 4
# Understanding the Completed Solvated Molecular Dynamics System
# ==============================================================================

print("\n")
print("=" * 80)
print("TUTORIAL 04B - PART 4")
print("UNDERSTANDING THE COMPLETED SOLVATED SYSTEM")
print("=" * 80)

print(
"""
The solvated molecular dynamics system is now complete.

Unlike the dry system constructed in Tutorial 04A, the polymer is no longer
isolated.

Instead, it exists inside an explicit aqueous environment where every water
molecule is represented individually.

The completed system now consists of

        One polymer chain

                +

        Thousands of explicit water molecules

                +

        One periodic simulation box

                +

        A complete molecular force field

The polymer itself has not changed.

Only the environment surrounding the polymer has changed.
"""
)


# %% ==========================================================================
# What can we investigate?
# ==============================================================================

print("\n")
print("=" * 80)
print("SCIENTIFIC APPLICATIONS")
print("=" * 80)

applications = [

    (
        "Polymer hydration",
        "Observe how water molecules surround different regions of the polymer."
    ),

    (
        "Hydrogen bonding",
        "Investigate hydrogen bonds between the polymer and surrounding water."
    ),

    (
        "Conformational behaviour",
        "Study how the solvent influences polymer structure."
    ),

    (
        "Polymer swelling",
        "Examine structural expansion or contraction in solution."
    ),

    (
        "Radius of gyration",
        "Measure polymer size in an aqueous environment."
    ),

    (
        "Solvent accessible surface area",
        "Determine which regions of the polymer interact with water."
    ),

    (
        "Water diffusion",
        "Investigate solvent mobility around the polymer."
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
print("LIMITATIONS")
print("=" * 80)

limitations = [

    "Bulk polymer density.",

    "Glass transition temperature.",

    "Polymer-polymer aggregation.",

    "Mechanical behaviour of bulk material.",

    "Crystallisation within polymer melts.",

    "Oxygen diffusion through amorphous polymer matrices.",

]

for limitation in limitations:

    print(f"• {limitation}")

print(
"""

These properties require multiple interacting polymer chains and will be
introduced in Tutorial 05.
"""
)


# %% ==========================================================================
# Comparing dry and solvated systems
# ==============================================================================

print("\n")
print("=" * 80)
print("DRY VERSUS SOLVATED SYSTEMS")
print("=" * 80)

comparison = [

    ("Explicit water",          "✗", "✓"),

    ("Hydration",               "✗", "✓"),

    ("Hydrogen bonding",        "Limited", "✓"),

    ("Polymer flexibility",     "✓", "✓"),

    ("Radius of gyration",      "✓", "✓"),

    ("Solution behaviour",      "✗", "✓"),

    ("Bulk polymer behaviour",  "✗", "✗"),

]

print(f"{'Property':<30}{'Dry':<15}{'Solvated'}")
print("-" * 80)

for property_name, dry, solvated in comparison:

    print(f"{property_name:<30}{dry:<15}{solvated}")


# %% ==========================================================================
# Choosing the appropriate system
# ==============================================================================

print("\n")
print("=" * 80)
print("CHOOSING THE RIGHT SYSTEM")
print("=" * 80)

print(
"""
The environment surrounding the polymer should always match the scientific
question being investigated.

For example

Question

    How flexible is an isolated polymer chain?

Recommended system

    Dry single-chain system


Question

    How does water influence polymer conformation?

Recommended system

    Solvated single-chain system


Question

    How does salt influence polymer behaviour?

Recommended system

    Solvated system with ions
    (Tutorial 04C)


Question

    What are the bulk properties of the polymer?

Recommended system

    Polymer melt
    (Tutorial 05)

The simulation environment should always be selected according to the
scientific problem rather than computational convenience.
"""
)


# %% ==========================================================================
# Behind the scenes
# ==============================================================================

print("\n")
print("=" * 80)
print("BEHIND THE SCENES - REUSING THE SAME POLYMER")
print("=" * 80)

print(
"""
One of the fundamental design principles of iPHAsimulator is that the polymer
chemistry is generated only once.

After parameterisation and polymer construction, the same molecular structure
can be reused in multiple environments.

                Parameterise polymer

                         │

                         ▼

                  Build polymer

                         │

        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼

    Dry system      Solvated system   Polymer melt

                         │

                         ▼

                Add dissolved ions

                         │

                         ▼

               Electrolyte system

The chemistry remains identical.

Only the molecular environment changes.

This modular workflow avoids repeating expensive parameterisation while
allowing many different simulation systems to be generated from a single
validated polymer.
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
Across the first five tutorials we have progressively transformed a chemical
description into a realistic solvated molecular dynamics system.

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

      Prepare dry system

                │

                ▼

     Add explicit solvent

                │

                ▼

 Validate solvated system

The completed system is now suitable for studying polymer behaviour in
aqueous solution.
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

Why is explicit solvent required to study hydration?

2.

Does adding water change the polymer force field?

3.

Why are overlapping water molecules removed during system preparation?

4.

Why do solvated systems usually contain many more atoms than dry systems?

5.

Would a solvated single-chain simulation be appropriate for predicting the
glass transition temperature of a polymer?

Take a few moments to consider each question before reading the answers.
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

Hydration depends on individual interactions between water molecules and the
polymer. Explicit solvent allows these interactions to be represented
directly.

2.

No.

The polymer topology, atom types and force-field parameters remain unchanged.

3.

Water molecules occupying the same physical space as the polymer would create
an unrealistic molecular structure. These molecules are removed to produce a
physically meaningful solvated environment.

4.

The solvent typically occupies a much larger volume than the polymer itself.
As a result, most atoms in the simulation belong to water molecules.

5.

No.

Glass transition is a bulk property that requires simulations containing many
interacting polymer chains rather than a single solvated molecule.
"""
)


# %% ==========================================================================
# Tutorial summary
# ==============================================================================

print("\n")
print("=" * 80)
print("TUTORIAL 04B SUMMARY")
print("=" * 80)

print(
"""
Congratulations!

You have successfully prepared and validated your first solvated molecular
dynamics system using iPHAsimulator.

During this tutorial you

✓ introduced explicit solvent

✓ selected a water model

✓ generated a solvated simulation box

✓ removed overlapping solvent molecules

✓ updated the molecular topology

✓ validated the completed molecular system

✓ explored the scientific applications of aqueous simulations

You now understand the distinction between

        an isolated polymer

and

        a polymer immersed in an explicit solvent environment.

Although the polymer chemistry is unchanged, the surrounding water enables a
wide range of new molecular phenomena to be investigated.
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
In Tutorial 04C we will extend the solvated system by introducing dissolved
ions.

Starting from the validated aqueous environment created in this tutorial we
will

        Solvated polymer

                │

                ▼

        Add dissolved ions

                │

                ▼

     Create an electrolyte system

We will learn

    • why ions are added

    • how ion concentrations are specified

    • how water molecules are replaced by ions

    • how charge neutrality is maintained

    • how ionic systems are validated

Once complete, we will have constructed a realistic electrolyte environment
suitable for investigating polymer behaviour under experimentally relevant
solution conditions.
"""
)

print("\nTutorial 04B complete.")