# WP4 — Notebook 13: enzyme–PHA results (read-only presentation layer)

**Prepend:** `dev_plan/01_rules_for_claude_code.md` · **Branch:** `dev/wp4-nb13` (from WP2)

**Goal:** one notebook that turns the existing research outputs (four systems: GK13/ANC45 × P3HO_4/P3HB_4, 0–1000 ns) into the presentation's results section. **It computes nothing from trajectories.** It reads CSVs written by `md_simulation_scripts/enzyme_pha_analysis/enzyme_pha_analysis.ipynb` (R8: do not modify that notebook).

## Step 0 — Discover inputs, then stop and report
Using `ipha_paths.enzyme_system_dir(...)` and `enzyme_analysis_root()` from WP2, list what exists:
- per system `analysis/`: files matching `*_research_0_1000ns_*` (expected: `total_energy`, `protein_backbone_rmsd`, `enzyme_pha_min_distance`, `residue_pha_distances_A`, `residue_pha_residues`, plus their `.png`/`.json`)
- shared `PHA_Enzyme/analysis/`: `enzyme_pha_research_0_1000ns_*` (within-cutoff comparison, figure 5 occupancy, figure 6 contacts)

Report the exact filenames and column headers (first line of each CSV). **Wait for approval before building the notebook.** The names above were inferred from printed output and may differ.

## Notebook structure: `notebooks/13_enzyme_pha_results.ipynb`
1. **Question** (markdown). Do the MD simulations reproduce the experimental observation that GK13 and ANC45 recognise P3HO but not P3HB? Leave a citation placeholder: `TODO(Zhiwen): reference`.
2. **Systems and provenance** (table). Enzyme, polymer, simulated time, sampling interval, trajectory used (`processed_protein_centered.xtc`), who produced it (research notebook + date from its JSON summary). Add one line stating how the complexes were built. **Leave it as `TODO(Zhiwen)`**: the build route (HADDOCK pose? CHARMM-GUI? force field?) is not documented in the repo.
3. **Global stability.** Backbone RMSD for the 4 systems in a 2×2 grid with a shared y-axis. Summary table: mean, SD, final-20% mean.
4. **Proximity.** Minimum enzyme–PHA heavy-atom distance (PBC-aware, from the CSV), 2×2 grid with shared y. Table: mean, SD, final-20% mean, % time ≤ 3.5 Å, ≤ 5 Å, ≤ 10 Å.
   - Uncertainty: split 0–1000 ns into five 200-ns blocks and report the block mean ± SD of "% time ≤ 5 Å". Label this "variation within one trajectory, not replica uncertainty".
5. **Where it binds.** Top 10 residues by contact occupancy (≤ 3.5 Å) per system, from the existing figure-5 CSV. Mark the catalytic triad residues (GK13: Ser139/Asp195/His227; ANC45: Ser138/Asp194/His226, from the NB11 table).
   - **First verify** that these resids exist with the expected residue names in `residue_pha_residues.csv`. If they don't match (numbering offset), stop and report; don't guess.
6. **Catalytic serine proximity.** Per system, the Ser–PHA distance time series from the residue-distance CSV, and % time ≤ 3.5 Å.
7. **Summary table** (one row per system) and a **three-sentence answer** in markdown, which Zhiwen will edit. The template must state direction, magnitude and n = 1.
8. **Limitations** (markdown). n = 1 per system. Starting poses: TODO(Zhiwen). Force field as in the 06C caveat, if the same route was used: TODO(Zhiwen) confirm. Contact is not affinity. No free-energy estimate.

## Style
- Colours: P3HB₄ blue, P3HO₄ orange, as in the research notebook's Figure 4/5. Use the same enzyme order everywhere: GK13, ANC45.
- Figures are displayed inline. They are saved only when `SAVE_FIGURES = True` (default `False`, so demo-mode Run All writes nothing). Save to a new folder, `examples/output/presentation_figures/`, as PNG (300 dpi) and SVG, one file per figure, with descriptive names; refuse to overwrite existing files.
- Every number shown in markdown must be computed in a cell, not typed.

## Consistency check (must pass)
Recompute mean, SD and final-20% mean of backbone RMSD and minimum distance from the CSVs. They must match the values printed in the research notebook to 1e-3 Å:

| System | RMSD mean | MinDist mean | MinDist SD | MinDist final 20% |
|---|---:|---:|---:|---:|
| GK13_P3HO_4 | 1.6535 | 8.1787 | 11.0233 | 10.0559 |
| GK13_P3HB_4 | 2.3606 | 22.1097 | 15.2572 | 25.4576 |
| ANC45_P3HO_4 | 2.5093 | 8.4539 | 12.4673 | 22.6743 |
| ANC45_P3HB_4 | 2.4210 | 25.0709 | 15.3694 | 23.5907 |

If they don't match, stop: it means a different window, stride or file.

## Acceptance
- [ ] Step 0 report approved before build
- [ ] Notebook runs top to bottom in < 60 s with `ipha_clean`; opens no `.xtc`/`.edr`
- [ ] Consistency table matches (show it in the notebook as an assert cell)
- [ ] Triad residue check reported (match / offset)
- [ ] All TODO(Zhiwen) items listed in the final report
