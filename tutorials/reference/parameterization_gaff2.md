# parameterization_gaff2.py

Whole-molecule SDF-to-Amber pipeline using Antechamber, Parmchk2 and LEaP. Includes executable checks, command invocation, charge-rounding adjustment, input preparation, timing and structured outputs. It is separate from trimer-to-residue parameterisation.

[Current source](../../src/iphasimulator/parameterization_gaff2.py)

This page is generated from source syntax. Original docstrings can be incomplete or outdated; module notes above identify known discrepancies. Call/return/error lists describe direct syntax, not all behaviour inside callees. Read the source excerpt for branch order and effects. No scientific execution is implied.

Explicit functions/methods/nested helpers: **8**.

## Module imports

```python
from __future__ import annotations
from decimal import Decimal
from dataclasses import dataclass
from pathlib import Path
import re
import shutil
import shlex
import subprocess
import time
from collections.abc import Sequence
from rdkit import Chem
from iphasimulator.export import prepare_molecule_3d
```

## Classes and result records

### `Gaff2Outputs`

Files produced by the GAFF2/AmberTools workflow.

Decorators: `dataclass(frozen=True)`.

Declared fields/defaults (instance state may also be set by methods):

```python
output_dir: Path
mol2_path: Path
frcmod_path: Path
tleap_input_path: Path
prmtop_path: Path
inpcrd_path: Path
pdb_path: Path
antechamber_log: Path
raw_antechamber_log: Path
sqm_log: Path
parmchk2_log: Path
tleap_log: Path
timing_log: Path
antechamber_seconds: float
parmchk2_seconds: float
tleap_seconds: float
```

Dataclass-generated methods are implicit and are not counted as explicit function definitions.

### `AmberToolsError`

Raised when AmberTools is unavailable or a command fails.

## Function map

- [`_normalize_mol2_charges` — source line 58](#definition-58)
- [`ambertools_available` — source line 132](#definition-132)
- [`require_ambertools` — source line 138](#definition-138)
- [`_run_command` — source line 152](#definition-152)
- [`_write_tleap_input` — source line 205](#definition-205)
- [`_prepare_antechamber_sdf` — source line 230](#definition-230)
- [`_write_timing_log` — source line 250](#definition-250)
- [`parameterize_gaff2` — source line 270](#definition-270)

<a id="definition-58"></a>

## `_normalize_mol2_charges`

Source lines 58–129. Internal helper/protocol method.

```python
def _normalize_mol2_charges(path: Path, *, net_charge: int, max_correction: Decimal=Decimal('0.05')) -> tuple[Decimal, Decimal]: ...
```

### Purpose and original contract

Distribute MOL2 charge-rounding residue to reach an integer net charge.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| path | Path | required |
| net_charge (keyword-only) | int | required |
| max_correction (keyword-only) | Decimal | Decimal('0.05') |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `'\n'.join`, `AmberToolsError`, `Decimal`, `abs`, `atom_entries.append`, `charge_token.end`, `charge_token.group`, `charge_token.start`, `divmod`, `enumerate`, `int`, `len`, `line.startswith`, `line.strip`, `list`, `path.read_text`, `path.read_text().splitlines`, `path.write_text`, `re.finditer`, `sum`.

Explicit return expressions; different branches may return different objects:

```python
(original_charge, original_charge)
(original_charge, normalized_total)
```

Calls worth inspecting for I/O, state changes or delegated execution: `path.read_text`, `path.read_text().splitlines`, `path.write_text`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
AmberToolsError(f'Invalid MOL2 atom line in {path}: {line}')
AmberToolsError(f'No MOL2 atoms found in {path}')
AmberToolsError(f'MOL2 charge {original_charge} is too far from requested net charge {net_charge} to normalize safely: {path}')
AmberToolsError(f'MOL2 charge correction {correction} cannot be represented at six-decimal precision: {path}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _normalize_mol2_charges(
    path: Path,
    *,
    net_charge: int,
    max_correction: Decimal = Decimal("0.05"),
) -> tuple[Decimal, Decimal]:
    """Distribute MOL2 charge-rounding residue to reach an integer net charge."""

    lines = path.read_text().splitlines()
    atom_entries: list[tuple[int, int, int, Decimal]] = []
    in_atom_section = False

    for line_index, line in enumerate(lines):
        if line.startswith("@<TRIPOS>ATOM"):
            in_atom_section = True
            continue
        if line.startswith("@<TRIPOS>") and in_atom_section:
            break
        if not in_atom_section or not line.strip():
            continue

        tokens = list(re.finditer(r"\S+", line))
        if len(tokens) < 9:
            raise AmberToolsError(f"Invalid MOL2 atom line in {path}: {line}")
        charge_token = tokens[8]
        atom_entries.append(
            (
                line_index,
                charge_token.start(),
                charge_token.end(),
                Decimal(charge_token.group()),
            )
        )

    if not atom_entries:
        raise AmberToolsError(f"No MOL2 atoms found in {path}")

    original_charge = sum((entry[3] for entry in atom_entries), Decimal("0"))
    correction = Decimal(net_charge) - original_charge
    if abs(correction) > max_correction:
        raise AmberToolsError(
            f"MOL2 charge {original_charge} is too far from requested net charge "
            f"{net_charge} to normalize safely: {path}"
        )
    if correction == 0:
        return original_charge, original_charge

    precision = Decimal("0.000001")
    correction_units = int(correction / precision)
    if Decimal(correction_units) * precision != correction:
        raise AmberToolsError(
            f"MOL2 charge correction {correction} cannot be represented at "
            f"six-decimal precision: {path}"
        )

    sign = 1 if correction_units > 0 else -1
    units_per_atom, remainder = divmod(abs(correction_units), len(atom_entries))
    for atom_index, (line_index, start, end, charge) in enumerate(atom_entries):
        extra_unit = 1 if atom_index < remainder else 0
        delta = Decimal(sign * (units_per_atom + extra_unit)) * precision
        normalized_charge = charge + delta
        lines[line_index] = (
            lines[line_index][:start]
            + f"{normalized_charge:.6f}"
            + lines[line_index][end:]
        )

    path.write_text("\n".join(lines) + "\n")
    normalized_total = sum(
        (entry[3] for entry in atom_entries), Decimal("0")
    ) + correction
    return original_charge, normalized_total
```

</details>

<a id="definition-132"></a>

## `ambertools_available`

Source lines 132–135. Named callable; inspect its callers before treating it as a stable public API.

```python
def ambertools_available() -> bool: ...
```

### Purpose and original contract

Return True when the required AmberTools executables are on PATH.

### Inputs

No explicit arguments.

### How to read this implementation

Direct calls (sorted inventory, not execution order): `all`, `shutil.which`.

Explicit return expressions; different branches may return different objects:

```python
all((shutil.which(command) for command in ('antechamber', 'parmchk2', 'tleap')))
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def ambertools_available() -> bool:
    """Return True when the required AmberTools executables are on PATH."""

    return all(shutil.which(command) for command in ("antechamber", "parmchk2", "tleap"))
```

</details>

<a id="definition-138"></a>

## `require_ambertools`

Source lines 138–149. Named callable; inspect its callers before treating it as a stable public API.

```python
def require_ambertools() -> None: ...
```

### Purpose and original contract

Raise a clear error if AmberTools executables are not available.

### Inputs

No explicit arguments.

### How to read this implementation

Direct calls (sorted inventory, not execution order): `', '.join`, `AmberToolsError`, `shutil.which`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
AmberToolsError('AmberTools executables not found on PATH: ' + ', '.join(missing))
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def require_ambertools() -> None:
    """Raise a clear error if AmberTools executables are not available."""

    missing = [
        command
        for command in ("antechamber", "parmchk2", "tleap")
        if shutil.which(command) is None
    ]
    if missing:
        raise AmberToolsError(
            "AmberTools executables not found on PATH: " + ", ".join(missing)
        )
```

</details>

<a id="definition-152"></a>

## `_run_command`

Source lines 152–202. Internal helper/protocol method.

```python
def _run_command(command: Sequence[str], cwd: Path, log_path: Path, *, stage_name: str, raw_log_path: Path | None=None, verbose: bool=False, runner=subprocess.run) -> float: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| command | Sequence[str] | required |
| cwd | Path | required |
| log_path | Path | required |
| stage_name (keyword-only) | str | required |
| raw_log_path (keyword-only) | Path \| None | None |
| verbose (keyword-only) | bool | False |
| runner (keyword-only) | not annotated | subprocess.run |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `' '.join`, `'\n'.join`, `AmberToolsError`, `list`, `log_path.write_text`, `print`, `raw_log_path.write_text`, `runner`, `shlex.join`, `str`, `time.perf_counter`.

Explicit return expressions; different branches may return different objects:

```python
elapsed_seconds
```

Calls worth inspecting for I/O, state changes or delegated execution: `log_path.write_text`, `raw_log_path.write_text`, `runner`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
AmberToolsError(f"Command failed with exit code {result.returncode}: {' '.join(command)}. See {log_path}")
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _run_command(
    command: Sequence[str],
    cwd: Path,
    log_path: Path,
    *,
    stage_name: str,
    raw_log_path: Path | None = None,
    verbose: bool = False,
    runner=subprocess.run,
) -> float:
    command_text = shlex.join(command)
    if verbose:
        print(f"[GAFF2:{stage_name}] Running: {command_text}")

    start = time.perf_counter()
    result = runner(
        list(command),
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    elapsed_seconds = time.perf_counter() - start

    output = result.stdout or ""
    if raw_log_path is not None:
        raw_log_path.write_text(output)
        log_path.write_text(
            "\n".join(
                [
                    f"Stage: {stage_name}",
                    f"Command: {command_text}",
                    f"Working directory: {cwd}",
                    f"Elapsed seconds: {elapsed_seconds:.3f}",
                    f"Raw log: {raw_log_path}",
                    "",
                    output,
                ]
            )
        )
    else:
        log_path.write_text(output)

    if result.returncode != 0:
        raise AmberToolsError(
            f"Command failed with exit code {result.returncode}: {' '.join(command)}. "
            f"See {log_path}"
        )
    if verbose:
        print(f"[GAFF2:{stage_name}] Completed in {elapsed_seconds:.1f}s")
    return elapsed_seconds
```

</details>

<a id="definition-205"></a>

## `_write_tleap_input`

Source lines 205–227. Internal helper/protocol method.

```python
def _write_tleap_input(path: Path, mol2_path: Path, frcmod_path: Path, prmtop_path: Path, inpcrd_path: Path, pdb_path: Path, unit_name: str) -> None: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| path | Path | required |
| mol2_path | Path | required |
| frcmod_path | Path | required |
| prmtop_path | Path | required |
| inpcrd_path | Path | required |
| pdb_path | Path | required |
| unit_name | str | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `'\n'.join`, `path.write_text`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Calls worth inspecting for I/O, state changes or delegated execution: `path.write_text`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _write_tleap_input(
    path: Path,
    mol2_path: Path,
    frcmod_path: Path,
    prmtop_path: Path,
    inpcrd_path: Path,
    pdb_path: Path,
    unit_name: str,
) -> None:
    path.write_text(
        "\n".join(
            [
                "source leaprc.gaff2",
                f"loadamberparams {frcmod_path.name}",
                f"{unit_name} = loadmol2 {mol2_path.name}",
                f"check {unit_name}",
                f"saveamberparm {unit_name} {prmtop_path.name} {inpcrd_path.name}",
                f"savepdb {unit_name} {pdb_path.name}",
                "quit",
                "",
            ]
        )
    )
```

</details>

<a id="definition-230"></a>

## `_prepare_antechamber_sdf`

Source lines 230–247. Internal helper/protocol method.

```python
def _prepare_antechamber_sdf(input_path: Path, output_path: Path, stem: str) -> tuple[Path, int | None]: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| input_path | Path | required |
| output_path | Path | required |
| stem | str | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `Chem.SDMolSupplier`, `Chem.SDWriter`, `next`, `prepare_molecule_3d`, `prepared.GetNumAtoms`, `str`, `writer.close`, `writer.write`.

Explicit return expressions; different branches may return different objects:

```python
(input_path, None)
(prepared_path, prepared.GetNumAtoms())
```

Calls worth inspecting for I/O, state changes or delegated execution: `Chem.SDWriter`, `writer.close`, `writer.write`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _prepare_antechamber_sdf(
    input_path: Path,
    output_path: Path,
    stem: str,
) -> tuple[Path, int | None]:
    supplier = Chem.SDMolSupplier(str(input_path), removeHs=False)
    mol = next((candidate for candidate in supplier if candidate is not None), None)
    if mol is None:
        return input_path, None

    prepared_path = output_path / f"{stem}.antechamber.sdf"
    prepared = prepare_molecule_3d(mol)
    writer = Chem.SDWriter(str(prepared_path))
    try:
        writer.write(prepared)
    finally:
        writer.close()
    return prepared_path, prepared.GetNumAtoms()
```

</details>

<a id="definition-250"></a>

## `_write_timing_log`

Source lines 250–267. Internal helper/protocol method.

```python
def _write_timing_log(path: Path, *, antechamber_seconds: float, parmchk2_seconds: float, tleap_seconds: float) -> None: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| path | Path | required |
| antechamber_seconds (keyword-only) | float | required |
| parmchk2_seconds (keyword-only) | float | required |
| tleap_seconds (keyword-only) | float | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `'\n'.join`, `path.write_text`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Calls worth inspecting for I/O, state changes or delegated execution: `path.write_text`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _write_timing_log(
    path: Path,
    *,
    antechamber_seconds: float,
    parmchk2_seconds: float,
    tleap_seconds: float,
) -> None:
    path.write_text(
        "\n".join(
            [
                f"antechamber_seconds={antechamber_seconds:.3f}",
                f"parmchk2_seconds={parmchk2_seconds:.3f}",
                f"tleap_seconds={tleap_seconds:.3f}",
                f"total_seconds={antechamber_seconds + parmchk2_seconds + tleap_seconds:.3f}",
                "",
            ]
        )
    )
```

</details>

<a id="definition-270"></a>

## `parameterize_gaff2`

Source lines 270–438. Named callable; inspect its callers before treating it as a stable public API.

```python
def parameterize_gaff2(input_sdf: str | Path, output_dir: str | Path, *, name: str | None=None, net_charge: int=0, residue_name: str='MOL', charge_method: str='abcg2', atom_count_warning_threshold: int | None=120, verbose: bool=False, runner=subprocess.run, check_tools: bool=True) -> Gaff2Outputs: ...
```

### Purpose and original contract

Create GAFF2 AMBER topology files from an input SDF.

The workflow runs AmberTools in three steps:
antechamber -> parmchk2 -> tleap.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| input_sdf | str \| Path | required |
| output_dir | str \| Path | required |
| name (keyword-only) | str \| None | None |
| net_charge (keyword-only) | int | 0 |
| residue_name (keyword-only) | str | 'MOL' |
| charge_method (keyword-only) | str | 'abcg2' |
| atom_count_warning_threshold (keyword-only) | int \| None | 120 |
| verbose (keyword-only) | bool | False |
| runner (keyword-only) | not annotated | subprocess.run |
| check_tools (keyword-only) | bool | True |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `FileNotFoundError`, `Gaff2Outputs`, `Path`, `_normalize_mol2_charges`, `_prepare_antechamber_sdf`, `_run_command`, `_write_timing_log`, `_write_tleap_input`, `antechamber_input_path.resolve`, `antechamber_log.open`, `generated_sqm_log.exists`, `handle.write`, `input_path.exists`, `mol2_path.exists`, `output_path.mkdir`, `print`, `require_ambertools`, `shutil.copyfile`, `sqm_log.exists`, `sqm_log.write_text`, `str`.

Explicit return expressions; different branches may return different objects:

```python
Gaff2Outputs(output_dir=output_path, mol2_path=mol2_path, frcmod_path=frcmod_path, tleap_input_path=tleap_input_path, prmtop_path=prmtop_path, inpcrd_path=inpcrd_path, pdb_path=pdb_path, antechamber_log=antechamber_log, raw_antechamber_log=raw_antechamber_log, sqm_log=sqm_log, parmchk2_log=parmchk2_log, tleap_log=tleap_log, timing_log=timing_log, antechamber_seconds=antechamber_seconds, parmchk2_s … [full expression below]
```

Calls worth inspecting for I/O, state changes or delegated execution: `_run_command`, `_write_timing_log`, `_write_tleap_input`, `antechamber_log.open`, `handle.write`, `output_path.mkdir`, `shutil.copyfile`, `sqm_log.write_text`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
FileNotFoundError(f'Input SDF not found: {input_path}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def parameterize_gaff2(
    input_sdf: str | Path,
    output_dir: str | Path,
    *,
    name: str | None = None,
    net_charge: int = 0,
    residue_name: str = "MOL",
    charge_method: str = "abcg2",
    atom_count_warning_threshold: int | None = 120,
    verbose: bool = False,
    runner=subprocess.run,
    check_tools: bool = True,
) -> Gaff2Outputs:
    """Create GAFF2 AMBER topology files from an input SDF.

    The workflow runs AmberTools in three steps:
    antechamber -> parmchk2 -> tleap.
    """

    if check_tools:
        require_ambertools()

    input_path = Path(input_sdf)
    if not input_path.exists():
        raise FileNotFoundError(f"Input SDF not found: {input_path}")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    stem = name or input_path.stem
    mol2_path = output_path / f"{stem}.gaff2.mol2"
    frcmod_path = output_path / f"{stem}.gaff2.frcmod"
    tleap_input_path = output_path / "tleap.in"
    prmtop_path = output_path / f"{stem}.prmtop"
    inpcrd_path = output_path / f"{stem}.inpcrd"
    pdb_path = output_path / f"{stem}.tleap.pdb"
    antechamber_log = output_path / "antechamber.log"
    raw_antechamber_log = output_path / "antechamber.raw.log"
    sqm_log = output_path / "sqm.raw.out"
    parmchk2_log = output_path / "parmchk2.log"
    tleap_log = output_path / "tleap.log"
    timing_log = output_path / "timing.log"
    antechamber_input_path, atom_count = _prepare_antechamber_sdf(
        input_path,
        output_path,
        stem,
    )
    if (
        atom_count_warning_threshold is not None
        and atom_count is not None
        and atom_count > atom_count_warning_threshold
    ):
        print(
            f"WARNING: {stem} has {atom_count} atoms after hydrogen addition; "
            f"AmberTools charge generation may be slow. Threshold: "
            f"{atom_count_warning_threshold} atoms."
        )

    antechamber_command = [
        "antechamber",
        "-i",
        str(antechamber_input_path.resolve()),
        "-fi",
        "sdf",
        "-o",
        mol2_path.name,
        "-fo",
        "mol2",
        "-at",
        "gaff2",
        "-c",
        charge_method,
        "-nc",
        str(net_charge),
        "-rn",
        residue_name,
        "-s",
        "2",
    ]
    generated_sqm_log = output_path / "sqm.out"
    try:
        antechamber_seconds = _run_command(
            antechamber_command,
            output_path,
            antechamber_log,
            stage_name="antechamber",
            raw_log_path=raw_antechamber_log,
            verbose=verbose,
            runner=runner,
        )
    finally:
        if generated_sqm_log.exists():
            shutil.copyfile(generated_sqm_log, sqm_log)
        elif not sqm_log.exists():
            sqm_log.write_text("sqm.out was not generated by antechamber.\n")
    if mol2_path.exists():
        original_charge, normalized_charge = _normalize_mol2_charges(
            mol2_path,
            net_charge=net_charge,
        )
        if original_charge != normalized_charge:
            with antechamber_log.open("a") as handle:
                handle.write(
                    "\nNormalized rounded MOL2 charge from "
                    f"{original_charge} to {normalized_charge}.\n"
                )

    parmchk2_command = [
        "parmchk2",
        "-i",
        mol2_path.name,
        "-f",
        "mol2",
        "-o",
        frcmod_path.name,
        "-s",
        "gaff2",
    ]
    parmchk2_seconds = _run_command(
        parmchk2_command,
        output_path,
        parmchk2_log,
        stage_name="parmchk2",
        verbose=verbose,
        runner=runner,
    )

    _write_tleap_input(
        tleap_input_path,
        mol2_path,
        frcmod_path,
        prmtop_path,
        inpcrd_path,
        pdb_path,
        unit_name="mol",
    )
    tleap_seconds = _run_command(
        ["tleap", "-f", tleap_input_path.name],
        output_path,
        tleap_log,
        stage_name="tleap",
        verbose=verbose,
        runner=runner,
    )
    _write_timing_log(
        timing_log,
        antechamber_seconds=antechamber_seconds,
        parmchk2_seconds=parmchk2_seconds,
        tleap_seconds=tleap_seconds,
    )

    return Gaff2Outputs(
        output_dir=output_path,
        mol2_path=mol2_path,
        frcmod_path=frcmod_path,
        tleap_input_path=tleap_input_path,
        prmtop_path=prmtop_path,
        inpcrd_path=inpcrd_path,
        pdb_path=pdb_path,
        antechamber_log=antechamber_log,
        raw_antechamber_log=raw_antechamber_log,
        sqm_log=sqm_log,
        parmchk2_log=parmchk2_log,
        tleap_log=tleap_log,
        timing_log=timing_log,
        antechamber_seconds=antechamber_seconds,
        parmchk2_seconds=parmchk2_seconds,
        tleap_seconds=tleap_seconds,
    )
```

</details>
