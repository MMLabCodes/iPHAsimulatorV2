"""Create a separate folder for your workshop work. Run this before lesson 02."""

# %% 1. Get ready
# The shared helper handles paths. Your research database is kept separate.
from workshop_helpers import prepare_workshop, create_workshop, check_output_files
workshop = prepare_workshop(modules=("parmed",), require_database=False)

# %% 2. Create the workshop inputs
# Input: the supplied 3HB building blocks in this project.
# Output: a copy in ~/iphasimulator_workshop/structure_database.
# Existing workshop chemistry is reused without replacing it.
database = create_workshop(workshop)

# %% 3. Check the result
# The catalogue tells the package which chemistries are registered.
check_output_files(database / "residue_codes.csv")
print("Your workshop database is:", database)
print("PHA_types contains building blocks; built_PHAs will contain your chains.")
