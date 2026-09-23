# analysis/simulation_loader.py

Find one minimised PDB and stage-specific DCD/TXT pair, load MDAnalysis/pandas objects, and check lengths plus selected time checkpoints. File matching is deliberately strict; a stage with multiple matches is ambiguous.

[Current source](../../src/iphasimulator/analysis/simulation_loader.py)

This page is generated from source syntax. Original docstrings can be incomplete or outdated; module notes above identify known discrepancies. Call/return/error lists describe direct syntax, not all behaviour inside callees. Read the source excerpt for branch order and effects. No scientific execution is implied.

Explicit functions/methods/nested helpers: **3**.

## Module imports

```python
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import MDAnalysis as mda
import pandas as pd
```

## Classes and result records

### `LoadedSimulation`

Container for a molecular dynamics simulation loaded for analysis.

Attributes
----------
system_directory : Path
    Directory containing the molecular system.

simulation_directory : Path
    Directory containing the selected simulation run.

topology_path : Path
    Path to the topology/structure file used by MDAnalysis.

trajectory_path : Path
    Path to the trajectory file.

data_path : Path
    Path to the simulation state-data file.

universe : MDAnalysis.Universe
    Loaded MDAnalysis Universe containing the topology and trajectory.

data : pandas.DataFrame
    Simulation state data associated with the trajectory.

Decorators: `dataclass(frozen=True)`.

Declared fields/defaults (instance state may also be set by methods):

```python
system_directory: Path
simulation_directory: Path
topology_path: Path
trajectory_path: Path
data_path: Path
universe: mda.Universe
data: pd.DataFrame
```

Dataclass-generated methods are implicit and are not counted as explicit function definitions.

## Function map

- [`_find_single_file` — source line 71](#definition-71)
- [`validate_frame_data_alignment` — source line 134](#definition-134)
- [`load_simulation` — source line 266](#definition-266)

<a id="definition-71"></a>

## `_find_single_file`

Source lines 71–127. Internal helper/protocol method.

```python
def _find_single_file(directory: Path, pattern: str, description: str) -> Path: ...
```

### Purpose and original contract

Find exactly one file matching a glob pattern.

Parameters
----------
directory : Path
    Directory to search.

pattern : str
    Glob pattern used to identify the required file.

description : str
    Human-readable description used in error messages.

Returns
-------
Path
    Path to the matching file.

Raises
------
FileNotFoundError
    If no matching file is found.

RuntimeError
    If more than one matching file is found.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| directory | Path | required |
| pattern | str | required |
| description | str | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `'\n'.join`, `FileNotFoundError`, `RuntimeError`, `directory.glob`, `len`, `sorted`.

Explicit return expressions; different branches may return different objects:

```python
matches[0]
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
FileNotFoundError(f'No {description} found in:\n{directory}\nPattern: {pattern}')
RuntimeError(f'Multiple {description} files found in:\n{directory}\nPattern: {pattern}\nMatches:\n{matching_names}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _find_single_file(
    directory: Path,
    pattern: str,
    description: str,
) -> Path:
    """
    Find exactly one file matching a glob pattern.

    Parameters
    ----------
    directory : Path
        Directory to search.

    pattern : str
        Glob pattern used to identify the required file.

    description : str
        Human-readable description used in error messages.

    Returns
    -------
    Path
        Path to the matching file.

    Raises
    ------
    FileNotFoundError
        If no matching file is found.

    RuntimeError
        If more than one matching file is found.
    """

    matches = sorted(directory.glob(pattern))

    if not matches:
        raise FileNotFoundError(
            f"No {description} found in:\n"
            f"{directory}\n"
            f"Pattern: {pattern}"
        )

    if len(matches) > 1:
        matching_names = "\n".join(
            f"  - {path.name}"
            for path in matches
        )

        raise RuntimeError(
            f"Multiple {description} files found in:\n"
            f"{directory}\n"
            f"Pattern: {pattern}\n"
            f"Matches:\n"
            f"{matching_names}"
        )

    return matches[0]
```

</details>

<a id="definition-134"></a>

## `validate_frame_data_alignment`

Source lines 134–259. Named callable; inspect its callers before treating it as a stable public API.

```python
def validate_frame_data_alignment(universe: mda.Universe, data: pd.DataFrame, time_column: str='Time (ps)', tolerance_ps: float=0.01) -> None: ...
```

### Purpose and original contract

Validate alignment between trajectory frames and state-data rows.

The trajectory and state-data file are expected to contain the same
number of entries. Selected trajectory frame times are compared with
their corresponding state-data times to confirm that the two files
describe the same points in the simulation.

Five points distributed across the trajectory are checked:

    - first frame
    - 25 % through trajectory
    - 50 % through trajectory
    - 75 % through trajectory
    - final frame

Parameters
----------
universe : MDAnalysis.Universe
    Loaded MDAnalysis Universe.

data : pandas.DataFrame
    Simulation state-data DataFrame.

time_column : str, optional
    Name of the column containing simulation time in ps.

    Default:
        "Time (ps)"

tolerance_ps : float, optional
    Maximum permitted difference between trajectory time and
    state-data time.

    Default:
        0.01 ps

Raises
------
ValueError
    If:

    - the trajectory contains no frames,
    - the state-data time column cannot be found,
    - the number of trajectory frames and data rows differs,
    - trajectory and state-data times are not aligned.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| universe | mda.Universe | required |
| data | pd.DataFrame | required |
| time_column | str | 'Time (ps)' |
| tolerance_ps | float | 0.01 |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `abs`, `float`, `len`, `sorted`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('Trajectory contains no frames.')
ValueError(f"Required time column '{time_column}' was not found in the state-data file.")
ValueError(f'Trajectory/data length mismatch:\nTrajectory frames: {n_frames}\nState-data rows:   {n_rows}')
ValueError(f'Trajectory/state-data time mismatch:\nFrame:           {frame_index}\nTrajectory time: {trajectory_time:.6f} ps\nState-data time: {data_time:.6f} ps\nDifference:      {difference:.6f} ps\nTolerance:       {tolerance_ps:.6f} ps')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def validate_frame_data_alignment(
    universe: mda.Universe,
    data: pd.DataFrame,
    time_column: str = "Time (ps)",
    tolerance_ps: float = 0.01,
) -> None:
    """
    Validate alignment between trajectory frames and state-data rows.

    The trajectory and state-data file are expected to contain the same
    number of entries. Selected trajectory frame times are compared with
    their corresponding state-data times to confirm that the two files
    describe the same points in the simulation.

    Five points distributed across the trajectory are checked:

        - first frame
        - 25 % through trajectory
        - 50 % through trajectory
        - 75 % through trajectory
        - final frame

    Parameters
    ----------
    universe : MDAnalysis.Universe
        Loaded MDAnalysis Universe.

    data : pandas.DataFrame
        Simulation state-data DataFrame.

    time_column : str, optional
        Name of the column containing simulation time in ps.

        Default:
            "Time (ps)"

    tolerance_ps : float, optional
        Maximum permitted difference between trajectory time and
        state-data time.

        Default:
            0.01 ps

    Raises
    ------
    ValueError
        If:

        - the trajectory contains no frames,
        - the state-data time column cannot be found,
        - the number of trajectory frames and data rows differs,
        - trajectory and state-data times are not aligned.
    """

    n_frames = len(universe.trajectory)
    n_rows = len(data)

    # -------------------------------------------------------------------------
    # Check trajectory contains frames
    # -------------------------------------------------------------------------

    if n_frames == 0:
        raise ValueError(
            "Trajectory contains no frames."
        )

    # -------------------------------------------------------------------------
    # Check required data column exists
    # -------------------------------------------------------------------------

    if time_column not in data.columns:
        raise ValueError(
            f"Required time column '{time_column}' "
            f"was not found in the state-data file."
        )

    # -------------------------------------------------------------------------
    # Check trajectory and state-data lengths
    # -------------------------------------------------------------------------

    if n_frames != n_rows:
        raise ValueError(
            "Trajectory/data length mismatch:\n"
            f"Trajectory frames: {n_frames}\n"
            f"State-data rows:   {n_rows}"
        )

    # -------------------------------------------------------------------------
    # Select representative frames for validation
    # -------------------------------------------------------------------------

    test_indices = {
        0,
        n_frames // 4,
        n_frames // 2,
        (3 * n_frames) // 4,
        n_frames - 1,
    }

    # -------------------------------------------------------------------------
    # Compare trajectory and state-data times
    # -------------------------------------------------------------------------

    for frame_index in sorted(test_indices):

        trajectory_time = float(
            universe.trajectory[frame_index].time
        )

        data_time = float(
            data[time_column].iloc[frame_index]
        )

        difference = abs(
            trajectory_time - data_time
        )

        if difference > tolerance_ps:
            raise ValueError(
                "Trajectory/state-data time mismatch:\n"
                f"Frame:           {frame_index}\n"
                f"Trajectory time: {trajectory_time:.6f} ps\n"
                f"State-data time: {data_time:.6f} ps\n"
                f"Difference:      {difference:.6f} ps\n"
                f"Tolerance:       {tolerance_ps:.6f} ps"
            )
```

</details>

<a id="definition-266"></a>

## `load_simulation`

Source lines 266–452. Named callable; inspect its callers before treating it as a stable public API.

```python
def load_simulation(system_directory: str | Path, simulation_name: str, stage: str, *, validate_alignment: bool=True, time_tolerance_ps: float=0.01) -> LoadedSimulation: ...
```

### Purpose and original contract

Load an iPHAsimulator molecular dynamics simulation for analysis.

The function locates the selected simulation directory, identifies
the topology, trajectory and state-data files, constructs an
MDAnalysis Universe, and loads the associated state data.

Parameters
----------
system_directory : str or Path
    Path to the molecular system directory.

    The directory is expected to contain::

        simulations/
            <simulation_name>/

simulation_name : str
    Name of the simulation run to load.

    Example::

        "broad_tg_sim_02"

stage : str
    Filename tag identifying the requested simulation stage.

    Example::

        "thermal_ramp_cooling"

validate_alignment : bool, optional
    If True, validate that trajectory frames correspond to rows
    in the state-data file.

    Default:
        True

time_tolerance_ps : float, optional
    Maximum permitted difference between trajectory and state-data
    times during alignment validation.

    Default:
        0.01 ps

Returns
-------
LoadedSimulation
    Object containing:

    - molecular system directory,
    - simulation directory,
    - topology path,
    - trajectory path,
    - state-data path,
    - MDAnalysis Universe,
    - simulation state-data DataFrame.

Raises
------
FileNotFoundError
    If the system directory, simulation directory, or required
    simulation files cannot be found.

RuntimeError
    If multiple files match one of the required file patterns.

ValueError
    If trajectory/state-data alignment validation fails.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| system_directory | str \| Path | required |
| simulation_name | str | required |
| stage | str | required |
| validate_alignment (keyword-only) | bool | True |
| time_tolerance_ps (keyword-only) | float | 0.01 |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `FileNotFoundError`, `LoadedSimulation`, `Path`, `Path(system_directory).expanduser`, `Path(system_directory).expanduser().resolve`, `_find_single_file`, `mda.Universe`, `pd.read_csv`, `simulation_directory.is_dir`, `str`, `system_directory.is_dir`, `validate_frame_data_alignment`.

Explicit return expressions; different branches may return different objects:

```python
LoadedSimulation(system_directory=system_directory, simulation_directory=simulation_directory, topology_path=topology_path, trajectory_path=trajectory_path, data_path=data_path, universe=universe, data=data)
```

Calls worth inspecting for I/O, state changes or delegated execution: `LoadedSimulation`, `pd.read_csv`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
FileNotFoundError(f'System directory not found:\n{system_directory}')
FileNotFoundError(f'Simulation directory not found:\n{simulation_directory}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def load_simulation(
    system_directory: str | Path,
    simulation_name: str,
    stage: str,
    *,
    validate_alignment: bool = True,
    time_tolerance_ps: float = 0.01,
) -> LoadedSimulation:
    """
    Load an iPHAsimulator molecular dynamics simulation for analysis.

    The function locates the selected simulation directory, identifies
    the topology, trajectory and state-data files, constructs an
    MDAnalysis Universe, and loads the associated state data.

    Parameters
    ----------
    system_directory : str or Path
        Path to the molecular system directory.

        The directory is expected to contain::

            simulations/
                <simulation_name>/

    simulation_name : str
        Name of the simulation run to load.

        Example::

            "broad_tg_sim_02"

    stage : str
        Filename tag identifying the requested simulation stage.

        Example::

            "thermal_ramp_cooling"

    validate_alignment : bool, optional
        If True, validate that trajectory frames correspond to rows
        in the state-data file.

        Default:
            True

    time_tolerance_ps : float, optional
        Maximum permitted difference between trajectory and state-data
        times during alignment validation.

        Default:
            0.01 ps

    Returns
    -------
    LoadedSimulation
        Object containing:

        - molecular system directory,
        - simulation directory,
        - topology path,
        - trajectory path,
        - state-data path,
        - MDAnalysis Universe,
        - simulation state-data DataFrame.

    Raises
    ------
    FileNotFoundError
        If the system directory, simulation directory, or required
        simulation files cannot be found.

    RuntimeError
        If multiple files match one of the required file patterns.

    ValueError
        If trajectory/state-data alignment validation fails.
    """

    # -------------------------------------------------------------------------
    # Resolve molecular system directory
    # -------------------------------------------------------------------------

    system_directory = (
        Path(system_directory)
        .expanduser()
        .resolve()
    )

    if not system_directory.is_dir():
        raise FileNotFoundError(
            f"System directory not found:\n"
            f"{system_directory}"
        )

    # -------------------------------------------------------------------------
    # Resolve simulation directory
    # -------------------------------------------------------------------------

    simulation_directory = (
        system_directory
        / "simulations"
        / simulation_name
    )

    if not simulation_directory.is_dir():
        raise FileNotFoundError(
            f"Simulation directory not found:\n"
            f"{simulation_directory}"
        )

    # -------------------------------------------------------------------------
    # Locate topology
    # -------------------------------------------------------------------------

    topology_path = _find_single_file(
        directory=simulation_directory,
        pattern="min_*.pdb",
        description="minimised topology PDB",
    )

    # -------------------------------------------------------------------------
    # Locate trajectory
    # -------------------------------------------------------------------------

    trajectory_path = _find_single_file(
        directory=simulation_directory,
        pattern=f"*{stage}*.dcd",
        description=(
            f"trajectory for simulation stage '{stage}'"
        ),
    )

    # -------------------------------------------------------------------------
    # Locate state-data file
    # -------------------------------------------------------------------------

    data_path = _find_single_file(
        directory=simulation_directory,
        pattern=f"*{stage}*.txt",
        description=(
            f"state-data file for simulation stage '{stage}'"
        ),
    )

    # -------------------------------------------------------------------------
    # Construct MDAnalysis Universe
    # -------------------------------------------------------------------------

    universe = mda.Universe(
        str(topology_path),
        str(trajectory_path),
    )

    # -------------------------------------------------------------------------
    # Load simulation state data
    # -------------------------------------------------------------------------

    data = pd.read_csv(
        data_path
    )

    # -------------------------------------------------------------------------
    # Validate trajectory/data alignment
    # -------------------------------------------------------------------------

    if validate_alignment:

        validate_frame_data_alignment(
            universe=universe,
            data=data,
            tolerance_ps=time_tolerance_ps,
        )

    # -------------------------------------------------------------------------
    # Return loaded simulation
    # -------------------------------------------------------------------------

    return LoadedSimulation(
        system_directory=system_directory,
        simulation_directory=simulation_directory,
        topology_path=topology_path,
        trajectory_path=trajectory_path,
        data_path=data_path,
        universe=universe,
        data=data,
    )
```

</details>
