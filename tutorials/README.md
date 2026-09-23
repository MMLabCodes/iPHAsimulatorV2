# iPHAsimulator tutorials

Each lesson follows three steps: **get ready → run the task → check and view the result**.
Comments explain the inputs, units, outputs, and what to look for in each picture.
Start with the 16 core lessons below,
then follow the [seven advanced developer tutorials](advanced/README.md) to learn
how the implementation works and how to extend it. The accompanying
[function reference](reference/coverage_index.md) covers all 417 explicit function
definitions across the current package's 39 Python modules.

## Start here

Use the **scientific `iphasimulator` environment**, not the lightweight GUI
environment. These lessons currently require this source checkout: some backend
imports and generated scripts still depend on its layout.

If the scientific environment is already installed, activate it:

```bash
conda activate iphasimulator
```

For a new installation, start from the repository root and use the existing
environment specification:

```bash
conda env create -f environment.yml
conda activate iphasimulator
```

The specification does not currently list all analysis dependencies. For lessons
12–14, install these into the scientific environment if they are missing:

```bash
conda install -c conda-forge mdanalysis scikit-learn kneed matplotlib
```

Environment installation changes your environment; the tutorials do not install
dependencies automatically. External-tool availability can vary by operating
system. Use the instructor's tested environment where one is supplied.

Run the readiness check from the repository root:

```bash
python tutorials/core/00_setup_check_your_environment.py
```

It checks Python imports and selected external commands. Enable its melt or
analysis checks when you reach those lessons. Import checks are not execution
tests of AmberTools, Polyply, or a GPU.

## How to run a lesson

1. Open the lesson and read its short task description.
2. Run **1. Get ready** unchanged. A shared helper handles paths and environment checks.
3. Read the inputs in **2.** and change the values you want to explore.
4. Run **2.** to perform the task, then **3.** to check and view the result.

Run the `# %%` cells in order in a Python script editor, or run the whole file
with the scientific Python. **Running a whole lesson performs its task**, including
building files or starting a calculation where indicated. There are no extra run
switches to find. Do not import a lesson as a library: these are sequential exercises.
The long cooling analysis requires a supplied dataset; use A06 to view saved results.

Example:

```bash
python tutorials/core/03_polymer_prep_build_a_chain.py
```

Every lesson starts from saved inputs. You do not need variables left over from
another lesson or an open GUI. If a check stops the lesson, resolve the reported
problem before continuing. A file check establishes that an output exists; it
does not certify scientific validity.

### Pictures and plots

Chemistry lessons use the package's existing monomer and polymer drawing functions.
These are **2D chemical drawings**, not views of the built 3D coordinates. The system
lessons plot residue counts, and lesson 12 plots recorded temperature and energy.
Lessons 13–14 generate and show the package's analysis figures; A06 views saved ones.

Pictures appear inline in compatible IPython editors and notebooks. Every generated
picture is also saved: open the printed PNG path in any image viewer if your editor
does not display it. Workshop drawings/charts go in `figures/`; backend analysis
figures stay beside their analysis results. Repeating a drawing replaces its derived
PNG; scientific build and analysis outputs remain protected from replacement.

You do not need to edit either `workshop_helpers.py` loader or the files in
`_support/`. They contain the shared setup, file checks and plotting details.
Keep the tutorial folders together so these helpers can be found. When using an
editor, open the lesson as a saved file and include its directory on the Python
import path (script execution does this automatically); do not paste isolated cells
into an unrelated notebook directory.

## Your workshop files

By default, lessons use a separate directory in your home folder:

```text
~/iphasimulator_workshop/
├── structure_database/
│   ├── residue_codes.csv
│   ├── md_systems.csv
│   ├── PHA_types/3HB/
│   ├── built_PHAs/
│   ├── PHA_dry/
│   ├── PHA_solvated/
│   ├── PHA_solvated_ions/
│   └── PHA_melts/
├── md_simulation_scripts/
├── execution_logs/
├── figures/
└── study_records/
```

Tutorial 01 creates the database and copies the supplied 3HB chemistry. Other
folders appear when their lessons run. This keeps workshop outputs away from the
checkout's research database. The catalogue includes chemistries whose parameters
are not supplied; Tutorial 02 distinguishes registration from readiness.

To choose another workspace, set `IPHA_WORKSHOP` in the terminal **before**
running lessons. Use the same setting throughout the course:

```bash
export IPHA_WORKSHOP="$HOME/iphasimulator_workshop"
```

An editor launched separately must inherit this setting or use the same default.
Do not choose the repository itself or its research database as your workspace.

Lessons protect existing build, protocol, and analysis destinations. A failed
backend operation can still leave partial files. Inspect those files and the logs
before deciding how to recover; the lessons do not delete or silently replace
them. Generated simulations create a new numbered run on each execution.

## Course map

| Lesson | Task | Prerequisite | Output |
|---|---|---|---|
| [00 — Setup](core/00_setup_check_your_environment.py) | Check the scientific environment | Installation | Printed readiness checklist |
| [01 — Workspace](core/01_package_structure_find_your_files.py) | Create and locate workshop inputs | 00 | Separate workshop database |
| [02 — Chemistry](core/02_polymer_prep_choose_available_chemistry.py) | Check prepared 3HB chemistry | 01 | Parameter checklist and monomer drawing |
| [03 — Polymer](core/03_polymer_prep_build_a_chain.py) | Build a ten-unit chain | 02 | PDB, PRMTOP, RST7, logs and polymer drawing |
| [04 — Validation](core/04_polymer_prep_check_your_chain.py) | Check the chain | 03 | Atom/residue checks and PDB location |
| [05 — Dry system](core/05_system_prep_build_a_dry_system.py) | Prepare a dry periodic system | 04 | Registered dry system |
| [06 — Water](core/06_system_prep_add_water.py) | Prepare a solvated system | 04 | Registered solvated system |
| [07 — Salt](core/07_system_prep_add_salt.py) | Prepare a salted system from the chain | 04; 06 is optional | Registered salted system |
| [08 — Melt](core/08_system_prep_build_a_melt.py) | Pack multiple chains and check counts | 04; ACPYPE and Polyply | Melt inputs; explicit failure if composition differs |
| [09 — Registry](core/09_package_structure_find_a_prepared_system.py) | Find a prepared system | One of 05–08 | Resolved simulation input paths |
| [10 — Protocol](core/10_simulations_create_a_protocol.py) | Save a minimisation/NVT protocol | 05 and 09 for the default example | Workflow JSON and executable script |
| [11 — Simulation](core/11_simulations_run_a_short_simulation.py) | Execute the short protocol | 10 | Numbered run and execution log |
| [12 — Outputs](core/12_simulations_check_your_outputs.py) | Inspect trajectory and state data | 11; MDAnalysis | Alignment check and temperature/energy plots |
| [13 — Replica Tg](core/13_analysis_analyse_one_tg_replica.py) | Analyse supplied cooling data | Prepared dataset; analysis dependencies | Replica summary and diagnostics |
| [14 — System Tg](core/14_analysis_combine_tg_replicas.py) | Combine comparable independent replicas | 13 completed for each selected replica | System summary and comparison tables |
| [15 — Provenance](core/15_reproducibility_record_your_workflow.py) | Record a simulation's inputs and outputs | 10–12 | Timestamped study record |

**First-session route:** 00 → 01 → 02 → 03 → 04 → 05 → 09 → 10 → 11 → 12 → 15.

Lessons 06–08 are alternative system-preparation branches, not prerequisites for
the short dry-system demonstration. Lessons 13–14 are a separate prepared-data
exercise. No live workshop needs to wait for a production cooling simulation.

## Prepared data for Tg lessons

No large trajectories are bundled with these tutorials. The instructor must
supply a dataset, its simulation protocol, its source/provenance, and the actual
system composition. Place a **copy** under the workshop database, not a symlink
back to research results. Analysis writes beneath the selected replica directory.

For the default names, the required layout is:

```text
<workspace>/structure_database/PHA_melts/25_P3HB_10_melt/
└── simulations/
    ├── broad_tg_sim_02/
    │   ├── min_<system>.pdb
    │   ├── <name-containing-thermal_ramp_cooling>.dcd
    │   └── <name-containing-thermal_ramp_cooling>.txt
    ├── broad_tg_sim_03/
    │   └── ...the same three kinds of input...
    └── broad_tg_sim_04/
        └── ...the same three kinds of input...
```

Preserve the original filenames. The loader requires exactly one `min_*.pdb`,
one matching stage DCD, and one matching stage state-data TXT in each replica.
Do not rename the state-data file to an arbitrary name. Do not include multiple
matching stages in one replica directory.

For a fresh calculation, copy the raw inputs without an existing `analysis/`
directory. Run Tutorial 13 separately for each replica name. For a results-only
exercise, supply the existing replica `analysis/tg_analysis/` directories,
including `analysis_summary.json` and `tg/temperature_response.csv`; Tutorial 14
can consume these without raw trajectories. Use advanced Tutorial A06 to view an
existing replica result without recalculating it; include its figures for the visual exercise.

The current demonstration settings are 200,000,000 requested steps, 700 → 140 K
in 10 K increments, reporting every 1,000 steps. These are settings to verify,
not facts inferred automatically from a trajectory. The backend retains its
historical nominal-temperature assignment convention. Protocol compatibility and
replica independence remain the instructor's responsibility.

The existing dataset named `25_P3HB_10_melt` reports **26 analysed chains**.
Its name must not be presented as evidence that it contains exactly 25 chains.
Document this discrepancy if using those data. Tutorial 08 checks requested
versus produced composition and may stop because of the current topology issue.
The tutorial does not alter that backend behaviour.

The default Tg calculation samples approximately 4,000 frames per chain and can
take substantial time and memory. Provide precomputed results when appropriate.
Changing sampling stride changes the analysis and requires renewed diagnostic
review. The short NVT run in Tutorial 11 cannot replace a cooling dataset.

## Current boundaries

- These are source-checkout tutorials, not a claim that all current code works
  from an independently installed wheel.
- The supplied chemistry is copied unchanged; new parameterisation and residue
  definition are deferred to the advanced series.
- The core path uses homopolymers and the current supported function signatures.
- Script generation leaves the engine's current timestep/reporting defaults in
  place and disables restart saving. Restart support has a known manager mismatch.
- The short simulation is an execution exercise, not a convergence demonstration.
- Melt composition checks must pass before using a newly built melt as the
  requested system. A registry entry alone is insufficient.
- Tg lessons use the existing historical clustering-based response, not a
  density-based estimator. Review scientific diagnostics separately.
- System aggregation compares saved metadata but cannot prove independent
  replicas or recover every original analysis option from the existing schema.
- The provenance lesson records package versions, source revision/status, and
  file checksums; it does not constitute a complete reproducibility archive.

The original notebooks, developer tutorials, package source, GUI, and research
files are unchanged by the creation of this tutorial collection.
