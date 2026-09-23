"""Compare independent cooling runs and combine their fitted Tg estimates."""

# %% 1. Get ready
from workshop_helpers import prepare_workshop, prepare_replica_comparison, check_output_files, show_saved_figures
workshop = prepare_workshop(modules=("pandas", "matplotlib", "scipy"))
from iphasimulator.analysis.tg_analysis.system_analysis import run_system_tg_analysis

# %% 2. Combine our replicas
# Inputs: completed lesson-13 analyses for independent, comparable simulations.
# The helper checks their identities and recorded schedules before combining them.
system_name = "25_P3HB_10_melt"
run_names = ["broad_tg_sim_02", "broad_tg_sim_03", "broad_tg_sim_04"]
output = prepare_replica_comparison(workshop, system_name, run_names)

# Output: the mean Tg, between-run spread, comparison tables and figures.
# This combines fitted results; it does not merge or rerun the trajectories.
result = run_system_tg_analysis(
    system_name=system_name, simulation_names=run_names,
    generate_figures=True, project_root=workshop.root,
)

# %% 3. Check and compare the results
check_output_files(output / "system_summary.json", output / "replica_summary.csv")
show_saved_figures(output, ["tg_by_replica.png", "temperature_response_by_replica.png"])
# Look for runs that disagree. Small spread alone does not prove adequate sampling.
print("Number of replicas combined:", result["n_replicas"])
