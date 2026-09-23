# A05 — Understand protocols, execution and cluster submission

**Task:** trace a workflow from settings to executable work, and identify what must be adapted for a cluster.

**Inputs:** the supplied YAML configuration and existing Slurm shell script. **Output of this exercise:** their settings and script text for inspection. No new script is generated and no job is submitted.

The older workflow currently cannot be imported: `build.py` contains a second top-level string before `from __future__ import annotations`, which Python rejects. The exercise therefore reads the two existing example files directly. It does not patch or silently bypass that package error. The API discussion below describes the source implementation; execution of that route remains blocked until the package is repaired separately.

## Current OpenMM workflow route

`OpenMMScriptBuilder` stores ordered stage dictionaries. `add_*` methods populate them; `validate()` checks supported settings and order; `to_dict()`/`from_dict()` define the serialised protocol; save/load methods persist it. `to_script()` generates an executable Python program and `_build_steps_code()` delegates formatting for each stage.

The generated script resolves a registered system, creates a numbered run directory and chooses Amber or GROMACS input parsing. Both classes execute OpenMM through `BuildSimulation`. Follow system/context creation, platform selection, minimisation, stage transitions, and reporter attachment. The stage methods return a simulation object and, for dynamics, a state-data path; that is how the next stage and end-of-run graphing receive their inputs.

Platform availability and successful context creation are distinct. The backend's environment override can request CUDA, OpenCL or CPU. Inspect the actual platform settings and test an appropriate small workload on the target machine before production use.

The current stages construct new simulation contexts. Inspect which state elements each transition copies; do not assume trajectories form one uninterrupted velocity-preserving context. Restart saving currently references a manager attribute not defined by the current path manager. The core course leaves it disabled.

## Older YAML workflow route

`load_workflow_config()` loads YAML and merges defaults. `targets_from_config()` parses validation targets. `workflow_plan()` describes enabled stages. `render_slurm_script()` emits a launcher for `examples/run_configured_workflow.py`. This route is not the same protocol schema as the newer OpenMM script-builder JSON.

`workflows/md_benchmark.py` coordinates earlier parameterisation/OpenMM/GROMACS preparation routes. `workflows/validation.py` creates tutorial molecules and exports; `workflows/design.py` maps user design choices to the RDKit builders. These are orchestration layers, not alternate implementations of every scientific operation.

## Before a real submission

The existing `cluster/submit_openmm_job.sh` is site-specific. Account, partition, storage paths, scientific environment, wall time, CPU/memory/GPU requests and platform configuration need deliberate review. Confirm the compute node can access the generated script, package, system inputs and output directory.

For workshop work on a cluster, create a separate cluster workspace. Recreate or copy the prepared inputs and saved protocol there, then generate the executable script in that workspace. The generated script locates its database relative to its own position. The current mixed `src.iphasimulator` and `iphasimulator` imports require the checkout/import paths to be available as described by the core execution lesson.

The YAML Slurm preview also uses relative log paths. Ensure the submission directory/log directory exist before submission; creating a log directory inside the job is not enough to guarantee Slurm can open its output paths. Review shell quoting for any paths containing spaces. This exercise only previews the current helper; it does not silently repair it.

## Exercise

Run the adjacent exercise, locate the configured stages, then identify every line of the supplied Slurm script that is site-specific. Explain which directory owns output and which command actually starts the work. The existing script has not been regenerated from the displayed settings: check their relationship explicitly. Compare it with the newer generated OpenMM script from core Tutorial 10.

**Review question:** Does a successful submission mean a successful simulation? **Answer:** No. Submission, job start, process completion, expected outputs, and scientific adequacy are separate checks.

## Function reading

Read [openmmscript_builder](../reference/openmmscript_builder.md), [sw_openmm](../reference/sw_openmm.md), [simulation_openmm_amber_runner](../reference/simulation_openmm_amber_runner.md), [workflows/hpc](../reference/workflows__hpc.md), [workflows/md_benchmark](../reference/workflows__md_benchmark.md), [workflows/design](../reference/workflows__design.md), and [workflows/validation](../reference/workflows__validation.md).
