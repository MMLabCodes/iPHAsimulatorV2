# system_builder_packmol.py

Separate Packmol route for initial solvated coordinates. Estimate counts, copy/write support structures, compose packing input and optionally invoke Packmol. Producing a packed PDB does not complete a parameterised dynamics workflow.

[Current source](../../src/iphasimulator/system_builder_packmol.py)

This page is generated from source syntax. Original docstrings can be incomplete or outdated; module notes above identify known discrepancies. Call/return/error lists describe direct syntax, not all behaviour inside callees. Read the source excerpt for branch order and effects. No scientific execution is implied.

Explicit functions/methods/nested helpers: **9**.

## Module imports

```python
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from collections.abc import Sequence
import shutil
import subprocess
```

## Classes and result records

### `PackmolBuildResult`

Files and counts produced by the Packmol solvated-system builder.

Decorators: `dataclass(frozen=True)`.

Declared fields/defaults (instance state may also be set by methods):

```python
output_dir: Path
solvated_pdb_path: Path
packmol_input_path: Path
packmol_log_path: Path
copied_polymer_paths: tuple[Path, ...]
support_structure_paths: tuple[Path, ...]
box_size_nm: float
water_count: int
sodium_count: int
chloride_count: int
polymer_counts: tuple[int, ...]
```

Dataclass-generated methods are implicit and are not counted as explicit function definitions.

## Function map

- [`estimate_tip3p_water_count` — source line 65](#definition-65)
- [`estimate_ion_pairs` — source line 73](#definition-73)
- [`_normalise_polymer_counts` — source line 88](#definition-88)
- [`_copy_polymer_structures` — source line 107](#definition-107)
- [`_write_support_structures` — source line 122](#definition-122)
- [`_structure_block` — source line 135](#definition-135)
- [`_write_packmol_input` — source line 161](#definition-161)
- [`_ensure_cryst1_record` — source line 227](#definition-227)
- [`build_packmol_solvated_system` — source line 239](#definition-239)

<a id="definition-65"></a>

## `estimate_tip3p_water_count`

Source lines 65–70. Named callable; inspect its callers before treating it as a stable public API.

```python
def estimate_tip3p_water_count(box_size_nm: float) -> int: ...
```

### Purpose and original contract

Estimate the number of TIP3P waters for a cubic box at bulk density.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| box_size_nm | float | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `max`, `round`.

Explicit return expressions; different branches may return different objects:

```python
max(1, round(TIP3P_WATER_DENSITY_PER_NM3 * box_size_nm ** 3))
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('box_size_nm must be positive')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def estimate_tip3p_water_count(box_size_nm: float) -> int:
    """Estimate the number of TIP3P waters for a cubic box at bulk density."""

    if box_size_nm <= 0:
        raise ValueError("box_size_nm must be positive")
    return max(1, round(TIP3P_WATER_DENSITY_PER_NM3 * box_size_nm**3))
```

</details>

<a id="definition-73"></a>

## `estimate_ion_pairs`

Source lines 73–85. Named callable; inspect its callers before treating it as a stable public API.

```python
def estimate_ion_pairs(box_size_nm: float, nacl_concentration_molar: float) -> int: ...
```

### Purpose and original contract

Estimate NaCl ion pairs from molarity and cubic box volume.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| box_size_nm | float | required |
| nacl_concentration_molar | float | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `max`, `round`.

Explicit return expressions; different branches may return different objects:

```python
0
max(1, ion_pairs)
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('box_size_nm must be positive')
ValueError('nacl_concentration_molar must be non-negative')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def estimate_ion_pairs(box_size_nm: float, nacl_concentration_molar: float) -> int:
    """Estimate NaCl ion pairs from molarity and cubic box volume."""

    if box_size_nm <= 0:
        raise ValueError("box_size_nm must be positive")
    if nacl_concentration_molar < 0:
        raise ValueError("nacl_concentration_molar must be non-negative")
    if nacl_concentration_molar == 0:
        return 0

    box_volume_liters = box_size_nm**3 * LITERS_PER_NM3
    ion_pairs = round(nacl_concentration_molar * box_volume_liters * AVOGADRO_CONSTANT)
    return max(1, ion_pairs)
```

</details>

<a id="definition-88"></a>

## `_normalise_polymer_counts`

Source lines 88–104. Internal helper/protocol method.

```python
def _normalise_polymer_counts(polymer_count: int, num_polymers: int | Sequence[int]) -> tuple[int, ...]: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| polymer_count | int | required |
| num_polymers | int \| Sequence[int] | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `any`, `isinstance`, `len`, `range`, `tuple`.

Explicit return expressions; different branches may return different objects:

```python
tuple((num_polymers for _ in range(polymer_count)))
counts
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('num_polymers must be positive')
ValueError('num_polymers must be an integer or a sequence matching polymer_structures')
ValueError('all polymer counts must be positive')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _normalise_polymer_counts(
    polymer_count: int,
    num_polymers: int | Sequence[int],
) -> tuple[int, ...]:
    if isinstance(num_polymers, int):
        if num_polymers <= 0:
            raise ValueError("num_polymers must be positive")
        return tuple(num_polymers for _ in range(polymer_count))

    counts = tuple(num_polymers)
    if len(counts) != polymer_count:
        raise ValueError(
            "num_polymers must be an integer or a sequence matching polymer_structures"
        )
    if any(count <= 0 for count in counts):
        raise ValueError("all polymer counts must be positive")
    return counts
```

</details>

<a id="definition-107"></a>

## `_copy_polymer_structures`

Source lines 107–119. Internal helper/protocol method.

```python
def _copy_polymer_structures(polymer_structures: Sequence[str | Path], output_dir: Path) -> tuple[Path, ...]: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| polymer_structures | Sequence[str \| Path] | required |
| output_dir | Path | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `FileNotFoundError`, `Path`, `copied_paths.append`, `enumerate`, `shutil.copy2`, `source.exists`, `tuple`.

Explicit return expressions; different branches may return different objects:

```python
tuple(copied_paths)
```

Calls worth inspecting for I/O, state changes or delegated execution: `shutil.copy2`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
FileNotFoundError(f'Polymer structure not found: {source}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _copy_polymer_structures(
    polymer_structures: Sequence[str | Path],
    output_dir: Path,
) -> tuple[Path, ...]:
    copied_paths: list[Path] = []
    for index, polymer_structure in enumerate(polymer_structures, start=1):
        source = Path(polymer_structure)
        if not source.exists():
            raise FileNotFoundError(f"Polymer structure not found: {source}")
        destination = output_dir / f"polymer_{index}{source.suffix or '.pdb'}"
        shutil.copy2(source, destination)
        copied_paths.append(destination)
    return tuple(copied_paths)
```

</details>

<a id="definition-122"></a>

## `_write_support_structures`

Source lines 122–132. Internal helper/protocol method.

```python
def _write_support_structures(output_dir: Path, water_model: str) -> tuple[Path, ...]: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| output_dir | Path | required |
| water_model | str | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `chloride_path.write_text`, `sodium_path.write_text`, `water_model.lower`, `water_path.write_text`.

Explicit return expressions; different branches may return different objects:

```python
(water_path, sodium_path, chloride_path)
```

Calls worth inspecting for I/O, state changes or delegated execution: `chloride_path.write_text`, `sodium_path.write_text`, `water_path.write_text`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError("Only water_model='tip3p' is currently supported")
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _write_support_structures(output_dir: Path, water_model: str) -> tuple[Path, ...]:
    if water_model.lower() != "tip3p":
        raise ValueError("Only water_model='tip3p' is currently supported")

    water_path = output_dir / "tip3p_water.pdb"
    sodium_path = output_dir / "sodium_ion.pdb"
    chloride_path = output_dir / "chloride_ion.pdb"
    water_path.write_text(TIP3P_WATER_PDB)
    sodium_path.write_text(SODIUM_PDB)
    chloride_path.write_text(CHLORIDE_PDB)
    return water_path, sodium_path, chloride_path
```

</details>

<a id="definition-135"></a>

## `_structure_block`

Source lines 135–158. Internal helper/protocol method.

```python
def _structure_block(structure_path: Path, number: int, *, box_size_angstrom: float, margin_angstrom: float, comment: str) -> str: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| structure_path | Path | required |
| number | int | required |
| box_size_angstrom (keyword-only) | float | required |
| margin_angstrom (keyword-only) | float | required |
| comment (keyword-only) | str | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `'\n'.join`.

Explicit return expressions; different branches may return different objects:

```python
'\n'.join([f'# {comment}', f'structure {structure_path.name}', f'  number {number}', f'  inside box {margin_angstrom:.3f} {margin_angstrom:.3f} {margin_angstrom:.3f} {box_size_angstrom - margin_angstrom:.3f} {box_size_angstrom - margin_angstrom:.3f} {box_size_angstrom - margin_angstrom:.3f}', 'end structure', ''])
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _structure_block(
    structure_path: Path,
    number: int,
    *,
    box_size_angstrom: float,
    margin_angstrom: float,
    comment: str,
) -> str:
    return "\n".join(
        [
            f"# {comment}",
            f"structure {structure_path.name}",
            f"  number {number}",
            (
                "  inside box "
                f"{margin_angstrom:.3f} {margin_angstrom:.3f} {margin_angstrom:.3f} "
                f"{box_size_angstrom - margin_angstrom:.3f} "
                f"{box_size_angstrom - margin_angstrom:.3f} "
                f"{box_size_angstrom - margin_angstrom:.3f}"
            ),
            "end structure",
            "",
        ]
    )
```

</details>

<a id="definition-161"></a>

## `_write_packmol_input`

Source lines 161–224. Internal helper/protocol method.

```python
def _write_packmol_input(output_dir: Path, solvated_pdb_path: Path, copied_polymer_paths: Sequence[Path], polymer_counts: Sequence[int], water_path: Path, sodium_path: Path, chloride_path: Path, *, box_size_nm: float, polymer_spacing_nm: float, water_count: int, sodium_count: int, chloride_count: int) -> tuple[Path, str]: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| output_dir | Path | required |
| solvated_pdb_path | Path | required |
| copied_polymer_paths | Sequence[Path] | required |
| polymer_counts | Sequence[int] | required |
| water_path | Path | required |
| sodium_path | Path | required |
| chloride_path | Path | required |
| box_size_nm (keyword-only) | float | required |
| polymer_spacing_nm (keyword-only) | float | required |
| water_count (keyword-only) | int | required |
| sodium_count (keyword-only) | int | required |
| chloride_count (keyword-only) | int | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `'\n'.join`, `ValueError`, `_structure_block`, `enumerate`, `lines.append`, `packmol_input_path.write_text`, `zip`.

Explicit return expressions; different branches may return different objects:

```python
(packmol_input_path, packmol_input)
```

Calls worth inspecting for I/O, state changes or delegated execution: `packmol_input_path.write_text`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('polymer_spacing_nm leaves no usable space inside the box')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _write_packmol_input(
    output_dir: Path,
    solvated_pdb_path: Path,
    copied_polymer_paths: Sequence[Path],
    polymer_counts: Sequence[int],
    water_path: Path,
    sodium_path: Path,
    chloride_path: Path,
    *,
    box_size_nm: float,
    polymer_spacing_nm: float,
    water_count: int,
    sodium_count: int,
    chloride_count: int,
) -> tuple[Path, str]:
    box_size_angstrom = box_size_nm * 10.0
    polymer_margin_angstrom = polymer_spacing_nm * 10.0
    if polymer_margin_angstrom * 2 >= box_size_angstrom:
        raise ValueError("polymer_spacing_nm leaves no usable space inside the box")

    lines = [
        "# Packmol input generated by iPHASimulator.",
        "# Advanced route for PHA oligomer + TIP3P water + NaCl systems.",
        "tolerance 2.0",
        "filetype pdb",
        f"output {solvated_pdb_path.name}",
        "",
    ]

    for index, (polymer_path, count) in enumerate(
        zip(copied_polymer_paths, polymer_counts, strict=True),
        start=1,
    ):
        lines.append(
            _structure_block(
                polymer_path,
                count,
                box_size_angstrom=box_size_angstrom,
                margin_angstrom=polymer_margin_angstrom,
                comment=f"Polymer component {index}",
            )
        )

    for path, count, comment in (
        (water_path, water_count, "TIP3P water"),
        (sodium_path, sodium_count, "Na+ ions"),
        (chloride_path, chloride_count, "Cl- ions"),
    ):
        if count == 0:
            continue
        lines.append(
            _structure_block(
                path,
                count,
                box_size_angstrom=box_size_angstrom,
                margin_angstrom=0.0,
                comment=comment,
            )
        )

    packmol_input = "\n".join(lines)
    packmol_input_path = output_dir / "packmol_input.inp"
    packmol_input_path.write_text(packmol_input)
    return packmol_input_path, packmol_input
```

</details>

<a id="definition-227"></a>

## `_ensure_cryst1_record`

Source lines 227–236. Internal helper/protocol method.

```python
def _ensure_cryst1_record(pdb_path: Path, box_size_nm: float) -> None: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| pdb_path | Path | required |
| box_size_nm | float | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `'\n'.join`, `lines[0].startswith`, `pdb_path.read_text`, `pdb_path.read_text().splitlines`, `pdb_path.write_text`.

Explicit return expressions; different branches may return different objects:

```python
None
```

Calls worth inspecting for I/O, state changes or delegated execution: `pdb_path.read_text`, `pdb_path.read_text().splitlines`, `pdb_path.write_text`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _ensure_cryst1_record(pdb_path: Path, box_size_nm: float) -> None:
    lines = pdb_path.read_text().splitlines()
    if lines and lines[0].startswith("CRYST1"):
        return
    box_size_angstrom = box_size_nm * 10.0
    cryst1 = (
        f"CRYST1{box_size_angstrom:9.3f}{box_size_angstrom:9.3f}"
        f"{box_size_angstrom:9.3f}{90.0:7.2f}{90.0:7.2f}{90.0:7.2f} P 1           1"
    )
    pdb_path.write_text("\n".join([cryst1, *lines]) + "\n")
```

</details>

<a id="definition-239"></a>

## `build_packmol_solvated_system`

Source lines 239–348. Named callable; inspect its callers before treating it as a stable public API.

```python
def build_packmol_solvated_system(polymer_structures: Sequence[str | Path], output_dir: str | Path, *, box_size_nm: float, water_model: str='tip3p', nacl_concentration_molar: float=0.15, num_polymers: int | Sequence[int]=1, polymer_spacing_nm: float=1.0, packmol_command: str='packmol', run_packmol: bool=True, runner=subprocess.run) -> PackmolBuildResult: ...
```

### Purpose and original contract

Build an advanced solvated PHA/TIP3P/NaCl initial PDB using Packmol.

This route does not replace the standard GROMACS solvate/genion workflow.
It is an advanced builder for future realistic polymer simulations and can
later be extended to enzyme/polymer systems. Membranes are intentionally not
implemented here yet.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| polymer_structures | Sequence[str \| Path] | required |
| output_dir | str \| Path | required |
| box_size_nm (keyword-only) | float | required |
| water_model (keyword-only) | str | 'tip3p' |
| nacl_concentration_molar (keyword-only) | float | 0.15 |
| num_polymers (keyword-only) | int \| Sequence[int] | 1 |
| polymer_spacing_nm (keyword-only) | float | 1.0 |
| packmol_command (keyword-only) | str | 'packmol' |
| run_packmol (keyword-only) | bool | True |
| runner (keyword-only) | not annotated | subprocess.run |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `FileNotFoundError`, `PackmolBuildResult`, `Path`, `RuntimeError`, `ValueError`, `_copy_polymer_structures`, `_ensure_cryst1_record`, `_normalise_polymer_counts`, `_write_packmol_input`, `_write_support_structures`, `estimate_ion_pairs`, `estimate_tip3p_water_count`, `len`, `output_path.mkdir`, `packmol_log_path.write_text`, `runner`, `solvated_pdb_path.exists`.

Explicit return expressions; different branches may return different objects:

```python
PackmolBuildResult(output_dir=output_path, solvated_pdb_path=solvated_pdb_path, packmol_input_path=packmol_input_path, packmol_log_path=packmol_log_path, copied_polymer_paths=copied_polymer_paths, support_structure_paths=(water_path, sodium_path, chloride_path), box_size_nm=box_size_nm, water_count=water_count, sodium_count=ion_pairs, chloride_count=ion_pairs, polymer_counts=polymer_counts)
```

Calls worth inspecting for I/O, state changes or delegated execution: `_copy_polymer_structures`, `_write_packmol_input`, `_write_support_structures`, `output_path.mkdir`, `packmol_log_path.write_text`, `runner`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('At least one polymer structure is required')
ValueError('box_size_nm must be positive')
ValueError('polymer_spacing_nm must be non-negative')
RuntimeError('Packmol executable not found. Install Packmol or set packmol_command to the correct executable.')
RuntimeError(f'Packmol failed while building solvated_system.pdb with return code {result.returncode}. See {packmol_log_path}.')
FileNotFoundError(f'Packmol did not write: {solvated_pdb_path}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def build_packmol_solvated_system(
    polymer_structures: Sequence[str | Path],
    output_dir: str | Path,
    *,
    box_size_nm: float,
    water_model: str = "tip3p",
    nacl_concentration_molar: float = 0.15,
    num_polymers: int | Sequence[int] = 1,
    polymer_spacing_nm: float = 1.0,
    packmol_command: str = "packmol",
    run_packmol: bool = True,
    runner=subprocess.run,
) -> PackmolBuildResult:
    """Build an advanced solvated PHA/TIP3P/NaCl initial PDB using Packmol.

    This route does not replace the standard GROMACS solvate/genion workflow.
    It is an advanced builder for future realistic polymer simulations and can
    later be extended to enzyme/polymer systems. Membranes are intentionally not
    implemented here yet.
    """

    if not polymer_structures:
        raise ValueError("At least one polymer structure is required")
    if box_size_nm <= 0:
        raise ValueError("box_size_nm must be positive")
    if polymer_spacing_nm < 0:
        raise ValueError("polymer_spacing_nm must be non-negative")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    polymer_counts = _normalise_polymer_counts(len(polymer_structures), num_polymers)
    copied_polymer_paths = _copy_polymer_structures(polymer_structures, output_path)
    water_path, sodium_path, chloride_path = _write_support_structures(
        output_path,
        water_model,
    )

    water_count = estimate_tip3p_water_count(box_size_nm)
    ion_pairs = estimate_ion_pairs(box_size_nm, nacl_concentration_molar)
    solvated_pdb_path = output_path / "solvated_system.pdb"
    packmol_log_path = output_path / "packmol.log"

    packmol_input_path, packmol_input = _write_packmol_input(
        output_path,
        solvated_pdb_path,
        copied_polymer_paths,
        polymer_counts,
        water_path,
        sodium_path,
        chloride_path,
        box_size_nm=box_size_nm,
        polymer_spacing_nm=polymer_spacing_nm,
        water_count=water_count,
        sodium_count=ion_pairs,
        chloride_count=ion_pairs,
    )

    if run_packmol:
        try:
            result = runner(
                [packmol_command],
                input=packmol_input,
                cwd=output_path,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except FileNotFoundError as exc:
            packmol_log_path.write_text(
                "Packmol executable not found. Install Packmol or set "
                "packmol_command to the correct executable.\n"
            )
            raise RuntimeError(
                "Packmol executable not found. Install Packmol or set "
                "packmol_command to the correct executable."
            ) from exc

        packmol_log_path.write_text(
            "STDOUT:\n"
            f"{result.stdout}\n"
            "STDERR:\n"
            f"{result.stderr}\n"
        )
        if result.returncode != 0:
            raise RuntimeError(
                "Packmol failed while building solvated_system.pdb with return "
                f"code {result.returncode}. See {packmol_log_path}."
            )
        if not solvated_pdb_path.exists():
            raise FileNotFoundError(f"Packmol did not write: {solvated_pdb_path}")
        _ensure_cryst1_record(solvated_pdb_path, box_size_nm)
    else:
        packmol_log_path.write_text(
            "Packmol was not run. Generated packmol_input.inp only.\n"
        )

    return PackmolBuildResult(
        output_dir=output_path,
        solvated_pdb_path=solvated_pdb_path,
        packmol_input_path=packmol_input_path,
        packmol_log_path=packmol_log_path,
        copied_polymer_paths=copied_polymer_paths,
        support_structure_paths=(water_path, sodium_path, chloride_path),
        box_size_nm=box_size_nm,
        water_count=water_count,
        sodium_count=ion_pairs,
        chloride_count=ion_pairs,
        polymer_counts=polymer_counts,
    )
```

</details>
