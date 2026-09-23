"""Explore a saved Tg analysis with pictures. No trajectory is reanalysed."""

# %% 1. Get ready
from workshop_helpers import prepare_workshop, read_replica_summary, replica_folder, show_saved_figures
workshop = prepare_workshop(modules=("PIL",))

# %% 2. Load an existing result
# Inputs: a completed cooling analysis supplied by your instructor or made in lesson 13.
# Output: a summary of the settings and fitted value, loaded from its saved JSON file.
system_name = "25_P3HB_10_melt"
run_name = "broad_tg_sim_02"
summary = read_replica_summary(workshop, system_name, run_name)
folder = replica_folder(workshop, system_name, run_name)

# %% 3. Follow the method through its figures
show_saved_figures(folder, ["pca_scree.png", "dbscan_noise_vs_min_samples.png", "tg_fit.png"])
# PCA: how much variation do the first few components capture?
# Clustering: how much data is treated as noise as the settings change?
# Tg fit: does the fitted curve describe the response across the sampled temperatures?
print("PCA choices:", summary["pca"])
print("Clustering choices:", summary["dbscan"])
print("Fit results:", summary["tg"])
# Read the guide for the equations and assumptions. Numeric cluster IDs are labels;
# interpreting their average as a physical response needs scientific scrutiny.
