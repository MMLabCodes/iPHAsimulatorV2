# WP7 — (Optional, only if decision D2 = yes) Polymer-only benchmark analysis

**Prepend:** `dev_plan/01_rules_for_claude_code.md` · **Branch:** `dev/wp7-polymer-benchmark`

**Precondition:** production runs for all six systems (`P3HB_4, P3HB_8, P3HO_4, P3HO_8, P3HDD_4, P3HDD_8`) are finished and copied under `DATA_ROOT`. Zhiwen submits them via NB10 or the cluster; Claude Code does not submit jobs (R6). If fewer than six are available, build the notebook for the ones present and mark the others missing.

## Step 0 — Inventory (stop and report)
For each system: the location of `step7_production.xtc/.tpr/index.ndx`, simulated time (`gmx check` or read from the XTC), and whether NB08 preprocessing outputs exist. Propose where to add these paths in `ipha_paths.py`.

## Step 1 — Preprocessing
Use the existing `iphasimulator.trajectory_preprocessing.preprocess_gromacs_trajectory` exactly as NB08 does (centre on `[ center ]`, `-pbc mol -ur compact`, no fit). This step runs `gmx trjconv`, so it needs Zhiwen's explicit go-ahead per system (R6 exception, scoped to this command only). New outputs go next to the raw files, with NB08's filenames. Refuse if they already exist.

## Step 2 — `notebooks/14_polymer_benchmark_comparison.ipynb`
- Load with `mdtraj.load(..., stride=S)`, S chosen so there are ~1000 frames per system (report S).
- Discard the first 10 ns as equilibration. Make this a parameter, and show the Rg time series with the cut marked.
- Metrics per system: Rg (geometric, polymer atoms from `[ center ]`), end-to-end distance between the two terminal **heavy** atoms (terminal hydroxyl O and carboxyl C; identify them from the topology bonds, not by atom order), polymer-only SASA (Shrake–Rupley, same settings as NB09).
- Uncertainty: block averaging (5 blocks), reporting mean ± SEM, and the autocorrelation time of Rg (report it; if it exceeds block length/2, say the SEM is underestimated).
- Figures: (a) Rg distributions, overlaid per DP; (b) mean Rg vs side-chain carbons (1, 5, 9) with DP 4 and DP 8 as two series; (c) SASA per repeat unit vs side-chain carbons.
- Limitations cell: one replica per system; FF composition (same text as the 06C caveat); oligomers, not polymer melts.

## Acceptance
- [ ] Inventory approved
- [ ] Preprocessing run only with explicit approval; no existing file overwritten
- [ ] Notebook runs in demo mode from saved CSV outputs in < 60 s (it computes and saves CSVs only when `RUN_ANALYSIS=True`)
- [ ] Block/autocorrelation numbers reported per system
