# WP1 — Consistency and bug fixes (issues I1–I5)

**Prepend:** `dev_plan/01_rules_for_claude_code.md` · **Branch:** `dev/wp1-consistency`

## I1 — NB11 benchmark path (bug)
`notebooks/11_PHA_Enzyme_Docking.ipynb`, cell 4: `benchmark_root = repo_root / "examples" / "output" / "md_tests" / "benchmark"`.
NB10 writes to `examples/output/benchmark/<SYSTEM>/`. Change NB11 to match, and update the markdown in cell 3 that states the expected path.
*Check:* `examples/output/benchmark/P3HB_4/gromacs/solvated_polymer/` exists; the NB11 path must resolve under `examples/output/benchmark/`.

## I2 — NB11 exports all atoms (bug)
`gro_to_pdb` (cell 6) writes every atom line, including SOL, SOD and CLA, but the notebook says it exports the *polymer* PDB for HADDOCK.
- Add a `residue_names=("PHA",)` filter parameter, so that only matching residues are written. Default to the polymer residue name used in the GAFF2 topology; confirm that name in `examples/output/benchmark/P3HB_4/gromacs/solvated_polymer/step5_input.gro` (expected `PHA`).
- The polymer must be whole. Either (a) document that the input must be a make-whole structure (e.g. `gmx trjconv -pbc mol`) and add a check that raises when any bonded heavy-atom pair is > 0.3 nm apart after filtering, or (b) take the representative frame from NB08. **Do not** implement your own unwrapping. Propose (a) or (b) in your plan.
- Keep the function inside the notebook (no `src/` change in this WP).
- Test it on `examples/output/benchmark/P3HB_4/gromacs/solvated_polymer/step5_input.gro` and write to a **new** file under `examples/output/docking_inputs/_wp1_test/`. Expect 51 atoms for P3HB_4 (25 heavy atoms + 26 H).

## I3 — Dead references and naming
- `notebooks/README.md`: add `12_enzyme_polymer_stable_analysis.ipynb` to the ordered list and its one-line description. Leave placeholders for `00_start_here` and `13_enzyme_pha_results` marked "(added in WP4/WP5)" only if those WPs are approved; otherwise don't mention them.
- NB05A cell 9: replace the reference to `06_openmm_setup.ipynb` with "the 06A–06D notebooks (see the roadmap below)".
- NB10 cell 0: `scripts/run_md_test_set.py` doesn't exist. The code calls `python -m iphasimulator.workflows.md_benchmark`; say that instead.
- NB07 cell 4 mentions `system_neutralized.gro`; NB06C calls the final structure `step5_input.gro`. Check `src/iphasimulator/simulation_gromacs_runner.py` for which files the solvation script writes, then make the NB07 text state accurately what each file is. **Do not rename files.**

## I4 — NB05A markdown vs code
Keep the code behaviour unchanged except for the RUN flag, which is WP2's job. Fix the text:
- Cell 1 says the default is AM1-BCC `bcc` and suggests `gas` for debugging. The code (cell 8) uses `charge_method = "abcg2"` with a comment calling it AM1-BCC.
- ABCG2 is a distinct charge model (AM1-BCC-type charges re-fitted for GAFF2), not AM1-BCC. Check what `parameterize_gaff2` in `src/iphasimulator/parameterization_gaff2.py` accepts and defaults to, then rewrite cells 1 and 7 and the cell-8 comment so the text matches the code. **Flag, don't fix:** don't change which charge method is used.

## I5 — Kernel metadata
Set `metadata.kernelspec` of `06A_openmm_dry_polymer.ipynb` and `06D_openmm_solvated_system.ipynb` to match notebook 01 exactly (name, display_name, language). Don't execute them.

## Acceptance
- [ ] NB11 path resolves to `examples/output/benchmark/...`
- [ ] Test PDB has only PHA atoms (51 for P3HB_4); the continuity check passes on a whole molecule and raises on a deliberately split copy (in a temporary test only; not saved in the repo)
- [ ] `grep -rn "06_openmm_setup\|run_md_test_set" notebooks/` → nothing
- [ ] README lists 12
- [ ] 05A text consistent with code; code behaviour unchanged
- [ ] 06A/06D kernelspec = `ipha_clean`
- [ ] `pytest -q` unchanged; all notebooks validate with `nbformat`
