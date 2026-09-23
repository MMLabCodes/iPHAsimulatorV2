"""Generate head, middle and tail residues from a reviewed trimer.
Before running, read A02 and have the three PREPGEN atom-definition files reviewed.
"""

# %% 1. Get ready
from workshop_helpers import prepare_workshop, prepare_residue_definitions, check_residue_files
workshop = prepare_workshop(modules=("iphasimulator.build_pha",), commands=("prepgen",), require_database=False)

# %% 2. Generate reusable building blocks
# Inputs: the A01 experiment, its AC file, and manually reviewed atom definitions.
# The helper checks these files, prints the definitions and protects existing outputs.
experiment_name = "parameterisation_3HB_01"
polymer_type = "3HB"
prepared = prepare_residue_definitions(workshop, experiment_name, polymer_type)

# Output: three PREPIN files, one for each position a unit can occupy in a chain.
prepared.builder.generate_polymer_prepins(polymer_type)

# %% 3. Check the residue files
check_residue_files(prepared.files)
# The files must also have sensible charges and correct connection atoms.
# Use the A02 guide to review these; file presence cannot establish chemical correctness.
