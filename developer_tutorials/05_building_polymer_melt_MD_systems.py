#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
===============================================================================
Tutorial 05 - Constructing Bulk Polymer Systems

Part 1 - Understanding Bulk Polymer Materials
===============================================================================

In the previous tutorials we prepared several molecular environments for a
single polymer chain.

Tutorial 04A

    Polymer

        inside

    an empty periodic box

Tutorial 04B

    Polymer

        inside

    explicit water

Tutorial 04C

    Polymer

        inside

    an electrolyte solution

Although these systems are extremely useful for studying the behaviour of an
individual polymer, they cannot describe the properties of bulk polymer
materials.

Many experimentally measured properties emerge only when large numbers of
polymer chains interact with one another.

Examples include

    • density

    • glass transition temperature

    • free volume

    • chain entanglement

    • thermal expansion

    • mechanical behaviour

    • oxygen diffusion through the material

To investigate these collective properties we must move beyond isolated
polymer chains and construct condensed polymer systems containing many
interacting molecules.

The preparation workflow is

        Finite polymer

               │

               ▼

      Duplicate polymer

               │

               ▼

     Create multiple chains

               │

               ▼

     Arrange within a box

               │

               ▼

      Specify target density

               │

               ▼

      Generate bulk system

               │

               ▼

      Register molecular system

By the end of this tutorial we will have prepared a realistic polymer melt
containing many interacting polymer chains.

In Part 1 we introduce

    • why bulk systems are required

    • emergent material properties

    • polymer melts

    • amorphous and crystalline structures

    • density

    • preparation of the source polymer

No bulk system is generated during Part 1.

We first establish the scientific concepts before constructing the condensed
polymer material.

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
print("Tutorial 05 - Constructing Bulk Polymer Systems")
print("Part 1 - Understanding Bulk Polymer Materials")
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

✓ Tutorial 04B

    Building a solvated single-chain system

✓ Tutorial 04C

    Building a solvated single-chain system with ions


Current tutorial

► Tutorial 05

    Constructing bulk polymer systems


Upcoming tutorials

□ Tutorial 06

    Understanding md_systems.csv

□ Tutorial 07

    Creating an OpenMM workflow
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
Unlike the previous tutorials, we are no longer preparing an environment
around a single polymer chain.

Instead, we will construct a condensed material containing many interacting
polymer chains.

The completed system consists of

        Many polymer chains

                +

        One periodic simulation box

                +

        A condensed polymer phase

This system is intended to represent the bulk polymer rather than an isolated
molecule.
"""
)


# %% ==========================================================================
# Why isn't one polymer enough?
# ==============================================================================

print("\n")
print("=" * 80)
print("WHY ISN'T ONE POLYMER ENOUGH?")
print("=" * 80)

print(
"""
An isolated polymer chain can reveal a great deal about its own molecular
structure.

For example, we can investigate

    • chain flexibility

    • molecular geometry

    • radius of gyration

    • solvent interactions

However, many experimentally measured material properties arise from
interactions between neighbouring polymer chains.

These include

    • density

    • glass transition temperature

    • free volume

    • chain packing

    • oxygen diffusion

    • thermal expansion

These properties cannot be measured from an isolated polymer because they are
collective properties of the material rather than individual molecules.
"""
)


# %% ==========================================================================
# Emergent properties
# ==============================================================================

print("\n")
print("=" * 80)
print("EMERGENT MATERIAL PROPERTIES")
print("=" * 80)

print(
"""
Some properties only emerge when many molecules interact together.

For example

Property                          One chain    Many chains

Radius of gyration                   ✓             ✓

Hydration                            ✓             ✓

Chain flexibility                    ✓             ✓

Density                              ✗             ✓

Glass transition                     ✗             ✓

Free volume                          ✗             ✓

Chain entanglement                   ✗             ✓

Bulk diffusion                       ✗             ✓

This distinction is one of the central ideas in molecular simulation.

Many technologically important material properties are emergent rather than
molecular.
"""
)


# %% ==========================================================================
# What is a polymer melt?
# ==============================================================================

print("\n")
print("=" * 80)
print("WHAT IS A POLYMER MELT?")
print("=" * 80)

print(
"""
A polymer melt is a condensed phase consisting almost entirely of polymer
chains.

Unlike the solvated systems introduced previously,

there is

    no water

    no ions

The available volume is almost completely occupied by polymer molecules.

Above the glass transition temperature the chains possess sufficient mobility
to rearrange continuously, producing the characteristic behaviour of a melt.

Polymer melts provide the starting point for many simulations investigating
bulk thermal and mechanical properties.
"""
)


# %% ==========================================================================
# Amorphous and crystalline materials
# ==============================================================================

print("\n")
print("=" * 80)
print("AMORPHOUS AND CRYSTALLINE POLYMERS")
print("=" * 80)

print(
"""
Polymer chains can be arranged in different ways.

Amorphous materials

    Chains are arranged without long-range order.

    This is typical for many polymer melts and glasses.


Crystalline materials

    Chains adopt a more ordered arrangement.

    Regular packing often produces increased density and different mechanical
    behaviour.

Throughout this tutorial we will begin with an amorphous polymer melt because
it provides a suitable starting point for many molecular dynamics studies.
"""
)


# %% ==========================================================================
# Density
# ==============================================================================

print("\n")
print("=" * 80)
print("POLYMER DENSITY")
print("=" * 80)

print(
"""
Unlike previous tutorials, density now becomes one of the most important
system preparation parameters.

Conceptually,

more polymer

inside the same volume

produces

higher density.

Conversely,

the same polymer

inside a larger box

produces

lower density.

During bulk system preparation we specify a target density, allowing the
simulation box dimensions to be chosen automatically.
"""
)


# %% ==========================================================================
# Periodic condensed phases
# ==============================================================================

print("\n")
print("=" * 80)
print("PERIODIC CONDENSED PHASES")
print("=" * 80)

print(
"""
Periodic boundary conditions are especially important for condensed polymer
systems.

Rather than representing a small isolated collection of polymer chains, the
simulation box becomes one repeating unit within an effectively infinite
material.

Every polymer chain therefore interacts not only with neighbouring chains
inside the simulation box but also with periodic images surrounding it.

This greatly reduces edge effects and allows relatively small molecular
systems to approximate much larger bulk materials.
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

NUMBER_OF_CHAINS = 25

TARGET_DENSITY = 0.75

STARTING_CONFIGURATION = "amorphous"

OVERWRITE = False

RUN_BUILD = False

print(f"Polymer                : {POLYMER_NAME}")
print(f"Number of chains       : {NUMBER_OF_CHAINS}")
print(f"Target density (g/cm³) : {TARGET_DENSITY}")
print(f"Starting configuration : {STARTING_CONFIGURATION}")
print(f"Build system           : {RUN_BUILD}")


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

identifies the finite polymer that will be duplicated.

NUMBER_OF_CHAINS

    {NUMBER_OF_CHAINS}

determines how many polymer molecules will be packed into the simulation box.

TARGET_DENSITY

    {TARGET_DENSITY} g/cm³

defines the initial density of the condensed material.

STARTING_CONFIGURATION

    {STARTING_CONFIGURATION}

selects how the polymer chains will initially be arranged.

RUN_BUILD

is a tutorial safety switch.

No polymer melt will be generated during Part 1.
""")


# %% ==========================================================================
# Locating the source polymer
# ==============================================================================

print("\n")
print("=" * 80)
print("LOCATING THE SOURCE POLYMER")
print("=" * 80)

print(
"""
The bulk polymer system begins with the finite polymer prepared in
Tutorial 02.

This polymer will be duplicated repeatedly until the requested number of
chains has been generated.

The original polymer itself is never modified.

Instead, it serves as the molecular building block for the condensed
material.
"""
)


# %% ==========================================================================
# Preparing for bulk system construction
# ==============================================================================

print("\n")
print("=" * 80)
print("PREPARING FOR BULK SYSTEM CONSTRUCTION")
print("=" * 80)

print(
"""
Before constructing the polymer melt, the system builder prepares the
required information.

Conceptually this consists of

    locating the polymer

            │

            ▼

    duplicating the chain

            │

            ▼

    selecting the number of chains

            │

            ▼

    choosing the target density

            │

            ▼

    defining the simulation box

Only after these inputs have been verified is the system ready for bulk
construction.
"""
)


# %% ==========================================================================
# Behind the scenes
# ==============================================================================

print("\n")
print("=" * 80)
print("BEHIND THE SCENES - PREPARING A BULK POLYMER")
print("=" * 80)

print(
"""
Unlike the previous tutorials, the environment surrounding the polymer is no
longer changing.

Instead, the molecular system itself is becoming larger.

Preparation confirms

✓ the finite polymer exists

✓ the requested number of chains is sensible

✓ the target density has been specified

✓ the starting configuration is recognised

✓ sufficient information exists to construct the condensed material

At this stage, no additional polymer chains have been generated.

In Part 2 we will duplicate the finite polymer, arrange many interacting
chains inside a periodic simulation box, and construct our first bulk polymer
system.
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
In this section we introduced the concepts underlying bulk polymer
simulations.

We learned that

✓ many material properties emerge only through interactions between polymer
  chains

✓ polymer melts contain many interacting molecules rather than a single chain

✓ density becomes a key system preparation parameter

✓ periodic boundary conditions allow finite simulations to represent bulk
  materials

✓ bulk system construction begins with the validated finite polymer created
  earlier in the course

In Part 2 we will duplicate the polymer, pack many chains into a periodic
simulation box, and generate our first bulk polymer material suitable for
molecular dynamics simulations.
"""
)

print("\nTutorial 05 Part 1 complete.")

# %% ==========================================================================
# Tutorial 05 - Part 2
# Constructing a Bulk Polymer System
# ==============================================================================

print("\n")
print("=" * 80)
print("TUTORIAL 05 - PART 2")
print("CONSTRUCTING A BULK POLYMER SYSTEM")
print("=" * 80)

print(
"""
In Part 1 we introduced the scientific motivation for constructing bulk
polymer systems.

We learned that many important material properties emerge only when multiple
polymer chains interact within a condensed phase.

We are now ready to construct our first bulk polymer material.

Conceptually, the preparation workflow is

        Finite polymer

                │

                ▼

      Duplicate polymer

                │

                ▼

     Create many chains

                │

                ▼

   Randomly arrange chains

                │

                ▼

     Define simulation box

                │

                ▼

     Generate bulk system

                │

                ▼

     Register new material

By the end of this section we will have created an initial bulk polymer
configuration ready for validation.
"""
)


# %% ==========================================================================
# Initialising the material builder
# ==============================================================================

print("\n")
print("=" * 80)
print("INITIALISING THE MATERIAL BUILDER")
print("=" * 80)

try:

    from src.iphasimulator.md_system_builder import MDSystemBuilder

    material_builder = MDSystemBuilder(
        file_manager=paths,
    )

    print("✓ Bulk material builder initialised.")

except Exception as error:

    material_builder = None

    print(error)

    print(
"""
Update the import so that it matches the public API used by the current
version of iPHAsimulator.
"""
    )


# %% ==========================================================================
# Defining the material
# ==============================================================================

print("\n")
print("=" * 80)
print("DEFINING THE BULK MATERIAL")
print("=" * 80)

SYSTEM_NAME = (
    f"{NUMBER_OF_CHAINS}_{POLYMER_NAME}_{STARTING_CONFIGURATION}"
)

print(f"Polymer              : {POLYMER_NAME}")
print(f"Number of chains     : {NUMBER_OF_CHAINS}")
print(f"Target density       : {TARGET_DENSITY} g/cm³")
print(f"Configuration        : {STARTING_CONFIGURATION}")

print(f"Material name        : {SYSTEM_NAME}")


# %% ==========================================================================
# The construction request
# ==============================================================================

print("\n")
print("=" * 80)
print("CONSTRUCTION REQUEST")
print("=" * 80)

print(
"""
The bulk system builder requires several pieces of information.

Which polymer should be duplicated?

        P3HB_10

How many copies are required?

        25 chains

How densely should they be packed?

        0.75 g/cm³

How should the chains be arranged?

        Amorphous

Once these questions have been answered the material construction can begin.
"""
)


# %% ==========================================================================
# Generate the bulk polymer system
# ==============================================================================

print("\n")
print("=" * 80)
print("GENERATING THE BULK MATERIAL")
print("=" * 80)

bulk_result = None

if RUN_BUILD and material_builder is not None:

    bulk_result = (

        material_builder.build_polymer_melt(

            polymer_name=POLYMER_NAME,

            number_of_chains=NUMBER_OF_CHAINS,

            target_density=TARGET_DENSITY,

            starting_configuration=STARTING_CONFIGURATION,

            overwrite=OVERWRITE,

        )

    )

    print("✓ Bulk polymer system generated.")

else:

    print(
"""
RUN_BUILD is False.

No molecular files have been modified.

Enable the execution switch after reviewing the settings.
"""
    )


# %% ==========================================================================
# Behind the scenes
# ==============================================================================

print("\n")
print("=" * 80)
print("BEHIND THE SCENES - BUILDING A BULK MATERIAL")
print("=" * 80)

print(
"""
Although construction appears to consist of a single function call,
multiple preparation stages occur internally.

        Read polymer

               │

               ▼

      Duplicate chain

               │

               ▼

 Generate requested copies

               │

               ▼

 Randomly orient chains

               │

               ▼

 Randomly position chains

               │

               ▼

 Determine simulation box

               │

               ▼

 Write molecular files

               │

               ▼

 Register material

The resulting configuration provides the starting point for subsequent
energy minimisation and equilibration.
"""
)


# %% ==========================================================================
# Duplicating the polymer
# ==============================================================================

print("\n")
print("=" * 80)
print("DUPLICATING THE POLYMER")
print("=" * 80)

print(
"""
The finite polymer prepared in Tutorial 02 acts as a molecular building
block.

Rather than creating new polymer chemistry, iPHAsimulator duplicates the
validated polymer repeatedly until the requested number of chains has been
generated.

For this example

        One polymer

                │

                ▼

        Twenty-five polymers

Each chain is chemically identical.

Only its position and orientation within the simulation box differ.
"""
)


# %% ==========================================================================
# Multiple chains are not one long chain
# ==============================================================================

print("\n")
print("=" * 80)
print("MANY CHAINS ARE NOT ONE LONG CHAIN")
print("=" * 80)

print(
"""
It is important to distinguish between

    Twenty-five 10-mer chains

and

    One 250-mer chain

These systems are fundamentally different.

Twenty-five independent chains

    • diffuse independently

    • interact with neighbouring chains

    • form interfaces

    • generate free volume

A single long chain cannot reproduce these collective interactions.

Consequently, many short chains are generally required when modelling bulk
polymer materials.
"""
)


# %% ==========================================================================
# Random orientation
# ==============================================================================

print("\n")
print("=" * 80)
print("RANDOM ORIENTATION")
print("=" * 80)

print(
"""
Each polymer chain is assigned an independent orientation before packing.

This avoids introducing artificial alignment into the initial structure.

Conceptually

Chain A

        →

Chain B

      ↗

Chain C

        ↓

Chain D

      ↖

Random orientations provide a more suitable starting point for generating an
amorphous material.
"""
)


# %% ==========================================================================
# Packing the chains
# ==============================================================================

print("\n")
print("=" * 80)
print("PACKING THE CHAINS")
print("=" * 80)

print(
"""
The polymer chains are then positioned throughout the simulation box.

Initially, the objective is simply to generate a physically reasonable
starting arrangement.

At this stage

✓ chains are present

✓ the target density is approximated

✓ periodic boundary conditions are defined

The molecular configuration will be refined during subsequent energy
minimisation and equilibration.
"""
)


# %% ==========================================================================
# Target density
# ==============================================================================

print("\n")
print("=" * 80)
print("TARGET DENSITY")
print("=" * 80)

print(
"""
The requested density determines the size of the simulation box.

Higher target density

        ↓

Smaller simulation box

Lower target density

        ↓

Larger simulation box

The density selected here represents the initial packing density.

The final density will be established naturally during molecular dynamics
equilibration.
"""
)


# %% ==========================================================================
# Initial overlaps
# ==============================================================================

print("\n")
print("=" * 80)
print("INITIAL OVERLAPS")
print("=" * 80)

print(
"""
Unlike the solvent preparation tutorials, slight steric overlaps between
polymer chains may exist in the initial configuration.

This is expected.

The purpose of the builder is to generate a sensible starting structure,
not a fully relaxed material.

Energy minimisation removes unfavourable contacts before the production
simulation begins.

Users should therefore not be concerned if the initial configuration appears
slightly crowded.
"""
)


# %% ==========================================================================
# Generated files
# ==============================================================================

print("\n")
print("=" * 80)
print("GENERATED FILES")
print("=" * 80)

print(
"""
The completed bulk material contains

Amber

    topology

    coordinates

GROMACS

    topology

    coordinates

Metadata

    registry information

These files describe the complete condensed polymer system and provide the
starting point for molecular dynamics simulations.
"""
)


# %% ==========================================================================
# Registering the material
# ==============================================================================

print("\n")
print("=" * 80)
print("REGISTERING THE BULK SYSTEM")
print("=" * 80)

print(
"""
The completed material is registered within the molecular system database.

The registry records

    • polymer identity

    • number of chains

    • target density

    • starting configuration

    • simulation files

Future simulation workflows can therefore identify and reuse the prepared
material automatically.
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
During this section we constructed an initial bulk polymer material.

We learned that

✓ the finite polymer is duplicated repeatedly

✓ many polymer chains interact within one periodic simulation box

✓ random orientations reduce artificial ordering

✓ the target density determines the initial box dimensions

✓ the resulting configuration is an initial structure rather than an
  equilibrated polymer melt

✓ the completed material is written to disk and registered

In Part 3 we will validate the bulk polymer system by examining chain counts,
chain lengths, density, periodic boundaries and the overall structure of the
prepared material.
"""
)

print("\nTutorial 05 Part 2 complete.")

# %% ==========================================================================
# Tutorial 05 - Part 3
# Validating the Bulk Polymer Material
# ==============================================================================

print("\n")
print("=" * 80)
print("TUTORIAL 05 - PART 3")
print("VALIDATING THE BULK POLYMER MATERIAL")
print("=" * 80)

print(
"""
The initial bulk polymer configuration has now been generated.

Before beginning molecular dynamics we should confirm that the prepared
material is chemically and structurally consistent.

Unlike the previous tutorials, validation now focuses on the polymer
material as a whole rather than individual molecules.

In this section we will verify

    • the molecular topology

    • polymer chain count

    • chain lengths

    • residue composition

    • atom counts

    • simulation box

    • estimated density

    • overall packing

Once these checks have passed, the material is ready for energy
minimisation and equilibration.
"""
)


# %% ==========================================================================
# Loading the material
# ==============================================================================

print("\n")
print("=" * 80)
print("LOADING THE BULK MATERIAL")
print("=" * 80)

try:

    from openmm.app import AmberPrmtopFile
    from openmm.app import AmberInpcrdFile

    prmtop = AmberPrmtopFile(str(prepared_prmtop))
    inpcrd = AmberInpcrdFile(str(prepared_rst7))

    topology = prmtop.topology

    print("✓ Bulk material loaded successfully.")

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

atoms = list(topology.atoms())
residues = list(topology.residues())
chains = list(topology.chains())

print(f"Atoms      : {len(atoms)}")
print(f"Residues   : {len(residues)}")
print(f"Chains     : {len(chains)}")


# %% ==========================================================================
# Polymer chain count
# ==============================================================================

print("\n")
print("=" * 80)
print("POLYMER CHAIN COUNT")
print("=" * 80)

print(f"Requested chains : {NUMBER_OF_CHAINS}")
print(f"Detected chains  : {len(chains)}")

if len(chains) == NUMBER_OF_CHAINS:

    print("\n✓ Correct number of polymer chains detected.")

else:

    print("\n⚠ Unexpected chain count detected.")


# %% ==========================================================================
# Chain lengths
# ==============================================================================

print("\n")
print("=" * 80)
print("CHAIN LENGTHS")
print("=" * 80)

chain_lengths = []

for chain in chains:

    residues_in_chain = list(chain.residues())

    chain_lengths.append(len(residues_in_chain))

print(f"Minimum residues : {min(chain_lengths)}")
print(f"Maximum residues : {max(chain_lengths)}")
print(f"Average residues : {sum(chain_lengths)/len(chain_lengths):.1f}")

print()

print(
"""
For a monodisperse polymer melt every chain should contain the same number
of repeat units.

Future tutorials will introduce polydisperse systems where chain lengths
vary intentionally.
"""
)


# %% ==========================================================================
# Residue composition
# ==============================================================================

print("\n")
print("=" * 80)
print("RESIDUE COMPOSITION")
print("=" * 80)

residue_names = {}

for residue in residues:

    residue_names.setdefault(residue.name, 0)

    residue_names[residue.name] += 1

for name in sorted(residue_names):

    print(f"{name:10s} {residue_names[name]}")


# %% ==========================================================================
# Simulation box
# ==============================================================================

print("\n")
print("=" * 80)
print("SIMULATION BOX")
print("=" * 80)

print(
"""
The periodic simulation box defines one repeating unit of the bulk material.

Every polymer chain interacts with neighbouring chains both inside the box
and across the periodic boundaries.

Correct box dimensions are therefore essential for realistic condensed-phase
simulations.
"""
)


# %% ==========================================================================
# Density
# ==============================================================================

print("\n")
print("=" * 80)
print("INITIAL DENSITY")
print("=" * 80)

print(f"Requested density : {TARGET_DENSITY:.3f} g/cm³")

print()

print(
"""
The builder selects the simulation box dimensions to approximate the
requested initial density.

Following energy minimisation and equilibration the density will normally
change slightly as the polymer chains relax into a lower-energy
configuration.

This behaviour is expected.
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
When viewing the prepared material you should observe

✓ many polymer chains

✓ random orientations

✓ no obvious long-range ordering

✓ a condensed polymer phase

✓ periodic packing

The initial structure may appear crowded and neighbouring chains may be
extremely close together.

This is expected for an unequilibrated bulk polymer configuration.
"""
)


# %% ==========================================================================
# Initial configuration versus equilibrated material
# ==============================================================================

print("\n")
print("=" * 80)
print("INITIAL CONFIGURATION ≠ EQUILIBRATED MATERIAL")
print("=" * 80)

print(
"""
One of the most important concepts in molecular simulation is recognising
that the generated coordinates are only an initial configuration.

Construction software cannot determine the equilibrium arrangement of
millions of atomic interactions.

Instead, it generates a physically sensible starting point.

Subsequent molecular dynamics will

    • remove steric clashes

    • relax polymer conformations

    • establish equilibrium density

    • generate realistic chain packing

The polymer melt is therefore created by molecular dynamics, not by the
builder itself.
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
The completed registry entry should include

    • polymer identity

    • chain length

    • number of chains

    • target density

    • starting configuration

    • generated molecular files

This allows future simulation workflows to locate and reuse the prepared
bulk material automatically.
"""
)


# %% ==========================================================================
# Behind the scenes
# ==============================================================================

print("\n")
print("=" * 80)
print("BEHIND THE SCENES - VALIDATING A MATERIAL")
print("=" * 80)

print(
"""
Validation now occurs at two different levels.

                 Molecules

                     ✓

             Polymer chains

                     ✓

          Bulk material properties

                     ✓

Rather than asking

    "Does the polymer exist?"

we now ask

    "Does this collection of polymers represent a sensible condensed
     material?"

This shift from molecular validation to material validation is one of the
major conceptual changes introduced in Tutorial 05.
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

    "Topology loaded":
        topology is not None,

    "Correct chain count":
        len(chains) == NUMBER_OF_CHAINS,

    "Chains detected":
        len(chains) > 0,

    "Residues detected":
        len(residues) > 0,

    "Atoms detected":
        len(atoms) > 0,

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
The bulk polymer material has now been validated.

We confirmed

✓ the molecular topology loads correctly

✓ the correct number of polymer chains was generated

✓ chain lengths are consistent

✓ residue and atom counts are sensible

✓ the simulation box has been defined

✓ the requested initial density has been applied

✓ the prepared material is suitable for molecular dynamics

Most importantly, we established that this structure represents an initial
configuration rather than an equilibrated polymer melt.

In Part 4 we will explore the scientific applications of bulk polymer
simulations and discuss how collective interactions between polymer chains
give rise to experimentally measurable material properties.
"""
)

print("\nTutorial 05 Part 3 complete.")

# %% ==========================================================================
# Tutorial 05 - Part 4
# Understanding Bulk Polymer Materials
# ==============================================================================

print("\n")
print("=" * 80)
print("TUTORIAL 05 - PART 4")
print("UNDERSTANDING BULK POLYMER MATERIALS")
print("=" * 80)

print(
"""
Congratulations!

You have now constructed your first bulk polymer material.

This marks an important milestone in the course.

For the first time we are no longer studying an individual polymer molecule.

Instead, we are studying a material composed of many interacting polymer
chains.

This change allows us to investigate properties that emerge only through
collective molecular behaviour.

The completed material consists of

        Many polymer chains

                +

        One periodic simulation box

                +

        A condensed polymer phase

                +

        A complete molecular force field

Although the structure is not yet equilibrated, it provides the starting
point for realistic molecular dynamics simulations of bulk polymers.
"""
)


# %% ==========================================================================
# Why bulk materials matter
# ==============================================================================

print("\n")
print("=" * 80)
print("WHY BULK MATERIALS MATTER")
print("=" * 80)

print(
"""
Many experimental measurements describe materials rather than individual
molecules.

Examples include

    • density

    • glass transition temperature

    • thermal expansion

    • oxygen permeability

    • mechanical properties

    • free volume

    • chain entanglement

None of these properties belong to an isolated polymer chain.

Instead, they emerge from interactions between many neighbouring chains.

Bulk molecular dynamics simulations allow these interactions to develop
naturally over time.
"""
)


# %% ==========================================================================
# Scientific applications
# ==============================================================================

print("\n")
print("=" * 80)
print("SCIENTIFIC APPLICATIONS")
print("=" * 80)

applications = [

    (
        "Glass transition",
        "Determine how polymer density changes with temperature."
    ),

    (
        "Density",
        "Predict equilibrium densities and compare with experiment."
    ),

    (
        "Thermal expansion",
        "Measure volume changes during heating and cooling."
    ),

    (
        "Chain packing",
        "Investigate how polymer molecules occupy space."
    ),

    (
        "Free volume",
        "Study microscopic voids throughout the material."
    ),

    (
        "Diffusion",
        "Measure the movement of gases and small molecules through polymers."
    ),

    (
        "Mechanical behaviour",
        "Provide atomistic insight into polymer structure before larger-scale mechanical models."
    ),

]

for title, description in applications:

    print(f"\n{title}")
    print("-" * len(title))
    print(description)


# %% ==========================================================================
# Emergent behaviour
# ==============================================================================

print("\n")
print("=" * 80)
print("EMERGENT BEHAVIOUR")
print("=" * 80)

print(
"""
Perhaps the most important idea introduced in this tutorial is emergence.

Individual polymer chains possess molecular properties.

Collections of polymer chains possess material properties.

For example

One chain

    Radius of gyration

    Molecular flexibility

    Intramolecular structure

Many chains

    Density

    Free volume

    Glass transition

    Chain entanglement

    Bulk diffusion

These material properties arise naturally from millions of interactions
between neighbouring molecules during molecular dynamics simulations.
"""
)


# %% ==========================================================================
# Comparing all prepared systems
# ==============================================================================

print("\n")
print("=" * 80)
print("COMPARING THE PREPARED SYSTEMS")
print("=" * 80)

comparison = [

    ("Single polymer",          "✓", "✓", "✓", "✓"),

    ("Explicit water",          "✗", "✓", "✓", "✗"),

    ("Dissolved ions",          "✗", "✗", "✓", "✗"),

    ("Many polymer chains",     "✗", "✗", "✗", "✓"),

    ("Bulk properties",         "✗", "✗", "✗", "✓"),

    ("Glass transition",        "✗", "✗", "✗", "✓"),

    ("Chain entanglement",      "✗", "✗", "✗", "✓"),

]

print(
f"{'Property':<30}"
f"{'Dry':<10}"
f"{'Water':<10}"
f"{'Ions':<10}"
f"{'Bulk'}"
)

print("-" * 75)

for row in comparison:

    print(
        f"{row[0]:<30}"
        f"{row[1]:<10}"
        f"{row[2]:<10}"
        f"{row[3]:<10}"
        f"{row[4]}"
    )


# %% ==========================================================================
# Preparation versus simulation
# ==============================================================================

print("\n")
print("=" * 80)
print("PREPARATION VERSUS SIMULATION")
print("=" * 80)

print(
"""
Constructing the material is only the first stage.

The generated coordinates are an initial configuration.

The molecular dynamics simulation is responsible for transforming this
initial structure into a realistic polymer melt.

The typical workflow is

    Initial configuration

            │

            ▼

    Energy minimisation

            │

            ▼

      Equilibration

            │

            ▼

     Production simulation

            │

            ▼

     Material properties

Preparation defines the system.

Molecular dynamics generates the physics.
"""
)


# %% ==========================================================================
# Behind the scenes
# ==============================================================================

print("\n")
print("=" * 80)
print("BEHIND THE SCENES - FROM MOLECULES TO MATERIALS")
print("=" * 80)

print(
"""
The philosophy of iPHAsimulator is highly modular.

                SMILES

                   │

                   ▼

        Parameterised polymer

                   │

                   ▼

          Finite polymer

                   │

        ┌──────────┴──────────┐
        │                     │

        ▼                     ▼

 Single-chain systems     Bulk materials

                                   │

                                   ▼

                     Molecular dynamics

                                   │

                                   ▼

                        Material properties

Notice that the polymer chemistry is generated only once.

Everything that follows simply places that validated polymer into different
scientifically relevant environments.
"""
)


# %% ==========================================================================
# The complete preparation workflow
# ==============================================================================

print("\n")
print("=" * 80)
print("THE COMPLETE PREPARATION WORKFLOW")
print("=" * 80)

print(
"""
Across Tutorials 00–05 we have built an increasingly sophisticated workflow.

        Monomer SMILES

                │

                ▼

    Parameterise chemistry

                │

                ▼

     Generate residues

                │

                ▼

      Build polymer

                │

        ┌───────┴────────┐
        │                │

        ▼                ▼

 Single-chain      Bulk material

   systems

At this point every major molecular system required for subsequent molecular
dynamics simulations has been prepared.
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

Why can't a single isolated polymer chain be used to determine the glass
transition temperature?

2.

Why is a collection of twenty-five 10-mer chains different from one 250-mer
chain?

3.

Why is the generated bulk configuration not immediately suitable for
production molecular dynamics?

4.

Which stage of the workflow establishes the equilibrium density of the
material?

5.

Which experimentally measurable properties require a bulk polymer system?

Take a few moments to answer each question before continuing.
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

The glass transition is a collective property that depends on interactions
between many polymer chains.

2.

Many shorter chains can diffuse, pack and interact with neighbouring chains,
whereas one very long chain cannot reproduce the same intermolecular
behaviour.

3.

The prepared coordinates are only an initial configuration. Molecular
dynamics is required to remove steric clashes and establish equilibrium.

4.

The equilibration stage of molecular dynamics.

5.

Examples include density, glass transition temperature, thermal expansion,
chain entanglement, free volume and diffusion through the material.
"""
)


# %% ==========================================================================
# Tutorial summary
# ==============================================================================

print("\n")
print("=" * 80)
print("TUTORIAL 05 SUMMARY")
print("=" * 80)

print(
"""
Congratulations!

You have successfully constructed your first bulk polymer material.

During this tutorial you

✓ learned why bulk systems are required

✓ explored emergent material properties

✓ constructed an initial condensed polymer configuration

✓ validated the bulk material

✓ distinguished between an initial configuration and an equilibrated polymer
  melt

You are now ready to begin molecular dynamics simulations of realistic bulk
polymer systems.

The following tutorials shift from preparing molecular systems to performing
and analysing molecular dynamics simulations.
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
Until now we have focused on preparing molecular systems.

The next stage is to simulate them.

In Tutorial 06 we will explore the md_systems.csv database and learn how
iPHAsimulator keeps track of every prepared molecular system.

Understanding this registry is essential because it allows simulation
workflows to locate systems automatically, ensuring that preparation,
simulation and analysis remain fully reproducible.

From there, we will begin creating complete molecular dynamics workflows
using the systems you have prepared throughout this course.
"""
)

print("\nTutorial 05 complete.")