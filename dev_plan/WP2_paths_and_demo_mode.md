# WP2 — Central paths and demo-mode flags (issues I6–I7)

**Prepend:** `dev_plan/01_rules_for_claude_code.md` · **Branch:** `dev/wp2-demo-mode` (from WP1)

**Goal:** during the live demo, "Run All" on any notebook finishes quickly and shows the saved results. Nothing expensive runs and no existing output is overwritten. External data paths are defined in one place.

## A. One place for external data paths
Create `notebooks/ipha_paths.py`, importable from notebooks because they run with cwd = `notebooks/`. Keep it small and dependency-free:
- `DATA_ROOT`: from env var `IPHA_DATA_ROOT`, defaulting to `/Users/k20098771/Data/MD_projects/PHA/MD_data`.
- `polymer_test_dir(system_name)` → `DATA_ROOT / "gromacs" / "test" / system_name` (used by 08, 09)
- `enzyme_system_dir(enzyme, polymer)` → `DATA_ROOT / "gromacs" / "PHA_Enzyme" / f"{enzyme}_{polymer}_gromacs"` (used by 12, 13)
- `enzyme_analysis_root()` → `DATA_ROOT / "gromacs" / "PHA_Enzyme" / "analysis"`
- `require(path, hint)`: raises `FileNotFoundError` with a one-line hint, for use in notebooks.

Replace the hardcoded `Path("/Users/k20098771/...")` in NB08 cell 4, NB09 cell 2 and NB12 cell 3 with these helpers. The resulting paths must be **identical** on Zhiwen's machine: assert this in a temporary check and report it. Fix the NB08 markdown (cell 5), which currently gives a different path from the code.

## B. Demo-mode flags (default `False`; existing outputs are displayed instead)
| Notebook | Cell | Current | Change |
|---|---|---|---|
| 05A | 8 | `RUN_GAFF2 = True` | `False`; the else-branch prints where the existing prmtop/inpcrd are |
| 06B | 4 | `RUN_GROMACS_CONVERSION = True` | `False` |
| 06C | 4 | `write_gromacs_solvation_files(..., clean=True)` runs unconditionally | wrap in `WRITE_SOLVATION_FILES = False`; when False, list the existing files in `solvated_polymer/` |
| 06C | 6 | `RUN_GROMACS_SOLVATION = True` | `False` |
| 08 | 10 | calls `preprocess_gromacs_trajectory(... dry_run=not have_required_inputs)` | add `RUN_PREPROCESSING = False`; pass `dry_run=not (RUN_PREPROCESSING and have_required_inputs)`. First check in `src/iphasimulator/trajectory_preprocessing.py` that dry_run returns the same output paths without calling gmx. If it doesn't, stop and report |
| 09 | 5 | `md.load(xtc, top=gro)`, then `trajectory[::100]` | `md.load(xtc, top=gro, stride=ANALYSIS_STRIDE)` with `ANALYSIS_STRIDE = 100`. This selects the same frames (0, 100, 200, …) and avoids loading ~4.4 GB. **Verify** that frame count and times match the saved output (501 frames) before and after |
| 10 | 8 | auto-`sbatch` when available | add `ALLOW_SBATCH = False`; when False, print the command only |
| 12 | 7–16 | always recomputes energy/RMSD | add `RUN_ANALYSIS = False`; when False and CSVs exist in `OUTPUT_DIR`, load `total_energy.csv`, `protein_backbone_rmsd.csv` and `polymer_rmsd_relative_to_protein.csv` and re-plot. Same plotting code |

Every flag gets a one-line markdown note above it: `Demo mode: False shows saved results; set True to recompute (takes ~X).` Take X from the saved outputs where known (e.g. antechamber 107 s for P3HB_4).

## C. Must not change
Default numerical settings, filenames of outputs, `src/` behaviour, saved outputs of cells whose code you did not touch.

## Execution check (allowed in this WP)
Copy each changed notebook to `/tmp/ipha_wp2/` and execute the copy with `jupyter nbconvert --to notebook --execute --ExecutePreprocessor.kernel_name=ipha_clean --ExecutePreprocessor.timeout=600`, with cwd set to the repo's `notebooks/` so relative paths resolve. **Do not** overwrite the originals. Report the wall time per notebook.

## Acceptance
- [ ] `grep -rn "/Users/k20098771" notebooks/*.ipynb` returns only `ipha_paths.py` defaults (and none in code cells)
- [ ] Resolved paths identical to before (report old == new)
- [ ] Every changed notebook executes in demo mode without error; each takes < 60 s except 09 (report its time)
- [ ] 09 in demo mode reproduces the 501 analysis frames and the same Rg mean to 1e-6 nm as a direct computation on the old path
- [ ] No file under `examples/output/` or `DATA_ROOT` has a changed mtime (compare `find -newer` against a marker file created before the run)
