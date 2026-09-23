"""Build a copolymer with alternating chemistries. Read the A03 guide first.
The default 4HB parameters are not supplied: prepare and review them before running.
"""

# %% 1. Get ready
from workshop_helpers import prepare_workshop, prepare_copolymer, describe_sequence, check_output_files, save_picture
workshop = prepare_workshop(modules=("iphasimulator.build_pha",), commands=("tleap",))
from iphasimulator.visualisation.visualiser import show_PHA_polymer

# %% 2. Choose the sequence and build it
# Inputs: A means the first chemistry; B means the second.
# Repeating AB to fill six units gives 3HB–4HB–3HB–4HB–3HB–4HB.
chemistries = ["3HB", "4HB"]
pattern = "AB"
chain_length = 6
sequence = describe_sequence(chemistries, pattern, chain_length)
builder = prepare_copolymer(workshop, chemistries, pattern, chain_length)

# Output: Amber files for the copolymer and a saved chemical formula for drawing it.
result = builder.build_PHA_copolymer(
    PHA_types=chemistries, length=chain_length, pattern=pattern, sequence_mode="pattern",
)

# %% 3. Check and view the copolymer
check_output_files(result["pdb_file"], result["prmtop_file"], result["rst7_file"])
image = show_PHA_polymer(
    result["copolymer_name"],
    polymer_smiles_csv=workshop.database / "polymer_smiles.csv",
)
save_picture(workshop, image, "A03_copolymer.png")
# Compare the drawing with the printed sequence; look for alternating side-group patterns.
# Current downstream system builders do not generally support co_* names; see the guide.
