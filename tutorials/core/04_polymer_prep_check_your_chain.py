"""Check that the chain's structure and simulation files agree."""

# %% 1. Get ready
from workshop_helpers import prepare_workshop, check_chain
workshop = prepare_workshop(modules=("openmm", "parmed"))

# %% 2. Check our chain
# Inputs: the saved polymer name and the number of units we asked for in lesson 03.
# The helper checks atom counts across all three files and counts the chain's units.
polymer_name = "P3HB_10"
expected_units = 10
files = check_chain(workshop, polymer_name, expected_units)

# %% 3. Inspect the output
# Passing these checks confirms file consistency, not the quality of the geometry.
# Open this PDB in your molecular viewer and look for overlaps or unexpected bonds.
print("Structure to inspect:", files["pdb"])
print("The atom counts agree, and the expected number of repeat units was found.")
