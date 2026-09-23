# trajectory_frame_extraction.py

Small GROMACS trjconv wrappers that extract a specified or first frame. The resulting frame must retain the atom ordering expected by downstream consumers.

[Current source](../../src/iphasimulator/trajectory_frame_extraction.py)

This page is generated from source syntax. Original docstrings can be incomplete or outdated; module notes above identify known discrepancies. Call/return/error lists describe direct syntax, not all behaviour inside callees. Read the source excerpt for branch order and effects. No scientific execution is implied.

Explicit functions/methods/nested helpers: **2**.

## Module imports

```python
from __future__ import annotations
from pathlib import Path
import subprocess
from iphasimulator.trajectory_gromacs_trjconv import Runner, TrjconvResult, run_trjconv
```

## Function map

- [`extract_frame` — source line 11](#definition-11)
- [`extract_first_frame` — source line 45](#definition-45)

<a id="definition-11"></a>

## `extract_frame`

Source lines 11–42. Named callable; inspect its callers before treating it as a stable public API.

```python
def extract_frame(*, trajectory: str | Path, structure: str | Path, output: str | Path, index: str | Path | None=None, time_ps: float | int | None=None, output_group: str='System', gmx_command: str='gmx', cwd: str | Path | None=None, runner: Runner=subprocess.run) -> TrjconvResult: ...
```

### Purpose and original contract

Extract a single representative frame using ``gmx trjconv``.

Pass ``time_ps`` to select the frame nearest that simulation time.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| trajectory (keyword-only) | str \| Path | required |
| structure (keyword-only) | str \| Path | required |
| output (keyword-only) | str \| Path | required |
| index (keyword-only) | str \| Path \| None | None |
| time_ps (keyword-only) | float \| int \| None | None |
| output_group (keyword-only) | str | 'System' |
| gmx_command (keyword-only) | str | 'gmx' |
| cwd (keyword-only) | str \| Path \| None | None |
| runner (keyword-only) | Runner | subprocess.run |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `args.extend`, `run_trjconv`, `str`, `tuple`.

Explicit return expressions; different branches may return different objects:

```python
run_trjconv(trajectory=trajectory, structure=structure, output=output, index=index, selections=(output_group,), trjconv_args=tuple(args), gmx_command=gmx_command, cwd=cwd, runner=runner)
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def extract_frame(
    *,
    trajectory: str | Path,
    structure: str | Path,
    output: str | Path,
    index: str | Path | None = None,
    time_ps: float | int | None = None,
    output_group: str = "System",
    gmx_command: str = "gmx",
    cwd: str | Path | None = None,
    runner: Runner = subprocess.run,
) -> TrjconvResult:
    """Extract a single representative frame using ``gmx trjconv``.

    Pass ``time_ps`` to select the frame nearest that simulation time.
    """

    args: list[str] = []
    if time_ps is not None:
        args.extend(["-dump", str(time_ps)])

    return run_trjconv(
        trajectory=trajectory,
        structure=structure,
        output=output,
        index=index,
        selections=(output_group,),
        trjconv_args=tuple(args),
        gmx_command=gmx_command,
        cwd=cwd,
        runner=runner,
    )
```

</details>

<a id="definition-45"></a>

## `extract_first_frame`

Source lines 45–48. Named callable; inspect its callers before treating it as a stable public API.

```python
def extract_first_frame(**kwargs) -> TrjconvResult: ...
```

### Purpose and original contract

Extract frame 0 as a lightweight visual sanity check.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| **kwargs | variadic keyword | optional |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `extract_frame`.

Explicit return expressions; different branches may return different objects:

```python
extract_frame(time_ps=0, **kwargs)
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def extract_first_frame(**kwargs) -> TrjconvResult:
    """Extract frame 0 as a lightweight visual sanity check."""

    return extract_frame(time_ps=0, **kwargs)
```

</details>
