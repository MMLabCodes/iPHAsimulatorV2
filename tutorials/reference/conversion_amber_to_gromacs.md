# conversion_amber_to_gromacs.py

Whole-system format conversion through ParmEd. A small charge-rounding correction precedes topology/coordinate writing. This is a representation change, not a new force-field fit or a dynamics run.

[Current source](../../src/iphasimulator/conversion_amber_to_gromacs.py)

This page is generated from source syntax. Original docstrings can be incomplete or outdated; module notes above identify known discrepancies. Call/return/error lists describe direct syntax, not all behaviour inside callees. Read the source excerpt for branch order and effects. No scientific execution is implied.

Explicit functions/methods/nested helpers: **2**.

## Module imports

```python
from __future__ import annotations
from dataclasses import dataclass
import math
from pathlib import Path
```

## Classes and result records

### `GromacsConversionOutputs`

Files produced by AMBER to GROMACS conversion.

Decorators: `dataclass(frozen=True)`.

Declared fields/defaults (instance state may also be set by methods):

```python
output_dir: Path
top_path: Path
gro_path: Path
```

Dataclass-generated methods are implicit and are not counted as explicit function definitions.

## Function map

- [`_normalize_structure_charge` — source line 30](#definition-30)
- [`convert_amber_to_gromacs` — source line 55](#definition-55)

<a id="definition-30"></a>

## `_normalize_structure_charge`

Source lines 30–52. Internal helper/protocol method.

```python
def _normalize_structure_charge(structure, *, max_correction: float=0.05) -> float: ...
```

### Purpose and original contract

Remove small charge-rounding residue before writing GROMACS topology.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| structure | not annotated | required |
| max_correction (keyword-only) | float | 0.05 |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `abs`, `len`, `list`, `math.fsum`, `round`.

Explicit return expressions; different branches may return different objects:

```python
total_charge
math.fsum((atom.charge for atom in atoms))
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('Cannot normalize the charge of a structure without atoms')
ValueError(f'Structure charge {total_charge:.8f} is too far from integer charge {target_charge} to normalize safely')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _normalize_structure_charge(structure, *, max_correction: float = 0.05) -> float:
    """Remove small charge-rounding residue before writing GROMACS topology."""

    atoms = list(structure.atoms)
    if not atoms:
        raise ValueError("Cannot normalize the charge of a structure without atoms")

    total_charge = math.fsum(atom.charge for atom in atoms)
    target_charge = round(total_charge)
    correction = target_charge - total_charge
    if abs(correction) > max_correction:
        raise ValueError(
            f"Structure charge {total_charge:.8f} is too far from integer charge "
            f"{target_charge} to normalize safely"
        )
    if correction == 0:
        return total_charge

    correction_per_atom = correction / len(atoms)
    for atom in atoms:
        atom.charge += correction_per_atom
    atoms[-1].charge += target_charge - math.fsum(atom.charge for atom in atoms)
    return math.fsum(atom.charge for atom in atoms)
```

</details>

<a id="definition-55"></a>

## `convert_amber_to_gromacs`

Source lines 55–98. Named callable; inspect its callers before treating it as a stable public API.

```python
def convert_amber_to_gromacs(prmtop_file: str, inpcrd_file: str, output_dir: str, system_name: str) -> GromacsConversionOutputs: ...
```

### Purpose and original contract

Convert AMBER ``prmtop``/``inpcrd`` files to GROMACS ``top``/``gro``.

ParmEd is required because it understands both AMBER and GROMACS topology
formats. Install it with ``conda install -c conda-forge parmed``.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| prmtop_file | str | required |
| inpcrd_file | str | required |
| output_dir | str | required |
| system_name | str | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `FileNotFoundError`, `GromacsConversionOutputs`, `ImportError`, `Path`, `ValueError`, `_normalize_structure_charge`, `inpcrd_path.exists`, `output_path.mkdir`, `pmd.load_file`, `prmtop_path.exists`, `str`, `structure.save`, `system_name.strip`.

Explicit return expressions; different branches may return different objects:

```python
GromacsConversionOutputs(output_dir=output_path, top_path=top_path, gro_path=gro_path)
```

Calls worth inspecting for I/O, state changes or delegated execution: `output_path.mkdir`, `pmd.load_file`, `structure.save`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ImportError('ParmEd is required to convert AMBER files to GROMACS. Install it with: conda install -c conda-forge parmed')
FileNotFoundError(f'AMBER topology file not found: {prmtop_path}')
FileNotFoundError(f'AMBER coordinate file not found: {inpcrd_path}')
ValueError('system_name must be a non-empty string')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def convert_amber_to_gromacs(
    prmtop_file: str,
    inpcrd_file: str,
    output_dir: str,
    system_name: str,
) -> GromacsConversionOutputs:
    """Convert AMBER ``prmtop``/``inpcrd`` files to GROMACS ``top``/``gro``.

    ParmEd is required because it understands both AMBER and GROMACS topology
    formats. Install it with ``conda install -c conda-forge parmed``.
    """

    try:
        import parmed as pmd
    except ImportError as exc:
        raise ImportError(
            "ParmEd is required to convert AMBER files to GROMACS. Install it "
            "with: conda install -c conda-forge parmed"
        ) from exc

    prmtop_path = Path(prmtop_file)
    inpcrd_path = Path(inpcrd_file)
    if not prmtop_path.exists():
        raise FileNotFoundError(f"AMBER topology file not found: {prmtop_path}")
    if not inpcrd_path.exists():
        raise FileNotFoundError(f"AMBER coordinate file not found: {inpcrd_path}")
    if not system_name.strip():
        raise ValueError("system_name must be a non-empty string")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    top_path = output_path / f"{system_name}.top"
    gro_path = output_path / f"{system_name}.gro"

    structure = pmd.load_file(str(prmtop_path), str(inpcrd_path))
    _normalize_structure_charge(structure)
    structure.save(str(top_path), overwrite=True)
    structure.save(str(gro_path), overwrite=True)

    return GromacsConversionOutputs(
        output_dir=output_path,
        top_path=top_path,
        gro_path=gro_path,
    )
```

</details>
