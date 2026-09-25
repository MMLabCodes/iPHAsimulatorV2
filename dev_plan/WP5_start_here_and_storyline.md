# WP5 — `00_start_here` notebook and presentation storyline

**Prepend:** `dev_plan/01_rules_for_claude_code.md` · **Branch:** `dev/wp5-storyline` (from WP3 + WP4)

## A. `notebooks/00_start_here.ipynb` (markdown-heavy; ≤ 3 small code cells)
1. What iPHASimulator is: 3 sentences. The target audience is scientists who are not MD specialists.
2. Workflow map: a static figure or mermaid showing build → validate → export → parameterise (GAFF2) → engine setup (GROMACS main route; OpenMM dry check) → HPC → preprocess → analyse → enzyme–PHA results (13).
3. Table of all notebooks with these columns: stage · notebook · status (`demo` = shows real saved results; `workflow` = prepares files; `template` = not functional yet, e.g. 05B, 06D) · runtime in demo mode (from the WP2/WP6 report).
4. "Demo mode" explanation: which flags exist and what setting them to `True` does.
5. Code cell: environment check (imports rdkit, mdtraj, MDAnalysis; `ambertools_available()`; `shutil.which("gmx")`), printed as a table. It must not fail when a tool is missing; report `False` instead.
6. Code cell: check that the key saved outputs exist (P3HB_4 gaff2 prmtop, solvated `step5_input.gro`, NB08 centered xtc, the NB13 CSVs), using `ipha_paths`.

## B. `dev_plan/presentation_outline.md`
A slide-by-slide outline, about 12 slides for ~20 min. For each slide: title · one-line message · source notebook/cell or figure file · the caveat to say out loud. Suggested spine; adjust it after reading 13's outputs:
1. Why PHA and why enzymatic depolymerisation (TODO: Zhiwen's framing)
2. Problem: no PHA-aware, stereo-correct MD setup tool
3. iPHASimulator pipeline (00 map)
4. Build & validate: R-configured oligomers, SMILES/chirality table (03/04)
5. Parameterisation & engines: GAFF2 → GROMACS solvated box (05A/06C); one line on the FF composition caveat
6. Single-polymer MD example: Rg / end-to-end / SASA for P3HB_4 (09), labelled "one 100 ns run"
7. Enzyme–PHA systems: 2 enzymes × 2 polymers, 1 µs each (13 §2)
8. Stability: backbone RMSD (13 §3)
9. Proximity: min distance plus % time within cutoff (13 §4), the headline
10. Where: top residues and catalytic Ser (13 §5–6)
11. Limitations & next steps: replicas, FF harmonisation, polymer benchmark, SwiftPol comparison, custom-stereo rule
12. Summary

Also list, per slide, the **live demo cell**, if any, to run during the talk. Recommend at most two live cells, e.g. NB02 Mode A build and NB03 drawing, with everything else pre-rendered.

## Acceptance
- [ ] 00 runs in < 30 s and doesn't fail when gmx or AmberTools is absent
- [ ] Status column is correct for every notebook (checked against WP2/WP3 results)
- [ ] Outline references only figures and cells that exist
