# Tutorial Notebooks

Run the notebooks in order:

1. `01_examples_pha_oligomers.ipynb`
2. `02_design_polymer_for_user_request.ipynb`
3. `03_validate_and_visualize.ipynb`
4. `04_export_structures.ipynb`
5. `05A_amber_gaff2_parameterisation.ipynb` - Amber/GAFF2 Parameterisation
6. `05B_charmm_cgenff_parameterisation.ipynb` - CHARMM/CGenFF Parameterisation
7. `06A_openmm_dry_polymer.ipynb`
8. `06B_gromacs_dry_polymer.ipynb`
9. `06C_gromacs_solvated_system.ipynb`
10. `06D_openmm_solvated_system.ipynb`
11. `07_hpc_workflows.ipynb`
12. `08_trajectory_preprocessing.ipynb`
13. `09_basic_polymer_analysis.ipynb`
14. `10_batch_md_benchmark.ipynb`
15. `11_PHA_Enzyme_Docking.ipynb`

The parameterisation and 06-series notebooks are workflow-oriented:

- `05A`: Amber/GAFF2 parameterisation and the roadmap explaining why the workflow branches after parameterisation.
- `05B`: CHARMM/CGenFF parameterisation placeholder covering CHARMM-GUI Ligand Reader & Modeler and Solution Builder handoff.
- `06A`: OpenMM dry polymer validation and local debugging.
- `06B`: AMBER to GROMACS conversion and dry GROMACS minimisation.
- `06C`: explicit-solvent GROMACS preparation with box, water, ions, PME, and NVT/NPT/production scripts.
- `06D`: explicit-solvent OpenMM setup template.
- `07`: HPC execution, SLURM submission, restart continuation, benchmarking, and performance tuning.
- `08`: GROMACS trajectory preprocessing with reusable `[ center ]` index groups, PBC reconstruction, compact wrapping, optional fitting, and representative frame extraction.
- `09_basic_polymer_analysis`: analysis entry point that uses the centered trajectory by default.
- `10_batch_md_benchmark`: workflow log, launcher, and progress checker for the six-system MD benchmark.
- `11_PHA_Enzyme_Docking`: prepares benchmark PHA oligomer PDB inputs and job notes for manual HADDOCK docking.

Workflow map:

```mermaid
flowchart LR
    A[build] --> B[parameterise]
    B --> C[convert or solvate]
    C --> D[engine-specific MD]
    D --> E[HPC execution]
```

These tutorials are written for users who may not be computational specialists.
They explain what each step means and keep editable input cells small.

Reusable Python logic belongs in `src/iphasimulator`. Notebook cells should guide
the workflow, not duplicate chemistry or simulation code.
