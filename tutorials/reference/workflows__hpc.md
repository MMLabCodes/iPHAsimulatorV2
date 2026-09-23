# workflows/hpc.py

Merge YAML defaults, parse targets, describe enabled stages and render a Slurm script for the older configured-workflow runner. The script is a starting template requiring site/path/log review, not a universal submission configuration.

[Current source](../../src/iphasimulator/workflows/hpc.py)

This page is generated from source syntax. Original docstrings can be incomplete or outdated; module notes above identify known discrepancies. Call/return/error lists describe direct syntax, not all behaviour inside callees. Read the source excerpt for branch order and effects. No scientific execution is implied.

Explicit functions/methods/nested helpers: **6**.

## Module imports

```python
from __future__ import annotations
from pathlib import Path
from typing import Any
import yaml
from iphasimulator.workflows.validation import ValidationTarget
```

## Function map

- [`_deep_merge` — source line 53](#definition-53)
- [`load_workflow_config` — source line 63](#definition-63)
- [`targets_from_config` — source line 74](#definition-74)
- [`target_stage_name` — source line 95](#definition-95)
- [`workflow_plan` — source line 101](#definition-101)
- [`render_slurm_script` — source line 127](#definition-127)

<a id="definition-53"></a>

## `_deep_merge`

Source lines 53–60. Internal helper/protocol method.

```python
def _deep_merge(base: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| base | dict[str, Any] | required |
| overrides | dict[str, Any] | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `_deep_merge`, `dict`, `isinstance`, `merged.get`, `overrides.items`.

Explicit return expressions; different branches may return different objects:

```python
merged
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _deep_merge(base: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged
```

</details>

<a id="definition-63"></a>

## `load_workflow_config`

Source lines 63–71. Named callable; inspect its callers before treating it as a stable public API.

```python
def load_workflow_config(path: str | Path) -> dict[str, Any]: ...
```

### Purpose and original contract

Load a YAML workflow config and apply defaults.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| path | str \| Path | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `Path`, `ValueError`, `_deep_merge`, `config_path.open`, `isinstance`, `yaml.safe_load`.

Explicit return expressions; different branches may return different objects:

```python
_deep_merge(DEFAULT_WORKFLOW_CONFIG, loaded)
```

Calls worth inspecting for I/O, state changes or delegated execution: `config_path.open`, `yaml.safe_load`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError(f'Workflow config must be a YAML mapping: {config_path}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def load_workflow_config(path: str | Path) -> dict[str, Any]:
    """Load a YAML workflow config and apply defaults."""

    config_path = Path(path)
    with config_path.open() as handle:
        loaded = yaml.safe_load(handle) or {}
    if not isinstance(loaded, dict):
        raise ValueError(f"Workflow config must be a YAML mapping: {config_path}")
    return _deep_merge(DEFAULT_WORKFLOW_CONFIG, loaded)
```

</details>

<a id="definition-74"></a>

## `targets_from_config`

Source lines 74–92. Named callable; inspect its callers before treating it as a stable public API.

```python
def targets_from_config(config: dict[str, Any]) -> tuple[ValidationTarget, ...]: ...
```

### Purpose and original contract

Parse validation targets from workflow config.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| config | dict[str, Any] | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValidationTarget`, `ValueError`, `config.get`, `int`, `isinstance`, `parsed.append`, `target.get`, `tuple`.

Explicit return expressions; different branches may return different objects:

```python
tuple(parsed)
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('Workflow config must define a non-empty targets list')
ValueError('Each target must be a mapping')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def targets_from_config(config: dict[str, Any]) -> tuple[ValidationTarget, ...]:
    """Parse validation targets from workflow config."""

    targets = config.get("targets", [])
    if not isinstance(targets, list) or not targets:
        raise ValueError("Workflow config must define a non-empty targets list")

    parsed: list[ValidationTarget] = []
    for target in targets:
        if not isinstance(target, dict):
            raise ValueError("Each target must be a mapping")
        parsed.append(
            ValidationTarget(
                monomer=target["monomer"],
                degree=int(target["degree"]),
                stereochemistry=target.get("stereochemistry", "R"),
            )
        )
    return tuple(parsed)
```

</details>

<a id="definition-95"></a>

## `target_stage_name`

Source lines 95–98. Named callable; inspect its callers before treating it as a stable public API.

```python
def target_stage_name(target: ValidationTarget) -> str: ...
```

### Purpose and original contract

Return the short target name used for MD output directories.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| target | ValidationTarget | required |

### How to read this implementation

No direct function calls were found in this definition's own body.

Explicit return expressions; different branches may return different objects:

```python
target.name
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def target_stage_name(target: ValidationTarget) -> str:
    """Return the short target name used for MD output directories."""

    return target.name
```

</details>

<a id="definition-101"></a>

## `workflow_plan`

Source lines 101–124. Named callable; inspect its callers before treating it as a stable public API.

```python
def workflow_plan(config: dict[str, Any]) -> list[str]: ...
```

### Purpose and original contract

Return human-readable planned workflow actions.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| config | dict[str, Any] | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `Path`, `plan.append`, `stages.get`, `target_stage_name`, `targets_from_config`.

Explicit return expressions; different branches may return different objects:

```python
plan
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def workflow_plan(config: dict[str, Any]) -> list[str]:
    """Return human-readable planned workflow actions."""

    stages = config["stages"]
    output_root = Path(config["output_root"])
    plan: list[str] = []
    structure_root = output_root / "polymer_structures"
    for target in targets_from_config(config):
        stage_name = target_stage_name(target)
        if stages.get("build", False):
            plan.append(
                f"build {target.name} -> {structure_root / (target.name + '.sdf')}"
            )
        if stages.get("gaff2", False):
            plan.append(
                f"gaff2 {target.name} -> "
                f"{output_root / 'md_tests' / stage_name / 'gaff2'}"
            )
        if stages.get("openmm", False):
            plan.append(
                f"openmm dry {stage_name} -> "
                f"{output_root / 'md_tests' / stage_name / 'openmm' / 'dry_polymer'}"
            )
    return plan
```

</details>

<a id="definition-127"></a>

## `render_slurm_script`

Source lines 127–163. Named callable; inspect its callers before treating it as a stable public API.

```python
def render_slurm_script(*, config_path: str | Path, repo_root: str | Path='.', config: dict[str, Any] | None=None) -> str: ...
```

### Purpose and original contract

Render a SLURM submission script for a configured workflow.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| config_path (keyword-only) | str \| Path | required |
| repo_root (keyword-only) | str \| Path | '.' |
| config (keyword-only) | dict[str, Any] \| None | None |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `'\n'.join`, `Path`, `load_workflow_config`.

Explicit return expressions; different branches may return different objects:

```python
'\n'.join(['#!/usr/bin/env bash', f"#SBATCH --job-name={slurm['job_name']}", f"#SBATCH --time={slurm['time']}", f"#SBATCH --partition={slurm['partition']}", f"#SBATCH --cpus-per-task={slurm['cpus_per_task']}", f"#SBATCH --mem={slurm['mem']}", '#SBATCH --output=logs/%x-%j.out', '#SBATCH --error=logs/%x-%j.err', '', 'set -euo pipefail', '', f'cd {repo_path}', 'mkdir -p logs', '', '# Adjust this bloc … [full expression below]
```

Calls worth inspecting for I/O, state changes or delegated execution: `load_workflow_config`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def render_slurm_script(
    *,
    config_path: str | Path,
    repo_root: str | Path = ".",
    config: dict[str, Any] | None = None,
) -> str:
    """Render a SLURM submission script for a configured workflow."""

    workflow_config = config or load_workflow_config(config_path)
    slurm = workflow_config["slurm"]
    repo_path = Path(repo_root)
    config_path = Path(config_path)

    return "\n".join(
        [
            "#!/usr/bin/env bash",
            f"#SBATCH --job-name={slurm['job_name']}",
            f"#SBATCH --time={slurm['time']}",
            f"#SBATCH --partition={slurm['partition']}",
            f"#SBATCH --cpus-per-task={slurm['cpus_per_task']}",
            f"#SBATCH --mem={slurm['mem']}",
            "#SBATCH --output=logs/%x-%j.out",
            "#SBATCH --error=logs/%x-%j.err",
            "",
            "set -euo pipefail",
            "",
            f"cd {repo_path}",
            "mkdir -p logs",
            "",
            "# Adjust this block to match your HPC module/conda setup.",
            "source \"$(conda info --base)/etc/profile.d/conda.sh\"",
            f"conda activate {slurm['conda_env']}",
            "",
            f"PYTHONPATH=src python examples/run_configured_workflow.py --config {config_path}",
            "",
        ]
    )
```

</details>
