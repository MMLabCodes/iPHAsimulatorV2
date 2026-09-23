"""Add water and dissolved salt. Start with the checked chain from lesson 04."""

# %% 1. Get ready
from workshop_helpers import prepare_workshop, prepare_system, check_system, plot_counts
workshop = prepare_workshop(modules=("openmm", "parmed", "matplotlib"), commands=("tleap",))
from iphasimulator.build_single_PHA_systems import build_solvated_PHA_ions

# %% 2. Prepare our system
# Input: the chain name from lesson 03. Water padding is in angstroms; salt concentration is in mol/L.
polymer_name = "P3HB_10"
water_padding = 12.0
salt_concentration = 0.15
prepared = prepare_system(workshop, polymer_name, "solvated_ions", concentration=salt_concentration)

# Output: PDB, PRMTOP and RST7 files for a new registered simulation system.
# The helper above checks the inputs and prevents replacing an existing system.
result = build_solvated_PHA_ions(
    polymer_name=polymer_name,
    root_dir=workshop.database,
    box_radius=water_padding, salt="KCl", pos_ion="K+", neg_ion="Cl-",
    ion_conc=salt_concentration,
)

# %% 3. Check and view the result
# Check that the files, atom counts, periodic box and expected composition agree.
counts = check_system(result, prepared)
# Look for water, potassium and chloride. The helper checks the rounded ion-pair count.
# This chart counts residues; it is not a 3D view of the simulation box.
plot_counts(workshop, counts, "Residues in our solvated_ions system", "07_system_composition.png")
print("For a 3D inspection, open:", result["pdb"])
