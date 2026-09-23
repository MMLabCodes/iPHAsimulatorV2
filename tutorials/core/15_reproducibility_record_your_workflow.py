"""Save a record of the inputs and outputs belonging to one workshop simulation."""

# %% 1. Get ready
from workshop_helpers import prepare_workshop, record_workflow, check_output_files
workshop = prepare_workshop(modules=("parmed",))

# %% 2. Record our work
# Inputs: the system, numbered run and recipe we used in lessons 10–12.
# Output: a dated JSON file listing inputs, outputs, versions and small-file checksums.
record = record_workflow(
    workshop,
    system_name="P3HB_10_dry",
    simulation_name="workshop_short_01",
    workflow_name="workshop_short",
)

# %% 3. Check the record
check_output_files(record)
print("Keep this record alongside your simulation files and scientific notes.")
# This is an inventory, not a backup. It does not prove which recipe generated old data.
# Keep the original files, environment details and external-tool versions too.
