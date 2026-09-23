# Advanced developer tutorials

These lessons explain how the current implementation works. Read each guide,
then use its adjacent cell-based Python exercise. Each exercise follows
**get ready → run the task → check and view the result**, with shared setup hidden
in the workshop helper. Running A01–A04 performs the stated preparation/build task
when its required inputs are available. A05 previews a cluster script, A06 reads
saved results and figures, and A07 reads source structure. None submits cluster jobs.

| Lesson | Guide | Exercise |
|---|---|---|
| A01 | [A01 parameterisation prepare new chemistry](A01_parameterisation_prepare_new_chemistry.md) | [Python exercise](A01_parameterisation_prepare_new_chemistry.py) |
| A02 | [A02 parameterisation define residue units](A02_parameterisation_define_residue_units.md) | [Python exercise](A02_parameterisation_define_residue_units.py) |
| A03 | [A03 polymer prep understand copolymers](A03_polymer_prep_understand_copolymers.md) | [Python exercise](A03_polymer_prep_understand_copolymers.py) |
| A04 | [A04 trajectories trace gromacs preprocessing](A04_trajectories_trace_gromacs_preprocessing.md) | [Python exercise](A04_trajectories_trace_gromacs_preprocessing.py) |
| A05 | [A05 simulations understand cluster submission](A05_simulations_understand_cluster_submission.md) | [Python exercise](A05_simulations_understand_cluster_submission.py) |
| A06 | [A06 analysis understand the tg method](A06_analysis_understand_the_tg_method.md) | [Python exercise](A06_analysis_understand_the_tg_method.py) |
| A07 | [A07 package structure trace and extend](A07_package_structure_trace_and_extend.md) | [Python exercise](A07_package_structure_trace_and_extend.py) |

## Prerequisites and scope

Use the scientific environment and separate workspace from the [core course](../README.md).
Some exercises require instructor-supplied datasets or additional reviewed chemistry.
A01 uses its own experimental database so that parameterisation does not replace
the core workshop's supplied parameters. A02 does not invent manual atom definitions.
A03 demonstrates sequences without assuming missing monomer parameters exist.
A04 requires a separate native GROMACS dataset. A05 previews rather than submits.
A06 reads completed results. A07 is an architecture-reading and design exercise.

The [function coverage index](../reference/coverage_index.md) links every explicit
function/method definition in the package source to a reference entry. Module
pages include class fields, original documentation, return/error/call information,
and source excerpts. This is source-derived documentation, not a statement that
all functions have passed runtime or scientific validation. See the index for
snapshot hashes and duplicate-definition handling.

The practical sequence has seven lessons, but exhaustive source coverage is in
the accompanying reference. Use that reference selectively during a workshop;
it is not intended to be read in one sitting. The package, GUI, existing tutorials,
and research database are not modified by the creation of this series.
