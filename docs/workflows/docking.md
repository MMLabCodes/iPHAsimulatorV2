# Docking preparation

**Status: notebook-based, manual preparation; incomplete as an end-to-end pipeline.**
There is no automated HADDOCK submission, validated enzyme–polymer complex
builder, or catalytic-activity predictor in this workflow.

## 1. Choose the polymer structure

Notebook **11** expects a final benchmark structure at
`examples/output/md_tests/benchmark/<system>/gromacs/solvated_polymer/step7_production.gro`.
Review that path and confirm the intended system and final structure. Its
benchmark import also depends on modules with [runtime blockers](../capabilities.md).

## 2. Prepare and inspect the PDB

The notebook contains a local GRO-to-PDB converter and writes to
`examples/output/docking_inputs/<system>/`. The converter loops over the GRO
atoms; it does **not** automatically isolate PHA from a solvated system. Extract
the intended ligand first or verify that the input already contains only the
polymer. Inspect chain/residue identifiers, atom names, elements, terminal groups
and unwanted solvent/ions in the exported PDB.

This converter is notebook-local logic, not a separately supported package API.
Do not assume its atom-name element inference or file formatting covers every
possible input structure.

## 3. Prepare the enzyme separately

Supply the reviewed enzyme structure and decide the docking restraints for the
specific research question. The enzyme annotations and binding statements in
the historical notebook are user-supplied context, not independently validated
results of this package. Confirm them against your own evidence before use.

## 4. Record the manual docking job

Upload inputs through your chosen docking service when ready, and retain the
input files, restraints, job identifiers and returned results. The notebook
provides preparation notes and records; it does not submit the job.

For an existing MD trajectory of a complex, use [contact analysis](analysis.md)
to examine proximity. Contact occupancy cannot establish affinity or catalytic
activity.

Notebook: [11 docking preparation](../notebooks.md#execution-and-analysis).
