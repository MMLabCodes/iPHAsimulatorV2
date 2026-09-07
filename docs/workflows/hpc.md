# HPC execution

**Start with:** prepared and checked simulation inputs. This workflow handles
planning and execution; it does not replace topology preparation or validate
equilibration automatically.

```{warning}
The configured runner imports construction and MD modules with existing
[syntax blockers](../capabilities.md#import-blockers). This also affects its
`--dry-run` and `--write-slurm` entry points until those imports are repaired.
```

## 1. Review the configuration

Download the existing {download}`workflow YAML <../../examples/hpc_validation_workflow.yaml>`
and {download}`SLURM example <../../examples/slurm_validation_workflow.sh>`.
Work from the repository root, and edit:

- Target monomers and repeat counts; use small chains first.
- Which stages are enabled (`build`, `gaff2`, `openmm`).
- Charge model and engine settings.
- Cluster partition, time, CPUs, memory and Conda environment.

Unlike the contact-analysis YAML, the configured workflow's output paths are
used relative to the process working directory. Launch it from the repository root.

## 2. Print a plan and generate a script

After the import blockers are resolved:

```bash
python examples/run_configured_workflow.py --config examples/hpc_validation_workflow.yaml --dry-run
python examples/run_configured_workflow.py --config examples/hpc_validation_workflow.yaml --write-slurm examples/output/run_validation.slurm
```

Read the generated script and adapt the environment block to your cluster.
The workflow plan does not submit a job. When the inputs, allocations and script
are ready, submission is a separate user action:

```bash
sbatch examples/output/run_validation.slurm
```

## 3. Monitor and restart

Keep checkpoints, topology, coordinates, parameter files, configuration and logs
together. Review stage completion and numerical behavior before continuation.
For GROMACS restarts, use the appropriate checkpoint with `mdrun -cpi`; for
OpenMM, use the restart format supported by the chosen runner. Benchmark a small
segment on the intended hardware before allocating a long production run.

The [07 notebook](../notebooks.md#execution-and-analysis) covers GROMACS SLURM
execution and restart guidance; notebook 10 is a six-system benchmark launcher
with fixed workflow assumptions. Batch benchmarks are separate from the current
single-system enzyme-contact analysis.

API: {py:func}`iphasimulator.workflows.hpc.workflow_plan`,
{py:func}`iphasimulator.workflows.hpc.render_slurm_script`.
