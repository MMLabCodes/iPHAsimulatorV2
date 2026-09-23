# trajectory_centering.py

Parse/write GROMACS index groups, choose source groups, merge atom indices and create/reuse a centring index. Index entries use the original topology atom ordering. Some helpers write files even when called by a larger dry-run workflow.

[Current source](../../src/iphasimulator/trajectory_centering.py)

This page is generated from source syntax. Original docstrings can be incomplete or outdated; module notes above identify known discrepancies. Call/return/error lists describe direct syntax, not all behaviour inside callees. Read the source excerpt for branch order and effects. No scientific execution is implied.

Explicit functions/methods/nested helpers: **9**.

## Module imports

```python
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import re
```

## Classes and result records

### `GromacsIndex`

Parsed GROMACS index groups, preserving group order.

Decorators: `dataclass(frozen=True)`.

Declared fields/defaults (instance state may also be set by methods):

```python
groups: dict[str, tuple[int, ...]]
```

Dataclass-generated methods are implicit and are not counted as explicit function definitions.

### `CenterIndexResult`

Result from creating or reusing a dedicated centering index.

Decorators: `dataclass(frozen=True)`.

Declared fields/defaults (instance state may also be set by methods):

```python
index_path: Path
center_group: str
source_groups: tuple[str, ...]
created: bool
reused_existing_center: bool
```

Dataclass-generated methods are implicit and are not counted as explicit function definitions.

## Function map

- [`GromacsIndex.names` — source line 31](#definition-31)
- [`GromacsIndex.has_group` — source line 34](#definition-34)
- [`GromacsIndex.group` — source line 39](#definition-39)
- [`_canonical_group_name` — source line 58](#definition-58)
- [`read_index` — source line 62](#definition-62)
- [`write_index` — source line 96](#definition-96)
- [`resolve_center_source_groups` — source line 114](#definition-114)
- [`merged_group_atoms` — source line 149](#definition-149)
- [`ensure_center_index` — source line 158](#definition-158)

<a id="definition-31"></a>

## `GromacsIndex.names`

Source lines 31–32. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `property`.

```python
def names(self) -> tuple[str, ...]: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `tuple`.

Explicit return expressions; different branches may return different objects:

```python
tuple(self.groups)
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def names(self) -> tuple[str, ...]:
    return tuple(self.groups)
```

</details>

<a id="definition-34"></a>

## `GromacsIndex.has_group`

Source lines 34–37. Named callable; inspect its callers before treating it as a stable public API.

```python
def has_group(self, name: str) -> bool: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| name | str | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `_canonical_group_name`.

Explicit return expressions; different branches may return different objects:

```python
_canonical_group_name(name) in {_canonical_group_name(group_name) for group_name in self.groups}
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def has_group(self, name: str) -> bool:
    return _canonical_group_name(name) in {
        _canonical_group_name(group_name) for group_name in self.groups
    }
```

</details>

<a id="definition-39"></a>

## `GromacsIndex.group`

Source lines 39–44. Named callable; inspect its callers before treating it as a stable public API.

```python
def group(self, name: str) -> tuple[int, ...]: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| name | str | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `KeyError`, `_canonical_group_name`, `self.groups.items`.

Explicit return expressions; different branches may return different objects:

```python
atoms
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
KeyError(f'Index group not found: {name}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def group(self, name: str) -> tuple[int, ...]:
    canonical = _canonical_group_name(name)
    for group_name, atoms in self.groups.items():
        if _canonical_group_name(group_name) == canonical:
            return atoms
    raise KeyError(f"Index group not found: {name}")
```

</details>

<a id="definition-58"></a>

## `_canonical_group_name`

Source lines 58–59. Internal helper/protocol method.

```python
def _canonical_group_name(name: str) -> str: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| name | str | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `' '.join`, `name.strip`, `name.strip().lower`, `name.strip().lower().split`.

Explicit return expressions; different branches may return different objects:

```python
' '.join(name.strip().lower().split())
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _canonical_group_name(name: str) -> str:
    return " ".join(name.strip().lower().split())
```

</details>

<a id="definition-62"></a>

## `read_index`

Source lines 62–93. Named callable; inspect its callers before treating it as a stable public API.

```python
def read_index(index_path: str | Path) -> GromacsIndex: ...
```

### Purpose and original contract

Read a GROMACS ``.ndx`` file into named atom groups.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| index_path | str \| Path | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `GROUP_HEADER_PATTERN.match`, `GromacsIndex`, `Path`, `ValueError`, `enumerate`, `groups.items`, `groups.setdefault`, `groups[current_name].extend`, `header_match.group`, `header_match.group(1).strip`, `int`, `line.strip`, `path.read_text`, `path.read_text().splitlines`, `stripped.split`, `tuple`.

Explicit return expressions; different branches may return different objects:

```python
GromacsIndex({name: tuple(atoms) for name, atoms in groups.items()})
```

Calls worth inspecting for I/O, state changes or delegated execution: `path.read_text`, `path.read_text().splitlines`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError(f'Empty index group name in {path}:{line_number}')
ValueError(f'Atom numbers appear before any index group in {path}:{line_number}')
ValueError(f'Invalid atom number in index group {current_name!r} at {path}:{line_number}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def read_index(index_path: str | Path) -> GromacsIndex:
    """Read a GROMACS ``.ndx`` file into named atom groups."""

    path = Path(index_path)
    groups: dict[str, list[int]] = {}
    current_name: str | None = None

    for line_number, line in enumerate(path.read_text().splitlines(), start=1):
        header_match = GROUP_HEADER_PATTERN.match(line)
        if header_match:
            current_name = header_match.group(1).strip()
            if not current_name:
                raise ValueError(f"Empty index group name in {path}:{line_number}")
            groups.setdefault(current_name, [])
            continue

        stripped = line.strip()
        if not stripped:
            continue
        if current_name is None:
            raise ValueError(
                f"Atom numbers appear before any index group in {path}:{line_number}"
            )
        try:
            groups[current_name].extend(int(value) for value in stripped.split())
        except ValueError as exc:
            raise ValueError(
                f"Invalid atom number in index group {current_name!r} "
                f"at {path}:{line_number}"
            ) from exc

    return GromacsIndex({name: tuple(atoms) for name, atoms in groups.items()})
```

</details>

<a id="definition-96"></a>

## `write_index`

Source lines 96–111. Named callable; inspect its callers before treating it as a stable public API.

```python
def write_index(index: GromacsIndex, index_path: str | Path) -> Path: ...
```

### Purpose and original contract

Write a GROMACS index file with stable 15-atom line wrapping.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| index | GromacsIndex | required |
| index_path | str \| Path | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `' '.join`, `'\n'.join`, `Path`, `index.groups.items`, `len`, `lines.append`, `path.parent.mkdir`, `path.write_text`, `range`, `str`.

Explicit return expressions; different branches may return different objects:

```python
path
```

Calls worth inspecting for I/O, state changes or delegated execution: `path.parent.mkdir`, `path.write_text`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def write_index(index: GromacsIndex, index_path: str | Path) -> Path:
    """Write a GROMACS index file with stable 15-atom line wrapping."""

    path = Path(index_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []

    for group_name, atoms in index.groups.items():
        lines.append(f"[ {group_name} ]")
        atom_text = [str(atom) for atom in atoms]
        for start in range(0, len(atom_text), 15):
            lines.append(" ".join(atom_text[start : start + 15]))
        lines.append("")

    path.write_text("\n".join(lines))
    return path
```

</details>

<a id="definition-114"></a>

## `resolve_center_source_groups`

Source lines 114–146. Named callable; inspect its callers before treating it as a stable public API.

```python
def resolve_center_source_groups(index: GromacsIndex, *, workflow_type: str='polymer', source_groups: tuple[str, ...] | list[str] | None=None) -> tuple[str, ...]: ...
```

### Purpose and original contract

Return source groups for a workflow, filtering to groups present in the index.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| index | GromacsIndex | required |
| workflow_type (keyword-only) | str | 'polymer' |
| source_groups (keyword-only) | tuple[str, ...] \| list[str] \| None | None |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `', '.join`, `ValueError`, `index.has_group`, `present.append`, `sorted`, `tuple`.

Explicit return expressions; different branches may return different objects:

```python
tuple(present)
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError(f'Unknown centering workflow type {workflow_type!r}. Known workflow types: {valid}. Pass source_groups for custom systems.')
ValueError(f'Cannot create [ {DEFAULT_CENTER_GROUP} ] group; none of the requested source groups exist: {missing}. Available groups: {available}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def resolve_center_source_groups(
    index: GromacsIndex,
    *,
    workflow_type: str = "polymer",
    source_groups: tuple[str, ...] | list[str] | None = None,
) -> tuple[str, ...]:
    """Return source groups for a workflow, filtering to groups present in the index."""

    requested = tuple(source_groups) if source_groups is not None else None
    if requested is None:
        try:
            requested = WORKFLOW_CENTER_SOURCES[workflow_type]
        except KeyError as exc:
            valid = ", ".join(sorted(WORKFLOW_CENTER_SOURCES))
            raise ValueError(
                f"Unknown centering workflow type {workflow_type!r}. "
                f"Known workflow types: {valid}. Pass source_groups for custom systems."
            ) from exc

    present: list[str] = []
    for group_name in requested:
        if index.has_group(group_name):
            present.append(group_name)

    if present:
        return tuple(present)

    missing = ", ".join(requested)
    available = ", ".join(index.names)
    raise ValueError(
        f"Cannot create [ {DEFAULT_CENTER_GROUP} ] group; none of the requested "
        f"source groups exist: {missing}. Available groups: {available}"
    )
```

</details>

<a id="definition-149"></a>

## `merged_group_atoms`

Source lines 149–155. Named callable; inspect its callers before treating it as a stable public API.

```python
def merged_group_atoms(index: GromacsIndex, group_names: tuple[str, ...]) -> tuple[int, ...]: ...
```

### Purpose and original contract

Merge one or more index groups into a sorted unique atom list.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| index | GromacsIndex | required |
| group_names | tuple[str, ...] | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `atom_numbers.update`, `index.group`, `set`, `sorted`, `tuple`.

Explicit return expressions; different branches may return different objects:

```python
tuple(sorted(atom_numbers))
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def merged_group_atoms(index: GromacsIndex, group_names: tuple[str, ...]) -> tuple[int, ...]:
    """Merge one or more index groups into a sorted unique atom list."""

    atom_numbers: set[int] = set()
    for group_name in group_names:
        atom_numbers.update(index.group(group_name))
    return tuple(sorted(atom_numbers))
```

</details>

<a id="definition-158"></a>

## `ensure_center_index`

Source lines 158–220. Named callable; inspect its callers before treating it as a stable public API.

```python
def ensure_center_index(source_index: str | Path, output_index: str | Path | None=None, *, workflow_type: str='polymer', source_groups: tuple[str, ...] | list[str] | None=None, center_group: str=DEFAULT_CENTER_GROUP) -> CenterIndexResult: ...
```

### Purpose and original contract

Create or reuse a GROMACS index file containing a dedicated ``center`` group.

Existing ``[ center ]`` groups are reused. Otherwise the group is generated from
the workflow source groups, currently ``PHA`` for polymer-only systems.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| source_index | str \| Path | required |
| output_index | str \| Path \| None | None |
| workflow_type (keyword-only) | str | 'polymer' |
| source_groups (keyword-only) | tuple[str, ...] \| list[str] \| None | None |
| center_group (keyword-only) | str | DEFAULT_CENTER_GROUP |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `CenterIndexResult`, `GromacsIndex`, `Path`, `dict`, `index.has_group`, `merged_group_atoms`, `output.has_group`, `output_path.exists`, `read_index`, `resolve_center_source_groups`, `write_index`.

Explicit return expressions; different branches may return different objects:

```python
CenterIndexResult(index_path=output_path, center_group=center_group, source_groups=(center_group,), created=False, reused_existing_center=True)
CenterIndexResult(index_path=output_path, center_group=center_group, source_groups=(center_group,), created=output_path != source_path, reused_existing_center=True)
CenterIndexResult(index_path=output_path, center_group=center_group, source_groups=resolved_sources, created=True, reused_existing_center=False)
```

Calls worth inspecting for I/O, state changes or delegated execution: `read_index`, `write_index`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def ensure_center_index(
    source_index: str | Path,
    output_index: str | Path | None = None,
    *,
    workflow_type: str = "polymer",
    source_groups: tuple[str, ...] | list[str] | None = None,
    center_group: str = DEFAULT_CENTER_GROUP,
) -> CenterIndexResult:
    """Create or reuse a GROMACS index file containing a dedicated ``center`` group.

    Existing ``[ center ]`` groups are reused. Otherwise the group is generated from
    the workflow source groups, currently ``PHA`` for polymer-only systems.
    """

    source_path = Path(source_index)
    output_path = Path(output_index) if output_index is not None else source_path

    if output_path.exists():
        output = read_index(output_path)
        if output.has_group(center_group):
            return CenterIndexResult(
                index_path=output_path,
                center_group=center_group,
                source_groups=(center_group,),
                created=False,
                reused_existing_center=True,
            )
    else:
        output = read_index(source_path)

    if not output_path.exists() or output_path != source_path:
        index = read_index(source_path)
    else:
        index = output

    if index.has_group(center_group):
        if output_path != source_path:
            write_index(index, output_path)
        return CenterIndexResult(
            index_path=output_path,
            center_group=center_group,
            source_groups=(center_group,),
            created=output_path != source_path,
            reused_existing_center=True,
        )

    resolved_sources = resolve_center_source_groups(
        index,
        workflow_type=workflow_type,
        source_groups=source_groups,
    )
    atoms = merged_group_atoms(index, resolved_sources)
    groups = dict(index.groups)
    groups[center_group] = atoms
    write_index(GromacsIndex(groups), output_path)

    return CenterIndexResult(
        index_path=output_path,
        center_group=center_group,
        source_groups=resolved_sources,
        created=True,
        reused_existing_center=False,
    )
```

</details>
