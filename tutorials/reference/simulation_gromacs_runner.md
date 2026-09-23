# simulation_gromacs_runner.py

Native GROMACS preparation, script generation, box/solvation operations and several levels of file/topology validation. Some functions write scripts; others invoke GROMACS. Keep these effects distinct when tracing a workflow. An output dataclass reports one operation, not complete scientific readiness.

[Current source](../../src/iphasimulator/simulation_gromacs_runner.py)

This page is generated from source syntax. Original docstrings can be incomplete or outdated; module notes above identify known discrepancies. Call/return/error lists describe direct syntax, not all behaviour inside callees. Read the source excerpt for branch order and effects. No scientific execution is implied.

Explicit functions/methods/nested helpers: **47**.

## Module imports

```python
from __future__ import annotations
from dataclasses import dataclass
from importlib import resources
from pathlib import Path
import shutil
import stat
import re
import subprocess
import warnings
from iphasimulator.conversion_amber_to_gromacs import convert_amber_to_gromacs
```

## Classes and result records

### `GromacsRunFiles`

Files generated for a staged GROMACS run.

Decorators: `dataclass(frozen=True)`.

Declared fields/defaults (instance state may also be set by methods):

```python
output_dir: Path
minim_mdp_path: Path
nvt_mdp_path: Path
npt_mdp_path: Path
production_mdp_path: Path
run_script_path: Path
```

Dataclass-generated methods are implicit and are not counted as explicit function definitions.

### `GromacsPreparedRunFolder`

Files generated for a GROMACS run folder.

Decorators: `dataclass(frozen=True)`.

Declared fields/defaults (instance state may also be set by methods):

```python
output_dir: Path
workflow_type: str
dry_polymer_dir: Path
solvated_polymer_dir: Path
charmm_gui_membrane_dir: Path
step5_input_gro_path: Path
topol_top_path: Path
index_ndx_path: Path
mdp_paths: tuple[Path, ...]
local_script_path: Path
hpc_script_path: Path
charmm_gui_membrane_hpc_script_path: Path
```

Dataclass-generated methods are implicit and are not counted as explicit function definitions.

### `GromacsTopologyValidation`

Validation result for GROMACS topology include files.

Decorators: `dataclass(frozen=True)`.

Declared fields/defaults (instance state may also be set by methods):

```python
topol_top_path: Path
is_standalone: bool
included_files: tuple[Path, ...]
missing_files: tuple[Path, ...]
```

Dataclass-generated methods are implicit and are not counted as explicit function definitions.

### `GromacsLocalMinimizationCheck`

Files and command needed to run local GROMACS minimisation.

Decorators: `dataclass(frozen=True)`.

Declared fields/defaults (instance state may also be set by methods):

```python
output_dir: Path
required_files: tuple[Path, ...]
missing_files: tuple[Path, ...]
command: tuple[str, ...]
```

Dataclass-generated methods are implicit and are not counted as explicit function definitions.

### `GromacsBoxValidation`

Box-size validation against GROMACS nonbonded cutoffs.

Decorators: `dataclass(frozen=True)`.

Declared fields/defaults (instance state may also be set by methods):

```python
gro_path: Path
mdp_path: Path
box_vectors_nm: tuple[float, ...]
shortest_box_vector_nm: float
cutoffs_nm: dict[str, float]
```

Dataclass-generated methods are implicit and are not counted as explicit function definitions.

### `GromacsSolvationFiles`

Files generated for the standard GROMACS solvate/genion workflow.

Decorators: `dataclass(frozen=True)`.

Declared fields/defaults (instance state may also be set by methods):

```python
output_dir: Path
ions_mdp_path: Path
solvation_itp_paths: tuple[Path, ...]
solvent_itp_path: Path
cation_itp_path: Path
anion_itp_path: Path
solvate_script_path: Path
local_script_path: Path
hpc_script_path: Path
charmm_gui_membrane_hpc_script_path: Path
```

Dataclass-generated methods are implicit and are not counted as explicit function definitions.

### `GromacsSolvatedTopologyValidation`

Water and ion molecule counts parsed from a GROMACS topology.

Decorators: `dataclass(frozen=True)`.

Declared fields/defaults (instance state may also be set by methods):

```python
topol_top_path: Path
molecule_counts: dict[str, int]
water_count: int
cation_count: int
anion_count: int
```

Dataclass-generated methods are implicit and are not counted as explicit function definitions.

### `GromacsGromppValidation`

Result of a lightweight GROMACS ``grompp`` validation command.

Decorators: `dataclass(frozen=True)`.

Declared fields/defaults (instance state may also be set by methods):

```python
command: tuple[str, ...]
returncode: int
stdout: str
stderr: str
```

Dataclass-generated methods are implicit and are not counted as explicit function definitions.

### `GromacsCoordinateTopologyValidation`

Atom-count comparison between a GRO coordinate file and topology.

Decorators: `dataclass(frozen=True)`.

Declared fields/defaults (instance state may also be set by methods):

```python
gro_path: Path
topol_top_path: Path
coordinate_atom_count: int
molecule_counts: dict[str, int]
molecule_atom_counts: dict[str, int]
expected_atom_count: int | None
```

Dataclass-generated methods are implicit and are not counted as explicit function definitions.

## Function map

- [`GromacsTopologyValidation.valid` — source line 66](#definition-66)
- [`GromacsLocalMinimizationCheck.ready` — source line 80](#definition-80)
- [`GromacsLocalMinimizationCheck.command_text` — source line 84](#definition-84)
- [`GromacsBoxValidation.max_cutoff_nm` — source line 99](#definition-99)
- [`GromacsBoxValidation.valid` — source line 105](#definition-105)
- [`GromacsSolvationFiles.tip3p_ions_itp_path` — source line 127](#definition-127)
- [`GromacsSolvatedTopologyValidation.sodium_count` — source line 144](#definition-144)
- [`GromacsSolvatedTopologyValidation.chloride_count` — source line 150](#definition-150)
- [`GromacsSolvatedTopologyValidation.has_water` — source line 156](#definition-156)
- [`GromacsSolvatedTopologyValidation.has_ions` — source line 160](#definition-160)
- [`GromacsGromppValidation.ok` — source line 174](#definition-174)
- [`GromacsCoordinateTopologyValidation.can_compare` — source line 190](#definition-190)
- [`GromacsCoordinateTopologyValidation.valid` — source line 194](#definition-194)
- [`_run_script` — source line 357](#definition-357)
- [`write_gromacs_run_files` — source line 379](#definition-379)
- [`_copy_mdp_templates` — source line 414](#definition-414)
- [`_copy_workflow_inputs` — source line 428](#definition-428)
- [`_copy_solvation_templates` — source line 449](#definition-449)
- [`_read_gro_atom_count` — source line 465](#definition-465)
- [`_write_default_index` — source line 475](#definition-475)
- [`_read_gro_box_vectors` — source line 485](#definition-485)
- [`_read_mdp_cutoffs` — source line 502](#definition-502)
- [`create_gromacs_simulation_box` — source line 519](#definition-519)
- [`validate_gromacs_box_against_mdp` — source line 570](#definition-570)
- [`_write_local_minimization_script` — source line 601](#definition-601)
- [`_write_hpc_equilibration_script` — source line 679](#definition-679)
- [`_write_kcl_polymer_hpc_script` — source line 729](#definition-729)
- [`_infer_polymer_hpc_job_name` — source line 771](#definition-771)
- [`_write_solvate_script` — source line 777](#definition-777)
- [`_ensure_topology_include` — source line 1055](#definition-1055)
- [`_write_solvation_topology_templates` — source line 1077](#definition-1077)
- [`_read_topology_molecule_counts` — source line 1087](#definition-1087)
- [`_topology_source_paths` — source line 1111](#definition-1111)
- [`_read_moleculetype_atom_counts` — source line 1125](#definition-1125)
- [`count_gro_atoms` — source line 1155](#definition-1155)
- [`validate_gromacs_coordinate_topology_counts` — source line 1168](#definition-1168)
- [`_sum_named_molecule_counts` — source line 1205](#definition-1205)
- [`_resolve_solvated_polymer_dir` — source line 1215](#definition-1215)
- [`_populate_solvated_polymer_inputs` — source line 1225](#definition-1225)
- [`_clean_solvated_polymer_generated_files` — source line 1239](#definition-1239)
- [`write_gromacs_solvation_files` — source line 1270](#definition-1270)
- [`validate_gromacs_solvated_topology` — source line 1336](#definition-1336)
- [`validate_gromacs_solvation_grompp` — source line 1359](#definition-1359)
- [`validate_gromacs_run_folder` — source line 1422](#definition-1422)
- [`check_gromacs_minimization_inputs` — source line 1458](#definition-1458)
- [`run_gromacs_local_minimization` — source line 1476](#definition-1476)
- [`prepare_gromacs_run_folder` — source line 1505](#definition-1505)

<a id="definition-66"></a>

## `GromacsTopologyValidation.valid`

Source lines 66–67. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `property`.

```python
def valid(self) -> bool: ...
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
not self.missing_files
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def valid(self) -> bool:
    return not self.missing_files
```

</details>

<a id="definition-80"></a>

## `GromacsLocalMinimizationCheck.ready`

Source lines 80–81. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `property`.

```python
def ready(self) -> bool: ...
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
not self.missing_files
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def ready(self) -> bool:
    return not self.missing_files
```

</details>

<a id="definition-84"></a>

## `GromacsLocalMinimizationCheck.command_text`

Source lines 84–85. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `property`.

```python
def command_text(self) -> str: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `' '.join`.

Explicit return expressions; different branches may return different objects:

```python
' '.join(self.command)
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def command_text(self) -> str:
    return " ".join(self.command)
```

</details>

<a id="definition-99"></a>

## `GromacsBoxValidation.max_cutoff_nm`

Source lines 99–102. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `property`.

```python
def max_cutoff_nm(self) -> float | None: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `max`, `self.cutoffs_nm.values`.

Explicit return expressions; different branches may return different objects:

```python
None
max(self.cutoffs_nm.values())
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def max_cutoff_nm(self) -> float | None:
    if not self.cutoffs_nm:
        return None
    return max(self.cutoffs_nm.values())
```

</details>

<a id="definition-105"></a>

## `GromacsBoxValidation.valid`

Source lines 105–108. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `property`.

```python
def valid(self) -> bool: ...
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
True
self.shortest_box_vector_nm > 2 * self.max_cutoff_nm
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def valid(self) -> bool:
    if self.max_cutoff_nm is None:
        return True
    return self.shortest_box_vector_nm > 2 * self.max_cutoff_nm
```

</details>

<a id="definition-127"></a>

## `GromacsSolvationFiles.tip3p_ions_itp_path`

Source lines 127–130. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `property`.

```python
def tip3p_ions_itp_path(self) -> Path: ...
```

### Purpose and original contract

Backward-compatible alias for older callers.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |

### How to read this implementation

No direct function calls were found in this definition's own body.

Explicit return expressions; different branches may return different objects:

```python
self.solvent_itp_path
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def tip3p_ions_itp_path(self) -> Path:
    """Backward-compatible alias for older callers."""

    return self.solvent_itp_path
```

</details>

<a id="definition-144"></a>

## `GromacsSolvatedTopologyValidation.sodium_count`

Source lines 144–147. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `property`.

```python
def sodium_count(self) -> int: ...
```

### Purpose and original contract

Backward-compatible alias; may include POT/K in newer workflows.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |

### How to read this implementation

No direct function calls were found in this definition's own body.

Explicit return expressions; different branches may return different objects:

```python
self.cation_count
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def sodium_count(self) -> int:
    """Backward-compatible alias; may include POT/K in newer workflows."""

    return self.cation_count
```

</details>

<a id="definition-150"></a>

## `GromacsSolvatedTopologyValidation.chloride_count`

Source lines 150–153. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `property`.

```python
def chloride_count(self) -> int: ...
```

### Purpose and original contract

Backward-compatible alias for anion count.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |

### How to read this implementation

No direct function calls were found in this definition's own body.

Explicit return expressions; different branches may return different objects:

```python
self.anion_count
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def chloride_count(self) -> int:
    """Backward-compatible alias for anion count."""

    return self.anion_count
```

</details>

<a id="definition-156"></a>

## `GromacsSolvatedTopologyValidation.has_water`

Source lines 156–157. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `property`.

```python
def has_water(self) -> bool: ...
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
self.water_count > 0
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def has_water(self) -> bool:
    return self.water_count > 0
```

</details>

<a id="definition-160"></a>

## `GromacsSolvatedTopologyValidation.has_ions`

Source lines 160–161. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `property`.

```python
def has_ions(self) -> bool: ...
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
self.cation_count + self.anion_count > 0
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def has_ions(self) -> bool:
    return self.cation_count + self.anion_count > 0
```

</details>

<a id="definition-174"></a>

## `GromacsGromppValidation.ok`

Source lines 174–175. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `property`.

```python
def ok(self) -> bool: ...
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
self.returncode == 0
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def ok(self) -> bool:
    return self.returncode == 0
```

</details>

<a id="definition-190"></a>

## `GromacsCoordinateTopologyValidation.can_compare`

Source lines 190–191. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `property`.

```python
def can_compare(self) -> bool: ...
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
self.expected_atom_count is not None
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def can_compare(self) -> bool:
    return self.expected_atom_count is not None
```

</details>

<a id="definition-194"></a>

## `GromacsCoordinateTopologyValidation.valid`

Source lines 194–195. Named callable; inspect its callers before treating it as a stable public API.

Decorators: `property`.

```python
def valid(self) -> bool: ...
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
self.expected_atom_count == self.coordinate_atom_count
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def valid(self) -> bool:
    return self.expected_atom_count == self.coordinate_atom_count
```

</details>

<a id="definition-357"></a>

## `_run_script`

Source lines 357–376. Internal helper/protocol method.

```python
def _run_script(system_name: str) -> str: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| system_name | str | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `'\n'.join`.

Explicit return expressions; different branches may return different objects:

```python
'\n'.join(['#!/usr/bin/env bash', 'set -euo pipefail', '', f'gmx grompp -f minim.mdp -c {system_name}.gro -p {system_name}.top -o minim.tpr', 'gmx mdrun -deffnm minim', '', f'gmx grompp -f nvt.mdp -c minim.gro -p {system_name}.top -o nvt.tpr', 'gmx mdrun -deffnm nvt', '', f'gmx grompp -f npt.mdp -c nvt.gro -p {system_name}.top -o npt.tpr', 'gmx mdrun -deffnm npt', '', f'gmx grompp -f production.md … [full expression below]
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _run_script(system_name: str) -> str:
    return "\n".join(
        [
            "#!/usr/bin/env bash",
            "set -euo pipefail",
            "",
            f"gmx grompp -f minim.mdp -c {system_name}.gro -p {system_name}.top -o minim.tpr",
            "gmx mdrun -deffnm minim",
            "",
            f"gmx grompp -f nvt.mdp -c minim.gro -p {system_name}.top -o nvt.tpr",
            "gmx mdrun -deffnm nvt",
            "",
            f"gmx grompp -f npt.mdp -c nvt.gro -p {system_name}.top -o npt.tpr",
            "gmx mdrun -deffnm npt",
            "",
            f"gmx grompp -f production.mdp -c npt.gro -p {system_name}.top -o production.tpr",
            "gmx mdrun -deffnm production",
            "",
        ]
    )
```

</details>

<a id="definition-379"></a>

## `write_gromacs_run_files`

Source lines 379–411. Named callable; inspect its callers before treating it as a stable public API.

```python
def write_gromacs_run_files(output_dir: str | Path, system_name: str='system') -> GromacsRunFiles: ...
```

### Purpose and original contract

Write basic GROMACS ``mdp`` files and a staged run script.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| output_dir | str \| Path | required |
| system_name | str | 'system' |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `GromacsRunFiles`, `Path`, `ValueError`, `_run_script`, `minim_mdp_path.write_text`, `npt_mdp_path.write_text`, `nvt_mdp_path.write_text`, `output_path.mkdir`, `production_mdp_path.write_text`, `run_script_path.chmod`, `run_script_path.stat`, `run_script_path.write_text`, `system_name.strip`.

Explicit return expressions; different branches may return different objects:

```python
GromacsRunFiles(output_dir=output_path, minim_mdp_path=minim_mdp_path, nvt_mdp_path=nvt_mdp_path, npt_mdp_path=npt_mdp_path, production_mdp_path=production_mdp_path, run_script_path=run_script_path)
```

Calls worth inspecting for I/O, state changes or delegated execution: `minim_mdp_path.write_text`, `npt_mdp_path.write_text`, `nvt_mdp_path.write_text`, `output_path.mkdir`, `production_mdp_path.write_text`, `run_script_path.write_text`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('system_name must be a non-empty string')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def write_gromacs_run_files(
    output_dir: str | Path,
    system_name: str = "system",
) -> GromacsRunFiles:
    """Write basic GROMACS ``mdp`` files and a staged run script."""

    if not system_name.strip():
        raise ValueError("system_name must be a non-empty string")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    minim_mdp_path = output_path / "minim.mdp"
    nvt_mdp_path = output_path / "nvt.mdp"
    npt_mdp_path = output_path / "npt.mdp"
    production_mdp_path = output_path / "production.mdp"
    run_script_path = output_path / "run_gromacs.sh"

    minim_mdp_path.write_text(MINIM_MDP)
    nvt_mdp_path.write_text(NVT_MDP)
    npt_mdp_path.write_text(NPT_MDP)
    production_mdp_path.write_text(PRODUCTION_MDP)
    run_script_path.write_text(_run_script(system_name))
    run_script_path.chmod(run_script_path.stat().st_mode | stat.S_IXUSR)

    return GromacsRunFiles(
        output_dir=output_path,
        minim_mdp_path=minim_mdp_path,
        nvt_mdp_path=nvt_mdp_path,
        npt_mdp_path=npt_mdp_path,
        production_mdp_path=production_mdp_path,
        run_script_path=run_script_path,
    )
```

</details>

<a id="definition-414"></a>

## `_copy_mdp_templates`

Source lines 414–425. Internal helper/protocol method.

```python
def _copy_mdp_templates(output_dir: Path, template_names: tuple[str, ...]) -> tuple[Path, ...]: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| output_dir | Path | required |
| template_names | tuple[str, ...] | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `destination.write_text`, `resources.files`, `resources.files('iphasimulator').joinpath`, `source.read_text`, `template_root.joinpath`, `tuple`, `written.append`.

Explicit return expressions; different branches may return different objects:

```python
tuple(written)
```

Calls worth inspecting for I/O, state changes or delegated execution: `destination.write_text`, `source.read_text`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _copy_mdp_templates(
    output_dir: Path,
    template_names: tuple[str, ...],
) -> tuple[Path, ...]:
    template_root = resources.files("iphasimulator").joinpath("data/gromacs_mdp")
    written: list[Path] = []
    for template_name in template_names:
        destination = output_dir / template_name
        source = template_root.joinpath(template_name)
        destination.write_text(source.read_text())
        written.append(destination)
    return tuple(written)
```

</details>

<a id="definition-428"></a>

## `_copy_workflow_inputs`

Source lines 428–446. Internal helper/protocol method.

```python
def _copy_workflow_inputs(source_dir: Path, destination_dir: Path, *, overwrite: bool=True) -> tuple[Path, Path, Path]: ...
```

### Purpose and original contract

Copy canonical GROMACS input files into a self-contained workflow dir.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| source_dir | Path | required |
| destination_dir | Path | required |
| overwrite (keyword-only) | bool | True |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `FileNotFoundError`, `copied_paths.append`, `destination.exists`, `destination_dir.mkdir`, `shutil.copy2`, `source.exists`.

Explicit return expressions; different branches may return different objects:

```python
(copied_paths[0], copied_paths[1], copied_paths[2])
```

Calls worth inspecting for I/O, state changes or delegated execution: `destination_dir.mkdir`, `shutil.copy2`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
FileNotFoundError(f'Required workflow input is missing: {source}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _copy_workflow_inputs(
    source_dir: Path,
    destination_dir: Path,
    *,
    overwrite: bool = True,
) -> tuple[Path, Path, Path]:
    """Copy canonical GROMACS input files into a self-contained workflow dir."""

    destination_dir.mkdir(parents=True, exist_ok=True)
    copied_paths: list[Path] = []
    for filename in ("step5_input.gro", "topol.top", "index.ndx"):
        source = source_dir / filename
        destination = destination_dir / filename
        if not source.exists():
            raise FileNotFoundError(f"Required workflow input is missing: {source}")
        if overwrite or not destination.exists():
            shutil.copy2(source, destination)
        copied_paths.append(destination)
    return copied_paths[0], copied_paths[1], copied_paths[2]
```

</details>

<a id="definition-449"></a>

## `_copy_solvation_templates`

Source lines 449–462. Internal helper/protocol method.

```python
def _copy_solvation_templates(output_dir: Path, template_names: tuple[str, ...]=GROMACS_SOLVATION_TEMPLATE_NAMES) -> tuple[Path, ...]: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| output_dir | Path | required |
| template_names | tuple[str, ...] | GROMACS_SOLVATION_TEMPLATE_NAMES |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `destination.write_text`, `resources.files`, `resources.files('iphasimulator').joinpath`, `source.read_text`, `template_root.joinpath`, `tuple`, `written.append`.

Explicit return expressions; different branches may return different objects:

```python
tuple(written)
```

Calls worth inspecting for I/O, state changes or delegated execution: `destination.write_text`, `source.read_text`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _copy_solvation_templates(
    output_dir: Path,
    template_names: tuple[str, ...] = GROMACS_SOLVATION_TEMPLATE_NAMES,
) -> tuple[Path, ...]:
    template_root = resources.files("iphasimulator").joinpath(
        GROMACS_SOLVATION_TEMPLATE_DIR
    )
    written: list[Path] = []
    for template_name in template_names:
        destination = output_dir / template_name
        source = template_root.joinpath(template_name)
        destination.write_text(source.read_text())
        written.append(destination)
    return tuple(written)
```

</details>

<a id="definition-465"></a>

## `_read_gro_atom_count`

Source lines 465–472. Internal helper/protocol method.

```python
def _read_gro_atom_count(gro_path: Path) -> int: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| gro_path | Path | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `gro_path.read_text`, `gro_path.read_text().splitlines`, `int`, `len`, `lines[1].strip`.

Explicit return expressions; different branches may return different objects:

```python
int(lines[1].strip())
```

Calls worth inspecting for I/O, state changes or delegated execution: `gro_path.read_text`, `gro_path.read_text().splitlines`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError(f'Invalid GRO file, missing atom-count line: {gro_path}')
ValueError(f'Invalid GRO atom count in {gro_path}: {lines[1]!r}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _read_gro_atom_count(gro_path: Path) -> int:
    lines = gro_path.read_text().splitlines()
    if len(lines) < 2:
        raise ValueError(f"Invalid GRO file, missing atom-count line: {gro_path}")
    try:
        return int(lines[1].strip())
    except ValueError as exc:
        raise ValueError(f"Invalid GRO atom count in {gro_path}: {lines[1]!r}") from exc
```

</details>

<a id="definition-475"></a>

## `_write_default_index`

Source lines 475–482. Internal helper/protocol method.

```python
def _write_default_index(gro_path: Path, index_path: Path) -> None: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| gro_path | Path | required |
| index_path | Path | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `' '.join`, `'\n'.join`, `_read_gro_atom_count`, `index_path.write_text`, `lines.append`, `range`, `str`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Calls worth inspecting for I/O, state changes or delegated execution: `_read_gro_atom_count`, `index_path.write_text`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _write_default_index(gro_path: Path, index_path: Path) -> None:
    atom_count = _read_gro_atom_count(gro_path)
    atom_numbers = [str(number) for number in range(1, atom_count + 1)]
    lines = ["[ System ]"]
    for start in range(0, atom_count, 15):
        lines.append(" ".join(atom_numbers[start : start + 15]))
    lines.append("")
    index_path.write_text("\n".join(lines))
```

</details>

<a id="definition-485"></a>

## `_read_gro_box_vectors`

Source lines 485–499. Internal helper/protocol method.

```python
def _read_gro_box_vectors(gro_path: Path) -> tuple[float, ...]: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| gro_path | Path | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `float`, `gro_path.read_text`, `gro_path.read_text().splitlines`, `len`, `line.strip`, `lines[-1].split`, `tuple`.

Explicit return expressions; different branches may return different objects:

```python
box_vectors
```

Calls worth inspecting for I/O, state changes or delegated execution: `gro_path.read_text`, `gro_path.read_text().splitlines`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError(f'Invalid GRO file, missing box-vector line: {gro_path}')
ValueError(f'Invalid GRO box-vector line in {gro_path}: {lines[-1]!r}')
ValueError(f'Invalid GRO box-vector count in {gro_path}: expected 3 or 9 values')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _read_gro_box_vectors(gro_path: Path) -> tuple[float, ...]:
    lines = [line for line in gro_path.read_text().splitlines() if line.strip()]
    if len(lines) < 3:
        raise ValueError(f"Invalid GRO file, missing box-vector line: {gro_path}")
    try:
        box_vectors = tuple(float(value) for value in lines[-1].split())
    except ValueError as exc:
        raise ValueError(
            f"Invalid GRO box-vector line in {gro_path}: {lines[-1]!r}"
        ) from exc
    if len(box_vectors) not in {3, 9}:
        raise ValueError(
            f"Invalid GRO box-vector count in {gro_path}: expected 3 or 9 values"
        )
    return box_vectors
```

</details>

<a id="definition-502"></a>

## `_read_mdp_cutoffs`

Source lines 502–516. Internal helper/protocol method.

```python
def _read_mdp_cutoffs(mdp_path: Path) -> dict[str, float]: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| mdp_path | Path | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `float`, `key.lower`, `line.split`, `line.split(';', 1)[0].strip`, `mdp_path.read_text`, `mdp_path.read_text().splitlines`, `part.strip`, `raw_value.split`, `setting.split`.

Explicit return expressions; different branches may return different objects:

```python
cutoffs
```

Calls worth inspecting for I/O, state changes or delegated execution: `mdp_path.read_text`, `mdp_path.read_text().splitlines`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _read_mdp_cutoffs(mdp_path: Path) -> dict[str, float]:
    cutoffs: dict[str, float] = {}
    for line in mdp_path.read_text().splitlines():
        setting = line.split(";", 1)[0].strip()
        if "=" not in setting:
            continue
        key, raw_value = (part.strip() for part in setting.split("=", 1))
        key = key.lower()
        if key not in MDP_CUTOFF_KEYS:
            continue
        try:
            cutoffs[key] = float(raw_value.split()[0])
        except (IndexError, ValueError):
            continue
    return cutoffs
```

</details>

<a id="definition-519"></a>

## `create_gromacs_simulation_box`

Source lines 519–567. Named callable; inspect its callers before treating it as a stable public API.

```python
def create_gromacs_simulation_box(input_gro: str | Path, output_gro: str | Path, *, padding_nm: float=3.0, box_type: str='cubic', gmx_command: str='gmx', runner=subprocess.run) -> Path: ...
```

### Purpose and original contract

Create a centered GROMACS simulation box with ``gmx editconf``.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| input_gro | str \| Path | required |
| output_gro | str \| Path | required |
| padding_nm (keyword-only) | float | 3.0 |
| box_type (keyword-only) | str | 'cubic' |
| gmx_command (keyword-only) | str | 'gmx' |
| runner (keyword-only) | not annotated | subprocess.run |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `FileNotFoundError`, `Path`, `RuntimeError`, `output_path.exists`, `runner`, `str`.

Explicit return expressions; different branches may return different objects:

```python
output_path
```

Calls worth inspecting for I/O, state changes or delegated execution: `runner`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
RuntimeError("GROMACS executable was not found while creating the simulation box. Install GROMACS or make sure the 'gmx' command is on PATH.")
RuntimeError(f'GROMACS editconf failed while creating the simulation box with return code {result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}')
FileNotFoundError(f'GROMACS editconf did not write: {output_path}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def create_gromacs_simulation_box(
    input_gro: str | Path,
    output_gro: str | Path,
    *,
    padding_nm: float = 3.0,
    box_type: str = "cubic",
    gmx_command: str = "gmx",
    runner=subprocess.run,
) -> Path:
    """Create a centered GROMACS simulation box with ``gmx editconf``."""

    input_path = Path(input_gro)
    output_path = Path(output_gro)
    command = [
        gmx_command,
        "editconf",
        "-f",
        input_path.name,
        "-o",
        output_path.name,
        "-c",
        "-d",
        str(padding_nm),
        "-bt",
        box_type,
    ]
    try:
        result = runner(
            command,
            cwd=input_path.parent,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except FileNotFoundError as exc:
        raise RuntimeError(
            "GROMACS executable was not found while creating the simulation box. "
            "Install GROMACS or make sure the 'gmx' command is on PATH."
        ) from exc

    if result.returncode != 0:
        raise RuntimeError(
            "GROMACS editconf failed while creating the simulation box with "
            f"return code {result.returncode}.\nSTDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )
    if not output_path.exists():
        raise FileNotFoundError(f"GROMACS editconf did not write: {output_path}")
    return output_path
```

</details>

<a id="definition-570"></a>

## `validate_gromacs_box_against_mdp`

Source lines 570–598. Named callable; inspect its callers before treating it as a stable public API.

```python
def validate_gromacs_box_against_mdp(gro_file: str | Path, mdp_file: str | Path) -> GromacsBoxValidation: ...
```

### Purpose and original contract

Warn when a GRO box is too small for the MDP nonbonded cutoffs.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| gro_file | str \| Path | required |
| mdp_file | str \| Path | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `GromacsBoxValidation`, `Path`, `_read_gro_box_vectors`, `_read_mdp_cutoffs`, `min`, `warnings.warn`.

Explicit return expressions; different branches may return different objects:

```python
validation
```

Calls worth inspecting for I/O, state changes or delegated execution: `_read_gro_box_vectors`, `_read_mdp_cutoffs`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def validate_gromacs_box_against_mdp(
    gro_file: str | Path,
    mdp_file: str | Path,
) -> GromacsBoxValidation:
    """Warn when a GRO box is too small for the MDP nonbonded cutoffs."""

    gro_path = Path(gro_file)
    mdp_path = Path(mdp_file)
    box_vectors = _read_gro_box_vectors(gro_path)
    shortest_box_vector = min(box_vectors[:3])
    cutoffs = _read_mdp_cutoffs(mdp_path)
    validation = GromacsBoxValidation(
        gro_path=gro_path,
        mdp_path=mdp_path,
        box_vectors_nm=box_vectors,
        shortest_box_vector_nm=shortest_box_vector,
        cutoffs_nm=cutoffs,
    )
    max_cutoff = validation.max_cutoff_nm
    if max_cutoff is not None and shortest_box_vector <= 2 * max_cutoff:
        warnings.warn(
            "GROMACS box may be too small for the nonbonded cutoff: "
            f"shortest box vector is {shortest_box_vector:.4f} nm, "
            f"max cutoff is {max_cutoff:.4f} nm, and GROMACS needs more than "
            f"{2 * max_cutoff:.4f} nm.",
            UserWarning,
            stacklevel=2,
        )
    return validation
```

</details>

<a id="definition-601"></a>

## `_write_local_minimization_script`

Source lines 601–618. Internal helper/protocol method.

```python
def _write_local_minimization_script(path: Path, *, coordinate_input: str='step5_input.gro') -> None: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| path | Path | required |
| coordinate_input (keyword-only) | str | 'step5_input.gro' |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `'\n'.join`, `path.chmod`, `path.stat`, `path.write_text`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Calls worth inspecting for I/O, state changes or delegated execution: `path.write_text`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _write_local_minimization_script(
    path: Path,
    *,
    coordinate_input: str = "step5_input.gro",
) -> None:
    path.write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "set -euo pipefail",
                "",
                f"gmx grompp -f step6.0_minimization.mdp -c {coordinate_input} -r {coordinate_input} -p topol.top -n index.ndx -o step6.0_minimization.tpr -maxwarn 1",
                "gmx mdrun -deffnm step6.0_minimization",
                "",
            ]
        )
    )
    path.chmod(path.stat().st_mode | stat.S_IXUSR)
```

</details>

<a id="definition-679"></a>

## `_write_hpc_equilibration_script`

Source lines 679–726. Internal helper/protocol method.

```python
def _write_hpc_equilibration_script(path: Path, *, job_name: str, workflow_type: str, reference_structure: str='step5_input.gro') -> None: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| path | Path | required |
| job_name (keyword-only) | str | required |
| workflow_type (keyword-only) | str | required |
| reference_structure (keyword-only) | str | 'step5_input.gro' |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `'\n'.join`, `_write_kcl_polymer_hpc_script`, `lines.extend`, `path.chmod`, `path.stat`, `path.write_text`.

Explicit return expressions; different branches may return different objects:

```python
None
```

Calls worth inspecting for I/O, state changes or delegated execution: `_write_kcl_polymer_hpc_script`, `path.write_text`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _write_hpc_equilibration_script(
    path: Path,
    *,
    job_name: str,
    workflow_type: str,
    reference_structure: str = "step5_input.gro",
) -> None:
    if workflow_type == "polymer":
        _write_kcl_polymer_hpc_script(path, job_name=job_name)
        return

    steps = GROMACS_WORKFLOW_HPC_STEPS[workflow_type]
    lines = [
        "#!/usr/bin/env bash",
        f"#SBATCH --job-name={job_name}_gmx",
        "#SBATCH --time=24:00:00",
        "#SBATCH --partition=standard",
        "#SBATCH --cpus-per-task=8",
        "#SBATCH --mem=16G",
        "#SBATCH --output=logs/%x-%j.out",
        "#SBATCH --error=logs/%x-%j.err",
        "",
        "set -euo pipefail",
        "mkdir -p logs",
        "",
        "# Adjust module/environment commands for your HPC system.",
        "# module load gromacs",
        "",
        f"# Workflow type: {workflow_type}",
        "# Common MD settings from the generated .mdp files:",
        "# - timestep: 0.002 ps (2 fs)",
        "# - constraints: h-bonds with LINCS",
        "# - periodic boundary conditions: xyz",
        "# - PME electrostatics",
        "# - nonbonded cutoffs: rlist/rcoulomb/rvdw = 1.0 nm",
        "",
    ]
    for step_name, coordinate_input, description in steps:
        lines.extend(
            [
                f"# {step_name}: {description}",
                f"gmx grompp -f {step_name}.mdp -c {coordinate_input} -r {reference_structure} -p topol.top -n index.ndx -o {step_name}.tpr",
                f"gmx mdrun -deffnm {step_name}",
                "",
            ]
        )
    path.write_text("\n".join(lines))
    path.chmod(path.stat().st_mode | stat.S_IXUSR)
```

</details>

<a id="definition-729"></a>

## `_write_kcl_polymer_hpc_script`

Source lines 729–768. Internal helper/protocol method.

```python
def _write_kcl_polymer_hpc_script(path: Path, *, job_name: str) -> None: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| path | Path | required |
| job_name (keyword-only) | str | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `'\n'.join`, `path.chmod`, `path.stat`, `path.write_text`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Calls worth inspecting for I/O, state changes or delegated execution: `path.write_text`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _write_kcl_polymer_hpc_script(path: Path, *, job_name: str) -> None:
    lines = [
        "#!/bin/bash -l",
        f"#SBATCH --job-name={job_name}_polymer_MD",
        "#SBATCH --partition=gpu",
        "#SBATCH --nodes=1",
        "#SBATCH --ntasks=1",
        "#SBATCH --cpus-per-task=8",
        "#SBATCH --gres=gpu:1",
        "#SBATCH --mem=16G",
        "#SBATCH --time=2-00:00",
        "#SBATCH --output=logs/%x-%j.out",
        "#SBATCH --error=logs/%x-%j.err",
        "",
        "module load gromacs/2021.5-gcc-11.4.0-cuda-11.8.0",
        "",
        "export OMP_NUM_THREADS=8",
        "",
        "mkdir -p logs",
        "",
        "# Step 6.1 — NVT",
        "",
        "gmx grompp -f step6.1_nvt.mdp -o step6.1_nvt.tpr -c step6.0_minimization.gro -r step5_input.gro -p topol.top -n index.ndx -maxwarn 1",
        "",
        "gmx mdrun -v -deffnm step6.1_nvt -pin on -nb gpu -pme gpu -bonded gpu -ntmpi 1 -ntomp 8",
        "",
        "# Step 6.2 — NPT",
        "",
        "gmx grompp -f step6.2_npt.mdp -o step6.2_npt.tpr -c step6.1_nvt.gro -r step5_input.gro -p topol.top -n index.ndx",
        "",
        "gmx mdrun -v -deffnm step6.2_npt -pin on -nb gpu -pme gpu -bonded gpu -ntmpi 1 -ntomp 8",
        "",
        "# Step 7 — Production",
        "",
        "gmx grompp -f step7_production.mdp -o step7_production.tpr -c step6.2_npt.gro -p topol.top -n index.ndx",
        "",
        "gmx mdrun -v -deffnm step7_production -pin on -nb gpu -pme gpu -bonded gpu -ntmpi 1 -ntomp 8",
    ]
    path.write_text("\n".join(lines) + "\n")
    path.chmod(path.stat().st_mode | stat.S_IXUSR)
```

</details>

<a id="definition-771"></a>

## `_infer_polymer_hpc_job_name`

Source lines 771–774. Internal helper/protocol method.

```python
def _infer_polymer_hpc_job_name(output_path: Path) -> str: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| output_path | Path | required |

### How to read this implementation

No direct function calls were found in this definition's own body.

Explicit return expressions; different branches may return different objects:

```python
output_path.parent.parent.name or 'gromacs'
output_path.parent.name or 'gromacs'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _infer_polymer_hpc_job_name(output_path: Path) -> str:
    if output_path.name == "solvated_polymer" and output_path.parent.name == "gromacs":
        return output_path.parent.parent.name or "gromacs"
    return output_path.parent.name or "gromacs"
```

</details>

<a id="definition-777"></a>

## `_write_solvate_script`

Source lines 777–1052. Internal helper/protocol method.

```python
def _write_solvate_script(path: Path, *, box_padding_nm: float, ion_concentration_molar: float) -> None: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| path | Path | required |
| box_padding_nm (keyword-only) | float | required |
| ion_concentration_molar (keyword-only) | float | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `path.chmod`, `path.stat`, `path.write_text`, `script.replace`, `script.replace('__BOX_PADDING__', f'{box_padding_nm:g}').replace`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Calls worth inspecting for I/O, state changes or delegated execution: `path.write_text`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _write_solvate_script(
    path: Path,
    *,
    box_padding_nm: float,
    ion_concentration_molar: float,
) -> None:
    script = """#!/usr/bin/env bash
set -euo pipefail
export GMX_MAXBACKUP=-1

fail_with_log() {
    local command_name="$1"
    local log_path="$2"
    echo "ERROR: ${command_name} failed. See ${log_path}." >&2
    if [[ -f "${log_path}" ]]; then
        echo "--- Last 50 lines of ${log_path} ---" >&2
        tail -n 50 "${log_path}" >&2 || true
        echo "--- End ${log_path} ---" >&2
    fi
    exit 1
}

run_logged() {
    local command_name="$1"
    local log_path="$2"
    shift 2
    printf '+ %q' "$@" > "${log_path}"
    printf '\\n' >> "${log_path}"
    if "$@" >> "${log_path}" 2>&1; then
        echo "${command_name} completed; log: ${log_path}"
    else
        fail_with_log "${command_name}" "${log_path}"
    fi
}

run_genion_logged() {
    local log_path="genion.log"
    local genion_args=(-s ions.tpr -o system_neutralized.gro -p topol.top -neutral -pname SOD -nname CLA)
    if awk -v concentration="${ION_CONCENTRATION_MOLAR}" 'BEGIN { exit !(concentration > 0) }'; then
        genion_args+=(-conc "${ION_CONCENTRATION_MOLAR}")
    fi
    printf '+ printf %q | gmx genion' "${SOLVENT_GROUP}" > "${log_path}"
    printf ' %q' "${genion_args[@]}" >> "${log_path}"
    printf '\\n' >> "${log_path}"
    if printf "%s\\n" "${SOLVENT_GROUP}" | gmx genion "${genion_args[@]}" >> "${log_path}" 2>&1; then
        echo "genion completed; log: ${log_path}"
    else
        echo "ERROR: genion failed while selecting solvent group '${SOLVENT_GROUP}'." >&2
        echo "If your solvent group is not SOL, rerun this script with --solvent-group <name>." >&2
        fail_with_log "genion" "${log_path}"
    fi
}

run_stdin_logged() {
    local command_name="$1"
    local log_path="$2"
    local stdin_text="$3"
    shift 3
    printf '+ printf %q |' "${stdin_text}" > "${log_path}"
    printf ' %q' "$@" >> "${log_path}"
    printf '\\n' >> "${log_path}"
    if printf "%b" "${stdin_text}" | "$@" >> "${log_path}" 2>&1; then
        echo "${command_name} completed; log: ${log_path}"
    else
        fail_with_log "${command_name}" "${log_path}"
    fi
}

clean_generated_files() {
    rm -f \
        step5_input_box.gro \
        step5_solvated.gro \
        step5_ions.gro \
        genion.tpr \
        mdout.mdp \
        editconf.log \
        minim_grompp_check.log \
        editconf_box.log \
        make_ndx_box.log \
        solvate.log \
        ions_grompp.log \
        genion.log \
        editconf_final.log \
        make_ndx_final.log \
        minim_grompp.log \
        \\#*\\# \
        \\#*.\\#
    for generated_path in step6.0_minimization.*; do
        [[ "${generated_path}" == "step6.0_minimization.mdp" ]] && continue
        rm -f "${generated_path}"
    done
}

reset_from_dry_polymer() {
    local dry_dir="../dry_polymer"
    if [[ -f "${dry_dir}/topol.top" && -f "${dry_dir}/step5_input.gro" ]]; then
        cp "${dry_dir}/topol.top" topol.top
        cp "${dry_dir}/step5_input.gro" step5_input.gro
        if [[ -f "${dry_dir}/index.ndx" ]]; then
            cp "${dry_dir}/index.ndx" index.ndx
        fi
        echo "Reset topol.top and step5_input.gro from ${dry_dir}."
    else
        echo "Using existing topol.top and step5_input.gro; ../dry_polymer was not found."
    fi
}

ensure_include() {
    local include_file="$1"
    if grep -Eq "^[[:space:]]*#include[[:space:]]+\\"${include_file}\\"" topol.top; then
        return
    fi
    if [[ ! -f "${include_file}" ]]; then
        echo "ERROR: topol.top does not include ${include_file}, and ${include_file} is missing." >&2
        exit 1
    fi

    local tmp_path="topol.top.tmp.$$"
    if awk -v include="#include \\"${include_file}\\"" '
        BEGIN { inserted = 0 }
        !inserted && tolower($0) ~ /^[[:space:]]*\\[ moleculetype \\]/ {
            print ""
            print include
            print ""
            inserted = 1
        }
        { print }
        END { if (!inserted) exit 42 }
    ' topol.top > "${tmp_path}"; then
        mv "${tmp_path}" topol.top
        echo "Added ${include_file} include to topol.top"
    else
        rm -f "${tmp_path}"
        echo "ERROR: Could not insert ${include_file}; no [ moleculetype ] section found in topol.top." >&2
        exit 1
    fi
}

topology_source_files() {
    printf '%s\\n' topol.top
    sed -n 's/^[[:space:]]*#include[[:space:]]*"\\([^"]*\\)".*/\\1/p' topol.top | while IFS= read -r include_path; do
        if [[ -f "${include_path}" ]]; then
            printf '%s\\n' "${include_path}"
        fi
    done
}

has_moleculetype() {
    local molecule_name="$1"
    awk -v target="${molecule_name}" '
        BEGIN { found = 0; in_moleculetype = 0 }
        tolower($0) ~ /^[[:space:]]*\\[ moleculetype \\]/ { in_moleculetype = 1; next }
        /^[[:space:]]*\\[/ { in_moleculetype = 0 }
        in_moleculetype {
            line = $0
            sub(/;.*/, "", line)
            gsub(/^[ \\t]+|[ \\t]+$/, "", line)
            split(line, fields, /[ \\t]+/)
            if (toupper(fields[1]) == target) found = 1
        }
        END { exit found ? 0 : 1 }
    ' $(topology_source_files)
}

has_atomtype() {
    local atom_type="$1"
    awk -v target="${atom_type}" '
        BEGIN { found = 0; in_atomtypes = 0 }
        tolower($0) ~ /^[[:space:]]*\\[ atomtypes \\]/ { in_atomtypes = 1; next }
        /^[[:space:]]*\\[/ { in_atomtypes = 0 }
        in_atomtypes {
            line = $0
            sub(/;.*/, "", line)
            gsub(/^[ \\t]+|[ \\t]+$/, "", line)
            split(line, fields, /[ \\t]+/)
            if (toupper(fields[1]) == target) found = 1
        }
        END { exit found ? 0 : 1 }
    ' $(topology_source_files)
}

validate_solvation_topology() {
    echo "Inspecting topol.top after gmx solvate for water and ion topology definitions."
    ensure_include "tip3_ions_atomtypes.itp"
    ensure_include "TIP3_SOL.itp"
    ensure_include "SOD.itp"
    ensure_include "CLA.itp"

    local missing=()
    for molecule_name in SOL SOD CLA; do
        if ! has_moleculetype "${molecule_name}"; then
            missing+=("[ moleculetype ] ${molecule_name}")
        fi
    done
    for atom_type in OT HT SOD CLA; do
        if ! has_atomtype "${atom_type}"; then
            missing+=("[ atomtypes ] ${atom_type}")
        fi
    done

    if (( ${#missing[@]} > 0 )); then
        echo "ERROR: topol.top is missing water/ion topology parameters required before ions.grompp:" >&2
        printf '  - %s\\n' "${missing[@]}" >&2
        echo "Expected the spc216.gro solvent route to use local includes: tip3_ions_atomtypes.itp, TIP3_SOL.itp, SOD.itp, CLA.itp." >&2
        exit 1
    fi
    echo "topol.top contains required SOL/SOD/CLA molecule definitions and OT/HT/SOD/CLA atom types."
}

validate_coordinate_topology_counts() {
    local coordinate_count
    coordinate_count="$(sed -n '2p' step5_input.gro | tr -d '[:space:]')"
    echo "Final step5_input.gro atom count: ${coordinate_count}"
    echo "Final topol.top [ molecules ] section:"
    awk '
        BEGIN { in_molecules = 0 }
        /^[[:space:]]*;/ { next }
        /^[[:space:]]*\\[/ {
            in_molecules = (tolower($0) ~ /^[[:space:]]*\\[ molecules \\]/)
            next
        }
        in_molecules && NF >= 2 { print "  " $1, $2 }
    ' topol.top
}

SOLVENT_GROUP="SOL"
ION_CONCENTRATION_MOLAR="__ION_CONCENTRATION__"
while (( $# > 0 )); do
    case "$1" in
        --solvent-group)
            shift
            if (( $# == 0 )); then
                echo "ERROR: --solvent-group requires a group name." >&2
                exit 2
            fi
            SOLVENT_GROUP="$1"
            ;;
        --solvent-group=*)
            SOLVENT_GROUP="${1#*=}"
            ;;
        --overwrite|--clean)
            ;;
        *)
            echo "ERROR: Unknown argument: $1" >&2
            echo "Usage: bash run_solvate_local.sh [--solvent-group SOL|--solvent-group=SOL] [--clean|--overwrite]" >&2
            exit 2
            ;;
    esac
    shift
done

# Build the real solvated GROMACS system.
# Polymer parameters are reset from dry_polymer before GROMACS solvate/genion can update local counts.
reset_from_dry_polymer
clean_generated_files
run_logged "editconf_box" "editconf_box.log" gmx editconf -f step5_input.gro -o step5_input_box.gro -c -d __BOX_PADDING__ -bt cubic
run_stdin_logged "make_ndx_box" "make_ndx_box.log" "q\\n" gmx make_ndx -f step5_input_box.gro -o index.ndx
run_logged "solvate" "solvate.log" gmx solvate -cp step5_input_box.gro -cs spc216.gro -p topol.top -o system_solvated.gro
validate_solvation_topology
run_logged "ions_grompp" "ions_grompp.log" gmx grompp -f ions.mdp -c system_solvated.gro -p topol.top -n index.ndx -o ions.tpr -maxwarn 1
run_genion_logged
run_logged "editconf_final" "editconf_final.log" gmx editconf -f system_neutralized.gro -o step5_input.gro
run_stdin_logged "make_ndx_final" "make_ndx_final.log" "q\\n" gmx make_ndx -f step5_input.gro -o index.ndx

# Validate that the solvated/ionised coordinates can enter minimisation.
validate_coordinate_topology_counts
run_logged "minim_grompp" "minim_grompp.log" gmx grompp -f step6.0_minimization.mdp -c step5_input.gro -r step5_input.gro -p topol.top -n index.ndx -o step6.0_minimization.tpr -maxwarn 1
rm -f \\#*\\# \\#*.\\#
"""
    path.write_text(
        script.replace("__BOX_PADDING__", f"{box_padding_nm:g}").replace(
            "__ION_CONCENTRATION__",
            f"{ion_concentration_molar:g}",
        )
    )
    path.chmod(path.stat().st_mode | stat.S_IXUSR)
```

</details>

<a id="definition-1055"></a>

## `_ensure_topology_include`

Source lines 1055–1074. Internal helper/protocol method.

```python
def _ensure_topology_include(topology_path: Path, include_filename: str) -> None: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| topology_path | Path | required |
| include_filename | str | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `'\n'.join`, `ValueError`, `any`, `enumerate`, `line.strip`, `line.strip().lower`, `lines.insert`, `topology_path.read_text`, `topology_path.read_text().splitlines`, `topology_path.write_text`.

Explicit return expressions; different branches may return different objects:

```python
None
```

Calls worth inspecting for I/O, state changes or delegated execution: `topology_path.read_text`, `topology_path.read_text().splitlines`, `topology_path.write_text`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError(f'Could not insert {include_line}; no [ moleculetype ] section found in {topology_path}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _ensure_topology_include(
    topology_path: Path,
    include_filename: str,
) -> None:
    include_line = f'#include "{include_filename}"'
    lines = topology_path.read_text().splitlines()
    if any(line.strip() == include_line for line in lines):
        return

    for index, line in enumerate(lines):
        if line.strip().lower() == "[ moleculetype ]":
            lines.insert(index, "")
            lines.insert(index + 1, include_line)
            lines.insert(index + 2, "")
            topology_path.write_text("\n".join(lines) + "\n")
            return

    raise ValueError(
        f"Could not insert {include_line}; no [ moleculetype ] section found in {topology_path}"
    )
```

</details>

<a id="definition-1077"></a>

## `_write_solvation_topology_templates`

Source lines 1077–1084. Internal helper/protocol method.

```python
def _write_solvation_topology_templates(output_dir: Path, topology_path: Path) -> tuple[Path, ...]: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| output_dir | Path | required |
| topology_path | Path | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `_copy_solvation_templates`, `_ensure_topology_include`.

Explicit return expressions; different branches may return different objects:

```python
template_paths
```

Calls worth inspecting for I/O, state changes or delegated execution: `_copy_solvation_templates`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _write_solvation_topology_templates(
    output_dir: Path,
    topology_path: Path,
) -> tuple[Path, ...]:
    template_paths = _copy_solvation_templates(output_dir)
    for include_name in GROMACS_SOLVATION_TOPOLOGY_INCLUDE_NAMES:
        _ensure_topology_include(topology_path, include_name)
    return template_paths
```

</details>

<a id="definition-1087"></a>

## `_read_topology_molecule_counts`

Source lines 1087–1108. Internal helper/protocol method.

```python
def _read_topology_molecule_counts(topology_path: Path) -> dict[str, int]: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| topology_path | Path | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `int`, `len`, `line.endswith`, `line.split`, `line.startswith`, `line.strip`, `line.strip('[]').strip`, `line.strip('[]').strip().lower`, `molecule_counts.get`, `raw_line.split`, `raw_line.split(';', 1)[0].strip`, `topology_path.read_text`, `topology_path.read_text().splitlines`.

Explicit return expressions; different branches may return different objects:

```python
molecule_counts
```

Calls worth inspecting for I/O, state changes or delegated execution: `topology_path.read_text`, `topology_path.read_text().splitlines`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _read_topology_molecule_counts(topology_path: Path) -> dict[str, int]:
    molecule_counts: dict[str, int] = {}
    in_molecules_section = False
    for raw_line in topology_path.read_text().splitlines():
        line = raw_line.split(";", 1)[0].strip()
        if not line:
            continue
        if line.startswith("[") and line.endswith("]"):
            in_molecules_section = line.strip("[]").strip().lower() == "molecules"
            continue
        if not in_molecules_section:
            continue
        fields = line.split()
        if len(fields) < 2:
            continue
        try:
            molecule_counts[fields[0]] = molecule_counts.get(fields[0], 0) + int(
                fields[1]
            )
        except ValueError:
            continue
    return molecule_counts
```

</details>

<a id="definition-1111"></a>

## `_topology_source_paths`

Source lines 1111–1122. Internal helper/protocol method.

```python
def _topology_source_paths(topology_path: Path) -> tuple[Path, ...]: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| topology_path | Path | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `INCLUDE_PATTERN.match`, `Path`, `include_path.exists`, `include_path.is_absolute`, `match.group`, `paths.append`, `topology_path.read_text`, `topology_path.read_text().splitlines`, `tuple`.

Explicit return expressions; different branches may return different objects:

```python
tuple(paths)
```

Calls worth inspecting for I/O, state changes or delegated execution: `topology_path.read_text`, `topology_path.read_text().splitlines`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _topology_source_paths(topology_path: Path) -> tuple[Path, ...]:
    paths = [topology_path]
    for line in topology_path.read_text().splitlines():
        match = INCLUDE_PATTERN.match(line)
        if match is None:
            continue
        include_path = Path(match.group(1))
        if not include_path.is_absolute():
            include_path = topology_path.parent / include_path
        if include_path.exists():
            paths.append(include_path)
    return tuple(paths)
```

</details>

<a id="definition-1125"></a>

## `_read_moleculetype_atom_counts`

Source lines 1125–1152. Internal helper/protocol method.

```python
def _read_moleculetype_atom_counts(topology_path: Path) -> dict[str, int]: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| topology_path | Path | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `_topology_source_paths`, `atom_counts.get`, `atom_counts.setdefault`, `int`, `line.endswith`, `line.split`, `line.startswith`, `line.strip`, `line.strip('[]').strip`, `line.strip('[]').strip().lower`, `raw_line.split`, `raw_line.split(';', 1)[0].strip`, `source_path.read_text`, `source_path.read_text().splitlines`.

Explicit return expressions; different branches may return different objects:

```python
atom_counts
```

Calls worth inspecting for I/O, state changes or delegated execution: `source_path.read_text`, `source_path.read_text().splitlines`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _read_moleculetype_atom_counts(topology_path: Path) -> dict[str, int]:
    atom_counts: dict[str, int] = {}
    for source_path in _topology_source_paths(topology_path):
        current_molecule: str | None = None
        in_moleculetype = False
        in_atoms = False
        for raw_line in source_path.read_text().splitlines():
            line = raw_line.split(";", 1)[0].strip()
            if not line:
                continue
            if line.startswith("[") and line.endswith("]"):
                section_name = line.strip("[]").strip().lower()
                in_moleculetype = section_name == "moleculetype"
                in_atoms = section_name == "atoms"
                continue
            fields = line.split()
            if in_moleculetype and fields:
                current_molecule = fields[0]
                atom_counts.setdefault(current_molecule, 0)
                in_moleculetype = False
                continue
            if in_atoms and current_molecule is not None and fields:
                try:
                    int(fields[0])
                except ValueError:
                    continue
                atom_counts[current_molecule] = atom_counts.get(current_molecule, 0) + 1
    return atom_counts
```

</details>

<a id="definition-1155"></a>

## `count_gro_atoms`

Source lines 1155–1165. Named callable; inspect its callers before treating it as a stable public API.

```python
def count_gro_atoms(gro_path: str | Path) -> int: ...
```

### Purpose and original contract

Read the atom count from the second line of a GROMACS ``.gro`` file.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| gro_path | str \| Path | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `Path`, `ValueError`, `int`, `len`, `lines[1].strip`, `path.read_text`, `path.read_text().splitlines`.

Explicit return expressions; different branches may return different objects:

```python
int(lines[1].strip())
```

Calls worth inspecting for I/O, state changes or delegated execution: `path.read_text`, `path.read_text().splitlines`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError(f'GRO file is too short to contain an atom count: {path}')
ValueError(f'Could not parse GRO atom count from {path}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def count_gro_atoms(gro_path: str | Path) -> int:
    """Read the atom count from the second line of a GROMACS ``.gro`` file."""

    path = Path(gro_path)
    lines = path.read_text().splitlines()
    if len(lines) < 2:
        raise ValueError(f"GRO file is too short to contain an atom count: {path}")
    try:
        return int(lines[1].strip())
    except ValueError as exc:
        raise ValueError(f"Could not parse GRO atom count from {path}") from exc
```

</details>

<a id="definition-1168"></a>

## `validate_gromacs_coordinate_topology_counts`

Source lines 1168–1202. Named callable; inspect its callers before treating it as a stable public API.

```python
def validate_gromacs_coordinate_topology_counts(output_dir: str | Path, *, coordinate_name: str='step5_input.gro', topology_name: str='topol.top') -> GromacsCoordinateTopologyValidation: ...
```

### Purpose and original contract

Compare final coordinate atoms with topology molecule atom counts.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| output_dir | str \| Path | required |
| coordinate_name (keyword-only) | str | 'step5_input.gro' |
| topology_name (keyword-only) | str | 'topol.top' |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `FileNotFoundError`, `GromacsCoordinateTopologyValidation`, `Path`, `_read_moleculetype_atom_counts`, `_read_topology_molecule_counts`, `count_gro_atoms`, `gro_path.exists`, `molecule_atom_counts.get`, `molecule_counts.items`, `topology_path.exists`.

Explicit return expressions; different branches may return different objects:

```python
GromacsCoordinateTopologyValidation(gro_path=gro_path, topol_top_path=topology_path, coordinate_atom_count=coordinate_atom_count, molecule_counts=molecule_counts, molecule_atom_counts=molecule_atom_counts, expected_atom_count=expected_atom_count)
```

Calls worth inspecting for I/O, state changes or delegated execution: `_read_moleculetype_atom_counts`, `_read_topology_molecule_counts`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
FileNotFoundError(f'GROMACS coordinate file not found: {gro_path}')
FileNotFoundError(f'GROMACS topology not found: {topology_path}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def validate_gromacs_coordinate_topology_counts(
    output_dir: str | Path,
    *,
    coordinate_name: str = "step5_input.gro",
    topology_name: str = "topol.top",
) -> GromacsCoordinateTopologyValidation:
    """Compare final coordinate atoms with topology molecule atom counts."""

    output_path = Path(output_dir)
    gro_path = output_path / coordinate_name
    topology_path = output_path / topology_name
    if not gro_path.exists():
        raise FileNotFoundError(f"GROMACS coordinate file not found: {gro_path}")
    if not topology_path.exists():
        raise FileNotFoundError(f"GROMACS topology not found: {topology_path}")

    coordinate_atom_count = count_gro_atoms(gro_path)
    molecule_counts = _read_topology_molecule_counts(topology_path)
    molecule_atom_counts = _read_moleculetype_atom_counts(topology_path)
    expected_atom_count: int | None = 0
    for molecule_name, molecule_count in molecule_counts.items():
        atom_count = molecule_atom_counts.get(molecule_name)
        if atom_count is None:
            expected_atom_count = None
            break
        expected_atom_count += molecule_count * atom_count

    return GromacsCoordinateTopologyValidation(
        gro_path=gro_path,
        topol_top_path=topology_path,
        coordinate_atom_count=coordinate_atom_count,
        molecule_counts=molecule_counts,
        molecule_atom_counts=molecule_atom_counts,
        expected_atom_count=expected_atom_count,
    )
```

</details>

<a id="definition-1205"></a>

## `_sum_named_molecule_counts`

Source lines 1205–1212. Internal helper/protocol method.

```python
def _sum_named_molecule_counts(molecule_counts: dict[str, int], names: tuple[str, ...]) -> int: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| molecule_counts | dict[str, int] | required |
| names | tuple[str, ...] | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `molecule_counts.items`, `name.upper`, `sum`.

Explicit return expressions; different branches may return different objects:

```python
sum((count for name, count in molecule_counts.items() if name.upper() in normalised_names))
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _sum_named_molecule_counts(
    molecule_counts: dict[str, int],
    names: tuple[str, ...],
) -> int:
    normalised_names = {name.upper() for name in names}
    return sum(
        count for name, count in molecule_counts.items() if name.upper() in normalised_names
    )
```

</details>

<a id="definition-1215"></a>

## `_resolve_solvated_polymer_dir`

Source lines 1215–1222. Internal helper/protocol method.

```python
def _resolve_solvated_polymer_dir(output_dir: str | Path) -> Path: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| output_dir | str \| Path | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `Path`, `dry_dir.exists`.

Explicit return expressions; different branches may return different objects:

```python
output_path
output_path / 'solvated_polymer'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _resolve_solvated_polymer_dir(output_dir: str | Path) -> Path:
    output_path = Path(output_dir)
    if output_path.name == "solvated_polymer":
        return output_path
    dry_dir = output_path / "dry_polymer"
    if dry_dir.exists() or output_path.name == "gromacs":
        return output_path / "solvated_polymer"
    return output_path
```

</details>

<a id="definition-1225"></a>

## `_populate_solvated_polymer_inputs`

Source lines 1225–1236. Internal helper/protocol method.

```python
def _populate_solvated_polymer_inputs(output_path: Path) -> None: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| output_path | Path | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `_copy_workflow_inputs`, `destination.exists`, `dry_dir.exists`, `shutil.copy2`, `source.exists`.

Explicit return expressions; different branches may return different objects:

```python
None
```

Calls worth inspecting for I/O, state changes or delegated execution: `_copy_workflow_inputs`, `shutil.copy2`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _populate_solvated_polymer_inputs(output_path: Path) -> None:
    if output_path.name != "solvated_polymer":
        return
    dry_dir = output_path.parent / "dry_polymer"
    if not dry_dir.exists():
        return
    _copy_workflow_inputs(dry_dir, output_path, overwrite=True)
    for template_name in GROMACS_POLYMER_MDP_TEMPLATE_NAMES:
        source = dry_dir / template_name
        destination = output_path / template_name
        if source.exists() and not destination.exists():
            shutil.copy2(source, destination)
```

</details>

<a id="definition-1239"></a>

## `_clean_solvated_polymer_generated_files`

Source lines 1239–1267. Internal helper/protocol method.

```python
def _clean_solvated_polymer_generated_files(output_path: Path) -> None: ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| output_path | Path | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `(output_path / filename).unlink`, `output_path.glob`, `path.is_file`, `path.unlink`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Calls worth inspecting for I/O, state changes or delegated execution: `(output_path / filename).unlink`, `path.unlink`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _clean_solvated_polymer_generated_files(output_path: Path) -> None:
    for filename in (
        "step5_input_box.gro",
        "step5_solvated.gro",
        "step5_ions.gro",
        "genion.tpr",
        "mdout.mdp",
        "editconf.log",
        "minim_grompp_check.log",
        "editconf_box.log",
        "make_ndx_box.log",
        "solvate.log",
        "ions_grompp.log",
        "genion.log",
        "editconf_final.log",
        "make_ndx_final.log",
        "minim_grompp.log",
    ):
        (output_path / filename).unlink(missing_ok=True)
    for pattern in (
        "step6.0_minimization.*",
        "#*#",
        "#*.#",
    ):
        for path in output_path.glob(pattern):
            if path.name == "step6.0_minimization.mdp":
                continue
            if path.is_file():
                path.unlink()
```

</details>

<a id="definition-1270"></a>

## `write_gromacs_solvation_files`

Source lines 1270–1333. Named callable; inspect its callers before treating it as a stable public API.

```python
def write_gromacs_solvation_files(output_dir: str | Path, *, workflow_type: str='polymer', box_padding_nm: float=1.2, ion_concentration_molar: float=0.15, clean: bool=False, overwrite: bool=False) -> GromacsSolvationFiles: ...
```

### Purpose and original contract

Write files for the standard GROMACS solvate/genion workflow.

This keeps the polymer GAFF2 topology unchanged and only adds the simulation
environment: box, TIP3P-compatible water from GROMACS, and neutralising NaCl ions.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| output_dir | str \| Path | required |
| workflow_type (keyword-only) | str | 'polymer' |
| box_padding_nm (keyword-only) | float | 1.2 |
| ion_concentration_molar (keyword-only) | float | 0.15 |
| clean (keyword-only) | bool | False |
| overwrite (keyword-only) | bool | False |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `', '.join`, `FileNotFoundError`, `GromacsSolvationFiles`, `ValueError`, `_clean_solvated_polymer_generated_files`, `_infer_polymer_hpc_job_name`, `_populate_solvated_polymer_inputs`, `_resolve_solvated_polymer_dir`, `_write_hpc_equilibration_script`, `_write_local_minimization_script`, `_write_solvate_script`, `_write_solvation_topology_templates`, `output_path.mkdir`, `sorted`, `topology_path.exists`.

Explicit return expressions; different branches may return different objects:

```python
GromacsSolvationFiles(output_dir=output_path, ions_mdp_path=ions_mdp_path, solvation_itp_paths=solvation_itp_paths, solvent_itp_path=output_path / 'TIP3_SOL.itp', cation_itp_path=output_path / 'SOD.itp', anion_itp_path=output_path / 'CLA.itp', solvate_script_path=solvate_script_path, local_script_path=local_script_path, hpc_script_path=hpc_script_path, charmm_gui_membrane_hpc_script_path=output_pa … [full expression below]
```

Calls worth inspecting for I/O, state changes or delegated execution: `_write_hpc_equilibration_script`, `_write_local_minimization_script`, `_write_solvate_script`, `_write_solvation_topology_templates`, `output_path.mkdir`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError(f'workflow_type must be one of: {valid}')
FileNotFoundError(f'GROMACS topology not found: {topology_path}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def write_gromacs_solvation_files(
    output_dir: str | Path,
    *,
    workflow_type: str = "polymer",
    box_padding_nm: float = 1.2,
    ion_concentration_molar: float = 0.15,
    clean: bool = False,
    overwrite: bool = False,
) -> GromacsSolvationFiles:
    """Write files for the standard GROMACS solvate/genion workflow.

    This keeps the polymer GAFF2 topology unchanged and only adds the simulation
    environment: box, TIP3P-compatible water from GROMACS, and neutralising NaCl ions.
    """

    if workflow_type not in GROMACS_WORKFLOW_MDP_TEMPLATE_NAMES:
        valid = ", ".join(sorted(GROMACS_WORKFLOW_MDP_TEMPLATE_NAMES))
        raise ValueError(f"workflow_type must be one of: {valid}")

    output_path = _resolve_solvated_polymer_dir(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    if clean or overwrite:
        _clean_solvated_polymer_generated_files(output_path)
    _populate_solvated_polymer_inputs(output_path)

    topology_path = output_path / "topol.top"
    if not topology_path.exists():
        raise FileNotFoundError(f"GROMACS topology not found: {topology_path}")

    solvation_itp_paths = _write_solvation_topology_templates(
        output_path,
        topology_path,
    )
    ions_mdp_path = output_path / "ions.mdp"
    solvate_script_path = output_path / "run_solvate_local.sh"
    local_script_path = output_path / "run_step6_local.sh"
    hpc_script_path = output_path / "run_hpc_equilibration_production.slurm"

    _write_solvate_script(
        solvate_script_path,
        box_padding_nm=box_padding_nm,
        ion_concentration_molar=ion_concentration_molar,
    )
    _write_local_minimization_script(local_script_path)
    _write_hpc_equilibration_script(
        hpc_script_path,
        job_name=_infer_polymer_hpc_job_name(output_path),
        workflow_type=workflow_type,
    )

    return GromacsSolvationFiles(
        output_dir=output_path,
        ions_mdp_path=ions_mdp_path,
        solvation_itp_paths=solvation_itp_paths,
        solvent_itp_path=output_path / "TIP3_SOL.itp",
        cation_itp_path=output_path / "SOD.itp",
        anion_itp_path=output_path / "CLA.itp",
        solvate_script_path=solvate_script_path,
        local_script_path=local_script_path,
        hpc_script_path=hpc_script_path,
        charmm_gui_membrane_hpc_script_path=output_path.parent
        / "charmm_gui_membrane"
        / "run_hpc_charmm_gui_membrane.slurm",
    )
```

</details>

<a id="definition-1336"></a>

## `validate_gromacs_solvated_topology`

Source lines 1336–1356. Named callable; inspect its callers before treating it as a stable public API.

```python
def validate_gromacs_solvated_topology(output_dir: str | Path, *, topology_name: str='topol.top') -> GromacsSolvatedTopologyValidation: ...
```

### Purpose and original contract

Validate that topology molecule counts include solvent and ions.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| output_dir | str \| Path | required |
| topology_name (keyword-only) | str | 'topol.top' |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `FileNotFoundError`, `GromacsSolvatedTopologyValidation`, `Path`, `_read_topology_molecule_counts`, `_sum_named_molecule_counts`, `topol_top_path.exists`.

Explicit return expressions; different branches may return different objects:

```python
GromacsSolvatedTopologyValidation(topol_top_path=topol_top_path, molecule_counts=molecule_counts, water_count=_sum_named_molecule_counts(molecule_counts, WATER_MOLECULE_NAMES), cation_count=_sum_named_molecule_counts(molecule_counts, CATION_MOLECULE_NAMES), anion_count=_sum_named_molecule_counts(molecule_counts, ANION_MOLECULE_NAMES))
```

Calls worth inspecting for I/O, state changes or delegated execution: `_read_topology_molecule_counts`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
FileNotFoundError(f'GROMACS topology not found: {topol_top_path}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def validate_gromacs_solvated_topology(
    output_dir: str | Path,
    *,
    topology_name: str = "topol.top",
) -> GromacsSolvatedTopologyValidation:
    """Validate that topology molecule counts include solvent and ions."""

    topol_top_path = Path(output_dir) / topology_name
    if not topol_top_path.exists():
        raise FileNotFoundError(f"GROMACS topology not found: {topol_top_path}")
    molecule_counts = _read_topology_molecule_counts(topol_top_path)
    return GromacsSolvatedTopologyValidation(
        topol_top_path=topol_top_path,
        molecule_counts=molecule_counts,
        water_count=_sum_named_molecule_counts(molecule_counts, WATER_MOLECULE_NAMES),
        cation_count=_sum_named_molecule_counts(molecule_counts, CATION_MOLECULE_NAMES),
        anion_count=_sum_named_molecule_counts(
            molecule_counts,
            ANION_MOLECULE_NAMES,
        ),
    )
```

</details>

<a id="definition-1359"></a>

## `validate_gromacs_solvation_grompp`

Source lines 1359–1419. Named callable; inspect its callers before treating it as a stable public API.

```python
def validate_gromacs_solvation_grompp(output_dir: str | Path, *, gmx_command: str='gmx', runner=subprocess.run) -> tuple[GromacsGromppValidation, GromacsGromppValidation]: ...
```

### Purpose and original contract

Run the two ``grompp`` checks required by the solvation workflow.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| output_dir | str \| Path | required |
| gmx_command (keyword-only) | str | 'gmx' |
| runner (keyword-only) | not annotated | subprocess.run |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `GromacsGromppValidation`, `Path`, `list`, `runner`, `tuple`, `validations.append`.

Explicit return expressions; different branches may return different objects:

```python
tuple(validations)
```

Calls worth inspecting for I/O, state changes or delegated execution: `runner`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def validate_gromacs_solvation_grompp(
    output_dir: str | Path,
    *,
    gmx_command: str = "gmx",
    runner=subprocess.run,
) -> tuple[GromacsGromppValidation, GromacsGromppValidation]:
    """Run the two ``grompp`` checks required by the solvation workflow."""

    output_path = Path(output_dir)
    commands = (
        (
            gmx_command,
            "grompp",
            "-f",
            "ions.mdp",
            "-c",
            "system_solvated.gro",
            "-p",
            "topol.top",
            "-n",
            "index.ndx",
            "-o",
            "ions.tpr",
            "-maxwarn",
            "1",
        ),
        (
            gmx_command,
            "grompp",
            "-f",
            "step6.0_minimization.mdp",
            "-c",
            "step5_input.gro",
            "-r",
            "step5_input.gro",
            "-p",
            "topol.top",
            "-n",
            "index.ndx",
            "-o",
            "step6.0_minimization.tpr",
        ),
    )
    validations: list[GromacsGromppValidation] = []
    for command in commands:
        result = runner(
            list(command),
            cwd=output_path,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        validations.append(
            GromacsGromppValidation(
                command=command,
                returncode=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
            )
        )
    return tuple(validations)  # type: ignore[return-value]
```

</details>

<a id="definition-1422"></a>

## `validate_gromacs_run_folder`

Source lines 1422–1455. Named callable; inspect its callers before treating it as a stable public API.

```python
def validate_gromacs_run_folder(output_dir: str | Path, *, topology_name: str='topol.top') -> GromacsTopologyValidation: ...
```

### Purpose and original contract

Validate external include files referenced by a GROMACS topology.

ParmEd GAFF2 conversion often writes a standalone topology with all molecule
definitions in ``topol.top``. In that case there are no ``#include`` lines
and no ``toppar`` directory is required.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| output_dir | str \| Path | required |
| topology_name (keyword-only) | str | 'topol.top' |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `FileNotFoundError`, `GromacsTopologyValidation`, `INCLUDE_PATTERN.match`, `Path`, `include_path.is_absolute`, `included_files.append`, `match.group`, `path.exists`, `topol_top_path.exists`, `topol_top_path.read_text`, `topol_top_path.read_text().splitlines`, `tuple`.

Explicit return expressions; different branches may return different objects:

```python
GromacsTopologyValidation(topol_top_path=topol_top_path, is_standalone=not included_files, included_files=tuple(included_files), missing_files=missing_files)
```

Calls worth inspecting for I/O, state changes or delegated execution: `topol_top_path.read_text`, `topol_top_path.read_text().splitlines`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
FileNotFoundError(f'GROMACS topology not found: {topol_top_path}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def validate_gromacs_run_folder(
    output_dir: str | Path,
    *,
    topology_name: str = "topol.top",
) -> GromacsTopologyValidation:
    """Validate external include files referenced by a GROMACS topology.

    ParmEd GAFF2 conversion often writes a standalone topology with all molecule
    definitions in ``topol.top``. In that case there are no ``#include`` lines
    and no ``toppar`` directory is required.
    """

    output_path = Path(output_dir)
    topol_top_path = output_path / topology_name
    if not topol_top_path.exists():
        raise FileNotFoundError(f"GROMACS topology not found: {topol_top_path}")

    included_files: list[Path] = []
    for line in topol_top_path.read_text().splitlines():
        match = INCLUDE_PATTERN.match(line)
        if match is None:
            continue
        include_path = Path(match.group(1))
        if not include_path.is_absolute():
            include_path = output_path / include_path
        included_files.append(include_path)

    missing_files = tuple(path for path in included_files if not path.exists())
    return GromacsTopologyValidation(
        topol_top_path=topol_top_path,
        is_standalone=not included_files,
        included_files=tuple(included_files),
        missing_files=missing_files,
    )
```

</details>

<a id="definition-1458"></a>

## `check_gromacs_minimization_inputs`

Source lines 1458–1473. Named callable; inspect its callers before treating it as a stable public API.

```python
def check_gromacs_minimization_inputs(output_dir: str | Path) -> GromacsLocalMinimizationCheck: ...
```

### Purpose and original contract

Check the files needed before running local GROMACS minimisation.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| output_dir | str \| Path | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `GromacsLocalMinimizationCheck`, `Path`, `Path(output_dir).expanduser`, `Path(output_dir).expanduser().resolve`, `path.exists`, `tuple`.

Explicit return expressions; different branches may return different objects:

```python
GromacsLocalMinimizationCheck(output_dir=output_path, required_files=required_files, missing_files=missing_files, command=('bash', 'run_step6_local.sh'))
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def check_gromacs_minimization_inputs(
    output_dir: str | Path,
) -> GromacsLocalMinimizationCheck:
    """Check the files needed before running local GROMACS minimisation."""

    output_path = Path(output_dir).expanduser().resolve()
    required_files = tuple(
        output_path / filename for filename in LOCAL_MINIMIZATION_REQUIRED_FILENAMES
    )
    missing_files = tuple(path for path in required_files if not path.exists())
    return GromacsLocalMinimizationCheck(
        output_dir=output_path,
        required_files=required_files,
        missing_files=missing_files,
        command=("bash", "run_step6_local.sh"),
    )
```

</details>

<a id="definition-1476"></a>

## `run_gromacs_local_minimization`

Source lines 1476–1502. Named callable; inspect its callers before treating it as a stable public API.

```python
def run_gromacs_local_minimization(output_dir: str | Path, *, runner=subprocess.run) -> subprocess.CompletedProcess: ...
```

### Purpose and original contract

Run the local minimisation script from inside the GROMACS folder.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| output_dir | str \| Path | required |
| runner (keyword-only) | not annotated | subprocess.run |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `', '.join`, `FileNotFoundError`, `RuntimeError`, `check_gromacs_minimization_inputs`, `list`, `runner`, `str`.

Explicit return expressions; different branches may return different objects:

```python
result
```

Calls worth inspecting for I/O, state changes or delegated execution: `runner`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
FileNotFoundError(f'Cannot run GROMACS minimisation; missing files: {missing}')
RuntimeError(f'GROMACS local minimisation failed with return code {result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def run_gromacs_local_minimization(
    output_dir: str | Path,
    *,
    runner=subprocess.run,
) -> subprocess.CompletedProcess:
    """Run the local minimisation script from inside the GROMACS folder."""

    check = check_gromacs_minimization_inputs(output_dir)
    if not check.ready:
        missing = ", ".join(str(path) for path in check.missing_files)
        raise FileNotFoundError(
            f"Cannot run GROMACS minimisation; missing files: {missing}"
        )

    result = runner(
        list(check.command),
        cwd=check.output_dir,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise RuntimeError(
            "GROMACS local minimisation failed with return code "
            f"{result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return result
```

</details>

<a id="definition-1505"></a>

## `prepare_gromacs_run_folder`

Source lines 1505–1630. Named callable; inspect its callers before treating it as a stable public API.

```python
def prepare_gromacs_run_folder(prmtop_file: str | Path, inpcrd_file: str | Path, output_dir: str | Path, system_name: str, *, workflow_type: str='polymer', index_file: str | Path | None=None, gmx_command: str='gmx', runner=subprocess.run) -> GromacsPreparedRunFolder: ...
```

### Purpose and original contract

Prepare self-contained GROMACS workflow folders from AMBER files.

``output_dir`` is the system-level ``gromacs`` directory. This function
writes independent ``dry_polymer``, ``solvated_polymer`` and
``charmm_gui_membrane`` subdirectories so one workflow cannot overwrite
another workflow's inputs or outputs.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| prmtop_file | str \| Path | required |
| inpcrd_file | str \| Path | required |
| output_dir | str \| Path | required |
| system_name | str | required |
| workflow_type (keyword-only) | str | 'polymer' |
| index_file (keyword-only) | str \| Path \| None | None |
| gmx_command (keyword-only) | str | 'gmx' |
| runner (keyword-only) | not annotated | subprocess.run |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `', '.join`, `FileNotFoundError`, `GromacsPreparedRunFolder`, `Path`, `Path(index_file).exists`, `ValueError`, `_copy_mdp_templates`, `_copy_workflow_inputs`, `_write_default_index`, `_write_hpc_equilibration_script`, `_write_local_minimization_script`, `charmm_gui_membrane_dir.mkdir`, `convert_amber_to_gromacs`, `converted.gro_path.replace`, `converted.top_path.replace`, `create_gromacs_simulation_box`, `dry_polymer_dir.mkdir`, `raw_step5_input_gro_path.unlink`, `shutil.copy2`, `solvated_polymer_dir.mkdir`, `sorted`, `str`, `system_name.strip`, `validate_gromacs_box_against_mdp`, `validate_gromacs_run_folder`.

Explicit return expressions; different branches may return different objects:

```python
GromacsPreparedRunFolder(output_dir=output_path, workflow_type=workflow_type, dry_polymer_dir=dry_polymer_dir, solvated_polymer_dir=solvated_polymer_dir, charmm_gui_membrane_dir=charmm_gui_membrane_dir, step5_input_gro_path=step5_input_gro_path, topol_top_path=topol_top_path, index_ndx_path=index_ndx_path, mdp_paths=dry_mdp_paths + solvated_mdp_paths + charmm_mdp_paths, local_script_path=local_scr … [full expression below]
```

Calls worth inspecting for I/O, state changes or delegated execution: `_copy_mdp_templates`, `_copy_workflow_inputs`, `_write_default_index`, `_write_hpc_equilibration_script`, `_write_local_minimization_script`, `charmm_gui_membrane_dir.mkdir`, `dry_polymer_dir.mkdir`, `raw_step5_input_gro_path.unlink`, `shutil.copy2`, `solvated_polymer_dir.mkdir`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('system_name must be a non-empty string')
ValueError(f'workflow_type must be one of: {valid}')
FileNotFoundError(f'GROMACS topology includes missing files: {missing}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def prepare_gromacs_run_folder(
    prmtop_file: str | Path,
    inpcrd_file: str | Path,
    output_dir: str | Path,
    system_name: str,
    *,
    workflow_type: str = "polymer",
    index_file: str | Path | None = None,
    gmx_command: str = "gmx",
    runner=subprocess.run,
) -> GromacsPreparedRunFolder:
    """Prepare self-contained GROMACS workflow folders from AMBER files.

    ``output_dir`` is the system-level ``gromacs`` directory. This function
    writes independent ``dry_polymer``, ``solvated_polymer`` and
    ``charmm_gui_membrane`` subdirectories so one workflow cannot overwrite
    another workflow's inputs or outputs.
    """

    if not system_name.strip():
        raise ValueError("system_name must be a non-empty string")
    if workflow_type not in GROMACS_WORKFLOW_MDP_TEMPLATE_NAMES:
        valid = ", ".join(sorted(GROMACS_WORKFLOW_MDP_TEMPLATE_NAMES))
        raise ValueError(f"workflow_type must be one of: {valid}")

    output_path = Path(output_dir)
    dry_polymer_dir = output_path / "dry_polymer"
    solvated_polymer_dir = output_path / "solvated_polymer"
    charmm_gui_membrane_dir = output_path / "charmm_gui_membrane"
    dry_polymer_dir.mkdir(parents=True, exist_ok=True)
    solvated_polymer_dir.mkdir(parents=True, exist_ok=True)
    charmm_gui_membrane_dir.mkdir(parents=True, exist_ok=True)

    converted = convert_amber_to_gromacs(
        str(prmtop_file),
        str(inpcrd_file),
        str(dry_polymer_dir),
        system_name,
    )
    topol_top_path = dry_polymer_dir / "topol.top"
    raw_step5_input_gro_path = dry_polymer_dir / "step5_input_raw.gro"
    step5_input_gro_path = dry_polymer_dir / "step5_input.gro"
    converted.top_path.replace(topol_top_path)
    converted.gro_path.replace(raw_step5_input_gro_path)
    create_gromacs_simulation_box(
        raw_step5_input_gro_path,
        step5_input_gro_path,
        padding_nm=3.0,
        box_type="cubic",
        gmx_command=gmx_command,
        runner=runner,
    )
    raw_step5_input_gro_path.unlink(missing_ok=True)

    index_ndx_path = dry_polymer_dir / "index.ndx"
    if index_file is not None and Path(index_file).exists():
        shutil.copy2(index_file, index_ndx_path)
    else:
        _write_default_index(step5_input_gro_path, index_ndx_path)

    dry_mdp_paths = _copy_mdp_templates(
        dry_polymer_dir,
        ("step6.0_minimization.mdp",),
    )
    validate_gromacs_box_against_mdp(
        step5_input_gro_path,
        dry_polymer_dir / "step6.0_minimization.mdp",
    )
    validation = validate_gromacs_run_folder(dry_polymer_dir)
    if not validation.valid:
        missing = ", ".join(str(path) for path in validation.missing_files)
        raise FileNotFoundError(
            f"GROMACS topology includes missing files: {missing}"
        )

    local_script_path = dry_polymer_dir / "run_step6_local.sh"
    _write_local_minimization_script(local_script_path)

    _copy_workflow_inputs(dry_polymer_dir, solvated_polymer_dir)
    solvated_mdp_paths = _copy_mdp_templates(
        solvated_polymer_dir,
        GROMACS_POLYMER_MDP_TEMPLATE_NAMES,
    )
    solvated_local_script_path = solvated_polymer_dir / "run_step6_local.sh"
    hpc_script_path = solvated_polymer_dir / "run_hpc_equilibration_production.slurm"
    _write_local_minimization_script(solvated_local_script_path)
    _write_hpc_equilibration_script(
        hpc_script_path,
        job_name=system_name,
        workflow_type="polymer",
    )

    _copy_workflow_inputs(dry_polymer_dir, charmm_gui_membrane_dir)
    charmm_mdp_paths = _copy_mdp_templates(
        charmm_gui_membrane_dir,
        GROMACS_CHARMM_GUI_MEMBRANE_MDP_TEMPLATE_NAMES,
    )
    charmm_local_script_path = charmm_gui_membrane_dir / "run_step6_local.sh"
    charmm_gui_membrane_hpc_script_path = (
        charmm_gui_membrane_dir / "run_hpc_charmm_gui_membrane.slurm"
    )
    _write_local_minimization_script(charmm_local_script_path)
    _write_hpc_equilibration_script(
        charmm_gui_membrane_hpc_script_path,
        job_name=f"{system_name}_charmm_gui_membrane",
        workflow_type="charmm_gui_membrane",
    )

    return GromacsPreparedRunFolder(
        output_dir=output_path,
        workflow_type=workflow_type,
        dry_polymer_dir=dry_polymer_dir,
        solvated_polymer_dir=solvated_polymer_dir,
        charmm_gui_membrane_dir=charmm_gui_membrane_dir,
        step5_input_gro_path=step5_input_gro_path,
        topol_top_path=topol_top_path,
        index_ndx_path=index_ndx_path,
        mdp_paths=dry_mdp_paths + solvated_mdp_paths + charmm_mdp_paths,
        local_script_path=local_script_path,
        hpc_script_path=(
            charmm_gui_membrane_hpc_script_path
            if workflow_type == "charmm_gui_membrane"
            else hpc_script_path
        ),
        charmm_gui_membrane_hpc_script_path=charmm_gui_membrane_hpc_script_path,
    )
```

</details>
