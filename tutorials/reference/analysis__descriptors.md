# analysis/descriptors.py

Convert sampled frames into per-segment pairwise heavy-atom distances. Segment identity, original frame indices and feature count travel in the result record. Segment equals polymer-chain is an assumption; the heavy-atom selection is name-based and distances use periodic box information.

[Current source](../../src/iphasimulator/analysis/descriptors.py)

This page is generated from source syntax. Original docstrings can be incomplete or outdated; module notes above identify known discrepancies. Call/return/error lists describe direct syntax, not all behaviour inside callees. Read the source excerpt for branch order and effects. No scientific execution is implied.

Explicit functions/methods/nested helpers: **5**.

## Module imports

```python
from __future__ import annotations
from dataclasses import dataclass
import MDAnalysis as mda
import numpy as np
from MDAnalysis.lib.distances import self_distance_array
from .simulation_loader import LoadedSimulation
```

## Classes and result records

### `ChainDistanceDescriptors`

Pairwise intramolecular distance descriptors for one polymer chain.

Attributes
----------
segment_id : str
    Unique analysis identifier assigned to the polymer chain.

    Example::

        "chain_001"

segment_index : int
    Zero-based MDAnalysis segment index corresponding to the polymer chain.

topology_segid : str
    Original segment identifier stored in the topology.

    This value is retained for reference only and is not assumed to be
    unique.

frame_indices : numpy.ndarray
    Original trajectory frame indices used to generate descriptors.

descriptors : numpy.ndarray
    Pairwise heavy-atom distance descriptors.

    Shape::

        (n_sampled_frames, n_pairwise_distances)

n_heavy_atoms : int
    Number of heavy atoms used to generate each descriptor vector.

Decorators: `dataclass(frozen=True)`.

Declared fields/defaults (instance state may also be set by methods):

```python
segment_id: str
segment_index: int
topology_segid: str
frame_indices: np.ndarray
descriptors: np.ndarray
n_heavy_atoms: int
```

Dataclass-generated methods are implicit and are not counted as explicit function definitions.

## Function map

- [`get_polymer_segments` — source line 83](#definition-83)
- [`get_segment_heavy_atoms` — source line 124](#definition-124)
- [`get_chain_analysis_id` — source line 168](#definition-168)
- [`calculate_chain_distance_descriptors` — source line 204](#definition-204)
- [`calculate_all_chain_distance_descriptors` — source line 433](#definition-433)

<a id="definition-83"></a>

## `get_polymer_segments`

Source lines 83–117. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_polymer_segments(simulation: LoadedSimulation) -> list[mda.core.groups.Segment]: ...
```

### Purpose and original contract

Return polymer segments contained in a loaded simulation.

In current iPHAsimulator molecular systems, individual polymer chains
are represented by separate MDAnalysis segments.

Parameters
----------
simulation : LoadedSimulation
    Loaded molecular dynamics simulation.

Returns
-------
list of MDAnalysis Segment
    Segments present in the molecular system.

Raises
------
ValueError
    If no segments are present in the loaded topology.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| simulation | LoadedSimulation | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `list`.

Explicit return expressions; different branches may return different objects:

```python
segments
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('No segments were found in the loaded molecular system.')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_polymer_segments(
    simulation: LoadedSimulation,
) -> list[mda.core.groups.Segment]:
    """
    Return polymer segments contained in a loaded simulation.

    In current iPHAsimulator molecular systems, individual polymer chains
    are represented by separate MDAnalysis segments.

    Parameters
    ----------
    simulation : LoadedSimulation
        Loaded molecular dynamics simulation.

    Returns
    -------
    list of MDAnalysis Segment
        Segments present in the molecular system.

    Raises
    ------
    ValueError
        If no segments are present in the loaded topology.
    """

    segments = list(
        simulation.universe.segments
    )

    if not segments:
        raise ValueError(
            "No segments were found in the loaded molecular system."
        )

    return segments
```

</details>

<a id="definition-124"></a>

## `get_segment_heavy_atoms`

Source lines 124–161. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_segment_heavy_atoms(segment: mda.core.groups.Segment) -> mda.core.groups.AtomGroup: ...
```

### Purpose and original contract

Select heavy atoms from a polymer segment.

Hydrogen atoms are excluded using the same atom-name selection
employed in the original Tg analysis workflow.

Parameters
----------
segment : MDAnalysis Segment
    Polymer segment from which heavy atoms are selected.

Returns
-------
MDAnalysis AtomGroup
    Heavy atoms belonging to the segment.

Raises
------
ValueError
    If no heavy atoms are found.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| segment | mda.core.groups.Segment | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `segment.atoms.select_atoms`.

Explicit return expressions; different branches may return different objects:

```python
heavy_atoms
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError(f"No heavy atoms found for segment '{segment.segid}'.")
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_segment_heavy_atoms(
    segment: mda.core.groups.Segment,
) -> mda.core.groups.AtomGroup:
    """
    Select heavy atoms from a polymer segment.

    Hydrogen atoms are excluded using the same atom-name selection
    employed in the original Tg analysis workflow.

    Parameters
    ----------
    segment : MDAnalysis Segment
        Polymer segment from which heavy atoms are selected.

    Returns
    -------
    MDAnalysis AtomGroup
        Heavy atoms belonging to the segment.

    Raises
    ------
    ValueError
        If no heavy atoms are found.
    """

    heavy_atoms = (
        segment.atoms.select_atoms(
            "not name H*"
        )
    )

    if heavy_atoms.n_atoms == 0:
        raise ValueError(
            "No heavy atoms found for segment "
            f"'{segment.segid}'."
        )

    return heavy_atoms
```

</details>

<a id="definition-168"></a>

## `get_chain_analysis_id`

Source lines 168–197. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_chain_analysis_id(segment_index: int) -> str: ...
```

### Purpose and original contract

Return a stable analysis identifier for a polymer chain.

Parameters
----------
segment_index : int
    Zero-based segment index.

Returns
-------
str
    Chain identifier.

    Example::

        0 -> "chain_001"
        1 -> "chain_002"

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| segment_index | int | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`.

Explicit return expressions; different branches may return different objects:

```python
f'chain_{segment_index + 1:03d}'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('segment_index must be greater than or equal to zero.')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_chain_analysis_id(
    segment_index: int,
) -> str:
    """
    Return a stable analysis identifier for a polymer chain.

    Parameters
    ----------
    segment_index : int
        Zero-based segment index.

    Returns
    -------
    str
        Chain identifier.

        Example::

            0 -> "chain_001"
            1 -> "chain_002"
    """

    if segment_index < 0:
        raise ValueError(
            "segment_index must be greater than or equal to zero."
        )

    return (
        f"chain_{segment_index + 1:03d}"
    )
```

</details>

<a id="definition-204"></a>

## `calculate_chain_distance_descriptors`

Source lines 204–426. Named callable; inspect its callers before treating it as a stable public API.

```python
def calculate_chain_distance_descriptors(simulation: LoadedSimulation, segment_index: int, stride: int=1) -> ChainDistanceDescriptors: ...
```

### Purpose and original contract

Calculate pairwise intramolecular heavy-atom distances for one chain.

Each sampled trajectory frame is represented by all unique pairwise
distances between heavy atoms within the selected polymer chain.

Polymer chains are identified using their zero-based MDAnalysis segment
index rather than their topology segid. This avoids ambiguity when
topology segment identifiers are reused.

Parameters
----------
simulation : LoadedSimulation
    Loaded molecular dynamics simulation.

segment_index : int
    Zero-based index of the polymer segment to analyse.

    Example::

        0

    corresponds to the first segment in::

        simulation.universe.segments

stride : int, optional
    Trajectory frame sampling stride.

    A stride of 1 uses every frame, a stride of 10 uses every tenth
    frame, etc.

    Default:
        1

Returns
-------
ChainDistanceDescriptors
    Pairwise distance descriptors and associated metadata.

Raises
------
ValueError
    If stride or segment_index is invalid, or the selected segment
    contains insufficient heavy atoms.

IndexError
    If segment_index is outside the available segment range.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| simulation | LoadedSimulation | required |
| segment_index | int | required |
| stride | int | 1 |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ChainDistanceDescriptors`, `IndexError`, `ValueError`, `enumerate`, `get_chain_analysis_id`, `get_segment_heavy_atoms`, `len`, `np.arange`, `np.empty`, `self_distance_array`, `str`.

Explicit return expressions; different branches may return different objects:

```python
ChainDistanceDescriptors(segment_id=segment_id, segment_index=segment_index, topology_segid=topology_segid, frame_indices=frame_indices, descriptors=descriptors, n_heavy_atoms=n_heavy_atoms)
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('stride must be greater than zero.')
ValueError('segment_index must be greater than or equal to zero.')
IndexError(f'Segment index is outside the available range:\nRequested index:   {segment_index}\nAvailable segments: {len(segments)}')
ValueError(f"{segment_id} (topology segid '{topology_segid}') contains fewer than two heavy atoms.")
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def calculate_chain_distance_descriptors(
    simulation: LoadedSimulation,
    segment_index: int,
    stride: int = 1,
) -> ChainDistanceDescriptors:
    """
    Calculate pairwise intramolecular heavy-atom distances for one chain.

    Each sampled trajectory frame is represented by all unique pairwise
    distances between heavy atoms within the selected polymer chain.

    Polymer chains are identified using their zero-based MDAnalysis segment
    index rather than their topology segid. This avoids ambiguity when
    topology segment identifiers are reused.

    Parameters
    ----------
    simulation : LoadedSimulation
        Loaded molecular dynamics simulation.

    segment_index : int
        Zero-based index of the polymer segment to analyse.

        Example::

            0

        corresponds to the first segment in::

            simulation.universe.segments

    stride : int, optional
        Trajectory frame sampling stride.

        A stride of 1 uses every frame, a stride of 10 uses every tenth
        frame, etc.

        Default:
            1

    Returns
    -------
    ChainDistanceDescriptors
        Pairwise distance descriptors and associated metadata.

    Raises
    ------
    ValueError
        If stride or segment_index is invalid, or the selected segment
        contains insufficient heavy atoms.

    IndexError
        If segment_index is outside the available segment range.
    """

    # -------------------------------------------------------------------------
    # Validate stride
    # -------------------------------------------------------------------------

    if stride <= 0:
        raise ValueError(
            "stride must be greater than zero."
        )


    # -------------------------------------------------------------------------
    # Resolve universe
    # -------------------------------------------------------------------------

    universe = (
        simulation.universe
    )

    segments = (
        universe.segments
    )


    # -------------------------------------------------------------------------
    # Validate segment index
    # -------------------------------------------------------------------------

    if segment_index < 0:
        raise ValueError(
            "segment_index must be greater than or equal to zero."
        )

    if segment_index >= len(
        segments
    ):
        raise IndexError(
            "Segment index is outside the available range:\n"
            f"Requested index:   {segment_index}\n"
            f"Available segments: {len(segments)}"
        )


    # -------------------------------------------------------------------------
    # Select requested segment
    # -------------------------------------------------------------------------

    segment = (
        segments[
            segment_index
        ]
    )

    segment_id = (
        get_chain_analysis_id(
            segment_index
        )
    )

    topology_segid = (
        str(
            segment.segid
        )
    )


    # -------------------------------------------------------------------------
    # Select heavy atoms
    # -------------------------------------------------------------------------

    heavy_atoms = (
        get_segment_heavy_atoms(
            segment
        )
    )

    n_heavy_atoms = (
        heavy_atoms.n_atoms
    )

    if n_heavy_atoms < 2:
        raise ValueError(
            f"{segment_id} "
            f"(topology segid '{topology_segid}') "
            "contains fewer than two heavy atoms."
        )


    # -------------------------------------------------------------------------
    # Determine sampled frames
    # -------------------------------------------------------------------------

    n_frames = (
        len(
            universe.trajectory
        )
    )

    frame_indices = np.arange(
        0,
        n_frames,
        stride,
        dtype=int,
    )


    # -------------------------------------------------------------------------
    # Determine descriptor dimensionality
    # -------------------------------------------------------------------------

    n_distances = (
        n_heavy_atoms
        * (n_heavy_atoms - 1)
        // 2
    )


    # -------------------------------------------------------------------------
    # Allocate descriptor array
    # -------------------------------------------------------------------------

    descriptors = np.empty(
        (
            len(
                frame_indices
            ),
            n_distances,
        ),
        dtype=np.float64,
    )


    # -------------------------------------------------------------------------
    # Calculate descriptors
    # -------------------------------------------------------------------------

    for (
        output_index,
        frame_index,
    ) in enumerate(
        frame_indices
    ):

        universe.trajectory[
            frame_index
        ]

        descriptors[
            output_index
        ] = (
            self_distance_array(
                heavy_atoms.positions,
                box=universe.dimensions,
            )
        )


    # -------------------------------------------------------------------------
    # Return descriptor container
    # -------------------------------------------------------------------------

    return ChainDistanceDescriptors(
        segment_id=segment_id,
        segment_index=segment_index,
        topology_segid=topology_segid,
        frame_indices=frame_indices,
        descriptors=descriptors,
        n_heavy_atoms=n_heavy_atoms,
    )
```

</details>

<a id="definition-433"></a>

## `calculate_all_chain_distance_descriptors`

Source lines 433–541. Named callable; inspect its callers before treating it as a stable public API.

```python
def calculate_all_chain_distance_descriptors(simulation: LoadedSimulation, stride: int=1) -> dict[str, ChainDistanceDescriptors]: ...
```

### Purpose and original contract

Calculate pairwise heavy-atom distance descriptors for all polymer chains.

Each MDAnalysis segment is treated as an independent polymer chain and
processed separately.

Chains are identified internally using stable analysis identifiers such as::

    chain_001
    chain_002
    chain_003

The original topology segid is retained within each result object but is
not used as a unique key.

Parameters
----------
simulation : LoadedSimulation
    Loaded molecular dynamics simulation.

stride : int, optional
    Trajectory frame sampling stride.

    A stride of 1 uses every trajectory frame, a stride of 10 uses every
    tenth frame, etc.

    Default:
        1

Returns
-------
dict
    Dictionary mapping unique analysis chain IDs to
    ChainDistanceDescriptors objects.

    Example::

        {
            "chain_001": ChainDistanceDescriptors(...),
            "chain_002": ChainDistanceDescriptors(...),
            ...
        }

Raises
------
ValueError
    If stride is not greater than zero or no polymer segments are found.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| simulation | LoadedSimulation | required |
| stride | int | 1 |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `calculate_chain_distance_descriptors`, `get_chain_analysis_id`, `get_polymer_segments`, `len`, `range`.

Explicit return expressions; different branches may return different objects:

```python
descriptors_by_segment
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('stride must be greater than zero.')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def calculate_all_chain_distance_descriptors(
    simulation: LoadedSimulation,
    stride: int = 1,
) -> dict[str, ChainDistanceDescriptors]:
    """
    Calculate pairwise heavy-atom distance descriptors for all polymer chains.

    Each MDAnalysis segment is treated as an independent polymer chain and
    processed separately.

    Chains are identified internally using stable analysis identifiers such as::

        chain_001
        chain_002
        chain_003

    The original topology segid is retained within each result object but is
    not used as a unique key.

    Parameters
    ----------
    simulation : LoadedSimulation
        Loaded molecular dynamics simulation.

    stride : int, optional
        Trajectory frame sampling stride.

        A stride of 1 uses every trajectory frame, a stride of 10 uses every
        tenth frame, etc.

        Default:
            1

    Returns
    -------
    dict
        Dictionary mapping unique analysis chain IDs to
        ChainDistanceDescriptors objects.

        Example::

            {
                "chain_001": ChainDistanceDescriptors(...),
                "chain_002": ChainDistanceDescriptors(...),
                ...
            }

    Raises
    ------
    ValueError
        If stride is not greater than zero or no polymer segments are found.
    """

    # -------------------------------------------------------------------------
    # Validate stride
    # -------------------------------------------------------------------------

    if stride <= 0:
        raise ValueError(
            "stride must be greater than zero."
        )


    # -------------------------------------------------------------------------
    # Discover polymer segments
    # -------------------------------------------------------------------------

    segments = (
        get_polymer_segments(
            simulation
        )
    )


    # -------------------------------------------------------------------------
    # Generate descriptors
    # -------------------------------------------------------------------------

    descriptors_by_segment = {}


    for segment_index in range(
        len(
            segments
        )
    ):

        chain_id = (
            get_chain_analysis_id(
                segment_index
            )
        )

        descriptors_by_segment[
            chain_id
        ] = (
            calculate_chain_distance_descriptors(
                simulation=simulation,
                segment_index=segment_index,
                stride=stride,
            )
        )


    # -------------------------------------------------------------------------
    # Return results
    # -------------------------------------------------------------------------

    return descriptors_by_segment
```

</details>
