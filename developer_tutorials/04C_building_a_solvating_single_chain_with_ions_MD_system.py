#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
===============================================================================
Tutorial 04C - Building a Solvated Single-Chain Molecular Dynamics System
with Ions

Part 1 - Understanding Ionic Solutions and Preparing the Inputs
===============================================================================

In Tutorial 04A we prepared a polymer inside an empty periodic simulation box.

In Tutorial 04B we surrounded that polymer with explicit water molecules to
create a realistic aqueous environment.

In this tutorial we take the next step by introducing dissolved ions into the
solution.

Many experimental systems are not composed of pure water.

Instead, they contain dissolved salts that influence molecular behaviour
through electrostatic interactions and changes to the solution environment.

The preparation workflow is

        Solvated polymer

               │

               ▼

      Validate solvated system

               │

               ▼

      Choose ion species

               │

               ▼

     Specify concentration

               │

               ▼

      Calculate ion numbers

               │

               ▼

      Replace water molecules

               │

               ▼

       Register new system

By the end of Tutorial 04C we will have produced a realistic electrolyte
solution suitable for molecular dynamics simulations.

In Part 1 we will introduce

    • why ions are added

    • common electrolyte solutions

    • ionic concentration

    • charge neutrality

    • preparation of the solvated source system

No ions are added during Part 1.

We first establish the concepts required before constructing an ionic
molecular dynamics system.

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
print("Tutorial 04C - Building a Solvated Single-Chain System with Ions")
print("Part 1 - Understanding Ionic Solutions")
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


Current tutorial

► Tutorial 04C

    Building a solvated single-chain system with ions


Upcoming tutorial

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
The molecular system now consists of

        One polymer chain

                +

        Thousands of water molecules

                +

        Dissolved ions

                +

        One periodic simulation box

Unlike Tutorial 04B, the solvent no longer contains only water.

A small number of water molecules will be replaced by positively and
negatively charged ions.

Although ions usually represent only a tiny fraction of the atoms present,
they can significantly influence molecular behaviour.
"""
)


# %% ==========================================================================
# Why add ions?
# ==============================================================================

print("\n")
print("=" * 80)
print("WHY ADD IONS?")
print("=" * 80)

print(
"""
Very few real solutions consist of perfectly pure water.

Instead, dissolved salts are almost always present.

Examples include

    • laboratory buffer solutions

    • physiological fluids

    • seawater

    • electrochemical electrolytes

    • corrosion environments

    • industrial process streams

Dissolved ions influence the behaviour of nearby molecules through
electrostatic interactions.

These interactions can affect

    • polymer conformation

    • hydrogen bonding

    • molecular diffusion

    • solution structure

    • intermolecular interactions

Including ions therefore produces a simulation environment that more closely
resembles many experimental conditions.
"""
)


# %% ==========================================================================
# What are ions?
# ==============================================================================

print("\n")
print("=" * 80)
print("WHAT ARE IONS?")
print("=" * 80)

print(
"""
An ion is an atom or molecule that carries an electrical charge.

Positive ions (cations)

    Na+

    K+

    Ca2+

    Mg2+

Negative ions (anions)

    Cl-

    Br-

    F-

These charged particles move independently throughout the solution and
interact continuously with water molecules and the polymer.
"""
)


# %% ==========================================================================
# Electrolytes
# ==============================================================================

print("\n")
print("=" * 80)
print("ELECTROLYTE SOLUTIONS")
print("=" * 80)

print(
"""
Many salts dissociate into ions when dissolved in water.

For example

        NaCl

            │

            ▼

      Na+      +      Cl-

Similarly

        KCl

            │

            ▼

      K+       +      Cl-

The resulting mixture of water and dissolved ions is known as an electrolyte
solution.

Throughout this tutorial we will use potassium chloride (KCl) as an example,
although iPHAsimulator can support different ion species.
"""
)


# %% ==========================================================================
# Ionic concentration
# ==============================================================================

print("\n")
print("=" * 80)
print("ION CONCENTRATION")
print("=" * 80)

print(
"""
The amount of dissolved salt is usually described using concentration.

Typical units include

    mol/L

    mM

    M

Examples

Pure water

    ~0 M

Laboratory buffer

    0.05–0.20 M

Physiological saline

    ~0.15 M

Seawater

    ~0.60 M

Higher concentrations correspond to larger numbers of ions within the
simulation box.
"""
)


# %% ==========================================================================
# Charge neutrality
# ==============================================================================

print("\n")
print("=" * 80)
print("CHARGE NEUTRALITY")
print("=" * 80)

print(
"""
Most molecular dynamics simulations are constructed to have an overall net
charge close to zero.

For a neutral polymer this is straightforward.

For example

        Add

        25 K+

            +

        25 Cl-

The positive and negative charges cancel, producing a neutral electrolyte
solution.

Maintaining charge neutrality improves the physical realism of the simulation
and is generally recommended for periodic molecular dynamics systems.
"""
)


# %% ==========================================================================
# User settings
# ==============================================================================

print("\n")
print("=" * 80)
print("USER SETTINGS")
print("=" * 80)

SYSTEM_NAME = "P3HB_10_solvated"

ION_TYPE = "KCl"

ION_CONCENTRATION = 0.15

OVERWRITE = False

RUN_ION_BUILD = False

print(f"Source system      : {SYSTEM_NAME}")
print(f"Ion species        : {ION_TYPE}")
print(f"Concentration (M)  : {ION_CONCENTRATION}")
print(f"Overwrite outputs  : {OVERWRITE}")
print(f"Build ionic system : {RUN_ION_BUILD}")


# %% ==========================================================================
# Interpreting the settings
# ==============================================================================

print("\n")
print("=" * 80)
print("INTERPRETING THE SETTINGS")
print("=" * 80)

print(f"""
SYSTEM_NAME

    {SYSTEM_NAME}

identifies the solvated molecular system prepared in Tutorial 04B.

ION_TYPE

    {ION_TYPE}

defines the electrolyte that will be added.

ION_CONCENTRATION

    {ION_CONCENTRATION} M

specifies the desired salt concentration within the simulation box.

RUN_ION_BUILD

is a tutorial safety switch.

No ions will be added during Part 1.
""")


# %% ==========================================================================
# Locating the solvated system
# ==============================================================================

print("\n")
print("=" * 80)
print("LOCATING THE SOURCE SYSTEM")
print("=" * 80)

print(
"""
Before ions can be introduced, the previously prepared solvated molecular
system must be located.

This system already contains

    ✓ polymer

    ✓ explicit water

    ✓ periodic box

Tutorial 04C builds directly upon this validated system rather than starting
from the polymer again.
"""
)


# %% ==========================================================================
# Preparing for ion insertion
# ==============================================================================

print("\n")
print("=" * 80)
print("PREPARING FOR ION INSERTION")
print("=" * 80)

print(
"""
Before any ions can be added, the system builder gathers the information
required to construct the electrolyte solution.

At a high level this consists of

    locating the solvated system

            │

            ▼

    reading the topology

            │

            ▼

    reading the coordinates

            │

            ▼

    measuring the simulation box

            │

            ▼

    determining the required ion numbers

Only after these inputs have been verified is the system ready for ion
insertion.
"""
)


# %% ==========================================================================
# Behind the scenes
# ==============================================================================

print("\n")
print("=" * 80)
print("BEHIND THE SCENES - PREPARING THE IONIC SYSTEM")
print("=" * 80)

print(
"""
Unlike solvation, ion insertion begins with an already complete aqueous
system.

The preparation stage confirms

✓ the solvated system exists

✓ topology files can be located

✓ coordinate files can be read

✓ the simulation box dimensions are available

✓ the requested electrolyte is recognised

At this stage, the molecular system has not been modified.

The polymer and water remain exactly as they were generated in Tutorial 04B.

In Part 2 we will calculate the number of ions required and construct the
complete electrolyte solution.
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
In this section we introduced ionic molecular dynamics systems and prepared
the information required to add dissolved ions.

We learned that

✓ most real solutions contain dissolved salts

✓ ions interact continuously with water and the polymer

✓ electrolyte concentration determines how many ions are added

✓ charge neutrality is an important consideration in molecular dynamics

✓ Tutorial 04C begins from the validated solvated system created in
  Tutorial 04B

In Part 2 we will calculate the required number of ions, replace selected
water molecules, and generate a complete electrolyte molecular dynamics
system.
"""
)

print("\nTutorial 04C Part 1 complete.")

# %% ==========================================================================
# Tutorial 04C - Part 2
# Constructing the Ionic Molecular Dynamics System
# ==============================================================================

print("\n")
print("=" * 80)
print("TUTORIAL 04C - PART 2")
print("CONSTRUCTING THE IONIC MOLECULAR DYNAMICS SYSTEM")
print("=" * 80)

print(
"""
In Part 1 we introduced electrolyte solutions and prepared the information
required to construct an ionic molecular dynamics system.

The source solvated system has already been validated.

The electrolyte has been selected.

The desired concentration has been specified.

We are now ready to introduce dissolved ions into the simulation box.

Conceptually, the workflow is

        Solvated system

                │

                ▼

     Measure simulation volume

                │

                ▼

    Calculate required ions

                │

                ▼

  Select water molecules

                │

                ▼

 Replace waters with ions

                │

                ▼

    Update molecular files

                │

                ▼

      Register new system

By the end of this section we will have produced a complete electrolyte
system ready for validation.
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

Only the public API is demonstrated throughout these tutorials.
"""
    )


# %% ==========================================================================
# Defining the ionic system
# ==============================================================================

print("\n")
print("=" * 80)
print("DEFINING THE IONIC SYSTEM")
print("=" * 80)

IONIC_SYSTEM_NAME = f"{SYSTEM_NAME}_{ION_TYPE}"

print(f"Source system      : {SYSTEM_NAME}")
print(f"New system         : {IONIC_SYSTEM_NAME}")
print(f"Electrolyte        : {ION_TYPE}")
print(f"Concentration (M)  : {ION_CONCENTRATION}")


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

Which solvated system should be modified?

        P3HB_10_solvated

2.

Which ions should be inserted?

        KCl

3.

What concentration is required?

        0.15 M

4.

Where should the completed system be written?

        Registered MD system directory

Once these questions have been answered, ion insertion can begin.
"""
)


# %% ==========================================================================
# Build the ionic system
# ==============================================================================

print("\n")
print("=" * 80)
print("GENERATING THE IONIC SYSTEM")
print("=" * 80)

ionic_result = None

if RUN_ION_BUILD and system_builder is not None:

    print(
f"""
Preparing

    {IONIC_SYSTEM_NAME}

using

    {ION_TYPE}

at

    {ION_CONCENTRATION:.2f} M
"""
    )

    ionic_result = (

        system_builder.build_solvated_system_with_ions(

            system_name=SYSTEM_NAME,

            output_name=IONIC_SYSTEM_NAME,

            ion_type=ION_TYPE,

            ion_concentration=ION_CONCENTRATION,

            overwrite=OVERWRITE,

        )

    )

    print()

    print("✓ Ionic system prepared.")

else:

    print(
"""
RUN_ION_BUILD is False.

No molecular files have been modified.

Enable the execution switch after confirming the settings.
"""
    )


# %% ==========================================================================
# Behind the scenes
# ==============================================================================

print("\n")
print("=" * 80)
print("BEHIND THE SCENES - THE ION INSERTION WORKFLOW")
print("=" * 80)

print(
"""
Although ion insertion appears to be a single operation, several preparation
steps occur internally.

The overall workflow is

      Read solvated system

               │

               ▼

    Measure simulation box

               │

               ▼

 Calculate required ion numbers

               │

               ▼

 Select replacement waters

               │

               ▼

 Replace waters with ions

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

Only a very small fraction of the water molecules are replaced.

The overwhelming majority of the solvent remains unchanged.
"""
)


# %% ==========================================================================
# Determining the number of ions
# ==============================================================================

print("\n")
print("=" * 80)
print("CALCULATING THE NUMBER OF IONS")
print("=" * 80)

print(
"""
The requested concentration must be converted into an actual number of ions.

Conceptually, the calculation depends upon

        Simulation volume

                ×

      Desired concentration

                ▼

      Number of ion pairs

Larger simulation boxes require more ions to achieve the same concentration.

Smaller simulation boxes require fewer ions.

The calculation is performed automatically by iPHAsimulator.
"""
)


# %% ==========================================================================
# Why replace water molecules?
# ==============================================================================

print("\n")
print("=" * 80)
print("WHY ARE WATER MOLECULES REPLACED?")
print("=" * 80)

print(
"""
A common misconception is that ions are simply inserted into empty space.

Instead, selected water molecules are replaced.

Conceptually

Before

    O   O   O   O

After

    O  K+  O  Cl-

This preserves the overall density of the solution because no additional
molecules are squeezed into the simulation box.

Only the chemical identity of a very small number of solvent molecules
changes.
"""
)


# %% ==========================================================================
# Maintaining charge neutrality
# ==============================================================================

print("\n")
print("=" * 80)
print("MAINTAINING CHARGE NEUTRALITY")
print("=" * 80)

print(
"""
For neutral polymers, equal numbers of positive and negative ions are added.

Example

        42 K+

            +

        42 Cl-

The total charge therefore remains approximately zero.

For charged molecular systems, such as many proteins or nucleic acids,
additional counterions are normally added first before introducing the
desired salt concentration.

Although PHAs are typically neutral, iPHAsimulator follows the same general
principles used throughout molecular simulation.
"""
)


# %% ==========================================================================
# Updating the molecular system
# ==============================================================================

print("\n")
print("=" * 80)
print("UPDATING THE MOLECULAR SYSTEM")
print("=" * 80)

print(
"""
After ion insertion, the molecular system now contains

        Polymer

            +

        Water

            +

        Dissolved ions

Both the topology and coordinate files are updated to represent the new
chemical composition.

The polymer itself remains unchanged.

Only the surrounding solution has been modified.
"""
)


# %% ==========================================================================
# Inspecting the generated directory
# ==============================================================================

print("\n")
print("=" * 80)
print("GENERATED DIRECTORY")
print("=" * 80)

if ionic_result is not None:

    if hasattr(ionic_result, "system_dir"):

        print(ionic_result.system_dir)

else:

    print(
"""
The output directory will become available after the ionic system has been
generated.
"""
    )


# %% ==========================================================================
# Generated molecular files
# ==============================================================================

print("\n")
print("=" * 80)
print("GENERATED MOLECULAR FILES")
print("=" * 80)

print(
"""
The completed electrolyte system contains

Amber

    topology

    coordinates

GROMACS

    topology

    coordinates

Metadata

    registry information

Compared with the solvated system created in Tutorial 04B, these files now
include explicit ions in addition to the polymer and water molecules.
"""
)


# %% ==========================================================================
# Comparing solvated and ionic systems
# ==============================================================================

print("\n")
print("=" * 80)
print("SOLVATED VERSUS IONIC SYSTEMS")
print("=" * 80)

comparison = [

    ("Polymer", "✓", "✓"),

    ("Water", "✓", "✓"),

    ("Dissolved ions", "✗", "✓"),

    ("Electrolyte concentration", "✗", "✓"),

    ("Charge neutrality", "Implicit", "Explicit"),

]

print(f"{'Property':<32}{'Solvated':<16}{'With Ions'}")
print("-"*80)

for name, solvated, ionic in comparison:

    print(f"{name:<32}{solvated:<16}{ionic}")


# %% ==========================================================================
# Registering the ionic system
# ==============================================================================

print("\n")
print("=" * 80)
print("REGISTERING THE SYSTEM")
print("=" * 80)

print(
"""
The completed electrolyte system is recorded within the molecular system
registry.

The registry now stores information such as

    • source solvated system

    • electrolyte type

    • requested concentration

    • simulation files

Future workflows can therefore identify and load the correct electrolyte
system automatically.
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
During this section we transformed a solvated polymer into an electrolyte
solution.

We learned that

✓ the simulation volume determines how many ions are required

✓ water molecules are replaced rather than adding extra particles

✓ charge neutrality is maintained

✓ the topology and coordinates are updated to include ions

✓ the completed system is written to disk and registered

The polymer has not changed.

Most of the water has not changed.

Only a very small fraction of the solvent has been replaced with dissolved
ions, producing a more realistic representation of many experimental
environments.

In Part 3 we will validate the completed ionic system by examining the
polymer, solvent, ion counts, charge balance, and overall system
consistency.
"""
)

print("\nTutorial 04C Part 2 complete.")

# %% ==========================================================================
# Tutorial 04C - Part 3
# Validating the Ionic Molecular Dynamics System
# ==============================================================================

print("\n")
print("=" * 80)
print("TUTORIAL 04C - PART 3")
print("VALIDATING THE IONIC MOLECULAR DYNAMICS SYSTEM")
print("=" * 80)

print(
"""
The electrolyte system has now been constructed.

Before beginning any molecular dynamics simulation we should verify that the
prepared system is chemically and structurally consistent.

In addition to the validation performed in Tutorial 04B, we now need to
confirm that

    • the requested ions are present

    • the ion counts are correct

    • the solution remains charge neutral

    • the requested concentration has been achieved

Once these checks have passed, the electrolyte system is ready for molecular
dynamics simulations.
"""
)


# %% ==========================================================================
# Loading the ionic system
# ==============================================================================

print("\n")
print("=" * 80)
print("LOADING THE IONIC SYSTEM")
print("=" * 80)

try:

    from openmm.app import AmberPrmtopFile
    from openmm.app import AmberInpcrdFile

    prmtop = AmberPrmtopFile(str(prepared_prmtop))
    inpcrd = AmberInpcrdFile(str(prepared_rst7))

    topology = prmtop.topology

    print("✓ Ionic system loaded successfully.")

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

print(f"Atoms     : {len(atoms)}")
print(f"Residues  : {len(residues)}")
print(f"Chains    : {len(chains)}")


# %% ==========================================================================
# Classifying molecular species
# ==============================================================================

print("\n")
print("=" * 80)
print("IDENTIFYING MOLECULAR SPECIES")
print("=" * 80)

polymer_residues = []
water_residues = []

cation_residues = []
anion_residues = []

for residue in residues:

    name = residue.name.upper()

    if name in {"WAT", "HOH", "SOL", "TIP3P"}:

        water_residues.append(residue)

    elif name in {"K", "K+", "POT"}:

        cation_residues.append(residue)

    elif name in {"CL", "CL-"}:

        anion_residues.append(residue)

    else:

        polymer_residues.append(residue)

print(f"Polymer residues : {len(polymer_residues)}")
print(f"Water molecules  : {len(water_residues)}")
print(f"Cations          : {len(cation_residues)}")
print(f"Anions           : {len(anion_residues)}")


# %% ==========================================================================
# Ion counts
# ==============================================================================

print("\n")
print("=" * 80)
print("ION COUNTS")
print("=" * 80)

print(f"K+ ions  : {len(cation_residues)}")
print(f"Cl- ions : {len(anion_residues)}")

print()

print(
"""
The number of cations and anions should agree with the requested electrolyte
concentration.

Small differences may occasionally arise due to rounding when converting a
continuous concentration into a discrete number of ions.
"""
)


# %% ==========================================================================
# Checking charge neutrality
# ==============================================================================

print("\n")
print("=" * 80)
print("CHARGE NEUTRALITY")
print("=" * 80)

if len(cation_residues) == len(anion_residues):

    print("✓ Equal numbers of positive and negative ions detected.")

else:

    print("⚠ Unequal ion numbers detected.")

print()

print(
"""
For neutral polymers, equal numbers of cations and anions generally produce
an overall neutral simulation box.

Charged molecular systems require additional counterions before salt is added.
"""
)


# %% ==========================================================================
# Estimating the achieved concentration
# ==============================================================================

print("\n")
print("=" * 80)
print("ION CONCENTRATION")
print("=" * 80)

print(f"Requested concentration : {ION_CONCENTRATION:.3f} M")

print()

print(
"""
The exact concentration depends on

    • simulation box volume

    • number of inserted ions

    • rounding to whole ions

Consequently, the achieved concentration may differ slightly from the
requested value.

Small differences are expected and are generally negligible.
"""
)


# %% ==========================================================================
# Water versus ions
# ==============================================================================

print("\n")
print("=" * 80)
print("WATER AND ION COMPOSITION")
print("=" * 80)

print(
f"""
Water molecules

    {len(water_residues)}

Ion pairs

    {len(cation_residues)}

Even relatively concentrated electrolyte solutions still contain far more
water molecules than ions.

The solvent therefore remains overwhelmingly water.
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
When visualising the completed system you should observe

    ✓ one polymer chain

    ✓ continuous solvent

    ✓ randomly distributed ions

    ✓ no obvious ion clustering

    ✓ no empty cavities

The ions should appear dispersed throughout the solution rather than grouped
together in one region.
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

    • source solvated system

    • ion species

    • requested concentration

    • molecular files

This information allows later simulation workflows to identify the correct
electrolyte system automatically.
"""
)


# %% ==========================================================================
# Behind the scenes
# ==============================================================================

print("\n")
print("=" * 80)
print("BEHIND THE SCENES - VALIDATING THE ELECTROLYTE")
print("=" * 80)

print(
"""
Unlike the previous tutorials, validation now extends beyond molecular
structure.

We are also validating the chemistry of the solution.

                Polymer

                    ✓

                Water

                    ✓

                 Ions

                    ✓

          Charge balance

                    ✓

      Requested concentration

                    ✓

Only when all of these components agree can the electrolyte solution be
considered scientifically meaningful.

Validation therefore confirms not only that the files were written correctly,
but that they represent the intended chemical environment.
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

    "Polymer detected":
        len(polymer_residues) > 0,

    "Water detected":
        len(water_residues) > 0,

    "Positive ions detected":
        len(cation_residues) > 0,

    "Negative ions detected":
        len(anion_residues) > 0,

    "Charge neutrality maintained":
        len(cation_residues) == len(anion_residues),

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
The electrolyte molecular dynamics system has now been validated.

We confirmed

✓ the molecular topology loads correctly

✓ the polymer remains unchanged

✓ explicit water molecules are present

✓ the requested ions were inserted

✓ charge neutrality has been maintained

✓ the prepared system represents the intended electrolyte solution

The completed system is now suitable for molecular dynamics simulations under
realistic ionic conditions.

In Part 4 we will explore the scientific applications of electrolyte
simulations and discuss how ionic environments influence polymer behaviour.
"""
)

print("\nTutorial 04C Part 3 complete.")

# %% ==========================================================================
# Tutorial 04C - Part 4
# Understanding the Completed Electrolyte Molecular Dynamics System
# ==============================================================================

print("\n")
print("=" * 80)
print("TUTORIAL 04C - PART 4")
print("UNDERSTANDING THE COMPLETED ELECTROLYTE SYSTEM")
print("=" * 80)

print(
"""
The electrolyte molecular dynamics system is now complete.

Beginning with a finite polymer, we have progressively increased the
complexity of the surrounding molecular environment.

Tutorial 04A

    Polymer

        inside

    an empty periodic box

↓

Tutorial 04B

    Polymer

        inside

    explicit water

↓

Tutorial 04C

    Polymer

        inside

    an electrolyte solution

Although the polymer itself has remained unchanged, the surrounding
environment has become increasingly representative of many real experimental
systems.

The completed molecular system now consists of

        One polymer chain

                +

        Thousands of water molecules

                +

        Dissolved ions

                +

        One periodic simulation box

                +

        A complete molecular force field
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
        "Salt effects",
        "Investigate how dissolved ions influence polymer behaviour."
    ),

    (
        "Electrostatic screening",
        "Study how ions reduce electrostatic interactions within solution."
    ),

    (
        "Hydration structure",
        "Examine how water molecules organise around the polymer in the presence of salt."
    ),

    (
        "Ion association",
        "Determine whether ions preferentially interact with particular regions of the polymer."
    ),

    (
        "Polymer conformation",
        "Measure changes in polymer structure caused by electrolyte concentration."
    ),

    (
        "Diffusion",
        "Study the mobility of polymers, water molecules and ions throughout the simulation."
    ),

]

for title, description in applications:

    print(f"\n{title}")
    print("-" * len(title))
    print(description)


# %% ==========================================================================
# Choosing realistic concentrations
# ==============================================================================

print("\n")
print("=" * 80)
print("CHOOSING ION CONCENTRATIONS")
print("=" * 80)

print(
"""
The concentration selected for a simulation should reflect the environment
being modelled.

Typical examples include

Pure water

    Approximately 0 M

Laboratory buffers

    Approximately 0.05–0.20 M

Physiological saline

    Approximately 0.15 M

Seawater

    Approximately 0.60 M

Higher concentrations introduce larger numbers of ions and can significantly
modify the behaviour of both water and dissolved molecules.

Selecting an appropriate concentration is therefore an important scientific
decision rather than simply a simulation setting.
"""
)


# %% ==========================================================================
# Comparing molecular environments
# ==============================================================================

print("\n")
print("=" * 80)
print("COMPARING MOLECULAR ENVIRONMENTS")
print("=" * 80)

comparison = [

    ("Polymer",                 "✓", "✓", "✓"),

    ("Explicit water",          "✗", "✓", "✓"),

    ("Dissolved ions",          "✗", "✗", "✓"),

    ("Hydration",               "✗", "✓", "✓"),

    ("Electrostatic screening", "✗", "Limited", "✓"),

    ("Solution chemistry",      "✗", "Basic", "Realistic"),

    ("Bulk polymer behaviour",  "✗", "✗", "✗"),

]

print(
f"{'Property':<32}"
f"{'Dry':<12}"
f"{'Water':<12}"
f"{'Water + Ions'}"
)

print("-" * 80)

for property_name, dry, water, ions in comparison:

    print(
        f"{property_name:<32}"
        f"{dry:<12}"
        f"{water:<12}"
        f"{ions}"
    )


# %% ==========================================================================
# Choosing the correct system
# ==============================================================================

print("\n")
print("=" * 80)
print("CHOOSING THE APPROPRIATE SYSTEM")
print("=" * 80)

print(
"""
Different scientific questions require different molecular environments.

Question

    How flexible is an isolated polymer chain?

Recommended system

    Dry single-chain system


Question

    How does water influence polymer conformation?

Recommended system

    Solvated single-chain system


Question

    How do dissolved salts influence polymer behaviour?

Recommended system

    Electrolyte system


Question

    What are the bulk thermal and mechanical properties of the polymer?

Recommended system

    Polymer melt

The molecular environment should always be chosen according to the
experimental conditions or scientific question being investigated.
"""
)


# %% ==========================================================================
# Behind the scenes
# ==============================================================================

print("\n")
print("=" * 80)
print("BEHIND THE SCENES - BUILD ONCE, REUSE MANY TIMES")
print("=" * 80)

print(
"""
One of the central design principles of iPHAsimulator is that polymer
chemistry is generated only once.

The validated polymer can then be reused to create many different molecular
environments.

                    Parameterise polymer

                             │

                             ▼

                      Build polymer

                             │

        ┌────────────────────┼────────────────────┐
        │                    │                    │

        ▼                    ▼                    ▼

    Dry system        Solvated system      Polymer melt

                             │

                             ▼

                     Electrolyte system

Each preparation workflow modifies only the surrounding environment.

The polymer chemistry, force-field parameters and molecular structure remain
unchanged.

This modular approach avoids repeating expensive preparation steps while
allowing multiple scientifically relevant simulation environments to be
generated from a single validated polymer.
"""
)


# %% ==========================================================================
# The complete system preparation workflow
# ==============================================================================

print("\n")
print("=" * 80)
print("SYSTEM PREPARATION WORKFLOW")
print("=" * 80)

print(
"""
Across Tutorials 00–04 we have transformed a simple chemical description into
a complete molecular dynamics system.

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

      Add explicit water

                │

                ▼

      Add dissolved ions

                │

                ▼

     Validate electrolyte system

At this point the molecular system is fully prepared and ready for molecular
dynamics simulations.
"""
)


# %% ==========================================================================
# Milestone
# ==============================================================================

print("\n")
print("=" * 80)
print("COURSE MILESTONE")
print("=" * 80)

print(
"""
Congratulations!

You can now prepare every major single-chain molecular environment supported
by iPHAsimulator.

You have learned how to construct

✓ Dry molecular systems

✓ Solvated molecular systems

✓ Electrolyte molecular systems

These preparation workflows form the foundation for all subsequent molecular
dynamics simulations.

The remainder of the course shifts from system preparation towards simulation,
analysis and scientific interpretation.
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

Why are water molecules replaced rather than simply adding ions to the
simulation box?

2.

Why should an electrolyte system usually remain electrically neutral?

3.

Why are there still far more water molecules than ions in a typical
electrolyte simulation?

4.

Which system would be most appropriate for investigating hydration around a
polymer in physiological saline?

5.

Would an electrolyte single-chain simulation be suitable for predicting the
glass transition temperature of a polymer?

Take a few moments to answer each question before reading the solutions.
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

Replacing water molecules preserves the overall density of the solution while
introducing the desired ions.

2.

Charge neutrality produces a physically meaningful system and avoids
introducing unnecessary electrostatic artefacts into periodic simulations.

3.

Even concentrated salt solutions contain many more water molecules than ions.
Water therefore remains the dominant component of the solvent.

4.

An electrolyte molecular dynamics system containing explicit water and ions.

5.

No.

Glass transition is a bulk material property that requires many interacting
polymer chains rather than a single polymer in solution.
"""
)


# %% ==========================================================================
# Tutorial summary
# ==============================================================================

print("\n")
print("=" * 80)
print("TUTORIAL 04C SUMMARY")
print("=" * 80)

print(
"""
Congratulations!

You have successfully prepared and validated your first electrolyte molecular
dynamics system using iPHAsimulator.

During this tutorial you

✓ introduced dissolved ions

✓ selected an electrolyte

✓ specified an ion concentration

✓ constructed an electrolyte solution

✓ validated the completed system

✓ explored the scientific applications of ionic simulations

You can now prepare realistic molecular environments representing isolated
polymers, aqueous solutions and electrolyte solutions.

These systems provide the starting point for many atomistic molecular
dynamics investigations.
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
Tutorials 04A–04C focused on changing the environment surrounding a single
polymer chain.

The next tutorial introduces a different challenge.

Instead of changing the solvent, we will change the polymer system itself.

        One polymer chain

                │

                ▼

      Many polymer chains

                │

                ▼

         Polymer melt

In Tutorial 05 we will learn how to construct realistic bulk polymer systems,
where interactions between many polymer chains give rise to macroscopic
properties such as density, chain packing and, ultimately, the glass
transition temperature.

This marks the beginning of a new chapter in the course, where our focus
moves from molecular system preparation to the construction of realistic
materials for molecular dynamics simulations.
"""
)

print("\nTutorial 04C complete.")