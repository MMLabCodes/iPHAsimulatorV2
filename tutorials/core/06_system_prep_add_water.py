"""Surround a polymer with water. Start with the checked chain from lesson 04."""

# %% 1. Get ready
from workshop_helpers import prepare_workshop, prepare_system, check_system, plot_counts
workshop = prepare_workshop(modules=("openmm", "parmed", "matplotlib"), commands=("tleap",))
from iphasimulator.build_single_PHA_systems import build_solvated_PHA

# %% 2. Prepare our system
# Input: the chain name from lesson 03. The water padding is in angstroms, measured around the polymer.
polymer_name = "P3HB_10"
water_padding = 12.0
prepared = prepare_system(workshop, polymer_name, "solvated")

# Output: PDB, PRMTOP and RST7 files for a new registered simulation system.
# The helper above checks the inputs and prevents replacing an existing system.
result = build_solvated_PHA(
    polymer_name=polymer_name,
    root_dir=workshop.database,
    box_radius=water_padding,
)

# %% 3. Check and view the result
# Check that the files, atom counts, periodic box and expected composition agree.
counts = check_system(result, prepared)
# Look for water residues as well as the polymer residues.
# This chart counts residues; it is not a 3D view of the simulation box.
plot_counts(workshop, counts, "Residues in our solvated system", "06_system_composition.png")
print("For a 3D inspection, open:", result["pdb"])
