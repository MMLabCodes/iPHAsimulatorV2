# analysis/tg_analysis/system_analysis.py

Consume completed replica summaries/temperature responses and aggregate independently fitted Tg values. No trajectory analysis or pooled refitting occurs. Automatic discovery can skip invalid replicas; explicit selection raises for invalid requested data. Compatibility/independence require additional review.

[Current source](../../src/iphasimulator/analysis/tg_analysis/system_analysis.py)

This page is generated from source syntax. Original docstrings can be incomplete or outdated; module notes above identify known discrepancies. Call/return/error lists describe direct syntax, not all behaviour inside callees. Read the source excerpt for branch order and effects. No scientific execution is implied.

Explicit functions/methods/nested helpers: **14**.

## Module imports

```python
from __future__ import annotations
from pathlib import Path
import json
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
```

## Function map

- [`_save_figure` — source line 95](#definition-95)
- [`_load_json` — source line 126](#definition-126)
- [`discover_completed_replica_analyses` — source line 148](#definition-148)
- [`load_replica_analysis` — source line 209](#definition-209)
- [`build_replica_summary_dataframe` — source line 357](#definition-357)
- [`build_temperature_response_dataframe` — source line 559](#definition-559)
- [`build_pca_summary_dataframe` — source line 614](#definition-614)
- [`build_dbscan_summary_dataframe` — source line 640](#definition-640)
- [`calculate_system_tg_statistics` — source line 672](#definition-672)
- [`plot_tg_by_replica` — source line 764](#definition-764)
- [`plot_temperature_response_by_replica` — source line 876](#definition-876)
- [`plot_metric_by_replica` — source line 948](#definition-948)
- [`generate_system_figures` — source line 1063](#definition-1063)
- [`run_system_tg_analysis` — source line 1299](#definition-1299)

<a id="definition-95"></a>

## `_save_figure`

Source lines 95–123. Internal helper/protocol method.

```python
def _save_figure(figure, output_path, dpi=300): ...
```

### Purpose and original contract

Save and close a matplotlib figure.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| figure | not annotated | required |
| output_path | not annotated | required |
| dpi | not annotated | 300 |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `Path`, `figure.savefig`, `figure.tight_layout`, `output_path.parent.mkdir`, `plt.close`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Calls worth inspecting for I/O, state changes or delegated execution: `figure.savefig`, `output_path.parent.mkdir`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _save_figure(
    figure,
    output_path,
    dpi=300,
):
    """
    Save and close a matplotlib figure.
    """

    output_path = Path(
        output_path
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    figure.tight_layout()

    figure.savefig(
        output_path,
        dpi=dpi,
        bbox_inches="tight",
    )

    plt.close(
        figure
    )
```

</details>

<a id="definition-126"></a>

## `_load_json`

Source lines 126–141. Internal helper/protocol method.

```python
def _load_json(path): ...
```

### Purpose and original contract

Load a JSON file.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| path | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `json.load`, `open`.

Explicit return expressions; different branches may return different objects:

```python
json.load(handle)
```

Calls worth inspecting for I/O, state changes or delegated execution: `json.load`, `open`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _load_json(
    path,
):
    """
    Load a JSON file.
    """

    with open(
        path,
        "r",
        encoding="utf-8",
    ) as handle:

        return json.load(
            handle
        )
```

</details>

<a id="definition-148"></a>

## `discover_completed_replica_analyses`

Source lines 148–202. Named callable; inspect its callers before treating it as a stable public API.

```python
def discover_completed_replica_analyses(simulations_directory): ...
```

### Purpose and original contract

Discover completed replica-level Tg analyses.

A simulation is considered to contain a completed replica analysis when
the following file exists:

    analysis/tg_analysis/analysis_summary.json

Parameters
----------
simulations_directory : pathlib.Path
    Directory containing simulation replicas.

Returns
-------
list[pathlib.Path]
    Completed replica simulation directories.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| simulations_directory | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `completed.append`, `simulation_directory.is_dir`, `simulations_directory.is_dir`, `simulations_directory.iterdir`, `sorted`, `summary_path.is_file`.

Explicit return expressions; different branches may return different objects:

```python
completed
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def discover_completed_replica_analyses(
    simulations_directory,
):
    """
    Discover completed replica-level Tg analyses.

    A simulation is considered to contain a completed replica analysis when
    the following file exists:

        analysis/tg_analysis/analysis_summary.json

    Parameters
    ----------
    simulations_directory : pathlib.Path
        Directory containing simulation replicas.

    Returns
    -------
    list[pathlib.Path]
        Completed replica simulation directories.
    """

    completed = []


    if not simulations_directory.is_dir():

        return completed


    for simulation_directory in sorted(
        simulations_directory.iterdir()
    ):

        if not simulation_directory.is_dir():

            continue


        summary_path = (
            simulation_directory
            / "analysis"
            / "tg_analysis"
            / "analysis_summary.json"
        )


        if summary_path.is_file():

            completed.append(
                simulation_directory
            )


    return completed
```

</details>

<a id="definition-209"></a>

## `load_replica_analysis`

Source lines 209–350. Named callable; inspect its callers before treating it as a stable public API.

```python
def load_replica_analysis(simulation_directory, expected_system_name): ...
```

### Purpose and original contract

Load and validate one completed replica-level Tg analysis.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| simulation_directory | not annotated | required |
| expected_system_name | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `FileNotFoundError`, `ValueError`, `_load_json`, `pd.read_csv`, `response_path.is_file`, `set`, `sorted`, `summary.get`, `summary_path.is_file`.

Explicit return expressions; different branches may return different objects:

```python
{'simulation_directory': simulation_directory, 'analysis_directory': analysis_directory, 'summary_path': summary_path, 'response_path': response_path, 'summary': summary, 'temperature_response': response_dataframe}
```

Calls worth inspecting for I/O, state changes or delegated execution: `_load_json`, `pd.read_csv`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
FileNotFoundError(f'Replica analysis summary was not found:\n{summary_path}')
FileNotFoundError(f'Replica temperature-response file was not found:\n{response_path}')
ValueError(f'Replica analysis belongs to a different system:\nExpected: {expected_system_name}\nFound:    {summary_system}\nReplica:  {simulation_directory.name}')
ValueError(f'Expected a replica-level analysis summary but found:\n{analysis_level}\n{summary_path}')
ValueError(f'Replica temperature-response file is missing columns:\n{sorted(missing_columns)}\n{response_path}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def load_replica_analysis(
    simulation_directory,
    expected_system_name,
):
    """
    Load and validate one completed replica-level Tg analysis.
    """

    analysis_directory = (
        simulation_directory
        / "analysis"
        / "tg_analysis"
    )


    summary_path = (
        analysis_directory
        / "analysis_summary.json"
    )


    response_path = (
        analysis_directory
        / "tg"
        / "temperature_response.csv"
    )


    if not summary_path.is_file():

        raise FileNotFoundError(
            "Replica analysis summary was not found:\n"
            f"{summary_path}"
        )


    if not response_path.is_file():

        raise FileNotFoundError(
            "Replica temperature-response file was not found:\n"
            f"{response_path}"
        )


    summary = (
        _load_json(
            summary_path
        )
    )


    summary_system = (
        summary.get(
            "system"
        )
    )


    if (
        summary_system is not None
        and summary_system
        != expected_system_name
    ):

        raise ValueError(
            "Replica analysis belongs to a different system:\n"
            f"Expected: {expected_system_name}\n"
            f"Found:    {summary_system}\n"
            f"Replica:  {simulation_directory.name}"
        )


    analysis_level = (
        summary.get(
            "analysis_level"
        )
    )


    if (
        analysis_level is not None
        and analysis_level
        != "replica"
    ):

        raise ValueError(
            "Expected a replica-level analysis summary but found:\n"
            f"{analysis_level}\n"
            f"{summary_path}"
        )


    response_dataframe = (
        pd.read_csv(
            response_path
        )
    )


    required_response_columns = {
        "Temperature (K)",
        "Response",
        "Count",
    }


    missing_columns = (
        required_response_columns
        - set(
            response_dataframe.columns
        )
    )


    if missing_columns:

        raise ValueError(
            "Replica temperature-response file is missing columns:\n"
            f"{sorted(missing_columns)}\n"
            f"{response_path}"
        )


    return {
        "simulation_directory":
            simulation_directory,

        "analysis_directory":
            analysis_directory,

        "summary_path":
            summary_path,

        "response_path":
            response_path,

        "summary":
            summary,

        "temperature_response":
            response_dataframe,
    }
```

</details>

<a id="definition-357"></a>

## `build_replica_summary_dataframe`

Source lines 357–552. Named callable; inspect its callers before treating it as a stable public API.

```python
def build_replica_summary_dataframe(replica_analyses): ...
```

### Purpose and original contract

Convert replica JSON summaries into one system-level DataFrame.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| replica_analyses | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `RuntimeError`, `dbscan.get`, `pca.get`, `pd.DataFrame`, `records.append`, `sampling.get`, `summary.get`, `temperature.get`, `tg.get`.

Explicit return expressions; different branches may return different objects:

```python
dataframe
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
RuntimeError('No replica summary data were generated.')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def build_replica_summary_dataframe(
    replica_analyses,
):
    """
    Convert replica JSON summaries into one system-level DataFrame.
    """

    records = []


    for replica in replica_analyses:

        summary = (
            replica[
                "summary"
            ]
        )


        simulation_name = (
            replica[
                "simulation_directory"
            ]
            .name
        )


        sampling = (
            summary.get(
                "sampling",
                {},
            )
        )

        temperature = (
            summary.get(
                "temperature_assignment",
                {},
            )
        )

        pca = (
            summary.get(
                "pca",
                {},
            )
        )

        dbscan = (
            summary.get(
                "dbscan",
                {},
            )
        )

        tg = (
            summary.get(
                "tg",
                {},
            )
        )


        records.append(
            {
                "Simulation":
                    simulation_name,

                "Tg (K)":
                    tg.get(
                        "tg_K"
                    ),

                "Selected PCs":
                    pca.get(
                        "selected_components"
                    ),

                "Median PCA Elbow":
                    pca.get(
                        "median_elbow"
                    ),

                "Mean PCA Elbow":
                    pca.get(
                        "mean_elbow"
                    ),

                "PCA Elbow Q1":
                    pca.get(
                        "elbow_q1"
                    ),

                "PCA Elbow Q3":
                    pca.get(
                        "elbow_q3"
                    ),

                "PCA Consensus Fraction":
                    pca.get(
                        "fraction_within_one_component"
                    ),

                "DBSCAN k":
                    dbscan.get(
                        "k"
                    ),

                "DBSCAN Min Samples":
                    dbscan.get(
                        "selected_min_samples"
                    ),

                "Median Epsilon":
                    dbscan.get(
                        "median_epsilon"
                    ),

                "Mean Epsilon":
                    dbscan.get(
                        "mean_epsilon"
                    ),

                "Median Clusters":
                    dbscan.get(
                        "median_clusters"
                    ),

                "Mean Clusters":
                    dbscan.get(
                        "mean_clusters"
                    ),

                "Median Noise Fraction":
                    dbscan.get(
                        "median_noise_fraction"
                    ),

                "Mean Noise Fraction":
                    dbscan.get(
                        "mean_noise_fraction"
                    ),

                "Sampling Stride":
                    sampling.get(
                        "stride"
                    ),

                "Trajectory Frames":
                    sampling.get(
                        "trajectory_frames"
                    ),

                "Frames Per Chain":
                    sampling.get(
                        "frames_per_chain"
                    ),

                "Polymer Chains":
                    sampling.get(
                        "polymer_chains"
                    ),

                "Temperature Blocks":
                    temperature.get(
                        "n_temperature_blocks"
                    ),

                "Maximum Temperature (K)":
                    temperature.get(
                        "max_temperature_K"
                    ),

                "Minimum Temperature (K)":
                    temperature.get(
                        "min_temperature_K"
                    ),
            }
        )


    dataframe = (
        pd.DataFrame(
            records
        )
    )


    if dataframe.empty:

        raise RuntimeError(
            "No replica summary data were generated."
        )


    return dataframe
```

</details>

<a id="definition-559"></a>

## `build_temperature_response_dataframe`

Source lines 559–607. Named callable; inspect its callers before treating it as a stable public API.

```python
def build_temperature_response_dataframe(replica_analyses): ...
```

### Purpose and original contract

Combine replica-level temperature-response tables.

The responses are concatenated for comparison only.

No averaged response is fitted to produce the final Tg. Each replica Tg
remains an independent fitted quantity.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| replica_analyses | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `dataframe.insert`, `frames.append`, `pd.concat`, `replica['temperature_response'].copy`.

Explicit return expressions; different branches may return different objects:

```python
pd.concat(frames, ignore_index=True)
```

Calls worth inspecting for I/O, state changes or delegated execution: `replica['temperature_response'].copy`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def build_temperature_response_dataframe(
    replica_analyses,
):
    """
    Combine replica-level temperature-response tables.

    The responses are concatenated for comparison only.

    No averaged response is fitted to produce the final Tg. Each replica Tg
    remains an independent fitted quantity.
    """

    frames = []


    for replica in replica_analyses:

        simulation_name = (
            replica[
                "simulation_directory"
            ]
            .name
        )


        dataframe = (
            replica[
                "temperature_response"
            ]
            .copy()
        )


        dataframe.insert(
            0,
            "Simulation",
            simulation_name,
        )


        frames.append(
            dataframe
        )


    return pd.concat(
        frames,
        ignore_index=True,
    )
```

</details>

<a id="definition-614"></a>

## `build_pca_summary_dataframe`

Source lines 614–637. Named callable; inspect its callers before treating it as a stable public API.

```python
def build_pca_summary_dataframe(replica_summary_dataframe): ...
```

### Purpose and original contract

Extract replica PCA diagnostics.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| replica_summary_dataframe | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `replica_summary_dataframe[columns].copy`.

Explicit return expressions; different branches may return different objects:

```python
replica_summary_dataframe[columns].copy()
```

Calls worth inspecting for I/O, state changes or delegated execution: `replica_summary_dataframe[columns].copy`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def build_pca_summary_dataframe(
    replica_summary_dataframe,
):
    """
    Extract replica PCA diagnostics.
    """

    columns = [
        "Simulation",
        "Selected PCs",
        "Median PCA Elbow",
        "Mean PCA Elbow",
        "PCA Elbow Q1",
        "PCA Elbow Q3",
        "PCA Consensus Fraction",
    ]


    return (
        replica_summary_dataframe[
            columns
        ]
        .copy()
    )
```

</details>

<a id="definition-640"></a>

## `build_dbscan_summary_dataframe`

Source lines 640–665. Named callable; inspect its callers before treating it as a stable public API.

```python
def build_dbscan_summary_dataframe(replica_summary_dataframe): ...
```

### Purpose and original contract

Extract replica DBSCAN diagnostics.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| replica_summary_dataframe | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `replica_summary_dataframe[columns].copy`.

Explicit return expressions; different branches may return different objects:

```python
replica_summary_dataframe[columns].copy()
```

Calls worth inspecting for I/O, state changes or delegated execution: `replica_summary_dataframe[columns].copy`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def build_dbscan_summary_dataframe(
    replica_summary_dataframe,
):
    """
    Extract replica DBSCAN diagnostics.
    """

    columns = [
        "Simulation",
        "DBSCAN k",
        "DBSCAN Min Samples",
        "Median Epsilon",
        "Mean Epsilon",
        "Median Clusters",
        "Mean Clusters",
        "Median Noise Fraction",
        "Mean Noise Fraction",
    ]


    return (
        replica_summary_dataframe[
            columns
        ]
        .copy()
    )
```

</details>

<a id="definition-672"></a>

## `calculate_system_tg_statistics`

Source lines 672–757. Named callable; inspect its callers before treating it as a stable public API.

```python
def calculate_system_tg_statistics(replica_summary_dataframe): ...
```

### Purpose and original contract

Calculate system-level Tg statistics from independent replica Tg values.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| replica_summary_dataframe | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `RuntimeError`, `float`, `int`, `len`, `np.max`, `np.mean`, `np.min`, `np.sqrt`, `np.std`, `pd.to_numeric`, `pd.to_numeric(replica_summary_dataframe['Tg (K)'], errors='coerce').dropna`, `pd.to_numeric(replica_summary_dataframe['Tg (K)'], errors='coerce').dropna().to_numpy`.

Explicit return expressions; different branches may return different objects:

```python
{'n_replicas': int(len(tg_values)), 'mean_tg_K': mean_tg, 'sample_sd_tg_K': sd_tg, 'sem_tg_K': sem_tg, 'minimum_tg_K': float(np.min(tg_values)), 'maximum_tg_K': float(np.max(tg_values))}
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
RuntimeError('No valid replica Tg values were found.')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def calculate_system_tg_statistics(
    replica_summary_dataframe,
):
    """
    Calculate system-level Tg statistics from independent replica Tg values.
    """

    tg_values = (
        pd.to_numeric(
            replica_summary_dataframe[
                "Tg (K)"
            ],
            errors="coerce",
        )
        .dropna()
        .to_numpy(
            dtype=float
        )
    )


    if len(tg_values) == 0:

        raise RuntimeError(
            "No valid replica Tg values were found."
        )


    mean_tg = float(
        np.mean(
            tg_values
        )
    )


    if len(tg_values) >= 2:

        sd_tg = float(
            np.std(
                tg_values,
                ddof=1,
            )
        )

        sem_tg = float(
            sd_tg
            / np.sqrt(
                len(tg_values)
            )
        )

    else:

        sd_tg = None
        sem_tg = None


    return {
        "n_replicas":
            int(
                len(tg_values)
            ),

        "mean_tg_K":
            mean_tg,

        "sample_sd_tg_K":
            sd_tg,

        "sem_tg_K":
            sem_tg,

        "minimum_tg_K":
            float(
                np.min(
                    tg_values
                )
            ),

        "maximum_tg_K":
            float(
                np.max(
                    tg_values
                )
            ),
    }
```

</details>

<a id="definition-764"></a>

## `plot_tg_by_replica`

Source lines 764–869. Named callable; inspect its callers before treating it as a stable public API.

```python
def plot_tg_by_replica(replica_summary_dataframe, system_statistics, system_name, output_path): ...
```

### Purpose and original contract

Plot independently fitted Tg values for each replica.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| replica_summary_dataframe | not annotated | required |
| system_statistics | not annotated | required |
| system_name | not annotated | required |
| output_path | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `_save_figure`, `axis.axhline`, `axis.legend`, `axis.scatter`, `axis.set_title`, `axis.set_xlabel`, `axis.set_xticklabels`, `axis.set_xticks`, `axis.set_ylabel`, `dataframe.dropna`, `dataframe.dropna(subset=['Tg (K)']).reset_index`, `len`, `np.arange`, `pd.to_numeric`, `plt.subplots`, `replica_summary_dataframe.copy`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Calls worth inspecting for I/O, state changes or delegated execution: `_save_figure`, `replica_summary_dataframe.copy`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def plot_tg_by_replica(
    replica_summary_dataframe,
    system_statistics,
    system_name,
    output_path,
):
    """
    Plot independently fitted Tg values for each replica.
    """

    dataframe = (
        replica_summary_dataframe
        .copy()
    )


    dataframe[
        "Tg (K)"
    ] = pd.to_numeric(
        dataframe[
            "Tg (K)"
        ],
        errors="coerce",
    )


    dataframe = (
        dataframe
        .dropna(
            subset=[
                "Tg (K)"
            ]
        )
        .reset_index(
            drop=True
        )
    )


    x_positions = np.arange(
        len(
            dataframe
        )
    )


    figure, axis = plt.subplots(
        figsize=(8, 5)
    )


    axis.scatter(
        x_positions,
        dataframe[
            "Tg (K)"
        ],
        s=70,
        label="Replica Tg",
    )


    axis.axhline(
        system_statistics[
            "mean_tg_K"
        ],
        linestyle="--",
        linewidth=1.5,
        label=(
            "Mean Tg = "
            f"{system_statistics['mean_tg_K']:.2f} K"
        ),
    )


    axis.set_xticks(
        x_positions
    )

    axis.set_xticklabels(
        dataframe[
            "Simulation"
        ],
        rotation=45,
        ha="right",
    )


    axis.set_xlabel(
        "Simulation replica"
    )

    axis.set_ylabel(
        "Tg (K)"
    )

    axis.set_title(
        f"{system_name}: Tg by replica"
    )

    axis.legend()


    _save_figure(
        figure,
        output_path,
    )
```

</details>

<a id="definition-876"></a>

## `plot_temperature_response_by_replica`

Source lines 876–941. Named callable; inspect its callers before treating it as a stable public API.

```python
def plot_temperature_response_by_replica(response_dataframe, system_name, output_path): ...
```

### Purpose and original contract

Plot the temperature-response curve from every replica.

These curves are shown for comparison only. They are not averaged and
refitted to obtain the system Tg.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| response_dataframe | not annotated | required |
| system_name | not annotated | required |
| output_path | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `_save_figure`, `axis.legend`, `axis.plot`, `axis.set_title`, `axis.set_xlabel`, `axis.set_ylabel`, `plt.subplots`, `replica_dataframe.sort_values`, `response_dataframe.groupby`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Calls worth inspecting for I/O, state changes or delegated execution: `_save_figure`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def plot_temperature_response_by_replica(
    response_dataframe,
    system_name,
    output_path,
):
    """
    Plot the temperature-response curve from every replica.

    These curves are shown for comparison only. They are not averaged and
    refitted to obtain the system Tg.
    """

    figure, axis = plt.subplots(
        figsize=(8, 5)
    )


    for (
        simulation_name,
        replica_dataframe,
    ) in response_dataframe.groupby(
        "Simulation"
    ):

        replica_dataframe = (
            replica_dataframe
            .sort_values(
                "Temperature (K)"
            )
        )


        axis.plot(
            replica_dataframe[
                "Temperature (K)"
            ],
            replica_dataframe[
                "Response"
            ],
            marker="o",
            markersize=3,
            label=simulation_name,
        )


    axis.set_xlabel(
        "Temperature (K)"
    )

    axis.set_ylabel(
        "Mean DBSCAN cluster-label response"
    )

    axis.set_title(
        f"{system_name}: replica temperature responses"
    )

    axis.legend(
        fontsize="small",
    )


    _save_figure(
        figure,
        output_path,
    )
```

</details>

<a id="definition-948"></a>

## `plot_metric_by_replica`

Source lines 948–1056. Named callable; inspect its callers before treating it as a stable public API.

```python
def plot_metric_by_replica(dataframe, value_column, ylabel, title, output_path): ...
```

### Purpose and original contract

Plot one replica-level diagnostic across simulations.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| dataframe | not annotated | required |
| value_column | not annotated | required |
| ylabel | not annotated | required |
| title | not annotated | required |
| output_path | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `_save_figure`, `axis.plot`, `axis.set_title`, `axis.set_xlabel`, `axis.set_xticklabels`, `axis.set_xticks`, `axis.set_ylabel`, `dataframe[['Simulation', value_column]].copy`, `len`, `np.arange`, `pd.to_numeric`, `plot_dataframe.dropna`, `plot_dataframe.dropna(subset=[value_column]).reset_index`, `plt.subplots`, `print`.

Explicit return expressions; different branches may return different objects:

```python
False
True
```

Calls worth inspecting for I/O, state changes or delegated execution: `_save_figure`, `dataframe[['Simulation', value_column]].copy`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def plot_metric_by_replica(
    dataframe,
    value_column,
    ylabel,
    title,
    output_path,
):
    """
    Plot one replica-level diagnostic across simulations.
    """

    plot_dataframe = (
        dataframe[
            [
                "Simulation",
                value_column,
            ]
        ]
        .copy()
    )


    plot_dataframe[
        value_column
    ] = pd.to_numeric(
        plot_dataframe[
            value_column
        ],
        errors="coerce",
    )


    plot_dataframe = (
        plot_dataframe
        .dropna(
            subset=[
                value_column
            ]
        )
        .reset_index(
            drop=True
        )
    )


    if plot_dataframe.empty:

        print(
            f"WARNING: no valid data for "
            f"'{value_column}'. Figure skipped."
        )

        return False


    x_positions = np.arange(
        len(
            plot_dataframe
        )
    )


    figure, axis = plt.subplots(
        figsize=(8, 5)
    )


    axis.plot(
        x_positions,
        plot_dataframe[
            value_column
        ],
        marker="o",
    )


    axis.set_xticks(
        x_positions
    )

    axis.set_xticklabels(
        plot_dataframe[
            "Simulation"
        ],
        rotation=45,
        ha="right",
    )


    axis.set_xlabel(
        "Simulation replica"
    )

    axis.set_ylabel(
        ylabel
    )

    axis.set_title(
        title
    )


    _save_figure(
        figure,
        output_path,
    )


    return True
```

</details>

<a id="definition-1063"></a>

## `generate_system_figures`

Source lines 1063–1292. Named callable; inspect its callers before treating it as a stable public API.

```python
def generate_system_figures(figure_directory, replica_summary_dataframe, temperature_response_dataframe, system_statistics, system_name): ...
```

### Purpose and original contract

Generate standard system-level Tg comparison figures.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| figure_directory | not annotated | required |
| replica_summary_dataframe | not annotated | required |
| temperature_response_dataframe | not annotated | required |
| system_statistics | not annotated | required |
| system_name | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `figure_directory.mkdir`, `figure_paths.append`, `len`, `plot_metric_by_replica`, `plot_temperature_response_by_replica`, `plot_tg_by_replica`, `print`.

Explicit return expressions; different branches may return different objects:

```python
figure_paths
```

Calls worth inspecting for I/O, state changes or delegated execution: `figure_directory.mkdir`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def generate_system_figures(
    figure_directory,
    replica_summary_dataframe,
    temperature_response_dataframe,
    system_statistics,
    system_name,
):
    """
    Generate standard system-level Tg comparison figures.
    """

    figure_directory.mkdir(
        parents=True,
        exist_ok=True,
    )


    print()
    print(
        "Generating system-level figures"
    )

    print("-" * 80)


    figure_paths = []


    # -------------------------------------------------------------------------
    # Tg by replica
    # -------------------------------------------------------------------------

    path = (
        figure_directory
        / "tg_by_replica.png"
    )


    plot_tg_by_replica(
        replica_summary_dataframe=(
            replica_summary_dataframe
        ),
        system_statistics=(
            system_statistics
        ),
        system_name=(
            system_name
        ),
        output_path=(
            path
        ),
    )


    figure_paths.append(
        path
    )


    # -------------------------------------------------------------------------
    # Temperature response
    # -------------------------------------------------------------------------

    path = (
        figure_directory
        / "temperature_response_by_replica.png"
    )


    plot_temperature_response_by_replica(
        response_dataframe=(
            temperature_response_dataframe
        ),
        system_name=(
            system_name
        ),
        output_path=(
            path
        ),
    )


    figure_paths.append(
        path
    )


    # -------------------------------------------------------------------------
    # PCA dimensionality
    # -------------------------------------------------------------------------

    path = (
        figure_directory
        / "selected_pca_components_by_replica.png"
    )


    if plot_metric_by_replica(
        dataframe=(
            replica_summary_dataframe
        ),
        value_column=(
            "Selected PCs"
        ),
        ylabel=(
            "Selected PCA components"
        ),
        title=(
            f"{system_name}: "
            "selected PCA dimensionality"
        ),
        output_path=(
            path
        ),
    ):

        figure_paths.append(
            path
        )


    # -------------------------------------------------------------------------
    # DBSCAN min_samples
    # -------------------------------------------------------------------------

    path = (
        figure_directory
        / "dbscan_min_samples_by_replica.png"
    )


    if plot_metric_by_replica(
        dataframe=(
            replica_summary_dataframe
        ),
        value_column=(
            "DBSCAN Min Samples"
        ),
        ylabel=(
            "DBSCAN min_samples"
        ),
        title=(
            f"{system_name}: "
            "selected DBSCAN min_samples"
        ),
        output_path=(
            path
        ),
    ):

        figure_paths.append(
            path
        )


    # -------------------------------------------------------------------------
    # DBSCAN epsilon
    # -------------------------------------------------------------------------

    path = (
        figure_directory
        / "dbscan_epsilon_by_replica.png"
    )


    if plot_metric_by_replica(
        dataframe=(
            replica_summary_dataframe
        ),
        value_column=(
            "Median Epsilon"
        ),
        ylabel=(
            "Median DBSCAN epsilon"
        ),
        title=(
            f"{system_name}: "
            "DBSCAN epsilon"
        ),
        output_path=(
            path
        ),
    ):

        figure_paths.append(
            path
        )


    # -------------------------------------------------------------------------
    # DBSCAN noise
    # -------------------------------------------------------------------------

    path = (
        figure_directory
        / "dbscan_noise_fraction_by_replica.png"
    )


    if plot_metric_by_replica(
        dataframe=(
            replica_summary_dataframe
        ),
        value_column=(
            "Median Noise Fraction"
        ),
        ylabel=(
            "Median DBSCAN noise fraction"
        ),
        title=(
            f"{system_name}: "
            "DBSCAN noise fraction"
        ),
        output_path=(
            path
        ),
    ):

        figure_paths.append(
            path
        )


    print(
        f"Generated {len(figure_paths)} "
        "system-level figures."
    )


    return figure_paths
```

</details>

<a id="definition-1299"></a>

## `run_system_tg_analysis`

Source lines 1299–2086. Named callable; inspect its callers before treating it as a stable public API.

```python
def run_system_tg_analysis(system_name, simulation_names=None, generate_figures=False, project_root=None): ...
```

### Purpose and original contract

Combine completed replica-level Tg analyses for one MD system.

Parameters
----------
system_name : str
    Name of the MD system.

simulation_names : iterable of str or None, optional
    Specific replica simulation directories to include.

    If None, all simulations containing:

        analysis/tg_analysis/analysis_summary.json

    are discovered automatically.

generate_figures : bool, optional
    Generate system-level comparison figures.

    Default:
        False

project_root : str or pathlib.Path, optional
    iPHAsimulatorV2 project root.

Returns
-------
dict
    System-level Tg analysis summary.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| system_name | not annotated | required |
| simulation_names | not annotated | None |
| generate_figures | not annotated | False |
| project_root | not annotated | None |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `FileNotFoundError`, `Path`, `Path(__file__).resolve`, `Path(project_root).expanduser`, `Path(project_root).expanduser().resolve`, `RuntimeError`, `ValueError`, `bool`, `build_dbscan_summary_dataframe`, `build_pca_summary_dataframe`, `build_replica_summary_dataframe`, `build_temperature_response_dataframe`, `calculate_system_tg_statistics`, `dbscan_summary_dataframe.to_csv`, `discover_completed_replica_analyses`, `float`, `generate_system_figures`, `int`, `json.dump`, `len`, `list`, `load_replica_analysis`, `open`, `output_directory.mkdir`, `pca_summary_dataframe.to_csv`, `print`, `replica_analyses.append`, `replica_summary_dataframe.to_csv`, `replica_summary_dataframe[['Simulation', 'Tg (K)', 'Selected PCs', 'DBSCAN Min Samples']].to_string`, `simulation_directories.append`, `simulation_directory.is_dir`, `simulations_directory.is_dir`, `str`, `system_directory.is_dir`, `temperature_response_dataframe.to_csv`.

Explicit return expressions; different branches may return different objects:

```python
result
```

Calls worth inspecting for I/O, state changes or delegated execution: `load_replica_analysis`, `open`, `output_directory.mkdir`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
FileNotFoundError(f'System directory was not found:\n{system_directory}')
FileNotFoundError(f'Simulation directory was not found:\n{simulations_directory}')
RuntimeError(f'No completed replica Tg analyses were found beneath:\n{simulations_directory}')
ValueError('simulation_names was supplied but is empty.')
FileNotFoundError(f'Requested simulation directory was not found:\n{simulation_directory}')
re-raises the active exception
RuntimeError('No valid replica analyses could be loaded.')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def run_system_tg_analysis(
    system_name,
    simulation_names=None,
    generate_figures=False,
    project_root=None,
):
    """
    Combine completed replica-level Tg analyses for one MD system.

    Parameters
    ----------
    system_name : str
        Name of the MD system.

    simulation_names : iterable of str or None, optional
        Specific replica simulation directories to include.

        If None, all simulations containing:

            analysis/tg_analysis/analysis_summary.json

        are discovered automatically.

    generate_figures : bool, optional
        Generate system-level comparison figures.

        Default:
            False

    project_root : str or pathlib.Path, optional
        iPHAsimulatorV2 project root.

    Returns
    -------
    dict
        System-level Tg analysis summary.
    """

    # =========================================================================
    # Resolve paths
    # =========================================================================

    if project_root is None:

        project_root = (
            Path(__file__)
            .resolve()
            .parents[4]
        )

    else:

        project_root = (
            Path(project_root)
            .expanduser()
            .resolve()
        )


    system_directory = (
        project_root
        / "structure_database"
        / "PHA_melts"
        / system_name
    )


    simulations_directory = (
        system_directory
        / "simulations"
    )


    output_directory = (
        system_directory
        / "analysis"
        / "tg_analysis"
    )


    figure_directory = (
        output_directory
        / "figures"
    )


    # =========================================================================
    # Validate system
    # =========================================================================

    if not system_directory.is_dir():

        raise FileNotFoundError(
            "System directory was not found:\n"
            f"{system_directory}"
        )


    if not simulations_directory.is_dir():

        raise FileNotFoundError(
            "Simulation directory was not found:\n"
            f"{simulations_directory}"
        )


    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )


    # =========================================================================
    # Header
    # =========================================================================

    print()
    print("=" * 80)
    print(
        "SYSTEM-LEVEL Tg ANALYSIS"
    )
    print("=" * 80)

    print(
        f"System:      "
        f"{system_name}"
    )

    print(
        f"Input:       "
        f"{simulations_directory}"
    )

    print(
        f"Output:      "
        f"{output_directory}"
    )

    print(
        f"Figures:     "
        f"{generate_figures}"
    )

    print("=" * 80)


    # =========================================================================
    # STEP 1
    # Resolve replica simulations
    # =========================================================================

    print()
    print(
        "Step 1: resolving replica analyses"
    )

    print("-" * 80)


    if simulation_names is None:

        simulation_directories = (
            discover_completed_replica_analyses(
                simulations_directory
            )
        )


        if not simulation_directories:

            raise RuntimeError(
                "No completed replica Tg analyses were found beneath:\n"
                f"{simulations_directory}"
            )


        print(
            "Automatically discovered completed replicas:"
        )


    else:

        simulation_names = list(
            simulation_names
        )


        if not simulation_names:

            raise ValueError(
                "simulation_names was supplied but is empty."
            )


        simulation_directories = []


        for simulation_name in (
            simulation_names
        ):

            simulation_directory = (
                simulations_directory
                / simulation_name
            )


            if not simulation_directory.is_dir():

                raise FileNotFoundError(
                    "Requested simulation directory "
                    "was not found:\n"
                    f"{simulation_directory}"
                )


            simulation_directories.append(
                simulation_directory
            )


        print(
            "Using explicitly selected replicas:"
        )


    for simulation_directory in (
        simulation_directories
    ):

        print(
            f"  - {simulation_directory.name}"
        )


    # =========================================================================
    # STEP 2
    # Load replica analyses
    # =========================================================================

    print()
    print(
        "Step 2: loading completed replica analyses"
    )

    print("-" * 80)


    replica_analyses = []


    for simulation_directory in (
        simulation_directories
    ):

        try:

            replica = (
                load_replica_analysis(
                    simulation_directory=(
                        simulation_directory
                    ),
                    expected_system_name=(
                        system_name
                    ),
                )
            )


            replica_analyses.append(
                replica
            )


            print(
                f"Loaded: "
                f"{simulation_directory.name}"
            )


        except Exception as error:

            if simulation_names is None:

                print(
                    f"WARNING: skipping "
                    f"{simulation_directory.name}"
                )

                print(
                    f"         {error}"
                )

                continue


            raise


    if not replica_analyses:

        raise RuntimeError(
            "No valid replica analyses could be loaded."
        )


    print(
        f"Valid replica analyses: "
        f"{len(replica_analyses)}"
    )


    if len(replica_analyses) < 2:

        print(
            "WARNING: only one valid replica was found. "
            "A system mean can be reported, but a sample "
            "standard deviation cannot yet be calculated."
        )


    # =========================================================================
    # STEP 3
    # Build replica summary
    # =========================================================================

    print()
    print(
        "Step 3: building replica summary table"
    )

    print("-" * 80)


    replica_summary_dataframe = (
        build_replica_summary_dataframe(
            replica_analyses
        )
    )


    print(
        replica_summary_dataframe[
            [
                "Simulation",
                "Tg (K)",
                "Selected PCs",
                "DBSCAN Min Samples",
            ]
        ]
        .to_string(
            index=False
        )
    )


    # =========================================================================
    # STEP 4
    # Calculate system Tg statistics
    # =========================================================================

    print()
    print(
        "Step 4: calculating system Tg statistics"
    )

    print("-" * 80)


    system_statistics = (
        calculate_system_tg_statistics(
            replica_summary_dataframe
        )
    )


    print(
        f"Replicas: "
        f"{system_statistics['n_replicas']}"
    )

    print(
        f"Mean Tg:  "
        f"{system_statistics['mean_tg_K']:.2f} K"
    )


    if (
        system_statistics[
            "sample_sd_tg_K"
        ]
        is not None
    ):

        print(
            f"SD:       "
            f"{system_statistics['sample_sd_tg_K']:.2f} K"
        )

        print(
            f"System Tg: "
            f"{system_statistics['mean_tg_K']:.2f} ± "
            f"{system_statistics['sample_sd_tg_K']:.2f} K"
        )

    else:

        print(
            "SD:       unavailable "
            "(requires at least two replicas)"
        )


    # =========================================================================
    # STEP 5
    # Combine saved replica outputs
    # =========================================================================

    print()
    print(
        "Step 5: combining replica analysis outputs"
    )

    print("-" * 80)


    temperature_response_dataframe = (
        build_temperature_response_dataframe(
            replica_analyses
        )
    )


    pca_summary_dataframe = (
        build_pca_summary_dataframe(
            replica_summary_dataframe
        )
    )


    dbscan_summary_dataframe = (
        build_dbscan_summary_dataframe(
            replica_summary_dataframe
        )
    )


    print(
        f"Temperature-response rows: "
        f"{len(temperature_response_dataframe)}"
    )


    # =========================================================================
    # STEP 6
    # Save system-level outputs
    # =========================================================================

    print()
    print(
        "Step 6: saving system-level outputs"
    )

    print("-" * 80)


    replica_summary_path = (
        output_directory
        / "replica_summary.csv"
    )


    replica_summary_dataframe.to_csv(
        replica_summary_path,
        index=False,
    )


    response_path = (
        output_directory
        / "temperature_response_by_replica.csv"
    )


    temperature_response_dataframe.to_csv(
        response_path,
        index=False,
    )


    pca_summary_path = (
        output_directory
        / "pca_summary_by_replica.csv"
    )


    pca_summary_dataframe.to_csv(
        pca_summary_path,
        index=False,
    )


    dbscan_summary_path = (
        output_directory
        / "dbscan_summary_by_replica.csv"
    )


    dbscan_summary_dataframe.to_csv(
        dbscan_summary_path,
        index=False,
    )


    replica_names = [
        replica[
            "simulation_directory"
        ].name
        for replica in replica_analyses
    ]


    system_summary = {

        "analysis_level":
            "system",

        "system":
            system_name,

        "replicas":
            replica_names,

        "n_replicas":
            int(
                len(
                    replica_names
                )
            ),

        "tg": {

            "aggregation":
                "mean_of_independently_fitted_replica_tg_values",

            "mean_tg_K":
                system_statistics[
                    "mean_tg_K"
                ],

            "sample_sd_tg_K":
                system_statistics[
                    "sample_sd_tg_K"
                ],

            "sem_tg_K":
                system_statistics[
                    "sem_tg_K"
                ],

            "minimum_tg_K":
                system_statistics[
                    "minimum_tg_K"
                ],

            "maximum_tg_K":
                system_statistics[
                    "maximum_tg_K"
                ],
        },

        "outputs": {

            "replica_summary":
                replica_summary_path.name,

            "temperature_response":
                response_path.name,

            "pca_summary":
                pca_summary_path.name,

            "dbscan_summary":
                dbscan_summary_path.name,
        },

        "figures_generated":
            bool(
                generate_figures
            ),
    }


    system_summary_path = (
        output_directory
        / "system_summary.json"
    )


    with open(
        system_summary_path,
        "w",
        encoding="utf-8",
    ) as handle:

        json.dump(
            system_summary,
            handle,
            indent=4,
        )


    # =========================================================================
    # STEP 7
    # Optional figures
    # =========================================================================

    figure_paths = []


    if generate_figures:

        print()
        print(
            "Step 7: generating system-level figures"
        )

        print("-" * 80)


        figure_paths = (
            generate_system_figures(
                figure_directory=(
                    figure_directory
                ),
                replica_summary_dataframe=(
                    replica_summary_dataframe
                ),
                temperature_response_dataframe=(
                    temperature_response_dataframe
                ),
                system_statistics=(
                    system_statistics
                ),
                system_name=(
                    system_name
                ),
            )
        )


    # =========================================================================
    # Result
    # =========================================================================

    result = {

        "analysis_level":
            "system",

        "system_name":
            system_name,

        "replicas":
            replica_names,

        "n_replicas":
            int(
                len(
                    replica_names
                )
            ),

        "mean_tg_K":
            float(
                system_statistics[
                    "mean_tg_K"
                ]
            ),

        "sample_sd_tg_K":
            system_statistics[
                "sample_sd_tg_K"
            ],

        "output_directory":
            str(
                output_directory
            ),

        "system_summary_path":
            str(
                system_summary_path
            ),

        "figure_directory":
            (
                str(
                    figure_directory
                )
                if generate_figures
                else None
            ),

        "n_figures":
            int(
                len(
                    figure_paths
                )
            ),
    }


    # =========================================================================
    # Final report
    # =========================================================================

    print()
    print("=" * 80)
    print(
        "SYSTEM-LEVEL Tg ANALYSIS COMPLETE"
    )
    print("=" * 80)

    print(
        f"System:            "
        f"{system_name}"
    )

    print(
        f"Replicas analysed: "
        f"{len(replica_names)}"
    )


    for replica_name in (
        replica_names
    ):

        print(
            f"  - {replica_name}"
        )


    print(
        f"Mean Tg:           "
        f"{system_statistics['mean_tg_K']:.2f} K"
    )


    if (
        system_statistics[
            "sample_sd_tg_K"
        ]
        is not None
    ):

        print(
            f"Sample SD:         "
            f"{system_statistics['sample_sd_tg_K']:.2f} K"
        )

        print(
            f"System Tg:         "
            f"{system_statistics['mean_tg_K']:.2f} ± "
            f"{system_statistics['sample_sd_tg_K']:.2f} K"
        )


    print(
        f"Output:            "
        f"{output_directory}"
    )


    if generate_figures:

        print(
            f"Figures:           "
            f"{figure_directory}"
        )


    print("=" * 80)


    return result
```

</details>
