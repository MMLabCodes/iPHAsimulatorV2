"""Load a completed short simulation and plot temperature and energy over time."""

# %% 1. Get ready
from workshop_helpers import prepare_workshop, find_system, check_simulation, plot_simulation
workshop = prepare_workshop(modules=("parmed", "MDAnalysis", "matplotlib"))
from iphasimulator.analysis.simulation_loader import load_simulation

# %% 2. Load our simulation
# Inputs: the system, exact numbered run from lesson 11, and the stage name.
# Output: 'loaded' contains the trajectory, recorded measurements and file paths.
system_name = "P3HB_10_dry"
run_name = "workshop_short_01"
system = find_system(workshop, system_name)
loaded = load_simulation(system.system_dir, run_name, "NVT", validate_alignment=True)

# %% 3. Check and plot the outputs
check_simulation(loaded)
plot_simulation(workshop, loaded)
# Look for temperature fluctuations around the requested 300 K and any energy drift.
# These short traces do not establish equilibration or convergence.
# Each axis includes the units recorded in the simulation output.
