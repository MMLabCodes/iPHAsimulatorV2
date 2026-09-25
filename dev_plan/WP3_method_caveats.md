# WP3 — Method caveats and a read-only stereochemistry diagnostic (issues I8–I15)

**Prepend:** `dev_plan/01_rules_for_claude_code.md` · **Branch:** `dev/wp3-caveats` (from WP1)

**Policy: flag, don't fix.** Add one markdown cell titled `## Method notes and limitations` at the end of each listed notebook. Keep it factual and short, one bullet per point. Do **not** change code, except for the new diagnostic script in part B.

## A. Caveat text

Use the text below as the draft. Before inserting, check each factual statement against the repo and fix the wording if it is wrong; report any discrepancy.

**02 (I10, I15)**
- The custom-monomer route (Mode C) accepts a monomer only if RDKit assigns CIP label **R** to the backbone stereocentre. CIP labels depend on substituent priority. For side chains that rank above the backbone CH₂–C(=O)O group (e.g. vinyl, isopropyl, CH₂OMe), label R corresponds to the *opposite* spatial arrangement from natural (R)-3-hydroxyalkanoate units. Check the spatial configuration with `dev_plan/diagnostics/check_custom_stereo.py` before using custom monomers.
- Mode B (`side_chain_carbons=5`) builds the same molecule as `P3HO_4`, but names it `PHA_C5_4_R`. Mode C names omit the `_` before the degree.

**05A**
- Charges are computed on a single RDKit conformer. For longer or flexible oligomers, charge conformer dependence has not been assessed.
- The whole oligomer is one residue (`PHA`). Per-monomer analysis needs atom-index mapping.

**06C (I8, I9)**
- Solute: GAFF2 (Amber combination rules; fudgeLJ 0.5, fudgeQQ 0.8333).
- Water: CHARMM-style TIP3P, **with Lennard-Jones parameters on hydrogen** (HT σ = 0.040 nm, ε = 0.192 kJ/mol). Ions: CHARMM-GUI SOD/CLA parameters (`src/iphasimulator/data/gromacs_solvation/`). The conventional GAFF2 pairing is standard TIP3P (no H LJ) with Joung–Cheatham ions. This mixed combination has not been validated for PHA.
- MDP: plain 1.0 nm van der Waals cut-off, no long-range dispersion correction (`DispCorr` not set). This affects NPT density slightly. Rg/SASA of a single solvated oligomer is expected to be less sensitive (not quantified).
- All `grompp` calls use `-maxwarn 1`. Current logs contain no warnings, but the flag would hide future ones. Inspect `*grompp.log`.

**06D (I11)**
- Template only. `amber14-all.xml` contains no PHA residue template, so `createSystem` cannot parameterise the polymer. The supported OpenMM route is 06A (AMBER prmtop/inpcrd).

**09 (I13)**
- One 100 ns trajectory, analysed from t = 0, with no equilibration period discarded and no uncertainty estimate. Values describe this run, not converged ensemble averages.
- "End-to-end" is the first and last atom of `[ center ]`. For P3HB_4 these are the terminal hydroxyl O (atom 1) and the carboxylic-acid H (atom 51). This follows RDKit atom ordering; it is not a chemically chosen pair.
- Rg is geometric (unweighted), as in `mdtraj.compute_rg` without masses.

**10 (I12)**
- "N/29 checks passed" counts expected files that exist, plus two script-content checks. It does not check that minimisation converged or that production ran, and it says nothing about physical validity.

**12 (I14)**
- This notebook reads the raw combined trajectory. Polymer RMSD "relative to protein" is computed without periodic-image handling, so after the polymer leaves the enzyme's image the value includes box-image jumps. Late-run frame-to-frame changes of 40–90 Å per 100 ps are non-physical for a diffusing 4-mer (expected ~5 Å). Do not interpret the "final 20%" polymer RMSD.
- PBC-aware enzyme–PHA distances for four systems are in `md_simulation_scripts/enzyme_pha_analysis/` (summarised in notebook 13).

**11**
- The GK13/ANC45 binding statements in the enzyme table need a literature citation. Add `TODO(Zhiwen): citation` next to the table. Do not invent one.

## B. Read-only stereo diagnostic
Create `dev_plan/diagnostics/check_custom_stereo.py`. It uses the builder and does not modify it.
- Input: a list of monomer SMILES. Defaults: the 3HB reference `C[C@@H](O)CC(=O)O` and the three NB02 examples `CC(C)[C@H](O)CC(=O)O`, `C=C[C@H](O)CC(=O)O`, `COC[C@H](O)CC(=O)O`.
- For each monomer, find the backbone stereocentre and identify its four neighbours **by role**: hydroxyl O, backbone CH₂ (the one bonded to the carboxyl C), side-chain atom, H. Compute handedness from a 3D embedding (`AllChem.EmbedMolecule` with a fixed seed) as the sign of the signed volume `(v_O − v_C)·[(v_CH2 − v_C) × (v_side − v_C)]`.
- Report the CIP label, the role-based handedness sign, and whether the sign matches the 3HB reference.
- Also run the diagnostic on one repeat unit inside a built dimer from `build_custom_pha(smiles, 2, "diag")`, to confirm the builder preserves what the monomer check says.
- Print a table. Do not change `build.py`.

**Expected result (hypothesis to test, not an assumption):** all three examples report CIP **R** but a handedness sign *opposite* to 3HB. If they match 3HB instead, report that and weaken the 02 caveat accordingly.

## Acceptance
- [ ] Caveat cells added to 02, 05A, 06C, 06D, 09, 10, 11, 12; no code cell changed in those notebooks
- [ ] Each factual number in the caveats re-checked against the repo (list: statement → evidence file:line)
- [ ] Diagnostic runs in `ipha_clean` and prints the table; the result is quoted in the report
- [ ] `pytest -q` unchanged
