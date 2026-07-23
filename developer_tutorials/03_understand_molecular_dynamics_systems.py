#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
===============================================================================
Tutorial 03 - Understanding Molecular Dynamics Systems
===============================================================================

Congratulations!

In Tutorial 02 we successfully constructed a finite PHA polymer.

For example

    P3HB_10

This polymer contains everything required to describe its chemistry.

It has

    • atom types

    • partial charges

    • bonded interactions

    • three residue definitions

    • Amber topology

    • GROMACS topology

However...

A polymer is NOT yet a molecular dynamics simulation.

Before we can perform molecular dynamics we must decide

    What physical environment should this polymer exist in?

That question is answered by preparing an MD system.

By the end of this tutorial you will understand

    • what an MD system is

    • why a polymer alone is not enough

    • the different environments available within iPHAsimulator

    • how prepared systems are organised

    • why the same polymer can generate many different simulations

Unlike the previous tutorials, this tutorial is mostly conceptual.

No new chemistry will be generated.

No simulations will be run.

Instead we will develop an understanding of how simulation systems are
constructed before creating them in Tutorials 04A–05.

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


# %% ==========================================================================
# Initialise the project
# ==============================================================================

paths = PHAFileManager(
    root_dir=STRUCTURE_DATABASE,
)

print("=" * 80)
print("Tutorial 03 - Understanding Molecular Dynamics Systems")
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
Previous tutorials

✓ Tutorial 00

    Understanding the structure database

✓ Tutorial 01

    Registering and parameterising a PHA

✓ Tutorial 02

    Building a finite polymer


Current tutorial

► Tutorial 03

    Understanding molecular dynamics systems


Upcoming tutorials

□ Tutorial 04A

    Building a dry single-chain system

□ Tutorial 04B

    Building a solvated single-chain system

□ Tutorial 04C

    Building a solvated single-chain system with ions

□ Tutorial 05

    Building a polymer melt

□ Tutorial 06+

    Running and analysing simulations
"""
)


# %% ==========================================================================
# What have we built so far?
# ==============================================================================

print("\n")
print("=" * 80)
print("WHAT HAVE WE BUILT SO FAR?")
print("=" * 80)

print(
"""
At the end of Tutorial 02 we created

        P3HB_10

This finite polymer contains

    ✓ Chemistry

    ✓ Coordinates

    ✓ Force-field parameters

    ✓ Amber topology

    ✓ GROMACS topology

This is a complete molecular description.

But there is still one important question left unanswered...

Where does this molecule actually exist?

For example

Is it

    floating in empty space?

or

    surrounded by water?

or

    dissolved in salt solution?

or

    packed together with hundreds of neighbouring polymer chains?

These questions define the molecular dynamics system.
"""
)


# %% ==========================================================================
# A polymer is not a simulation
# ==============================================================================

print("\n")
print("=" * 80)
print("A POLYMER IS NOT A SIMULATION")
print("=" * 80)

print(
"""
Many new users assume the workflow looks like

        Polymer

           │

           ▼

     Molecular dynamics

Unfortunately it is not quite that simple.

Instead the workflow is

        Polymer

           │

           ▼

    Physical environment

           │

           ▼

     Simulation box

           │

           ▼

    Molecular dynamics

The same polymer can therefore be simulated in many different ways
depending on its environment.
"""
)


# %% ==========================================================================
# What is an MD system?
# ==============================================================================

print("\n")
print("=" * 80)
print("WHAT IS AN MD SYSTEM?")
print("=" * 80)

print(
"""
A molecular dynamics system is a complete physical description of what
will be simulated.

It consists of

        Polymer

            +

     Physical environment

            +

      Simulation box

            +

      Force field

            +

        Coordinates

Only when all of these pieces exist can a simulation begin.

Notice something important.

The polymer itself is only ONE component of the complete system.
"""
)


# %% ==========================================================================
# The polymer stays the same
# ==============================================================================

print("\n")
print("=" * 80)
print("THE POLYMER DOES NOT CHANGE")
print("=" * 80)

print(
"""
Suppose we have built

        P3HB_10

Now imagine three different simulations.

Simulation A

        P3HB_10

Simulation B

        P3HB_10

        +

        Water

Simulation C

        P3HB_10

        +

        Water

        +

        Salt

Notice something.

The polymer itself has not changed.

Its chemistry

its atom types

its charges

its bonded parameters

remain exactly the same.

Only the surrounding environment changes.

This is one of the key design principles of iPHAsimulator.

Parameterise once.

Reuse everywhere.
"""
)


# %% ==========================================================================
# The four system types
# ==============================================================================

print("\n")
print("=" * 80)
print("THE FOUR SYSTEM TYPES")
print("=" * 80)

print(
"""
Within iPHAsimulator there are four common simulation environments.

                     Built polymer
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼

      Dry system      Solvated system   Polymer melt
                           │
                           ▼

                 Solvated + ions

Each environment answers different scientific questions.

The polymer chemistry never changes.

Only its surroundings do.
"""
)


# %% ==========================================================================
# Dry single-chain system
# ==============================================================================

print("\n")
print("=" * 80)
print("SYSTEM TYPE 1 - DRY SINGLE CHAIN")
print("=" * 80)

print(
"""
Representation

        Polymer

            +

      Empty simulation box

Typical uses

    • chain folding

    • radius of gyration

    • intrinsic flexibility

    • conformational analysis

Advantages

    • smallest system

    • fastest simulations

    • easiest to interpret

Limitations

    • no solvent

    • no neighbouring polymers

    • not representative of bulk behaviour
"""
)


# %% ==========================================================================
# Solvated single-chain system
# ==============================================================================

print("\n")
print("=" * 80)
print("SYSTEM TYPE 2 - SOLVATED SINGLE CHAIN")
print("=" * 80)

print(
"""
Representation

        Polymer

            +

        Water box

Typical uses

    • hydration

    • hydrogen bonding

    • polymer-water interactions

    • swelling

Advantages

    • realistic aqueous environment

    • suitable for solution studies

Limitations

    • more atoms

    • longer simulations

    • not suitable for bulk polymer properties
"""
)


# %% ==========================================================================
# Solvated system with ions
# ==============================================================================

print("\n")
print("=" * 80)
print("SYSTEM TYPE 3 - SOLVATED WITH IONS")
print("=" * 80)

print(
"""
Representation

        Polymer

            +

         Water

            +

      Positive ions

            +

      Negative ions

Typical uses

    • electrolyte environments

    • salt effects

    • ionic strength

    • realistic biological or environmental conditions

The ions do not change the polymer chemistry.

They simply modify the surrounding solution.
"""
)


# %% ==========================================================================
# Polymer melt
# ==============================================================================

print("\n")
print("=" * 80)
print("SYSTEM TYPE 4 - POLYMER MELT")
print("=" * 80)

print(
"""
Representation

      Many polymer chains

               +

       Periodic simulation box

Typical uses

    • density

    • glass transition temperature

    • oxygen diffusion

    • bulk polymer properties

Unlike the previous systems, the melt contains many copies of the same
polymer.

The force field is identical.

Only the number of chains changes.
"""
)


# %% ==========================================================================
# Comparing the environments
# ==============================================================================

print("\n")
print("=" * 80)
print("COMPARING THE ENVIRONMENTS")
print("=" * 80)

comparison = [
    ("Dry",               "1",    "No",  "No",  "Chain behaviour"),
    ("Solvated",          "1",    "Yes", "No",  "Hydration"),
    ("Solvated + ions",   "1",    "Yes", "Yes", "Salt effects"),
    ("Polymer melt",      "Many", "No",  "Usually no", "Bulk properties"),
]

print(
    f"{'System':<22}"
    f"{'Chains':<10}"
    f"{'Water':<10}"
    f"{'Ions':<12}"
    f"{'Typical use'}"
)

print("-"*80)

for row in comparison:

    print(
        f"{row[0]:<22}"
        f"{row[1]:<10}"
        f"{row[2]:<10}"
        f"{row[3]:<12}"
        f"{row[4]}"
    )


# %% ==========================================================================
# One chemistry, many simulations
# ==============================================================================

print("\n")
print("=" * 80)
print("ONE CHEMISTRY, MANY SIMULATIONS")
print("=" * 80)

print(
"""
This is perhaps the most important concept introduced so far.

Once a polymer has been parameterised

        P3HB_10

it can immediately be reused to construct

        Dry system

                ↓

        Solvated system

                ↓

     Solvated ionic system

                ↓

         Polymer melt

without repeating

    atom typing

    charge calculation

    parameterisation

or

    residue generation.

The chemistry is generated once.

The environment can be generated many times.

This separation keeps the workflow both efficient and reproducible.
"""
)

# %% ==========================================================================
# How does iPHAsimulator remember prepared systems?
# ==============================================================================

print("\n")
print("=" * 80)
print("HOW DOES iPHASIMULATOR REMEMBER MD SYSTEMS?")
print("=" * 80)

print(
"""
Imagine you have spent several days preparing systems.

You might create

    • a dry P3HB system

    • a solvated P3HB system

    • the same polymer with KCl

    • a 25-chain polymer melt

If these systems only existed as folders on your computer, it would quickly
become difficult to remember

    Which system was which?

    Which polymer was used?

    Which water model?

    Which salt concentration?

    Which files belong together?

Instead, iPHAsimulator keeps a registry of every prepared system.

Think of it as a catalogue rather than simply a collection of folders.
"""
)


# %% ==========================================================================
# The MD system registry
# ==============================================================================

print("\n")
print("=" * 80)
print("THE MD SYSTEM REGISTRY")
print("=" * 80)

print(
"""
Every prepared simulation is registered.

                    Build system

                         │

                         ▼

                  Register system

                         │

                         ▼

                  md_systems.csv

                         │

                         ▼

             Available for simulation

Rather than searching through folders manually, the software can simply
look inside the registry.

This makes prepared systems

    searchable

    reproducible

    reusable

and easy to manage.
"""
)


# %% ==========================================================================
# Locate the registry
# ==============================================================================

print("\n")
print("=" * 80)
print("LOCATING THE REGISTRY")
print("=" * 80)

try:

    registry_path = paths.get_md_system_registry_path()

except AttributeError:

    registry_path = (
        STRUCTURE_DATABASE
        / "md_systems.csv"
    )

print(registry_path)

print()

if registry_path.exists():

    print("✓ Registry found.")

else:

    print("The registry has not yet been created.")

    print(
"""
This is perfectly normal if no molecular dynamics systems have been built
yet.

The registry is normally created automatically the first time a prepared
system is generated.
"""
    )


# %% ==========================================================================
# What information is stored?
# ==============================================================================

print("\n")
print("=" * 80)
print("WHAT INFORMATION IS STORED?")
print("=" * 80)

print(
"""
Each row represents ONE prepared molecular dynamics system.

For example

+--------------------------------------------------------------+

System name

Polymer

System type

Number of chains

Water model

Salt

Density

Topology

Coordinates

Simulation directory

+--------------------------------------------------------------+

Notice that this is NOT storing chemistry.

The chemistry already exists inside the polymer.

Instead the registry stores information describing the environment in which
that polymer should be simulated.
"""
)


# %% ==========================================================================
# Reading the registry
# ==============================================================================

print("\n")
print("=" * 80)
print("READING THE REGISTRY")
print("=" * 80)

import pandas as pd

if registry_path.exists():

    registry = pd.read_csv(
        registry_path
    )

    print(
        f"Number of registered systems: "
        f"{len(registry)}"
    )

    print()

    print(registry.head())

else:

    print(
        "No registry is currently available."
    )


# %% ==========================================================================
# Inspect the registry columns
# ==============================================================================

print("\n")
print("=" * 80)
print("REGISTRY COLUMNS")
print("=" * 80)

if registry_path.exists():

    for column in registry.columns:

        print(column)

else:

    print(
        "No registry columns available."
    )


print(
"""

Although the exact columns may evolve as iPHAsimulator develops, they
typically describe

    the polymer

    the surrounding environment

    where the files are stored

rather than the molecular force field itself.
"""
)


# %% ==========================================================================
# Every system has a unique identity
# ==============================================================================

print("\n")
print("=" * 80)
print("EVERY SYSTEM HAS A UNIQUE IDENTITY")
print("=" * 80)

print(
"""
Consider these systems.

P3HB_10_dry

P3HB_10_water

P3HB_10_water_KCl

25_P3HB_10_melt

Notice that

    every one

uses

        P3HB_10

The polymer has not changed.

Only the environment has changed.

This allows the same validated polymer to be reused many times without
duplicating chemistry.
"""
)


# %% ==========================================================================
# Where are the files?
# ==============================================================================

print("\n")
print("=" * 80)
print("WHERE ARE THE FILES?")
print("=" * 80)

print(
"""
Each registered system corresponds to a directory.

For example

MD_systems/

    P3HB_10_dry/

    P3HB_10_water/

    P3HB_10_water_KCl/

    25_P3HB_10_melt/

Each folder contains

    coordinates

    topology

    simulation inputs

and any additional files required to run molecular dynamics.

The registry simply tells iPHAsimulator where each system lives.
"""
)


# %% ==========================================================================
# Registry versus folders
# ==============================================================================

print("\n")
print("=" * 80)
print("WHY USE A REGISTRY?")
print("=" * 80)

print(
"""
Imagine there are 150 prepared systems.

Without a registry you would need to

    browse folders

    inspect filenames

    remember naming conventions

Instead

the registry allows the software to answer questions such as

    Show every melt.

    Show every solvated system.

    Show every system containing P3HB.

    Show every system using TIP3P water.

without manually searching the directory tree.

This is one of the reasons iPHAsimulator scales well to large projects.
"""
)


# %% ==========================================================================
# Viewing the available systems
# ==============================================================================

print("\n")
print("=" * 80)
print("AVAILABLE SYSTEMS")
print("=" * 80)

if registry_path.exists():

    if len(registry) == 0:

        print(
            "No molecular dynamics systems have been registered."
        )

    else:

        for system_number, row in registry.iterrows():

            print()

            print(
                f"System {system_number + 1}"
            )

            print("-" * 40)

            for column in registry.columns:

                print(
                    f"{column:<25}"
                    f"{row[column]}"
                )

else:

    print(
        "No registry available."
    )


# %% ==========================================================================
# A polymer can have many systems
# ==============================================================================

print("\n")
print("=" * 80)
print("ONE POLYMER - MANY SYSTEMS")
print("=" * 80)

print(
"""
Think about P3HB_10.

It can generate

        Dry

          │

          ▼

     Solvated

          │

          ▼

 Solvated + ions

          │

          ▼

    Polymer melt

These are four different simulation systems.

However

they all point back to

the same polymer.

The registry records this relationship.

This avoids storing duplicate chemistry while still allowing many
simulation environments.
"""
)


# %% ==========================================================================
# Summary of Part 2
# ==============================================================================

print("\n")
print("=" * 80)
print("PART 2 SUMMARY")
print("=" * 80)

print(
"""
In this section we introduced the MD system registry.

The registry does NOT replace the molecular files.

Instead it provides a searchable catalogue describing every prepared
simulation system.

Each registered system records

    • the polymer used

    • the environment

    • where the files are stored

    • the information needed to prepare simulations

In the next section we will learn how to decide

which type of molecular dynamics system is appropriate for a particular
scientific question.

This will lead directly into Tutorial 04A, where we will build our first
simulation-ready dry single-chain system.
"""
)

# %% ==========================================================================
# Choosing the correct MD system
# ==============================================================================

print("\n")
print("=" * 80)
print("CHOOSING THE CORRECT MD SYSTEM")
print("=" * 80)

print(
"""
One of the most common questions new users ask is

    Which simulation system should I build?

The answer depends entirely on the scientific question you are trying to
answer.

There is no universally "best" molecular dynamics system.

Each environment has been designed to answer different types of questions.

Choosing the correct system is therefore one of the most important
decisions made before any simulation begins.
"""
)


# %% ==========================================================================
# Which system answers which question?
# ==============================================================================

print("\n")
print("=" * 80)
print("MATCHING THE SYSTEM TO THE SCIENCE")
print("=" * 80)

questions = [

    ("How flexible is a polymer chain?",
     "Dry single-chain"),

    ("How does the polymer fold?",
     "Dry single-chain"),

    ("How does water interact with the polymer?",
     "Solvated"),

    ("How hydrated is the polymer?",
     "Solvated"),

    ("How does salt affect behaviour?",
     "Solvated + ions"),

    ("How does ionic strength change the polymer?",
     "Solvated + ions"),

    ("What is the density?",
     "Polymer melt"),

    ("What is the glass transition temperature?",
     "Polymer melt"),

    ("What is the oxygen diffusion coefficient?",
     "Polymer melt"),

    ("How do polymer chains pack together?",
     "Polymer melt"),

]

print(f"{'Scientific question':<50}Recommended system")
print("-"*80)

for question, system in questions:

    print(f"{question:<50}{system}")


# %% ==========================================================================
# A simple decision tree
# ==============================================================================

print("\n")
print("=" * 80)
print("A SIMPLE DECISION TREE")
print("=" * 80)

print(
"""
Start with one question.

        What do I want to study?

                │

                ▼

      One polymer chain?

         │             │

        Yes            No

         │             │

         ▼             ▼

   Water needed?    Polymer melt

     │        │

    No       Yes

     │        │

     ▼        ▼

 Dry system  Salt?

               │

          ┌────┴────┐

          │         │

         No        Yes

          │         │

          ▼         ▼

     Solvated   Solvated
                  + ions

This simple workflow covers the vast majority of molecular dynamics
systems produced by iPHAsimulator.
"""
)


# %% ==========================================================================
# The lifecycle of a polymer
# ==============================================================================

print("\n")
print("=" * 80)
print("THE LIFECYCLE OF A POLYMER")
print("=" * 80)

print(
"""
Throughout these tutorials we have gradually transformed a simple SMILES
string into a molecular dynamics system.

The complete journey now looks like this.

        Monomer SMILES

               │

               ▼

      Parameterise chemistry

               │

               ▼

     Generate residue definitions

               │

               ▼

      Build finite polymer

               │

               ▼

      Choose an environment

               │

               ▼

     Prepare MD system

               │

               ▼

     Register MD system

               │

               ▼

     Ready for simulation

Notice that chemistry only appears once.

Everything after that stage simply changes the environment in which the
polymer exists.
"""
)


# %% ==========================================================================
# Reusability
# ==============================================================================

print("\n")
print("=" * 80)
print("WHY IS THIS DESIGN IMPORTANT?")
print("=" * 80)

print(
"""
Imagine a research project containing

    30 PHA chemistries

Each chemistry might be simulated as

    dry

    solvated

    solvated with ions

    polymer melt

This immediately creates

        30 × 4 = 120

simulation systems.

Without reusable chemistry this would require parameterising every one of
those systems independently.

Instead

iPHAsimulator parameterises each chemistry once

then simply reuses that chemistry to create many different simulation
environments.

This greatly reduces both computational cost and the possibility of
introducing inconsistencies between systems.
"""
)


# %% ==========================================================================
# Thinking like a molecular modeller
# ==============================================================================

print("\n")
print("=" * 80)
print("THINKING LIKE A MOLECULAR MODELLER")
print("=" * 80)

print(
"""
One of the biggest changes when learning molecular simulation is changing
how we think about molecules.

Instead of asking

    What molecule do I have?

we begin asking

    Under what conditions should this molecule exist?

Those conditions include

    solvent

    ions

    neighbouring polymers

    temperature

    pressure

    simulation box

The molecule itself is only part of the problem.

The surrounding environment is equally important.
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
We now understand what a molecular dynamics system is.

The remaining tutorials will focus on constructing these systems.

Tutorial 04A

        Built polymer

                │

                ▼

      Dry single-chain system

Tutorial 04B

        Dry system

                │

                ▼

          Add explicit water

Tutorial 04C

       Solvated system

                │

                ▼

           Add salt ions

Tutorial 05

      One polymer chain

                │

                ▼

     Many polymer chains

                │

                ▼

        Polymer melt

Notice that every one of these tutorials starts from exactly the same
validated polymer generated in Tutorial 02.
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
Before continuing, see if you can answer these questions.

1.

Why is a polymer alone not an MD system?

2.

Which parts of a polymer remain unchanged when moving from

    dry

to

    solvated?

3.

Why are prepared systems registered?

4.

Which system would you choose for measuring

    glass transition temperature?

5.

Which system would you choose for studying

    polymer hydration?

6.

Can the same parameterised polymer be reused in multiple environments?

7.

What additional information must be supplied before molecular dynamics can
begin?

Take a moment to answer these yourself before reading the solutions below.
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

Because a polymer has no defined simulation environment.

2.

The chemistry, atom types, charges, bonded parameters and residue
definitions remain identical.

3.

So that prepared systems become searchable, reproducible and reusable.

4.

A polymer melt.

5.

A solvated single-chain system.

6.

Yes.

This is one of the central design principles of iPHAsimulator.

7.

A physical environment together with the simulation box and all associated
topology and coordinate information.
"""
)


# %% ==========================================================================
# Tutorial summary
# ==============================================================================

print("\n")
print("=" * 80)
print("TUTORIAL 03 SUMMARY")
print("=" * 80)

print(
"""
Congratulations!

You now understand the philosophy behind molecular dynamics systems in
iPHAsimulator.

The key ideas introduced in this tutorial are

✓ A polymer is not yet a simulation.

✓ A molecular dynamics system combines

      chemistry

          +

      physical environment.

✓ The same polymer can be reused in many different simulation
  environments.

✓ Prepared systems are organised and registered for future reuse.

✓ Different scientific questions require different system types.

Most importantly, remember this principle:

        Parameterise once.

                │

                ▼

      Reuse everywhere.

This design makes large simulation studies practical while ensuring that
every simulation begins from exactly the same validated chemistry.
"""
)


# %% ==========================================================================
# Course roadmap
# ==============================================================================

print("\n")
print("=" * 80)
print("COURSE ROADMAP")
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


Next

► Tutorial 04A

    Building a dry single-chain molecular dynamics system

Later

□ Tutorial 04B

    Building a solvated molecular dynamics system

□ Tutorial 04C

    Building a solvated molecular dynamics system with ions

□ Tutorial 05

    Building a polymer melt

□ Tutorial 06

    Exploring the MD system registry

□ Tutorial 07

    Creating an OpenMM workflow

□ Tutorial 08

    Running molecular dynamics

□ Tutorial 09

    Inspecting simulation outputs

□ Tutorial 10

    Analysing trajectories and calculated properties

□ Tutorial 11

    Complete end-to-end workflow
"""
)

print("\nTutorial 03 complete.")