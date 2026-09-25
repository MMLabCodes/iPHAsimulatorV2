# iPHASimulator v2 — project design for the collaborator presentation

Written: 2026-09-24 · Target: collaborator presentation in ~4 weeks (late Oct 2026)
Owner: Zhiwen Zhong · Implementation: Claude Code in VS Code, one work package (WP) at a time

---

## 1. Goal and constraints

**Goal.** A live demo. Zhiwen presents and the collaborators watch. It should show:
1. **Capability:** iPHASimulator builds stereochemically defined PHA oligomers and takes them to MD-ready GROMACS/OpenMM systems.
2. **Result:** enzyme–PHA MD agrees qualitatively with the experimental expectation that GK13/ANC45 bind P3HO and not P3HB.

**Constraints (decided 2026-09-24)**
- Audience: demo only. Collaborators do not run the notebooks. Portability is secondary.
- Science: **flag, don't fix.** Keep the current methods (force field, MDP, stereochemistry rule). Add explicit caveats instead. No simulation is re-run.
- Available data: GK13/ANC45 × P3HO_4/P3HB_4, 0–1000 ns each, with processed trajectories and CSVs. The six polymer-only benchmark productions are **not** complete. There is no SwiftPol comparison.
- All notebooks 01–12 already run on Zhiwen's Mac (`ipha_clean` kernel).

## 2. Current state

### 2.1 Two layers that don't talk to each other
| Layer | Location | State |
|---|---|---|
| Teaching workflow | `notebooks/01–12` | Runs. Shows the pipeline for one system (P3HB_4). Insight only in 09 (single polymer) and 12 (single complex, raw trajectory). |
| Research analysis | `md_simulation_scripts/` (`trajectory_preparation/`, `enzyme_contacts/`, `enzyme_pha_analysis/`) | 4 enzyme systems, processed trajectories, PBC-aware minimum distance, residue contact occupancy, snapshots. This is where the results are. |

The presentation needs one path from 01 to the research figures. Notebook 11 ends at a manual HADDOCK step, and 12 analyses one system with a method that the research notebook already supersedes.

### 2.2 Headline numbers already computed (research notebook, 0–1000 ns, stride 0.1 ns, one replica per system)
| System | Backbone RMSD mean (Å) | Min enzyme–PHA heavy-atom distance mean ± SD (Å) | Final 20% mean (Å) |
|---|---:|---:|---:|
| GK13 + P3HO_4 | 1.65 | 8.2 ± 11.0 | 10.1 |
| GK13 + P3HB_4 | 2.36 | 22.1 ± 15.3 | 25.5 |
| ANC45 + P3HO_4 | 2.51 | 8.5 ± 12.5 | 22.7 |
| ANC45 + P3HB_4 | 2.42 | 25.1 ± 15.4 | 23.6 |

**Interpretation, provisional:**
- P3HO_4 stays about 3× closer to both enzymes on average than P3HB_4. The direction matches the experimental claim.
- ANC45 + P3HO_4 moves away in the last 20%.
- n = 1 per system, SDs are large, and residence is intermittent. This is **qualitative agreement, not a binding measurement**. Say so on the slide.

### 2.3 Known issues (from the 2026-09-24 review), classified
| # | Issue | Class | Handling |
|---|---|---|---|
| I1 | NB11 looks in `examples/output/md_tests/benchmark/`; NB10 writes `examples/output/benchmark/` | bug | fix (WP1) |
| I2 | NB11 `gro_to_pdb` writes all atoms (water, ions), not the polymer; no make-whole | bug | fix (WP1) |
| I3 | Dead references: `06_openmm_setup.ipynb`, `scripts/run_md_test_set.py`; `system_neutralized.gro` vs `step5_input.gro` wording; README omits 12 | docs | fix (WP1) |
| I4 | 05A markdown contradicts code (RUN flag default; `abcg2` described as AM1-BCC; "debug with gas") | docs | fix (WP1) |
| I5 | 06A/06D kernel "Python 3", not `ipha_clean` | metadata | fix (WP1) |
| I6 | Hardcoded `/Users/k20098771/Data/...` in 08, 09, 12 (08 markdown path ≠ code path) | portability | centralise (WP2) |
| I7 | Run All in 05A/06B/06C regenerates outputs (slow; overwrites) | demo risk | demo-mode flags (WP2) |
| I8 | Water/ions are CHARMM TIP3P + CHARMM-GUI SOD/CLA with a GAFF2 solute; no `DispCorr` | method | **caveat only** (WP3) |
| I9 | `-maxwarn 1` in every grompp call, though current logs have no warnings | method | caveat only (WP3) |
| I10 | Custom-monomer rule accepts CIP label R. For side chains that outrank the backbone (vinyl, isopropyl, CH2OMe) this is the mirror spatial configuration of natural units | method | caveat + read-only diagnostic (WP3) |
| I11 | 06D is a template: `amber14-all.xml` has no PHA template | scope | caveat (WP3) |
| I12 | NB10 "29/29 checks" = file existence, not physical validation | wording | caveat (WP3) |
| I13 | NB09: single replica, no equilibration discard, no error bars; end-to-end pair chosen by atom order | method | caveat (WP3) |
| I14 | NB12 polymer RMSD from the raw trajectory: 40–90 Å frame-to-frame jumps late in the run are most likely PBC image jumps (est. ~85%) | **analysis artefact** | caveat in 12 and point to research results (WP3/WP4). Decision D1 |
| I15 | Mode B naming `PHA_C5_4_R` for a molecule identical to `P3HO_4`; Mode C name lacks `_` | naming | caveat (WP3); optional fix is D3 |

## 3. Target architecture

```
notebooks/
  00_start_here.ipynb           NEW  storyline, workflow map, "what is demo vs. template", links
  01–04  build & validate       unchanged logic; wording fixes
  05A/05B parameterise          wording fixes; demo-mode flags
  06A–06D engine setup          kernel/wording fixes; caveats
  07     HPC                    wording fixes
  08–09  polymer analysis       paths via config; caveats
  10     benchmark tracker      caveat on what "checks" mean
  11     docking prep           bug fixes (path, polymer-only PDB)
  12     single-run diagnostic  caveat: raw trajectory; point to 13
  13_enzyme_pha_results.ipynb   NEW  read-only: loads research CSVs/PNGs for 4 systems → presentation figures
notebooks/ipha_paths.py (or config/paths.yaml)  NEW  one place for DATA_ROOT and system folders
dev_plan/                       this plan and the Claude Code briefs
```

Design rules:
- **Demo mode by default.** Every expensive or side-effect cell (antechamber, GROMACS, sbatch, trajectory reads) is behind a flag that defaults to `False`. "Run All" then shows saved results in seconds. This follows the `RUN_ANALYSIS=False` pattern already used in `enzyme_pha_analysis.ipynb`.
- **No new analysis code in notebooks.** 13 reads CSVs that `md_simulation_scripts/enzyme_pha_analysis` has already written. It does not recompute.
- **Caveats are visible.** Each notebook with a method limitation ends with a short `## Method notes and limitations` markdown cell.
- **`src/` physics is untouched.** No change to force-field files, MDP templates, builder stereochemistry or charge methods.

## 4. Work packages and schedule

| Week | WP | Title | Effort | Depends on |
|---|---|---|---|---|
| 1 | WP0 | Baseline and safety net | 0.5 d | – |
| 1 | WP1 | Consistency and bug fixes (I1–I5) | 1 d | WP0 |
| 1 | WP2 | Central paths and demo-mode flags (I6–I7) | 1 d | WP1 |
| 2 | WP3 | Method caveats and read-only stereo diagnostic (I8–I15) | 1 d | WP1 |
| 2 | WP4 | Notebook 13: enzyme–PHA results bridge | 1.5 d | WP2 |
| 3 | WP5 | `00_start_here` and presentation storyline | 1 d | WP3, WP4 |
| 3 | WP7 | *Optional:* polymer-only benchmark analysis (only if D2 = yes) | 2 d + HPC | WP2 |
| 4 | WP6 | Verification, freeze and rehearsal | 1 d | all |

The briefs in this folder are written so each one can be pasted into Claude Code as-is. Always prepend `01_rules_for_claude_code.md`.

## 5. Decisions still open

**D1: Notebook 12, flag only vs. switch to processed trajectory.**
- (a) Flag only (current default). Add a caveat and point to 13. *Pro:* zero method change, consistent with "flag, don't fix". *Con:* a teaching notebook keeps showing a misleading plot.
- (b) Also point 12 at `analysis/processed_protein_centered.xtc` and add the PBC-aware minimum distance, reusing the research code. *Pro:* 12 becomes correct and teachable. *Con:* this is an analysis change, about 0.5 d more.
- Prefer (b) if 12 will be shown on screen; (a) if it is skipped in the demo.

**D2: Polymer-only benchmark (6 systems).**
- (a) Drop it from the presentation and mention it as ongoing.
- (b) Submit the 6 × 100 ns runs now (scripts exist), then do WP7 in week 3.
- (b) is only worth it if HPC turnaround is under about 10 days. It adds the "side-chain length and DP vs. Rg/SASA" result.

**D3: Mode B/C naming (I15).** Leave it and add a caveat, or normalise names (a small change to `workflows/design.py` plus tests; changes output filenames).

**D4: Replicas.** n = 1 per enzyme system. For the talk, state it as a limitation. For a paper, 3 replicas per system is the minimum defensible design. This is outside the 4-week scope.

## 6. Risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| A live demo cell hangs (antechamber ~100 s, GROMACS) | high without WP2 | demo-mode flags; pre-executed notebooks |
| Collaborator asks about force-field consistency (I8) | medium | caveat slide with the exact composition; state it as a known limitation and planned change |
| Collaborator reads a 10 Å distance difference as "binding" | medium | show the time-within-cutoff figure plus n = 1 caveat; avoid the word "affinity" |
| Claude Code edits notebooks and loses saved outputs | medium | WP0 git tag; rule R3 (edit JSON via nbformat, keep outputs) |
| Research CSV paths move | low | WP2 config; WP4 fails with a clear message |
