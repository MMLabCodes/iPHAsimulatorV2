"""Build a chain containing 10 units of 3HB, then draw the resulting polymer."""

# %% 1. Get ready
# This checks the environment and locates your workshop. Leave it unchanged.
from workshop_helpers import prepare_workshop, prepare_polymer, check_output_files, save_picture
workshop = prepare_workshop(modules=("iphasimulator.build_pha",), commands=("tleap",))
from iphasimulator.visualisation.visualiser import show_PHA_polymer

# %% 2. Build our polymer
# Inputs: the chemistry name and the number of units in our chain.
# Try changing chain_length first. Existing builds are protected from replacement.
polymer_type = "3HB"
chain_length = 10
builder = prepare_polymer(workshop, polymer_type, chain_length)

# The function saves the chain. 'result' contains the paths of the output files.
result = builder.build_PHA_polymer(PHA_type=polymer_type, length=chain_length)

# %% 3. Check and view our polymer
# PDB: atoms and positions. PRMTOP: simulation parameters. RST7: starting coordinates.
check_output_files(result["pdb_file"], result["prmtop_file"], result["rst7_file"])

# Look for the repeating backbone and the two chain ends in this 2D chemical drawing.
# It is drawn from the saved chemical formula, not from the 3D coordinates.
image = show_PHA_polymer(
    polymer_name=f"P{polymer_type}_{chain_length}",
    polymer_smiles_csv=workshop.database / "polymer_smiles.csv",
)
save_picture(workshop, image, f"03_P{polymer_type}_{chain_length}.png")
# Next: lesson 04 checks that the saved structure has the expected number of units.
