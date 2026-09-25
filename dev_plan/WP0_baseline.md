# WP0 — Baseline and safety net

**Prepend:** `dev_plan/01_rules_for_claude_code.md`
**Why:** everything after this edits notebooks. We need a restorable reference state and a record of the environment.

## Tasks
1. Report `git status`. If there are uncommitted changes, **stop and show them**; do not commit on the user's behalf without approval.
2. Create the annotated tag `pre-presentation-baseline` on the current `main` HEAD (local only; no push unless asked).
3. Export the environment without changing it:
   - `conda env export -n ipha_clean --no-builds > dev_plan/env_ipha_clean_2026-09.yml`
   - Record `gmx --version | head -1`, `antechamber -h | head -3` (or the AmberTools version) and the Python version in `dev_plan/env_versions.txt`.
4. Run `pytest -q` and save the summary line to `dev_plan/baseline_pytest.txt`.
5. Write `dev_plan/baseline_notebooks.csv` with these columns: notebook, kernelspec name, n_cells, n_code_cells, n_executed_cells, n_error_outputs, sha256 of the file. Include `notebooks/*.ipynb` and `md_simulation_scripts/**/*.ipynb`. Use a small Python script; do not execute notebooks.

## Acceptance
- [ ] Tag exists and points to HEAD of `main`
- [ ] The three baseline files exist and are non-empty
- [ ] No existing file modified (`git status` shows only new `dev_plan/` files)
