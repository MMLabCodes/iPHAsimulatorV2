"""Choose a monomer, check its building blocks, and see its chemical structure."""

# %% 1. Get ready
# No path editing is needed. The supplied workshop chemistry is 3HB.
from workshop_helpers import prepare_workshop, check_chemistry, save_picture
workshop = prepare_workshop(modules=("parmed", "rdkit"))
from iphasimulator.visualisation.visualiser import show_PHA_monomer

# %% 2. Choose and check a monomer
# Input: the chemistry name. Use 3HB first; other names may lack parameter files.
# Output: the locations of the building blocks needed to construct a chain.
polymer_type = "3HB"
parameters = check_chemistry(workshop, polymer_type)

# %% 3. View the result
# This drawing shows one monomer. Look for its methyl side group and ester-forming ends.
# A drawing shows the chemistry; it does not prove that force-field parameters are good.
image = show_PHA_monomer(
    PHA_type=polymer_type,
    residue_codes_csv=workshop.database / "residue_codes.csv",
)
save_picture(workshop, image, "02_selected_monomer.png")
# Open the printed PNG path if your editor does not display the picture inline.
