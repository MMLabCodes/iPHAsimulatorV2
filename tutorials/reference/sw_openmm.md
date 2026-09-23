# sw_openmm.py

OpenMM engine implementation for Amber and GROMACS input formats. BuildSimulation owns platform/system/context creation, simulation stages, reporting, restart output and graphing. Read state transfer between stages explicitly. Restart/default-output paths still reference manager.systems_dir, which the current PHAFileManager does not expose.

[Current source](../../src/iphasimulator/sw_openmm.py)

This page is generated from source syntax. Original docstrings can be incomplete or outdated; module notes above identify known discrepancies. Call/return/error lists describe direct syntax, not all behaviour inside callees. Read the source excerpt for branch order and effects. No scientific execution is implied.

Explicit functions/methods/nested helpers: **40**.

## Module imports

```python
import os
import time
import shutil
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import parmed as pmd
import openmm
import openmm.app as app
from openmm import *
from openmm.app import *
from openmm.unit import *
```

## Classes and result records

### `DcdWriter`

Write DCD trajectory files for OpenMM simulations.

### `DataWriter`

Write OpenMM state data to a comma-separated text file.

### `BuildSimulation`

Parent class for OpenMM simulations.

Child classes:

    AmberSimulation

    GromacsSimulation

Declared fields/defaults (instance state may also be set by methods):

```python
savepdb_traj = False
pressure = 1
temp = 300
min_temp = 0
timestep = 2.0
friction_coeff = 1.0
total_steps = 1000
reporter_freq = 1000
nonbondedcutoff = 1.0
timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
anneal_parameters = [300, 700, 5, 10, 500000]
minimized_only = None
restrain_heavys = False
```

### `GromacsSimulation`

OpenMM simulation using GROMACS topology and coordinate files.

### `AmberSimulation`

OpenMM simulation using AMBER topology and coordinate files.

## Function map

- [`DcdWriter.__init__` — source line 23](#definition-23)
- [`DataWriter.__init__` — source line 34](#definition-34)
- [`BuildSimulation.__init__` — source line 94](#definition-94)
- [`BuildSimulation.type_of_simulation` — source line 135](#definition-135)
- [`BuildSimulation.get_platform` — source line 147](#definition-147)
- [`BuildSimulation.get_platform.configure_platform` — source line 195](#definition-195)
- [`BuildSimulation.create_openmm_system` — source line 286](#definition-286)
- [`BuildSimulation.create_openmm_simulation` — source line 328](#definition-328)
- [`BuildSimulation.minimize_energy` — source line 356](#definition-356)
- [`BuildSimulation.minimize_energy_help` — source line 416](#definition-416)
- [`BuildSimulation.anneal_NVT` — source line 419](#definition-419)
- [`BuildSimulation.anneal_NVT.cycle` — source line 556](#definition-556)
- [`BuildSimulation.anneal_help` — source line 637](#definition-637)
- [`BuildSimulation.basic_NPT` — source line 642](#definition-642)
- [`BuildSimulation.basic_NPT_help` — source line 820](#definition-820)
- [`BuildSimulation.basic_NVT` — source line 825](#definition-825)
- [`BuildSimulation.thermal_ramp` — source line 981](#definition-981)
- [`BuildSimulation.save_rst` — source line 1199](#definition-1199)
- [`BuildSimulation.restrain_heavy_atoms` — source line 1261](#definition-1261)
- [`BuildSimulation.__repr__` — source line 1292](#definition-1292)
- [`BuildSimulation.__str__` — source line 1317](#definition-1317)
- [`BuildSimulation.display_start_time` — source line 1321](#definition-1321)
- [`BuildSimulation.savepdb_trajectories` — source line 1328](#definition-1328)
- [`BuildSimulation.set_temperature` — source line 1346](#definition-1346)
- [`BuildSimulation.set_pressure` — source line 1356](#definition-1356)
- [`BuildSimulation.set_timestep` — source line 1366](#definition-1366)
- [`BuildSimulation.set_friction_coeff` — source line 1375](#definition-1375)
- [`BuildSimulation.set_total_steps` — source line 1384](#definition-1384)
- [`BuildSimulation.set_reporter_freq` — source line 1393](#definition-1393)
- [`BuildSimulation.set_nonbondedcutoff` — source line 1403](#definition-1403)
- [`BuildSimulation.set_anneal_parameters` — source line 1417](#definition-1417)
- [`BuildSimulation.set_anneal_parameters_help` — source line 1438](#definition-1438)
- [`BuildSimulation.graph_state_data` — source line 1442](#definition-1442)
- [`BuildSimulation.graph_state_data_help` — source line 1516](#definition-1516)
- [`GromacsSimulation.__new__` — source line 1528](#definition-1528)
- [`GromacsSimulation.__init__` — source line 1552](#definition-1552)
- [`GromacsSimulation.__str__` — source line 1602](#definition-1602)
- [`AmberSimulation.__new__` — source line 1612](#definition-1612)
- [`AmberSimulation.__init__` — source line 1626](#definition-1626)
- [`AmberSimulation.__str__` — source line 1657](#definition-1657)

<a id="definition-23"></a>

## `DcdWriter.__init__`

Source lines 23–28. Internal helper/protocol method.

```python
def __init__(self, prefix, freq): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| prefix | not annotated | required |
| freq | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `app.DCDReporter`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Instance/class attributes assigned directly: `self.dcdReporter`.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def __init__(self, prefix, freq):
    self.dcdReporter = app.DCDReporter(
        f"{prefix}.dcd",
        freq,
        enforcePeriodicBox=True,
    )
```

</details>

<a id="definition-34"></a>

## `DataWriter.__init__`

Source lines 34–51. Internal helper/protocol method.

```python
def __init__(self, prefix, freq, steps): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| prefix | not annotated | required |
| freq | not annotated | required |
| steps | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `app.StateDataReporter`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Instance/class attributes assigned directly: `self.stateDataReporter`.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def __init__(self, prefix, freq, steps):
    self.stateDataReporter = app.StateDataReporter(
        f"{prefix}.txt",
        freq,
        totalSteps=steps,
        step=True,
        time=True,
        speed=True,
        progress=True,
        elapsedTime=True,
        totalEnergy=True,
        kineticEnergy=True,
        potentialEnergy=True,
        temperature=True,
        volume=True,
        density=True,
        separator=",",
    )
```

</details>

<a id="definition-94"></a>

## `BuildSimulation.__init__`

Source lines 94–133. Internal helper/protocol method.

```python
def __init__(self, manager, filename, output_dir=None): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| manager | not annotated | required |
| filename | not annotated | required |
| output_dir | not annotated | None |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `os.makedirs`, `os.path.basename`, `os.path.join`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Instance/class attributes assigned directly: `self.filename`, `self.manager`, `self.output_dir`, `self.run_name`.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def __init__(

    self,

    manager,

    filename,

    output_dir=None,

):

    self.manager = manager

    self.filename = filename

    if output_dir is None:

        self.output_dir = os.path.join(

            self.manager.systems_dir,

            self.filename,

            self.timestamp,

        )


    else:

        self.output_dir = output_dir
    self.run_name = os.path.basename(self.output_dir)       
    os.makedirs(

        self.output_dir,

        exist_ok=True,

    )
```

</details>

<a id="definition-135"></a>

## `BuildSimulation.type_of_simulation`

Source lines 135–145. Named callable; inspect its callers before treating it as a stable public API.

```python
def type_of_simulation(self): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `isinstance`.

Explicit return expressions; different branches may return different objects:

```python
'AMB'
'GRO'
'UNKNOWN'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def type_of_simulation(self):

    if isinstance(self, AmberSimulation):

        return "AMB"

    if isinstance(self, GromacsSimulation):

        return "GRO"

    return "UNKNOWN"
```

</details>

<a id="definition-147"></a>

## `BuildSimulation.get_platform`

Source lines 147–284. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_platform(self, platform_name=None): ...
```

### Purpose and original contract

Select and configure the OpenMM platform.

Priority
--------
1. Explicit platform_name argument.
2. IPHA_OPENMM_PLATFORM environment variable.
3. CUDA.
4. OpenCL.
5. CPU.

Precision
---------
CUDA
    Mixed precision.

OpenCL
    Single precision.

CPU
    OpenMM default precision.

Parameters
----------
platform_name : str, optional
    Explicit OpenMM platform to use.

Returns
-------
openmm.Platform
    Configured OpenMM platform.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| platform_name | not annotated | None |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `Platform.getPlatformByName`, `RuntimeError`, `configure_platform`, `os.environ.get`, `print`.

Explicit return expressions; different branches may return different objects:

```python
platform
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
RuntimeError('No usable OpenMM platform was found.')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_platform(self, platform_name=None):
    """
    Select and configure the OpenMM platform.

    Priority
    --------
    1. Explicit platform_name argument.
    2. IPHA_OPENMM_PLATFORM environment variable.
    3. CUDA.
    4. OpenCL.
    5. CPU.

    Precision
    ---------
    CUDA
        Mixed precision.

    OpenCL
        Single precision.

    CPU
        OpenMM default precision.

    Parameters
    ----------
    platform_name : str, optional
        Explicit OpenMM platform to use.

    Returns
    -------
    openmm.Platform
        Configured OpenMM platform.
    """

    import os
    from openmm import Platform

    requested_platform = (
        platform_name
        or os.environ.get(
            "IPHA_OPENMM_PLATFORM"
        )
    )

    # ---------------------------------------------------------
    # Helper for platform-specific configuration
    # ---------------------------------------------------------

    def configure_platform(
        platform,
        name,
    ):

        if name == "CUDA":

            platform.setPropertyDefaultValue(
                "Precision",
                "mixed",
            )

            print(
                "CUDA precision: mixed"
            )

        elif name == "OpenCL":

            platform.setPropertyDefaultValue(
                "Precision",
                "single",
            )

            print(
                "OpenCL precision: single"
            )

        return platform

    # ---------------------------------------------------------
    # Explicitly requested platform
    # ---------------------------------------------------------

    if requested_platform is not None:

        platform = Platform.getPlatformByName(
            requested_platform
        )

        platform = configure_platform(
            platform,
            requested_platform,
        )

        print(
            f"Using requested platform: "
            f"{requested_platform}"
        )

        return platform

    # ---------------------------------------------------------
    # Automatic platform selection
    # ---------------------------------------------------------

    for candidate in [
        "CUDA",
        "OpenCL",
        "CPU",
    ]:

        try:

            platform = (
                Platform.getPlatformByName(
                    candidate
                )
            )

            platform = configure_platform(
                platform,
                candidate,
            )

            print(
                f"Using {candidate} platform."
            )

            return platform

        except Exception:
            continue

    # ---------------------------------------------------------
    # Nothing worked
    # ---------------------------------------------------------

    raise RuntimeError(
        "No usable OpenMM platform was found."
    )
```

</details>

<a id="definition-195"></a>

## `BuildSimulation.get_platform.configure_platform`

Source lines 195–222. Named callable; inspect its callers before treating it as a stable public API.

```python
def configure_platform(platform, name): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| platform | not annotated | required |
| name | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `platform.setPropertyDefaultValue`, `print`.

Explicit return expressions; different branches may return different objects:

```python
platform
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def configure_platform(
    platform,
    name,
):

    if name == "CUDA":

        platform.setPropertyDefaultValue(
            "Precision",
            "mixed",
        )

        print(
            "CUDA precision: mixed"
        )

    elif name == "OpenCL":

        platform.setPropertyDefaultValue(
            "Precision",
            "single",
        )

        print(
            "OpenCL precision: single"
        )

    return platform
```

</details>

<a id="definition-286"></a>

## `BuildSimulation.create_openmm_system`

Source lines 286–326. Named callable; inspect its callers before treating it as a stable public API.

```python
def create_openmm_system(self, ensemble='NVT', temp=None, pressure=None): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| ensemble | not annotated | 'NVT' |
| temp | not annotated | None |
| pressure | not annotated | None |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `MonteCarloBarostat`, `ValueError`, `self.amb_topology.createSystem`, `self.gro_topology.createSystem`, `self.type_of_simulation`, `system.addForce`.

Explicit return expressions; different branches may return different objects:

```python
system
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('Simulation type must be AmberSimulation or GromacsSimulation.')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def create_openmm_system(
    self,
    ensemble="NVT",
    temp=None,
    pressure=None,
):
    if temp is None:
        temp = self.temp

    if pressure is None:
        pressure = self.pressure

    sim_type = self.type_of_simulation()

    if sim_type == "AMB":
        system = self.amb_topology.createSystem(
            nonbondedMethod=app.PME,
            nonbondedCutoff=self.nonbondedcutoff * nanometers,
            constraints=app.HBonds,
        )

    elif sim_type == "GRO":
        system = self.gro_topology.createSystem(
            nonbondedMethod=app.PME,
            nonbondedCutoff=self.nonbondedcutoff * nanometers,
            constraints=app.HBonds,
        )

    else:
        raise ValueError(
            "Simulation type must be AmberSimulation or GromacsSimulation."
        )

    if ensemble == "NPT":
        barostat = MonteCarloBarostat(
            pressure * atmosphere,
            temp * kelvin,
        )
        system.addForce(barostat)

    return system
```

</details>

<a id="definition-328"></a>

## `BuildSimulation.create_openmm_simulation`

Source lines 328–354. Named callable; inspect its callers before treating it as a stable public API.

```python
def create_openmm_simulation(self, system, integrator, platform): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| system | not annotated | required |
| integrator | not annotated | required |
| platform | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `app.Simulation`, `self.type_of_simulation`.

Explicit return expressions; different branches may return different objects:

```python
app.Simulation(self.amb_topology.topology, system, integrator, platform)
app.Simulation(self.gro_topology.topology, system, integrator, platform)
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('Simulation type must be AmberSimulation or GromacsSimulation.')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def create_openmm_simulation(
    self,
    system,
    integrator,
    platform,
):
    sim_type = self.type_of_simulation()

    if sim_type == "AMB":
        return app.Simulation(
            self.amb_topology.topology,
            system,
            integrator,
            platform,
        )

    if sim_type == "GRO":
        return app.Simulation(
            self.gro_topology.topology,
            system,
            integrator,
            platform,
        )

    raise ValueError(
        "Simulation type must be AmberSimulation or GromacsSimulation."
    )
```

</details>

<a id="definition-356"></a>

## `BuildSimulation.minimize_energy`

Source lines 356–413. Named callable; inspect its callers before treating it as a stable public API.

```python
def minimize_energy(self): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `LangevinIntegrator`, `PDBFile.writeFile`, `len`, `open`, `os.path.join`, `print`, `self.create_openmm_simulation`, `self.create_openmm_system`, `self.get_platform`, `self.gro_topology.topology.getNumAtoms`, `self.type_of_simulation`, `simulation.context.getState`, `simulation.context.setPositions`, `simulation.minimizeEnergy`, `state.getPositions`, `time.time`.

Explicit return expressions; different branches may return different objects:

```python
simulation
```

Instance/class attributes assigned directly: `self.min_pdbname`.

Calls worth inspecting for I/O, state changes or delegated execution: `PDBFile.writeFile`, `open`, `self.create_openmm_simulation`, `self.create_openmm_system`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def minimize_energy(self):
    min_start_time = time.time()

    integrator = LangevinIntegrator(
        self.min_temp * kelvin,
        self.friction_coeff / picoseconds,
        self.timestep * femtoseconds,
    )

    platform = self.get_platform()

    system = self.create_openmm_system(
        ensemble="NVT",
        temp=self.min_temp,
    )

    simulation = self.create_openmm_simulation(
        system,
        integrator,
        platform,
    )

    if self.type_of_simulation() == "AMB":
        simulation.context.setPositions(
            self.amb_coordinates.positions
        )

    elif self.type_of_simulation() == "GRO":
        print("Atoms in GRO:", len(self.gro_coordinates.positions))
        print("Atoms in TOP:", self.gro_topology.topology.getNumAtoms())

        simulation.context.setPositions(
            self.gro_coordinates.positions
        )

    simulation.minimizeEnergy()

    state = simulation.context.getState(
        getPositions=True,
        getEnergy=True,
    )

    self.min_pdbname = os.path.join(
        self.output_dir,
        f"min_{self.filename}.pdb",
    )

    with open(self.min_pdbname, "w") as output:
        PDBFile.writeFile(
            simulation.topology,
            state.getPositions(),
            output,
        )

    time_taken = time.time() - min_start_time
    print(f"Minimization completed in {time_taken:.2f} seconds.")

    return simulation
```

</details>

<a id="definition-416"></a>

## `BuildSimulation.minimize_energy_help`

Source lines 416–417. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `classmethod`.

```python
def minimize_energy_help(cls): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| cls | not annotated | bound instance/class |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `print`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def minimize_energy_help(cls):
    print(cls.minimize_energy.__doc__)
```

</details>

<a id="definition-419"></a>

## `BuildSimulation.anneal_NVT`

Source lines 419–634. Named callable; inspect its callers before treating it as a stable public API.

```python
def anneal_NVT(self, simulation, start_temp=None, max_temp=None, cycles=None, quench_rate=None, steps_per_cycle=None, filename=None, save_restart=False, restart_name=None, verbose=True): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| simulation | not annotated | required |
| start_temp | not annotated | None |
| max_temp | not annotated | None |
| cycles | not annotated | None |
| quench_rate | not annotated | None |
| steps_per_cycle | not annotated | None |
| filename | not annotated | None |
| save_restart | not annotated | False |
| restart_name | not annotated | None |
| verbose | not annotated | True |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `DataWriter`, `DcdWriter`, `LangevinIntegrator`, `PDBFile.writeFile`, `app.PDBReporter`, `cycle`, `final_state.getPositions`, `int`, `open`, `os.path.join`, `print`, `range`, `self.create_openmm_simulation`, `self.create_openmm_system`, `self.get_platform`, `self.save_rst`, `simulation.context.getState`, `simulation.context.setPeriodicBoxVectors`, `simulation.context.setPositions`, `simulation.reporters.append`, `state.getPeriodicBoxVectors`, `state.getPositions`, `time.time`.

Explicit return expressions; different branches may return different objects:

```python
(simulation, output_dataname + '.txt')
```

Instance/class attributes assigned directly: `self.final_pdbname`.

Calls worth inspecting for I/O, state changes or delegated execution: `DataWriter`, `DcdWriter`, `PDBFile.writeFile`, `open`, `self.create_openmm_simulation`, `self.create_openmm_system`, `self.save_rst`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def anneal_NVT(
    self,
    simulation,
    start_temp=None,
    max_temp=None,
    cycles=None,
    quench_rate=None,
    steps_per_cycle=None,
    filename=None,
    save_restart=False,
    restart_name=None,
    verbose=True,
):
    anneal_start_time = time.time()

    if filename is None:
        filename = "_anneal_"
    else:
        filename = f"_{filename}_"

    if start_temp is None:
        start_temp = self.anneal_parameters[0]

    if max_temp is None:
        max_temp = self.anneal_parameters[1]

    if cycles is None:
        cycles = self.anneal_parameters[2]

    if quench_rate is None:
        quench_rate = self.anneal_parameters[3]

    if steps_per_cycle is None:
        steps_per_cycle = self.anneal_parameters[4]

    state = simulation.context.getState(
        getPositions=True,
        getEnergy=True,
        enforcePeriodicBox=True,
    )

    xyz = state.getPositions()
    vx, vy, vz = state.getPeriodicBoxVectors()

    integrator = LangevinIntegrator(
        start_temp * kelvin,
        self.friction_coeff / picoseconds,
        self.timestep * femtoseconds,
    )

    platform = self.get_platform()

    system = self.create_openmm_system(
        ensemble="NVT",
        temp=start_temp,
    )

    simulation = self.create_openmm_simulation(
        system,
        integrator,
        platform,
    )

    simulation.context.setPeriodicBoxVectors(vx, vy, vz)
    simulation.context.setPositions(xyz)

    total_steps = steps_per_cycle * cycles

    if self.savepdb_traj is True:
        output_pdbname = os.path.join(
            self.output_dir,
            self.filename + filename + self.run_name + ".pdb",
        )

        simulation.reporters.append(
            app.PDBReporter(
                output_pdbname,
                self.reporter_freq,
            )
        )

    output_dcdname = os.path.join(
        self.output_dir,
        self.filename + filename + self.run_name,
    )

    dcdWriter = DcdWriter(
        output_dcdname,
        self.reporter_freq,
    )

    simulation.reporters.append(
        dcdWriter.dcdReporter
    )

    output_dataname = os.path.join(
        self.output_dir,
        self.filename + filename + self.run_name,
    )

    dataWriter = DataWriter(
        output_dataname,
        self.reporter_freq,
        total_steps,
    )

    simulation.reporters.append(
        dataWriter.stateDataReporter
    )

    increments = int(
        (max_temp - start_temp) / quench_rate
    )

    steps_per_slope = int(
        steps_per_cycle * 0.4
    )

    holding_steps = int(
        steps_per_cycle * 0.1
    )

    steps_at_increment = int(
        steps_per_slope / increments
    )

    if verbose is True:
        print(
            f"""Annealing information:
             - Number of heating/cooling increments: {increments}
             - Steps per temperature in-/decrease: {steps_per_slope}
             - Holding steps at {max_temp} K: {holding_steps}
             - Steps at heating/cooling increment: {steps_at_increment}
             - Total simulation time {(total_steps * self.timestep):.0f} fs
            """
        )

    def cycle():
        integrator.setTemperature(
            start_temp * kelvin
        )

        simulation.step(
            steps_at_increment
        )

        for i in range(increments):
            integrator.setTemperature(
                (start_temp + i * quench_rate) * kelvin
            )

            simulation.step(
                steps_at_increment
            )

        integrator.setTemperature(
            max_temp * kelvin
        )

        simulation.step(
            holding_steps
        )

        for i in range(increments):
            integrator.setTemperature(
                (max_temp - i * quench_rate) * kelvin
            )

            simulation.step(
                steps_at_increment
            )

        integrator.setTemperature(
            start_temp * kelvin
        )

        simulation.step(
            holding_steps
        )

    for _ in range(cycles):
        cycle()

    time_taken = time.time() - anneal_start_time

    print(
        f"Annealing completed in {time_taken:.2f} seconds."
    )

    final_state = simulation.context.getState(
        getPositions=True,
        getEnergy=True,
    )

    self.final_pdbname = os.path.join(
        self.output_dir,
        "final" + filename + self.filename + ".pdb",
    )

    with open(
        self.final_pdbname,
        "w",
    ) as output:
        PDBFile.writeFile(
            simulation.topology,
            final_state.getPositions(),
            output,
        )

    if save_restart is True:
        self.save_rst(
            simulation,
            restart_name=restart_name,
        )

    return simulation, output_dataname + ".txt"
```

</details>

<a id="definition-556"></a>

## `BuildSimulation.anneal_NVT.cycle`

Source lines 556–597. Named callable; inspect its callers before treating it as a stable public API.

```python
def cycle(): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

No explicit arguments.

### How to read this implementation

Direct calls (sorted inventory, not execution order): `integrator.setTemperature`, `range`, `simulation.step`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Calls worth inspecting for I/O, state changes or delegated execution: `simulation.step`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def cycle():
    integrator.setTemperature(
        start_temp * kelvin
    )

    simulation.step(
        steps_at_increment
    )

    for i in range(increments):
        integrator.setTemperature(
            (start_temp + i * quench_rate) * kelvin
        )

        simulation.step(
            steps_at_increment
        )

    integrator.setTemperature(
        max_temp * kelvin
    )

    simulation.step(
        holding_steps
    )

    for i in range(increments):
        integrator.setTemperature(
            (max_temp - i * quench_rate) * kelvin
        )

        simulation.step(
            steps_at_increment
        )

    integrator.setTemperature(
        start_temp * kelvin
    )

    simulation.step(
        holding_steps
    )
```

</details>

<a id="definition-637"></a>

## `BuildSimulation.anneal_help`

Source lines 637–640. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `classmethod`.

```python
def anneal_help(cls): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| cls | not annotated | bound instance/class |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `print`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def anneal_help(cls):
    print(
        cls.anneal_NVT.__doc__
    )
```

</details>

<a id="definition-642"></a>

## `BuildSimulation.basic_NPT`

Source lines 642–817. Named callable; inspect its callers before treating it as a stable public API.

```python
def basic_NPT(self, simulation, total_steps=None, temp=None, pressure=None, filename=None, save_restart=False, restart_name=None, verbose=True): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| simulation | not annotated | required |
| total_steps | not annotated | None |
| temp | not annotated | None |
| pressure | not annotated | None |
| filename | not annotated | None |
| save_restart | not annotated | False |
| restart_name | not annotated | None |
| verbose | not annotated | True |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `DataWriter`, `DcdWriter`, `LangevinIntegrator`, `PDBFile.writeFile`, `app.PDBReporter`, `final_state.getPositions`, `open`, `os.path.join`, `print`, `self.create_openmm_simulation`, `self.create_openmm_system`, `self.get_platform`, `self.save_rst`, `simulation.context.getState`, `simulation.context.setPeriodicBoxVectors`, `simulation.context.setPositions`, `simulation.context.setVelocitiesToTemperature`, `simulation.reporters.append`, `simulation.step`, `state.getPeriodicBoxVectors`, `state.getPositions`, `str`, `time.time`.

Explicit return expressions; different branches may return different objects:

```python
(simulation, output_dataname + '.txt')
```

Instance/class attributes assigned directly: `self.final_pdbname`.

Calls worth inspecting for I/O, state changes or delegated execution: `DataWriter`, `DcdWriter`, `PDBFile.writeFile`, `open`, `self.create_openmm_simulation`, `self.create_openmm_system`, `self.save_rst`, `simulation.step`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def basic_NPT(
    self,
    simulation,
    total_steps=None,
    temp=None,
    pressure=None,
    filename=None,
    save_restart=False,
    restart_name=None,
    verbose=True,
):
    equili_start_time = time.time()

    if filename is None:
        filename = "_basic_NPT_"
    else:
        filename = f"_{filename}_"

    if total_steps is None:
        total_steps = self.total_steps

    if temp is None:
        temp = self.temp

    if pressure is None:
        pressure = self.pressure

    if verbose is True:
        print(
            f"""Basic NPT information:
            - Total steps: {total_steps}
            - Total simulation time: {(total_steps * self.timestep):.0f} fs
            - Temperature: {temp} K
            - Pressure: {pressure} atm
            """
        )

    state = simulation.context.getState(
        getPositions=True,
        getEnergy=True,
    )

    xyz = state.getPositions()
    vx, vy, vz = state.getPeriodicBoxVectors()

    integrator = LangevinIntegrator(
        temp * kelvin,
        self.friction_coeff / picoseconds,
        self.timestep * femtoseconds,
    )

    platform = self.get_platform()

    system = self.create_openmm_system(
        ensemble="NPT",
        temp=temp,
        pressure=pressure,
    )

    simulation = self.create_openmm_simulation(
        system,
        integrator,
        platform,
    )

    simulation.context.setPeriodicBoxVectors(
        vx,
        vy,
        vz,
    )

    simulation.context.setPositions(
        xyz
    )

    simulation.context.setVelocitiesToTemperature(
        temp * kelvin
    )

    if self.savepdb_traj is True:
        output_pdbname = os.path.join(
            self.output_dir,
            self.filename
            + "_"
            + str(pressure)
            + filename
            + self.run_name
            + ".pdb",
        )

        simulation.reporters.append(
            app.PDBReporter(
                output_pdbname,
                self.reporter_freq,
            )
        )

    output_dcdname = os.path.join(
        self.output_dir,
        self.filename
        + "_"
        + str(pressure)
        + filename
        + self.run_name,
    )

    dcdWriter = DcdWriter(
        output_dcdname,
        self.reporter_freq,
    )

    simulation.reporters.append(
        dcdWriter.dcdReporter
    )

    output_dataname = os.path.join(
        self.output_dir,
        self.filename
        + "_"
        + str(pressure)
        + filename
        + self.run_name,
    )

    dataWriter = DataWriter(
        output_dataname,
        self.reporter_freq,
        total_steps,
    )

    simulation.reporters.append(
        dataWriter.stateDataReporter
    )

    simulation.step(
        total_steps
    )

    time_taken = time.time() - equili_start_time

    print(
        f"Basic NPT completed in {time_taken:.2f} seconds."
    )

    final_state = simulation.context.getState(
        getPositions=True,
        getEnergy=True,
    )

    self.final_pdbname = os.path.join(
        self.output_dir,
        "final_"
        + filename
        + self.filename
        + "_"
        + str(pressure)
        + "_atm.pdb",
    )

    with open(
        self.final_pdbname,
        "w",
    ) as output:
        PDBFile.writeFile(
            simulation.topology,
            final_state.getPositions(),
            output,
        )

    if save_restart is True:
        self.save_rst(
            simulation,
            restart_name=restart_name,
        )

    return simulation, output_dataname + ".txt"
```

</details>

<a id="definition-820"></a>

## `BuildSimulation.basic_NPT_help`

Source lines 820–823. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `classmethod`.

```python
def basic_NPT_help(cls): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| cls | not annotated | bound instance/class |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `print`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def basic_NPT_help(cls):
    print(
        cls.basic_NPT.__doc__
    )
```

</details>

<a id="definition-825"></a>

## `BuildSimulation.basic_NVT`

Source lines 825–979. Named callable; inspect its callers before treating it as a stable public API.

```python
def basic_NVT(self, simulation, total_steps=None, temp=None, filename=None, save_restart=False, restart_name=None, verbose=True): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| simulation | not annotated | required |
| total_steps | not annotated | None |
| temp | not annotated | None |
| filename | not annotated | None |
| save_restart | not annotated | False |
| restart_name | not annotated | None |
| verbose | not annotated | True |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `DataWriter`, `DcdWriter`, `LangevinIntegrator`, `PDBFile.writeFile`, `app.PDBReporter`, `final_state.getPositions`, `open`, `os.path.join`, `print`, `self.create_openmm_simulation`, `self.create_openmm_system`, `self.get_platform`, `self.save_rst`, `simulation.context.getState`, `simulation.context.setPeriodicBoxVectors`, `simulation.context.setPositions`, `simulation.reporters.append`, `simulation.step`, `state.getPeriodicBoxVectors`, `state.getPositions`, `time.time`.

Explicit return expressions; different branches may return different objects:

```python
(simulation, output_dataname + '.txt')
```

Instance/class attributes assigned directly: `self.final_pdbname`.

Calls worth inspecting for I/O, state changes or delegated execution: `DataWriter`, `DcdWriter`, `PDBFile.writeFile`, `open`, `self.create_openmm_simulation`, `self.create_openmm_system`, `self.save_rst`, `simulation.step`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def basic_NVT(
    self,
    simulation,
    total_steps=None,
    temp=None,
    filename=None,
    save_restart=False,
    restart_name=None,
    verbose=True,
):
    prod_start_time = time.time()

    if filename is None:
        filename = "_basic_NVT_"
    else:
        filename = f"_{filename}_"

    if total_steps is None:
        total_steps = self.total_steps

    if temp is None:
        temp = self.temp

    if verbose is True:
        print(
            f"""Basic NVT information:
            - Total steps: {total_steps}
            - Total simulation time: {(total_steps * self.timestep):.0f} fs
            - Temperature: {temp} K
            """
        )

    state = simulation.context.getState(
        getPositions=True,
        getEnergy=True,
    )

    xyz = state.getPositions()
    vx, vy, vz = state.getPeriodicBoxVectors()

    integrator = LangevinIntegrator(
        temp * kelvin,
        self.friction_coeff / picoseconds,
        self.timestep * femtoseconds,
    )

    platform = self.get_platform()

    system = self.create_openmm_system(
        ensemble="NVT",
        temp=temp,
    )

    simulation = self.create_openmm_simulation(
        system,
        integrator,
        platform,
    )

    simulation.context.setPositions(
        xyz
    )

    simulation.context.setPeriodicBoxVectors(
        vx,
        vy,
        vz,
    )

    if self.savepdb_traj is True:
        output_pdbname = os.path.join(
            self.output_dir,
            self.filename
            + filename
            + self.run_name
            + ".pdb",
        )

        simulation.reporters.append(
            app.PDBReporter(
                output_pdbname,
                self.reporter_freq,
            )
        )

    output_dcdname = os.path.join(
        self.output_dir,
        self.filename
        + filename
        + self.run_name,
    )

    dcdWriter = DcdWriter(
        output_dcdname,
        self.reporter_freq,
    )

    simulation.reporters.append(
        dcdWriter.dcdReporter
    )

    output_dataname = os.path.join(
        self.output_dir,
        self.filename
        + filename
        + self.run_name,
    )

    dataWriter = DataWriter(
        output_dataname,
        self.reporter_freq,
        total_steps,
    )

    simulation.reporters.append(
        dataWriter.stateDataReporter
    )

    simulation.step(
        total_steps
    )

    time_taken = time.time() - prod_start_time

    print(
        f"Basic NVT completed in {time_taken:.2f} seconds."
    )

    final_state = simulation.context.getState(
        getPositions=True,
        getEnergy=True,
    )

    self.final_pdbname = os.path.join(
        self.output_dir,
        "final_" + filename + self.filename + ".pdb",
    )

    with open(
        self.final_pdbname,
        "w",
    ) as output:
        PDBFile.writeFile(
            simulation.topology,
            final_state.getPositions(),
            output,
        )

    if save_restart is True:
        self.save_rst(
            simulation,
            restart_name=restart_name,
        )

    return simulation, output_dataname + ".txt"
```

</details>

<a id="definition-981"></a>

## `BuildSimulation.thermal_ramp`

Source lines 981–1197. Named callable; inspect its callers before treating it as a stable public API.

```python
def thermal_ramp(self, simulation, heating=None, quench_rate=None, ensemble=None, start_temp=None, max_temp=None, total_steps=None, pressure=None, filename=None, save_restart=False, restart_name=None): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| simulation | not annotated | required |
| heating | not annotated | None |
| quench_rate | not annotated | None |
| ensemble | not annotated | None |
| start_temp | not annotated | None |
| max_temp | not annotated | None |
| total_steps | not annotated | None |
| pressure | not annotated | None |
| filename | not annotated | None |
| save_restart | not annotated | False |
| restart_name | not annotated | None |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `DataWriter`, `DcdWriter`, `LangevinIntegrator`, `PDBFile.writeFile`, `ValueError`, `abs`, `app.PDBReporter`, `final_state.getPositions`, `int`, `integrator.setTemperature`, `len`, `np.arange`, `np.arange(start_temp, max_temp + abs(quench_rate), abs(quench_rate)).tolist`, `np.arange(start_temp, max_temp - abs(quench_rate), -abs(quench_rate)).tolist`, `open`, `os.path.join`, `print`, `self.create_openmm_simulation`, `self.create_openmm_system`, `self.get_platform`, `self.save_rst`, `simulation.context.getState`, `simulation.context.setPeriodicBoxVectors`, `simulation.context.setPositions`, `simulation.reporters.append`, `simulation.step`, `state.getPeriodicBoxVectors`, `state.getPositions`, `time.time`.

Explicit return expressions; different branches may return different objects:

```python
None
(simulation, output_dataname + '.txt')
```

Instance/class attributes assigned directly: `self.final_pdbname`.

Calls worth inspecting for I/O, state changes or delegated execution: `DataWriter`, `DcdWriter`, `PDBFile.writeFile`, `open`, `self.create_openmm_simulation`, `self.create_openmm_system`, `self.save_rst`, `simulation.step`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError(f'Heating selected, but max_temp ({max_temp}) <= start_temp ({start_temp})')
ValueError(f'Cooling selected, but start_temp ({start_temp}) <= max_temp ({max_temp})')
ValueError(f'No temperature increments generated. Check start_temp={start_temp}, max_temp={max_temp}, quench_rate={quench_rate}.')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def thermal_ramp(
    self,
    simulation,
    heating=None,
    quench_rate=None,
    ensemble=None,
    start_temp=None,
    max_temp=None,
    total_steps=None,
    pressure=None,
    filename=None,
    save_restart=False,
    restart_name=None,
):
    if ensemble not in ["NVT", "NPT"]:
        print("Please specify 'NVT' or 'NPT' ensemble for the thermal ramp")
        return None

    if heating is None:
        print("Please specify True for heating or False for cooling")
        return None

    if quench_rate is None:
        print("Please specify a quench rate as an integer")
        return None

    thermal_ramp_start_time = time.time()

    if filename is None:
        filename = "_thermal_ramp_"
    else:
        filename = f"_{filename}_"

    if start_temp is None:
        start_temp = self.anneal_parameters[0]

    if max_temp is None:
        max_temp = self.anneal_parameters[1]

    if pressure is None:
        pressure = self.pressure

    if total_steps is None:
        total_steps = self.total_steps

    state = simulation.context.getState(
        getPositions=True,
        getEnergy=True,
        enforcePeriodicBox=True,
    )

    xyz = state.getPositions()
    vx, vy, vz = state.getPeriodicBoxVectors()

    initial_temp = start_temp if heating is True else max_temp

    integrator = LangevinIntegrator(
        initial_temp * kelvin,
        self.friction_coeff / picoseconds,
        self.timestep * femtoseconds,
    )

    platform = self.get_platform()

    system = self.create_openmm_system(
        ensemble=ensemble,
        temp=initial_temp,
        pressure=pressure,
    )

    simulation = self.create_openmm_simulation(
        system,
        integrator,
        platform,
    )

    simulation.context.setPeriodicBoxVectors(
        vx,
        vy,
        vz,
    )

    simulation.context.setPositions(
        xyz
    )

    method = "heat" if heating is True else "cool"

    output_filename = (
        self.filename
        + filename
        + method
        + self.run_name
    )

    if self.savepdb_traj is True:
        output_pdbname = os.path.join(
            self.output_dir,
            output_filename + ".pdb",
        )

        simulation.reporters.append(
            app.PDBReporter(
                output_pdbname,
                self.reporter_freq,
            )
        )

    output_dcdname = os.path.join(
        self.output_dir,
        output_filename,
    )

    dcdWriter = DcdWriter(
        output_dcdname,
        self.reporter_freq,
    )

    simulation.reporters.append(
        dcdWriter.dcdReporter
    )

    output_dataname = os.path.join(
        self.output_dir,
        output_filename,
    )

    dataWriter = DataWriter(
        output_dataname,
        self.reporter_freq,
        total_steps,
    )

    simulation.reporters.append(
        dataWriter.stateDataReporter
    )

    if heating is True:
        if max_temp <= start_temp:
            raise ValueError(
                f"Heating selected, but max_temp ({max_temp}) "
                f"<= start_temp ({start_temp})"
            )

        incremental_temps = np.arange(
            start_temp,
            max_temp + abs(quench_rate),
            abs(quench_rate),
        ).tolist()

    else:
        if start_temp <= max_temp:
            raise ValueError(
                f"Cooling selected, but start_temp ({start_temp}) "
                f"<= max_temp ({max_temp})"
            )

        incremental_temps = np.arange(
            start_temp,
            max_temp - abs(quench_rate),
            -abs(quench_rate),
        ).tolist()

    if len(incremental_temps) == 0:
        raise ValueError(
            f"No temperature increments generated. "
            f"Check start_temp={start_temp}, "
            f"max_temp={max_temp}, "
            f"quench_rate={quench_rate}."
        )

    steps_at_increment = int(
        total_steps / len(incremental_temps)
    )

    for temp_i in incremental_temps:
        integrator.setTemperature(
            temp_i * kelvin
        )

        simulation.step(
            steps_at_increment
        )

    time_taken = time.time() - thermal_ramp_start_time

    print(
        f"Thermal ramp completed in {time_taken:.2f} seconds."
    )

    final_state = simulation.context.getState(
        getPositions=True,
        getEnergy=True,
    )

    self.final_pdbname = os.path.join(
        self.output_dir,
        "final_" + output_filename + ".pdb",
    )

    with open(
        self.final_pdbname,
        "w",
    ) as output:
        PDBFile.writeFile(
            simulation.topology,
            final_state.getPositions(),
            output,
        )

    if save_restart is True:
        self.save_rst(
            simulation,
            restart_name=restart_name,
        )

    return simulation, output_dataname + ".txt"
```

</details>

<a id="definition-1199"></a>

## `BuildSimulation.save_rst`

Source lines 1199–1259. Named callable; inspect its callers before treating it as a stable public API.

```python
def save_rst(self, simulation, restart_name=None, overwrite=False): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| simulation | not annotated | required |
| restart_name | not annotated | None |
| overwrite | not annotated | False |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `final_state.getPositions`, `final_state.getPositions(asNumpy=True).value_in_unit`, `final_state.getVelocities`, `final_state.getVelocities(asNumpy=True).value_in_unit`, `os.makedirs`, `os.path.join`, `parm.save`, `pmd.load_file`, `restart_name.strip`, `shutil.copy`, `simulation.context.getState`.

Explicit return expressions; different branches may return different objects:

```python
rst_filename
```

Calls worth inspecting for I/O, state changes or delegated execution: `parm.save`, `pmd.load_file`, `shutil.copy`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def save_rst(
    self,
    simulation,
    restart_name=None,
    overwrite=False,
):
    if restart_name is None:
        restart_name = f"final_{self.filename}"
    else:
        restart_name = f"{self.filename}_{restart_name.strip()}"

    parm = pmd.load_file(
        self.topology_file,
        self.coordinates_file,
    )

    final_state = simulation.context.getState(
        getPositions=True,
        getVelocities=True,
    )

    parm.coordinates = final_state.getPositions(
        asNumpy=True
    ).value_in_unit(angstroms)

    parm.velocities = final_state.getVelocities(
        asNumpy=True
    ).value_in_unit(angstroms / picoseconds)

    restart_folder = os.path.join(
        self.manager.systems_dir,
        restart_name,
    )

    os.makedirs(
        restart_folder,
        exist_ok=True,
    )

    rst_filename = os.path.join(
        restart_folder,
        f"{restart_name}.rst7",
    )

    parm.save(
        rst_filename,
        format="rst7",
        overwrite=overwrite,
    )

    new_top_name = os.path.join(
        restart_folder,
        f"{restart_name}.prmtop",
    )

    shutil.copy(
        self.topology_file,
        new_top_name,
    )

    return rst_filename
```

</details>

<a id="definition-1261"></a>

## `BuildSimulation.restrain_heavy_atoms`

Source lines 1261–1290. Named callable; inspect its callers before treating it as a stable public API.

```python
def restrain_heavy_atoms(self, system, topology, positions): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| system | not annotated | required |
| topology | not annotated | required |
| positions | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `force.addParticle`, `force.addPerParticleParameter`, `openmm.CustomExternalForce`, `system.addForce`, `topology.atoms`.

Explicit return expressions; different branches may return different objects:

```python
system
```

Calls worth inspecting for I/O, state changes or delegated execution: `openmm.CustomExternalForce`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def restrain_heavy_atoms(
    self,
    system,
    topology,
    positions,
):
    force = openmm.CustomExternalForce(
        "1000*(x-x0)^2 + 1000*(y-y0)^2 + 1000*(z-z0)^2"
    )

    force.addPerParticleParameter("x0")
    force.addPerParticleParameter("y0")
    force.addPerParticleParameter("z0")

    for atom in topology.atoms():
        if atom.element.symbol != "H":
            pos = positions[atom.index]

            force.addParticle(
                atom.index,
                [
                    pos.x,
                    pos.y,
                    pos.z,
                ],
            )

    system.addForce(force)

    return system
```

</details>

<a id="definition-1292"></a>

## `BuildSimulation.__repr__`

Source lines 1292–1315. Internal helper/protocol method.

```python
def __repr__(self): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `"Simulation parameters given in the following format: ('{}', '{}', '{}, {}, {}, {}')".format`, `"Simulation parameters: ('{}', '{}', '{}, {}, {}, {}')".format`, `print`.

Explicit return expressions; different branches may return different objects:

```python
"Simulation parameters given in the following format: ('{}', '{}', '{}, {}, {}, {}')".format('pressure', 'temperature', 'timestep', 'friction coefficient', 'total steps', 'reporter frequency')
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def __repr__(self):
    print(
        "Simulation parameters: "
        "('{}', '{}', '{}, {}, {}, {}')".format(
            self.pressure,
            self.temp,
            self.timestep,
            self.friction_coeff,
            self.total_steps,
            self.reporter_freq,
        )
    )

    return (
        "Simulation parameters given in the following format: "
        "('{}', '{}', '{}, {}, {}, {}')".format(
            "pressure",
            "temperature",
            "timestep",
            "friction coefficient",
            "total steps",
            "reporter frequency",
        )
    )
```

</details>

<a id="definition-1317"></a>

## `BuildSimulation.__str__`

Source lines 1317–1318. Internal helper/protocol method.

```python
def __str__(self): ...
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
f'Simulation object of - {self.filename}'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def __str__(self):
    return f"Simulation object of - {self.filename}"
```

</details>

<a id="definition-1321"></a>

## `BuildSimulation.display_start_time`

Source lines 1321–1325. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `classmethod`.

```python
def display_start_time(cls): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| cls | not annotated | bound instance/class |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `print`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def display_start_time(cls):
    print(
        "Simulation initiated at: ",
        cls.timestamp,
    )
```

</details>

<a id="definition-1328"></a>

## `BuildSimulation.savepdb_trajectories`

Source lines 1328–1343. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `classmethod`.

```python
def savepdb_trajectories(cls, boolean): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| cls | not annotated | bound instance/class |
| boolean | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `isinstance`, `print`.

Explicit return expressions; different branches may return different objects:

```python
None
```

Instance/class attributes assigned directly: `cls.savepdb_traj`.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def savepdb_trajectories(cls, boolean):
    if not isinstance(boolean, bool):
        print("Please pass True or False to this function.")
        return

    cls.savepdb_traj = boolean

    if boolean:
        print(
            "Simulation will save trajectories in both "
            ".pdb and .dcd format."
        )
    else:
        print(
            "Simulation will save trajectories in .dcd format only."
        )
```

</details>

<a id="definition-1346"></a>

## `BuildSimulation.set_temperature`

Source lines 1346–1353. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `classmethod`.

```python
def set_temperature(cls, temp): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| cls | not annotated | bound instance/class |
| temp | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `print`, `str`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Instance/class attributes assigned directly: `cls.temp`.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def set_temperature(cls, temp):
    cls.temp = temp

    print(
        "Temperature set to: ",
        str(temp),
        "kelvin",
    )
```

</details>

<a id="definition-1356"></a>

## `BuildSimulation.set_pressure`

Source lines 1356–1363. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `classmethod`.

```python
def set_pressure(cls, pressure): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| cls | not annotated | bound instance/class |
| pressure | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `print`, `str`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Instance/class attributes assigned directly: `cls.pressure`.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def set_pressure(cls, pressure):
    cls.pressure = pressure

    print(
        "Pressure set to: ",
        str(pressure),
        " atmospheres",
    )
```

</details>

<a id="definition-1366"></a>

## `BuildSimulation.set_timestep`

Source lines 1366–1372. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `classmethod`.

```python
def set_timestep(cls, timestep): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| cls | not annotated | bound instance/class |
| timestep | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `print`, `str`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Instance/class attributes assigned directly: `cls.timestep`.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def set_timestep(cls, timestep):
    cls.timestep = timestep

    print(
        "Timestep set to: ",
        str(timestep),
    )
```

</details>

<a id="definition-1375"></a>

## `BuildSimulation.set_friction_coeff`

Source lines 1375–1381. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `classmethod`.

```python
def set_friction_coeff(cls, friction_coeff): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| cls | not annotated | bound instance/class |
| friction_coeff | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `print`, `str`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Instance/class attributes assigned directly: `cls.friction_coeff`.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def set_friction_coeff(cls, friction_coeff):
    cls.friction_coeff = friction_coeff

    print(
        "Friction coefficient set to: ",
        str(friction_coeff),
    )
```

</details>

<a id="definition-1384"></a>

## `BuildSimulation.set_total_steps`

Source lines 1384–1390. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `classmethod`.

```python
def set_total_steps(cls, total_steps): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| cls | not annotated | bound instance/class |
| total_steps | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `print`, `str`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Instance/class attributes assigned directly: `cls.total_steps`.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def set_total_steps(cls, total_steps):
    cls.total_steps = total_steps

    print(
        "Total steps for simulation set to: ",
        str(total_steps),
    )
```

</details>

<a id="definition-1393"></a>

## `BuildSimulation.set_reporter_freq`

Source lines 1393–1400. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `classmethod`.

```python
def set_reporter_freq(cls, reporter_freq): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| cls | not annotated | bound instance/class |
| reporter_freq | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `print`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Instance/class attributes assigned directly: `cls.reporter_freq`.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def set_reporter_freq(cls, reporter_freq):
    cls.reporter_freq = reporter_freq

    print(
        "Reporter frequency set to every: ",
        reporter_freq,
        " steps",
    )
```

</details>

<a id="definition-1403"></a>

## `BuildSimulation.set_nonbondedcutoff`

Source lines 1403–1414. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `classmethod`.

```python
def set_nonbondedcutoff(cls, nonbondedcutoff): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| cls | not annotated | bound instance/class |
| nonbondedcutoff | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `isinstance`, `print`.

Explicit return expressions; different branches may return different objects:

```python
None
```

Instance/class attributes assigned directly: `cls.nonbondedcutoff`.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def set_nonbondedcutoff(cls, nonbondedcutoff):
    if not isinstance(nonbondedcutoff, float):
        print(
            "Please pass a float to this method to set "
            "a new nonbondedcutoff."
        )
        print(
            "Example: simulation.set_nonbondedcutoff(5.0)"
        )
        return None

    cls.nonbondedcutoff = nonbondedcutoff
```

</details>

<a id="definition-1417"></a>

## `BuildSimulation.set_anneal_parameters`

Source lines 1417–1435. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `classmethod`.

```python
def set_anneal_parameters(cls, new_anneal_parameters): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| cls | not annotated | bound instance/class |
| new_anneal_parameters | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `len`, `print`, `str`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Instance/class attributes assigned directly: `cls.anneal_parameters`.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError(f'Invalid parameters provided. {format_str}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def set_anneal_parameters(cls, new_anneal_parameters):
    if len(new_anneal_parameters) != len(cls.anneal_parameters):
        format_str = (
            "Expected format: "
            "[start_temp, max_temp, cycles, quench_rate, steps_per_cycle]"
        )

        raise ValueError(
            f"Invalid parameters provided. {format_str}"
        )

    cls.anneal_parameters = new_anneal_parameters

    print("Anneal parameters set.")
    print("Starting temperature is: ", str(new_anneal_parameters[0]))
    print("Target temperature is: ", str(new_anneal_parameters[1]))
    print("Number of annealing cycles is: ", str(new_anneal_parameters[2]))
    print("The quench rate is: ", str(new_anneal_parameters[3]))
    print("The number of steps per cycle is: ", str(new_anneal_parameters[4]))
```

</details>

<a id="definition-1438"></a>

## `BuildSimulation.set_anneal_parameters_help`

Source lines 1438–1439. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `classmethod`.

```python
def set_anneal_parameters_help(cls): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| cls | not annotated | bound instance/class |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `print`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def set_anneal_parameters_help(cls):
    print(cls.set_anneal_parameters.__doc__)
```

</details>

<a id="definition-1442"></a>

## `BuildSimulation.graph_state_data`

Source lines 1442–1513. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `staticmethod`.

```python
def graph_state_data(data_file): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| data_file | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `axes[row, col].grid`, `axes[row, col].plot`, `axes[row, col].set_title`, `axes[row, col].set_xlabel`, `axes[row, col].set_ylabel`, `data_file.rsplit`, `enumerate`, `fig.delaxes`, `len`, `min`, `np.array`, `pd.read_csv`, `plt.savefig`, `plt.show`, `plt.subplots`, `plt.tight_layout`, `range`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Calls worth inspecting for I/O, state changes or delegated execution: `pd.read_csv`, `plt.savefig`, `plt.show`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def graph_state_data(data_file):
    png_file_name = data_file.rsplit(
        ".",
        1,
    )[0] + ".png"

    df = pd.read_csv(
        data_file,
        delimiter=",",
    )

    columns_to_plot = df.columns[3:-2]

    num_rows = (
        len(columns_to_plot) + 1
    ) // 2

    num_cols = min(
        2,
        len(columns_to_plot),
    )

    fig, axes = plt.subplots(
        num_rows,
        num_cols,
        figsize=(12, 4 * num_rows),
    )

    if num_rows == 1 and num_cols == 1:
        axes = np.array([[axes]])

    elif num_rows == 1:
        axes = np.array([axes])

    elif num_cols == 1:
        axes = np.array([[ax] for ax in axes])

    for i, column in enumerate(columns_to_plot):
        row = i // num_cols
        col = i % num_cols

        axes[row, col].plot(
            df["Time (ps)"],
            df[column],
        )

        axes[row, col].set_title(column)
        axes[row, col].set_xlabel("Time (ps)")
        axes[row, col].set_ylabel(column)
        axes[row, col].grid(True)

    for i in range(
        len(columns_to_plot),
        num_rows * num_cols,
    ):
        row = i // num_cols
        col = i % num_cols

        fig.delaxes(
            axes[row, col]
        )

    plt.tight_layout(
        rect=[0, 0, 1, 0.96]
    )

    plt.savefig(
        png_file_name,
        dpi=600,
    )

    plt.show()
```

</details>

<a id="definition-1516"></a>

## `BuildSimulation.graph_state_data_help`

Source lines 1516–1517. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `classmethod`.

```python
def graph_state_data_help(cls): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| cls | not annotated | bound instance/class |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `print`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def graph_state_data_help(cls):
    print(cls.graph_state_data.__doc__)
```

</details>

<a id="definition-1528"></a>

## `GromacsSimulation.__new__`

Source lines 1528–1550. Internal helper/protocol method.

```python
def __new__(cls, *args, **kwargs): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| cls | not annotated | bound instance/class |
| *args | variadic positional | optional |
| **kwargs | variadic keyword | optional |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `TypeError`, `len`, `super`, `super().__new__`.

Explicit return expressions; different branches may return different objects:

```python
super().__new__(cls)
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
TypeError('Usage:\nsim = GromacsSimulation(\n    manager,\n    topology_file,\n    coordinates_file,\n    output_dir=None,\n)')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def __new__(cls, *args, **kwargs):

    if len(args) < 3:

        raise TypeError(

            "Usage:\n"

            "sim = GromacsSimulation(\n"

            "    manager,\n"

            "    topology_file,\n"

            "    coordinates_file,\n"

            "    output_dir=None,\n"

            ")"

        )

    return super().__new__(cls)
```

</details>

<a id="definition-1552"></a>

## `GromacsSimulation.__init__`

Source lines 1552–1600. Internal helper/protocol method.

```python
def __init__(self, manager, topology_file, coordinates_file, output_dir=None): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| manager | not annotated | required |
| topology_file | not annotated | required |
| coordinates_file | not annotated | required |
| output_dir | not annotated | None |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `GromacsGroFile`, `GromacsTopFile`, `os.path.basename`, `os.path.basename(topology_file).split`, `self.gro_coordinates.getPeriodicBoxVectors`, `super`, `super().__init__`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Instance/class attributes assigned directly: `self.coordinates_file`, `self.filename`, `self.gro_coordinates`, `self.gro_topology`, `self.manager`, `self.topology_file`.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def __init__(

    self,

    manager,

    topology_file,

    coordinates_file,

    output_dir=None,

):

    self.manager = manager

    self.filename = os.path.basename(

        topology_file

    ).split(".")[0]

    super().__init__(

        manager,

        self.filename,

        output_dir=output_dir,

    )

    self.coordinates_file = coordinates_file

    self.topology_file = topology_file

    self.gro_coordinates = GromacsGroFile(

        coordinates_file

    )

    self.gro_topology = GromacsTopFile(

        topology_file,

        periodicBoxVectors=self.gro_coordinates.getPeriodicBoxVectors(),

    )
```

</details>

<a id="definition-1602"></a>

## `GromacsSimulation.__str__`

Source lines 1602–1604. Internal helper/protocol method.

```python
def __str__(self): ...
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
f'GROMACS simulation object of - {self.filename}'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def __str__(self):

    return f"GROMACS simulation object of - {self.filename}"
```

</details>

<a id="definition-1612"></a>

## `AmberSimulation.__new__`

Source lines 1612–1624. Internal helper/protocol method.

```python
def __new__(cls, *args, **kwargs): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| cls | not annotated | bound instance/class |
| *args | variadic positional | optional |
| **kwargs | variadic keyword | optional |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `TypeError`, `len`, `super`, `super().__new__`.

Explicit return expressions; different branches may return different objects:

```python
super().__new__(cls)
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
TypeError('Usage:\nsim = AmberSimulation(\n    manager,\n    topology_file,\n    coordinates_file,\n    output_dir=None,\n)')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def __new__(cls, *args, **kwargs):
    if len(args) < 3:
        raise TypeError(
            "Usage:\n"
            "sim = AmberSimulation(\n"
            "    manager,\n"
            "    topology_file,\n"
            "    coordinates_file,\n"
            "    output_dir=None,\n"
            ")"
        )

    return super().__new__(cls)
```

</details>

<a id="definition-1626"></a>

## `AmberSimulation.__init__`

Source lines 1626–1655. Internal helper/protocol method.

```python
def __init__(self, manager, topology_file, coordinates_file, output_dir=None): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| manager | not annotated | required |
| topology_file | not annotated | required |
| coordinates_file | not annotated | required |
| output_dir | not annotated | None |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `app.AmberInpcrdFile`, `app.AmberPrmtopFile`, `os.path.basename`, `os.path.basename(topology_file).split`, `super`, `super().__init__`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Instance/class attributes assigned directly: `self.amb_coordinates`, `self.amb_topology`, `self.coordinates_file`, `self.filename`, `self.manager`, `self.topology_file`.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def __init__(
    self,
    manager,
    topology_file,
    coordinates_file,
    output_dir=None,
):
    self.manager = manager

    self.filename = os.path.basename(
        topology_file
    ).split(".")[0]

    super().__init__(
        manager,
        self.filename,
        output_dir=output_dir,
    )

    self.coordinates_file = coordinates_file
    self.topology_file = topology_file

    self.amb_coordinates = app.AmberInpcrdFile(
        coordinates_file
    )

    self.amb_topology = app.AmberPrmtopFile(
        topology_file,
        periodicBoxVectors=self.amb_coordinates.boxVectors,
    )
```

</details>

<a id="definition-1657"></a>

## `AmberSimulation.__str__`

Source lines 1657–1658. Internal helper/protocol method.

```python
def __str__(self): ...
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
f'Amber simulation object of - {self.filename}'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def __str__(self):
    return f"Amber simulation object of - {self.filename}"
```

</details>
