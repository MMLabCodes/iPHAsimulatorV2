# workflows/design.py

Translate one user design choice into the corresponding RDKit builder call. PolymerDesign holds configuration; supported_polymer_table provides catalogue records. This is a convenient orchestration layer rather than another chemistry engine.

[Current source](../../src/iphasimulator/workflows/design.py)

This page is generated from source syntax. Original docstrings can be incomplete or outdated; module notes above identify known discrepancies. Call/return/error lists describe direct syntax, not all behaviour inside callees. Read the source excerpt for branch order and effects. No scientific execution is implied.

Explicit functions/methods/nested helpers: **3**.

## Module imports

```python
from __future__ import annotations
from dataclasses import dataclass
from rdkit import Chem
from iphasimulator.build import build_custom_pha, build_pha_by_sidechain, build_pha_chain
from iphasimulator.monomers import MONOMERS
from iphasimulator.naming import monomer_to_polymer_code, oligomer_name
```

## Classes and result records

### `PolymerDesign`

A plain-language request for one PHA oligomer.

Use exactly one of ``common_name``, ``side_chain_carbons``, or
``custom_monomer_smiles``.

Decorators: `dataclass(frozen=True)`.

Declared fields/defaults (instance state may also be set by methods):

```python
degree: int
common_name: str | None = None
side_chain_carbons: int | None = None
custom_monomer_smiles: str | None = None
name: str = 'custom_pha'
stereochemistry: str = 'R'
```

Dataclass-generated methods are implicit and are not counted as explicit function definitions.

## Function map

- [`supported_polymer_table` — source line 30](#definition-30)
- [`_selected_design_modes` — source line 49](#definition-49)
- [`design_polymer` — source line 60](#definition-60)

<a id="definition-30"></a>

## `supported_polymer_table`

Source lines 30–46. Named callable; inspect its callers before treating it as a stable public API.

```python
def supported_polymer_table() -> list[dict[str, object]]: ...
```

### Purpose and original contract

Return curated PHA options as notebook-friendly records.

### Inputs

No explicit arguments.

### How to read this implementation

Direct calls (sorted inventory, not execution order): `MONOMERS.values`, `monomer_to_polymer_code`.

Explicit return expressions; different branches may return different objects:

```python
[{'code': monomer.code, 'polymer_code': monomer_to_polymer_code(monomer.code), 'polymer_name': monomer.polymer_name, 'residue_code': monomer.residue_code, 'head_residue_code': monomer.head_residue_code, 'main_residue_code': monomer.main_residue_code, 'tail_residue_code': monomer.tail_residue_code, 'side_chain_carbons': monomer.side_chain_length, 'monomer_smiles': monomer.chiral_smiles} for monomer … [full expression below]
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def supported_polymer_table() -> list[dict[str, object]]:
    """Return curated PHA options as notebook-friendly records."""

    return [
        {
            "code": monomer.code,
            "polymer_code": monomer_to_polymer_code(monomer.code),
            "polymer_name": monomer.polymer_name,
            "residue_code": monomer.residue_code,
            "head_residue_code": monomer.head_residue_code,
            "main_residue_code": monomer.main_residue_code,
            "tail_residue_code": monomer.tail_residue_code,
            "side_chain_carbons": monomer.side_chain_length,
            "monomer_smiles": monomer.chiral_smiles,
        }
        for monomer in MONOMERS.values()
    ]
```

</details>

<a id="definition-49"></a>

## `_selected_design_modes`

Source lines 49–57. Internal helper/protocol method.

```python
def _selected_design_modes(design: PolymerDesign) -> int: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| design | PolymerDesign | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `sum`.

Explicit return expressions; different branches may return different objects:

```python
sum((option is not None for option in (design.common_name, design.side_chain_carbons, design.custom_monomer_smiles)))
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _selected_design_modes(design: PolymerDesign) -> int:
    return sum(
        option is not None
        for option in (
            design.common_name,
            design.side_chain_carbons,
            design.custom_monomer_smiles,
        )
    )
```

</details>

<a id="definition-60"></a>

## `design_polymer`

Source lines 60–90. Named callable; inspect its callers before treating it as a stable public API.

```python
def design_polymer(design: PolymerDesign) -> tuple[str, Chem.Mol]: ...
```

### Purpose and original contract

Build a PHA oligomer from a plain user design request.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| design | PolymerDesign | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `_selected_design_modes`, `build_custom_pha`, `build_pha_by_sidechain`, `build_pha_chain`, `oligomer_name`.

Explicit return expressions; different branches may return different objects:

```python
(name, build_pha_chain(design.common_name, design.degree, design.stereochemistry))
(name, build_pha_by_sidechain(design.side_chain_carbons, design.degree))
(name, build_custom_pha(design.custom_monomer_smiles or '', design.degree, design.name))
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('Choose exactly one design mode: common_name, side_chain_carbons, or custom_monomer_smiles.')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def design_polymer(design: PolymerDesign) -> tuple[str, Chem.Mol]:
    """Build a PHA oligomer from a plain user design request."""

    selected_modes = _selected_design_modes(design)
    if selected_modes != 1:
        raise ValueError(
            "Choose exactly one design mode: common_name, side_chain_carbons, "
            "or custom_monomer_smiles."
        )

    if design.common_name is not None:
        name = oligomer_name(design.common_name, design.degree)
        return name, build_pha_chain(
            design.common_name,
            design.degree,
            design.stereochemistry,
        )

    if design.side_chain_carbons is not None:
        name = f"PHA_C{design.side_chain_carbons}_{design.degree}_R"
        return name, build_pha_by_sidechain(
            design.side_chain_carbons,
            design.degree,
        )

    name = f"{design.name}{design.degree}_R"
    return name, build_custom_pha(
        design.custom_monomer_smiles or "",
        design.degree,
        design.name,
    )
```

</details>
