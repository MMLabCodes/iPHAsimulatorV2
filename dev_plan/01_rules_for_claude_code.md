# Rules for Claude Code — read before every work package

You are working in the iPHASimulator v2 repository (`/Users/k20098771/opt/iPHASimulator_v2`). It is a PHA (polyhydroxyalkanoate) oligomer builder and MD-preparation toolkit: RDKit → AmberTools/GAFF2 → GROMACS/OpenMM, plus trajectory analysis. The design and rationale are in `dev_plan/00_project_design.md`; read §1–§3 first.

The user is a computational biophysics postdoc. Be concise and technical. Separate facts, inferences and assumptions.

## Working method
- **R1 Plan first.** Before editing, list the files you will change and, for each, the exact change. Wait for approval.
- **R2 One WP per branch.** Work on `dev/<wp-id>` (e.g. `dev/wp1-consistency`), branched from the WP0 tag or the previous WP's merged state. One logical change per commit. Messages look like `WP1: fix NB11 benchmark path`.
- **R3 Notebook edits.** Edit `.ipynb` files with `nbformat` (read → modify cell source → write), or with the VS Code notebook editor. Never hand-edit the JSON text. **Preserve existing outputs** unless the WP says to re-execute. Keep `kernelspec` = `ipha_clean` (display name as in notebook 01).
- **R4 Minimal diff.** Change only what the WP lists. No reformatting, renaming, reordering or "improvements" outside scope. If you see another problem, write it under "Out-of-scope findings" in your report instead of fixing it.

## Hard limits (flag, don't fix)
- **R5** Do not change physics or chemistry defaults in `src/`: MDP templates (`src/iphasimulator/data/gromacs_mdp/`), water/ion files (`data/gromacs_solvation/`), GAFF2/charge settings, stereochemistry rules in `build.py`/`stereochemistry.py`, `-maxwarn` usage. Method limitations get documented, not changed.
- **R6** Do not run antechamber, tleap, gmx, sbatch or OpenMM simulations, and do not re-execute notebooks unless the WP explicitly says so.
- **R7** Never delete or overwrite anything under `examples/output/` or `/Users/k20098771/Data/`. New outputs must use new filenames.
- **R8** Do not modify `md_simulation_scripts/` (the research layer). Read from it only.
- **R9** Do not add dependencies beyond what `ipha_clean` already has. Check with `python -c "import X"` first.

## Verification (every WP)
- **R10** Run `pytest -q` before and after. Report both results. New failures block the WP.
- **R11** For every changed notebook, report its code-cell count and the unchanged/changed cell indices, and confirm with `nbformat.validate` that it still parses.
- **R12** Finish with a report: files changed · acceptance checklist (each item ✅/❌ with evidence) · out-of-scope findings · anything you were unsure about.

## Stop and ask when
- an acceptance criterion cannot be met without breaking R5–R9;
- a path, file or group name in the brief doesn't exist in the repo;
- a fix would change a numerical result or a generated filename.
