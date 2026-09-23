# openmmscript_builder.py

Represent ordered simulation stages, validate them, serialise workflow JSON and generate executable Python. Generating code does not run dynamics. The generated script expects a workspace directory layout and still uses source-checkout imports; its first execution stage is minimisation.

[Current source](../../src/iphasimulator/openmmscript_builder.py)

This page is generated from source syntax. Original docstrings can be incomplete or outdated; module notes above identify known discrepancies. Call/return/error lists describe direct syntax, not all behaviour inside callees. Read the source excerpt for branch order and effects. No scientific execution is implied.

Explicit functions/methods/nested helpers: **18**.

## Module imports

```python
from pathlib import Path
from copy import deepcopy
import json
import textwrap
```

## Classes and result records

### `OpenMMScriptBuilder`

Build OpenMM workflow scripts for iPHAsimulator.

Parameters
----------
system_name : str
    Name of the registered MD system.

    Examples:

        P3HB_10_dry
        P3HB_10_solvated
        P3HB_10_solvated_KCl_0_15
        25_P3HB_10_melt

system_type : str
    Registered system type.

    Supported values:

        dry
        solvated
        solvated_ions
        melt

run_name : str, optional
    Base name used for the numbered simulation directory.

    Examples:

        Test       -> Test_01
        Tg         -> Tg_01
        Annealing  -> Annealing_01

Declared fields/defaults (instance state may also be set by methods):

```python
workflow_format_version = 1
supported_system_types = {'dry', 'solvated', 'solvated_ions', 'melt'}
```

## Function map

- [`OpenMMScriptBuilder.__init__` — source line 69](#definition-69)
- [`OpenMMScriptBuilder.add_minimization` — source line 166](#definition-166)
- [`OpenMMScriptBuilder.add_basic_NVT` — source line 177](#definition-177)
- [`OpenMMScriptBuilder.add_basic_NPT` — source line 200](#definition-200)
- [`OpenMMScriptBuilder.add_anneal_NVT` — source line 225](#definition-225)
- [`OpenMMScriptBuilder.add_thermal_ramp` — source line 254](#definition-254)
- [`OpenMMScriptBuilder.to_dict` — source line 291](#definition-291)
- [`OpenMMScriptBuilder.from_dict` — source line 328](#definition-328)
- [`OpenMMScriptBuilder.save_workflow` — source line 460](#definition-460)
- [`OpenMMScriptBuilder.load_workflow` — source line 522](#definition-522)
- [`OpenMMScriptBuilder.validate` — source line 577](#definition-577)
- [`OpenMMScriptBuilder.write_script` — source line 854](#definition-854)
- [`OpenMMScriptBuilder.to_script` — source line 892](#definition-892)
- [`OpenMMScriptBuilder._build_steps_code` — source line 1109](#definition-1109)
- [`OpenMMScriptBuilder._format_basic_NVT` — source line 1182](#definition-1182)
- [`OpenMMScriptBuilder._format_basic_NPT` — source line 1199](#definition-1199)
- [`OpenMMScriptBuilder._format_anneal_NVT` — source line 1217](#definition-1217)
- [`OpenMMScriptBuilder._format_thermal_ramp` — source line 1237](#definition-1237)

<a id="definition-69"></a>

## `OpenMMScriptBuilder.__init__`

Source lines 69–160. Internal helper/protocol method.

```python
def __init__(self, system_name, system_type, run_name='Test', workflow_name=None): ...
```

### Purpose and original contract

Create an OpenMM workflow builder.

Parameters
----------
system_name : str
    Name of the registered MD system.

system_type : str
    Registered system type.

run_name : str, optional
    Prefix used when creating numbered simulation run
    directories.

    Example:

        broad_tg_sim

    may generate:

        broad_tg_sim_01
        broad_tg_sim_02
        broad_tg_sim_03

workflow_name : str, optional
    Human-readable name for the reusable workflow.

    If omitted, run_name is used.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| system_name | not annotated | required |
| system_type | not annotated | required |
| run_name | not annotated | 'Test' |
| workflow_name | not annotated | None |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `isinstance`, `run_name.strip`, `sorted`, `system_name.strip`, `workflow_name.strip`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Instance/class attributes assigned directly: `self.run_name`, `self.steps`, `self.system_name`, `self.system_type`, `self.workflow_name`.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('system_name must be a non-empty string.')
ValueError(f'Unsupported system type: {system_type}\nSupported values: {sorted(self.supported_system_types)}')
ValueError('run_name must be a non-empty string.')
ValueError('workflow_name must be a non-empty string.')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def __init__(
    self,
    system_name,
    system_type,
    run_name="Test",
    workflow_name=None,
):
    """
    Create an OpenMM workflow builder.

    Parameters
    ----------
    system_name : str
        Name of the registered MD system.

    system_type : str
        Registered system type.

    run_name : str, optional
        Prefix used when creating numbered simulation run
        directories.

        Example:

            broad_tg_sim

        may generate:

            broad_tg_sim_01
            broad_tg_sim_02
            broad_tg_sim_03

    workflow_name : str, optional
        Human-readable name for the reusable workflow.

        If omitted, run_name is used.
    """

    if (
        not isinstance(system_name, str)
        or not system_name.strip()
    ):
        raise ValueError(
            "system_name must be a non-empty string."
        )

    if (
        system_type
        not in self.supported_system_types
    ):
        raise ValueError(
            f"Unsupported system type: {system_type}\n"
            f"Supported values: "
            f"{sorted(self.supported_system_types)}"
        )

    if (
        not isinstance(run_name, str)
        or not run_name.strip()
    ):
        raise ValueError(
            "run_name must be a non-empty string."
        )

    if workflow_name is None:
        workflow_name = run_name

    if (
        not isinstance(workflow_name, str)
        or not workflow_name.strip()
    ):
        raise ValueError(
            "workflow_name must be a non-empty string."
        )

    self.system_name = (
        system_name.strip()
    )

    self.system_type = (
        system_type
    )

    self.run_name = (
        run_name.strip()
    )

    self.workflow_name = (
        workflow_name.strip()
    )

    self.steps = []
```

</details>

<a id="definition-166"></a>

## `OpenMMScriptBuilder.add_minimization`

Source lines 166–175. Named callable; inspect its callers before treating it as a stable public API.

```python
def add_minimization(self): ...
```

### Purpose and original contract

Add an energy-minimisation step.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.steps.append`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Calls worth inspecting for I/O, state changes or delegated execution: `self.steps.append`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def add_minimization(self):
    """
    Add an energy-minimisation step.
    """

    self.steps.append(
        {
            "method": "minimize_energy",
        }
    )
```

</details>

<a id="definition-177"></a>

## `OpenMMScriptBuilder.add_basic_NVT`

Source lines 177–198. Named callable; inspect its callers before treating it as a stable public API.

```python
def add_basic_NVT(self, total_steps=3000, temp=300, filename='NVT', save_restart=False, restart_name=None): ...
```

### Purpose and original contract

Add a constant-volume, constant-temperature simulation.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| total_steps | not annotated | 3000 |
| temp | not annotated | 300 |
| filename | not annotated | 'NVT' |
| save_restart | not annotated | False |
| restart_name | not annotated | None |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.steps.append`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Calls worth inspecting for I/O, state changes or delegated execution: `self.steps.append`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def add_basic_NVT(
    self,
    total_steps=3000,
    temp=300,
    filename="NVT",
    save_restart=False,
    restart_name=None,
):
    """
    Add a constant-volume, constant-temperature simulation.
    """

    self.steps.append(
        {
            "method": "basic_NVT",
            "total_steps": total_steps,
            "temp": temp,
            "filename": filename,
            "save_restart": save_restart,
            "restart_name": restart_name,
        }
    )
```

</details>

<a id="definition-200"></a>

## `OpenMMScriptBuilder.add_basic_NPT`

Source lines 200–223. Named callable; inspect its callers before treating it as a stable public API.

```python
def add_basic_NPT(self, total_steps=3000, temp=300, pressure=1, filename='NPT', save_restart=False, restart_name=None): ...
```

### Purpose and original contract

Add a constant-pressure, constant-temperature simulation.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| total_steps | not annotated | 3000 |
| temp | not annotated | 300 |
| pressure | not annotated | 1 |
| filename | not annotated | 'NPT' |
| save_restart | not annotated | False |
| restart_name | not annotated | None |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.steps.append`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Calls worth inspecting for I/O, state changes or delegated execution: `self.steps.append`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def add_basic_NPT(
    self,
    total_steps=3000,
    temp=300,
    pressure=1,
    filename="NPT",
    save_restart=False,
    restart_name=None,
):
    """
    Add a constant-pressure, constant-temperature simulation.
    """

    self.steps.append(
        {
            "method": "basic_NPT",
            "total_steps": total_steps,
            "temp": temp,
            "pressure": pressure,
            "filename": filename,
            "save_restart": save_restart,
            "restart_name": restart_name,
        }
    )
```

</details>

<a id="definition-225"></a>

## `OpenMMScriptBuilder.add_anneal_NVT`

Source lines 225–252. Named callable; inspect its callers before treating it as a stable public API.

```python
def add_anneal_NVT(self, start_temp=300, max_temp=700, cycles=5, quench_rate=10, steps_per_cycle=500000, filename='anneal_NVT', save_restart=False, restart_name=None): ...
```

### Purpose and original contract

Add an NVT annealing workflow.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| start_temp | not annotated | 300 |
| max_temp | not annotated | 700 |
| cycles | not annotated | 5 |
| quench_rate | not annotated | 10 |
| steps_per_cycle | not annotated | 500000 |
| filename | not annotated | 'anneal_NVT' |
| save_restart | not annotated | False |
| restart_name | not annotated | None |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.steps.append`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Calls worth inspecting for I/O, state changes or delegated execution: `self.steps.append`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def add_anneal_NVT(
    self,
    start_temp=300,
    max_temp=700,
    cycles=5,
    quench_rate=10,
    steps_per_cycle=500000,
    filename="anneal_NVT",
    save_restart=False,
    restart_name=None,
):
    """
    Add an NVT annealing workflow.
    """

    self.steps.append(
        {
            "method": "anneal_NVT",
            "start_temp": start_temp,
            "max_temp": max_temp,
            "cycles": cycles,
            "quench_rate": quench_rate,
            "steps_per_cycle": steps_per_cycle,
            "filename": filename,
            "save_restart": save_restart,
            "restart_name": restart_name,
        }
    )
```

</details>

<a id="definition-254"></a>

## `OpenMMScriptBuilder.add_thermal_ramp`

Source lines 254–285. Named callable; inspect its callers before treating it as a stable public API.

```python
def add_thermal_ramp(self, heating=True, ensemble='NPT', start_temp=300, max_temp=700, quench_rate=10, total_steps=100000, pressure=1, filename='thermal_ramp', save_restart=False, restart_name=None): ...
```

### Purpose and original contract

Add a heating or cooling ramp.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| heating | not annotated | True |
| ensemble | not annotated | 'NPT' |
| start_temp | not annotated | 300 |
| max_temp | not annotated | 700 |
| quench_rate | not annotated | 10 |
| total_steps | not annotated | 100000 |
| pressure | not annotated | 1 |
| filename | not annotated | 'thermal_ramp' |
| save_restart | not annotated | False |
| restart_name | not annotated | None |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.steps.append`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Calls worth inspecting for I/O, state changes or delegated execution: `self.steps.append`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def add_thermal_ramp(
    self,
    heating=True,
    ensemble="NPT",
    start_temp=300,
    max_temp=700,
    quench_rate=10,
    total_steps=100000,
    pressure=1,
    filename="thermal_ramp",
    save_restart=False,
    restart_name=None,
):
    """
    Add a heating or cooling ramp.
    """

    self.steps.append(
        {
            "method": "thermal_ramp",
            "heating": heating,
            "ensemble": ensemble,
            "start_temp": start_temp,
            "max_temp": max_temp,
            "quench_rate": quench_rate,
            "total_steps": total_steps,
            "pressure": pressure,
            "filename": filename,
            "save_restart": save_restart,
            "restart_name": restart_name,
        }
    )
```

</details>

<a id="definition-291"></a>

## `OpenMMScriptBuilder.to_dict`

Source lines 291–324. Named callable; inspect its callers before treating it as a stable public API.

```python
def to_dict(self): ...
```

### Purpose and original contract

Return the complete workflow definition as a dictionary.

The returned dictionary contains all information required
to reconstruct the OpenMMScriptBuilder later.

Returns
-------
dict
    Serialisable workflow definition.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `deepcopy`.

Explicit return expressions; different branches may return different objects:

```python
{'workflow_format_version': self.workflow_format_version, 'workflow_name': self.workflow_name, 'system_name': self.system_name, 'system_type': self.system_type, 'run_name': self.run_name, 'steps': deepcopy(self.steps)}
```

Calls worth inspecting for I/O, state changes or delegated execution: `deepcopy`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def to_dict(self):
    """
    Return the complete workflow definition as a dictionary.

    The returned dictionary contains all information required
    to reconstruct the OpenMMScriptBuilder later.

    Returns
    -------
    dict
        Serialisable workflow definition.
    """

    return {
        "workflow_format_version":
            self.workflow_format_version,

        "workflow_name":
            self.workflow_name,

        "system_name":
            self.system_name,

        "system_type":
            self.system_type,

        "run_name":
            self.run_name,

        "steps":
            deepcopy(
                self.steps
            ),
    }
```

</details>

<a id="definition-328"></a>

## `OpenMMScriptBuilder.from_dict`

Source lines 328–457. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `classmethod`.

```python
def from_dict(cls, workflow_data): ...
```

### Purpose and original contract

Reconstruct an OpenMMScriptBuilder from a dictionary.

Parameters
----------
workflow_data : dict
    Workflow definition previously generated using
    ``to_dict()``.

Returns
-------
OpenMMScriptBuilder
    Reconstructed workflow builder.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| cls | not annotated | bound instance/class |
| workflow_data | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `TypeError`, `ValueError`, `builder.validate`, `cls`, `deepcopy`, `isinstance`, `set`, `sorted`, `workflow_data.get`.

Explicit return expressions; different branches may return different objects:

```python
builder
```

Calls worth inspecting for I/O, state changes or delegated execution: `deepcopy`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
TypeError('workflow_data must be a dictionary.')
ValueError(f'Workflow definition is missing required fields: {sorted(missing_fields)}')
ValueError(f'Unsupported workflow format version: {workflow_version}. Current supported version: {cls.workflow_format_version}.')
TypeError("Workflow 'steps' must be a list.")
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def from_dict(
    cls,
    workflow_data,
):
    """
    Reconstruct an OpenMMScriptBuilder from a dictionary.

    Parameters
    ----------
    workflow_data : dict
        Workflow definition previously generated using
        ``to_dict()``.

    Returns
    -------
    OpenMMScriptBuilder
        Reconstructed workflow builder.
    """

    if not isinstance(
        workflow_data,
        dict,
    ):
        raise TypeError(
            "workflow_data must be a dictionary."
        )


    required_fields = {
        "system_name",
        "system_type",
        "run_name",
        "steps",
    }


    missing_fields = (
        required_fields
        - set(
            workflow_data
        )
    )


    if missing_fields:

        raise ValueError(
            "Workflow definition is missing required "
            "fields: "
            f"{sorted(missing_fields)}"
        )


    workflow_version = (
        workflow_data.get(
            "workflow_format_version",
            1,
        )
    )


    if (
        workflow_version
        != cls.workflow_format_version
    ):
        raise ValueError(
            "Unsupported workflow format version: "
            f"{workflow_version}. "
            "Current supported version: "
            f"{cls.workflow_format_version}."
        )


    workflow_name = (
        workflow_data.get(
            "workflow_name",
            workflow_data["run_name"],
        )
    )


    builder = cls(
        system_name=(
            workflow_data[
                "system_name"
            ]
        ),
        system_type=(
            workflow_data[
                "system_type"
            ]
        ),
        run_name=(
            workflow_data[
                "run_name"
            ]
        ),
        workflow_name=(
            workflow_name
        ),
    )


    steps = (
        workflow_data[
            "steps"
        ]
    )


    if not isinstance(
        steps,
        list,
    ):
        raise TypeError(
            "Workflow 'steps' must be a list."
        )


    builder.steps = deepcopy(
        steps
    )


    builder.validate(
        require_steps=False
    )


    return builder
```

</details>

<a id="definition-460"></a>

## `OpenMMScriptBuilder.save_workflow`

Source lines 460–518. Named callable; inspect its callers before treating it as a stable public API.

```python
def save_workflow(self, output_file): ...
```

### Purpose and original contract

Save the reusable workflow definition as JSON.

Parameters
----------
output_file : str or pathlib.Path
    Destination JSON file.

Returns
-------
pathlib.Path
    Path to the saved workflow definition.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| output_file | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `Path`, `json.dump`, `open`, `output_file.parent.mkdir`, `print`, `self.to_dict`, `self.validate`.

Explicit return expressions; different branches may return different objects:

```python
output_file
```

Calls worth inspecting for I/O, state changes or delegated execution: `open`, `output_file.parent.mkdir`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def save_workflow(
    self,
    output_file,
):
    """
    Save the reusable workflow definition as JSON.

    Parameters
    ----------
    output_file : str or pathlib.Path
        Destination JSON file.

    Returns
    -------
    pathlib.Path
        Path to the saved workflow definition.
    """

    self.validate(
        require_steps=False
    )


    output_file = Path(
        output_file
    )


    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )


    workflow_data = (
        self.to_dict()
    )


    with open(
        output_file,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            workflow_data,
            file,
            indent=4,
        )


    print(
        "OpenMM workflow written to:\n"
        f"{output_file}"
    )


    return output_file
```

</details>

<a id="definition-522"></a>

## `OpenMMScriptBuilder.load_workflow`

Source lines 522–571. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `classmethod`.

```python
def load_workflow(cls, workflow_file): ...
```

### Purpose and original contract

Load a reusable OpenMM workflow from JSON.

Parameters
----------
workflow_file : str or pathlib.Path
    Saved workflow JSON file.

Returns
-------
OpenMMScriptBuilder
    Reconstructed workflow builder.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| cls | not annotated | bound instance/class |
| workflow_file | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `FileNotFoundError`, `Path`, `cls.from_dict`, `json.load`, `open`, `workflow_file.exists`.

Explicit return expressions; different branches may return different objects:

```python
builder
```

Calls worth inspecting for I/O, state changes or delegated execution: `json.load`, `open`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
FileNotFoundError(f'Workflow file not found:\n{workflow_file}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def load_workflow(
    cls,
    workflow_file,
):
    """
    Load a reusable OpenMM workflow from JSON.

    Parameters
    ----------
    workflow_file : str or pathlib.Path
        Saved workflow JSON file.

    Returns
    -------
    OpenMMScriptBuilder
        Reconstructed workflow builder.
    """

    workflow_file = Path(
        workflow_file
    )


    if not workflow_file.exists():

        raise FileNotFoundError(
            "Workflow file not found:\n"
            f"{workflow_file}"
        )


    with open(
        workflow_file,
        "r",
        encoding="utf-8",
    ) as file:

        workflow_data = (
            json.load(
                file
            )
        )


    builder = cls.from_dict(
        workflow_data
    )


    return builder
```

</details>

<a id="definition-577"></a>

## `OpenMMScriptBuilder.validate`

Source lines 577–848. Named callable; inspect its callers before treating it as a stable public API.

```python
def validate(self, require_steps=True): ...
```

### Purpose and original contract

Validate the configured OpenMM workflow.

Parameters
----------
require_steps : bool, optional
    If True, the workflow must contain at least one
    simulation step.

    False is useful when saving an unfinished workflow.

Returns
-------
bool
    True when the workflow is valid.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| require_steps | not annotated | True |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `TypeError`, `ValueError`, `enumerate`, `first_step.get`, `isinstance`, `len`, `set`, `sorted`, `step.get`, `step['filename'].strip`.

Explicit return expressions; different branches may return different objects:

```python
True
```

Calls worth inspecting for I/O, state changes or delegated execution: `first_step.get`, `step.get`, `step['filename'].strip`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
TypeError('Workflow steps must be stored as a list.')
ValueError('The workflow does not contain any simulation steps.')
TypeError('Workflow step 1 must be a dictionary.')
ValueError('The first workflow step must currently be minimization.')
TypeError(f'Workflow step {step_index} must be a dictionary.')
ValueError(f'Workflow step {step_index} does not define a method.')
ValueError(f'Unsupported workflow method in step {step_index}: {method}')
ValueError(f'Workflow step {step_index} ({method}) is missing fields: {sorted(missing_fields)}')
ValueError(f'Workflow step {step_index}: total_steps must be greater than zero.')
ValueError(f'Workflow step {step_index}: steps_per_cycle must be greater than zero.')
ValueError(f'Workflow step {step_index}: filename must be a non-empty string.')
ValueError(f"Workflow step {step_index}: thermal-ramp ensemble must be 'NVT' or 'NPT'.")
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def validate(
    self,
    require_steps=True,
):
    """
    Validate the configured OpenMM workflow.

    Parameters
    ----------
    require_steps : bool, optional
        If True, the workflow must contain at least one
        simulation step.

        False is useful when saving an unfinished workflow.

    Returns
    -------
    bool
        True when the workflow is valid.
    """

    if not isinstance(
        self.steps,
        list,
    ):
        raise TypeError(
            "Workflow steps must be stored as a list."
        )


    if len(self.steps) == 0:

        if require_steps:

            raise ValueError(
                "The workflow does not contain any "
                "simulation steps."
            )

        return True


    supported_methods = {
        "minimize_energy",
        "basic_NVT",
        "basic_NPT",
        "anneal_NVT",
        "thermal_ramp",
    }


    required_step_fields = {
        "minimize_energy": {
            "method",
        },

        "basic_NVT": {
            "method",
            "total_steps",
            "temp",
            "filename",
            "save_restart",
            "restart_name",
        },

        "basic_NPT": {
            "method",
            "total_steps",
            "temp",
            "pressure",
            "filename",
            "save_restart",
            "restart_name",
        },

        "anneal_NVT": {
            "method",
            "start_temp",
            "max_temp",
            "cycles",
            "quench_rate",
            "steps_per_cycle",
            "filename",
            "save_restart",
            "restart_name",
        },

        "thermal_ramp": {
            "method",
            "heating",
            "ensemble",
            "start_temp",
            "max_temp",
            "quench_rate",
            "total_steps",
            "pressure",
            "filename",
            "save_restart",
            "restart_name",
        },
    }


    # --------------------------------------------------
    # Validate first step
    # --------------------------------------------------

    first_step = (
        self.steps[0]
    )


    if not isinstance(
        first_step,
        dict,
    ):
        raise TypeError(
            "Workflow step 1 must be a dictionary."
        )


    if (
        first_step.get(
            "method"
        )
        != "minimize_energy"
    ):
        raise ValueError(
            "The first workflow step must currently "
            "be minimization."
        )


    # --------------------------------------------------
    # Validate every step
    # --------------------------------------------------

    for step_index, step in enumerate(
        self.steps,
        start=1,
    ):

        if not isinstance(
            step,
            dict,
        ):
            raise TypeError(
                f"Workflow step {step_index} "
                "must be a dictionary."
            )


        method = (
            step.get(
                "method"
            )
        )


        if method is None:

            raise ValueError(
                f"Workflow step {step_index} "
                "does not define a method."
            )


        if (
            method
            not in supported_methods
        ):

            raise ValueError(
                f"Unsupported workflow method "
                f"in step {step_index}: "
                f"{method}"
            )


        required_fields = (
            required_step_fields[
                method
            ]
        )


        missing_fields = (
            required_fields
            - set(
                step
            )
        )


        if missing_fields:

            raise ValueError(
                f"Workflow step {step_index} "
                f"({method}) is missing fields: "
                f"{sorted(missing_fields)}"
            )


        # ----------------------------------------------
        # Common simulation-step checks
        # ----------------------------------------------

        if (
            "total_steps" in step
            and step["total_steps"] <= 0
        ):
            raise ValueError(
                f"Workflow step {step_index}: "
                "total_steps must be greater than zero."
            )


        if (
            "steps_per_cycle" in step
            and step[
                "steps_per_cycle"
            ] <= 0
        ):
            raise ValueError(
                f"Workflow step {step_index}: "
                "steps_per_cycle must be greater "
                "than zero."
            )


        if (
            "filename" in step
            and (
                not isinstance(
                    step["filename"],
                    str,
                )
                or not step[
                    "filename"
                ].strip()
            )
        ):
            raise ValueError(
                f"Workflow step {step_index}: "
                "filename must be a non-empty string."
            )


        # ----------------------------------------------
        # Thermal-ramp checks
        # ----------------------------------------------

        if (
            method
            == "thermal_ramp"
        ):

            if (
                step["ensemble"]
                not in {
                    "NVT",
                    "NPT",
                }
            ):
                raise ValueError(
                    f"Workflow step {step_index}: "
                    "thermal-ramp ensemble must be "
                    "'NVT' or 'NPT'."
                )


    return True
```

</details>

<a id="definition-854"></a>

## `OpenMMScriptBuilder.write_script`

Source lines 854–890. Named callable; inspect its callers before treating it as a stable public API.

```python
def write_script(self, output_script): ...
```

### Purpose and original contract

Write the generated workflow to a Python file.

Parameters
----------
output_script : str or pathlib.Path
    Destination path for the generated Python script.

Returns
-------
pathlib.Path
    Path to the generated script.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| output_script | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `Path`, `file.write`, `open`, `output_script.parent.mkdir`, `print`, `self.to_script`.

Explicit return expressions; different branches may return different objects:

```python
output_script
```

Calls worth inspecting for I/O, state changes or delegated execution: `file.write`, `open`, `output_script.parent.mkdir`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def write_script(self, output_script):
    """
    Write the generated workflow to a Python file.

    Parameters
    ----------
    output_script : str or pathlib.Path
        Destination path for the generated Python script.

    Returns
    -------
    pathlib.Path
        Path to the generated script.
    """

    output_script = Path(output_script)

    output_script.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    script_text = self.to_script()

    with open(
        output_script,
        "w",
        encoding="utf-8",
    ) as file:
        file.write(script_text)

    print(
        "OpenMM script written to:\n"
        f"{output_script}"
    )

    return output_script
```

</details>

<a id="definition-892"></a>

## `OpenMMScriptBuilder.to_script`

Source lines 892–1103. Named callable; inspect its callers before treating it as a stable public API.

```python
def to_script(self): ...
```

### Purpose and original contract

Return the complete generated OpenMM Python script.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self._build_steps_code`, `self.validate`.

Explicit return expressions; different branches may return different objects:

```python
f'#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n\n"""\nGenerated OpenMM simulation script.\n\nGenerated automatically by OpenMMScriptBuilder.\n\nWorkflow name:\n    {self.workflow_name}\n\nSystem name:\n    {self.system_name}\n\nSystem type:\n    {self.system_type}\n\nRun name:\n    {self.run_name}\n"""\n\nfrom pathlib import Path\nimport sys\n\n\n# ============================================= … [full expression below]
```

Calls worth inspecting for I/O, state changes or delegated execution: `self._build_steps_code`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
    def to_script(self):
        """
        Return the complete generated OpenMM Python script.
        """
        self.validate()
        step_code = self._build_steps_code()

        return f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generated OpenMM simulation script.

Generated automatically by OpenMMScriptBuilder.

Workflow name:
    {self.workflow_name}

System name:
    {self.system_name}

System type:
    {self.system_type}

Run name:
    {self.run_name}
"""

from pathlib import Path
import sys


# ==========================================================
# Project paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
STRUCTURE_DATABASE = PROJECT_ROOT / "structure_database"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ==========================================================
# iPHAsimulator imports
# ==========================================================

from src.iphasimulator.pha_filepath_manager import PHAFileManager
from src.iphasimulator.sw_openmm import (
    AmberSimulation,
    GromacsSimulation,
)


if __name__ == "__main__":

    # ======================================================
    # Load the selected MD system
    # ======================================================

    paths = PHAFileManager(
        STRUCTURE_DATABASE
    )

    system_name = {self.system_name!r}
    system_type = {self.system_type!r}
    run_name = {self.run_name!r}

    workflow_name = {self.workflow_name!r}

    system_files = paths.get_md_system_files(
        system_name=system_name,
        system_type=system_type,
    )

    system_dir = Path(
        system_files["system_dir"]
    )

    topology_file = Path(
        system_files["topology_file"]
    )

    coordinate_file = Path(
        system_files["coordinate_file"]
    )

    simulations_dir = Path(
        system_files["simulations_dir"]
    )

    run_dir = paths.create_named_md_system_simulation_run_dir(
        system_name=system_name,
        system_type=system_type,
        run_name=run_name,
    )

    print("=" * 80)
    print("OpenMM simulation workflow")
    print("=" * 80)
    print("Project root:           ", PROJECT_ROOT)
    print("Structure database:     ", STRUCTURE_DATABASE)
    print("Workflow name:          ", workflow_name)
    print("System name:            ", system_name)
    print("System type:            ", system_type)
    print("System directory:       ", system_dir)
    print("Simulations directory:  ", simulations_dir)
    print("Topology file:          ", topology_file)
    print("Coordinate file:        ", coordinate_file)
    print("OpenMM output directory:", run_dir)
    print("=" * 80)

    if not topology_file.exists():
        raise FileNotFoundError(
            f"Topology file not found:\\n{{topology_file}}"
        )

    if not coordinate_file.exists():
        raise FileNotFoundError(
            f"Coordinate file not found:\\n{{coordinate_file}}"
        )

    # ======================================================
    # Detect Amber or GROMACS input format
    # ======================================================

    topology_suffix = topology_file.suffix.lower()
    coordinate_suffix = coordinate_file.suffix.lower()

    if (
        topology_suffix == ".top"
        and coordinate_suffix == ".gro"
    ):
        simulation_class = GromacsSimulation
        simulation_format = "GROMACS"

    elif (
        topology_suffix == ".prmtop"
        and coordinate_suffix in {{
            ".rst7",
            ".inpcrd",
        }}
    ):
        simulation_class = AmberSimulation
        simulation_format = "Amber"

    else:
        raise ValueError(
            "Could not infer the OpenMM simulation class from "
            "the input file extensions.\\n"
            f"Topology: {{topology_file}}\\n"
            f"Coordinates: {{coordinate_file}}"
        )

    print("Detected input format:", simulation_format)

    # ======================================================
    # Create the OpenMM simulation object
    # ======================================================

    sim = simulation_class(
        paths,
        str(topology_file),
        str(coordinate_file),
        output_dir=str(run_dir),
    )

    print(sim)

    data_files = []

{step_code}

    # ======================================================
    # Workflow complete
    # ======================================================

    print("=" * 80)
    print("Simulation workflow finished.")
    print("Final output directory:", sim.output_dir)
    print("=" * 80)

    if data_files:
        print("State-data files generated:")

        for data_file in data_files:
            print("  ", data_file)

        for data_file in data_files:
            try:
                print(
                    "Generating state-data graph for:",
                    data_file,
                )

                sim.graph_state_data(
                    data_file
                )

            except Exception as error:
                print(
                    "Could not graph state-data file:",
                    data_file,
                )
                print("Reason:", error)

    else:
        print(
            "No state-data files were generated. "
            "This is expected for a minimisation-only workflow."
        )
'''
```

</details>

<a id="definition-1109"></a>

## `OpenMMScriptBuilder._build_steps_code`

Source lines 1109–1180. Internal helper/protocol method.

```python
def _build_steps_code(self): ...
```

### Purpose and original contract

Convert configured workflow steps into executable Python code.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `'\n'.join`, `ValueError`, `enumerate`, `len`, `lines.append`, `lines.extend`, `self._format_anneal_NVT`, `self._format_basic_NPT`, `self._format_basic_NVT`, `self._format_thermal_ramp`, `textwrap.indent`.

Explicit return expressions; different branches may return different objects:

```python
textwrap.indent('print("No simulation steps were added.")', '    ')
textwrap.indent('\n'.join(lines), '    ')
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('The first workflow step must currently be minimization.')
ValueError(f'Unknown OpenMM workflow method: {method}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _build_steps_code(self):
    """
    Convert configured workflow steps into executable Python code.
    """

    if len(self.steps) == 0:
        return textwrap.indent(
            'print("No simulation steps were added.")',
            "    ",
        )

    lines = []
    has_current_sim = False

    for index, step in enumerate(
        self.steps,
        start=1,
    ):
        method = step["method"]

        lines.append("")
        lines.append("#" * 60)
        lines.append(f"# Step {index}: {method}")
        lines.append("#" * 60)
        lines.append(
            f'print("Running step {index}: {method}")'
        )

        if method == "minimize_energy":
            lines.append(
                "current_sim = sim.minimize_energy()"
            )

            has_current_sim = True

        else:
            if not has_current_sim:
                raise ValueError(
                    "The first workflow step must currently "
                    "be minimization."
                )

            if method == "basic_NVT":
                lines.extend(
                    self._format_basic_NVT(step)
                )

            elif method == "basic_NPT":
                lines.extend(
                    self._format_basic_NPT(step)
                )

            elif method == "anneal_NVT":
                lines.extend(
                    self._format_anneal_NVT(step)
                )

            elif method == "thermal_ramp":
                lines.extend(
                    self._format_thermal_ramp(step)
                )

            else:
                raise ValueError(
                    "Unknown OpenMM workflow method: "
                    f"{method}"
                )

    return textwrap.indent(
        "\n".join(lines),
        "    ",
    )
```

</details>

<a id="definition-1182"></a>

## `OpenMMScriptBuilder._format_basic_NVT`

Source lines 1182–1197. Internal helper/protocol method.

```python
def _format_basic_NVT(self, step): ...
```

### Purpose and original contract

Format a basic NVT workflow step.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| step | not annotated | required |

### How to read this implementation

No direct function calls were found in this definition's own body.

Explicit return expressions; different branches may return different objects:

```python
['current_sim, data_file = sim.basic_NVT(', '    current_sim,', f"    total_steps={step['total_steps']},", f"    temp={step['temp']},", f"    filename={step['filename']!r},", f"    save_restart={step['save_restart']},", f"    restart_name={step['restart_name']!r},", ')', 'data_files.append(data_file)']
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _format_basic_NVT(self, step):
    """
    Format a basic NVT workflow step.
    """

    return [
        "current_sim, data_file = sim.basic_NVT(",
        "    current_sim,",
        f"    total_steps={step['total_steps']},",
        f"    temp={step['temp']},",
        f"    filename={step['filename']!r},",
        f"    save_restart={step['save_restart']},",
        f"    restart_name={step['restart_name']!r},",
        ")",
        "data_files.append(data_file)",
    ]
```

</details>

<a id="definition-1199"></a>

## `OpenMMScriptBuilder._format_basic_NPT`

Source lines 1199–1215. Internal helper/protocol method.

```python
def _format_basic_NPT(self, step): ...
```

### Purpose and original contract

Format a basic NPT workflow step.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| step | not annotated | required |

### How to read this implementation

No direct function calls were found in this definition's own body.

Explicit return expressions; different branches may return different objects:

```python
['current_sim, data_file = sim.basic_NPT(', '    current_sim,', f"    total_steps={step['total_steps']},", f"    temp={step['temp']},", f"    pressure={step['pressure']},", f"    filename={step['filename']!r},", f"    save_restart={step['save_restart']},", f"    restart_name={step['restart_name']!r},", ')', 'data_files.append(data_file)']
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _format_basic_NPT(self, step):
    """
    Format a basic NPT workflow step.
    """

    return [
        "current_sim, data_file = sim.basic_NPT(",
        "    current_sim,",
        f"    total_steps={step['total_steps']},",
        f"    temp={step['temp']},",
        f"    pressure={step['pressure']},",
        f"    filename={step['filename']!r},",
        f"    save_restart={step['save_restart']},",
        f"    restart_name={step['restart_name']!r},",
        ")",
        "data_files.append(data_file)",
    ]
```

</details>

<a id="definition-1217"></a>

## `OpenMMScriptBuilder._format_anneal_NVT`

Source lines 1217–1235. Internal helper/protocol method.

```python
def _format_anneal_NVT(self, step): ...
```

### Purpose and original contract

Format an NVT annealing workflow step.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| step | not annotated | required |

### How to read this implementation

No direct function calls were found in this definition's own body.

Explicit return expressions; different branches may return different objects:

```python
['current_sim, data_file = sim.anneal_NVT(', '    current_sim,', f"    start_temp={step['start_temp']},", f"    max_temp={step['max_temp']},", f"    cycles={step['cycles']},", f"    quench_rate={step['quench_rate']},", f"    steps_per_cycle={step['steps_per_cycle']},", f"    filename={step['filename']!r},", f"    save_restart={step['save_restart']},", f"    restart_name={step['restart_name']!r},", … [full expression below]
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _format_anneal_NVT(self, step):
    """
    Format an NVT annealing workflow step.
    """

    return [
        "current_sim, data_file = sim.anneal_NVT(",
        "    current_sim,",
        f"    start_temp={step['start_temp']},",
        f"    max_temp={step['max_temp']},",
        f"    cycles={step['cycles']},",
        f"    quench_rate={step['quench_rate']},",
        f"    steps_per_cycle={step['steps_per_cycle']},",
        f"    filename={step['filename']!r},",
        f"    save_restart={step['save_restart']},",
        f"    restart_name={step['restart_name']!r},",
        ")",
        "data_files.append(data_file)",
    ]
```

</details>

<a id="definition-1237"></a>

## `OpenMMScriptBuilder._format_thermal_ramp`

Source lines 1237–1257. Internal helper/protocol method.

```python
def _format_thermal_ramp(self, step): ...
```

### Purpose and original contract

Format a heating or cooling ramp workflow step.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| step | not annotated | required |

### How to read this implementation

No direct function calls were found in this definition's own body.

Explicit return expressions; different branches may return different objects:

```python
['current_sim, data_file = sim.thermal_ramp(', '    current_sim,', f"    heating={step['heating']},", f"    ensemble={step['ensemble']!r},", f"    start_temp={step['start_temp']},", f"    max_temp={step['max_temp']},", f"    quench_rate={step['quench_rate']},", f"    total_steps={step['total_steps']},", f"    pressure={step['pressure']},", f"    filename={step['filename']!r},", f"    save_restart= … [full expression below]
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _format_thermal_ramp(self, step):
    """
    Format a heating or cooling ramp workflow step.
    """

    return [
        "current_sim, data_file = sim.thermal_ramp(",
        "    current_sim,",
        f"    heating={step['heating']},",
        f"    ensemble={step['ensemble']!r},",
        f"    start_temp={step['start_temp']},",
        f"    max_temp={step['max_temp']},",
        f"    quench_rate={step['quench_rate']},",
        f"    total_steps={step['total_steps']},",
        f"    pressure={step['pressure']},",
        f"    filename={step['filename']!r},",
        f"    save_restart={step['save_restart']},",
        f"    restart_name={step['restart_name']!r},",
        ")",
        "data_files.append(data_file)",
    ]
```

</details>
