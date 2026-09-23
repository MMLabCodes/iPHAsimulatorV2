"""Find a prepared system and its simulation input files."""

# %% 1. Get ready
from workshop_helpers import prepare_workshop, find_system, check_output_files
workshop = prepare_workshop(modules=("parmed",))

# %% 2. Select our system
# Input: a system name printed by one of lessons 05–08.
# Output: 'system' contains its type and the locations of its saved files.
system_name = "P3HB_10_dry"
system = find_system(workshop, system_name)

# %% 3. Check the files
# A topology describes the simulation parameters; coordinates locate the atoms.
check_output_files(system.topology_file, system.coordinate_file)
print("Future simulations will be saved in:", system.simulations_dir)
print("Saved protocols belong in:", system.workflows_dir)
