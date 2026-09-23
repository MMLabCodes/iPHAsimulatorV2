# naming.py

Canonical naming and validation for chemistry/polymer identifiers and residue variants. Other parts of the current project still construct names independently, so this module is not yet the only naming implementation.

[Current source](../../src/iphasimulator/naming.py)

This page is generated from source syntax. Original docstrings can be incomplete or outdated; module notes above identify known discrepancies. Call/return/error lists describe direct syntax, not all behaviour inside callees. Read the source excerpt for branch order and effects. No scientific execution is implied.

Explicit functions/methods/nested helpers: **13**.

## Module imports

```python
from __future__ import annotations
from typing import Literal
```

## Function map

- [`_require_text` — source line 53](#definition-53)
- [`_require_positive_int` — source line 59](#definition-59)
- [`canonical_monomer_code` — source line 67](#definition-67)
- [`validate_monomer_code` — source line 78](#definition-78)
- [`monomer_to_polymer_code` — source line 89](#definition-89)
- [`validate_polymer_code` — source line 95](#definition-95)
- [`oligomer_name` — source line 106](#definition-106)
- [`validate_oligomer_name` — source line 113](#definition-113)
- [`multi_chain_system_name` — source line 135](#definition-135)
- [`validate_system_name` — source line 156](#definition-156)
- [`residue_variant_name` — source line 177](#definition-177)
- [`residue_variant_names` — source line 188](#definition-188)
- [`validate_pha_name` — source line 195](#definition-195)

<a id="definition-53"></a>

## `_require_text`

Source lines 53–56. Internal helper/protocol method.

```python
def _require_text(value: str, label: str) -> str: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| value | str | required |
| label | str | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `isinstance`, `value.strip`.

Explicit return expressions; different branches may return different objects:

```python
value.strip()
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError(f'{label} must be a non-empty string')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _require_text(value: str, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    return value.strip()
```

</details>

<a id="definition-59"></a>

## `_require_positive_int`

Source lines 59–64. Internal helper/protocol method.

```python
def _require_positive_int(value: int, label: str) -> int: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| value | int | required |
| label | str | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `isinstance`.

Explicit return expressions; different branches may return different objects:

```python
value
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError(f'{label} must be an integer')
ValueError(f'{label} must be at least 1')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _require_positive_int(value: int, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"{label} must be an integer")
    if value < 1:
        raise ValueError(f"{label} must be at least 1")
    return value
```

</details>

<a id="definition-67"></a>

## `canonical_monomer_code`

Source lines 67–75. Named callable; inspect its callers before treating it as a stable public API.

```python
def canonical_monomer_code(code: str) -> str: ...
```

### Purpose and original contract

Return the canonical monomer/residue code, accepting legacy aliases.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| code | str | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `', '.join`, `ValueError`, `_MONOMER_LOOKUP.get`, `_require_text`, `sorted`, `text.upper`.

Explicit return expressions; different branches may return different objects:

```python
canonical
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError(f'Unknown monomer code {code!r}. Supported monomers: {supported}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def canonical_monomer_code(code: str) -> str:
    """Return the canonical monomer/residue code, accepting legacy aliases."""

    text = _require_text(code, "monomer code")
    canonical = _MONOMER_LOOKUP.get(text.upper())
    if canonical is None:
        supported = ", ".join(sorted(MONOMER_TO_POLYMER))
        raise ValueError(f"Unknown monomer code {code!r}. Supported monomers: {supported}")
    return canonical
```

</details>

<a id="definition-78"></a>

## `validate_monomer_code`

Source lines 78–86. Named callable; inspect its callers before treating it as a stable public API.

```python
def validate_monomer_code(code: str) -> str: ...
```

### Purpose and original contract

Validate and return a canonical monomer/residue code such as ``3HB``.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| code | str | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `', '.join`, `MONOMER_TO_POLYMER.get`, `ValueError`, `_require_text`, `sorted`.

Explicit return expressions; different branches may return different objects:

```python
text
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError(f'Invalid monomer code {code!r}. Expected one of: {supported}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def validate_monomer_code(code: str) -> str:
    """Validate and return a canonical monomer/residue code such as ``3HB``."""

    text = _require_text(code, "monomer code")
    canonical = MONOMER_TO_POLYMER.get(text)
    if canonical is None:
        supported = ", ".join(sorted(MONOMER_TO_POLYMER))
        raise ValueError(f"Invalid monomer code {code!r}. Expected one of: {supported}")
    return text
```

</details>

<a id="definition-89"></a>

## `monomer_to_polymer_code`

Source lines 89–92. Named callable; inspect its callers before treating it as a stable public API.

```python
def monomer_to_polymer_code(monomer_code: str) -> str: ...
```

### Purpose and original contract

Convert a monomer/residue code such as ``3HB`` to ``P3HB``.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| monomer_code | str | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `canonical_monomer_code`.

Explicit return expressions; different branches may return different objects:

```python
MONOMER_TO_POLYMER[canonical_monomer_code(monomer_code)]
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def monomer_to_polymer_code(monomer_code: str) -> str:
    """Convert a monomer/residue code such as ``3HB`` to ``P3HB``."""

    return MONOMER_TO_POLYMER[canonical_monomer_code(monomer_code)]
```

</details>

<a id="definition-95"></a>

## `validate_polymer_code`

Source lines 95–103. Named callable; inspect its callers before treating it as a stable public API.

```python
def validate_polymer_code(code: str) -> str: ...
```

### Purpose and original contract

Validate and return a polymer code such as ``P3HB``.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| code | str | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `', '.join`, `ValueError`, `_POLYMER_LOOKUP.get`, `_require_text`, `sorted`, `text.upper`.

Explicit return expressions; different branches may return different objects:

```python
canonical
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError(f'Invalid polymer code {code!r}. Expected one of: {supported}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def validate_polymer_code(code: str) -> str:
    """Validate and return a polymer code such as ``P3HB``."""

    text = _require_text(code, "polymer code")
    canonical = _POLYMER_LOOKUP.get(text.upper())
    if canonical is None:
        supported = ", ".join(sorted(POLYMER_TO_MONOMER))
        raise ValueError(f"Invalid polymer code {code!r}. Expected one of: {supported}")
    return canonical
```

</details>

<a id="definition-106"></a>

## `oligomer_name`

Source lines 106–110. Named callable; inspect its callers before treating it as a stable public API.

```python
def oligomer_name(monomer_code: str, repeat_units: int) -> str: ...
```

### Purpose and original contract

Return a single-chain oligomer name such as ``P3HB_4``.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| monomer_code | str | required |
| repeat_units | int | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `_require_positive_int`, `monomer_to_polymer_code`.

Explicit return expressions; different branches may return different objects:

```python
f'{monomer_to_polymer_code(monomer_code)}_{repeat_units}'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def oligomer_name(monomer_code: str, repeat_units: int) -> str:
    """Return a single-chain oligomer name such as ``P3HB_4``."""

    repeat_units = _require_positive_int(repeat_units, "repeat units")
    return f"{monomer_to_polymer_code(monomer_code)}_{repeat_units}"
```

</details>

<a id="definition-113"></a>

## `validate_oligomer_name`

Source lines 113–132. Named callable; inspect its callers before treating it as a stable public API.

```python
def validate_oligomer_name(name: str) -> str: ...
```

### Purpose and original contract

Validate and return a single-chain oligomer name such as ``P3HO_8``.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| name | str | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `_require_positive_int`, `_require_text`, `int`, `text.rsplit`, `validate_polymer_code`.

Explicit return expressions; different branches may return different objects:

```python
f'{polymer_code}_{repeat_units}'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError(f'Invalid oligomer name {name!r}. Expected format P3HB_4')
ValueError(f'Invalid oligomer name {name!r}. Repeat units must be an integer')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def validate_oligomer_name(name: str) -> str:
    """Validate and return a single-chain oligomer name such as ``P3HO_8``."""

    text = _require_text(name, "oligomer name")
    try:
        polymer_code, repeat_text = text.rsplit("_", 1)
    except ValueError as exc:
        raise ValueError(
            f"Invalid oligomer name {name!r}. Expected format P3HB_4"
        ) from exc

    polymer_code = validate_polymer_code(polymer_code)
    try:
        repeat_units = int(repeat_text)
    except ValueError as exc:
        raise ValueError(
            f"Invalid oligomer name {name!r}. Repeat units must be an integer"
        ) from exc
    repeat_units = _require_positive_int(repeat_units, "repeat units")
    return f"{polymer_code}_{repeat_units}"
```

</details>

<a id="definition-135"></a>

## `multi_chain_system_name`

Source lines 135–153. Named callable; inspect its callers before treating it as a stable public API.

```python
def multi_chain_system_name(chain_count: int, monomer_code: str | None=None, repeat_units: int | None=None, *, oligomer: str | None=None) -> str: ...
```

### Purpose and original contract

Return a multi-chain system name such as ``25_P3HB_3``.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| chain_count | int | required |
| monomer_code | str \| None | None |
| repeat_units | int \| None | None |
| oligomer (keyword-only) | str \| None | None |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `_require_positive_int`, `oligomer_name`, `validate_oligomer_name`.

Explicit return expressions; different branches may return different objects:

```python
f'{chain_count}_{oligomer}'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('monomer_code and repeat_units are required when oligomer is not set')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def multi_chain_system_name(
    chain_count: int,
    monomer_code: str | None = None,
    repeat_units: int | None = None,
    *,
    oligomer: str | None = None,
) -> str:
    """Return a multi-chain system name such as ``25_P3HB_3``."""

    chain_count = _require_positive_int(chain_count, "chain count")
    if oligomer is None:
        if monomer_code is None or repeat_units is None:
            raise ValueError(
                "monomer_code and repeat_units are required when oligomer is not set"
            )
        oligomer = oligomer_name(monomer_code, repeat_units)
    else:
        oligomer = validate_oligomer_name(oligomer)
    return f"{chain_count}_{oligomer}"
```

</details>

<a id="definition-156"></a>

## `validate_system_name`

Source lines 156–174. Named callable; inspect its callers before treating it as a stable public API.

```python
def validate_system_name(name: str) -> str: ...
```

### Purpose and original contract

Validate and return a multi-chain system name such as ``25_P3HB_3``.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| name | str | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `_require_positive_int`, `_require_text`, `int`, `text.split`, `validate_oligomer_name`.

Explicit return expressions; different branches may return different objects:

```python
f'{chain_count}_{validate_oligomer_name(oligomer)}'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError(f'Invalid system name {name!r}. Expected format 25_P3HB_3')
ValueError(f'Invalid system name {name!r}. Chain count must be an integer')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def validate_system_name(name: str) -> str:
    """Validate and return a multi-chain system name such as ``25_P3HB_3``."""

    text = _require_text(name, "system name")
    try:
        chain_text, oligomer = text.split("_", 1)
    except ValueError as exc:
        raise ValueError(
            f"Invalid system name {name!r}. Expected format 25_P3HB_3"
        ) from exc

    try:
        chain_count = int(chain_text)
    except ValueError as exc:
        raise ValueError(
            f"Invalid system name {name!r}. Chain count must be an integer"
        ) from exc
    chain_count = _require_positive_int(chain_count, "chain count")
    return f"{chain_count}_{validate_oligomer_name(oligomer)}"
```

</details>

<a id="definition-177"></a>

## `residue_variant_name`

Source lines 177–185. Named callable; inspect its callers before treating it as a stable public API.

```python
def residue_variant_name(monomer_code: str, role: ResidueRole) -> str: ...
```

### Purpose and original contract

Return a head/main/tail residue name such as ``3HB_H``.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| monomer_code | str | required |
| role | ResidueRole | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `_ROLE_LOOKUP.get`, `_require_text`, `canonical_monomer_code`, `role_text.upper`.

Explicit return expressions; different branches may return different objects:

```python
f'{monomer_code}_{suffix}'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('residue role must be H, M, T, head, main, or tail')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def residue_variant_name(monomer_code: str, role: ResidueRole) -> str:
    """Return a head/main/tail residue name such as ``3HB_H``."""

    monomer_code = canonical_monomer_code(monomer_code)
    role_text = _require_text(role, "residue role")
    suffix = _ROLE_LOOKUP.get(role_text.upper())
    if suffix is None:
        raise ValueError("residue role must be H, M, T, head, main, or tail")
    return f"{monomer_code}_{suffix}"
```

</details>

<a id="definition-188"></a>

## `residue_variant_names`

Source lines 188–192. Named callable; inspect its callers before treating it as a stable public API.

```python
def residue_variant_names(monomer_code: str) -> tuple[str, str, str]: ...
```

### Purpose and original contract

Return head, main, and tail residue names for one monomer code.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| monomer_code | str | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `canonical_monomer_code`, `tuple`.

Explicit return expressions; different branches may return different objects:

```python
tuple((f'{monomer_code}_{suffix}' for suffix in RESIDUE_ROLE_SUFFIXES))
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def residue_variant_names(monomer_code: str) -> tuple[str, str, str]:
    """Return head, main, and tail residue names for one monomer code."""

    monomer_code = canonical_monomer_code(monomer_code)
    return tuple(f"{monomer_code}_{suffix}" for suffix in RESIDUE_ROLE_SUFFIXES)
```

</details>

<a id="definition-195"></a>

## `validate_pha_name`

Source lines 195–211. Named callable; inspect its callers before treating it as a stable public API.

```python
def validate_pha_name(name: str) -> str: ...
```

### Purpose and original contract

Validate any canonical PHA monomer, polymer, oligomer, or system name.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| name | str | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `validator`.

Explicit return expressions; different branches may return different objects:

```python
validator(name)
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError(f'Invalid PHA name {name!r}. Expected 3HB, P3HB, P3HB_4, or 25_P3HB_3')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def validate_pha_name(name: str) -> str:
    """Validate any canonical PHA monomer, polymer, oligomer, or system name."""

    validators = (
        validate_system_name,
        validate_oligomer_name,
        validate_polymer_code,
        validate_monomer_code,
    )
    for validator in validators:
        try:
            return validator(name)
        except ValueError:
            continue
    raise ValueError(
        f"Invalid PHA name {name!r}. Expected 3HB, P3HB, P3HB_4, or 25_P3HB_3"
    )
```

</details>
