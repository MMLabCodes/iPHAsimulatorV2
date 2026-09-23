"""Run the short simulation recipe from lesson 10. This performs a calculation."""

# %% 1. Get ready
from workshop_helpers import prepare_workshop, run_simulation, check_output_files
workshop = prepare_workshop(modules=("openmm", "parmed"))

# %% 2. Run our simulation
# Inputs: the prepared system and saved recipe. CPU is a portable starting choice.
# The helper runs the exact saved script and records its messages in a log file.
system_name = "P3HB_10_dry"
recipe_name = "workshop_short"
run = run_simulation(workshop, system_name, recipe_name, platform="CPU")

# %% 3. Find the outputs
# Each execution creates a new numbered folder, so earlier runs are retained.
# Copy the printed run name into lesson 12; it may differ from its default.
check_output_files(run.log)
print("Completed run:", run.name)
print("Output folder:", run.directory)
# Lesson 12 checks the trajectory and plots the temperature and energy.
