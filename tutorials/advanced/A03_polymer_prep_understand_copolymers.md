# A03 — Trace polymer sequences and copolymer construction

**Task:** connect a requested sequence to residue roles, names and generated files.

**Inputs:** prepared chemistries and a sequence specification. **Outputs:** an expanded sequence, a built copolymer and a chemical drawing.

## Sequence is different from chemistry

A chemistry defines reusable units. A sequence decides which chemistry occupies each position. In `build_PHA_copolymer()`, letters map to the order of `PHA_types`: for `["3HB", "4HB"]`, A is 3HB and B is 4HB. Pattern `AB` and length six produces `ABABAB`. A full-length pattern is accepted directly; otherwise the length must be a multiple of the pattern length.

The first position uses its chemistry's head code, the last uses its tail code, and internal positions use mainchain codes. Every chemistry must therefore have the required prepins and force-field files, even if a particular role is not used in this particular sequence.

The builder combines prepin/FRCMOD loading statements, creates a LEaP sequence, writes topology/coordinates/PDB, and records polymer SMILES. It does not produce an equilibrated copolymer or automatically solve all downstream system preparation.

## Random construction and identity

The random mode uses Python's random selection and optionally seeds it. Inspect the actual returned `sequence_PHA_types` rather than treating the seed or filename as a complete description. The current random output name uses `rand` and length; different realisations can share that name. Preserve the sequence and avoid reusing destinations when comparing realisations.

The practical exercise intentionally uses pattern mode. Section 2 prints the expanded sequence, checks the required parameters and then builds. The supplied core seed does not include ready 4HB prepins, so the default build stops until appropriate reviewed parameters are supplied. Study the printed sequence or the examples below before preparing those additional inputs.

## Current boundaries

The backend uses pattern-based copolymer names, while the GUI's preview uses a `custom` naming form. Several downstream helpers parse only names of the form `P<chemistry>_<length>`. A successful copolymer build therefore does not imply that the existing dry, solvated or melt helper accepts that result.

The two chain-construction routes also remain separate. `build.py` constructs RDKit molecules from curated or custom monomers, while `build_pha.py` constructs parameterised residue-based chains. Do not replace one with the other solely because both build polymers.

## Exercises

1. Expand `AAB` to length nine and identify the role at every position.
2. Predict why length eight fails for that pattern.
3. Compare the saved SMILES and topology residue sequence for a built example.
4. Inspect a downstream parser before passing it a `co_*` name.

**Answers:** The expanded sequence is `AABAABAAB`; its first A is head and final B is tail. Eight is not divisible by three. SMILES and topology should represent the requested sequence, but agreement must be checked rather than assumed. The current homopolymer parser rejects `co_*` names.

## Function reading

Read `build_PHA_copolymer()` and the SMILES methods in [build_pha](../reference/build_pha.md). Read naming and parsing in [naming](../reference/naming.md) and [pha_filepath_manager](../reference/pha_filepath_manager.md). The separate direct-molecule route is in [build](../reference/build.md). Molecular catalogue drawing functions are covered in [visualisation/visualiser](../reference/visualisation__visualiser.md).
