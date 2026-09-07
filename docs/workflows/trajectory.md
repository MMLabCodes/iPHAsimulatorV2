# Trajectory preprocessing

**Inputs:** a matching GROMACS trajectory, topology and index. **Outputs:**
centered/wrapped coordinates, an optional fitted trajectory and a representative
frame. These helpers require GROMACS but do not launch MD production.

## 1. Choose exactly the intended trajectory

For an existing merged XTC, use that file alone. Do not concatenate it with the
continuations from which it was made. Filenames do not establish time coverage.

For unmerged restart outputs, inspect the merge plan first:

```bash
python -m iphasimulator.trajectory_gromacs_merge /path/to/system --dry-run
```

The merge module discovers supported `step7_production` / `step8_production_2us`
patterns, orders continuation parts numerically and checks inputs/outputs with
GROMACS. It is not a generic arbitrary-filename merger.

## 2. Plan preprocessing

```python
from pathlib import Path
from iphasimulator.trajectory_preprocessing import preprocess_gromacs_trajectory

system_dir = Path("/path/to/system")
outputs = preprocess_gromacs_trajectory(
    system_dir,
    trajectory="step7_production.xtc",
    structure="step7_production.tpr",
    index="index.ndx",
    workflow_type="polymer",
    fit=False,
    dry_run=True,
)
print(outputs.analysis_trajectory_path)
```

This dry run skips GROMACS commands, but it can create/reuse `center.ndx` and
therefore requires a valid source index. The default polymer centering group is
derived from `PHA`; pass suitable `source_groups` if your index differs.

## 3. Produce and inspect processed coordinates

Review output paths first, then change `dry_run=False` to run the commands.
The full `System` group is retained, while the selected group controls centering.
Inspect a representative frame to ensure molecules are reconstructed correctly.

Use centering/wrapping for the basic polymer structure analysis in notebook 09.
Fitting is optional and appropriate only for analyses that need it. For
[periodic enzyme–PHA distances](analysis.md), use unfitted coordinates and their
same-frame box; fitting coordinates without transforming the box invalidates
that minimum-image calculation.

Notebook: [08 trajectory preprocessing](../notebooks.md#execution-and-analysis).
API: {py:func}`iphasimulator.trajectory_preprocessing.preprocess_gromacs_trajectory`,
{py:func}`iphasimulator.trajectory_gromacs_merge.merge_simulation_outputs`.
