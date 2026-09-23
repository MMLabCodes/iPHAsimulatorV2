# analysis/pca.py

Standardise each chain's descriptor matrix, fit PCA and preserve frame indices and variance information. Different chains have separate fitted transforms even if they share a selected number of components.

[Current source](../../src/iphasimulator/analysis/pca.py)

This page is generated from source syntax. Original docstrings can be incomplete or outdated; module notes above identify known discrepancies. Call/return/error lists describe direct syntax, not all behaviour inside callees. Read the source excerpt for branch order and effects. No scientific execution is implied.

Explicit functions/methods/nested helpers: **2**.

## Module imports

```python
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from .descriptors import ChainDistanceDescriptors
```

## Classes and result records

### `ChainPCAResult`

PCA results for one polymer chain.

Attributes
----------
segment_id : str
    Segment identifier corresponding to the polymer chain.

frame_indices : numpy.ndarray
    Original trajectory frame indices represented in the PCA result.

transformed_data : numpy.ndarray
    PCA-transformed structural descriptors.

    Shape::

        (n_sampled_frames, n_components)

explained_variance_ratio : numpy.ndarray
    Fraction of total variance explained by each principal component.

cumulative_explained_variance : numpy.ndarray
    Cumulative fraction of variance explained by the retained
    principal components.

n_components : int
    Number of principal components retained.

Decorators: `dataclass(frozen=True)`.

Declared fields/defaults (instance state may also be set by methods):

```python
segment_id: str
frame_indices: np.ndarray
transformed_data: np.ndarray
explained_variance_ratio: np.ndarray
cumulative_explained_variance: np.ndarray
n_components: int
```

Dataclass-generated methods are implicit and are not counted as explicit function definitions.

## Function map

- [`calculate_chain_pca` — source line 75](#definition-75)
- [`calculate_all_chain_pca` — source line 183](#definition-183)

<a id="definition-75"></a>

## `calculate_chain_pca`

Source lines 75–176. Named callable; inspect its callers before treating it as a stable public API.

```python
def calculate_chain_pca(chain_descriptors: ChainDistanceDescriptors, n_components: int) -> ChainPCAResult: ...
```

### Purpose and original contract

Standardise and PCA-transform structural descriptors for one chain.

Structural descriptor features are first independently standardised
to zero mean and unit variance using StandardScaler. PCA is then
applied to the standardised descriptor matrix.

Parameters
----------
chain_descriptors : ChainDistanceDescriptors
    Pairwise intramolecular distance descriptors for one polymer
    chain.

n_components : int
    Number of principal components to retain.

Returns
-------
ChainPCAResult
    PCA-transformed descriptors and explained-variance information.

Raises
------
ValueError
    If n_components is invalid or the descriptor matrix cannot
    support the requested number of components.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| chain_descriptors | ChainDistanceDescriptors | required |
| n_components | int | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ChainPCAResult`, `PCA`, `StandardScaler`, `ValueError`, `chain_descriptors.frame_indices.copy`, `min`, `np.cumsum`, `pca.explained_variance_ratio_.copy`, `pca.fit_transform`, `scaler.fit_transform`.

Explicit return expressions; different branches may return different objects:

```python
ChainPCAResult(segment_id=chain_descriptors.segment_id, frame_indices=chain_descriptors.frame_indices.copy(), transformed_data=transformed_data, explained_variance_ratio=explained_variance_ratio, cumulative_explained_variance=cumulative_explained_variance, n_components=n_components)
```

Calls worth inspecting for I/O, state changes or delegated execution: `chain_descriptors.frame_indices.copy`, `pca.explained_variance_ratio_.copy`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('n_components must be greater than zero.')
ValueError('Descriptor matrix must be two-dimensional.')
ValueError('At least two sampled frames are required for PCA.')
ValueError(f'n_components={n_components} exceeds the maximum supported value of {max_components}.')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def calculate_chain_pca(
    chain_descriptors: ChainDistanceDescriptors,
    n_components: int,
) -> ChainPCAResult:
    """
    Standardise and PCA-transform structural descriptors for one chain.

    Structural descriptor features are first independently standardised
    to zero mean and unit variance using StandardScaler. PCA is then
    applied to the standardised descriptor matrix.

    Parameters
    ----------
    chain_descriptors : ChainDistanceDescriptors
        Pairwise intramolecular distance descriptors for one polymer
        chain.

    n_components : int
        Number of principal components to retain.

    Returns
    -------
    ChainPCAResult
        PCA-transformed descriptors and explained-variance information.

    Raises
    ------
    ValueError
        If n_components is invalid or the descriptor matrix cannot
        support the requested number of components.
    """

    if n_components <= 0:
        raise ValueError(
            "n_components must be greater than zero."
        )

    descriptors = chain_descriptors.descriptors

    if descriptors.ndim != 2:
        raise ValueError(
            "Descriptor matrix must be two-dimensional."
        )

    n_samples, n_features = descriptors.shape

    if n_samples < 2:
        raise ValueError(
            "At least two sampled frames are required for PCA."
        )

    max_components = min(
        n_samples,
        n_features,
    )

    if n_components > max_components:
        raise ValueError(
            f"n_components={n_components} exceeds the maximum "
            f"supported value of {max_components}."
        )

    # -------------------------------------------------------------------------
    # Standardise descriptor features
    # -------------------------------------------------------------------------

    scaler = StandardScaler()

    scaled_descriptors = scaler.fit_transform(
        descriptors
    )

    # -------------------------------------------------------------------------
    # Principal component analysis
    # -------------------------------------------------------------------------

    pca = PCA(
        n_components=n_components
    )

    transformed_data = pca.fit_transform(
        scaled_descriptors
    )

    explained_variance_ratio = (
        pca.explained_variance_ratio_.copy()
    )

    cumulative_explained_variance = (
        np.cumsum(
            explained_variance_ratio
        )
    )

    return ChainPCAResult(
        segment_id=chain_descriptors.segment_id,
        frame_indices=chain_descriptors.frame_indices.copy(),
        transformed_data=transformed_data,
        explained_variance_ratio=explained_variance_ratio,
        cumulative_explained_variance=cumulative_explained_variance,
        n_components=n_components,
    )
```

</details>

<a id="definition-183"></a>

## `calculate_all_chain_pca`

Source lines 183–232. Named callable; inspect its callers before treating it as a stable public API.

```python
def calculate_all_chain_pca(descriptors_by_segment: dict[str, ChainDistanceDescriptors], n_components: int) -> dict[str, ChainPCAResult]: ...
```

### Purpose and original contract

Perform independent PCA for all polymer chains.

Each chain is standardised and PCA-transformed separately.

Parameters
----------
descriptors_by_segment : dict
    Dictionary mapping segment IDs to ChainDistanceDescriptors.

n_components : int
    Number of principal components retained for each chain.

Returns
-------
dict
    Dictionary mapping segment IDs to ChainPCAResult objects.

Raises
------
ValueError
    If no descriptor sets are supplied.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| descriptors_by_segment | dict[str, ChainDistanceDescriptors] | required |
| n_components | int | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `calculate_chain_pca`, `descriptors_by_segment.items`.

Explicit return expressions; different branches may return different objects:

```python
results
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('No chain descriptor sets were supplied.')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def calculate_all_chain_pca(
    descriptors_by_segment: dict[
        str,
        ChainDistanceDescriptors,
    ],
    n_components: int,
) -> dict[str, ChainPCAResult]:
    """
    Perform independent PCA for all polymer chains.

    Each chain is standardised and PCA-transformed separately.

    Parameters
    ----------
    descriptors_by_segment : dict
        Dictionary mapping segment IDs to ChainDistanceDescriptors.

    n_components : int
        Number of principal components retained for each chain.

    Returns
    -------
    dict
        Dictionary mapping segment IDs to ChainPCAResult objects.

    Raises
    ------
    ValueError
        If no descriptor sets are supplied.
    """

    if not descriptors_by_segment:
        raise ValueError(
            "No chain descriptor sets were supplied."
        )

    results = {}

    for segment_id, chain_descriptors in (
        descriptors_by_segment.items()
    ):

        results[segment_id] = (
            calculate_chain_pca(
                chain_descriptors=chain_descriptors,
                n_components=n_components,
            )
        )

    return results
```

</details>
