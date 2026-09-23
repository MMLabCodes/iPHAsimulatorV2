"""Create a short simulation recipe. This lesson saves it without running it."""

# %% 1. Get ready
from workshop_helpers import prepare_workshop, find_system, save_protocol, check_output_files
workshop = prepare_workshop(modules=("parmed",))
from iphasimulator.openmmscript_builder import OpenMMScriptBuilder

# %% 2. Write our simulation recipe
# Inputs: a prepared system, a name for this recipe, a step count and temperature.
# Temperature is in kelvin. 5,000 steps is a short demonstration, not a production run.
system_name = "P3HB_10_dry"
recipe_name = "workshop_short"
steps = 5000
temperature = 300.0
system = find_system(workshop, system_name)

protocol = OpenMMScriptBuilder(
    system_name=system_name, system_type=system.kind,
    run_name=recipe_name, workflow_name=recipe_name,
)
# First relieve unfavourable contacts, then simulate at constant volume and temperature.
protocol.add_minimization()
protocol.add_basic_NVT(total_steps=steps, temp=temperature, filename="NVT", save_restart=False)
saved = save_protocol(workshop, protocol)

# %% 3. Check the outputs
# JSON stores the recipe; the Python script runs it in lesson 11.
# The helper also reloads the JSON to check that the saved recipe matches.
check_output_files(saved.definition, saved.script)
print("Recipe saved. No simulation has run yet.")
