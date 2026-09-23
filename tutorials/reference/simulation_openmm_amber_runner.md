# simulation_openmm_amber_runner.py

Earlier compact OpenMM validation route using Amber inputs. It orchestrates minimisation, NVT, periodic NPT where applicable, production and output summaries. It is not the newer OpenMMScriptBuilder/sw_openmm implementation. _temperature_schedule currently has no callers found in the inspected teaching/source routes.

[Current source](../../src/iphasimulator/simulation_openmm_amber_runner.py)

This page is generated from source syntax. Original docstrings can be incomplete or outdated; module notes above identify known discrepancies. Call/return/error lists describe direct syntax, not all behaviour inside callees. Read the source excerpt for branch order and effects. No scientific execution is implied.

Explicit functions/methods/nested helpers: **12**.

## Module imports

```python
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import time
```

## Classes and result records

### `OpenMMOutputs`

Files produced by an OpenMM AMBER-topology run.

Decorators: `dataclass(frozen=True)`.

Declared fields/defaults (instance state may also be set by methods):

```python
output_dir: Path
minimized_pdb_path: Path
trajectory_path: Path
state_xml_path: Path
log_path: Path
nvt_trajectory_path: Path
nvt_log_path: Path
npt_trajectory_path: Path
npt_log_path: Path
production_trajectory_path: Path
production_log_path: Path
final_pdb_path: Path
summary_log_path: Path
```

Dataclass-generated methods are implicit and are not counted as explicit function definitions.

### `OpenMMStageTimings`

Wall-clock timings for an OpenMM AMBER workflow.

Decorators: `dataclass(frozen=True)`.

Declared fields/defaults (instance state may also be set by methods):

```python
minimization_seconds: float
nvt_seconds: float
npt_seconds: float
production_seconds: float
```

Dataclass-generated methods are implicit and are not counted as explicit function definitions.

### `OpenMMRunnerError`

Raised when OpenMM is unavailable or simulation setup fails.

## Function map

- [`openmm_available` — source line 49](#definition-49)
- [`_platform` — source line 60](#definition-60)
- [`_simulation` — source line 72](#definition-72)
- [`_write_pdb` — source line 78](#definition-78)
- [`_append_stage_reporters` — source line 83](#definition-83)
- [`_run_stage` — source line 113](#definition-113)
- [`_write_summary` — source line 120](#definition-120)
- [`_temperature_schedule` — source line 135](#definition-135)
- [`run_openmm_with_amber_topology` — source line 159](#definition-159)
- [`run_openmm_with_amber_topology.create_system` — source line 219](#definition-219)
- [`run_openmm_with_amber_topology.create_integrator` — source line 234](#definition-234)
- [`run_openmm_with_amber_topology.set_initial_context` — source line 241](#definition-241)

<a id="definition-49"></a>

## `openmm_available`

Source lines 49–57. Named callable; inspect its callers before treating it as a stable public API.

```python
def openmm_available() -> bool: ...
```

### Purpose and original contract

Return True when OpenMM can be imported.

### Inputs

No explicit arguments.

### How to read this implementation

No direct function calls were found in this definition's own body.

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
def openmm_available() -> bool:
    """Return True when OpenMM can be imported."""

    try:
        import openmm  # noqa: F401
        import openmm.app  # noqa: F401
    except ImportError:
        return False
    return True
```

</details>

<a id="definition-60"></a>

## `_platform`

Source lines 60–69. Internal helper/protocol method.

```python
def _platform(mm, platform_name: str | None, precision: str | None): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| mm | not annotated | required |
| platform_name | str \| None | required |
| precision | str \| None | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `mm.Platform.getPlatformByName`, `platform.setPropertyDefaultValue`.

Explicit return expressions; different branches may return different objects:

```python
None
platform
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _platform(mm, platform_name: str | None, precision: str | None):
    if platform_name is None:
        return None
    platform = mm.Platform.getPlatformByName(platform_name)
    if precision is not None:
        try:
            platform.setPropertyDefaultValue("Precision", precision)
        except Exception:
            pass
    return platform
```

</details>

<a id="definition-72"></a>

## `_simulation`

Source lines 72–75. Internal helper/protocol method.

```python
def _simulation(app, topology, system, integrator, platform): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| app | not annotated | required |
| topology | not annotated | required |
| system | not annotated | required |
| integrator | not annotated | required |
| platform | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `app.Simulation`.

Explicit return expressions; different branches may return different objects:

```python
app.Simulation(topology, system, integrator)
app.Simulation(topology, system, integrator, platform)
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _simulation(app, topology, system, integrator, platform):
    if platform is None:
        return app.Simulation(topology, system, integrator)
    return app.Simulation(topology, system, integrator, platform)
```

</details>

<a id="definition-78"></a>

## `_write_pdb`

Source lines 78–80. Internal helper/protocol method.

```python
def _write_pdb(app, topology, positions, output_path: Path) -> None: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| app | not annotated | required |
| topology | not annotated | required |
| positions | not annotated | required |
| output_path | Path | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `app.PDBFile.writeFile`, `output_path.open`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Calls worth inspecting for I/O, state changes or delegated execution: `app.PDBFile.writeFile`, `output_path.open`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _write_pdb(app, topology, positions, output_path: Path) -> None:
    with output_path.open("w") as handle:
        app.PDBFile.writeFile(topology, positions, handle)
```

</details>

<a id="definition-83"></a>

## `_append_stage_reporters`

Source lines 83–110. Internal helper/protocol method.

```python
def _append_stage_reporters(app, simulation, trajectory_path: Path, log_path: Path, interval: int, *, total_steps: int, include_box_data: bool) -> None: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| app | not annotated | required |
| simulation | not annotated | required |
| trajectory_path | Path | required |
| log_path | Path | required |
| interval | int | required |
| total_steps (keyword-only) | int | required |
| include_box_data (keyword-only) | bool | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `app.DCDReporter`, `app.StateDataReporter`, `simulation.reporters.append`, `str`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _append_stage_reporters(
    app,
    simulation,
    trajectory_path: Path,
    log_path: Path,
    interval: int,
    *,
    total_steps: int,
    include_box_data: bool,
) -> None:
    simulation.reporters.append(app.DCDReporter(str(trajectory_path), interval))
    simulation.reporters.append(
        app.StateDataReporter(
            str(log_path),
            interval,
            step=True,
            potentialEnergy=True,
            kineticEnergy=True,
            totalEnergy=True,
            temperature=True,
            volume=include_box_data,
            density=include_box_data,
            speed=True,
            remainingTime=True,
            totalSteps=total_steps,
            separator=",",
        )
    )
```

</details>

<a id="definition-113"></a>

## `_run_stage`

Source lines 113–117. Internal helper/protocol method.

```python
def _run_stage(simulation, steps: int) -> float: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| simulation | not annotated | required |
| steps | int | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `simulation.step`, `time.perf_counter`.

Explicit return expressions; different branches may return different objects:

```python
time.perf_counter() - start
```

Calls worth inspecting for I/O, state changes or delegated execution: `simulation.step`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _run_stage(simulation, steps: int) -> float:
    start = time.perf_counter()
    if steps > 0:
        simulation.step(steps)
    return time.perf_counter() - start
```

</details>

<a id="definition-120"></a>

## `_write_summary`

Source lines 120–132. Internal helper/protocol method.

```python
def _write_summary(path: Path, *, timings: OpenMMStageTimings, npt_ran: bool) -> None: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| path | Path | required |
| timings (keyword-only) | OpenMMStageTimings | required |
| npt_ran (keyword-only) | bool | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `'\n'.join`, `path.write_text`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Calls worth inspecting for I/O, state changes or delegated execution: `path.write_text`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _write_summary(path: Path, *, timings: OpenMMStageTimings, npt_ran: bool) -> None:
    path.write_text(
        "\n".join(
            [
                f"minimization_seconds={timings.minimization_seconds:.3f}",
                f"nvt_seconds={timings.nvt_seconds:.3f}",
                f"npt_seconds={timings.npt_seconds:.3f}",
                f"production_seconds={timings.production_seconds:.3f}",
                f"npt_ran={npt_ran}",
                "",
            ]
        )
    )
```

</details>

<a id="definition-135"></a>

## `_temperature_schedule`

Source lines 135–156. Internal helper/protocol method.

```python
def _temperature_schedule(*, start_kelvin: float, target_kelvin: float, increment_kelvin: float) -> list[float]: ...
```

### Purpose and original contract

Return inclusive thermal-ramp temperatures.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| start_kelvin (keyword-only) | float | required |
| target_kelvin (keyword-only) | float | required |
| increment_kelvin (keyword-only) | float | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `temperatures.append`.

Explicit return expressions; different branches may return different objects:

```python
[start_kelvin]
temperatures
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('Temperature increment must be positive')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _temperature_schedule(
    *,
    start_kelvin: float,
    target_kelvin: float,
    increment_kelvin: float,
) -> list[float]:
    """Return inclusive thermal-ramp temperatures."""

    if increment_kelvin <= 0:
        raise ValueError("Temperature increment must be positive")
    if start_kelvin == target_kelvin:
        return [start_kelvin]

    direction = 1.0 if target_kelvin > start_kelvin else -1.0
    temperatures = [start_kelvin]
    current = start_kelvin
    while (current + direction * increment_kelvin - target_kelvin) * direction < 0:
        current += direction * increment_kelvin
        temperatures.append(current)
    if temperatures[-1] != target_kelvin:
        temperatures.append(target_kelvin)
    return temperatures
```

</details>

<a id="definition-159"></a>

## `run_openmm_with_amber_topology`

Source lines 159–364. Named callable; inspect its callers before treating it as a stable public API.

```python
def run_openmm_with_amber_topology(prmtop_path: str | Path, inpcrd_path: str | Path, output_dir: str | Path, *, temperature_kelvin: float=300.0, friction_per_picosecond: float=1.0, timestep_femtoseconds: float=2.0, minimization_max_iterations: int=200, simulation_steps: int=100, nvt_steps: int | None=None, npt_steps: int=100, production_steps: int=100, report_interval: int=10, pressure_bar: float=1.0, nonbonded_cutoff_nanometers: float=1.0, platform_name: str | None=None, platform_precision: str | None='mixed') -> OpenMMOutputs: ...
```

### Purpose and original contract

Run minimization, NVT, NPT when periodic, and production from AMBER files.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| prmtop_path | str \| Path | required |
| inpcrd_path | str \| Path | required |
| output_dir | str \| Path | required |
| temperature_kelvin (keyword-only) | float | 300.0 |
| friction_per_picosecond (keyword-only) | float | 1.0 |
| timestep_femtoseconds (keyword-only) | float | 2.0 |
| minimization_max_iterations (keyword-only) | int | 200 |
| simulation_steps (keyword-only) | int | 100 |
| nvt_steps (keyword-only) | int \| None | None |
| npt_steps (keyword-only) | int | 100 |
| production_steps (keyword-only) | int | 100 |
| report_interval (keyword-only) | int | 10 |
| pressure_bar (keyword-only) | float | 1.0 |
| nonbonded_cutoff_nanometers (keyword-only) | float | 1.0 |
| platform_name (keyword-only) | str \| None | None |
| platform_precision (keyword-only) | str \| None | 'mixed' |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `FileNotFoundError`, `OpenMMOutputs`, `OpenMMRunnerError`, `OpenMMStageTimings`, `Path`, `XmlSerializer.serialize`, `_append_stage_reporters`, `_platform`, `_run_stage`, `_simulation`, `_write_pdb`, `_write_summary`, `app.AmberInpcrdFile`, `app.AmberPrmtopFile`, `create_integrator`, `create_system`, `final_state.getPositions`, `inpcrd.exists`, `npt_log_path.write_text`, `npt_simulation.context.setPeriodicBoxVectors`, `npt_simulation.context.setPositions`, `npt_simulation.context.setVelocities`, `output_path.mkdir`, `prmtop.exists`, `production_simulation.context.getState`, `production_simulation.context.setPeriodicBoxVectors`, `production_simulation.context.setPositions`, `production_simulation.context.setVelocities`, `set_initial_context`, `simulation.context.getState`, `simulation.context.setVelocitiesToTemperature`, `simulation.minimizeEnergy`, `state.getPeriodicBoxVectors`, `state.getPositions`, `state.getVelocities`, `state_xml_path.write_text`, `str`, `time.perf_counter`.

Explicit return expressions; different branches may return different objects:

```python
OpenMMOutputs(output_dir=output_path, minimized_pdb_path=minimized_pdb_path, trajectory_path=trajectory_path, state_xml_path=state_xml_path, log_path=log_path, nvt_trajectory_path=nvt_trajectory_path, nvt_log_path=nvt_log_path, npt_trajectory_path=npt_trajectory_path, npt_log_path=npt_log_path, production_trajectory_path=production_trajectory_path, production_log_path=production_log_path, final_pd … [full expression below]
```

Calls worth inspecting for I/O, state changes or delegated execution: `OpenMMOutputs`, `OpenMMRunnerError`, `OpenMMStageTimings`, `_write_pdb`, `_write_summary`, `npt_log_path.write_text`, `output_path.mkdir`, `state_xml_path.write_text`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
OpenMMRunnerError('OpenMM is not installed. Install OpenMM before running Stage 2.')
FileNotFoundError(f'AMBER topology not found: {prmtop}')
FileNotFoundError(f'AMBER coordinates not found: {inpcrd}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def run_openmm_with_amber_topology(
    prmtop_path: str | Path,
    inpcrd_path: str | Path,
    output_dir: str | Path,
    *,
    temperature_kelvin: float = 300.0,
    friction_per_picosecond: float = 1.0,
    timestep_femtoseconds: float = 2.0,
    minimization_max_iterations: int = 200,
    simulation_steps: int = 100,
    nvt_steps: int | None = None,
    npt_steps: int = 100,
    production_steps: int = 100,
    report_interval: int = 10,
    pressure_bar: float = 1.0,
    nonbonded_cutoff_nanometers: float = 1.0,
    platform_name: str | None = None,
    platform_precision: str | None = "mixed",
) -> OpenMMOutputs:
    """Run minimization, NVT, NPT when periodic, and production from AMBER files."""

    try:
        import openmm as mm
        from openmm import app, unit
        from openmm import XmlSerializer
    except ImportError as exc:
        raise OpenMMRunnerError(
            "OpenMM is not installed. Install OpenMM before running Stage 2."
        ) from exc

    prmtop = Path(prmtop_path)
    inpcrd = Path(inpcrd_path)
    if not prmtop.exists():
        raise FileNotFoundError(f"AMBER topology not found: {prmtop}")
    if not inpcrd.exists():
        raise FileNotFoundError(f"AMBER coordinates not found: {inpcrd}")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    minimized_pdb_path = output_path / "minimized.pdb"
    trajectory_path = output_path / "production.dcd"
    state_xml_path = output_path / "state.xml"
    log_path = output_path / "production.log"
    nvt_trajectory_path = output_path / "nvt.dcd"
    nvt_log_path = output_path / "nvt.log"
    npt_trajectory_path = output_path / "npt.dcd"
    npt_log_path = output_path / "npt.log"
    production_trajectory_path = output_path / "production.dcd"
    production_log_path = output_path / "production.log"
    final_pdb_path = output_path / "final.pdb"
    summary_log_path = output_path / "openmm_summary.log"

    amber_prmtop = app.AmberPrmtopFile(str(prmtop))
    amber_inpcrd = app.AmberInpcrdFile(str(inpcrd))
    is_periodic = amber_inpcrd.boxVectors is not None
    nonbonded_method = app.PME if is_periodic else app.NoCutoff
    nvt_steps = simulation_steps if nvt_steps is None else nvt_steps
    platform = _platform(mm, platform_name, platform_precision)

    def create_system(*, with_barostat: bool):
        system = amber_prmtop.createSystem(
            nonbondedMethod=nonbonded_method,
            nonbondedCutoff=nonbonded_cutoff_nanometers * unit.nanometers,
            constraints=app.HBonds,
        )
        if with_barostat:
            system.addForce(
                mm.MonteCarloBarostat(
                    pressure_bar * unit.bar,
                    temperature_kelvin * unit.kelvin,
                )
            )
        return system

    def create_integrator():
        return mm.LangevinMiddleIntegrator(
            temperature_kelvin * unit.kelvin,
            friction_per_picosecond / unit.picosecond,
            timestep_femtoseconds * unit.femtoseconds,
        )

    def set_initial_context(simulation) -> None:
        if is_periodic:
            simulation.context.setPeriodicBoxVectors(*amber_inpcrd.boxVectors)
        simulation.context.setPositions(amber_inpcrd.positions)

    simulation = _simulation(
        app,
        amber_prmtop.topology,
        create_system(with_barostat=False),
        create_integrator(),
        platform,
    )
    set_initial_context(simulation)
    min_start = time.perf_counter()
    simulation.minimizeEnergy(maxIterations=minimization_max_iterations)
    minimization_seconds = time.perf_counter() - min_start
    state = simulation.context.getState(getPositions=True, getEnergy=True)
    _write_pdb(app, amber_prmtop.topology, state.getPositions(), minimized_pdb_path)

    simulation.context.setVelocitiesToTemperature(temperature_kelvin * unit.kelvin)
    _append_stage_reporters(
        app,
        simulation,
        nvt_trajectory_path,
        nvt_log_path,
        report_interval,
        total_steps=nvt_steps,
        include_box_data=is_periodic,
    )
    nvt_seconds = _run_stage(simulation, nvt_steps)

    state = simulation.context.getState(getPositions=True, getVelocities=True, getEnergy=True)
    positions = state.getPositions()
    velocities = state.getVelocities()
    box_vectors = state.getPeriodicBoxVectors() if is_periodic else None

    npt_ran = is_periodic and npt_steps > 0
    if npt_ran:
        npt_simulation = _simulation(
            app,
            amber_prmtop.topology,
            create_system(with_barostat=True),
            create_integrator(),
            platform,
        )
        npt_simulation.context.setPeriodicBoxVectors(*box_vectors)
        npt_simulation.context.setPositions(positions)
        npt_simulation.context.setVelocities(velocities)
        _append_stage_reporters(
            app,
            npt_simulation,
            npt_trajectory_path,
            npt_log_path,
            report_interval,
            total_steps=npt_steps,
            include_box_data=True,
        )
        npt_seconds = _run_stage(npt_simulation, npt_steps)
        simulation = npt_simulation
        state = simulation.context.getState(getPositions=True, getVelocities=True, getEnergy=True)
        positions = state.getPositions()
        velocities = state.getVelocities()
        box_vectors = state.getPeriodicBoxVectors()
    else:
        npt_seconds = 0.0
        npt_log_path.write_text(
            "NPT skipped: AMBER coordinates do not contain periodic box vectors.\n"
            if not is_periodic
            else "NPT skipped: npt_steps is 0.\n"
        )

    production_simulation = _simulation(
        app,
        amber_prmtop.topology,
        create_system(with_barostat=is_periodic),
        create_integrator(),
        platform,
    )
    if is_periodic:
        production_simulation.context.setPeriodicBoxVectors(*box_vectors)
    production_simulation.context.setPositions(positions)
    production_simulation.context.setVelocities(velocities)
    _append_stage_reporters(
        app,
        production_simulation,
        production_trajectory_path,
        production_log_path,
        report_interval,
        total_steps=production_steps,
        include_box_data=is_periodic,
    )
    production_seconds = _run_stage(production_simulation, production_steps)

    final_state = production_simulation.context.getState(
        getPositions=True,
        getVelocities=True,
        getEnergy=True,
    )
    _write_pdb(app, amber_prmtop.topology, final_state.getPositions(), final_pdb_path)
    state_xml_path.write_text(XmlSerializer.serialize(final_state))

    timings = OpenMMStageTimings(
        minimization_seconds=minimization_seconds,
        nvt_seconds=nvt_seconds,
        npt_seconds=npt_seconds,
        production_seconds=production_seconds,
    )
    _write_summary(summary_log_path, timings=timings, npt_ran=npt_ran)

    return OpenMMOutputs(
        output_dir=output_path,
        minimized_pdb_path=minimized_pdb_path,
        trajectory_path=trajectory_path,
        state_xml_path=state_xml_path,
        log_path=log_path,
        nvt_trajectory_path=nvt_trajectory_path,
        nvt_log_path=nvt_log_path,
        npt_trajectory_path=npt_trajectory_path,
        npt_log_path=npt_log_path,
        production_trajectory_path=production_trajectory_path,
        production_log_path=production_log_path,
        final_pdb_path=final_pdb_path,
        summary_log_path=summary_log_path,
    )
```

</details>

<a id="definition-219"></a>

## `run_openmm_with_amber_topology.create_system`

Source lines 219–232. Named callable; inspect its callers before treating it as a stable public API.

```python
def create_system(*, with_barostat: bool): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| with_barostat (keyword-only) | bool | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `amber_prmtop.createSystem`, `mm.MonteCarloBarostat`, `system.addForce`.

Explicit return expressions; different branches may return different objects:

```python
system
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def create_system(*, with_barostat: bool):
    system = amber_prmtop.createSystem(
        nonbondedMethod=nonbonded_method,
        nonbondedCutoff=nonbonded_cutoff_nanometers * unit.nanometers,
        constraints=app.HBonds,
    )
    if with_barostat:
        system.addForce(
            mm.MonteCarloBarostat(
                pressure_bar * unit.bar,
                temperature_kelvin * unit.kelvin,
            )
        )
    return system
```

</details>

<a id="definition-234"></a>

## `run_openmm_with_amber_topology.create_integrator`

Source lines 234–239. Named callable; inspect its callers before treating it as a stable public API.

```python
def create_integrator(): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

No explicit arguments.

### How to read this implementation

Direct calls (sorted inventory, not execution order): `mm.LangevinMiddleIntegrator`.

Explicit return expressions; different branches may return different objects:

```python
mm.LangevinMiddleIntegrator(temperature_kelvin * unit.kelvin, friction_per_picosecond / unit.picosecond, timestep_femtoseconds * unit.femtoseconds)
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def create_integrator():
    return mm.LangevinMiddleIntegrator(
        temperature_kelvin * unit.kelvin,
        friction_per_picosecond / unit.picosecond,
        timestep_femtoseconds * unit.femtoseconds,
    )
```

</details>

<a id="definition-241"></a>

## `run_openmm_with_amber_topology.set_initial_context`

Source lines 241–244. Named callable; inspect its callers before treating it as a stable public API.

```python
def set_initial_context(simulation) -> None: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| simulation | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `simulation.context.setPeriodicBoxVectors`, `simulation.context.setPositions`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def set_initial_context(simulation) -> None:
    if is_periodic:
        simulation.context.setPeriodicBoxVectors(*amber_inpcrd.boxVectors)
    simulation.context.setPositions(amber_inpcrd.positions)
```

</details>
