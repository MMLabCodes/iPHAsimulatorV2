# analysis/tg_analysis/workflow.py

Replica orchestration plus output writing, plots and text reports. Load, assign temperatures, describe, optimise PCA/DBSCAN, fit, preserve conformational states, then save diagnostics. The system path currently targets PHA_melts. Summary output is written before optional plotting completes, so inspect full-run status as well as file presence.

[Current source](../../src/iphasimulator/analysis/tg_analysis/workflow.py)

This page is generated from source syntax. Original docstrings can be incomplete or outdated; module notes above identify known discrepancies. Call/return/error lists describe direct syntax, not all behaviour inside callees. Read the source excerpt for branch order and effects. No scientific execution is implied.

Explicit functions/methods/nested helpers: **17**.

## Module imports

```python
from __future__ import annotations
from pathlib import Path
import json
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from iphasimulator.analysis.simulation_loader import load_simulation
from iphasimulator.analysis.descriptors import calculate_all_chain_distance_descriptors
from iphasimulator.analysis.tg_analysis.temperature_assignment import assign_nominal_temperatures
from iphasimulator.analysis.tg_analysis.optimisation import optimise_pca_dimensionality, calculate_optimised_pca, optimise_dbscan
from iphasimulator.analysis.tg_analysis.clustering import cluster_all_chain_pca
from iphasimulator.analysis.tg_analysis.glass_transition import calculate_historical_cluster_response, fit_historical_tg
```

## Function map

- [`_save_figure` — source line 108](#definition-108)
- [`plot_temperature_block_agreement` — source line 143](#definition-143)
- [`plot_pca_scree` — source line 297](#definition-297)
- [`plot_pca_elbow_distribution` — source line 396](#definition-396)
- [`_summarise_dbscan_parameter` — source line 499](#definition-499)
- [`plot_dbscan_noise` — source line 536](#definition-536)
- [`plot_dbscan_clusters` — source line 611](#definition-611)
- [`plot_dbscan_ari` — source line 686](#definition-686)
- [`_historical_tg_model` — source line 806](#definition-806)
- [`plot_tg_fit` — source line 843](#definition-843)
- [`build_conformational_state_dataframe` — source line 953](#definition-953)
- [`plot_chain_pca_temperature` — source line 1185](#definition-1185)
- [`plot_chain_pca_dbscan` — source line 1272](#definition-1272)
- [`generate_chain_pca_figures` — source line 1386](#definition-1386)
- [`generate_analysis_figures` — source line 1516](#definition-1516)
- [`write_analysis_report` — source line 1767](#definition-1767)
- [`run_tg_analysis` — source line 2029](#definition-2029)

<a id="definition-108"></a>

## `_save_figure`

Source lines 108–136. Internal helper/protocol method.

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

<a id="definition-143"></a>

## `plot_temperature_block_agreement`

Source lines 143–290. Named callable; inspect its callers before treating it as a stable public API.

```python
def plot_temperature_block_agreement(temperatures, simulation_data, output_path): ...
```

### Purpose and original contract

Plot nominal temperature against mean recorded temperature.

Error bars represent the standard deviation of the instantaneous
recorded temperature within each nominal temperature block.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| temperatures | not annotated | required |
| simulation_data | not annotated | required |
| output_path | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `_save_figure`, `axis.errorbar`, `axis.legend`, `axis.plot`, `axis.set_title`, `axis.set_xlabel`, `axis.set_ylabel`, `block_statistics['Mean_Recorded_Temperature'].max`, `block_statistics['Mean_Recorded_Temperature'].min`, `block_statistics['Nominal Temperature (K)'].max`, `block_statistics['Nominal Temperature (K)'].min`, `comparison.groupby`, `comparison.groupby('Nominal Temperature (K)', as_index=False).agg`, `comparison.groupby('Nominal Temperature (K)', as_index=False).agg(Mean_Recorded_Temperature=('Recorded Temperature (K)', 'mean'), Temperature_SD=('Recorded Temperature (K)', 'std')).sort_values`, `max`, `min`, `plt.subplots`, `print`, `simulation_data[required_column].to_numpy`, `temperatures[['Nominal Temperature (K)']].copy`.

Explicit return expressions; different branches may return different objects:

```python
False
True
```

Calls worth inspecting for I/O, state changes or delegated execution: `_save_figure`, `temperatures[['Nominal Temperature (K)']].copy`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def plot_temperature_block_agreement(
    temperatures,
    simulation_data,
    output_path,
):
    """
    Plot nominal temperature against mean recorded temperature.

    Error bars represent the standard deviation of the instantaneous
    recorded temperature within each nominal temperature block.
    """

    required_column = (
        "Temperature (K)"
    )

    if (
        required_column
        not in simulation_data.columns
    ):

        print(
            "WARNING: temperature_block_agreement.png "
            "was not generated because the state-data "
            "file does not contain 'Temperature (K)'."
        )

        return False


    comparison = (
        temperatures[
            [
                "Nominal Temperature (K)"
            ]
        ]
        .copy()
    )


    comparison[
        "Recorded Temperature (K)"
    ] = (
        simulation_data[
            required_column
        ]
        .to_numpy()
    )


    block_statistics = (
        comparison
        .groupby(
            "Nominal Temperature (K)",
            as_index=False,
        )
        .agg(
            Mean_Recorded_Temperature=(
                "Recorded Temperature (K)",
                "mean",
            ),
            Temperature_SD=(
                "Recorded Temperature (K)",
                "std",
            ),
        )
        .sort_values(
            "Nominal Temperature (K)"
        )
    )


    figure, axis = plt.subplots(
        figsize=(7, 6)
    )


    axis.errorbar(
        block_statistics[
            "Nominal Temperature (K)"
        ],
        block_statistics[
            "Mean_Recorded_Temperature"
        ],
        yerr=block_statistics[
            "Temperature_SD"
        ],
        marker="o",
        linestyle="none",
        capsize=2,
        label="Recorded block mean ± SD",
    )


    temperature_min = min(
        block_statistics[
            "Nominal Temperature (K)"
        ].min(),
        block_statistics[
            "Mean_Recorded_Temperature"
        ].min(),
    )

    temperature_max = max(
        block_statistics[
            "Nominal Temperature (K)"
        ].max(),
        block_statistics[
            "Mean_Recorded_Temperature"
        ].max(),
    )


    axis.plot(
        [
            temperature_min,
            temperature_max,
        ],
        [
            temperature_min,
            temperature_max,
        ],
        linestyle="--",
        label="Ideal agreement",
    )


    axis.set_xlabel(
        "Nominal temperature (K)"
    )

    axis.set_ylabel(
        "Mean recorded temperature (K)"
    )

    axis.set_title(
        "Temperature-block agreement"
    )

    axis.legend()


    _save_figure(
        figure,
        output_path,
    )

    return True
```

</details>

<a id="definition-297"></a>

## `plot_pca_scree`

Source lines 297–389. Named callable; inspect its callers before treating it as a stable public API.

```python
def plot_pca_scree(pca_optimisation, output_path): ...
```

### Purpose and original contract

Plot the median PCA scree curve across polymer chains.

The interquartile range across chains is shown as a shaded region.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| pca_optimisation | not annotated | required |
| output_path | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `_save_figure`, `axis.axvline`, `axis.fill_between`, `axis.legend`, `axis.plot`, `axis.set_title`, `axis.set_xlabel`, `axis.set_ylabel`, `pca_optimisation.spectra_dataframe.copy`, `plt.subplots`, `spectra.groupby`, `spectra.groupby('PC', as_index=False).agg`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Calls worth inspecting for I/O, state changes or delegated execution: `_save_figure`, `pca_optimisation.spectra_dataframe.copy`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def plot_pca_scree(
    pca_optimisation,
    output_path,
):
    """
    Plot the median PCA scree curve across polymer chains.

    The interquartile range across chains is shown as a shaded region.
    """

    spectra = (
        pca_optimisation
        .spectra_dataframe
        .copy()
    )


    summary = (
        spectra
        .groupby(
            "PC",
            as_index=False,
        )
        .agg(
            Median=(
                "Explained Variance",
                "median",
            ),
            Q1=(
                "Explained Variance",
                lambda values:
                    values.quantile(0.25),
            ),
            Q3=(
                "Explained Variance",
                lambda values:
                    values.quantile(0.75),
            ),
        )
    )


    figure, axis = plt.subplots(
        figsize=(7, 5)
    )


    axis.plot(
        summary["PC"],
        summary["Median"] * 100,
        marker="o",
        label="Median spectrum",
    )


    axis.fill_between(
        summary["PC"],
        summary["Q1"] * 100,
        summary["Q3"] * 100,
        alpha=0.25,
        label="Chain Q1–Q3",
    )


    axis.axvline(
        pca_optimisation.selected_components,
        linestyle="--",
        label=(
            "Selected PCs = "
            f"{pca_optimisation.selected_components}"
        ),
    )


    axis.set_xlabel(
        "Principal component"
    )

    axis.set_ylabel(
        "Explained variance (%)"
    )

    axis.set_title(
        "PCA scree analysis"
    )

    axis.legend()


    _save_figure(
        figure,
        output_path,
    )
```

</details>

<a id="definition-396"></a>

## `plot_pca_elbow_distribution`

Source lines 396–492. Named callable; inspect its callers before treating it as a stable public API.

```python
def plot_pca_elbow_distribution(pca_optimisation, output_path): ...
```

### Purpose and original contract

Plot the distribution of PCA elbow positions across polymer chains.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| pca_optimisation | not annotated | required |
| output_path | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `_save_figure`, `axis.axvline`, `axis.hist`, `axis.legend`, `axis.set_title`, `axis.set_xlabel`, `axis.set_xticks`, `axis.set_ylabel`, `elbows.max`, `elbows.min`, `int`, `len`, `np.arange`, `pca_optimisation.dimensionality_dataframe['Elbow PC'].dropna`, `pca_optimisation.dimensionality_dataframe['Elbow PC'].dropna().astype`, `pca_optimisation.dimensionality_dataframe['Elbow PC'].dropna().astype(int).to_numpy`, `plt.subplots`, `print`.

Explicit return expressions; different branches may return different objects:

```python
False
True
```

Calls worth inspecting for I/O, state changes or delegated execution: `_save_figure`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def plot_pca_elbow_distribution(
    pca_optimisation,
    output_path,
):
    """
    Plot the distribution of PCA elbow positions across polymer chains.
    """

    elbows = (
        pca_optimisation
        .dimensionality_dataframe[
            "Elbow PC"
        ]
        .dropna()
        .astype(int)
        .to_numpy()
    )


    if len(elbows) == 0:

        print(
            "WARNING: no PCA elbows available; "
            "PCA elbow figure skipped."
        )

        return False


    minimum = int(
        elbows.min()
    )

    maximum = int(
        elbows.max()
    )


    bins = np.arange(
        minimum - 0.5,
        maximum + 1.5,
        1,
    )


    figure, axis = plt.subplots(
        figsize=(7, 5)
    )


    axis.hist(
        elbows,
        bins=bins,
        edgecolor="black",
    )


    axis.axvline(
        pca_optimisation.selected_components,
        linestyle="--",
        linewidth=2,
        label=(
            "Selected PCs = "
            f"{pca_optimisation.selected_components}"
        ),
    )


    axis.set_xlabel(
        "PCA elbow position"
    )

    axis.set_ylabel(
        "Number of polymer chains"
    )

    axis.set_title(
        "Distribution of chain-level PCA elbows"
    )


    axis.set_xticks(
        np.arange(
            minimum,
            maximum + 1,
        )
    )

    axis.legend()


    _save_figure(
        figure,
        output_path,
    )

    return True
```

</details>

<a id="definition-499"></a>

## `_summarise_dbscan_parameter`

Source lines 499–529. Internal helper/protocol method.

```python
def _summarise_dbscan_parameter(parameter_dataframe, value_column): ...
```

### Purpose and original contract

Calculate median and IQR across chains for one DBSCAN diagnostic.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| parameter_dataframe | not annotated | required |
| value_column | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `parameter_dataframe.groupby`, `parameter_dataframe.groupby('Min Samples', as_index=False).agg`.

Explicit return expressions; different branches may return different objects:

```python
parameter_dataframe.groupby('Min Samples', as_index=False).agg(Median=(value_column, 'median'), Q1=(value_column, lambda values: values.quantile(0.25)), Q3=(value_column, lambda values: values.quantile(0.75)))
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _summarise_dbscan_parameter(
    parameter_dataframe,
    value_column,
):
    """
    Calculate median and IQR across chains for one DBSCAN diagnostic.
    """

    return (
        parameter_dataframe
        .groupby(
            "Min Samples",
            as_index=False,
        )
        .agg(
            Median=(
                value_column,
                "median",
            ),
            Q1=(
                value_column,
                lambda values:
                    values.quantile(0.25),
            ),
            Q3=(
                value_column,
                lambda values:
                    values.quantile(0.75),
            ),
        )
    )
```

</details>

<a id="definition-536"></a>

## `plot_dbscan_noise`

Source lines 536–604. Named callable; inspect its callers before treating it as a stable public API.

```python
def plot_dbscan_noise(dbscan_optimisation, output_path): ...
```

### Purpose and original contract

Plot DBSCAN noise fraction against min_samples.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| dbscan_optimisation | not annotated | required |
| output_path | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `_save_figure`, `_summarise_dbscan_parameter`, `axis.axvline`, `axis.fill_between`, `axis.legend`, `axis.plot`, `axis.set_title`, `axis.set_xlabel`, `axis.set_ylabel`, `plt.subplots`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Calls worth inspecting for I/O, state changes or delegated execution: `_save_figure`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def plot_dbscan_noise(
    dbscan_optimisation,
    output_path,
):
    """
    Plot DBSCAN noise fraction against min_samples.
    """

    summary = (
        _summarise_dbscan_parameter(
            dbscan_optimisation
            .parameter_dataframe,
            "Noise Fraction",
        )
    )


    figure, axis = plt.subplots(
        figsize=(7, 5)
    )


    axis.plot(
        summary["Min Samples"],
        summary["Median"] * 100,
        marker="o",
        label="Median noise fraction",
    )


    axis.fill_between(
        summary["Min Samples"],
        summary["Q1"] * 100,
        summary["Q3"] * 100,
        alpha=0.25,
        label="Chain Q1–Q3",
    )


    axis.axvline(
        dbscan_optimisation
        .selected_min_samples,
        linestyle="--",
        label=(
            "Selected min_samples = "
            f"{dbscan_optimisation.selected_min_samples}"
        ),
    )


    axis.set_xlabel(
        "DBSCAN min_samples"
    )

    axis.set_ylabel(
        "Noise fraction (%)"
    )

    axis.set_title(
        "DBSCAN noise sensitivity"
    )

    axis.legend()


    _save_figure(
        figure,
        output_path,
    )
```

</details>

<a id="definition-611"></a>

## `plot_dbscan_clusters`

Source lines 611–679. Named callable; inspect its callers before treating it as a stable public API.

```python
def plot_dbscan_clusters(dbscan_optimisation, output_path): ...
```

### Purpose and original contract

Plot the number of DBSCAN clusters against min_samples.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| dbscan_optimisation | not annotated | required |
| output_path | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `_save_figure`, `_summarise_dbscan_parameter`, `axis.axvline`, `axis.fill_between`, `axis.legend`, `axis.plot`, `axis.set_title`, `axis.set_xlabel`, `axis.set_ylabel`, `plt.subplots`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Calls worth inspecting for I/O, state changes or delegated execution: `_save_figure`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def plot_dbscan_clusters(
    dbscan_optimisation,
    output_path,
):
    """
    Plot the number of DBSCAN clusters against min_samples.
    """

    summary = (
        _summarise_dbscan_parameter(
            dbscan_optimisation
            .parameter_dataframe,
            "Clusters",
        )
    )


    figure, axis = plt.subplots(
        figsize=(7, 5)
    )


    axis.plot(
        summary["Min Samples"],
        summary["Median"],
        marker="o",
        label="Median clusters",
    )


    axis.fill_between(
        summary["Min Samples"],
        summary["Q1"],
        summary["Q3"],
        alpha=0.25,
        label="Chain Q1–Q3",
    )


    axis.axvline(
        dbscan_optimisation
        .selected_min_samples,
        linestyle="--",
        label=(
            "Selected min_samples = "
            f"{dbscan_optimisation.selected_min_samples}"
        ),
    )


    axis.set_xlabel(
        "DBSCAN min_samples"
    )

    axis.set_ylabel(
        "Number of clusters"
    )

    axis.set_title(
        "DBSCAN cluster-count sensitivity"
    )

    axis.legend()


    _save_figure(
        figure,
        output_path,
    )
```

</details>

<a id="definition-686"></a>

## `plot_dbscan_ari`

Source lines 686–799. Named callable; inspect its callers before treating it as a stable public API.

```python
def plot_dbscan_ari(dbscan_optimisation, output_path): ...
```

### Purpose and original contract

Plot adjacent-min_samples Adjusted Rand Index stability.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| dbscan_optimisation | not annotated | required |
| output_path | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `_save_figure`, `axis.axvline`, `axis.fill_between`, `axis.legend`, `axis.plot`, `axis.set_title`, `axis.set_xlabel`, `axis.set_ylabel`, `axis.set_ylim`, `dbscan_optimisation.stability_dataframe.copy`, `plt.subplots`, `print`, `stability.groupby`, `stability.groupby('Min Samples', as_index=False).agg`.

Explicit return expressions; different branches may return different objects:

```python
False
True
```

Calls worth inspecting for I/O, state changes or delegated execution: `_save_figure`, `dbscan_optimisation.stability_dataframe.copy`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def plot_dbscan_ari(
    dbscan_optimisation,
    output_path,
):
    """
    Plot adjacent-min_samples Adjusted Rand Index stability.
    """

    stability = (
        dbscan_optimisation
        .stability_dataframe
        .copy()
    )


    if (
        stability.empty
        or "ARI All"
        not in stability.columns
    ):

        print(
            "WARNING: DBSCAN ARI figure skipped "
            "because no ARI stability data are available."
        )

        return False


    summary = (
        stability
        .groupby(
            "Min Samples",
            as_index=False,
        )
        .agg(
            Median=(
                "ARI All",
                "median",
            ),
            Q1=(
                "ARI All",
                lambda values:
                    values.quantile(0.25),
            ),
            Q3=(
                "ARI All",
                lambda values:
                    values.quantile(0.75),
            ),
        )
    )


    figure, axis = plt.subplots(
        figsize=(7, 5)
    )


    axis.plot(
        summary["Min Samples"],
        summary["Median"],
        marker="o",
        label="Median adjacent ARI",
    )


    axis.fill_between(
        summary["Min Samples"],
        summary["Q1"],
        summary["Q3"],
        alpha=0.25,
        label="Chain Q1–Q3",
    )


    axis.axvline(
        dbscan_optimisation
        .selected_min_samples,
        linestyle="--",
        label=(
            "Selected min_samples = "
            f"{dbscan_optimisation.selected_min_samples}"
        ),
    )


    axis.set_xlabel(
        "DBSCAN min_samples"
    )

    axis.set_ylabel(
        "Adjusted Rand Index"
    )

    axis.set_title(
        "DBSCAN adjacent-parameter stability"
    )


    axis.set_ylim(
        -0.05,
        1.05,
    )

    axis.legend()


    _save_figure(
        figure,
        output_path,
    )

    return True
```

</details>

<a id="definition-806"></a>

## `_historical_tg_model`

Source lines 806–836. Internal helper/protocol method.

```python
def _historical_tg_model(temperature, C, s, d): ...
```

### Purpose and original contract

Evaluate the historical hyperbolic-tangent Tg response model.

g(T) = C/2 * (1 - tanh(sT - d)) - 1

Tg = d / s

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| temperature | not annotated | required |
| C | not annotated | required |
| s | not annotated | required |
| d | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `np.asarray`, `np.tanh`.

Explicit return expressions; different branches may return different objects:

```python
C / 2.0 * (1.0 - np.tanh(s * temperature - d)) - 1.0
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _historical_tg_model(
    temperature,
    C,
    s,
    d,
):
    """
    Evaluate the historical hyperbolic-tangent Tg response model.

    g(T) = C/2 * (1 - tanh(sT - d)) - 1

    Tg = d / s
    """

    temperature = np.asarray(
        temperature,
        dtype=float,
    )


    return (
        (C / 2.0)
        * (
            1.0
            - np.tanh(
                s * temperature
                - d
            )
        )
        - 1.0
    )
```

</details>

<a id="definition-843"></a>

## `plot_tg_fit`

Source lines 843–946. Named callable; inspect its callers before treating it as a stable public API.

```python
def plot_tg_fit(temperature_response, tg_result, system_name, simulation_name, output_path): ...
```

### Purpose and original contract

Plot the historical temperature response and fitted Tg model.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| temperature_response | not annotated | required |
| tg_result | not annotated | required |
| system_name | not annotated | required |
| simulation_name | not annotated | required |
| output_path | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `_historical_tg_model`, `_save_figure`, `axis.axvline`, `axis.legend`, `axis.plot`, `axis.scatter`, `axis.set_title`, `axis.set_xlabel`, `axis.set_ylabel`, `np.argsort`, `np.asarray`, `np.linspace`, `plt.subplots`, `temperatures.max`, `temperatures.min`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Calls worth inspecting for I/O, state changes or delegated execution: `_save_figure`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def plot_tg_fit(
    temperature_response,
    tg_result,
    system_name,
    simulation_name,
    output_path,
):
    """
    Plot the historical temperature response and fitted Tg model.
    """

    temperatures = np.asarray(
        temperature_response
        .temperatures,
        dtype=float,
    )

    response = np.asarray(
        temperature_response
        .response,
        dtype=float,
    )


    sort_order = np.argsort(
        temperatures
    )


    temperatures = temperatures[
        sort_order
    ]

    response = response[
        sort_order
    ]


    fit_temperatures = np.linspace(
        temperatures.min(),
        temperatures.max(),
        500,
    )


    fitted_response = (
        _historical_tg_model(
            fit_temperatures,
            tg_result.C,
            tg_result.s,
            tg_result.d,
        )
    )


    figure, axis = plt.subplots(
        figsize=(8, 5)
    )


    axis.scatter(
        temperatures,
        response,
        label="Temperature response",
    )


    axis.plot(
        fit_temperatures,
        fitted_response,
        linewidth=2,
        label="Hyperbolic-tangent fit",
    )


    axis.axvline(
        tg_result.tg,
        linestyle="--",
        linewidth=2,
        label=(
            f"Tg = {tg_result.tg:.2f} K"
        ),
    )


    axis.set_xlabel(
        "Temperature (K)"
    )

    axis.set_ylabel(
        "Mean DBSCAN cluster-label response"
    )

    axis.set_title(
        f"{system_name} | {simulation_name}"
    )

    axis.legend()


    _save_figure(
        figure,
        output_path,
    )
```

</details>

<a id="definition-953"></a>

## `build_conformational_state_dataframe`

Source lines 953–1178. Named callable; inspect its callers before treating it as a stable public API.

```python
def build_conformational_state_dataframe(all_descriptors, pca_results, clustering_results, temperature_assignment): ...
```

### Purpose and original contract

Build a reusable chain/frame-level conformational-state table.

One row corresponds to one sampled trajectory frame for one polymer
chain.

Columns include:

- chain analysis identifier
- original topology segid, where available
- trajectory frame
- nominal temperature
- all selected principal components
- final DBSCAN label
- DBSCAN noise status

Notes
-----
PCA is performed independently for each polymer chain. Consequently,
PC coordinates belonging to different chains should not automatically
be interpreted as sharing a common PCA basis.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| all_descriptors | not annotated | required |
| pca_results | not annotated | required |
| clustering_results | not annotated | required |
| temperature_assignment | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `IndexError`, `KeyError`, `RuntimeError`, `ValueError`, `all_descriptors.items`, `bool`, `float`, `frame_indices.max`, `getattr`, `int`, `len`, `np.asarray`, `pd.DataFrame`, `range`, `records.append`, `temperature_assignment.iloc[frame_indices][temperature_column].to_numpy`.

Explicit return expressions; different branches may return different objects:

```python
dataframe
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
KeyError(f"PCA results are missing for chain '{chain_id}'.")
KeyError(f"DBSCAN results are missing for chain '{chain_id}'.")
ValueError(f'PCA/frame count mismatch for {chain_id}:\nFrames: {n_samples}\nPCA rows: {transformed_data.shape[0]}')
ValueError(f'DBSCAN/frame count mismatch for {chain_id}:\nFrames: {n_samples}\nLabels: {len(labels)}')
IndexError(f'Sampled frame index for {chain_id} exceeds the temperature-assignment table.')
RuntimeError('Conformational-state table is empty.')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def build_conformational_state_dataframe(
    all_descriptors,
    pca_results,
    clustering_results,
    temperature_assignment,
):
    """
    Build a reusable chain/frame-level conformational-state table.

    One row corresponds to one sampled trajectory frame for one polymer
    chain.

    Columns include:

    - chain analysis identifier
    - original topology segid, where available
    - trajectory frame
    - nominal temperature
    - all selected principal components
    - final DBSCAN label
    - DBSCAN noise status

    Notes
    -----
    PCA is performed independently for each polymer chain. Consequently,
    PC coordinates belonging to different chains should not automatically
    be interpreted as sharing a common PCA basis.
    """

    temperature_column = (
        "Nominal Temperature (K)"
    )


    records = []


    for (
        chain_id,
        descriptor_result,
    ) in all_descriptors.items():

        if chain_id not in pca_results:

            raise KeyError(
                f"PCA results are missing for "
                f"chain '{chain_id}'."
            )


        if chain_id not in clustering_results:

            raise KeyError(
                f"DBSCAN results are missing for "
                f"chain '{chain_id}'."
            )


        pca_result = (
            pca_results[
                chain_id
            ]
        )

        clustering_result = (
            clustering_results[
                chain_id
            ]
        )


        frame_indices = np.asarray(
            descriptor_result.frame_indices,
            dtype=int,
        )

        transformed_data = np.asarray(
            pca_result.transformed_data,
            dtype=float,
        )

        labels = np.asarray(
            clustering_result.labels,
            dtype=int,
        )


        n_samples = len(
            frame_indices
        )


        if transformed_data.shape[0] != n_samples:

            raise ValueError(
                f"PCA/frame count mismatch for "
                f"{chain_id}:\n"
                f"Frames: {n_samples}\n"
                f"PCA rows: {transformed_data.shape[0]}"
            )


        if len(labels) != n_samples:

            raise ValueError(
                f"DBSCAN/frame count mismatch for "
                f"{chain_id}:\n"
                f"Frames: {n_samples}\n"
                f"Labels: {len(labels)}"
            )


        if frame_indices.max() >= len(
            temperature_assignment
        ):

            raise IndexError(
                f"Sampled frame index for {chain_id} "
                "exceeds the temperature-assignment table."
            )


        sampled_temperatures = (
            temperature_assignment
            .iloc[
                frame_indices
            ][
                temperature_column
            ]
            .to_numpy(
                dtype=float
            )
        )


        topology_segid = getattr(
            descriptor_result,
            "topology_segid",
            None,
        )


        segment_index = getattr(
            descriptor_result,
            "segment_index",
            None,
        )


        for sample_index in range(
            n_samples
        ):

            record = {
                "Chain":
                    chain_id,

                "Topology SegID":
                    topology_segid,

                "Segment Index":
                    segment_index,

                "Frame":
                    int(
                        frame_indices[
                            sample_index
                        ]
                    ),

                "Temperature (K)":
                    float(
                        sampled_temperatures[
                            sample_index
                        ]
                    ),

                "DBSCAN Label":
                    int(
                        labels[
                            sample_index
                        ]
                    ),

                "DBSCAN Noise":
                    bool(
                        labels[
                            sample_index
                        ]
                        == -1
                    ),
            }


            for component_index in range(
                transformed_data.shape[1]
            ):

                record[
                    f"PC{component_index + 1}"
                ] = float(
                    transformed_data[
                        sample_index,
                        component_index,
                    ]
                )


            records.append(
                record
            )


    dataframe = pd.DataFrame(
        records
    )


    if dataframe.empty:

        raise RuntimeError(
            "Conformational-state table is empty."
        )


    return dataframe
```

</details>

<a id="definition-1185"></a>

## `plot_chain_pca_temperature`

Source lines 1185–1269. Named callable; inspect its callers before treating it as a stable public API.

```python
def plot_chain_pca_temperature(chain_dataframe, pca_result, chain_id, output_path): ...
```

### Purpose and original contract

Plot PC1 versus PC2 for one chain, coloured by nominal temperature.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| chain_dataframe | not annotated | required |
| pca_result | not annotated | required |
| chain_id | not annotated | required |
| output_path | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `_save_figure`, `axis.scatter`, `axis.set_title`, `axis.set_xlabel`, `axis.set_ylabel`, `colourbar.set_label`, `figure.colorbar`, `len`, `np.asarray`, `plt.subplots`.

Explicit return expressions; different branches may return different objects:

```python
False
True
```

Calls worth inspecting for I/O, state changes or delegated execution: `_save_figure`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def plot_chain_pca_temperature(
    chain_dataframe,
    pca_result,
    chain_id,
    output_path,
):
    """
    Plot PC1 versus PC2 for one chain, coloured by nominal temperature.
    """

    if (
        "PC1" not in chain_dataframe.columns
        or "PC2" not in chain_dataframe.columns
    ):

        return False


    explained_variance = np.asarray(
        pca_result.explained_variance_ratio,
        dtype=float,
    )


    pc1_variance = (
        explained_variance[0] * 100
        if len(explained_variance) >= 1
        else np.nan
    )

    pc2_variance = (
        explained_variance[1] * 100
        if len(explained_variance) >= 2
        else np.nan
    )


    figure, axis = plt.subplots(
        figsize=(7, 6)
    )


    scatter = axis.scatter(
        chain_dataframe["PC1"],
        chain_dataframe["PC2"],
        c=chain_dataframe[
            "Temperature (K)"
        ],
        cmap="viridis",
        s=10,
        alpha=0.7,
    )


    colourbar = (
        figure.colorbar(
            scatter,
            ax=axis,
        )
    )

    colourbar.set_label(
        "Temperature (K)"
    )


    axis.set_xlabel(
        f"PC1 ({pc1_variance:.2f} %)"
    )

    axis.set_ylabel(
        f"PC2 ({pc2_variance:.2f} %)"
    )

    axis.set_title(
        f"{chain_id}: PC1 vs PC2 coloured by temperature"
    )


    _save_figure(
        figure,
        output_path,
    )

    return True
```

</details>

<a id="definition-1272"></a>

## `plot_chain_pca_dbscan`

Source lines 1272–1379. Named callable; inspect its callers before treating it as a stable public API.

```python
def plot_chain_pca_dbscan(chain_dataframe, pca_result, chain_id, output_path): ...
```

### Purpose and original contract

Plot PC1 versus PC2 for one chain, coloured by final DBSCAN label.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| chain_dataframe | not annotated | required |
| pca_result | not annotated | required |
| chain_id | not annotated | required |
| output_path | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `_save_figure`, `axis.legend`, `axis.scatter`, `axis.set_title`, `axis.set_xlabel`, `axis.set_ylabel`, `chain_dataframe['DBSCAN Label'].unique`, `len`, `np.asarray`, `plt.subplots`, `sorted`.

Explicit return expressions; different branches may return different objects:

```python
False
True
```

Calls worth inspecting for I/O, state changes or delegated execution: `_save_figure`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def plot_chain_pca_dbscan(
    chain_dataframe,
    pca_result,
    chain_id,
    output_path,
):
    """
    Plot PC1 versus PC2 for one chain, coloured by final DBSCAN label.
    """

    if (
        "PC1" not in chain_dataframe.columns
        or "PC2" not in chain_dataframe.columns
    ):

        return False


    explained_variance = np.asarray(
        pca_result.explained_variance_ratio,
        dtype=float,
    )


    pc1_variance = (
        explained_variance[0] * 100
        if len(explained_variance) >= 1
        else np.nan
    )

    pc2_variance = (
        explained_variance[1] * 100
        if len(explained_variance) >= 2
        else np.nan
    )


    figure, axis = plt.subplots(
        figsize=(7, 6)
    )


    unique_labels = sorted(
        chain_dataframe[
            "DBSCAN Label"
        ]
        .unique()
    )


    for label in unique_labels:

        label_data = (
            chain_dataframe[
                chain_dataframe[
                    "DBSCAN Label"
                ]
                == label
            ]
        )


        if label == -1:

            display_label = (
                "Noise (-1)"
            )

        else:

            display_label = (
                f"Cluster {label}"
            )


        axis.scatter(
            label_data["PC1"],
            label_data["PC2"],
            s=10,
            alpha=0.7,
            label=display_label,
        )


    axis.set_xlabel(
        f"PC1 ({pc1_variance:.2f} %)"
    )

    axis.set_ylabel(
        f"PC2 ({pc2_variance:.2f} %)"
    )

    axis.set_title(
        f"{chain_id}: PC1 vs PC2 coloured by DBSCAN state"
    )

    axis.legend(
        markerscale=2,
        fontsize="small",
    )


    _save_figure(
        figure,
        output_path,
    )

    return True
```

</details>

<a id="definition-1386"></a>

## `generate_chain_pca_figures`

Source lines 1386–1509. Named callable; inspect its callers before treating it as a stable public API.

```python
def generate_chain_pca_figures(conformational_state_dataframe, pca_results, output_directory): ...
```

### Purpose and original contract

Generate temperature- and DBSCAN-coloured PCA plots for every chain.

PCA is calculated independently for each chain, so separate figures
are generated rather than pooling chain coordinates into one PCA space.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| conformational_state_dataframe | not annotated | required |
| pca_results | not annotated | required |
| output_directory | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `conformational_state_dataframe[conformational_state_dataframe['Chain'] == chain_id].copy`, `output_directory.mkdir`, `pca_results.items`, `plot_chain_pca_dbscan`, `plot_chain_pca_temperature`, `print`, `saved_paths.append`.

Explicit return expressions; different branches may return different objects:

```python
saved_paths
```

Calls worth inspecting for I/O, state changes or delegated execution: `conformational_state_dataframe[conformational_state_dataframe['Chain'] == chain_id].copy`, `output_directory.mkdir`, `saved_paths.append`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def generate_chain_pca_figures(
    conformational_state_dataframe,
    pca_results,
    output_directory,
):
    """
    Generate temperature- and DBSCAN-coloured PCA plots for every chain.

    PCA is calculated independently for each chain, so separate figures
    are generated rather than pooling chain coordinates into one PCA space.
    """

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )


    saved_paths = []


    for (
        chain_id,
        pca_result,
    ) in pca_results.items():

        chain_dataframe = (
            conformational_state_dataframe[
                conformational_state_dataframe[
                    "Chain"
                ]
                == chain_id
            ]
            .copy()
        )


        if chain_dataframe.empty:

            print(
                f"WARNING: no conformational-state "
                f"data found for {chain_id}."
            )

            continue


        # ---------------------------------------------------------------------
        # Temperature-coloured PCA
        # ---------------------------------------------------------------------

        temperature_path = (
            output_directory
            / (
                f"{chain_id}"
                "_pc1_pc2_temperature.png"
            )
        )


        generated = (
            plot_chain_pca_temperature(
                chain_dataframe=(
                    chain_dataframe
                ),
                pca_result=(
                    pca_result
                ),
                chain_id=(
                    chain_id
                ),
                output_path=(
                    temperature_path
                ),
            )
        )


        if generated:

            saved_paths.append(
                temperature_path
            )


        # ---------------------------------------------------------------------
        # DBSCAN-coloured PCA
        # ---------------------------------------------------------------------

        dbscan_path = (
            output_directory
            / (
                f"{chain_id}"
                "_pc1_pc2_dbscan.png"
            )
        )


        generated = (
            plot_chain_pca_dbscan(
                chain_dataframe=(
                    chain_dataframe
                ),
                pca_result=(
                    pca_result
                ),
                chain_id=(
                    chain_id
                ),
                output_path=(
                    dbscan_path
                ),
            )
        )


        if generated:

            saved_paths.append(
                dbscan_path
            )


    return saved_paths
```

</details>

<a id="definition-1516"></a>

## `generate_analysis_figures`

Source lines 1516–1760. Named callable; inspect its callers before treating it as a stable public API.

```python
def generate_analysis_figures(figure_directory, temperatures, simulation_data, pca_optimisation, pca_results, dbscan_optimisation, temperature_response, tg_result, conformational_state_dataframe, system_name, simulation_name): ...
```

### Purpose and original contract

Generate the complete replica-level Tg analysis figure set.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| figure_directory | not annotated | required |
| temperatures | not annotated | required |
| simulation_data | not annotated | required |
| pca_optimisation | not annotated | required |
| pca_results | not annotated | required |
| dbscan_optimisation | not annotated | required |
| temperature_response | not annotated | required |
| tg_result | not annotated | required |
| conformational_state_dataframe | not annotated | required |
| system_name | not annotated | required |
| simulation_name | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `figure_directory.mkdir`, `figure_paths.append`, `figure_paths.extend`, `generate_chain_pca_figures`, `len`, `plot_dbscan_ari`, `plot_dbscan_clusters`, `plot_dbscan_noise`, `plot_pca_elbow_distribution`, `plot_pca_scree`, `plot_temperature_block_agreement`, `plot_tg_fit`, `print`.

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
def generate_analysis_figures(
    figure_directory,
    temperatures,
    simulation_data,
    pca_optimisation,
    pca_results,
    dbscan_optimisation,
    temperature_response,
    tg_result,
    conformational_state_dataframe,
    system_name,
    simulation_name,
):
    """
    Generate the complete replica-level Tg analysis figure set.
    """

    figure_directory.mkdir(
        parents=True,
        exist_ok=True,
    )


    print()
    print(
        "Generating replica-level analysis figures"
    )

    print("-" * 80)


    figure_paths = []


    # -------------------------------------------------------------------------
    # Temperature agreement
    # -------------------------------------------------------------------------

    path = (
        figure_directory
        / "temperature_block_agreement.png"
    )


    if plot_temperature_block_agreement(
        temperatures=temperatures,
        simulation_data=simulation_data,
        output_path=path,
    ):

        figure_paths.append(
            path
        )


    # -------------------------------------------------------------------------
    # PCA scree
    # -------------------------------------------------------------------------

    path = (
        figure_directory
        / "pca_scree.png"
    )


    plot_pca_scree(
        pca_optimisation=(
            pca_optimisation
        ),
        output_path=(
            path
        ),
    )

    figure_paths.append(
        path
    )


    # -------------------------------------------------------------------------
    # PCA elbows
    # -------------------------------------------------------------------------

    path = (
        figure_directory
        / "pca_elbow_distribution.png"
    )


    if plot_pca_elbow_distribution(
        pca_optimisation=(
            pca_optimisation
        ),
        output_path=(
            path
        ),
    ):

        figure_paths.append(
            path
        )


    # -------------------------------------------------------------------------
    # DBSCAN ARI
    # -------------------------------------------------------------------------

    path = (
        figure_directory
        / "dbscan_ari_vs_min_samples.png"
    )


    if plot_dbscan_ari(
        dbscan_optimisation=(
            dbscan_optimisation
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
        / "dbscan_noise_vs_min_samples.png"
    )


    plot_dbscan_noise(
        dbscan_optimisation=(
            dbscan_optimisation
        ),
        output_path=(
            path
        ),
    )

    figure_paths.append(
        path
    )


    # -------------------------------------------------------------------------
    # DBSCAN clusters
    # -------------------------------------------------------------------------

    path = (
        figure_directory
        / "dbscan_clusters_vs_min_samples.png"
    )


    plot_dbscan_clusters(
        dbscan_optimisation=(
            dbscan_optimisation
        ),
        output_path=(
            path
        ),
    )

    figure_paths.append(
        path
    )


    # -------------------------------------------------------------------------
    # Tg fit
    # -------------------------------------------------------------------------

    path = (
        figure_directory
        / "tg_fit.png"
    )


    plot_tg_fit(
        temperature_response=(
            temperature_response
        ),
        tg_result=(
            tg_result
        ),
        system_name=(
            system_name
        ),
        simulation_name=(
            simulation_name
        ),
        output_path=(
            path
        ),
    )

    figure_paths.append(
        path
    )


    # -------------------------------------------------------------------------
    # Per-chain PCA figures
    # -------------------------------------------------------------------------

    chain_pca_directory = (
        figure_directory
        / "pca_by_chain"
    )


    chain_paths = (
        generate_chain_pca_figures(
            conformational_state_dataframe=(
                conformational_state_dataframe
            ),
            pca_results=(
                pca_results
            ),
            output_directory=(
                chain_pca_directory
            ),
        )
    )


    figure_paths.extend(
        chain_paths
    )


    print(
        f"Generated "
        f"{len(figure_paths)} figures."
    )


    return figure_paths
```

</details>

<a id="definition-1767"></a>

## `write_analysis_report`

Source lines 1767–2022. Named callable; inspect its callers before treating it as a stable public API.

```python
def write_analysis_report(output_path, system_name, simulation_name, stage, loaded_simulation, analysis_stride, temperatures, all_descriptors, pca_optimisation, dbscan_optimisation, selected_dbscan_dataframe, tg_result, conformational_state_dataframe): ...
```

### Purpose and original contract

Write a concise human-readable replica-level Tg analysis report.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| output_path | not annotated | required |
| system_name | not annotated | required |
| simulation_name | not annotated | required |
| stage | not annotated | required |
| loaded_simulation | not annotated | required |
| analysis_stride | not annotated | required |
| temperatures | not annotated | required |
| all_descriptors | not annotated | required |
| pca_optimisation | not annotated | required |
| dbscan_optimisation | not annotated | required |
| selected_dbscan_dataframe | not annotated | required |
| tg_result | not annotated | required |
| conformational_state_dataframe | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `'\n'.join`, `all_descriptors.values`, `float`, `iter`, `len`, `next`, `output_path.write_text`, `selected_dbscan_dataframe['Clusters'].median`, `selected_dbscan_dataframe['Epsilon'].median`, `selected_dbscan_dataframe['Noise Fraction'].median`, `temperatures['Nominal Temperature (K)'].max`, `temperatures['Nominal Temperature (K)'].min`, `temperatures['Nominal Temperature (K)'].nunique`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Calls worth inspecting for I/O, state changes or delegated execution: `output_path.write_text`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def write_analysis_report(
    output_path,
    system_name,
    simulation_name,
    stage,
    loaded_simulation,
    analysis_stride,
    temperatures,
    all_descriptors,
    pca_optimisation,
    dbscan_optimisation,
    selected_dbscan_dataframe,
    tg_result,
    conformational_state_dataframe,
):
    """
    Write a concise human-readable replica-level Tg analysis report.
    """

    median_epsilon = float(
        selected_dbscan_dataframe[
            "Epsilon"
        ].median()
    )

    median_clusters = float(
        selected_dbscan_dataframe[
            "Clusters"
        ].median()
    )

    median_noise = float(
        selected_dbscan_dataframe[
            "Noise Fraction"
        ].median()
    )


    example_chain = next(
        iter(
            all_descriptors.values()
        )
    )


    lines = [

        "=" * 80,

        "REPLICA Tg ANALYSIS REPORT",

        "=" * 80,

        "",

        "SYSTEM",

        "-" * 80,

        f"System: {system_name}",

        f"Simulation: {simulation_name}",

        f"Stage: {stage}",

        (
            "Topology: "
            f"{loaded_simulation.topology_path.name}"
        ),

        (
            "Trajectory: "
            f"{loaded_simulation.trajectory_path.name}"
        ),

        (
            "Trajectory frames: "
            f"{len(loaded_simulation.universe.trajectory)}"
        ),

        (
            "Polymer chains analysed: "
            f"{len(all_descriptors)}"
        ),

        "",

        "TEMPERATURE ASSIGNMENT",

        "-" * 80,

        (
            "Temperature blocks: "
            f"{temperatures['Nominal Temperature (K)'].nunique()}"
        ),

        (
            "Maximum nominal temperature: "
            f"{temperatures['Nominal Temperature (K)'].max():.1f} K"
        ),

        (
            "Minimum nominal temperature: "
            f"{temperatures['Nominal Temperature (K)'].min():.1f} K"
        ),

        "",

        "STRUCTURAL DESCRIPTORS",

        "-" * 80,

        (
            "Sampling stride: "
            f"{analysis_stride}"
        ),

        (
            "Frames analysed per chain: "
            f"{len(example_chain.frame_indices)}"
        ),

        (
            "Heavy atoms per example chain: "
            f"{example_chain.n_heavy_atoms}"
        ),

        (
            "Distances per conformation: "
            f"{example_chain.descriptors.shape[1]}"
        ),

        "",

        "PCA",

        "-" * 80,

        (
            "Selected PCs: "
            f"{pca_optimisation.selected_components}"
        ),

        (
            "Median PCA elbow: "
            f"{pca_optimisation.median_elbow:.3f}"
        ),

        (
            "Mean PCA elbow: "
            f"{pca_optimisation.mean_elbow:.3f}"
        ),

        (
            "PCA elbow Q1-Q3: "
            f"{pca_optimisation.elbow_q1:.3f}"
            " - "
            f"{pca_optimisation.elbow_q3:.3f}"
        ),

        (
            "Chains within ±1 PC: "
            f"{pca_optimisation.fraction_within_one_component * 100:.2f} %"
        ),

        "",

        "DBSCAN",

        "-" * 80,

        (
            "Neighbour rank k: "
            f"{dbscan_optimisation.k}"
        ),

        (
            "Selected min_samples: "
            f"{dbscan_optimisation.selected_min_samples}"
        ),

        (
            "Median epsilon: "
            f"{median_epsilon:.6f}"
        ),

        (
            "Median clusters: "
            f"{median_clusters:.3f}"
        ),

        (
            "Median noise fraction: "
            f"{median_noise:.6f}"
        ),

        "",

        "CONFORMATIONAL STATE TABLE",

        "-" * 80,

        (
            "Rows: "
            f"{len(conformational_state_dataframe)}"
        ),

        (
            "Columns: "
            f"{len(conformational_state_dataframe.columns)}"
        ),

        "",

        "GLASS TRANSITION",

        "-" * 80,

        (
            "Observable: "
            "historical_mean_dbscan_cluster_id"
        ),

        (
            "Estimated Tg: "
            f"{tg_result.tg:.2f} K"
        ),

        (
            "C: "
            f"{tg_result.C:.6f}"
        ),

        (
            "s: "
            f"{tg_result.s:.6f}"
        ),

        (
            "d: "
            f"{tg_result.d:.6f}"
        ),

        "",

        "=" * 80,

    ]


    output_path.write_text(
        "\n".join(
            lines
        ),
        encoding="utf-8",
    )
```

</details>

<a id="definition-2029"></a>

## `run_tg_analysis`

Source lines 2029–3549. Named callable; inspect its callers before treating it as a stable public API.

```python
def run_tg_analysis(system_name, simulation_name, stage='thermal_ramp_cooling', total_steps=200000000, max_temp=700, min_temp=140, temp_change=10, reporter_freq=1000, analysis_stride=50, max_pca_components=20, dbscan_min_samples_values=range(2, 11), generate_figures=False, project_root=None): ...
```

### Purpose and original contract

Run the complete Tg analysis for one simulation replica.

Parameters
----------
system_name : str
    MD system name.

simulation_name : str
    Name of the completed simulation / replica.

stage : str, optional
    Simulation stage to analyse.

total_steps : int, optional
    Total integration steps in the thermal ramp.

max_temp : float, optional
    Maximum cooling-ramp temperature in kelvin.

min_temp : float, optional
    Minimum cooling-ramp temperature in kelvin.

temp_change : float, optional
    Temperature step between nominal temperature blocks.

reporter_freq : int, optional
    Reporter frequency in MD integration steps.

analysis_stride : int, optional
    Trajectory frame sampling stride.

max_pca_components : int, optional
    Maximum PCA dimensionality considered during optimisation.

dbscan_min_samples_values : iterable of int, optional
    Candidate DBSCAN min_samples values.

generate_figures : bool, optional
    Generate replica-level diagnostic figures and text report.

    Default:
        False

project_root : str or pathlib.Path, optional
    iPHAsimulatorV2 project root.

Returns
-------
dict
    Completed replica-level analysis summary.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| system_name | not annotated | required |
| simulation_name | not annotated | required |
| stage | not annotated | 'thermal_ramp_cooling' |
| total_steps | not annotated | 200000000 |
| max_temp | not annotated | 700 |
| min_temp | not annotated | 140 |
| temp_change | not annotated | 10 |
| reporter_freq | not annotated | 1000 |
| analysis_stride | not annotated | 50 |
| max_pca_components | not annotated | 20 |
| dbscan_min_samples_values | not annotated | range(2, 11) |
| generate_figures | not annotated | False |
| project_root | not annotated | None |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `(tg_directory / 'temperature_response.csv').relative_to`, `FileNotFoundError`, `Path`, `Path(__file__).resolve`, `Path(project_root).expanduser`, `Path(project_root).expanduser().resolve`, `RuntimeError`, `ValueError`, `all_descriptors.values`, `assign_nominal_temperatures`, `bool`, `build_conformational_state_dataframe`, `calculate_all_chain_distance_descriptors`, `calculate_historical_cluster_response`, `calculate_optimised_pca`, `cluster_all_chain_pca`, `conformational_state_dataframe.to_csv`, `conformational_state_path.relative_to`, `dbscan_optimisation.parameter_dataframe.to_csv`, `dbscan_optimisation.parameter_dataframe[dbscan_optimisation.parameter_dataframe['Min Samples'] == selected_min_samples].copy`, `dbscan_optimisation.stability_dataframe.to_csv`, `dbscan_optimisation.summary_dataframe.to_csv`, `directory.mkdir`, `fit_historical_tg`, `float`, `generate_analysis_figures`, `int`, `iter`, `json.dump`, `len`, `load_simulation`, `next`, `open`, `optimise_dbscan`, `optimise_pca_dimensionality`, `pca_optimisation.dimensionality_dataframe.to_csv`, `pca_optimisation.spectra_dataframe.to_csv`, `pd.DataFrame`, `print`, `selected_dbscan_dataframe['Clusters'].mean`, `selected_dbscan_dataframe['Clusters'].median`, `selected_dbscan_dataframe['Epsilon'].mean`, `selected_dbscan_dataframe['Epsilon'].median`, `selected_dbscan_dataframe['Noise Fraction'].mean`, `selected_dbscan_dataframe['Noise Fraction'].median`, `simulation_directory.is_dir`, `str`, `system_directory.is_dir`, `temperature_response_dataframe.to_csv`, `temperatures.to_csv`, `temperatures[temperature_column].isna`, `temperatures[temperature_column].isna().any`, `temperatures[temperature_column].nunique`, `write_analysis_report`.

Explicit return expressions; different branches may return different objects:

```python
result
```

Calls worth inspecting for I/O, state changes or delegated execution: `dbscan_optimisation.parameter_dataframe[dbscan_optimisation.parameter_dataframe['Min Samples'] == selected_min_samples].copy`, `directory.mkdir`, `load_simulation`, `open`, `write_analysis_report`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
FileNotFoundError(f'MD system directory was not found:\n{system_directory}')
FileNotFoundError(f'Simulation directory was not found:\n{simulation_directory}')
ValueError(f'Temperature assignment does not match trajectory length:\nTrajectory frames:       {len(universe.trajectory)}\nTemperature assignments: {len(temperatures)}')
ValueError('Temperature assignment contains missing nominal temperatures.')
ValueError(f'Unexpected starting nominal temperature:\nExpected: {max_temp} K\nFound:    {first_temperature} K')
ValueError(f'Unexpected final nominal temperature:\nExpected: {min_temp} K\nFound:    {final_temperature} K')
RuntimeError('No structural descriptors were generated.')
RuntimeError('No PCA results were generated.')
RuntimeError('No DBSCAN clustering results were generated.')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def run_tg_analysis(
    system_name,
    simulation_name,
    stage="thermal_ramp_cooling",
    total_steps=200_000_000,
    max_temp=700,
    min_temp=140,
    temp_change=10,
    reporter_freq=1000,
    analysis_stride=50,
    max_pca_components=20,
    dbscan_min_samples_values=range(2, 11),
    generate_figures=False,
    project_root=None,
):
    """
    Run the complete Tg analysis for one simulation replica.

    Parameters
    ----------
    system_name : str
        MD system name.

    simulation_name : str
        Name of the completed simulation / replica.

    stage : str, optional
        Simulation stage to analyse.

    total_steps : int, optional
        Total integration steps in the thermal ramp.

    max_temp : float, optional
        Maximum cooling-ramp temperature in kelvin.

    min_temp : float, optional
        Minimum cooling-ramp temperature in kelvin.

    temp_change : float, optional
        Temperature step between nominal temperature blocks.

    reporter_freq : int, optional
        Reporter frequency in MD integration steps.

    analysis_stride : int, optional
        Trajectory frame sampling stride.

    max_pca_components : int, optional
        Maximum PCA dimensionality considered during optimisation.

    dbscan_min_samples_values : iterable of int, optional
        Candidate DBSCAN min_samples values.

    generate_figures : bool, optional
        Generate replica-level diagnostic figures and text report.

        Default:
            False

    project_root : str or pathlib.Path, optional
        iPHAsimulatorV2 project root.

    Returns
    -------
    dict
        Completed replica-level analysis summary.
    """

    # =========================================================================
    # Resolve project paths
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


    structure_database = (
        project_root
        / "structure_database"
    )


    system_directory = (
        structure_database
        / "PHA_melts"
        / system_name
    )


    simulation_directory = (
        system_directory
        / "simulations"
        / simulation_name
    )


    # =========================================================================
    # Replica-level analysis directory
    # =========================================================================

    analysis_directory = (
        simulation_directory
        / "analysis"
        / "tg_analysis"
    )


    pca_directory = (
        analysis_directory
        / "pca"
    )


    dbscan_directory = (
        analysis_directory
        / "dbscan"
    )


    tg_directory = (
        analysis_directory
        / "tg"
    )


    figure_directory = (
        analysis_directory
        / "figures"
    )


    report_path = (
        analysis_directory
        / "tg_analysis_output.txt"
    )


    # =========================================================================
    # Validate paths
    # =========================================================================

    if not system_directory.is_dir():

        raise FileNotFoundError(
            "MD system directory was not found:\n"
            f"{system_directory}"
        )


    if not simulation_directory.is_dir():

        raise FileNotFoundError(
            "Simulation directory was not found:\n"
            f"{simulation_directory}"
        )


    for directory in (
        analysis_directory,
        pca_directory,
        dbscan_directory,
        tg_directory,
    ):

        directory.mkdir(
            parents=True,
            exist_ok=True,
        )


    # =========================================================================
    # Header
    # =========================================================================

    print()
    print("=" * 80)
    print("REPLICA Tg ANALYSIS WORKFLOW")
    print("=" * 80)

    print(
        f"System:      {system_name}"
    )

    print(
        f"Simulation:  {simulation_name}"
    )

    print(
        f"Stage:       {stage}"
    )

    print(
        f"Input:       {simulation_directory}"
    )

    print(
        f"Output:      {analysis_directory}"
    )

    print(
        f"Figures:     {generate_figures}"
    )

    print("=" * 80)


    # =========================================================================
    # STEP 1
    # Load simulation
    # =========================================================================

    print()
    print(
        "Step 1: loading simulation"
    )

    print("-" * 80)


    loaded_simulation = (
        load_simulation(
            system_directory=(
                system_directory
            ),
            simulation_name=(
                simulation_name
            ),
            stage=(
                stage
            ),
            validate_alignment=True,
        )
    )


    universe = (
        loaded_simulation.universe
    )

    simulation_data = (
        loaded_simulation.data
    )


    print(
        f"Topology:    "
        f"{loaded_simulation.topology_path.name}"
    )

    print(
        f"Trajectory:  "
        f"{loaded_simulation.trajectory_path.name}"
    )

    print(
        f"State data:  "
        f"{loaded_simulation.data_path.name}"
    )

    print(
        f"Atoms:       "
        f"{universe.atoms.n_atoms}"
    )

    print(
        f"Residues:    "
        f"{universe.residues.n_residues}"
    )

    print(
        f"Segments:    "
        f"{universe.segments.n_segments}"
    )

    print(
        f"Frames:      "
        f"{len(universe.trajectory)}"
    )

    print(
        f"Data rows:   "
        f"{len(simulation_data)}"
    )

    print(
        "Trajectory/state-data alignment: OK"
    )


    # =========================================================================
    # STEP 2
    # Assign temperatures
    # =========================================================================

    print()
    print(
        "Step 2: assigning temperatures"
    )

    print("-" * 80)


    temperatures = (
        assign_nominal_temperatures(
            simulation=(
                loaded_simulation
            ),
            total_steps=(
                total_steps
            ),
            max_temp=(
                max_temp
            ),
            min_temp=(
                min_temp
            ),
            temp_change=(
                temp_change
            ),
            reporter_freq=(
                reporter_freq
            ),
        )
    )


    temperature_column = (
        "Nominal Temperature (K)"
    )


    if len(temperatures) != len(
        universe.trajectory
    ):

        raise ValueError(
            "Temperature assignment does not match trajectory length:\n"
            f"Trajectory frames:       {len(universe.trajectory)}\n"
            f"Temperature assignments: {len(temperatures)}"
        )


    if temperatures[
        temperature_column
    ].isna().any():

        raise ValueError(
            "Temperature assignment contains missing nominal temperatures."
        )


    first_temperature = float(
        temperatures[
            temperature_column
        ].iloc[0]
    )

    final_temperature = float(
        temperatures[
            temperature_column
        ].iloc[-1]
    )


    if first_temperature != float(
        max_temp
    ):

        raise ValueError(
            "Unexpected starting nominal temperature:\n"
            f"Expected: {max_temp} K\n"
            f"Found:    {first_temperature} K"
        )


    if final_temperature != float(
        min_temp
    ):

        raise ValueError(
            "Unexpected final nominal temperature:\n"
            f"Expected: {min_temp} K\n"
            f"Found:    {final_temperature} K"
        )


    n_temperature_blocks = int(
        temperatures[
            temperature_column
        ].nunique()
    )


    print(
        f"Maximum temperature:   "
        f"{max_temp} K"
    )

    print(
        f"Minimum temperature:   "
        f"{min_temp} K"
    )

    print(
        f"Temperature step:      "
        f"{temp_change} K"
    )

    print(
        f"Temperature blocks:    "
        f"{n_temperature_blocks}"
    )

    print(
        f"Assigned frames:       "
        f"{len(temperatures)}"
    )

    print(
        "Temperature assignment: OK"
    )


    # =========================================================================
    # STEP 3
    # Structural descriptors
    # =========================================================================

    print()
    print(
        "Step 3: generating structural descriptors"
    )

    print("-" * 80)


    print(
        f"Sampling stride: "
        f"{analysis_stride}"
    )


    all_descriptors = (
        calculate_all_chain_distance_descriptors(
            simulation=(
                loaded_simulation
            ),
            stride=(
                analysis_stride
            ),
        )
    )


    if not all_descriptors:

        raise RuntimeError(
            "No structural descriptors were generated."
        )


    example_chain = next(
        iter(
            all_descriptors.values()
        )
    )


    print(
        f"Polymer chains analysed: "
        f"{len(all_descriptors)}"
    )

    print(
        f"Frames per chain: "
        f"{len(example_chain.frame_indices)}"
    )

    print(
        f"Descriptor matrix per chain: "
        f"{example_chain.descriptors.shape}"
    )

    print(
        f"Heavy atoms per chain: "
        f"{example_chain.n_heavy_atoms}"
    )

    print(
        f"Distances per conformation: "
        f"{example_chain.descriptors.shape[1]}"
    )


    # =========================================================================
    # STEP 4
    # PCA dimensionality optimisation
    # =========================================================================

    print()
    print(
        "Step 4: optimising PCA dimensionality"
    )

    print("-" * 80)


    pca_optimisation = (
        optimise_pca_dimensionality(
            descriptors_by_segment=(
                all_descriptors
            ),
            max_components=(
                max_pca_components
            ),
        )
    )


    print(
        f"Selected PCs: "
        f"{pca_optimisation.selected_components}"
    )

    print(
        f"Median elbow: "
        f"{pca_optimisation.median_elbow:.3f}"
    )

    print(
        f"Mean elbow: "
        f"{pca_optimisation.mean_elbow:.3f}"
    )

    print(
        f"Elbow Q1-Q3: "
        f"{pca_optimisation.elbow_q1:.3f}"
        " - "
        f"{pca_optimisation.elbow_q3:.3f}"
    )

    print(
        f"Chains within ±1 PC: "
        f"{pca_optimisation.fraction_within_one_component * 100:.2f} %"
    )


    # =========================================================================
    # STEP 5
    # Final PCA representation
    # =========================================================================

    print()
    print(
        "Step 5: calculating final PCA representation"
    )

    print("-" * 80)


    pca_results = (
        calculate_optimised_pca(
            descriptors_by_segment=(
                all_descriptors
            ),
            optimisation_result=(
                pca_optimisation
            ),
        )
    )


    if not pca_results:

        raise RuntimeError(
            "No PCA results were generated."
        )


    if (
        pca_optimisation
        .selected_components
        < 2
    ):

        print(
            "WARNING: fewer than two PCs were selected. "
            "PC1-vs-PC2 figures cannot be generated."
        )


    print(
        f"Selected dimensionality: "
        f"{pca_optimisation.selected_components} PCs"
    )

    print(
        f"Polymer chains transformed: "
        f"{len(pca_results)}"
    )


    # =========================================================================
    # STEP 6
    # DBSCAN optimisation
    # =========================================================================

    print()
    print(
        "Step 6: optimising DBSCAN"
    )

    print("-" * 80)


    dbscan_optimisation = (
        optimise_dbscan(
            pca_results=(
                pca_results
            ),
            min_samples_values=(
                dbscan_min_samples_values
            ),
            n_temperatures=(
                n_temperature_blocks
            ),
        )
    )


    selected_min_samples = (
        dbscan_optimisation
        .selected_min_samples
    )

    selected_k = (
        dbscan_optimisation
        .k
    )


    print(
        f"PCA dimensions:      "
        f"{dbscan_optimisation.n_components}"
    )

    print(
        f"Neighbour rank k:     "
        f"{selected_k}"
    )

    print(
        f"Selected min_samples: "
        f"{selected_min_samples}"
    )


    # =========================================================================
    # STEP 7
    # Final DBSCAN clustering
    # =========================================================================

    print()
    print(
        "Step 7: performing final DBSCAN clustering"
    )

    print("-" * 80)


    clustering_results = (
        cluster_all_chain_pca(
            pca_results=(
                pca_results
            ),
            k=(
                selected_k
            ),
            min_samples=(
                selected_min_samples
            ),
            n_temperatures=(
                n_temperature_blocks
            ),
        )
    )


    if not clustering_results:

        raise RuntimeError(
            "No DBSCAN clustering results were generated."
        )


    print(
        f"Chains clustered: "
        f"{len(clustering_results)}"
    )


    # =========================================================================
    # STEP 8
    # Temperature response
    # =========================================================================

    print()
    print(
        "Step 8: constructing temperature response"
    )

    print("-" * 80)


    temperature_response = (
        calculate_historical_cluster_response(
            clustering_results=(
                clustering_results
            ),
            temperature_assignment=(
                temperatures
            ),
        )
    )


    print(
        f"Temperature response points: "
        f"{len(temperature_response.temperatures)}"
    )


    # =========================================================================
    # STEP 9
    # Tg fitting
    # =========================================================================

    print()
    print(
        "Step 9: fitting glass transition"
    )

    print("-" * 80)


    tg_result = (
        fit_historical_tg(
            temperature_response
        )
    )


    print(
        f"Tg: {tg_result.tg:.2f} K"
    )

    print(
        f"C:  {tg_result.C:.6f}"
    )

    print(
        f"s:  {tg_result.s:.6f}"
    )

    print(
        f"d:  {tg_result.d:.6f}"
    )


    # =========================================================================
    # STEP 10
    # Build conformational-state table
    # =========================================================================

    print()
    print(
        "Step 10: building conformational-state table"
    )

    print("-" * 80)


    conformational_state_dataframe = (
        build_conformational_state_dataframe(
            all_descriptors=(
                all_descriptors
            ),
            pca_results=(
                pca_results
            ),
            clustering_results=(
                clustering_results
            ),
            temperature_assignment=(
                temperatures
            ),
        )
    )


    print(
        f"Conformational-state rows: "
        f"{len(conformational_state_dataframe)}"
    )

    print(
        f"Conformational-state columns: "
        f"{len(conformational_state_dataframe.columns)}"
    )


    # =========================================================================
    # STEP 11
    # Save machine-readable outputs
    # =========================================================================

    print()
    print(
        "Step 11: saving replica analysis outputs"
    )

    print("-" * 80)


    # -------------------------------------------------------------------------
    # Temperature assignment
    # -------------------------------------------------------------------------

    temperatures.to_csv(
        analysis_directory
        / "temperature_assignment.csv",
        index=False,
    )


    # -------------------------------------------------------------------------
    # Conformational-state table
    # -------------------------------------------------------------------------

    conformational_state_path = (
        analysis_directory
        / "conformational_state_by_chain.csv"
    )


    conformational_state_dataframe.to_csv(
        conformational_state_path,
        index=False,
    )


    # -------------------------------------------------------------------------
    # PCA diagnostics
    # -------------------------------------------------------------------------

    (
        pca_optimisation
        .dimensionality_dataframe
        .to_csv(
            pca_directory
            / "pca_dimensionality_by_chain.csv",
            index=False,
        )
    )


    (
        pca_optimisation
        .spectra_dataframe
        .to_csv(
            pca_directory
            / "pca_spectrum_by_chain.csv",
            index=False,
        )
    )


    # -------------------------------------------------------------------------
    # DBSCAN diagnostics
    # -------------------------------------------------------------------------

    (
        dbscan_optimisation
        .parameter_dataframe
        .to_csv(
            dbscan_directory
            / "dbscan_parameters.csv",
            index=False,
        )
    )


    (
        dbscan_optimisation
        .stability_dataframe
        .to_csv(
            dbscan_directory
            / "dbscan_stability.csv",
            index=False,
        )
    )


    (
        dbscan_optimisation
        .summary_dataframe
        .to_csv(
            dbscan_directory
            / "dbscan_stability_summary.csv",
            index=False,
        )
    )


    # -------------------------------------------------------------------------
    # Temperature response
    # -------------------------------------------------------------------------

    temperature_response_dataframe = (
        pd.DataFrame(
            {
                "Temperature (K)":
                    temperature_response
                    .temperatures,

                "Response":
                    temperature_response
                    .response,

                "Count":
                    temperature_response
                    .counts,
            }
        )
    )


    temperature_response_dataframe.to_csv(
        tg_directory
        / "temperature_response.csv",
        index=False,
    )


    # -------------------------------------------------------------------------
    # Selected DBSCAN statistics
    # -------------------------------------------------------------------------

    selected_dbscan_dataframe = (
        dbscan_optimisation
        .parameter_dataframe[
            dbscan_optimisation
            .parameter_dataframe[
                "Min Samples"
            ]
            == selected_min_samples
        ]
        .copy()
    )


    median_epsilon = float(
        selected_dbscan_dataframe[
            "Epsilon"
        ].median()
    )

    mean_epsilon = float(
        selected_dbscan_dataframe[
            "Epsilon"
        ].mean()
    )

    median_clusters = float(
        selected_dbscan_dataframe[
            "Clusters"
        ].median()
    )

    mean_clusters = float(
        selected_dbscan_dataframe[
            "Clusters"
        ].mean()
    )

    median_noise_fraction = float(
        selected_dbscan_dataframe[
            "Noise Fraction"
        ].median()
    )

    mean_noise_fraction = float(
        selected_dbscan_dataframe[
            "Noise Fraction"
        ].mean()
    )


    # -------------------------------------------------------------------------
    # Analysis summary
    # -------------------------------------------------------------------------

    analysis_summary = {

        "analysis_level":
            "replica",

        "system":
            system_name,

        "simulation":
            simulation_name,

        "stage":
            stage,

        "sampling": {

            "stride":
                int(
                    analysis_stride
                ),

            "trajectory_frames":
                int(
                    len(
                        universe.trajectory
                    )
                ),

            "frames_per_chain":
                int(
                    len(
                        example_chain.frame_indices
                    )
                ),

            "polymer_chains":
                int(
                    len(
                        all_descriptors
                    )
                ),
        },

        "temperature_assignment": {

            "total_steps":
                int(
                    total_steps
                ),

            "reporter_frequency":
                int(
                    reporter_freq
                ),

            "max_temperature_K":
                float(
                    max_temp
                ),

            "min_temperature_K":
                float(
                    min_temp
                ),

            "temperature_change_K":
                float(
                    temp_change
                ),

            "n_temperature_blocks":
                int(
                    n_temperature_blocks
                ),
        },

        "pca": {

            "selected_components":
                int(
                    pca_optimisation
                    .selected_components
                ),

            "median_elbow":
                float(
                    pca_optimisation
                    .median_elbow
                ),

            "mean_elbow":
                float(
                    pca_optimisation
                    .mean_elbow
                ),

            "elbow_q1":
                float(
                    pca_optimisation
                    .elbow_q1
                ),

            "elbow_q3":
                float(
                    pca_optimisation
                    .elbow_q3
                ),

            "elbow_iqr":
                float(
                    pca_optimisation
                    .elbow_iqr
                ),

            "fraction_within_one_component":
                float(
                    pca_optimisation
                    .fraction_within_one_component
                ),
        },

        "dbscan": {

            "k":
                int(
                    selected_k
                ),

            "selected_min_samples":
                int(
                    selected_min_samples
                ),

            "median_epsilon":
                median_epsilon,

            "mean_epsilon":
                mean_epsilon,

            "median_clusters":
                median_clusters,

            "mean_clusters":
                mean_clusters,

            "median_noise_fraction":
                median_noise_fraction,

            "mean_noise_fraction":
                mean_noise_fraction,
        },

        "tg": {

            "observable":
                "historical_mean_dbscan_cluster_id",

            "tg_K":
                float(
                    tg_result.tg
                ),

            "C":
                float(
                    tg_result.C
                ),

            "s":
                float(
                    tg_result.s
                ),

            "d":
                float(
                    tg_result.d
                ),
        },

        "outputs": {

            "conformational_state_file":
                str(
                    conformational_state_path
                    .relative_to(
                        analysis_directory
                    )
                ),

            "temperature_response_file":
                str(
                    (
                        tg_directory
                        / "temperature_response.csv"
                    )
                    .relative_to(
                        analysis_directory
                    )
                ),
        },

        "figures_generated":
            bool(
                generate_figures
            ),
    }


    summary_path = (
        analysis_directory
        / "analysis_summary.json"
    )


    with open(
        summary_path,
        "w",
        encoding="utf-8",
    ) as handle:

        json.dump(
            analysis_summary,
            handle,
            indent=4,
        )


    # =========================================================================
    # STEP 12
    # Optional figures and report
    # =========================================================================

    figure_paths = []


    if generate_figures:

        print()
        print(
            "Step 12: generating replica figures and report"
        )

        print("-" * 80)


        figure_paths = (
            generate_analysis_figures(
                figure_directory=(
                    figure_directory
                ),
                temperatures=(
                    temperatures
                ),
                simulation_data=(
                    simulation_data
                ),
                pca_optimisation=(
                    pca_optimisation
                ),
                pca_results=(
                    pca_results
                ),
                dbscan_optimisation=(
                    dbscan_optimisation
                ),
                temperature_response=(
                    temperature_response
                ),
                tg_result=(
                    tg_result
                ),
                conformational_state_dataframe=(
                    conformational_state_dataframe
                ),
                system_name=(
                    system_name
                ),
                simulation_name=(
                    simulation_name
                ),
            )
        )


        write_analysis_report(
            output_path=(
                report_path
            ),
            system_name=(
                system_name
            ),
            simulation_name=(
                simulation_name
            ),
            stage=(
                stage
            ),
            loaded_simulation=(
                loaded_simulation
            ),
            analysis_stride=(
                analysis_stride
            ),
            temperatures=(
                temperatures
            ),
            all_descriptors=(
                all_descriptors
            ),
            pca_optimisation=(
                pca_optimisation
            ),
            dbscan_optimisation=(
                dbscan_optimisation
            ),
            selected_dbscan_dataframe=(
                selected_dbscan_dataframe
            ),
            tg_result=(
                tg_result
            ),
            conformational_state_dataframe=(
                conformational_state_dataframe
            ),
        )


        print(
            f"Saved report: "
            f"{report_path}"
        )


    # =========================================================================
    # Return result
    # =========================================================================

    result = {

        "analysis_level":
            "replica",

        "system_name":
            system_name,

        "simulation_name":
            simulation_name,

        "analysis_directory":
            str(
                analysis_directory
            ),

        "analysis_summary_path":
            str(
                summary_path
            ),

        "conformational_state_path":
            str(
                conformational_state_path
            ),

        "n_chains":
            int(
                len(
                    all_descriptors
                )
            ),

        "analysis_stride":
            int(
                analysis_stride
            ),

        "selected_pca_components":
            int(
                pca_optimisation
                .selected_components
            ),

        "dbscan_k":
            int(
                selected_k
            ),

        "dbscan_min_samples":
            int(
                selected_min_samples
            ),

        "tg_K":
            float(
                tg_result.tg
            ),

        "generate_figures":
            bool(
                generate_figures
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

        "report_path":
            (
                str(
                    report_path
                )
                if generate_figures
                else None
            ),
    }


    # =========================================================================
    # Final report
    # =========================================================================

    print()
    print("=" * 80)
    print(
        "REPLICA Tg ANALYSIS COMPLETE"
    )
    print("=" * 80)

    print(
        f"System:             "
        f"{system_name}"
    )

    print(
        f"Simulation:         "
        f"{simulation_name}"
    )

    print(
        f"Sampling stride:    "
        f"{analysis_stride}"
    )

    print(
        f"Chains analysed:    "
        f"{len(all_descriptors)}"
    )

    print(
        f"PCA dimensions:     "
        f"{pca_optimisation.selected_components}"
    )

    print(
        f"DBSCAN k:           "
        f"{selected_k}"
    )

    print(
        f"DBSCAN min_samples: "
        f"{selected_min_samples}"
    )

    print(
        f"Estimated Tg:       "
        f"{tg_result.tg:.2f} K"
    )

    print(
        f"Analysis output:    "
        f"{analysis_directory}"
    )

    print(
        f"State table:        "
        f"{conformational_state_path}"
    )


    if generate_figures:

        print(
            f"Figure output:      "
            f"{figure_directory}"
        )

        print(
            f"Figures generated:  "
            f"{len(figure_paths)}"
        )


    print("=" * 80)


    return result
```

</details>
