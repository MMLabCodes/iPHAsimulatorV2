# trajectory_gromacs_trjconv.py

Build and execute GROMACS trajectory commands with explicit group-selection input. Dedicated wrappers express reconstruction, centring/compact wrapping and fitting. Optional runner injection supports testing command composition.

[Current source](../../src/iphasimulator/trajectory_gromacs_trjconv.py)

This page is generated from source syntax. Original docstrings can be incomplete or outdated; module notes above identify known discrepancies. Call/return/error lists describe direct syntax, not all behaviour inside callees. Read the source excerpt for branch order and effects. No scientific execution is implied.

Explicit functions/methods/nested helpers: **7**.

## Module imports

```python
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import subprocess
from typing import Callable, Sequence
```

## Classes and result records

### `TrjconvResult`

Captured command result for a ``gmx trjconv`` operation.

Decorators: `dataclass(frozen=True)`.

Declared fields/defaults (instance state may also be set by methods):

```python
command: tuple[str, ...]
selections: tuple[str, ...]
output_path: Path
returncode: int
stdout: str
stderr: str
```

Dataclass-generated methods are implicit and are not counted as explicit function definitions.

## Function map

- [`TrjconvResult.ok` — source line 26](#definition-26)
- [`_selection_input` — source line 30](#definition-30)
- [`run_trjconv` — source line 34](#definition-34)
- [`center_and_compact_wrap` — source line 88](#definition-88)
- [`reconstruct_molecules` — source line 115](#definition-115)
- [`compact_wrap` — source line 141](#definition-141)
- [`fit_trajectory` — source line 167](#definition-167)

<a id="definition-26"></a>

## `TrjconvResult.ok`

Source lines 26–27. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `property`.

```python
def ok(self) -> bool: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |

### How to read this implementation

No direct function calls were found in this definition's own body.

Explicit return expressions; different branches may return different objects:

```python
self.returncode == 0
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def ok(self) -> bool:
    return self.returncode == 0
```

</details>

<a id="definition-30"></a>

## `_selection_input`

Source lines 30–31. Internal helper/protocol method.

```python
def _selection_input(selections: Sequence[str]) -> str: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| selections | Sequence[str] | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `'\n'.join`.

Explicit return expressions; different branches may return different objects:

```python
'\n'.join(selections) + '\n'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _selection_input(selections: Sequence[str]) -> str:
    return "\n".join(selections) + "\n"
```

</details>

<a id="definition-34"></a>

## `run_trjconv`

Source lines 34–85. Named callable; inspect its callers before treating it as a stable public API.

```python
def run_trjconv(*, trajectory: str | Path, structure: str | Path, output: str | Path, index: str | Path | None=None, selections: Sequence[str]=('System',), trjconv_args: Sequence[str]=(), gmx_command: str='gmx', cwd: str | Path | None=None, runner: Runner=subprocess.run) -> TrjconvResult: ...
```

### Purpose and original contract

Run ``gmx trjconv`` with explicit stdin group selections.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| trajectory (keyword-only) | str \| Path | required |
| structure (keyword-only) | str \| Path | required |
| output (keyword-only) | str \| Path | required |
| index (keyword-only) | str \| Path \| None | None |
| selections (keyword-only) | Sequence[str] | ('System',) |
| trjconv_args (keyword-only) | Sequence[str] | () |
| gmx_command (keyword-only) | str | 'gmx' |
| cwd (keyword-only) | str \| Path \| None | None |
| runner (keyword-only) | Runner | subprocess.run |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `Path`, `RuntimeError`, `TrjconvResult`, `_selection_input`, `command.extend`, `output_path.parent.mkdir`, `runner`, `str`, `tuple`.

Explicit return expressions; different branches may return different objects:

```python
TrjconvResult(command=tuple(command), selections=tuple(selections), output_path=output_path, returncode=result.returncode, stdout=result.stdout, stderr=result.stderr)
```

Calls worth inspecting for I/O, state changes or delegated execution: `output_path.parent.mkdir`, `runner`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
RuntimeError(f'gmx trjconv failed with return code {result.returncode}: {result.stderr or result.stdout}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def run_trjconv(
    *,
    trajectory: str | Path,
    structure: str | Path,
    output: str | Path,
    index: str | Path | None = None,
    selections: Sequence[str] = ("System",),
    trjconv_args: Sequence[str] = (),
    gmx_command: str = "gmx",
    cwd: str | Path | None = None,
    runner: Runner = subprocess.run,
) -> TrjconvResult:
    """Run ``gmx trjconv`` with explicit stdin group selections."""

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    command: list[str] = [
        gmx_command,
        "trjconv",
        "-f",
        str(trajectory),
        "-s",
        str(structure),
    ]
    if index is not None:
        command.extend(["-n", str(index)])
    command.extend(trjconv_args)
    command.extend(["-o", str(output_path)])

    result = runner(
        command,
        input=_selection_input(selections),
        text=True,
        capture_output=True,
        cwd=Path(cwd) if cwd is not None else None,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "gmx trjconv failed with return code "
            f"{result.returncode}: {result.stderr or result.stdout}"
        )

    return TrjconvResult(
        command=tuple(command),
        selections=tuple(selections),
        output_path=output_path,
        returncode=result.returncode,
        stdout=result.stdout,
        stderr=result.stderr,
    )
```

</details>

<a id="definition-88"></a>

## `center_and_compact_wrap`

Source lines 88–112. Named callable; inspect its callers before treating it as a stable public API.

```python
def center_and_compact_wrap(*, trajectory: str | Path, structure: str | Path, index: str | Path, output: str | Path, center_group: str='center', output_group: str='System', gmx_command: str='gmx', cwd: str | Path | None=None, runner: Runner=subprocess.run) -> TrjconvResult: ...
```

### Purpose and original contract

Center on ``center_group`` and write the full compact solvated system.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| trajectory (keyword-only) | str \| Path | required |
| structure (keyword-only) | str \| Path | required |
| index (keyword-only) | str \| Path | required |
| output (keyword-only) | str \| Path | required |
| center_group (keyword-only) | str | 'center' |
| output_group (keyword-only) | str | 'System' |
| gmx_command (keyword-only) | str | 'gmx' |
| cwd (keyword-only) | str \| Path \| None | None |
| runner (keyword-only) | Runner | subprocess.run |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `run_trjconv`.

Explicit return expressions; different branches may return different objects:

```python
run_trjconv(trajectory=trajectory, structure=structure, index=index, output=output, selections=(center_group, output_group), trjconv_args=('-pbc', 'mol', '-ur', 'compact', '-center'), gmx_command=gmx_command, cwd=cwd, runner=runner)
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def center_and_compact_wrap(
    *,
    trajectory: str | Path,
    structure: str | Path,
    index: str | Path,
    output: str | Path,
    center_group: str = "center",
    output_group: str = "System",
    gmx_command: str = "gmx",
    cwd: str | Path | None = None,
    runner: Runner = subprocess.run,
) -> TrjconvResult:
    """Center on ``center_group`` and write the full compact solvated system."""

    return run_trjconv(
        trajectory=trajectory,
        structure=structure,
        index=index,
        output=output,
        selections=(center_group, output_group),
        trjconv_args=("-pbc", "mol", "-ur", "compact", "-center"),
        gmx_command=gmx_command,
        cwd=cwd,
        runner=runner,
    )
```

</details>

<a id="definition-115"></a>

## `reconstruct_molecules`

Source lines 115–138. Named callable; inspect its callers before treating it as a stable public API.

```python
def reconstruct_molecules(*, trajectory: str | Path, structure: str | Path, index: str | Path, output: str | Path, output_group: str='System', gmx_command: str='gmx', cwd: str | Path | None=None, runner: Runner=subprocess.run) -> TrjconvResult: ...
```

### Purpose and original contract

Repair molecules split across periodic boundaries without centering.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| trajectory (keyword-only) | str \| Path | required |
| structure (keyword-only) | str \| Path | required |
| index (keyword-only) | str \| Path | required |
| output (keyword-only) | str \| Path | required |
| output_group (keyword-only) | str | 'System' |
| gmx_command (keyword-only) | str | 'gmx' |
| cwd (keyword-only) | str \| Path \| None | None |
| runner (keyword-only) | Runner | subprocess.run |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `run_trjconv`.

Explicit return expressions; different branches may return different objects:

```python
run_trjconv(trajectory=trajectory, structure=structure, index=index, output=output, selections=(output_group,), trjconv_args=('-pbc', 'mol'), gmx_command=gmx_command, cwd=cwd, runner=runner)
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def reconstruct_molecules(
    *,
    trajectory: str | Path,
    structure: str | Path,
    index: str | Path,
    output: str | Path,
    output_group: str = "System",
    gmx_command: str = "gmx",
    cwd: str | Path | None = None,
    runner: Runner = subprocess.run,
) -> TrjconvResult:
    """Repair molecules split across periodic boundaries without centering."""

    return run_trjconv(
        trajectory=trajectory,
        structure=structure,
        index=index,
        output=output,
        selections=(output_group,),
        trjconv_args=("-pbc", "mol"),
        gmx_command=gmx_command,
        cwd=cwd,
        runner=runner,
    )
```

</details>

<a id="definition-141"></a>

## `compact_wrap`

Source lines 141–164. Named callable; inspect its callers before treating it as a stable public API.

```python
def compact_wrap(*, trajectory: str | Path, structure: str | Path, index: str | Path, output: str | Path, output_group: str='System', gmx_command: str='gmx', cwd: str | Path | None=None, runner: Runner=subprocess.run) -> TrjconvResult: ...
```

### Purpose and original contract

Wrap the full system into a compact unit-cell representation.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| trajectory (keyword-only) | str \| Path | required |
| structure (keyword-only) | str \| Path | required |
| index (keyword-only) | str \| Path | required |
| output (keyword-only) | str \| Path | required |
| output_group (keyword-only) | str | 'System' |
| gmx_command (keyword-only) | str | 'gmx' |
| cwd (keyword-only) | str \| Path \| None | None |
| runner (keyword-only) | Runner | subprocess.run |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `run_trjconv`.

Explicit return expressions; different branches may return different objects:

```python
run_trjconv(trajectory=trajectory, structure=structure, index=index, output=output, selections=(output_group,), trjconv_args=('-ur', 'compact'), gmx_command=gmx_command, cwd=cwd, runner=runner)
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def compact_wrap(
    *,
    trajectory: str | Path,
    structure: str | Path,
    index: str | Path,
    output: str | Path,
    output_group: str = "System",
    gmx_command: str = "gmx",
    cwd: str | Path | None = None,
    runner: Runner = subprocess.run,
) -> TrjconvResult:
    """Wrap the full system into a compact unit-cell representation."""

    return run_trjconv(
        trajectory=trajectory,
        structure=structure,
        index=index,
        output=output,
        selections=(output_group,),
        trjconv_args=("-ur", "compact"),
        gmx_command=gmx_command,
        cwd=cwd,
        runner=runner,
    )
```

</details>

<a id="definition-167"></a>

## `fit_trajectory`

Source lines 167–192. Named callable; inspect its callers before treating it as a stable public API.

```python
def fit_trajectory(*, trajectory: str | Path, structure: str | Path, index: str | Path, output: str | Path, fit_group: str='center', output_group: str='System', fit: str='rot+trans', gmx_command: str='gmx', cwd: str | Path | None=None, runner: Runner=subprocess.run) -> TrjconvResult: ...
```

### Purpose and original contract

Fit/alignment wrapper using the centering group as the reference group.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| trajectory (keyword-only) | str \| Path | required |
| structure (keyword-only) | str \| Path | required |
| index (keyword-only) | str \| Path | required |
| output (keyword-only) | str \| Path | required |
| fit_group (keyword-only) | str | 'center' |
| output_group (keyword-only) | str | 'System' |
| fit (keyword-only) | str | 'rot+trans' |
| gmx_command (keyword-only) | str | 'gmx' |
| cwd (keyword-only) | str \| Path \| None | None |
| runner (keyword-only) | Runner | subprocess.run |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `run_trjconv`.

Explicit return expressions; different branches may return different objects:

```python
run_trjconv(trajectory=trajectory, structure=structure, index=index, output=output, selections=(fit_group, output_group), trjconv_args=('-fit', fit), gmx_command=gmx_command, cwd=cwd, runner=runner)
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def fit_trajectory(
    *,
    trajectory: str | Path,
    structure: str | Path,
    index: str | Path,
    output: str | Path,
    fit_group: str = "center",
    output_group: str = "System",
    fit: str = "rot+trans",
    gmx_command: str = "gmx",
    cwd: str | Path | None = None,
    runner: Runner = subprocess.run,
) -> TrjconvResult:
    """Fit/alignment wrapper using the centering group as the reference group."""

    return run_trjconv(
        trajectory=trajectory,
        structure=structure,
        index=index,
        output=output,
        selections=(fit_group, output_group),
        trjconv_args=("-fit", fit),
        gmx_command=gmx_command,
        cwd=cwd,
        runner=runner,
    )
```

</details>
