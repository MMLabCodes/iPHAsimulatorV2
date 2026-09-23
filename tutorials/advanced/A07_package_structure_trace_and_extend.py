"""Trace how a package module is connected, without executing its functions."""

# %% 1. Get ready
from workshop_helpers import prepare_workshop, inspect_module
workshop = prepare_workshop(require_database=False)

# %% 2. Read a module's structure
# Input: the module we want to explore, relative to src/iphasimulator.
# Output: its imports and top-level function signatures, printed for inspection.
module = "analysis/tg_analysis/workflow.py"
functions = inspect_module(workshop, module)

# %% 3. Follow the connections
print("Top-level functions found:", len(functions))
# Find run_tg_analysis in the output and follow its imported analysis modules.
# Use the adjacent guide's extension exercise to design your own inputs and outputs.
# The reference/coverage_index.md file explains each current package function.
# No functions from the selected module were executed or changed.
