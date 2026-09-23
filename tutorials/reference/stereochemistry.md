# stereochemistry.py

Validate supported stereochemistry settings and assigned chiral centres on RDKit molecules. These checks support chemical construction and are different from inspecting the geometry of a simulated trajectory.

[Current source](../../src/iphasimulator/stereochemistry.py)

This page is generated from source syntax. Original docstrings can be incomplete or outdated; module notes above identify known discrepancies. Call/return/error lists describe direct syntax, not all behaviour inside callees. Read the source excerpt for branch order and effects. No scientific execution is implied.

Explicit functions/methods/nested helpers: **3**.

## Module imports

```python
from __future__ import annotations
from rdkit import Chem
```

## Function map

- [`validate_stereochemistry_option` — source line 14](#definition-14)
- [`validate_chiral_centres` — source line 26](#definition-26)
- [`validate_r_chiral_centres` — source line 51](#definition-51)

<a id="definition-14"></a>

## `validate_stereochemistry_option`

Source lines 14–23. Named callable; inspect its callers before treating it as a stable public API.

```python
def validate_stereochemistry_option(stereochemistry: str) -> str: ...
```

### Purpose and original contract

Validate and normalize the requested stereochemistry.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| stereochemistry | str | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `isinstance`, `stereochemistry.upper`.

Explicit return expressions; different branches may return different objects:

```python
normalized
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('Stereochemistry must be R or S')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def validate_stereochemistry_option(stereochemistry: str) -> str:
    """Validate and normalize the requested stereochemistry."""

    if not isinstance(stereochemistry, str):
        raise ValueError("Stereochemistry must be R or S")

    normalized = stereochemistry.upper()
    if normalized not in {"R", "S"}:
        raise ValueError("Stereochemistry must be R or S")
    return normalized
```

</details>

<a id="definition-26"></a>

## `validate_chiral_centres`

Source lines 26–48. Named callable; inspect its callers before treating it as a stable public API.

```python
def validate_chiral_centres(mol: Chem.Mol, expected_count: int, stereochemistry: str) -> None: ...
```

### Purpose and original contract

Ensure every repeat unit has one assigned chiral centre.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| mol | Chem.Mol | required |
| expected_count | int | required |
| stereochemistry | str | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `', '.join`, `Chem.AssignStereochemistry`, `Chem.FindMolChiralCenters`, `ValueError`, `len`, `validate_stereochemistry_option`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError(f'Expected {expected_count} chiral centres, found {len(centres)}')
ValueError(f'Expected all chiral centres to be {expected_label}; found {details}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def validate_chiral_centres(
    mol: Chem.Mol, expected_count: int, stereochemistry: str
) -> None:
    """Ensure every repeat unit has one assigned chiral centre."""

    expected_label = validate_stereochemistry_option(stereochemistry)

    Chem.AssignStereochemistry(mol, cleanIt=True, force=True)
    centres = Chem.FindMolChiralCenters(mol, includeUnassigned=True)

    if len(centres) != expected_count:
        raise ValueError(
            f"Expected {expected_count} chiral centres, found {len(centres)}"
        )

    mismatched = [
        (atom_idx, label) for atom_idx, label in centres if label != expected_label
    ]
    if mismatched:
        details = ", ".join(f"atom {atom_idx}: {label}" for atom_idx, label in mismatched)
        raise ValueError(
            f"Expected all chiral centres to be {expected_label}; found {details}"
        )
```

</details>

<a id="definition-51"></a>

## `validate_r_chiral_centres`

Source lines 51–54. Named callable; inspect its callers before treating it as a stable public API.

```python
def validate_r_chiral_centres(mol: Chem.Mol, expected_count: int) -> None: ...
```

### Purpose and original contract

Ensure every repeat unit has one assigned R chiral centre.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| mol | Chem.Mol | required |
| expected_count | int | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `validate_chiral_centres`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def validate_r_chiral_centres(mol: Chem.Mol, expected_count: int) -> None:
    """Ensure every repeat unit has one assigned R chiral centre."""

    validate_chiral_centres(mol, expected_count=expected_count, stereochemistry="R")
```

</details>
