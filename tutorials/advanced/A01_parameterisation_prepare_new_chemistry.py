"""Prepare trimer parameters in a separate experiment. Read the A01 guide first.
This runs external parameterisation tools; it can take time.
"""

# %% 1. Get ready
from workshop_helpers import prepare_workshop, prepare_parameterisation, check_output_files, save_picture
workshop = prepare_workshop(modules=("iphasimulator.build_pha",), commands=("antechamber", "parmchk2"), require_database=False)
from iphasimulator.visualisation.visualiser import show_PHA_monomer

# %% 2. Parameterise our chemistry
# Inputs: a chemistry name and SMILES strings describing one unit and three units.
# This example uses known 3HB. New chemistry needs scientific review of these inputs.
polymer_type = "3HB"
monomer_smiles = "O[C@H](C)CC(=O)O"
trimer_smiles = "O[C@H](C)CC(=O)O[C@H](C)CC(=O)O[C@H](C)CC(=O)O"
experiment_name = "parameterisation_3HB_01"
geometry_mode = "none"  # This currently still generates 3D geometry with Open Babel.
builder = prepare_parameterisation(workshop, experiment_name, geometry_mode)

# Output: PDB geometry, MOL2 charges/types, FRCMOD terms and an AC atom-description file.
result = builder.parameterise_trimer(
    PHA_type=polymer_type, trimer_name=f"P{polymer_type}_3",
    monomer_smiles=monomer_smiles, trimer_smiles=trimer_smiles,
    forcefield="gaff2", charge_model="abcg2", geometry_optimization=geometry_mode,
)

# %% 3. Check the files and view the selected chemistry
check_output_files(result["pdb_file"], result["mol2_file"], result["frcmod_file"], result["ac_file"])
image = show_PHA_monomer(
    polymer_type,
    residue_codes_csv=workshop.root / "advanced_experiments" / experiment_name / "structure_database/residue_codes.csv",
)
save_picture(workshop, image, "A01_parameterised_monomer.png")
# Check the side group and stereochemistry shown in the drawing.
# Review the trimer's charges, 3D geometry and atom identities before lesson A02.
