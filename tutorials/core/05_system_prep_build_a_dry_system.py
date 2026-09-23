"""Prepare a dry system. Start with the checked chain from lesson 04."""

# %% 1. Get ready
from workshop_helpers import prepare_workshop, prepare_system, check_system, plot_counts
workshop = prepare_workshop(modules=("openmm", "parmed", "matplotlib"), commands=("tleap",))
from iphasimulator.build_single_PHA_systems import build_dry_PHA

# %% 2. Prepare our system
# Input: the chain name from lesson 03. The box setting is in angstroms and uses Amber setBox centers.
polymer_name = "P3HB_10"
box_size = 20.0
prepared = prepare_system(workshop, polymer_name, "dry")

# Output: PDB, PRMTOP and RST7 files for a new registered simulation system.
# The helper above checks the inputs and prevents replacing an existing system.
result = build_dry_PHA(
    polymer_name=polymer_name,
    root_dir=workshop.database,
    box_radius=box_size,
)

# %% 3. Check and view the result
# Check that the files, atom counts, periodic box and expected composition agree.
counts = check_system(result, prepared)
# The chart should contain polymer residues and no water.
# This chart counts residues; it is not a 3D view of the simulation box.
plot_counts(workshop, counts, "Residues in our dry system", "05_system_composition.png")
print("For a 3D inspection, open:", result["pdb"])
