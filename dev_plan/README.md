# dev_plan — how to use these files with Claude Code (VS Code)

| File | What |
|---|---|
| `00_project_design.md` | Goal, current state, target architecture, schedule, open decisions (D1–D4). Read first; edit freely. |
| `01_rules_for_claude_code.md` | Standing rules. **Prepend to every WP prompt.** |
| `WP0_baseline.md` … `WP7_…md` | One self-contained task brief per work package |

## Order
WP0 → WP1 → WP2 → WP3 (WP3 can run in parallel with WP2) → WP4 → WP5 → (WP7 optional) → WP6.

## Prompt to paste into Claude Code for each WP
```
Read dev_plan/01_rules_for_claude_code.md and dev_plan/00_project_design.md §1–3,
then dev_plan/WP1_consistency_fixes.md.
Follow rule R1: give me the plan (files + exact changes) and wait for my approval.
```
After it reports (R12), check the acceptance checklist yourself before merging the branch.

## Before starting
- Decide D1–D4 in `00_project_design.md` §5 and update WP briefs if needed. D1(b) adds a section to WP3/WP4; D2 = yes enables WP7.
- Fill in the `TODO(Zhiwen)` items that only you know: enzyme–PHA system build route and force field, citation for GK13/ANC45 selectivity, the talk's opening framing.

Created 2026-09-24 in a Cowork session. It was based on a read-only review of `notebooks/01–12`, `src/`, `examples/output/` and `md_simulation_scripts/`.
