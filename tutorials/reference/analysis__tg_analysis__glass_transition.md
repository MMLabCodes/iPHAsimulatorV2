# analysis/tg_analysis/glass_transition.py

Build the historical mean-numeric-cluster-label response by nominal temperature, then fit a tanh-based curve and report d/s as Tg. Numeric labels are identifiers, so interpreting their average requires scientific scrutiny. The fit covariance is not returned and Tg is not bounded to the sampled temperature interval.

[Current source](../../src/iphasimulator/analysis/tg_analysis/glass_transition.py)

This page is generated from source syntax. Original docstrings can be incomplete or outdated; module notes above identify known discrepancies. Call/return/error lists describe direct syntax, not all behaviour inside callees. Read the source excerpt for branch order and effects. No scientific execution is implied.

Explicit functions/methods/nested helpers: **3**.

## Module imports

```python
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
import pandas as pd
from .clustering import ChainClusteringResult
from scipy.optimize import curve_fit
```

## Classes and result records

### `TemperatureResponse`

Temperature-dependent clustering response.

Decorators: `dataclass(frozen=True)`.

Declared fields/defaults (instance state may also be set by methods):

```python
temperatures: np.ndarray
response: np.ndarray
counts: np.ndarray
```

Dataclass-generated methods are implicit and are not counted as explicit function definitions.

### `TgFitResult`

Result of the provisional Tg transition fit.

Decorators: `dataclass(frozen=True)`.

Declared fields/defaults (instance state may also be set by methods):

```python
tg: float
C: float
s: float
d: float
temperatures: np.ndarray
fitted_response: np.ndarray
```

Dataclass-generated methods are implicit and are not counted as explicit function definitions.

## Function map

- [`calculate_historical_cluster_response` — source line 36](#definition-36)
- [`_historical_transition_function` — source line 118](#definition-118)
- [`fit_historical_tg` — source line 131](#definition-131)

<a id="definition-36"></a>

## `calculate_historical_cluster_response`

Source lines 36–101. Named callable; inspect its callers before treating it as a stable public API.

```python
def calculate_historical_cluster_response(clustering_results: dict[str, ChainClusteringResult], temperature_assignment: pd.DataFrame) -> TemperatureResponse: ...
```

### Purpose and original contract

Calculate the historical cluster-label response as a function of temperature.

Cluster labels are associated with their original trajectory frames and
grouped by nominal temperature. Mean numerical DBSCAN labels are then
calculated across all chains and sampled conformations.

Notes
-----
This reproduces the historical analysis behaviour for diagnostic purposes.
DBSCAN cluster labels are categorical identifiers, so this response should
not yet be interpreted as a physically rigorous order parameter.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| clustering_results | dict[str, ChainClusteringResult] | required |
| temperature_assignment | pd.DataFrame | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `TemperatureResponse`, `ValueError`, `clustering_results.items`, `data.groupby`, `data.groupby('Temperature')['Cluster Label'].agg`, `data.groupby('Temperature')['Cluster Label'].agg(['mean', 'count']).sort_index`, `dict`, `grouped.index.to_numpy`, `grouped['count'].to_numpy`, `grouped['mean'].to_numpy`, `pd.DataFrame`, `records.append`, `zip`.

Explicit return expressions; different branches may return different objects:

```python
TemperatureResponse(temperatures=grouped.index.to_numpy(dtype=float), response=grouped['mean'].to_numpy(dtype=float), counts=grouped['count'].to_numpy(dtype=int))
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('No clustering observations could be matched to temperatures.')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def calculate_historical_cluster_response(
    clustering_results: dict[str, ChainClusteringResult],
    temperature_assignment: pd.DataFrame,
) -> TemperatureResponse:
    """
    Calculate the historical cluster-label response as a function of temperature.

    Cluster labels are associated with their original trajectory frames and
    grouped by nominal temperature. Mean numerical DBSCAN labels are then
    calculated across all chains and sampled conformations.

    Notes
    -----
    This reproduces the historical analysis behaviour for diagnostic purposes.
    DBSCAN cluster labels are categorical identifiers, so this response should
    not yet be interpreted as a physically rigorous order parameter.
    """

    records = []

    frame_to_temperature = dict(
        zip(
            temperature_assignment["Frame"],
            temperature_assignment["Nominal Temperature (K)"],
        )
    )

    for segment_id, result in clustering_results.items():

        for frame_index, label in zip(
            result.frame_indices,
            result.labels,
        ):

            if frame_index not in frame_to_temperature:
                continue

            records.append(
                {
                    "Segment": segment_id,
                    "Frame": frame_index,
                    "Temperature": frame_to_temperature[frame_index],
                    "Cluster Label": label,
                }
            )

    if not records:
        raise ValueError(
            "No clustering observations could be matched to temperatures."
        )

    data = pd.DataFrame(records)

    grouped = (
        data
        .groupby("Temperature")
        ["Cluster Label"]
        .agg(["mean", "count"])
        .sort_index(ascending=False)
    )

    return TemperatureResponse(
        temperatures=grouped.index.to_numpy(dtype=float),
        response=grouped["mean"].to_numpy(dtype=float),
        counts=grouped["count"].to_numpy(dtype=int),
    )
```

</details>

<a id="definition-118"></a>

## `_historical_transition_function`

Source lines 118–128. Internal helper/protocol method.

```python
def _historical_transition_function(temperature, C, s, d): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| temperature | not annotated | required |
| C | not annotated | required |
| s | not annotated | required |
| d | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `np.tanh`.

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
def _historical_transition_function(
    temperature,
    C,
    s,
    d,
):
    return (
        C / 2.0
        * (1.0 - np.tanh(s * temperature - d))
        - 1.0
    )
```

</details>

<a id="definition-131"></a>

## `fit_historical_tg`

Source lines 131–275. Named callable; inspect its callers before treating it as a stable public API.

```python
def fit_historical_tg(temperature_response: TemperatureResponse) -> TgFitResult: ...
```

### Purpose and original contract

Fit the historical tanh transition model and estimate Tg.

This reproduces the fitting procedure used in the original
Tg analysis workflow.

Tg is defined as:

    Tg = d / s

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| temperature_response | TemperatureResponse | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `TgFitResult`, `ValueError`, `_historical_transition_function`, `abs`, `curve_fit`, `float`, `len`, `max`, `np.argsort`, `np.asarray`, `np.isfinite`, `np.isfinite(response).all`, `np.isfinite(temperatures).all`, `np.mean`, `np.median`.

Explicit return expressions; different branches may return different objects:

```python
TgFitResult(tg=float(tg), C=float(C), s=float(s), d=float(d), temperatures=temperatures_sorted, fitted_response=fitted_response)
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('At least four temperature points are required for Tg fitting.')
ValueError('Temperature values contain non-finite values.')
ValueError('Temperature response contains non-finite values.')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def fit_historical_tg(
    temperature_response: TemperatureResponse,
) -> TgFitResult:
    """
    Fit the historical tanh transition model and estimate Tg.

    This reproduces the fitting procedure used in the original
    Tg analysis workflow.

    Tg is defined as:

        Tg = d / s
    """

    temperatures = np.asarray(
        temperature_response.temperatures,
        dtype=float,
    )

    response = np.asarray(
        temperature_response.response,
        dtype=float,
    )

    if len(temperatures) < 4:
        raise ValueError(
            "At least four temperature points are required for Tg fitting."
        )

    if not np.isfinite(temperatures).all():
        raise ValueError(
            "Temperature values contain non-finite values."
        )

    if not np.isfinite(response).all():
        raise ValueError(
            "Temperature response contains non-finite values."
        )

    # ---------------------------------------------------------------------
    # Historical ordering
    # ---------------------------------------------------------------------

    order = np.argsort(
        temperatures
    )

    temperatures_sorted = temperatures[
        order
    ]

    response_sorted = response[
        order
    ]

    # ---------------------------------------------------------------------
    # Historical initial parameter estimates
    # ---------------------------------------------------------------------

    n_end = max(
        1,
        len(response_sorted) // 5,
    )

    response_low_temperature = np.mean(
        response_sorted[:n_end]
    )

    response_high_temperature = np.mean(
        response_sorted[-n_end:]
    )

    C0 = max(
        0.2,
        abs(
            response_low_temperature
            - response_high_temperature
        ),
    )

    tg0 = np.median(
        temperatures_sorted
    )

    s0 = 0.05

    d0 = s0 * tg0

    initial_guess = [
        C0,
        s0,
        d0,
    ]

    # ---------------------------------------------------------------------
    # Historical parameter bounds
    # ---------------------------------------------------------------------

    bounds = (
        [
            1e-6,   # C > 0
            1e-6,   # s > 0
            -np.inf,
        ],
        [
            np.inf,
            np.inf,
            np.inf,
        ],
    )

    # ---------------------------------------------------------------------
    # Fit transition function
    # ---------------------------------------------------------------------

    parameters, _ = curve_fit(
        _historical_transition_function,
        temperatures_sorted,
        response_sorted,
        p0=initial_guess,
        bounds=bounds,
        maxfev=20000,
    )

    C, s, d = parameters

    tg = d / s

    fitted_response = (
        _historical_transition_function(
            temperatures_sorted,
            C,
            s,
            d,
        )
    )

    return TgFitResult(
        tg=float(tg),
        C=float(C),
        s=float(s),
        d=float(d),
        temperatures=temperatures_sorted,
        fitted_response=fitted_response,
    )
```

</details>
