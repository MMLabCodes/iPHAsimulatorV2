"""Analyse an instructor-supplied cooling trajectory and view the fitted Tg.
This can take substantial time. The short NVT run from lesson 11 is not suitable.
"""

# %% 1. Get ready
from workshop_helpers import prepare_workshop, prepare_replica_analysis, check_output_files, read_replica_summary, show_saved_figures
workshop = prepare_workshop(modules=("MDAnalysis", "sklearn", "kneed", "matplotlib", "scipy"))
from iphasimulator.analysis.tg_analysis.workflow import run_tg_analysis

# %% 2. Analyse one cooling run
# Inputs: the supplied system/run names and the cooling schedule used to produce them.
# Ask your instructor to confirm these values; they are not inferred from the files.
system_name = "25_P3HB_10_melt"
run_name = "broad_tg_sim_02"
output = prepare_replica_analysis(workshop, system_name, run_name)

# Output: estimated Tg, diagnostic tables and figures in this run's analysis folder.
# Temperatures are in kelvin. Stride 50 analyses every 50th saved frame.
result = run_tg_analysis(
    system_name=system_name, simulation_name=run_name,
    stage="thermal_ramp_cooling",
    total_steps=200_000_000, reporter_freq=1000,
    max_temp=700, min_temp=140, temp_change=10,
    analysis_stride=50, max_pca_components=20,
    generate_figures=True, project_root=workshop.root,
)

# %% 3. Check and view the results
check_output_files(output / "analysis_summary.json", output / "tg/temperature_response.csv", output / "conformational_state_by_chain.csv")
summary = read_replica_summary(workshop, system_name, run_name)
show_saved_figures(output, ["temperature_block_agreement.png", "tg_fit.png"])
# First compare measured and requested temperatures. Then inspect the fitted curve.
# This is the package's historical cluster-label method; a fit is not proof of validity.
# For already-computed results, use advanced lesson A06 without rerunning this calculation.
