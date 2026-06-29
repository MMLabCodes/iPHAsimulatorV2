# iPHASimulator v2

iPHASimulator v2 is a notebook-driven Python toolkit for building, validating,
parameterising, simulating, preprocessing, and analysing polyhydroxyalkanoate
(PHA) oligomer systems.

The current v2 workflow focuses on reproducible PHA molecular simulation
preparation. It starts from chemically defined PHA oligomers, exports structure
files, prepares Amber/GAFF2 and GROMACS/OpenMM simulation inputs, supports HPC
execution patterns, and provides early analysis and PHA-enzyme docking
preparation notebooks.

## What It Does

iPHASimulator v2 currently provides:

- RDKit-based PHA oligomer generation for curated common PHAs and custom
  3-hydroxy acid monomers.
- Validation and visualisation of generated oligomer structures.
- PDB and SDF export for downstream molecular simulation workflows.
- AmberTools/GAFF2 parameterisation for PHA oligomers.
- OpenMM and GROMACS workflow preparation for dry and solvated systems.
- HPC workflow helpers for repeatable simulation execution.
- GROMACS trajectory preprocessing for analysis-ready trajectories.
- Basic polymer trajectory analysis.
- PHA-enzyme docking input preparation for manual HADDOCK workflows.

DFT workflows are not documented as a current v2 capability.

## Workflow Overview

```text
Design -> validation -> structure export -> parameterisation -> MD simulation
       -> trajectory preprocessing -> analysis -> PHA-enzyme docking
```

The repository is organised around guided notebooks. Reusable code lives in
`src/iphasimulator`; notebooks should remain workflow tutorials rather than the
home of core package logic.

## Current Status

| Area | Status | Notes |
|---|---|---|
| Polymer generation | Working | Curated PHA names, side-chain based generation, and custom monomers are implemented in `src/iphasimulator`. |
| GAFF2/Amber parameterisation | Working | AmberTools workflow writes GAFF2 `mol2`, `frcmod`, `prmtop`, `inpcrd`, logs, and timing files. |
| CHARMM/CGenFF parameterisation | In progress | Notebook `05B` documents the CHARMM/CGenFF handoff route; it is not yet equivalent to the GAFF2 workflow. |
| GROMACS/OpenMM MD workflows | Working/in progress | Dry OpenMM and GROMACS preparation are working; solvated workflows and production-style routes are under active development by notebook. |
| HPC workflow | Working | YAML/SLURM-oriented helpers and notebook guidance are present for staged runs. |
| Polymer analysis | Working | Basic analysis notebook supports analysis from preprocessed trajectories. |
| PHA-enzyme docking preparation | Working/in progress | Notebook `11` prepares docking-ready polymer PDB inputs and manual HADDOCK job notes; docking submission is manual. |
| Enzyme-polymer MD | Planned | Docked complexes are not yet converted into enzyme-polymer MD systems. |
| ML/database functionality | Planned | Reusable databases and ML-backed workflows are future work. |

## Installation

The recommended installation route is conda for scientific and external MD
dependencies, followed by an editable install of the local package.

```bash
conda create -n iphasimulator-v2 python=3.11
conda activate iphasimulator-v2

conda install -c conda-forge \
  rdkit ambertools openmm gromacs parmed mdtraj mdanalysis \
  pandas numpy scipy matplotlib pyyaml networkx jupyterlab pytest openbabel

python -m pip install -e ".[dev,md]"
```

Then start the notebooks from the repository root:

```bash
jupyter lab notebooks/
```

Generated structures, parameter files, simulation inputs, trajectories, and logs
are written under `examples/output/`, which is ignored by Git.

## Required Dependencies

| Dependency | Purpose |
|---|---|
| RDKit | PHA molecule construction, stereochemistry handling, structure validation, and SDF/PDB export. |
| AmberTools | GAFF2 parameterisation through `antechamber`, `parmchk2`, and `tleap`. |
| OpenMM | Python-native MD validation and OpenMM simulation workflows. |
| GROMACS | GROMACS dry/solvated workflow execution and trajectory preprocessing. |
| ParmEd | AMBER-to-GROMACS topology conversion. |
| MDTraj / MDAnalysis | Trajectory handling and analysis support. |
| pandas | Workflow tables, status summaries, and analysis data frames. |
| numpy | Numerical calculations. |
| matplotlib | Notebook plots and basic analysis visualisation. |
| Open Babel | Optional structure format conversion support where needed. |

The package metadata also includes supporting Python dependencies such as
`scipy`, `networkx`, and `pyyaml`.

## Repository Structure

```text
notebooks/   Guided v2 workflow notebooks.
src/         Reusable `iphasimulator` Python package code.
examples/    Thin runnable scripts, YAML workflow examples, SLURM templates,
             and generated output under `examples/output/`.
docs/        Developer and design documentation.
tests/       Automated tests for builders, export, MD workflow helpers,
             GROMACS conversion, HPC helpers, and trajectory preprocessing.
```

## Notebook Workflow

| Notebook | Purpose | Main output |
|---|---|---|
| `01_examples_pha_oligomers.ipynb` | Introduce built-in PHA oligomer generation examples. | Example RDKit PHA molecules for tutorial use. |
| `02_design_polymer_for_user_request.ipynb` | Select or define a PHA target from user-facing design inputs. | A designed polymer target such as `PHB4_R`. |
| `03_validate_and_visualize.ipynb` | Validate generated oligomers and inspect molecular structures. | Validation summaries and visual checks. |
| `04_export_structures.ipynb` | Export validated oligomers to structure files. | PDB/SDF files in `examples/output/polymer_structures/`. |
| `05A_amber_gaff2_parameterisation.ipynb` | Run AmberTools/GAFF2 parameterisation. | `prmtop`, `inpcrd`, GAFF2 `mol2`/`frcmod`, and logs under `examples/output/md_tests/<SYSTEM>/gaff2/`. |
| `05B_charmm_cgenff_parameterisation.ipynb` | Document CHARMM/CGenFF parameterisation handoff. | In-progress CHARMM/CGenFF preparation notes. |
| `06A_openmm_dry_polymer.ipynb` | Validate GAFF2-derived AMBER files with dry OpenMM MD. | Dry OpenMM outputs under `examples/output/md_tests/<SYSTEM>/openmm/dry_polymer/`. |
| `06B_gromacs_dry_polymer.ipynb` | Convert AMBER files and prepare dry GROMACS validation. | Dry GROMACS folder under `examples/output/md_tests/<SYSTEM>/gromacs/dry_polymer/`. |
| `06C_gromacs_solvated_system.ipynb` | Prepare explicit-solvent GROMACS inputs and scripts. | Solvated GROMACS workflow under `examples/output/md_tests/<SYSTEM>/gromacs/solvated_polymer/`. |
| `06D_openmm_solvated_system.ipynb` | Prepare explicit-solvent OpenMM workflow templates. | Solvated OpenMM preparation under `examples/output/md_tests/<SYSTEM>/openmm/solvated_polymer/`. |
| `07_hpc_workflows.ipynb` | Prepare and document local/HPC staged execution. | SLURM scripts, restart guidance, and benchmark execution notes. |
| `08_trajectory_preprocessing.ipynb` | Reconstruct, center, wrap, and optionally fit GROMACS trajectories. | `step7_centered.xtc`, optional `step7_fitted.xtc`, and representative frames. |
| `09_basic_polymer_analysis.ipynb` | Run basic polymer trajectory analysis. | Analysis tables and plots for metrics such as radius of gyration and SASA. |
| `10_batch_md_benchmark.ipynb` | Launch and track multi-system MD benchmark preparation. | Benchmark outputs under `examples/output/benchmark/`. |
| `11_PHA_Enzyme_Docking.ipynb` | Prepare PHA oligomer inputs for manual enzyme docking. | Docking-ready polymer PDBs and manual HADDOCK job records under `examples/output/docking_inputs/`. |

## Minimal PHB4 Benchmark Workflow

`PHB4` is the default small benchmark system for checking the v2 workflow.

1. Install the environment and start Jupyter:

   ```bash
   conda activate iphasimulator-v2
   jupyter lab notebooks/
   ```

2. Run notebooks `01` to `04` using the PHB tetramer target. The expected
   exported structure names are:

   ```text
   examples/output/polymer_structures/PHB4_R.sdf
   examples/output/polymer_structures/PHB4_R.pdb
   ```

3. Run `05A_amber_gaff2_parameterisation.ipynb` with `PHB4_R` as the target.
   The expected Amber/GAFF2 outputs are written under:

   ```text
   examples/output/md_tests/PHB4/gaff2/
   ```

4. Run the relevant MD notebook for the route being tested:

   - `06A_openmm_dry_polymer.ipynb` for dry OpenMM validation.
   - `06B_gromacs_dry_polymer.ipynb` for dry GROMACS validation.
   - `06C_gromacs_solvated_system.ipynb` for explicit-solvent GROMACS setup.
   - `06D_openmm_solvated_system.ipynb` for explicit-solvent OpenMM setup.

5. For production-style GROMACS trajectories, continue with:

   - `07_hpc_workflows.ipynb` for local/HPC execution guidance.
   - `08_trajectory_preprocessing.ipynb` to generate analysis-ready trajectories.
   - `09_basic_polymer_analysis.ipynb` for basic trajectory analysis.
   - `11_PHA_Enzyme_Docking.ipynb` only after suitable production structures are available.

## Developer Documentation

- [Developer guide](docs/developer_guide.md)
- [Notebook guide](notebooks/README.md)

## Roadmap

- Reusable PHA residue database.
- Head/main/tail building blocks for more robust polymer assembly.
- Mixed PHA sequences and sequence-aware validation.
- Enzyme-polymer MD workflows from reviewed docking poses.
- ML potential and database support for future screening workflows.

## Citation and Acknowledgements

Citation information will be added before publication or formal release. Until
then, please cite the repository URL and acknowledge the iPHASimulator v2
development team when using this software in research outputs.
