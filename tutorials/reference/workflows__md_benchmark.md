# workflows/md_benchmark.py

Discover validation targets and coordinate whole-molecule GAFF2, the earlier OpenMM runner and GROMACS preparation. CLI parsing and per-target failure collection belong to this orchestration layer.

[Current source](../../src/iphasimulator/workflows/md_benchmark.py)

This page is generated from source syntax. Original docstrings can be incomplete or outdated; module notes above identify known discrepancies. Call/return/error lists describe direct syntax, not all behaviour inside callees. Read the source excerpt for branch order and effects. No scientific execution is implied.

Explicit functions/methods/nested helpers: **14**.

## Module imports

```python
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import argparse
from iphasimulator.parameterization_gaff2 import AmberToolsError, parameterize_gaff2
from iphasimulator.simulation_gromacs_runner import prepare_gromacs_run_folder, write_gromacs_solvation_files
from iphasimulator.simulation_openmm_amber_runner import OpenMMRunnerError, openmm_available, run_openmm_with_amber_topology
```

## Classes and result records

### `BenchmarkTarget`

Input and output paths for one benchmark system.

Decorators: `dataclass(frozen=True)`.

Declared fields/defaults (instance state may also be set by methods):

```python
name: str
sdf_path: Path
output_dir: Path
```

Dataclass-generated methods are implicit and are not counted as explicit function definitions.

## Function map

- [`BenchmarkTarget.gaff2_dir` — source line 38](#definition-38)
- [`BenchmarkTarget.prmtop_path` — source line 42](#definition-42)
- [`BenchmarkTarget.inpcrd_path` — source line 46](#definition-46)
- [`BenchmarkTarget.openmm_dir` — source line 50](#definition-50)
- [`BenchmarkTarget.gromacs_dir` — source line 54](#definition-54)
- [`_find_sdf` — source line 58](#definition-58)
- [`discover_targets` — source line 72](#definition-72)
- [`selected_system_names` — source line 100](#definition-100)
- [`_run_gaff2` — source line 112](#definition-112)
- [`_run_openmm` — source line 145](#definition-145)
- [`_prepare_gromacs` — source line 168](#definition-168)
- [`run_benchmark` — source line 193](#definition-193)
- [`parse_args` — source line 258](#definition-258)
- [`main` — source line 356](#definition-356)

<a id="definition-38"></a>

## `BenchmarkTarget.gaff2_dir`

Source lines 38–39. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `property`.

```python
def gaff2_dir(self) -> Path: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |

### How to read this implementation

No direct function calls were found in this definition's own body.

Explicit return expressions; different branches may return different objects:

```python
self.output_dir / 'gaff2'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def gaff2_dir(self) -> Path:
    return self.output_dir / "gaff2"
```

</details>

<a id="definition-42"></a>

## `BenchmarkTarget.prmtop_path`

Source lines 42–43. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `property`.

```python
def prmtop_path(self) -> Path: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |

### How to read this implementation

No direct function calls were found in this definition's own body.

Explicit return expressions; different branches may return different objects:

```python
self.gaff2_dir / f'{self.name}.prmtop'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def prmtop_path(self) -> Path:
    return self.gaff2_dir / f"{self.name}.prmtop"
```

</details>

<a id="definition-46"></a>

## `BenchmarkTarget.inpcrd_path`

Source lines 46–47. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `property`.

```python
def inpcrd_path(self) -> Path: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |

### How to read this implementation

No direct function calls were found in this definition's own body.

Explicit return expressions; different branches may return different objects:

```python
self.gaff2_dir / f'{self.name}.inpcrd'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def inpcrd_path(self) -> Path:
    return self.gaff2_dir / f"{self.name}.inpcrd"
```

</details>

<a id="definition-50"></a>

## `BenchmarkTarget.openmm_dir`

Source lines 50–51. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `property`.

```python
def openmm_dir(self) -> Path: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |

### How to read this implementation

No direct function calls were found in this definition's own body.

Explicit return expressions; different branches may return different objects:

```python
self.output_dir / 'openmm' / 'dry_polymer'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def openmm_dir(self) -> Path:
    return self.output_dir / "openmm" / "dry_polymer"
```

</details>

<a id="definition-54"></a>

## `BenchmarkTarget.gromacs_dir`

Source lines 54–55. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `property`.

```python
def gromacs_dir(self) -> Path: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |

### How to read this implementation

No direct function calls were found in this definition's own body.

Explicit return expressions; different branches may return different objects:

```python
self.output_dir / 'gromacs'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def gromacs_dir(self) -> Path:
    return self.output_dir / "gromacs"
```

</details>

<a id="definition-58"></a>

## `_find_sdf`

Source lines 58–69. Internal helper/protocol method.

```python
def _find_sdf(output_root: Path, system_name: str) -> Path | None: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| output_root | Path | required |
| system_name | str | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `candidate.exists`.

Explicit return expressions; different branches may return different objects:

```python
candidate
None
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _find_sdf(output_root: Path, system_name: str) -> Path | None:
    structures_root = output_root / "polymer_structures"
    candidates = (
        structures_root / f"{system_name}.sdf",
        structures_root / system_name / f"{system_name}.sdf",
        output_root / f"{system_name}.sdf",
        output_root / system_name / f"{system_name}.sdf",
    )
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None
```

</details>

<a id="definition-72"></a>

## `discover_targets`

Source lines 72–97. Named callable; inspect its callers before treating it as a stable public API.

```python
def discover_targets(system_names: tuple[str, ...], *, repo_root: Path=DEFAULT_REPO_ROOT) -> list[BenchmarkTarget]: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| system_names | tuple[str, ...] | required |
| repo_root (keyword-only) | Path | DEFAULT_REPO_ROOT |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `BenchmarkTarget`, `_find_sdf`, `print`, `targets.append`.

Explicit return expressions; different branches may return different objects:

```python
targets
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def discover_targets(
    system_names: tuple[str, ...],
    *,
    repo_root: Path = DEFAULT_REPO_ROOT,
) -> list[BenchmarkTarget]:
    output_root = repo_root / "examples" / "output"
    md_root = output_root / "benchmark"
    targets: list[BenchmarkTarget] = []

    for system_name in system_names:
        sdf_path = _find_sdf(output_root, system_name)
        if sdf_path is None:
            print(
                f"[{system_name}] missing SDF input under "
                f"{output_root / 'polymer_structures'}; skipping"
            )
            continue
        targets.append(
            BenchmarkTarget(
                name=system_name,
                sdf_path=sdf_path,
                output_dir=md_root / system_name,
            )
        )

    return targets
```

</details>

<a id="definition-100"></a>

## `selected_system_names`

Source lines 100–109. Named callable; inspect its callers before treating it as a stable public API.

```python
def selected_system_names(args: argparse.Namespace) -> tuple[str, ...]: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| args | argparse.Namespace | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `dict.fromkeys`, `names.extend`, `tuple`.

Explicit return expressions; different branches may return different objects:

```python
SYSTEMS
tuple(dict.fromkeys(names))
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def selected_system_names(args: argparse.Namespace) -> tuple[str, ...]:
    names: list[str] = []
    for option in (args.system, args.systems, args.target):
        if option:
            names.extend(option)

    if not names:
        return SYSTEMS

    return tuple(dict.fromkeys(names))
```

</details>

<a id="definition-112"></a>

## `_run_gaff2`

Source lines 112–142. Internal helper/protocol method.

```python
def _run_gaff2(target: BenchmarkTarget, *, charge_method: str, atom_count_warning_threshold: int | None, verbose: bool, reuse_existing_gaff2: bool) -> None: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| target | BenchmarkTarget | required |
| charge_method (keyword-only) | str | required |
| atom_count_warning_threshold (keyword-only) | int \| None | required |
| verbose (keyword-only) | bool | required |
| reuse_existing_gaff2 (keyword-only) | bool | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `parameterize_gaff2`, `print`, `target.inpcrd_path.exists`, `target.prmtop_path.exists`.

Explicit return expressions; different branches may return different objects:

```python
None
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _run_gaff2(
    target: BenchmarkTarget,
    *,
    charge_method: str,
    atom_count_warning_threshold: int | None,
    verbose: bool,
    reuse_existing_gaff2: bool,
) -> None:
    if (
        reuse_existing_gaff2
        and target.prmtop_path.exists()
        and target.inpcrd_path.exists()
    ):
        print(f"[{target.name}] reusing {target.prmtop_path}")
        print(f"[{target.name}] reusing {target.inpcrd_path}")
        return

    print(f"[{target.name}] GAFF2 parameterisation from {target.sdf_path}")
    outputs = parameterize_gaff2(
        target.sdf_path,
        target.gaff2_dir,
        name=target.name,
        net_charge=0,
        residue_name="PHA",
        charge_method=charge_method,
        atom_count_warning_threshold=atom_count_warning_threshold,
        verbose=verbose,
    )
    print(f"[{target.name}] wrote {outputs.prmtop_path}")
    print(f"[{target.name}] wrote {outputs.inpcrd_path}")
    print(f"[{target.name}] timings {outputs.timing_log}")
```

</details>

<a id="definition-145"></a>

## `_run_openmm`

Source lines 145–165. Internal helper/protocol method.

```python
def _run_openmm(target: BenchmarkTarget, *, minimization_iterations: int, nvt_steps: int, npt_steps: int, production_steps: int) -> None: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| target | BenchmarkTarget | required |
| minimization_iterations (keyword-only) | int | required |
| nvt_steps (keyword-only) | int | required |
| npt_steps (keyword-only) | int | required |
| production_steps (keyword-only) | int | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `print`, `run_openmm_with_amber_topology`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Calls worth inspecting for I/O, state changes or delegated execution: `run_openmm_with_amber_topology`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _run_openmm(
    target: BenchmarkTarget,
    *,
    minimization_iterations: int,
    nvt_steps: int,
    npt_steps: int,
    production_steps: int,
) -> None:
    print(f"[{target.name}] OpenMM dry-polymer MD")
    outputs = run_openmm_with_amber_topology(
        target.prmtop_path,
        target.inpcrd_path,
        target.openmm_dir,
        minimization_max_iterations=minimization_iterations,
        nvt_steps=nvt_steps,
        npt_steps=npt_steps,
        production_steps=production_steps,
    )
    print(f"[{target.name}] wrote {outputs.minimized_pdb_path}")
    print(f"[{target.name}] wrote {outputs.final_pdb_path}")
    print(f"[{target.name}] summary {outputs.summary_log_path}")
```

</details>

<a id="definition-168"></a>

## `_prepare_gromacs`

Source lines 168–190. Internal helper/protocol method.

```python
def _prepare_gromacs(target: BenchmarkTarget) -> None: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| target | BenchmarkTarget | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `prepare_gromacs_run_folder`, `print`, `write_gromacs_solvation_files`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Calls worth inspecting for I/O, state changes or delegated execution: `write_gromacs_solvation_files`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _prepare_gromacs(target: BenchmarkTarget) -> None:
    print(f"[{target.name}] GROMACS workflow folder preparation")
    outputs = prepare_gromacs_run_folder(
        target.prmtop_path,
        target.inpcrd_path,
        target.gromacs_dir,
        target.name,
    )
    print(f"[{target.name}] wrote {outputs.dry_polymer_dir}")
    print(f"[{target.name}] wrote {outputs.solvated_polymer_dir}")
    print(f"[{target.name}] wrote {outputs.charmm_gui_membrane_dir}")

    solvation_outputs = write_gromacs_solvation_files(
        outputs.solvated_polymer_dir,
        workflow_type="polymer",
        box_padding_nm=1.2,
        ion_concentration_molar=0.15,
        clean=True,
    )
    print(f"[{target.name}] wrote {solvation_outputs.solvate_script_path}")
    print(f"[{target.name}] wrote {solvation_outputs.ions_mdp_path}")
    for solvation_itp_path in solvation_outputs.solvation_itp_paths:
        print(f"[{target.name}] wrote {solvation_itp_path}")
```

</details>

<a id="definition-193"></a>

## `run_benchmark`

Source lines 193–255. Named callable; inspect its callers before treating it as a stable public API.

```python
def run_benchmark(args: argparse.Namespace) -> int: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| args | argparse.Namespace | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `_prepare_gromacs`, `_run_gaff2`, `_run_openmm`, `discover_targets`, `failures.append`, `openmm_available`, `print`, `selected_system_names`, `str`, `target.output_dir.mkdir`.

Explicit return expressions; different branches may return different objects:

```python
1
0
```

Calls worth inspecting for I/O, state changes or delegated execution: `_run_openmm`, `openmm_available`, `target.output_dir.mkdir`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def run_benchmark(args: argparse.Namespace) -> int:
    system_names = selected_system_names(args)
    charge_method = "gas" if args.skip_am1_bcc else args.charge_method
    atom_count_warning_threshold = (
        None
        if args.atom_count_warning_threshold <= 0
        else args.atom_count_warning_threshold
    )
    targets = discover_targets(system_names)

    if not targets:
        print("No benchmark inputs were found.")
        return 1

    can_run_openmm = openmm_available()
    if args.skip_openmm:
        can_run_openmm = False
    elif not can_run_openmm:
        print("OpenMM is not installed; dry-polymer MD will be skipped.")

    failures: list[tuple[str, str]] = []
    for target in targets:
        try:
            target.output_dir.mkdir(parents=True, exist_ok=True)
            _run_gaff2(
                target,
                charge_method=charge_method,
                atom_count_warning_threshold=atom_count_warning_threshold,
                verbose=not args.quiet_ambertools,
                reuse_existing_gaff2=args.reuse_existing_gaff2,
            )
            if can_run_openmm:
                _run_openmm(
                    target,
                    minimization_iterations=args.minimization_iterations,
                    nvt_steps=args.nvt_steps,
                    npt_steps=args.npt_steps,
                    production_steps=args.production_steps,
                )
            if args.prepare_gromacs:
                _prepare_gromacs(target)
        except (
            AmberToolsError,
            OpenMMRunnerError,
            ImportError,
            FileNotFoundError,
            ValueError,
        ) as exc:
            failures.append((target.name, str(exc)))
            print(f"[{target.name}] FAILED: {exc}")
            if args.stop_on_error:
                break

    if failures:
        print("\nFailures:")
        for system_name, message in failures:
            print(f"- {system_name}: {message}")
        return 1

    print("\nBenchmark workflow completed for:")
    for target in targets:
        print(f"- {target.name}: {target.output_dir}")
    return 0
```

</details>

<a id="definition-258"></a>

## `parse_args`

Source lines 258–353. Named callable; inspect its callers before treating it as a stable public API.

```python
def parse_args(argv: list[str] | None=None) -> argparse.Namespace: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| argv | list[str] \| None | None |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `argparse.ArgumentParser`, `parser.add_argument`, `parser.parse_args`.

Explicit return expressions; different branches may return different objects:

```python
parser.parse_args(argv)
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--system",
        action="append",
        choices=SYSTEMS,
        help=(
            "Run one system. May be passed more than once. Defaults to all six "
            "if no system option is provided."
        ),
    )
    parser.add_argument(
        "--systems",
        nargs="+",
        choices=SYSTEMS,
        help=(
            "Run one or more systems, for example --systems P3HB_4 P3HB_8. "
            "Defaults to all six if no system option is provided."
        ),
    )
    parser.add_argument(
        "--target",
        action="append",
        choices=SYSTEMS,
        help="Deprecated alias for --system.",
    )
    parser.add_argument(
        "--skip-openmm",
        action="store_true",
        help="Run GAFF2 parameterisation only.",
    )
    parser.add_argument(
        "--prepare-gromacs",
        action="store_true",
        help=(
            "Also prepare GROMACS dry, solvated, and CHARMM-GUI-style folders, "
            "including solvated_polymer solvation files."
        ),
    )
    parser.add_argument(
        "--reuse-existing-gaff2",
        action="store_true",
        help="Reuse existing prmtop/inpcrd files instead of rerunning AmberTools.",
    )
    parser.add_argument(
        "--charge-method",
        choices=CHARGE_METHODS,
        default="bcc",
        help="Charge method passed to antechamber.",
    )
    parser.add_argument(
        "--skip-am1-bcc",
        action="store_true",
        help="Shortcut for --charge-method gas.",
    )
    parser.add_argument(
        "--atom-count-warning-threshold",
        type=int,
        default=120,
        help="Warn when prepared molecules exceed this atom count. Use 0 to disable.",
    )
    parser.add_argument(
        "--quiet-ambertools",
        action="store_true",
        help="Do not print each AmberTools command before it runs.",
    )
    parser.add_argument(
        "--stop-on-error",
        action="store_true",
        help="Stop after the first system failure instead of reporting all failures.",
    )
    parser.add_argument(
        "--minimization-iterations",
        type=int,
        default=200,
        help="Maximum OpenMM minimization iterations.",
    )
    parser.add_argument(
        "--nvt-steps",
        type=int,
        default=100,
        help="OpenMM NVT equilibration steps.",
    )
    parser.add_argument(
        "--npt-steps",
        type=int,
        default=100,
        help="OpenMM NPT equilibration steps when box vectors are present.",
    )
    parser.add_argument(
        "--production-steps",
        type=int,
        default=100,
        help="OpenMM production steps.",
    )
    return parser.parse_args(argv)
```

</details>

<a id="definition-356"></a>

## `main`

Source lines 356–357. Named callable; inspect its callers before treating it as a stable public API.

```python
def main(argv: list[str] | None=None) -> None: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| argv | list[str] \| None | None |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `SystemExit`, `parse_args`, `run_benchmark`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
SystemExit(run_benchmark(parse_args(argv)))
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def main(argv: list[str] | None = None) -> None:
    raise SystemExit(run_benchmark(parse_args(argv)))
```

</details>
