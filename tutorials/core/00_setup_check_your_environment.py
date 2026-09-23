"""Check that your computer is ready for the workshop. Nothing is built here."""

# %% 1. Get ready
# This finds the package and your workshop folder. Leave this section unchanged.
from workshop_helpers import prepare_workshop, check_environment
workshop = prepare_workshop(require_database=False)

# %% 2. Check the environment
# Start with the chain-building tools. Change analysis to True before lesson 13.
# The helper checks Python libraries and whether the external programs are found.
ready = check_environment(workshop, build_tools=True, melt_tools=False, analysis=False)

# %% 3. Read the result
# If something is missing, the check stops and tells you what needs installing.
# Reaching this line means the selected checks passed; no simulation was run.
print("Environment checks passed. Continue to lesson 01.")
