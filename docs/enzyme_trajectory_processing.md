# Enzyme–PHA trajectories: edit instructions, then Run All

This workflow reads YAML from the existing **`analysis/instrcution.txt`** (the
filename spelling is retained). It reduces an XTC trajectory, optionally applies
explicit PBC/centring/fitting settings, and prepares matching files for VMD.
It never launches MD, changes raw simulation files, watches files or opens VMD.

## 1. Open the notebook

Use {download}`01_GK13_PHO4_trajactory_process.ipynb <../md_simulation_scripts/01_GK13_PHO4_trajactory_process.ipynb>`.
Select a Python environment with this repository and the analysis dependencies:

```bash
python -m pip install -e '.[analysis]'
gmx --version
```

The locally validated environment is `ipha_clean`. Select that environment in
your notebook editor. If using JupyterLab and it is not listed, register it once
from that environment with `python -m ipykernel install --user --name ipha_clean`.
The only notebook setting is `INSTRUCTION_FILE`, already pointing to:

```text
/Users/k20098771/Data/MD_projects/PHA/MD_data/gromacs/PHA_Enzyme/GK13_P3HO_4_gromacs/analysis/instrcution.txt
```

## 2. Edit the instruction file

The original prose is preserved alongside it as `instrcution.original.txt`.
The reusable template is
{download}`enzyme_trajectory_GK13_P3HO_4.yaml <../examples/enzyme_trajectory_GK13_P3HO_4.yaml>`.
Its paths assume it has been copied into the system's `analysis/instrcution.txt`.

```yaml
schema_version: 1
input_trajectory: ../production_combined_1us.xtc
structure: ../step6.2_npt.tpr
index: ../index.ndx
stride: 100
pbc: none
center: false
center_group: SOLU
fit: none
fit_group: enzyme_ca
output_group: SYSTEM
custom_groups:
  enzyme: protein
  enzyme_ca: protein and name CA
  pha: resname LIG
output_dir: processed
prepare_vmd: true
overwrite: false
dry_run: false
gmx: gmx
```

All relative file paths, including `output_dir` and an explicit executable path,
resolve from the instruction file's directory. Thus `processed` means
**`analysis/processed/`**, regardless of where you launched Jupyter or the CLI.

| Setting | Meaning / accepted values |
| --- | --- |
| `input_trajectory` | Existing XTC; use the combined file alone, not its continuation parts as well |
| `structure` | Matching TPR or GRO with exactly the same atom count/order; TPR required for `mol`/`whole` |
| `index` | Existing GROMACS NDX with valid, nonempty atom groups |
| `stride` | Positive integer: keep zero-based frames 0, stride, 2×stride, …; times/steps are preserved |
| `pbc` | `none`, `mol`, `whole`, `res`, `atom`; no automatic choice |
| `center` / `center_group` | Boolean and exact index/custom-group name; group required when enabled |
| `fit` / `fit_group` | `none`, `rot+trans` or `translation`, with an explicit group when enabled |
| `output_group` | Exact group name controlling retained atoms and their order |
| `custom_groups` | Optional names mapped to explicit MDAnalysis selection expressions |
| `output_dir` | Dedicated result directory, outside all input files |
| `prepare_vmd` | Boolean; create `view.vmd`; matching `viewing.gro` is always written |
| `overwrite` | Default `false`; `true` archives a previous result from this workflow before replacement |
| `dry_run` | Boolean; validate first-frame metadata/groups/tools and return the plan without writing anything |
| `gmx` | Executable name or path, without shell arguments |

Unknown or duplicate YAML keys, quoted booleans, empty/unknown selections, invalid
indices and inconsistent atom counts are rejected. Use `none` for disabled PBC or
fitting, and unquoted `true`/`false` for boolean settings.

`stride: 100` selects **frames**, not every 100 ps. The first inspected frames in
this example are at 0, 100 and 200 ps; the reduced spacing is consequently 10,000 ps
where the source spacing remains regular. `frames.csv` records the actual choices.

## 3. Use the inspected atom groups

The supplied `index.ndx` contains only these groups (names are case-sensitive here):

| Existing group | Atom count | Inspected contents / use |
| --- | ---: | --- |
| `SOLU` | 3,800 | Protein atoms 1–3701 plus 99 `LIG` atoms 3702–3800; candidate centre for the complex |
| `SOLV` | 133,560 | Solvent/ions; usually not an enzyme alignment group |
| `SYSTEM` | 137,360 | Entire simulation; initial output choice |

The explicit `custom_groups` above add `enzyme` (3,701 protein atoms), `enzyme_ca`
(245 protein Cα atoms, a candidate alignment group) and `pha` (99 `LIG` atoms).
They are resolved from the supplied topology, then saved in a separate output
index as needed. The original NDX is never amended. No default GROMACS group
numbers, `Protein` group or automatic “centre if necessary” decision is assumed.

Both `step6.2_npt.tpr` and `step7_production.tpr` have the same atom names, residue
names and residue numbers in the same order as `step7_production.gro`. The example
uses `step6.2_npt.tpr`. An XTC itself contains coordinates, not atom identities;
matching counts cannot independently prove its topology provenance. For another
system, supply its matching files and check the reported group contents.

## 4. Save and run

Set `dry_run: true` for a read-only plan, save, and select **Run All**. Then set
`dry_run: false`, save, and Run All to process. No notebook edits are needed.

The command-line route uses exactly the same implementation:

```bash
python -m iphasimulator.trajectory_processing /absolute/path/to/instrcution.txt --dry-run
python -m iphasimulator.trajectory_processing /absolute/path/to/instrcution.txt
# After installing this checkout, the equivalent console command is:
ipha-process-trajectory /absolute/path/to/instrcution.txt
```

The CLI `--dry-run` takes precedence over YAML. Dry runs inspect the topology and
first XTC frame, without scanning/processing the complete trajectory or writing
offset caches, logs or output folders. Existing-output conflicts still cause a
validation error. A successful dry run is not a complete corruption check.

GROMACS streams processing with `-skip`. PBC/centring happens before the separate
optional fitting stage. All atoms are retained until fitting is complete, so
the original topology and fit indices remain valid even for a subset output.
Supported PBC modes operate per frame; history-dependent `nojump` and iterative
`cluster` are deliberately rejected. For details see the
[GROMACS trjconv reference](https://manual.gromacs.org/current/onlinehelp/gmx-trjconv.html).

The final validation streams through raw and output frames, checking atom counts,
finite coordinates, strictly increasing source times, frame stride, times and
steps. For the initial untransformed run it also checks retained coordinates and
box vectors within XTC precision. Memory scales with atoms per frame, not the
number of trajectory frames. GROMACS logs stream directly to disk.

## 5. Inspect outputs in VMD

| Output | Purpose |
| --- | --- |
| `processed.xtc` | Reduced trajectory, with configured transformations/subset |
| `viewing.gro` | First processed frame with matching atom identities/order |
| `view.vmd` | Portable loader resolving files beside the script, independent of terminal directory |
| `frames.csv` | Output frame → original frame, time in ps and simulation step |
| `settings.yaml`, `instruction_used.txt` | Resolved settings and exact instruction snapshot |
| `selections.ndx` | Original input atom numbers used for processing; **not** a reindexed subset topology |
| `command_*.json`, `command_*.stdout.log`, `command_*.stderr.log` | Actual commands, group input, return codes and logs |
| `summary.json` | Completion status, versions, input sizes/mtimes, group counts and verification results |
| `unfitted.xtc` | Only for fitted runs: full-atom reduced intermediate before fitting |

Run `vmd -e /absolute/path/to/analysis/processed/view.vmd` yourself. The script loads
the GRO and XTC and removes the duplicate GRO coordinate frame. In VMD, select
`protein or resname LIG` to view this pair and `resname LIG` to inspect the ligand.
Scrub through the reduced trajectory, including its first and last frames. Check
for broken molecules, box crossings and whether the pair is useful to view.
**Preparing these files does not perform visual inspection.**

If your inspection calls for centring, change these settings and rerun:

```yaml
pbc: mol
center: true
center_group: SOLU
fit: none
output_dir: processed_centered
```

If only the enzyme should define the centre, explicitly choose `enzyme` instead.
Centring the complex does not keep an unbound ligand attached or guarantee all
components use the same periodic image. Inspect again. If you need alignment,
choose `fit: rot+trans`, `fit_group: enzyme_ca` and another output directory.
Rotated/fitted coordinates with unrotated box vectors are unsuitable for periodic
enzyme–PHA contact calculations; keep the unfitted/raw trajectory for that use.

## Reruns and failures

By default an existing output directory causes an error. Prefer a new
`output_dir` for changed treatment. To repeat intentionally in the same location,
set `overwrite: true`: only a directory identified by this workflow's summary is
eligible; the old result moves to `processed.backup-<id>` after the new result
passes validation. No previous result or unrelated folder is deleted.

Work takes place in a sibling `.processed-<id>` staging folder. Failure preserves
its command logs/failed summary and leaves an earlier completed output intact.
Actual command logs contain that staging path; the summary plan lists the final
paths. A `.processed.lock` prevents concurrent runs targeting the same directory.
After a forcibly killed kernel, remove that lock only after checking that no
processing job is still running. Inputs are opened read-only and their sizes and
modification times are checked before/after processing.

API: {py:func}`iphasimulator.trajectory_processing.load_config`,
{py:func}`iphasimulator.trajectory_processing.process_trajectory`.

## Validation completed for GK13–P3HO₄

On 14 September 2026, using GROMACS 2023.2 and the `ipha_clean` environment:

- **53 tests passed** across the new configuration workflow and existing trajectory
  preprocessing/merge tests. These cover strict parsing, instruction-relative
  paths, read-only dry runs, actual GROMACS stride/subset behaviour, matching GRO
  atom order, centring/fitting command order, invalid selections, overwrite archives
  and preservation of an earlier output after a failed replacement.
- A **205-frame sample** of this system reduced to frames **0, 100, 200** with
  coordinates and boxes preserved. Another sample run exercised molecule PBC,
  centring, fitting and a 3,800-atom `SOLU` output.
- The **unchanged notebook executed both code cells successfully** with the
  instruction file above, after a successful CLI dry run.
- The full input had **14,806 frames**; output contains **149 frames**, **137,360
  atoms**, from **0 to 1,480,000 ps** at the selected frames. Its size is
  **75,980,140 bytes** (about 76 MB), compared with the 7,550,069,852-byte source.
  Despite the `1us` filename, the source extends beyond 1 µs.
- The full run kept PBC correction, centring and fitting **disabled**. Streaming
  verification confirmed stride, times/steps, coordinates and boxes. Input sizes
  and modification times remained unchanged; the instruction backup hash matched.

Results are in the example system's `analysis/processed/`; its `summary.json` and
`frames.csv` contain the measured details. Local test artifacts and an executed
notebook copy are under ignored `examples/output/trajectory_validation/`.
VMD loading files were prepared; **no VMD visual inspection was performed**.
