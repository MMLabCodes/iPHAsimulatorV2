# workflows/validation.py

Define small benchmark targets, build RDKit molecules, describe chemistry and export SDF/PDB. These validation examples belong to the earlier direct-molecule route, not the newer MD-system registry.

[Current source](../../src/iphasimulator/workflows/validation.py)

This page is generated from source syntax. Original docstrings can be incomplete or outdated; module notes above identify known discrepancies. Call/return/error lists describe direct syntax, not all behaviour inside callees. Read the source excerpt for branch order and effects. No scientific execution is implied.

Explicit functions/methods/nested helpers: **4**.

## Module imports

```python
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from rdkit import Chem
from iphasimulator.build import build_pha_chain
from iphasimulator.export import to_pdb, to_sdf
from iphasimulator.naming import oligomer_name
```

## Classes and result records

### `ValidationTarget`

A named PHA oligomer used for quick build validation.

Decorators: `dataclass(frozen=True)`.

Declared fields/defaults (instance state may also be set by methods):

```python
monomer: str
degree: int
stereochemistry: str = 'R'
```

Dataclass-generated methods are implicit and are not counted as explicit function definitions.

## Function map

- [`ValidationTarget.name` — source line 24](#definition-24)
- [`build_validation_molecules` — source line 41](#definition-41)
- [`describe_molecules` — source line 56](#definition-56)
- [`export_molecules` — source line 76](#definition-76)

<a id="definition-24"></a>

## `ValidationTarget.name`

Source lines 24–25. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `property`.

```python
def name(self) -> str: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `oligomer_name`.

Explicit return expressions; different branches may return different objects:

```python
oligomer_name(self.monomer, self.degree)
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def name(self) -> str:
    return oligomer_name(self.monomer, self.degree)
```

</details>

<a id="definition-41"></a>

## `build_validation_molecules`

Source lines 41–53. Named callable; inspect its callers before treating it as a stable public API.

```python
def build_validation_molecules(targets: tuple[ValidationTarget, ...]=DEFAULT_VALIDATION_TARGETS) -> dict[str, Chem.Mol]: ...
```

### Purpose and original contract

Build the requested validation PHA oligomers.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| targets | tuple[ValidationTarget, ...] | DEFAULT_VALIDATION_TARGETS |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `build_pha_chain`.

Explicit return expressions; different branches may return different objects:

```python
{target.name: build_pha_chain(target.monomer, target.degree, target.stereochemistry) for target in targets}
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def build_validation_molecules(
    targets: tuple[ValidationTarget, ...] = DEFAULT_VALIDATION_TARGETS,
) -> dict[str, Chem.Mol]:
    """Build the requested validation PHA oligomers."""

    return {
        target.name: build_pha_chain(
            target.monomer,
            target.degree,
            target.stereochemistry,
        )
        for target in targets
    }
```

</details>

<a id="definition-56"></a>

## `describe_molecules`

Source lines 56–73. Named callable; inspect its callers before treating it as a stable public API.

```python
def describe_molecules(molecules: dict[str, Chem.Mol]) -> list[dict[str, object]]: ...
```

### Purpose and original contract

Return SMILES and chiral-centre summaries for built molecules.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| molecules | dict[str, Chem.Mol] | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `Chem.AssignStereochemistry`, `Chem.FindMolChiralCenters`, `Chem.MolToSmiles`, `mol.GetNumAtoms`, `molecules.items`, `rows.append`.

Explicit return expressions; different branches may return different objects:

```python
rows
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def describe_molecules(molecules: dict[str, Chem.Mol]) -> list[dict[str, object]]:
    """Return SMILES and chiral-centre summaries for built molecules."""

    rows: list[dict[str, object]] = []
    for name, mol in molecules.items():
        Chem.AssignStereochemistry(mol, cleanIt=True, force=True)
        rows.append(
            {
                "name": name,
                "atoms": mol.GetNumAtoms(),
                "smiles": Chem.MolToSmiles(mol, isomericSmiles=True),
                "chiral_centres": Chem.FindMolChiralCenters(
                    mol,
                    includeUnassigned=True,
                ),
            }
        )
    return rows
```

</details>

<a id="definition-76"></a>

## `export_molecules`

Source lines 76–92. Named callable; inspect its callers before treating it as a stable public API.

```python
def export_molecules(molecules: dict[str, Chem.Mol], output_dir: str | Path) -> list[Path]: ...
```

### Purpose and original contract

Export molecules to SDF and PDB files.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| molecules | dict[str, Chem.Mol] | required |
| output_dir | str \| Path | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `Path`, `molecules.items`, `output_path.mkdir`, `to_pdb`, `to_sdf`, `written.extend`.

Explicit return expressions; different branches may return different objects:

```python
written
```

Calls worth inspecting for I/O, state changes or delegated execution: `output_path.mkdir`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def export_molecules(
    molecules: dict[str, Chem.Mol],
    output_dir: str | Path,
) -> list[Path]:
    """Export molecules to SDF and PDB files."""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    for name, mol in molecules.items():
        sdf_path = output_path / f"{name}.sdf"
        pdb_path = output_path / f"{name}.pdb"
        to_sdf(mol, sdf_path)
        to_pdb(mol, pdb_path)
        written.extend([sdf_path, pdb_path])
    return written
```

</details>
