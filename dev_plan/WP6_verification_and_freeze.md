# WP6 — Verification, freeze and rehearsal support

**Prepend:** `dev_plan/01_rules_for_claude_code.md` · **Branch:** `dev/wp6-freeze` (after WP1–WP5 are merged)

## A. Full demo-mode execution (allowed in this WP)
- Execute **copies** of `notebooks/00–13` in order into `/tmp/ipha_freeze/` with the `ipha_clean` kernel (nbconvert/nbclient, 600 s timeout per notebook, cwd = repo `notebooks/`).
- Report per notebook: pass/fail, wall time, number of error outputs, and any warning text printed to stderr.
- Snapshot check: before and after, record `find examples/output "$IPHA_DATA_ROOT" -newer <marker>`; the result must be empty (no writes in demo mode). Report it.

## B. Output comparison
For notebooks 01–04, 09, 12 and 13, compare key text outputs between the committed notebook and the fresh execution: SMILES strings, atom counts, chirality lists, frame counts, summary statistics. Tolerance: exact for strings/ints, 1e-6 relative for floats. Report any differences; don't "fix" them.

## C. Tests
- Add `tests/test_notebooks_demo_mode.py`, marked `@pytest.mark.slow` and skipped unless `IPHA_RUN_NOTEBOOK_TESTS=1`. It executes 00–04 and 13 in demo mode and asserts that there are no error outputs. Register the `slow` marker in `pyproject.toml` if pytest warns (the only `pyproject.toml` change allowed).
- `pytest -q` (default, fast) must still pass.

## D. Freeze
- Merge to `main` only after Zhiwen approves the report. Tag `presentation-freeze-YYYYMMDD`.
- Write `dev_plan/demo_checklist.md`: kernel = `ipha_clean`; `IPHA_DATA_ROOT` set (or default valid); external drive mounted if the data lives there; which notebooks to pre-open; the two live cells; fallback = the pre-executed copies in `/tmp/ipha_freeze/` exported to HTML (`jupyter nbconvert --to html`) in `examples/output/presentation_html/`.

## Acceptance
- [ ] All notebooks pass in demo mode; times reported
- [ ] No writes to `examples/output/` or DATA_ROOT during demo execution
- [ ] Output comparison report with zero unexplained differences
- [ ] HTML fallback exported; checklist written
