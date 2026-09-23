# analysis/tg_analysis/temperature_assignment.py

Assign nominal cooling temperatures using supplied total steps, reporting frequency, temperature range and step. The historical frame-zero convention is preserved. This does not infer the protocol from instantaneous temperature measurements.

[Current source](../../src/iphasimulator/analysis/tg_analysis/temperature_assignment.py)

This page is generated from source syntax. Original docstrings can be incomplete or outdated; module notes above identify known discrepancies. Call/return/error lists describe direct syntax, not all behaviour inside callees. Read the source excerpt for branch order and effects. No scientific execution is implied.

Explicit functions/methods/nested helpers: **1**.

## Module imports

```python
from __future__ import annotations
import numpy as np
import pandas as pd
from ..simulation_loader import LoadedSimulation
```

## Function map

- [`assign_nominal_temperatures` — source line 26](#definition-26)

<a id="definition-26"></a>

## `assign_nominal_temperatures`

Source lines 26–169. Named callable; inspect its callers before treating it as a stable public API.

```python
def assign_nominal_temperatures(simulation: LoadedSimulation, total_steps: int, max_temp: float, min_temp: float, temp_change: float, reporter_freq: int) -> pd.DataFrame: ...
```

### Purpose and original contract

Assign nominal temperatures to trajectory frames.

This reproduces the temperature-assignment method used in the
original Tg analysis workflow.

The total number of simulation steps is divided equally between
the requested nominal temperatures. Each trajectory frame is then
assigned a temperature according to its frame index and reporter
frequency.

Parameters
----------
simulation : LoadedSimulation
    Loaded molecular dynamics simulation.

total_steps : int
    Total number of simulation steps represented by the cooling
    trajectory.

max_temp : float
    Highest nominal temperature.

min_temp : float
    Lowest nominal temperature.

temp_change : float
    Temperature interval between neighbouring nominal temperatures.

reporter_freq : int
    Number of simulation steps between trajectory frames.

Returns
-------
pandas.DataFrame
    Table containing, for every trajectory frame:

    - frame index
    - nominal step
    - nominal temperature

Notes
-----
This function intentionally reproduces the original temperature
assignment method, including its use of::

    step = frame_index * reporter_freq

Therefore, frame zero is assigned nominal step zero even when the
first recorded simulation frame corresponds to a later simulation
step.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| simulation | LoadedSimulation | required |
| total_steps | int | required |
| max_temp | float | required |
| min_temp | float | required |
| temp_change | float | required |
| reporter_freq | int | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `int`, `len`, `np.arange`, `np.floor`, `np.floor(nominal_steps / steps_per_temp).astype`, `pd.DataFrame`.

Explicit return expressions; different branches may return different objects:

```python
assignments
```

Calls worth inspecting for I/O, state changes or delegated execution: `np.floor(nominal_steps / steps_per_temp).astype`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('total_steps must be greater than zero.')
ValueError('reporter_freq must be greater than zero.')
ValueError('temp_change must be greater than zero.')
ValueError('max_temp must be greater than min_temp for a cooling trajectory.')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def assign_nominal_temperatures(
    simulation: LoadedSimulation,
    total_steps: int,
    max_temp: float,
    min_temp: float,
    temp_change: float,
    reporter_freq: int,
) -> pd.DataFrame:
    """
    Assign nominal temperatures to trajectory frames.

    This reproduces the temperature-assignment method used in the
    original Tg analysis workflow.

    The total number of simulation steps is divided equally between
    the requested nominal temperatures. Each trajectory frame is then
    assigned a temperature according to its frame index and reporter
    frequency.

    Parameters
    ----------
    simulation : LoadedSimulation
        Loaded molecular dynamics simulation.

    total_steps : int
        Total number of simulation steps represented by the cooling
        trajectory.

    max_temp : float
        Highest nominal temperature.

    min_temp : float
        Lowest nominal temperature.

    temp_change : float
        Temperature interval between neighbouring nominal temperatures.

    reporter_freq : int
        Number of simulation steps between trajectory frames.

    Returns
    -------
    pandas.DataFrame
        Table containing, for every trajectory frame:

        - frame index
        - nominal step
        - nominal temperature

    Notes
    -----
    This function intentionally reproduces the original temperature
    assignment method, including its use of::

        step = frame_index * reporter_freq

    Therefore, frame zero is assigned nominal step zero even when the
    first recorded simulation frame corresponds to a later simulation
    step.
    """

    # -------------------------------------------------------------------------
    # Validate inputs
    # -------------------------------------------------------------------------

    if total_steps <= 0:
        raise ValueError(
            "total_steps must be greater than zero."
        )

    if reporter_freq <= 0:
        raise ValueError(
            "reporter_freq must be greater than zero."
        )

    if temp_change <= 0:
        raise ValueError(
            "temp_change must be greater than zero."
        )

    if max_temp <= min_temp:
        raise ValueError(
            "max_temp must be greater than min_temp "
            "for a cooling trajectory."
        )

    # -------------------------------------------------------------------------
    # Determine temperature schedule
    # -------------------------------------------------------------------------

    n_temps = (
        int((max_temp - min_temp) / temp_change)
        + 1
    )

    steps_per_temp = total_steps / n_temps

    # -------------------------------------------------------------------------
    # Determine trajectory frames
    # -------------------------------------------------------------------------

    n_frames = len(
        simulation.universe.trajectory
    )

    frame_indices = np.arange(
        n_frames,
        dtype=int,
    )

    # -------------------------------------------------------------------------
    # Reproduce original step assignment
    # -------------------------------------------------------------------------

    nominal_steps = (
        frame_indices * reporter_freq
    )

    # -------------------------------------------------------------------------
    # Assign temperature block
    # -------------------------------------------------------------------------

    temperature_indices = np.floor(
        nominal_steps / steps_per_temp
    ).astype(int)

    nominal_temperatures = (
        max_temp
        - temp_change * temperature_indices
    )

    # -------------------------------------------------------------------------
    # Construct output table
    # -------------------------------------------------------------------------

    assignments = pd.DataFrame(
        {
            "Frame": frame_indices,
            "Nominal Step": nominal_steps,
            "Nominal Temperature (K)": nominal_temperatures,
        }
    )

    return assignments
```

</details>
