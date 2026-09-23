# build.py

Direct RDKit construction route: validate the request, derive repeat-unit chemistry, build the molecule, and check stereochemistry/connectivity. These molecules feed the older SDF-based parameterisation route; they are not the reusable PREPIN database objects.

[Current source](../../src/iphasimulator/build.py)

This page is generated from source syntax. Original docstrings can be incomplete or outdated; module notes above identify known discrepancies. Call/return/error lists describe direct syntax, not all behaviour inside callees. Read the source excerpt for branch order and effects. No scientific execution is implied.

Explicit functions/methods/nested helpers: **19**.

## Module imports

```python
from __future__ import annotations
from rdkit import Chem
from iphasimulator.monomers import Monomer, get_monomer
from iphasimulator.stereochemistry import validate_stereochemistry_option
```

## Function map

- [`_validate_repeat_units` — source line 23](#definition-23)
- [`_validate_side_chain_carbons` — source line 30](#definition-30)
- [`_build_oligomer_smiles` — source line 37](#definition-37)
- [`_sanitize_molecule` — source line 44](#definition-44)
- [`_count_carbons` — source line 58](#definition-58)
- [`_validate_ester_bond_count` — source line 62](#definition-62)
- [`_has_hydroxy_neighbor` — source line 71](#definition-71)
- [`_is_carboxyl_carbon` — source line 79](#definition-79)
- [`_is_backbone_methylene` — source line 96](#definition-96)
- [`_pha_chiral_atom_indices` — source line 106](#definition-106)
- [`_validate_pha_stereochemistry` — source line 122](#definition-122)
- [`_validate_side_chain_carbon_count` — source line 148](#definition-148)
- [`validate_pha_chain` — source line 162](#definition-162)
- [`_build_validated_pha_from_side_chain` — source line 174](#definition-174)
- [`_validate_custom_name` — source line 202](#definition-202)
- [`_side_chain_from_monomer_smiles` — source line 208](#definition-208)
- [`build_pha_chain` — source line 257](#definition-257)
- [`build_pha_by_sidechain` — source line 278](#definition-278)
- [`build_custom_pha` — source line 296](#definition-296)

<a id="definition-23"></a>

## `_validate_repeat_units`

Source lines 23–27. Internal helper/protocol method.

```python
def _validate_repeat_units(n: int) -> None: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| n | int | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `isinstance`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('Number of repeat units must be an integer')
ValueError('Number of repeat units must be at least 1')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _validate_repeat_units(n: int) -> None:
    if not isinstance(n, int) or isinstance(n, bool):
        raise ValueError("Number of repeat units must be an integer")
    if n < 1:
        raise ValueError("Number of repeat units must be at least 1")
```

</details>

<a id="definition-30"></a>

## `_validate_side_chain_carbons`

Source lines 30–34. Internal helper/protocol method.

```python
def _validate_side_chain_carbons(side_chain_carbons: int) -> None: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| side_chain_carbons | int | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `isinstance`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('Side-chain carbons must be an integer')
ValueError('Side-chain carbons must be at least 1')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _validate_side_chain_carbons(side_chain_carbons: int) -> None:
    if not isinstance(side_chain_carbons, int) or isinstance(side_chain_carbons, bool):
        raise ValueError("Side-chain carbons must be an integer")
    if side_chain_carbons < 1:
        raise ValueError("Side-chain carbons must be at least 1")
```

</details>

<a id="definition-37"></a>

## `_build_oligomer_smiles`

Source lines 37–41. Internal helper/protocol method.

```python
def _build_oligomer_smiles(side_chain: str, n: int, chiral_tag: str) -> str: ...
```

### Purpose and original contract

Build HO-terminated/carboxy-terminated PHA oligomer SMILES.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| side_chain | str | required |
| n | int | required |
| chiral_tag | str | required |

### How to read this implementation

No direct function calls were found in this definition's own body.

Explicit return expressions; different branches may return different objects:

```python
repeat * n + 'O'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _build_oligomer_smiles(side_chain: str, n: int, chiral_tag: str) -> str:
    """Build HO-terminated/carboxy-terminated PHA oligomer SMILES."""

    repeat = f"O[C{chiral_tag}H]({side_chain})CC(=O)"
    return (repeat * n) + "O"
```

</details>

<a id="definition-44"></a>

## `_sanitize_molecule`

Source lines 44–55. Internal helper/protocol method.

```python
def _sanitize_molecule(mol: Chem.Mol | None, name: str, n: int) -> Chem.Mol: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| mol | Chem.Mol \| None | required |
| name | str | required |
| n | int | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `Chem.SanitizeMol`, `ValueError`.

Explicit return expressions; different branches may return different objects:

```python
mol
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError(f'Failed to build RDKit molecule for {name} n={n}')
ValueError(f'RDKit sanitisation failed for {name} n={n}: {exc}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _sanitize_molecule(mol: Chem.Mol | None, name: str, n: int) -> Chem.Mol:
    if mol is None:
        raise ValueError(f"Failed to build RDKit molecule for {name} n={n}")

    try:
        Chem.SanitizeMol(mol)
    except Chem.AtomValenceException as exc:
        raise ValueError(f"RDKit sanitisation failed for {name} n={n}: {exc}") from exc
    except Chem.KekulizeException as exc:
        raise ValueError(f"RDKit sanitisation failed for {name} n={n}: {exc}") from exc

    return mol
```

</details>

<a id="definition-58"></a>

## `_count_carbons`

Source lines 58–59. Internal helper/protocol method.

```python
def _count_carbons(mol: Chem.Mol) -> int: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| mol | Chem.Mol | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `atom.GetAtomicNum`, `mol.GetAtoms`, `sum`.

Explicit return expressions; different branches may return different objects:

```python
sum((1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6))
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _count_carbons(mol: Chem.Mol) -> int:
    return sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)
```

</details>

<a id="definition-62"></a>

## `_validate_ester_bond_count`

Source lines 62–68. Internal helper/protocol method.

```python
def _validate_ester_bond_count(mol: Chem.Mol, n: int) -> None: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| mol | Chem.Mol | required |
| n | int | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `len`, `mol.GetSubstructMatches`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError(f'Expected {expected_count} ester bonds, found {ester_count}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _validate_ester_bond_count(mol: Chem.Mol, n: int) -> None:
    ester_count = len(mol.GetSubstructMatches(ESTER_BOND))
    expected_count = n - 1
    if ester_count != expected_count:
        raise ValueError(
            f"Expected {expected_count} ester bonds, found {ester_count}"
        )
```

</details>

<a id="definition-71"></a>

## `_has_hydroxy_neighbor`

Source lines 71–76. Internal helper/protocol method.

```python
def _has_hydroxy_neighbor(atom: Chem.Atom) -> bool: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| atom | Chem.Atom | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `atom.GetIdx`, `atom.GetNeighbors`, `atom.GetOwningMol`, `atom.GetOwningMol().GetBondBetweenAtoms`, `bond.GetBondType`, `neighbor.GetAtomicNum`, `neighbor.GetIdx`.

Explicit return expressions; different branches may return different objects:

```python
True
False
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _has_hydroxy_neighbor(atom: Chem.Atom) -> bool:
    for neighbor in atom.GetNeighbors():
        bond = atom.GetOwningMol().GetBondBetweenAtoms(atom.GetIdx(), neighbor.GetIdx())
        if neighbor.GetAtomicNum() == 8 and bond.GetBondType() == Chem.BondType.SINGLE:
            return True
    return False
```

</details>

<a id="definition-79"></a>

## `_is_carboxyl_carbon`

Source lines 79–93. Internal helper/protocol method.

```python
def _is_carboxyl_carbon(atom: Chem.Atom) -> bool: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| atom | Chem.Atom | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `atom.GetAtomicNum`, `atom.GetIdx`, `atom.GetNeighbors`, `atom.GetOwningMol`, `atom.GetOwningMol().GetBondBetweenAtoms`, `bond.GetBondType`, `neighbor.GetAtomicNum`, `neighbor.GetIdx`.

Explicit return expressions; different branches may return different objects:

```python
False
has_double_o and has_single_o
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _is_carboxyl_carbon(atom: Chem.Atom) -> bool:
    if atom.GetAtomicNum() != 6:
        return False

    has_double_o = False
    has_single_o = False
    for neighbor in atom.GetNeighbors():
        bond = atom.GetOwningMol().GetBondBetweenAtoms(atom.GetIdx(), neighbor.GetIdx())
        if neighbor.GetAtomicNum() != 8:
            continue
        if bond.GetBondType() == Chem.BondType.DOUBLE:
            has_double_o = True
        elif bond.GetBondType() == Chem.BondType.SINGLE:
            has_single_o = True
    return has_double_o and has_single_o
```

</details>

<a id="definition-96"></a>

## `_is_backbone_methylene`

Source lines 96–103. Internal helper/protocol method.

```python
def _is_backbone_methylene(atom: Chem.Atom, chiral_idx: int) -> bool: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| atom | Chem.Atom | required |
| chiral_idx | int | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `_is_carboxyl_carbon`, `atom.GetAtomicNum`, `atom.GetNeighbors`, `neighbor.GetIdx`.

Explicit return expressions; different branches may return different objects:

```python
False
True
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _is_backbone_methylene(atom: Chem.Atom, chiral_idx: int) -> bool:
    if atom.GetAtomicNum() != 6:
        return False

    for neighbor in atom.GetNeighbors():
        if neighbor.GetIdx() != chiral_idx and _is_carboxyl_carbon(neighbor):
            return True
    return False
```

</details>

<a id="definition-106"></a>

## `_pha_chiral_atom_indices`

Source lines 106–119. Internal helper/protocol method.

```python
def _pha_chiral_atom_indices(mol: Chem.Mol) -> list[int]: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| mol | Chem.Mol | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `_has_hydroxy_neighbor`, `_is_backbone_methylene`, `atom.GetAtomicNum`, `atom.GetIdx`, `atom.GetNeighbors`, `indices.append`, `len`, `mol.GetAtoms`.

Explicit return expressions; different branches may return different objects:

```python
indices
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _pha_chiral_atom_indices(mol: Chem.Mol) -> list[int]:
    indices: list[int] = []
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() != 6 or not _has_hydroxy_neighbor(atom):
            continue

        backbone_neighbors = [
            neighbor
            for neighbor in atom.GetNeighbors()
            if _is_backbone_methylene(neighbor, atom.GetIdx())
        ]
        if len(backbone_neighbors) == 1:
            indices.append(atom.GetIdx())
    return indices
```

</details>

<a id="definition-122"></a>

## `_validate_pha_stereochemistry`

Source lines 122–145. Internal helper/protocol method.

```python
def _validate_pha_stereochemistry(mol: Chem.Mol, expected_count: int, stereochemistry: str) -> None: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| mol | Chem.Mol | required |
| expected_count | int | required |
| stereochemistry | str | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `', '.join`, `Chem.AssignStereochemistry`, `Chem.FindMolChiralCenters`, `ValueError`, `_pha_chiral_atom_indices`, `centres.get`, `dict`, `len`, `validate_stereochemistry_option`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError(f'Expected {expected_count} PHA chiral centres, found {len(pha_centres)}')
ValueError(f'Expected all PHA chiral centres to be {expected_label}; found {details}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _validate_pha_stereochemistry(
    mol: Chem.Mol, expected_count: int, stereochemistry: str
) -> None:
    expected_label = validate_stereochemistry_option(stereochemistry)

    Chem.AssignStereochemistry(mol, cleanIt=True, force=True)
    centres = dict(Chem.FindMolChiralCenters(mol, includeUnassigned=True))
    pha_centres = _pha_chiral_atom_indices(mol)

    if len(pha_centres) != expected_count:
        raise ValueError(
            f"Expected {expected_count} PHA chiral centres, found {len(pha_centres)}"
        )

    mismatched = [
        (atom_idx, centres.get(atom_idx, "unassigned"))
        for atom_idx in pha_centres
        if centres.get(atom_idx) != expected_label
    ]
    if mismatched:
        details = ", ".join(f"atom {atom_idx}: {label}" for atom_idx, label in mismatched)
        raise ValueError(
            f"Expected all PHA chiral centres to be {expected_label}; found {details}"
        )
```

</details>

<a id="definition-148"></a>

## `_validate_side_chain_carbon_count`

Source lines 148–159. Internal helper/protocol method.

```python
def _validate_side_chain_carbon_count(mol: Chem.Mol, side_chain_length: int, n: int) -> None: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| mol | Chem.Mol | required |
| side_chain_length | int | required |
| n | int | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `_count_carbons`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError(f'Expected {expected_side_chain_carbons} side-chain carbons, found {observed_side_chain_carbons}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _validate_side_chain_carbon_count(
    mol: Chem.Mol, side_chain_length: int, n: int
) -> None:
    expected_side_chain_carbons = side_chain_length * n
    observed_side_chain_carbons = _count_carbons(mol) - (3 * n)

    if observed_side_chain_carbons != expected_side_chain_carbons:
        raise ValueError(
            "Expected "
            f"{expected_side_chain_carbons} side-chain carbons, "
            f"found {observed_side_chain_carbons}"
        )
```

</details>

<a id="definition-162"></a>

## `validate_pha_chain`

Source lines 162–171. Named callable; inspect its callers before treating it as a stable public API.

```python
def validate_pha_chain(mol: Chem.Mol | None, monomer: Monomer, n: int, stereochemistry: str) -> Chem.Mol: ...
```

### Purpose and original contract

Validate core chemistry invariants for a generated PHA oligomer.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| mol | Chem.Mol \| None | required |
| monomer | Monomer | required |
| n | int | required |
| stereochemistry | str | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `_sanitize_molecule`, `_validate_ester_bond_count`, `_validate_pha_stereochemistry`, `_validate_side_chain_carbon_count`.

Explicit return expressions; different branches may return different objects:

```python
mol
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def validate_pha_chain(
    mol: Chem.Mol | None, monomer: Monomer, n: int, stereochemistry: str
) -> Chem.Mol:
    """Validate core chemistry invariants for a generated PHA oligomer."""

    mol = _sanitize_molecule(mol, monomer.code, n)
    _validate_pha_stereochemistry(mol, expected_count=n, stereochemistry=stereochemistry)
    _validate_ester_bond_count(mol, n)
    _validate_side_chain_carbon_count(mol, monomer.side_chain_length, n)
    return mol
```

</details>

<a id="definition-174"></a>

## `_build_validated_pha_from_side_chain`

Source lines 174–199. Internal helper/protocol method.

```python
def _build_validated_pha_from_side_chain(side_chain: str, degree: int, stereochemistry: str, name: str, side_chain_length: int | None=None, validate_ester_count: bool=False) -> Chem.Mol: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| side_chain | str | required |
| degree | int | required |
| stereochemistry | str | required |
| name | str | required |
| side_chain_length | int \| None | None |
| validate_ester_count | bool | False |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `'; '.join`, `Chem.MolFromSmiles`, `ValueError`, `_build_oligomer_smiles`, `_sanitize_molecule`, `_validate_ester_bond_count`, `_validate_pha_stereochemistry`, `_validate_side_chain_carbon_count`, `errors.append`, `str`.

Explicit return expressions; different branches may return different objects:

```python
mol
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError(f'Failed to build {stereochemistry} PHA for {name}: {details}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _build_validated_pha_from_side_chain(
    side_chain: str,
    degree: int,
    stereochemistry: str,
    name: str,
    side_chain_length: int | None = None,
    validate_ester_count: bool = False,
) -> Chem.Mol:
    errors: list[str] = []
    for chiral_tag in ("@", "@@"):
        smiles = _build_oligomer_smiles(side_chain, degree, chiral_tag)
        try:
            mol = _sanitize_molecule(Chem.MolFromSmiles(smiles), name, degree)
            _validate_pha_stereochemistry(
                mol, expected_count=degree, stereochemistry=stereochemistry
            )
            if validate_ester_count:
                _validate_ester_bond_count(mol, degree)
            if side_chain_length is not None:
                _validate_side_chain_carbon_count(mol, side_chain_length, degree)
            return mol
        except ValueError as exc:
            errors.append(str(exc))

    details = "; ".join(errors)
    raise ValueError(f"Failed to build {stereochemistry} PHA for {name}: {details}")
```

</details>

<a id="definition-202"></a>

## `_validate_custom_name`

Source lines 202–205. Internal helper/protocol method.

```python
def _validate_custom_name(name: str) -> str: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| name | str | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `isinstance`, `name.strip`.

Explicit return expressions; different branches may return different objects:

```python
name.strip()
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('Custom PHA name must be a non-empty string')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _validate_custom_name(name: str) -> str:
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Custom PHA name must be a non-empty string")
    return name.strip()
```

</details>

<a id="definition-208"></a>

## `_side_chain_from_monomer_smiles`

Source lines 208–254. Internal helper/protocol method.

```python
def _side_chain_from_monomer_smiles(monomer_smiles: str, name: str) -> str: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| monomer_smiles | str | required |
| name | str | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `Chem.AssignStereochemistry`, `Chem.MolFragmentToSmiles`, `Chem.MolFromSmiles`, `ValueError`, `_is_backbone_methylene`, `_pha_chiral_atom_indices`, `_sanitize_molecule`, `atom.GetNeighbors`, `chiral_atom.GetIdx`, `chiral_atom.GetNeighbors`, `chiral_atom.GetProp`, `chiral_atom.HasProp`, `isinstance`, `len`, `mol.GetAtomWithIdx`, `monomer_smiles.strip`, `neighbor.GetAtomicNum`, `neighbor.GetIdx`, `set`, `side_atoms.add`, `side_neighbors[0].GetIdx`, `sorted`, `stack.extend`, `stack.pop`.

Explicit return expressions; different branches may return different objects:

```python
Chem.MolFragmentToSmiles(mol, atomsToUse=sorted(side_atoms), rootedAtAtom=side_root, isomericSmiles=True, canonical=False)
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('Custom monomer SMILES must be a non-empty string')
ValueError('Custom monomer must be a chiral 3-hydroxyalkanoic acid with one PHA backbone stereocentre')
ValueError('Custom monomer PHA stereocentre must be R')
ValueError('Custom monomer must have exactly one side chain')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _side_chain_from_monomer_smiles(monomer_smiles: str, name: str) -> str:
    if not isinstance(monomer_smiles, str) or not monomer_smiles.strip():
        raise ValueError("Custom monomer SMILES must be a non-empty string")

    mol = Chem.MolFromSmiles(monomer_smiles)
    mol = _sanitize_molecule(mol, name, 1)
    Chem.AssignStereochemistry(mol, cleanIt=True, force=True)

    pha_centres = _pha_chiral_atom_indices(mol)
    if len(pha_centres) != 1:
        raise ValueError(
            "Custom monomer must be a chiral 3-hydroxyalkanoic acid with one "
            "PHA backbone stereocentre"
        )

    chiral_atom = mol.GetAtomWithIdx(pha_centres[0])
    if not chiral_atom.HasProp("_CIPCode") or chiral_atom.GetProp("_CIPCode") != "R":
        raise ValueError("Custom monomer PHA stereocentre must be R")

    excluded = {chiral_atom.GetIdx()}
    side_neighbors = [
        neighbor
        for neighbor in chiral_atom.GetNeighbors()
        if neighbor.GetAtomicNum() != 8
        and not _is_backbone_methylene(neighbor, chiral_atom.GetIdx())
    ]
    if len(side_neighbors) != 1:
        raise ValueError("Custom monomer must have exactly one side chain")

    side_root = side_neighbors[0].GetIdx()
    stack = [side_root]
    side_atoms: set[int] = set()
    while stack:
        atom_idx = stack.pop()
        if atom_idx in side_atoms or atom_idx in excluded:
            continue
        side_atoms.add(atom_idx)
        atom = mol.GetAtomWithIdx(atom_idx)
        stack.extend(neighbor.GetIdx() for neighbor in atom.GetNeighbors())

    return Chem.MolFragmentToSmiles(
        mol,
        atomsToUse=sorted(side_atoms),
        rootedAtAtom=side_root,
        isomericSmiles=True,
        canonical=False,
    )
```

</details>

<a id="definition-257"></a>

## `build_pha_chain`

Source lines 257–275. Named callable; inspect its callers before treating it as a stable public API.

```python
def build_pha_chain(monomer: str, n: int, stereochemistry: str='R') -> Chem.Mol: ...
```

### Purpose and original contract

Build a minimal RDKit molecule for a homopolymeric PHA oligomer.

The returned molecule is capped as the linear hydroxy acid oligomer:
HO-[CH(R)-CH2-C(=O)-O]n-H, represented with implicit hydrogens.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| monomer | str | required |
| n | int | required |
| stereochemistry | str | 'R' |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `_build_validated_pha_from_side_chain`, `_validate_repeat_units`, `get_monomer`, `validate_stereochemistry_option`.

Explicit return expressions; different branches may return different objects:

```python
_build_validated_pha_from_side_chain(side_chain=monomer_entry.side_chain, degree=n, stereochemistry=stereochemistry, name=monomer_entry.code, side_chain_length=monomer_entry.side_chain_length, validate_ester_count=True)
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def build_pha_chain(monomer: str, n: int, stereochemistry: str = "R") -> Chem.Mol:
    """Build a minimal RDKit molecule for a homopolymeric PHA oligomer.

    The returned molecule is capped as the linear hydroxy acid oligomer:
    HO-[CH(R)-CH2-C(=O)-O]n-H, represented with implicit hydrogens.
    """

    _validate_repeat_units(n)
    stereochemistry = validate_stereochemistry_option(stereochemistry)

    monomer_entry = get_monomer(monomer)
    return _build_validated_pha_from_side_chain(
        side_chain=monomer_entry.side_chain,
        degree=n,
        stereochemistry=stereochemistry,
        name=monomer_entry.code,
        side_chain_length=monomer_entry.side_chain_length,
        validate_ester_count=True,
    )
```

</details>

<a id="definition-278"></a>

## `build_pha_by_sidechain`

Source lines 278–293. Named callable; inspect its callers before treating it as a stable public API.

```python
def build_pha_by_sidechain(side_chain_carbons: int, degree: int) -> Chem.Mol: ...
```

### Purpose and original contract

Build a linear R-PHA oligomer from an alkyl side-chain length.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| side_chain_carbons | int | required |
| degree | int | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `_build_validated_pha_from_side_chain`, `_validate_repeat_units`, `_validate_side_chain_carbons`.

Explicit return expressions; different branches may return different objects:

```python
_build_validated_pha_from_side_chain(side_chain=side_chain, degree=degree, stereochemistry='R', name=name, side_chain_length=side_chain_carbons, validate_ester_count=True)
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def build_pha_by_sidechain(side_chain_carbons: int, degree: int) -> Chem.Mol:
    """Build a linear R-PHA oligomer from an alkyl side-chain length."""

    _validate_side_chain_carbons(side_chain_carbons)
    _validate_repeat_units(degree)

    side_chain = "C" * side_chain_carbons
    name = f"PHA-C{side_chain_carbons}"
    return _build_validated_pha_from_side_chain(
        side_chain=side_chain,
        degree=degree,
        stereochemistry="R",
        name=name,
        side_chain_length=side_chain_carbons,
        validate_ester_count=True,
    )
```

</details>

<a id="definition-296"></a>

## `build_custom_pha`

Source lines 296–308. Named callable; inspect its callers before treating it as a stable public API.

```python
def build_custom_pha(monomer_smiles: str, degree: int, name: str) -> Chem.Mol: ...
```

### Purpose and original contract

Build an R-PHA oligomer from a user-defined 3-hydroxy acid monomer.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| monomer_smiles | str | required |
| degree | int | required |
| name | str | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `_build_validated_pha_from_side_chain`, `_side_chain_from_monomer_smiles`, `_validate_custom_name`, `_validate_repeat_units`.

Explicit return expressions; different branches may return different objects:

```python
_build_validated_pha_from_side_chain(side_chain=side_chain, degree=degree, stereochemistry='R', name=name)
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def build_custom_pha(monomer_smiles: str, degree: int, name: str) -> Chem.Mol:
    """Build an R-PHA oligomer from a user-defined 3-hydroxy acid monomer."""

    name = _validate_custom_name(name)
    _validate_repeat_units(degree)

    side_chain = _side_chain_from_monomer_smiles(monomer_smiles, name)
    return _build_validated_pha_from_side_chain(
        side_chain=side_chain,
        degree=degree,
        stereochemistry="R",
        name=name,
    )
```

</details>
