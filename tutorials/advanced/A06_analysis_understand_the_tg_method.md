# A06 — Trace the Tg calculation from frames to system statistics

**Task:** explain how saved Tg results arise from the current functions, and distinguish implementation checks from scientific validation.

**Inputs:** a completed replica analysis from core Tutorial 13, including saved figures. **Output:** a review of PCA, clustering and Tg figures alongside the saved settings. The exercise does not recompute expensive arrays. If figures were not generated, it reports what is missing and still prints the settings; supply precomputed figures for the visual exercise.

## 1. Load aligned observations

`load_simulation()` locates one minimised PDB and one stage-specific DCD/TXT pair. `_find_single_file()` rejects absent or ambiguous matches. `validate_frame_data_alignment()` compares row/frame counts and checks times at selected frame indices, not every frame.

`assign_nominal_temperatures()` reconstructs a cooling schedule from supplied settings and frame indices. It retains a historical frame-zero convention. It does not infer all protocol details from instantaneous temperatures or guarantee agreement with every reporting boundary.

## 2. Represent each chain

The descriptor module treats topology segments as chains. `get_polymer_segments()` does not independently prove each segment is a polymer. `get_segment_heavy_atoms()` selects atoms using `not name H*`. `calculate_chain_distance_descriptors()` samples frames and calculates all pairwise selected-atom distances using the box. With H selected heavy atoms, each frame contains H(H−1)/2 features. The dataclass preserves segment identity and sampled frame indices.

`calculate_chain_pca()` standardises features separately for each chain and fits PCA. The optimisation helpers evaluate scree elbows and additional dimensionality diagnostics. `optimise_pca_dimensionality()` chooses a common dimension by rounding the median chain elbow. Common dimensionality does not imply a common fitted PCA coordinate basis across chains.

## 3. Select and apply clustering

`estimate_dbscan_eps()` builds a nearest-neighbour distance curve, trims a fraction based on the number of temperature blocks, and uses a knee or percentile fallback for epsilon. `get_dbscan_neighbor_rank()` links the neighbour rank to selected PCA dimensionality.

The parameter-analysis functions evaluate candidates per chain. Stability functions compare adjacent min_samples settings using adjusted Rand agreement. Summary builders aggregate chain-level diagnostics. `select_dbscan_min_samples()` applies nontrivial-clustering/noise guardrails before choosing a candidate by stability. A guardrail pass is an algorithmic condition, not proof of physical state separation.

`cluster_all_chain_pca()` performs the final per-chain fits and stores labels, noise fractions, cluster counts and epsilon information. Preserve noise label −1 when tracing how the historical response is computed.

## 4. Fit the implemented observable

`calculate_historical_cluster_response()` groups sampled labels by assigned temperature and averages the numeric labels across observations. It does not align cluster identities across independent chains. DBSCAN labels are identifiers; their numeric mean therefore needs particular scientific scrutiny. This lesson describes the implemented historical method rather than presenting label arithmetic as a generally validated physical observable.

`fit_historical_tg()` fits `C/2 * (1 - tanh(s*T - d)) - 1` and reports `Tg = d/s`. Bounds keep C and s positive, but the returned Tg is not constrained to lie inside the sampled interval. A numerical fit should be inspected along with the response, diagnostics and assumptions.

## 5. Preserve outputs and aggregate replicas

`build_conformational_state_dataframe()` links chain identity, original frame, temperature, PCA scores and final labels. `run_tg_analysis()` writes those records, optimisation diagnostics and `analysis_summary.json`; figure/report generation is optional. Plotting uses results, but much of it currently shares the orchestration module.

`run_system_tg_analysis()` loads completed replica summaries and temperature responses. It computes the mean of independently fitted Tg values, sample SD and SEM. It does not pool trajectories or refit a shared curve. Automatic discovery may skip invalid replicas, whereas explicitly requested invalid inputs raise errors. The core aggregation lesson adds compatibility checks before calling this function.

## Exercise

Run the adjacent script and trace the selected component count and min_samples to their CSV diagnostics. Compare two replicas: which settings stayed constant, which were optimised independently, and which observations support compatibility? Inspect the fitted curve before interpreting the scalar Tg.

**Review questions:** Does equal PCA dimensionality establish comparable axes? Does the fitting routine return fit uncertainty from its covariance? **Answers:** No; each chain has its own fitted transform. The current routine discards the covariance returned by curve_fit, so it does not report that uncertainty.

## Function reading

Read [simulation_loader](../reference/analysis__simulation_loader.md), [descriptors](../reference/analysis__descriptors.md), [pca](../reference/analysis__pca.md), and all modules beginning `analysis/tg_analysis` in the [coverage index](../reference/coverage_index.md). Every optimisation helper, plotting function, return-record class and workflow function has a source-derived entry.
