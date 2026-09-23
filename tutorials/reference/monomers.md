# monomers.py

Curated in-code monomer definitions for the RDKit builder, with canonical names and residue-name metadata. This catalogue and the persistent residue_codes.csv database are separate representations; registration in either does not prove PREPIN readiness.

[Current source](../../src/iphasimulator/monomers.py)

This page is generated from source syntax. Original docstrings can be incomplete or outdated; module notes above identify known discrepancies. Call/return/error lists describe direct syntax, not all behaviour inside callees. Read the source excerpt for branch order and effects. No scientific execution is implied.

Explicit functions/methods/nested helpers: **5**.

## Module imports

```python
from __future__ import annotations
from dataclasses import dataclass
from iphasimulator.naming import canonical_monomer_code, residue_variant_names
```

## Classes and result records

### `Monomer`

A 3-hydroxyalkanoate monomer entry.

``chiral_smiles`` stores the free 3-hydroxy acid with explicit R chirality.
``side_chain_length`` is the number of carbons in the alkyl side chain.

Decorators: `dataclass(frozen=True)`.

Declared fields/defaults (instance state may also be set by methods):

```python
code: str
polymer_name: str
residue_code: str
chiral_smiles: str
side_chain_length: int
expected_stereochemistry: str = 'R'
```

Dataclass-generated methods are implicit and are not counted as explicit function definitions.

## Function map

- [`Monomer.side_chain` — source line 35](#definition-35)
- [`Monomer.head_residue_code` — source line 41](#definition-41)
- [`Monomer.main_residue_code` — source line 47](#definition-47)
- [`Monomer.tail_residue_code` — source line 53](#definition-53)
- [`get_monomer` — source line 119](#definition-119)

<a id="definition-35"></a>

## `Monomer.side_chain`

Source lines 35–38. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `property`.

```python
def side_chain(self) -> str: ...
```

### Purpose and original contract

Return the straight saturated alkyl side-chain SMILES fragment.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |

### How to read this implementation

No direct function calls were found in this definition's own body.

Explicit return expressions; different branches may return different objects:

```python
'C' * self.side_chain_length
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def side_chain(self) -> str:
    """Return the straight saturated alkyl side-chain SMILES fragment."""

    return "C" * self.side_chain_length
```

</details>

<a id="definition-41"></a>

## `Monomer.head_residue_code`

Source lines 41–44. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `property`.

```python
def head_residue_code(self) -> str: ...
```

### Purpose and original contract

Return the head residue variant code for this monomer.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `residue_variant_names`.

Explicit return expressions; different branches may return different objects:

```python
residue_variant_names(self.code)[0]
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def head_residue_code(self) -> str:
    """Return the head residue variant code for this monomer."""

    return residue_variant_names(self.code)[0]
```

</details>

<a id="definition-47"></a>

## `Monomer.main_residue_code`

Source lines 47–50. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `property`.

```python
def main_residue_code(self) -> str: ...
```

### Purpose and original contract

Return the main-chain residue variant code for this monomer.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `residue_variant_names`.

Explicit return expressions; different branches may return different objects:

```python
residue_variant_names(self.code)[1]
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def main_residue_code(self) -> str:
    """Return the main-chain residue variant code for this monomer."""

    return residue_variant_names(self.code)[1]
```

</details>

<a id="definition-53"></a>

## `Monomer.tail_residue_code`

Source lines 53–56. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `property`.

```python
def tail_residue_code(self) -> str: ...
```

### Purpose and original contract

Return the tail residue variant code for this monomer.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `residue_variant_names`.

Explicit return expressions; different branches may return different objects:

```python
residue_variant_names(self.code)[2]
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def tail_residue_code(self) -> str:
    """Return the tail residue variant code for this monomer."""

    return residue_variant_names(self.code)[2]
```

</details>

<a id="definition-119"></a>

## `get_monomer`

Source lines 119–134. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_monomer(code: str) -> Monomer: ...
```

### Purpose and original contract

Return a registered monomer by case-insensitive code.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| code | str | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `', '.join`, `ValueError`, `canonical_monomer_code`, `isinstance`, `sorted`.

Explicit return expressions; different branches may return different objects:

```python
MONOMERS[key]
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError(f'Unknown monomer {code!r}. Supported monomers: {supported}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_monomer(code: str) -> Monomer:
    """Return a registered monomer by case-insensitive code."""

    if not isinstance(code, str):
        supported = ", ".join(sorted(MONOMERS))
        raise ValueError(f"Unknown monomer {code!r}. Supported monomers: {supported}")

    try:
        key = canonical_monomer_code(code)
    except ValueError as exc:
        supported = ", ".join(sorted(MONOMERS))
        raise ValueError(
            f"Unknown monomer {code!r}. Supported monomers: {supported}"
        ) from exc

    return MONOMERS[key]
```

</details>
