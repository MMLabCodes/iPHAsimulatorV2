# export.py

RDKit molecule export: prepare a hydrogen-explicit 3D conformer and write SDF/PDB. This route supports the earlier direct-molecule workflow and is distinct from LEaP residue assembly.

[Current source](../../src/iphasimulator/export.py)

This page is generated from source syntax. Original docstrings can be incomplete or outdated; module notes above identify known discrepancies. Call/return/error lists describe direct syntax, not all behaviour inside callees. Read the source excerpt for branch order and effects. No scientific execution is implied.

Explicit functions/methods/nested helpers: **3**.

## Module imports

```python
from __future__ import annotations
from pathlib import Path
from rdkit import Chem
from rdkit.Chem import AllChem
```

## Function map

- [`prepare_molecule_3d` — source line 21](#definition-21)
- [`to_sdf` — source line 40](#definition-40)
- [`to_pdb` — source line 54](#definition-54)

<a id="definition-21"></a>

## `prepare_molecule_3d`

Source lines 21–37. Named callable; inspect its callers before treating it as a stable public API.

```python
def prepare_molecule_3d(mol: Chem.Mol) -> Chem.Mol: ...
```

### Purpose and original contract

Return a copy with explicit hydrogens and an optimized 3D conformer.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| mol | Chem.Mol | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `AllChem.ETKDGv3`, `AllChem.EmbedMolecule`, `AllChem.UFFOptimizeMolecule`, `Chem.AddHs`, `Chem.Mol`, `ValueError`.

Explicit return expressions; different branches may return different objects:

```python
embedded
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('RDKit ETKDG embedding failed')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def prepare_molecule_3d(mol: Chem.Mol) -> Chem.Mol:
    """Return a copy with explicit hydrogens and an optimized 3D conformer."""

    embedded = Chem.AddHs(Chem.Mol(mol))
    params = AllChem.ETKDGv3()
    params.randomSeed = 0xC0FFEE

    status = AllChem.EmbedMolecule(embedded, params)
    if status != 0:
        params.useRandomCoords = True
        params.randomSeed = 0xC0FFEE
        status = AllChem.EmbedMolecule(embedded, params)
    if status != 0:
        raise ValueError("RDKit ETKDG embedding failed")

    AllChem.UFFOptimizeMolecule(embedded, maxIters=200)
    return embedded
```

</details>

<a id="definition-40"></a>

## `to_sdf`

Source lines 40–51. Named callable; inspect its callers before treating it as a stable public API.

```python
def to_sdf(mol: Chem.Mol, path: str | Path) -> None: ...
```

### Purpose and original contract

Embed an RDKit molecule with ETKDG and write it to SDF.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| mol | Chem.Mol | required |
| path | str \| Path | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `Chem.SDWriter`, `Path`, `output_path.parent.mkdir`, `prepare_molecule_3d`, `str`, `writer.close`, `writer.write`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Calls worth inspecting for I/O, state changes or delegated execution: `Chem.SDWriter`, `output_path.parent.mkdir`, `writer.close`, `writer.write`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def to_sdf(mol: Chem.Mol, path: str | Path) -> None:
    """Embed an RDKit molecule with ETKDG and write it to SDF."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    embedded = prepare_molecule_3d(mol)
    writer = Chem.SDWriter(str(output_path))
    try:
        writer.write(embedded)
    finally:
        writer.close()
```

</details>

<a id="definition-54"></a>

## `to_pdb`

Source lines 54–61. Named callable; inspect its callers before treating it as a stable public API.

```python
def to_pdb(mol: Chem.Mol, path: str | Path) -> None: ...
```

### Purpose and original contract

Embed an RDKit molecule with ETKDG and write it to PDB.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| mol | Chem.Mol | required |
| path | str \| Path | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `Chem.MolToPDBFile`, `Path`, `output_path.parent.mkdir`, `prepare_molecule_3d`, `str`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Calls worth inspecting for I/O, state changes or delegated execution: `output_path.parent.mkdir`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def to_pdb(mol: Chem.Mol, path: str | Path) -> None:
    """Embed an RDKit molecule with ETKDG and write it to PDB."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    embedded = prepare_molecule_3d(mol)
    Chem.MolToPDBFile(embedded, str(output_path))
```

</details>
