# trajectory_preprocessing.py

Orchestrate centring-index preparation, trajectory processing, optional fitting and representative-frame extraction. The full System remains in output. dry_run skips trajectory commands after index preparation, so it can still write an index.

[Current source](../../src/iphasimulator/trajectory_preprocessing.py)

This page is generated from source syntax. Original docstrings can be incomplete or outdated; module notes above identify known discrepancies. Call/return/error lists describe direct syntax, not all behaviour inside callees. Read the source excerpt for branch order and effects. No scientific execution is implied.

Explicit functions/methods/nested helpers: **3**.

## Module imports

```python
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import subprocess
from iphasimulator.trajectory_centering import CenterIndexResult, ensure_center_index
from iphasimulator.trajectory_frame_extraction import extract_first_frame
from iphasimulator.trajectory_gromacs_trjconv import Runner, TrjconvResult, center_and_compact_wrap, fit_trajectory
```

## Classes and result records

### `TrajectoryPreprocessingOutputs`

Files created by the standard preprocessing workflow.

Decorators: `dataclass(frozen=True)`.

Declared fields/defaults (instance state may also be set by methods):

```python
system_dir: Path
center_index: CenterIndexResult
raw_trajectory_path: Path
structure_path: Path
centered_trajectory_path: Path
fitted_trajectory_path: Path | None
representative_frame_path: Path | None
center_result: TrjconvResult | None
fit_result: TrjconvResult | None
frame_result: TrjconvResult | None
```

Dataclass-generated methods are implicit and are not counted as explicit function definitions.

## Function map

- [`TrajectoryPreprocessingOutputs.analysis_trajectory_path` — source line 35](#definition-35)
- [`_resolve_existing_path` — source line 39](#definition-39)
- [`preprocess_gromacs_trajectory` — source line 47](#definition-47)

<a id="definition-35"></a>

## `TrajectoryPreprocessingOutputs.analysis_trajectory_path`

Source lines 35–36. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `property`.

```python
def analysis_trajectory_path(self) -> Path: ...
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
self.fitted_trajectory_path or self.centered_trajectory_path
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def analysis_trajectory_path(self) -> Path:
    return self.fitted_trajectory_path or self.centered_trajectory_path
```

</details>

<a id="definition-39"></a>

## `_resolve_existing_path`

Source lines 39–44. Internal helper/protocol method.

```python
def _resolve_existing_path(system_dir: Path, filename: str | Path) -> Path: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| system_dir | Path | required |
| filename | str \| Path | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `Path`, `path.is_absolute`.

Explicit return expressions; different branches may return different objects:

```python
path
system_dir / path
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _resolve_existing_path(system_dir: Path, filename: str | Path) -> Path:
    path = Path(filename)
    if path.is_absolute():
        return path

    return system_dir / path
```

</details>

<a id="definition-47"></a>

## `preprocess_gromacs_trajectory`

Source lines 47–160. Named callable; inspect its callers before treating it as a stable public API.

```python
def preprocess_gromacs_trajectory(system_dir: str | Path, *, trajectory: str | Path='step7_production.xtc', structure: str | Path='step7_production.tpr', index: str | Path='index.ndx', workflow_type: str='polymer', source_groups: tuple[str, ...] | list[str] | None=None, fit: bool=False, extract_representative_frame: bool=True, gmx_command: str='gmx', runner: Runner=subprocess.run, dry_run: bool=False) -> TrajectoryPreprocessingOutputs: ...
```

### Purpose and original contract

Run the standard GROMACS preprocessing pipeline.

The output trajectory keeps ``System`` so water and ions remain available for
downstream analyses, while centering/fitting use the reusable ``center`` group.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| system_dir | str \| Path | required |
| trajectory (keyword-only) | str \| Path | 'step7_production.xtc' |
| structure (keyword-only) | str \| Path | 'step7_production.tpr' |
| index (keyword-only) | str \| Path | 'index.ndx' |
| workflow_type (keyword-only) | str | 'polymer' |
| source_groups (keyword-only) | tuple[str, ...] \| list[str] \| None | None |
| fit (keyword-only) | bool | False |
| extract_representative_frame (keyword-only) | bool | True |
| gmx_command (keyword-only) | str | 'gmx' |
| runner (keyword-only) | Runner | subprocess.run |
| dry_run (keyword-only) | bool | False |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `', '.join`, `FileNotFoundError`, `Path`, `TrajectoryPreprocessingOutputs`, `_resolve_existing_path`, `center_and_compact_wrap`, `ensure_center_index`, `extract_first_frame`, `fit_trajectory`, `path.exists`, `str`.

Explicit return expressions; different branches may return different objects:

```python
TrajectoryPreprocessingOutputs(system_dir=system_path, center_index=center_index, raw_trajectory_path=raw_trajectory_path, structure_path=structure_path, centered_trajectory_path=centered_path, fitted_trajectory_path=fitted_path if fit else None, representative_frame_path=frame_path if extract_representative_frame else None, center_result=None, fit_result=None, frame_result=None)
TrajectoryPreprocessingOutputs(system_dir=system_path, center_index=center_index, raw_trajectory_path=raw_trajectory_path, structure_path=structure_path, centered_trajectory_path=centered_path, fitted_trajectory_path=fitted_path, representative_frame_path=frame_path, center_result=center_result, fit_result=fit_result, frame_result=frame_result)
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
FileNotFoundError(f'Cannot preprocess trajectory because required GROMACS outputs are missing: {missing_text}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def preprocess_gromacs_trajectory(
    system_dir: str | Path,
    *,
    trajectory: str | Path = "step7_production.xtc",
    structure: str | Path = "step7_production.tpr",
    index: str | Path = "index.ndx",
    workflow_type: str = "polymer",
    source_groups: tuple[str, ...] | list[str] | None = None,
    fit: bool = False,
    extract_representative_frame: bool = True,
    gmx_command: str = "gmx",
    runner: Runner = subprocess.run,
    dry_run: bool = False,
) -> TrajectoryPreprocessingOutputs:
    """Run the standard GROMACS preprocessing pipeline.

    The output trajectory keeps ``System`` so water and ions remain available for
    downstream analyses, while centering/fitting use the reusable ``center`` group.
    """

    system_path = Path(system_dir)

    source_index = _resolve_existing_path(system_path, index)
    center_index = ensure_center_index(
        source_index,
        system_path / "center.ndx",
        workflow_type=workflow_type,
        source_groups=source_groups,
    )

    raw_trajectory_path = _resolve_existing_path(system_path, trajectory)
    structure_path = _resolve_existing_path(system_path, structure)
    centered_path = system_path / "step7_centered.xtc"
    fitted_path = system_path / "step7_fitted.xtc"
    frame_path = system_path / "representative_frame.gro"

    if dry_run:
        return TrajectoryPreprocessingOutputs(
            system_dir=system_path,
            center_index=center_index,
            raw_trajectory_path=raw_trajectory_path,
            structure_path=structure_path,
            centered_trajectory_path=centered_path,
            fitted_trajectory_path=fitted_path if fit else None,
            representative_frame_path=frame_path if extract_representative_frame else None,
            center_result=None,
            fit_result=None,
            frame_result=None,
        )

    missing_inputs = [
        path for path in (raw_trajectory_path, structure_path) if not path.exists()
    ]
    if missing_inputs:
        missing_text = ", ".join(str(path) for path in missing_inputs)
        raise FileNotFoundError(
            "Cannot preprocess trajectory because required GROMACS outputs are "
            f"missing: {missing_text}"
        )

    center_result = center_and_compact_wrap(
        trajectory=raw_trajectory_path,
        structure=structure_path,
        index=center_index.index_path,
        output=centered_path,
        center_group=center_index.center_group,
        output_group="System",
        gmx_command=gmx_command,
        runner=runner,
    )

    fit_result: TrjconvResult | None = None
    analysis_trajectory = centered_path
    if fit:
        fit_result = fit_trajectory(
            trajectory=centered_path,
            structure=structure_path,
            index=center_index.index_path,
            output=fitted_path,
            fit_group=center_index.center_group,
            output_group="System",
            gmx_command=gmx_command,
            runner=runner,
        )
        analysis_trajectory = fitted_path
    else:
        fitted_path = None

    frame_result: TrjconvResult | None = None
    if extract_representative_frame:
        frame_result = extract_first_frame(
            trajectory=analysis_trajectory,
            structure=structure_path,
            index=center_index.index_path,
            output=frame_path,
            output_group="System",
            gmx_command=gmx_command,
            runner=runner,
        )
    else:
        frame_path = None

    return TrajectoryPreprocessingOutputs(
        system_dir=system_path,
        center_index=center_index,
        raw_trajectory_path=raw_trajectory_path,
        structure_path=structure_path,
        centered_trajectory_path=centered_path,
        fitted_trajectory_path=fitted_path,
        representative_frame_path=frame_path,
        center_result=center_result,
        fit_result=fit_result,
        frame_result=frame_result,
    )
```

</details>
