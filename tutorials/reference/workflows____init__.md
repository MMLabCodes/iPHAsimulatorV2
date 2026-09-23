# workflows/__init__.py

Public re-exports for the earlier design, validation and HPC workflow helpers. This module contains no explicit function definitions of its own; imported functions are documented in their defining modules.

[Current source](../../src/iphasimulator/workflows/__init__.py)

This page is generated from source syntax. Original docstrings can be incomplete or outdated; module notes above identify known discrepancies. Call/return/error lists describe direct syntax, not all behaviour inside callees. Read the source excerpt for branch order and effects. No scientific execution is implied.

Explicit functions/methods/nested helpers: **0**.

## Module imports

```python
from iphasimulator.workflows.design import PolymerDesign, design_polymer, supported_polymer_table
from iphasimulator.workflows.hpc import load_workflow_config, render_slurm_script, target_stage_name, targets_from_config, workflow_plan
from iphasimulator.workflows.validation import DEFAULT_VALIDATION_TARGETS, LARGE_VALIDATION_TARGETS, ValidationTarget, build_validation_molecules, describe_molecules, export_molecules
```

No explicit function definitions occur in this module.
