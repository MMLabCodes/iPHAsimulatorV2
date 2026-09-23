# pha_filepath_manager.py

Paths and persistent registries for chemistry, built chains, systems, protocols and runs. Constructors initialise directories/CSV files; this is not a strictly read-only path abstraction. The module imports ParmEd for atom counting. Registry identity and file existence checks do not establish scientific validity.

[Current source](../../src/iphasimulator/pha_filepath_manager.py)

This page is generated from source syntax. Original docstrings can be incomplete or outdated; module notes above identify known discrepancies. Call/return/error lists describe direct syntax, not all behaviour inside callees. Read the source excerpt for branch order and effects. No scientific execution is implied.

Explicit functions/methods/nested helpers: **71**.

## Module imports

```python
from pathlib import Path
import csv
import itertools
import re
import parmed as pmd
```

## Classes and result records

### `PHAFileManager`

Manage paths for the PHA structure database.

This class is the central source of truth for directory names,
system names, and file locations.

### `PHAResidueCodeManager`

Manage the PHA residue code registry.

The residue code CSV links user-facing PHA names to internal Amber-style
residue codes.

Expected CSV format:

    PHA_type,component,readable_name,residue_code,smiles

    3HB,trimer,P3HB_3,AAA,...
    3HB,head,hP3HB,AAB,...
    3HB,mainchain,mP3HB,AAC,...
    3HB,tail,tP3HB,AAD,...

Parameters
----------
paths : PHAFileManager
    Filepath manager used to locate residue_codes.csv.

Declared fields/defaults (instance state may also be set by methods):

```python
forbidden_codes = {'UNL', 'ALA', 'ARG', 'ASN', 'ASP', 'ASX', 'CYS', 'GLU', 'GLN', 'GLX', 'HIS', 'ILE', 'LEU', 'LYS', 'MET', 'PHE', 'PRO', 'SER', 'THR', 'SEC', 'TRP', 'TYR', 'VAL'}
header = ['PHA_type', 'component', 'readable_name', 'residue_code', 'smiles']
```

## Function map

- [`PHAFileManager.__init__` — source line 38](#definition-38)
- [`PHAFileManager._create_base_structure` — source line 59](#definition-59)
- [`PHAFileManager.get_root_dir` — source line 84](#definition-84)
- [`PHAFileManager.get_temp_dir` — source line 87](#definition-87)
- [`PHAFileManager.get_residue_codes_csv` — source line 90](#definition-90)
- [`PHAFileManager.get_polymer_smiles_csv` — source line 93](#definition-93)
- [`PHAFileManager.get_md_systems_csv` — source line 96](#definition-96)
- [`PHAFileManager.get_PHA_type_dir` — source line 106](#definition-106)
- [`PHAFileManager.create_PHA_type_dir` — source line 109](#definition-109)
- [`PHAFileManager.get_PHA_input_dir` — source line 125](#definition-125)
- [`PHAFileManager.get_PHA_trimer_dir` — source line 128](#definition-128)
- [`PHAFileManager.get_PHA_monomer_units_dir` — source line 131](#definition-131)
- [`PHAFileManager.get_PHA_leap_template_dir` — source line 134](#definition-134)
- [`PHAFileManager.get_PHA_monomer_unit_files` — source line 137](#definition-137)
- [`PHAFileManager.get_built_PHA_name` — source line 157](#definition-157)
- [`PHAFileManager.parse_built_PHA_name` — source line 160](#definition-160)
- [`PHAFileManager.get_built_PHA_dir` — source line 183](#definition-183)
- [`PHAFileManager.create_built_PHA_dir` — source line 191](#definition-191)
- [`PHAFileManager.get_built_PHA_leap_dir` — source line 209](#definition-209)
- [`PHAFileManager.get_built_PHA_amber_dir` — source line 212](#definition-212)
- [`PHAFileManager.get_built_PHA_gromacs_dir` — source line 215](#definition-215)
- [`PHAFileManager.get_built_PHA_amber_files` — source line 218](#definition-218)
- [`PHAFileManager.get_PHA_dry_dir` — source line 241](#definition-241)
- [`PHAFileManager.get_dry_PHA_system_name` — source line 248](#definition-248)
- [`PHAFileManager.get_dry_PHA_dir` — source line 251](#definition-251)
- [`PHAFileManager.get_dry_PHA_inputs_dir` — source line 256](#definition-256)
- [`PHAFileManager.get_dry_PHA_simulations_dir` — source line 259](#definition-259)
- [`PHAFileManager.create_dry_PHA_dir` — source line 262](#definition-262)
- [`PHAFileManager.get_PHA_solvated_dir` — source line 286](#definition-286)
- [`PHAFileManager.get_solvated_PHA_system_name` — source line 293](#definition-293)
- [`PHAFileManager.get_solvated_PHA_dir` — source line 296](#definition-296)
- [`PHAFileManager.get_solvated_PHA_inputs_dir` — source line 301](#definition-301)
- [`PHAFileManager.get_solvated_PHA_simulations_dir` — source line 304](#definition-304)
- [`PHAFileManager.create_solvated_PHA_dir` — source line 307](#definition-307)
- [`PHAFileManager.get_PHA_solvated_ions_dir` — source line 331](#definition-331)
- [`PHAFileManager.format_concentration_label` — source line 337](#definition-337)
- [`PHAFileManager.get_solvated_ions_PHA_system_name` — source line 347](#definition-347)
- [`PHAFileManager.get_solvated_ions_PHA_dir` — source line 369](#definition-369)
- [`PHAFileManager.get_solvated_ions_PHA_inputs_dir` — source line 386](#definition-386)
- [`PHAFileManager.get_solvated_ions_PHA_simulations_dir` — source line 404](#definition-404)
- [`PHAFileManager.create_solvated_ions_PHA_dir` — source line 422](#definition-422)
- [`PHAFileManager.get_PHA_melt_name` — source line 465](#definition-465)
- [`PHAFileManager.get_PHA_melt_dir` — source line 488](#definition-488)
- [`PHAFileManager.create_PHA_melt_dir` — source line 500](#definition-500)
- [`PHAFileManager.get_PHA_melt_inputs_dir` — source line 533](#definition-533)
- [`PHAFileManager.get_PHA_melt_simulations_dir` — source line 546](#definition-546)
- [`PHAFileManager.create_PHA_melt_simulation_run_dir` — source line 559](#definition-559)
- [`PHAFileManager.create_named_PHA_melt_simulation_run_dir` — source line 587](#definition-587)
- [`PHAFileManager.ensure_md_systems_csv_exists` — source line 630](#definition-630)
- [`PHAFileManager.load_md_systems` — source line 657](#definition-657)
- [`PHAFileManager.get_md_system` — source line 677](#definition-677)
- [`PHAFileManager.md_system_exists` — source line 707](#definition-707)
- [`PHAFileManager.register_md_system` — source line 719](#definition-719)
- [`PHAFileManager.get_md_system_files` — source line 825](#definition-825)
- [`PHAFileManager.get_md_system_workflows_dir` — source line 918](#definition-918)
- [`PHAFileManager.get_md_system_workflow_path` — source line 964](#definition-964)
- [`PHAFileManager.list_md_system_workflows` — source line 1047](#definition-1047)
- [`PHAFileManager.create_named_md_system_simulation_run_dir` — source line 1089](#definition-1089)
- [`PHAFileManager.validate_md_system_files` — source line 1149](#definition-1149)
- [`PHAFileManager.find_file` — source line 1189](#definition-1189)
- [`PHAFileManager.find_files` — source line 1201](#definition-1201)
- [`PHAFileManager.count_atoms_from_amber_topology` — source line 1208](#definition-1208)
- [`PHAFileManager.count_atoms_from_gromacs_gro` — source line 1226](#definition-1226)
- [`PHAResidueCodeManager.__init__` — source line 1311](#definition-1311)
- [`PHAResidueCodeManager._ensure_csv_exists` — source line 1324](#definition-1324)
- [`PHAResidueCodeManager.load_rows` — source line 1334](#definition-1334)
- [`PHAResidueCodeManager.get_used_codes` — source line 1347](#definition-1347)
- [`PHAResidueCodeManager.PHA_type_exists` — source line 1359](#definition-1359)
- [`PHAResidueCodeManager.get_code` — source line 1374](#definition-1374)
- [`PHAResidueCodeManager.generate_unique_codes` — source line 1400](#definition-1400)
- [`PHAResidueCodeManager.register_PHA_type` — source line 1444](#definition-1444)

<a id="definition-38"></a>

## `PHAFileManager.__init__`

Source lines 38–57. Internal helper/protocol method.

```python
def __init__(self, root_dir='structure_database'): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| root_dir | not annotated | 'structure_database' |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `Path`, `self._create_base_structure`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Instance/class attributes assigned directly: `self.PHA_dry_dir`, `self.PHA_melts_dir`, `self.PHA_solvated_dir`, `self.PHA_solvated_ions_dir`, `self.PHA_types_dir`, `self.built_PHAs_dir`, `self.md_systems_csv`, `self.polymer_smiles_csv`, `self.residue_codes_csv`, `self.root_dir`, `self.temp_dir`.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def __init__(self, root_dir="structure_database"):
    self.root_dir = Path(root_dir)

    # Main database directories
    self.PHA_types_dir = self.root_dir / "PHA_types"
    self.built_PHAs_dir = self.root_dir / "built_PHAs"
    self.PHA_melts_dir = self.root_dir / "PHA_melts"

    self.PHA_dry_dir = self.root_dir / "PHA_dry"
    self.PHA_solvated_dir = self.root_dir / "PHA_solvated"
    self.PHA_solvated_ions_dir = self.root_dir / "PHA_solvated_ions"

    self.temp_dir = self.root_dir / "temp"

    # Database files
    self.residue_codes_csv = self.root_dir / "residue_codes.csv"
    self.polymer_smiles_csv = self.root_dir / "polymer_smiles.csv"
    self.md_systems_csv = self.root_dir / "md_systems.csv"

    self._create_base_structure()
```

</details>

<a id="definition-59"></a>

## `PHAFileManager._create_base_structure`

Source lines 59–78. Internal helper/protocol method.

```python
def _create_base_structure(self): ...
```

### Purpose and original contract

Create the main structure-database directories.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `directory.mkdir`, `self.ensure_md_systems_csv_exists`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Calls worth inspecting for I/O, state changes or delegated execution: `directory.mkdir`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _create_base_structure(self):
    """
    Create the main structure-database directories.
    """

    for directory in [
        self.root_dir,
        self.PHA_types_dir,
        self.built_PHAs_dir,
        self.PHA_melts_dir,
        self.PHA_dry_dir,
        self.PHA_solvated_dir,
        self.PHA_solvated_ions_dir,
        self.temp_dir,
    ]:
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )
    self.ensure_md_systems_csv_exists()
```

</details>

<a id="definition-84"></a>

## `PHAFileManager.get_root_dir`

Source lines 84–85. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_root_dir(self): ...
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
self.root_dir
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_root_dir(self):
    return self.root_dir
```

</details>

<a id="definition-87"></a>

## `PHAFileManager.get_temp_dir`

Source lines 87–88. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_temp_dir(self): ...
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
self.temp_dir
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_temp_dir(self):
    return self.temp_dir
```

</details>

<a id="definition-90"></a>

## `PHAFileManager.get_residue_codes_csv`

Source lines 90–91. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_residue_codes_csv(self): ...
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
self.residue_codes_csv
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_residue_codes_csv(self):
    return self.residue_codes_csv
```

</details>

<a id="definition-93"></a>

## `PHAFileManager.get_polymer_smiles_csv`

Source lines 93–94. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_polymer_smiles_csv(self): ...
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
self.polymer_smiles_csv
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_polymer_smiles_csv(self):
    return self.polymer_smiles_csv
```

</details>

<a id="definition-96"></a>

## `PHAFileManager.get_md_systems_csv`

Source lines 96–100. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_md_systems_csv(self): ...
```

### Purpose and original contract

Return the path to md_systems.csv.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |

### How to read this implementation

No direct function calls were found in this definition's own body.

Explicit return expressions; different branches may return different objects:

```python
self.md_systems_csv
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_md_systems_csv(self):
    """
    Return the path to md_systems.csv.
    """
    return self.md_systems_csv
```

</details>

<a id="definition-106"></a>

## `PHAFileManager.get_PHA_type_dir`

Source lines 106–107. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_PHA_type_dir(self, PHA_type): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| PHA_type | not annotated | required |

### How to read this implementation

No direct function calls were found in this definition's own body.

Explicit return expressions; different branches may return different objects:

```python
self.PHA_types_dir / PHA_type
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_PHA_type_dir(self, PHA_type):
    return self.PHA_types_dir / PHA_type
```

</details>

<a id="definition-109"></a>

## `PHAFileManager.create_PHA_type_dir`

Source lines 109–123. Named callable; inspect its callers before treating it as a stable public API.

```python
def create_PHA_type_dir(self, PHA_type): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| PHA_type | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `(pha_dir / subdir).mkdir`, `self.get_PHA_type_dir`.

Explicit return expressions; different branches may return different objects:

```python
pha_dir
```

Calls worth inspecting for I/O, state changes or delegated execution: `(pha_dir / subdir).mkdir`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def create_PHA_type_dir(self, PHA_type):
    pha_dir = self.get_PHA_type_dir(PHA_type)

    for subdir in [
        "input",
        "trimer",
        "monomer_units",
        "leap_templates",
    ]:
        (pha_dir / subdir).mkdir(
            parents=True,
            exist_ok=True,
        )

    return pha_dir
```

</details>

<a id="definition-125"></a>

## `PHAFileManager.get_PHA_input_dir`

Source lines 125–126. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_PHA_input_dir(self, PHA_type): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| PHA_type | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.get_PHA_type_dir`.

Explicit return expressions; different branches may return different objects:

```python
self.get_PHA_type_dir(PHA_type) / 'input'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_PHA_input_dir(self, PHA_type):
    return self.get_PHA_type_dir(PHA_type) / "input"
```

</details>

<a id="definition-128"></a>

## `PHAFileManager.get_PHA_trimer_dir`

Source lines 128–129. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_PHA_trimer_dir(self, PHA_type): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| PHA_type | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.get_PHA_type_dir`.

Explicit return expressions; different branches may return different objects:

```python
self.get_PHA_type_dir(PHA_type) / 'trimer'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_PHA_trimer_dir(self, PHA_type):
    return self.get_PHA_type_dir(PHA_type) / "trimer"
```

</details>

<a id="definition-131"></a>

## `PHAFileManager.get_PHA_monomer_units_dir`

Source lines 131–132. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_PHA_monomer_units_dir(self, PHA_type): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| PHA_type | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.get_PHA_type_dir`.

Explicit return expressions; different branches may return different objects:

```python
self.get_PHA_type_dir(PHA_type) / 'monomer_units'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_PHA_monomer_units_dir(self, PHA_type):
    return self.get_PHA_type_dir(PHA_type) / "monomer_units"
```

</details>

<a id="definition-134"></a>

## `PHAFileManager.get_PHA_leap_template_dir`

Source lines 134–135. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_PHA_leap_template_dir(self, PHA_type): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| PHA_type | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.get_PHA_type_dir`.

Explicit return expressions; different branches may return different objects:

```python
self.get_PHA_type_dir(PHA_type) / 'leap_templates'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_PHA_leap_template_dir(self, PHA_type):
    return self.get_PHA_type_dir(PHA_type) / "leap_templates"
```

</details>

<a id="definition-137"></a>

## `PHAFileManager.get_PHA_monomer_unit_files`

Source lines 137–151. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_PHA_monomer_unit_files(self, PHA_type): ...
```

### Purpose and original contract

Return the parameter files for one PHA chemistry.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| PHA_type | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.get_PHA_monomer_units_dir`, `self.get_PHA_trimer_dir`.

Explicit return expressions; different branches may return different objects:

```python
{'monomer_units_dir': monomer_units_dir, 'head_prepin': monomer_units_dir / f'hP{PHA_type}.prepin', 'mainchain_prepin': monomer_units_dir / f'mP{PHA_type}.prepin', 'tail_prepin': monomer_units_dir / f'tP{PHA_type}.prepin', 'frcmod': trimer_dir / f'P{PHA_type}_3.frcmod'}
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_PHA_monomer_unit_files(self, PHA_type):
    """
    Return the parameter files for one PHA chemistry.
    """

    monomer_units_dir = self.get_PHA_monomer_units_dir(PHA_type)
    trimer_dir = self.get_PHA_trimer_dir(PHA_type)

    return {
        "monomer_units_dir": monomer_units_dir,
        "head_prepin": monomer_units_dir / f"hP{PHA_type}.prepin",
        "mainchain_prepin": monomer_units_dir / f"mP{PHA_type}.prepin",
        "tail_prepin": monomer_units_dir / f"tP{PHA_type}.prepin",
        "frcmod": trimer_dir / f"P{PHA_type}_3.frcmod",
    }
```

</details>

<a id="definition-157"></a>

## `PHAFileManager.get_built_PHA_name`

Source lines 157–158. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_built_PHA_name(self, PHA_type, length): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| PHA_type | not annotated | required |
| length | not annotated | required |

### How to read this implementation

No direct function calls were found in this definition's own body.

Explicit return expressions; different branches may return different objects:

```python
f'P{PHA_type}_{length}'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_built_PHA_name(self, PHA_type, length):
    return f"P{PHA_type}_{length}"
```

</details>

<a id="definition-160"></a>

## `PHAFileManager.parse_built_PHA_name`

Source lines 160–181. Named callable; inspect its callers before treating it as a stable public API.

```python
def parse_built_PHA_name(self, polymer_name): ...
```

### Purpose and original contract

Parse a polymer name such as P3HB_10.

Returns
-------
tuple
    PHA type and polymer length.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| polymer_name | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `int`, `match.group`, `re.fullmatch`.

Explicit return expressions; different branches may return different objects:

```python
(PHA_type, length)
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError(f'Invalid polymer name: {polymer_name}\nExpected format like: P3HB_10')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def parse_built_PHA_name(self, polymer_name):
    """
    Parse a polymer name such as P3HB_10.

    Returns
    -------
    tuple
        PHA type and polymer length.
    """

    match = re.fullmatch(r"P(.+)_(\d+)", polymer_name)

    if match is None:
        raise ValueError(
            f"Invalid polymer name: {polymer_name}\n"
            "Expected format like: P3HB_10"
        )

    PHA_type = match.group(1)
    length = int(match.group(2))

    return PHA_type, length
```

</details>

<a id="definition-183"></a>

## `PHAFileManager.get_built_PHA_dir`

Source lines 183–189. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_built_PHA_dir(self, PHA_type, length): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| PHA_type | not annotated | required |
| length | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.get_built_PHA_name`.

Explicit return expressions; different branches may return different objects:

```python
self.built_PHAs_dir / polymer_name
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_built_PHA_dir(self, PHA_type, length):
    polymer_name = self.get_built_PHA_name(
        PHA_type,
        length,
    )

    return self.built_PHAs_dir / polymer_name
```

</details>

<a id="definition-191"></a>

## `PHAFileManager.create_built_PHA_dir`

Source lines 191–207. Named callable; inspect its callers before treating it as a stable public API.

```python
def create_built_PHA_dir(self, PHA_type, length): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| PHA_type | not annotated | required |
| length | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `(build_dir / subdir).mkdir`, `self.get_built_PHA_dir`.

Explicit return expressions; different branches may return different objects:

```python
build_dir
```

Calls worth inspecting for I/O, state changes or delegated execution: `(build_dir / subdir).mkdir`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def create_built_PHA_dir(self, PHA_type, length):
    build_dir = self.get_built_PHA_dir(
        PHA_type,
        length,
    )

    for subdir in [
        "leap",
        "amber",
        "gromacs",
    ]:
        (build_dir / subdir).mkdir(
            parents=True,
            exist_ok=True,
        )

    return build_dir
```

</details>

<a id="definition-209"></a>

## `PHAFileManager.get_built_PHA_leap_dir`

Source lines 209–210. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_built_PHA_leap_dir(self, PHA_type, length): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| PHA_type | not annotated | required |
| length | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.get_built_PHA_dir`.

Explicit return expressions; different branches may return different objects:

```python
self.get_built_PHA_dir(PHA_type, length) / 'leap'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_built_PHA_leap_dir(self, PHA_type, length):
    return self.get_built_PHA_dir(PHA_type, length) / "leap"
```

</details>

<a id="definition-212"></a>

## `PHAFileManager.get_built_PHA_amber_dir`

Source lines 212–213. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_built_PHA_amber_dir(self, PHA_type, length): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| PHA_type | not annotated | required |
| length | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.get_built_PHA_dir`.

Explicit return expressions; different branches may return different objects:

```python
self.get_built_PHA_dir(PHA_type, length) / 'amber'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_built_PHA_amber_dir(self, PHA_type, length):
    return self.get_built_PHA_dir(PHA_type, length) / "amber"
```

</details>

<a id="definition-215"></a>

## `PHAFileManager.get_built_PHA_gromacs_dir`

Source lines 215–216. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_built_PHA_gromacs_dir(self, PHA_type, length): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| PHA_type | not annotated | required |
| length | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.get_built_PHA_dir`.

Explicit return expressions; different branches may return different objects:

```python
self.get_built_PHA_dir(PHA_type, length) / 'gromacs'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_built_PHA_gromacs_dir(self, PHA_type, length):
    return self.get_built_PHA_dir(PHA_type, length) / "gromacs"
```

</details>

<a id="definition-218"></a>

## `PHAFileManager.get_built_PHA_amber_files`

Source lines 218–235. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_built_PHA_amber_files(self, polymer_name): ...
```

### Purpose and original contract

Return expected Amber files for an already-built polymer.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| polymer_name | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.get_built_PHA_amber_dir`, `self.parse_built_PHA_name`.

Explicit return expressions; different branches may return different objects:

```python
{'amber_dir': amber_dir, 'pdb': amber_dir / f'{polymer_name}.pdb', 'prmtop': amber_dir / f'{polymer_name}.prmtop', 'rst7': amber_dir / f'{polymer_name}.rst7'}
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_built_PHA_amber_files(self, polymer_name):
    """
    Return expected Amber files for an already-built polymer.
    """

    PHA_type, length = self.parse_built_PHA_name(polymer_name)

    amber_dir = self.get_built_PHA_amber_dir(
        PHA_type,
        length,
    )

    return {
        "amber_dir": amber_dir,
        "pdb": amber_dir / f"{polymer_name}.pdb",
        "prmtop": amber_dir / f"{polymer_name}.prmtop",
        "rst7": amber_dir / f"{polymer_name}.rst7",
    }
```

</details>

<a id="definition-241"></a>

## `PHAFileManager.get_PHA_dry_dir`

Source lines 241–246. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_PHA_dry_dir(self): ...
```

### Purpose and original contract

Return the parent directory for all dry PHA systems.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |

### How to read this implementation

No direct function calls were found in this definition's own body.

Explicit return expressions; different branches may return different objects:

```python
self.PHA_dry_dir
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_PHA_dry_dir(self):
    """
    Return the parent directory for all dry PHA systems.
    """

    return self.PHA_dry_dir
```

</details>

<a id="definition-248"></a>

## `PHAFileManager.get_dry_PHA_system_name`

Source lines 248–249. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_dry_PHA_system_name(self, polymer_name): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| polymer_name | not annotated | required |

### How to read this implementation

No direct function calls were found in this definition's own body.

Explicit return expressions; different branches may return different objects:

```python
f'{polymer_name}_dry'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_dry_PHA_system_name(self, polymer_name):
    return f"{polymer_name}_dry"
```

</details>

<a id="definition-251"></a>

## `PHAFileManager.get_dry_PHA_dir`

Source lines 251–254. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_dry_PHA_dir(self, polymer_name): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| polymer_name | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.get_PHA_dry_dir`, `self.get_dry_PHA_system_name`.

Explicit return expressions; different branches may return different objects:

```python
self.get_PHA_dry_dir() / system_name
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_dry_PHA_dir(self, polymer_name):
    system_name = self.get_dry_PHA_system_name(polymer_name)

    return self.get_PHA_dry_dir() / system_name
```

</details>

<a id="definition-256"></a>

## `PHAFileManager.get_dry_PHA_inputs_dir`

Source lines 256–257. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_dry_PHA_inputs_dir(self, polymer_name): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| polymer_name | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.get_dry_PHA_dir`.

Explicit return expressions; different branches may return different objects:

```python
self.get_dry_PHA_dir(polymer_name) / 'inputs'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_dry_PHA_inputs_dir(self, polymer_name):
    return self.get_dry_PHA_dir(polymer_name) / "inputs"
```

</details>

<a id="definition-259"></a>

## `PHAFileManager.get_dry_PHA_simulations_dir`

Source lines 259–260. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_dry_PHA_simulations_dir(self, polymer_name): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| polymer_name | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.get_dry_PHA_dir`.

Explicit return expressions; different branches may return different objects:

```python
self.get_dry_PHA_dir(polymer_name) / 'simulations'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_dry_PHA_simulations_dir(self, polymer_name):
    return self.get_dry_PHA_dir(polymer_name) / "simulations"
```

</details>

<a id="definition-262"></a>

## `PHAFileManager.create_dry_PHA_dir`

Source lines 262–280. Named callable; inspect its callers before treating it as a stable public API.

```python
def create_dry_PHA_dir(self, polymer_name): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| polymer_name | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.get_dry_PHA_dir`, `self.get_dry_PHA_inputs_dir`, `self.get_dry_PHA_inputs_dir(polymer_name).mkdir`, `self.get_dry_PHA_simulations_dir`, `self.get_dry_PHA_simulations_dir(polymer_name).mkdir`, `system_dir.mkdir`.

Explicit return expressions; different branches may return different objects:

```python
system_dir
```

Calls worth inspecting for I/O, state changes or delegated execution: `self.get_dry_PHA_inputs_dir(polymer_name).mkdir`, `self.get_dry_PHA_simulations_dir(polymer_name).mkdir`, `system_dir.mkdir`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def create_dry_PHA_dir(self, polymer_name):
    system_dir = self.get_dry_PHA_dir(polymer_name)

    system_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    self.get_dry_PHA_inputs_dir(polymer_name).mkdir(
        parents=True,
        exist_ok=True,
    )

    self.get_dry_PHA_simulations_dir(polymer_name).mkdir(
        parents=True,
        exist_ok=True,
    )

    return system_dir
```

</details>

<a id="definition-286"></a>

## `PHAFileManager.get_PHA_solvated_dir`

Source lines 286–291. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_PHA_solvated_dir(self): ...
```

### Purpose and original contract

Return the parent directory for all solvated PHA systems.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |

### How to read this implementation

No direct function calls were found in this definition's own body.

Explicit return expressions; different branches may return different objects:

```python
self.PHA_solvated_dir
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_PHA_solvated_dir(self):
    """
    Return the parent directory for all solvated PHA systems.
    """

    return self.PHA_solvated_dir
```

</details>

<a id="definition-293"></a>

## `PHAFileManager.get_solvated_PHA_system_name`

Source lines 293–294. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_solvated_PHA_system_name(self, polymer_name): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| polymer_name | not annotated | required |

### How to read this implementation

No direct function calls were found in this definition's own body.

Explicit return expressions; different branches may return different objects:

```python
f'{polymer_name}_solvated'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_solvated_PHA_system_name(self, polymer_name):
    return f"{polymer_name}_solvated"
```

</details>

<a id="definition-296"></a>

## `PHAFileManager.get_solvated_PHA_dir`

Source lines 296–299. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_solvated_PHA_dir(self, polymer_name): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| polymer_name | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.get_PHA_solvated_dir`, `self.get_solvated_PHA_system_name`.

Explicit return expressions; different branches may return different objects:

```python
self.get_PHA_solvated_dir() / system_name
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_solvated_PHA_dir(self, polymer_name):
    system_name = self.get_solvated_PHA_system_name(polymer_name)

    return self.get_PHA_solvated_dir() / system_name
```

</details>

<a id="definition-301"></a>

## `PHAFileManager.get_solvated_PHA_inputs_dir`

Source lines 301–302. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_solvated_PHA_inputs_dir(self, polymer_name): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| polymer_name | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.get_solvated_PHA_dir`.

Explicit return expressions; different branches may return different objects:

```python
self.get_solvated_PHA_dir(polymer_name) / 'inputs'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_solvated_PHA_inputs_dir(self, polymer_name):
    return self.get_solvated_PHA_dir(polymer_name) / "inputs"
```

</details>

<a id="definition-304"></a>

## `PHAFileManager.get_solvated_PHA_simulations_dir`

Source lines 304–305. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_solvated_PHA_simulations_dir(self, polymer_name): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| polymer_name | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.get_solvated_PHA_dir`.

Explicit return expressions; different branches may return different objects:

```python
self.get_solvated_PHA_dir(polymer_name) / 'simulations'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_solvated_PHA_simulations_dir(self, polymer_name):
    return self.get_solvated_PHA_dir(polymer_name) / "simulations"
```

</details>

<a id="definition-307"></a>

## `PHAFileManager.create_solvated_PHA_dir`

Source lines 307–325. Named callable; inspect its callers before treating it as a stable public API.

```python
def create_solvated_PHA_dir(self, polymer_name): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| polymer_name | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.get_solvated_PHA_dir`, `self.get_solvated_PHA_inputs_dir`, `self.get_solvated_PHA_inputs_dir(polymer_name).mkdir`, `self.get_solvated_PHA_simulations_dir`, `self.get_solvated_PHA_simulations_dir(polymer_name).mkdir`, `system_dir.mkdir`.

Explicit return expressions; different branches may return different objects:

```python
system_dir
```

Calls worth inspecting for I/O, state changes or delegated execution: `self.get_solvated_PHA_inputs_dir(polymer_name).mkdir`, `self.get_solvated_PHA_simulations_dir(polymer_name).mkdir`, `system_dir.mkdir`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def create_solvated_PHA_dir(self, polymer_name):
    system_dir = self.get_solvated_PHA_dir(polymer_name)

    system_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    self.get_solvated_PHA_inputs_dir(polymer_name).mkdir(
        parents=True,
        exist_ok=True,
    )

    self.get_solvated_PHA_simulations_dir(polymer_name).mkdir(
        parents=True,
        exist_ok=True,
    )

    return system_dir
```

</details>

<a id="definition-331"></a>

## `PHAFileManager.get_PHA_solvated_ions_dir`

Source lines 331–335. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_PHA_solvated_ions_dir(self): ...
```

### Purpose and original contract

Return the parent directory containing all solvated + ionised PHA systems.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |

### How to read this implementation

No direct function calls were found in this definition's own body.

Explicit return expressions; different branches may return different objects:

```python
self.PHA_solvated_ions_dir
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_PHA_solvated_ions_dir(self):
    """
    Return the parent directory containing all solvated + ionised PHA systems.
    """
    return self.PHA_solvated_ions_dir
```

</details>

<a id="definition-337"></a>

## `PHAFileManager.format_concentration_label`

Source lines 337–345. Named callable; inspect its callers before treating it as a stable public API.

```python
def format_concentration_label(self, ion_concentration): ...
```

### Purpose and original contract

Convert an ion concentration into a filename-safe label.

Example
-------
0.15 -> 0_15

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| ion_concentration | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `str`, `str(ion_concentration).replace`.

Explicit return expressions; different branches may return different objects:

```python
str(ion_concentration).replace('.', '_')
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def format_concentration_label(self, ion_concentration):
    """
    Convert an ion concentration into a filename-safe label.

    Example
    -------
    0.15 -> 0_15
    """
    return str(ion_concentration).replace(".", "_")
```

</details>

<a id="definition-347"></a>

## `PHAFileManager.get_solvated_ions_PHA_system_name`

Source lines 347–367. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_solvated_ions_PHA_system_name(self, polymer_name, salt, ion_concentration): ...
```

### Purpose and original contract

Return the standard name for a solvated + ionised PHA system.

Example
-------
P3HB_10_solvated_KCl_0_15

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| polymer_name | not annotated | required |
| salt | not annotated | required |
| ion_concentration | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.format_concentration_label`.

Explicit return expressions; different branches may return different objects:

```python
f'{polymer_name}_solvated_{salt}_{concentration_label}'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_solvated_ions_PHA_system_name(
    self,
    polymer_name,
    salt,
    ion_concentration,
):
    """
    Return the standard name for a solvated + ionised PHA system.

    Example
    -------
    P3HB_10_solvated_KCl_0_15
    """
    concentration_label = self.format_concentration_label(
        ion_concentration
    )

    return (
        f"{polymer_name}_solvated_"
        f"{salt}_{concentration_label}"
    )
```

</details>

<a id="definition-369"></a>

## `PHAFileManager.get_solvated_ions_PHA_dir`

Source lines 369–384. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_solvated_ions_PHA_dir(self, polymer_name, salt, ion_concentration): ...
```

### Purpose and original contract

Return the directory for a solvated + ionised PHA system.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| polymer_name | not annotated | required |
| salt | not annotated | required |
| ion_concentration | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.get_PHA_solvated_ions_dir`, `self.get_solvated_ions_PHA_system_name`.

Explicit return expressions; different branches may return different objects:

```python
self.get_PHA_solvated_ions_dir() / system_name
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_solvated_ions_PHA_dir(
    self,
    polymer_name,
    salt,
    ion_concentration,
):
    """
    Return the directory for a solvated + ionised PHA system.
    """
    system_name = self.get_solvated_ions_PHA_system_name(
        polymer_name=polymer_name,
        salt=salt,
        ion_concentration=ion_concentration,
    )

    return self.get_PHA_solvated_ions_dir() / system_name
```

</details>

<a id="definition-386"></a>

## `PHAFileManager.get_solvated_ions_PHA_inputs_dir`

Source lines 386–402. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_solvated_ions_PHA_inputs_dir(self, polymer_name, salt, ion_concentration): ...
```

### Purpose and original contract

Return the inputs directory for a solvated + ionised PHA system.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| polymer_name | not annotated | required |
| salt | not annotated | required |
| ion_concentration | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.get_solvated_ions_PHA_dir`.

Explicit return expressions; different branches may return different objects:

```python
self.get_solvated_ions_PHA_dir(polymer_name=polymer_name, salt=salt, ion_concentration=ion_concentration) / 'inputs'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_solvated_ions_PHA_inputs_dir(
    self,
    polymer_name,
    salt,
    ion_concentration,
):
    """
    Return the inputs directory for a solvated + ionised PHA system.
    """
    return (
        self.get_solvated_ions_PHA_dir(
            polymer_name=polymer_name,
            salt=salt,
            ion_concentration=ion_concentration,
        )
        / "inputs"
    )
```

</details>

<a id="definition-404"></a>

## `PHAFileManager.get_solvated_ions_PHA_simulations_dir`

Source lines 404–420. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_solvated_ions_PHA_simulations_dir(self, polymer_name, salt, ion_concentration): ...
```

### Purpose and original contract

Return the simulations directory for a solvated + ionised PHA system.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| polymer_name | not annotated | required |
| salt | not annotated | required |
| ion_concentration | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.get_solvated_ions_PHA_dir`.

Explicit return expressions; different branches may return different objects:

```python
self.get_solvated_ions_PHA_dir(polymer_name=polymer_name, salt=salt, ion_concentration=ion_concentration) / 'simulations'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_solvated_ions_PHA_simulations_dir(
    self,
    polymer_name,
    salt,
    ion_concentration,
):
    """
    Return the simulations directory for a solvated + ionised PHA system.
    """
    return (
        self.get_solvated_ions_PHA_dir(
            polymer_name=polymer_name,
            salt=salt,
            ion_concentration=ion_concentration,
        )
        / "simulations"
    )
```

</details>

<a id="definition-422"></a>

## `PHAFileManager.create_solvated_ions_PHA_dir`

Source lines 422–460. Named callable; inspect its callers before treating it as a stable public API.

```python
def create_solvated_ions_PHA_dir(self, polymer_name, salt, ion_concentration): ...
```

### Purpose and original contract

Create the directory structure for a solvated + ionised PHA system.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| polymer_name | not annotated | required |
| salt | not annotated | required |
| ion_concentration | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.get_solvated_ions_PHA_dir`, `self.get_solvated_ions_PHA_inputs_dir`, `self.get_solvated_ions_PHA_inputs_dir(polymer_name=polymer_name, salt=salt, ion_concentration=ion_concentration).mkdir`, `self.get_solvated_ions_PHA_simulations_dir`, `self.get_solvated_ions_PHA_simulations_dir(polymer_name=polymer_name, salt=salt, ion_concentration=ion_concentration).mkdir`, `system_dir.mkdir`.

Explicit return expressions; different branches may return different objects:

```python
system_dir
```

Calls worth inspecting for I/O, state changes or delegated execution: `self.get_solvated_ions_PHA_inputs_dir(polymer_name=polymer_name, salt=salt, ion_concentration=ion_concentration).mkdir`, `self.get_solvated_ions_PHA_simulations_dir(polymer_name=polymer_name, salt=salt, ion_concentration=ion_concentration).mkdir`, `system_dir.mkdir`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def create_solvated_ions_PHA_dir(
    self,
    polymer_name,
    salt,
    ion_concentration,
):
    """
    Create the directory structure for a solvated + ionised PHA system.
    """
    system_dir = self.get_solvated_ions_PHA_dir(
        polymer_name=polymer_name,
        salt=salt,
        ion_concentration=ion_concentration,
    )

    system_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    self.get_solvated_ions_PHA_inputs_dir(
        polymer_name=polymer_name,
        salt=salt,
        ion_concentration=ion_concentration,
    ).mkdir(
        parents=True,
        exist_ok=True,
    )

    self.get_solvated_ions_PHA_simulations_dir(
        polymer_name=polymer_name,
        salt=salt,
        ion_concentration=ion_concentration,
    ).mkdir(
        parents=True,
        exist_ok=True,
    )

    return system_dir
```

</details>

<a id="definition-465"></a>

## `PHAFileManager.get_PHA_melt_name`

Source lines 465–486. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_PHA_melt_name(self, polymer_names, number_of_polymers): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| polymer_names | not annotated | required |
| number_of_polymers | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `'_'.join`, `ValueError`, `len`, `name_parts.append`, `zip`.

Explicit return expressions; different branches may return different objects:

```python
'_'.join(name_parts) + '_melt'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('polymer_names and number_of_polymers must have the same length.')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_PHA_melt_name(
    self,
    polymer_names,
    number_of_polymers,
):
    if len(polymer_names) != len(number_of_polymers):
        raise ValueError(
            "polymer_names and number_of_polymers must have "
            "the same length."
        )

    name_parts = []

    for polymer_name, number in zip(
        polymer_names,
        number_of_polymers,
    ):
        name_parts.append(
            f"{number}_{polymer_name}"
        )

    return "_".join(name_parts) + "_melt"
```

</details>

<a id="definition-488"></a>

## `PHAFileManager.get_PHA_melt_dir`

Source lines 488–498. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_PHA_melt_dir(self, polymer_names, number_of_polymers): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| polymer_names | not annotated | required |
| number_of_polymers | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.get_PHA_melt_name`.

Explicit return expressions; different branches may return different objects:

```python
self.PHA_melts_dir / melt_name
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_PHA_melt_dir(
    self,
    polymer_names,
    number_of_polymers,
):
    melt_name = self.get_PHA_melt_name(
        polymer_names,
        number_of_polymers,
    )

    return self.PHA_melts_dir / melt_name
```

</details>

<a id="definition-500"></a>

## `PHAFileManager.create_PHA_melt_dir`

Source lines 500–531. Named callable; inspect its callers before treating it as a stable public API.

```python
def create_PHA_melt_dir(self, polymer_names, number_of_polymers): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| polymer_names | not annotated | required |
| number_of_polymers | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `melt_dir.mkdir`, `self.get_PHA_melt_dir`, `self.get_PHA_melt_inputs_dir`, `self.get_PHA_melt_inputs_dir(polymer_names, number_of_polymers).mkdir`, `self.get_PHA_melt_simulations_dir`, `self.get_PHA_melt_simulations_dir(polymer_names, number_of_polymers).mkdir`.

Explicit return expressions; different branches may return different objects:

```python
melt_dir
```

Calls worth inspecting for I/O, state changes or delegated execution: `melt_dir.mkdir`, `self.get_PHA_melt_inputs_dir(polymer_names, number_of_polymers).mkdir`, `self.get_PHA_melt_simulations_dir(polymer_names, number_of_polymers).mkdir`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def create_PHA_melt_dir(
    self,
    polymer_names,
    number_of_polymers,
):
    melt_dir = self.get_PHA_melt_dir(
        polymer_names,
        number_of_polymers,
    )

    melt_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    self.get_PHA_melt_inputs_dir(
        polymer_names,
        number_of_polymers,
    ).mkdir(
        parents=True,
        exist_ok=True,
    )

    self.get_PHA_melt_simulations_dir(
        polymer_names,
        number_of_polymers,
    ).mkdir(
        parents=True,
        exist_ok=True,
    )

    return melt_dir
```

</details>

<a id="definition-533"></a>

## `PHAFileManager.get_PHA_melt_inputs_dir`

Source lines 533–544. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_PHA_melt_inputs_dir(self, polymer_names, number_of_polymers): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| polymer_names | not annotated | required |
| number_of_polymers | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.get_PHA_melt_dir`.

Explicit return expressions; different branches may return different objects:

```python
self.get_PHA_melt_dir(polymer_names, number_of_polymers) / 'inputs'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_PHA_melt_inputs_dir(
    self,
    polymer_names,
    number_of_polymers,
):
    return (
        self.get_PHA_melt_dir(
            polymer_names,
            number_of_polymers,
        )
        / "inputs"
    )
```

</details>

<a id="definition-546"></a>

## `PHAFileManager.get_PHA_melt_simulations_dir`

Source lines 546–557. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_PHA_melt_simulations_dir(self, polymer_names, number_of_polymers): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| polymer_names | not annotated | required |
| number_of_polymers | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.get_PHA_melt_dir`.

Explicit return expressions; different branches may return different objects:

```python
self.get_PHA_melt_dir(polymer_names, number_of_polymers) / 'simulations'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_PHA_melt_simulations_dir(
    self,
    polymer_names,
    number_of_polymers,
):
    return (
        self.get_PHA_melt_dir(
            polymer_names,
            number_of_polymers,
        )
        / "simulations"
    )
```

</details>

<a id="definition-559"></a>

## `PHAFileManager.create_PHA_melt_simulation_run_dir`

Source lines 559–585. Named callable; inspect its callers before treating it as a stable public API.

```python
def create_PHA_melt_simulation_run_dir(self, polymer_names, number_of_polymers, timestamp=None): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| polymer_names | not annotated | required |
| number_of_polymers | not annotated | required |
| timestamp | not annotated | None |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `datetime.now`, `datetime.now().strftime`, `run_dir.mkdir`, `self.get_PHA_melt_simulations_dir`.

Explicit return expressions; different branches may return different objects:

```python
run_dir
```

Calls worth inspecting for I/O, state changes or delegated execution: `run_dir.mkdir`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def create_PHA_melt_simulation_run_dir(
    self,
    polymer_names,
    number_of_polymers,
    timestamp=None,
):
    from datetime import datetime

    if timestamp is None:
        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H%M%S"
        )

    run_dir = (
        self.get_PHA_melt_simulations_dir(
            polymer_names,
            number_of_polymers,
        )
        / timestamp
    )

    run_dir.mkdir(
        parents=True,
        exist_ok=False,
    )

    return run_dir
```

</details>

<a id="definition-587"></a>

## `PHAFileManager.create_named_PHA_melt_simulation_run_dir`

Source lines 587–624. Named callable; inspect its callers before treating it as a stable public API.

```python
def create_named_PHA_melt_simulation_run_dir(self, polymer_names, number_of_polymers, run_name): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| polymer_names | not annotated | required |
| number_of_polymers | not annotated | required |
| run_name | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `candidate_dir.exists`, `candidate_dir.mkdir`, `run_name.strip`, `run_name.strip().replace`, `self.get_PHA_melt_simulations_dir`, `simulations_dir.mkdir`.

Explicit return expressions; different branches may return different objects:

```python
candidate_dir
```

Calls worth inspecting for I/O, state changes or delegated execution: `candidate_dir.mkdir`, `simulations_dir.mkdir`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('run_name cannot be empty.')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def create_named_PHA_melt_simulation_run_dir(
    self,
    polymer_names,
    number_of_polymers,
    run_name,
):
    simulations_dir = self.get_PHA_melt_simulations_dir(
        polymer_names,
        number_of_polymers,
    )

    simulations_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    run_name = run_name.strip().replace(" ", "_")

    if not run_name:
        raise ValueError("run_name cannot be empty.")

    counter = 1

    while True:
        candidate_dir = (
            simulations_dir
            / f"{run_name}_{counter:02d}"
        )

        if not candidate_dir.exists():
            candidate_dir.mkdir(
                parents=True,
                exist_ok=False,
            )

            return candidate_dir

        counter += 1
```

</details>

<a id="definition-630"></a>

## `PHAFileManager.ensure_md_systems_csv_exists`

Source lines 630–655. Named callable; inspect its callers before treating it as a stable public API.

```python
def ensure_md_systems_csv_exists(self): ...
```

### Purpose and original contract

Create md_systems.csv if it does not already exist.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `csv.writer`, `open`, `self.md_systems_csv.exists`, `self.md_systems_csv.parent.mkdir`, `writer.writerow`.

Explicit return expressions; different branches may return different objects:

```python
self.md_systems_csv
```

Calls worth inspecting for I/O, state changes or delegated execution: `csv.writer`, `open`, `self.md_systems_csv.parent.mkdir`, `writer.writerow`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def ensure_md_systems_csv_exists(self):
    """
    Create md_systems.csv if it does not already exist.
    """

    header = [
        "system_name",
        "system_type",
        "number_of_atoms",
    ]

    if not self.md_systems_csv.exists():
        self.md_systems_csv.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            self.md_systems_csv,
            "w",
            newline="",
        ) as file:
            writer = csv.writer(file)
            writer.writerow(header)

    return self.md_systems_csv
```

</details>

<a id="definition-657"></a>

## `PHAFileManager.load_md_systems`

Source lines 657–675. Named callable; inspect its callers before treating it as a stable public API.

```python
def load_md_systems(self): ...
```

### Purpose and original contract

Load all registered molecular dynamics systems.

Returns
-------
list[dict]
    Rows from md_systems.csv.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `csv.DictReader`, `list`, `open`, `self.ensure_md_systems_csv_exists`.

Explicit return expressions; different branches may return different objects:

```python
list(reader)
```

Calls worth inspecting for I/O, state changes or delegated execution: `csv.DictReader`, `open`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def load_md_systems(self):
    """
    Load all registered molecular dynamics systems.

    Returns
    -------
    list[dict]
        Rows from md_systems.csv.
    """

    self.ensure_md_systems_csv_exists()

    with open(
        self.md_systems_csv,
        "r",
        newline="",
    ) as file:
        reader = csv.DictReader(file)
        return list(reader)
```

</details>

<a id="definition-677"></a>

## `PHAFileManager.get_md_system`

Source lines 677–705. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_md_system(self, system_name): ...
```

### Purpose and original contract

Return one registered MD system from md_systems.csv.

Parameters
----------
system_name : str
    Name of the registered system.

Returns
-------
dict
    Registry row for the requested system.

Raises
------
KeyError
    If the system is not registered.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| system_name | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `KeyError`, `self.load_md_systems`.

Explicit return expressions; different branches may return different objects:

```python
system
```

Calls worth inspecting for I/O, state changes or delegated execution: `self.load_md_systems`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
KeyError(f'MD system is not registered: {system_name}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_md_system(self, system_name):
    """
    Return one registered MD system from md_systems.csv.

    Parameters
    ----------
    system_name : str
        Name of the registered system.

    Returns
    -------
    dict
        Registry row for the requested system.

    Raises
    ------
    KeyError
        If the system is not registered.
    """

    systems = self.load_md_systems()

    for system in systems:
        if system["system_name"] == system_name:
            return system

    raise KeyError(
        f"MD system is not registered: {system_name}"
    )
```

</details>

<a id="definition-707"></a>

## `PHAFileManager.md_system_exists`

Source lines 707–717. Named callable; inspect its callers before treating it as a stable public API.

```python
def md_system_exists(self, system_name): ...
```

### Purpose and original contract

Check whether a molecular dynamics system is already registered.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| system_name | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `any`, `self.load_md_systems`.

Explicit return expressions; different branches may return different objects:

```python
any((row['system_name'] == system_name for row in systems))
```

Calls worth inspecting for I/O, state changes or delegated execution: `self.load_md_systems`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def md_system_exists(self, system_name):
    """
    Check whether a molecular dynamics system is already registered.
    """

    systems = self.load_md_systems()

    return any(
        row["system_name"] == system_name
        for row in systems
    )
```

</details>

<a id="definition-719"></a>

## `PHAFileManager.register_md_system`

Source lines 719–823. Named callable; inspect its callers before treating it as a stable public API.

```python
def register_md_system(self, system_name, system_type, number_of_atoms=None): ...
```

### Purpose and original contract

Add or update a system in md_systems.csv.

Parameters
----------
system_name : str
    Unique name of the prepared molecular dynamics system.

system_type : str
    Type of system, for example:

        dry
        solvated
        solvated_ions
        melt

number_of_atoms : int, optional
    Number of atoms in the system. If unavailable, the field is left
    blank.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| system_name | not annotated | required |
| system_type | not annotated | required |
| number_of_atoms | not annotated | None |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `csv.DictWriter`, `enumerate`, `int`, `isinstance`, `open`, `print`, `self.ensure_md_systems_csv_exists`, `self.load_md_systems`, `sorted`, `str`, `system_name.strip`, `systems.append`, `writer.writeheader`, `writer.writerows`.

Explicit return expressions; different branches may return different objects:

```python
new_row
```

Calls worth inspecting for I/O, state changes or delegated execution: `csv.DictWriter`, `open`, `self.load_md_systems`, `writer.writeheader`, `writer.writerows`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('system_name must be a non-empty string.')
ValueError(f'Unsupported system type: {system_type}\nAllowed values: {sorted(allowed_system_types)}')
ValueError('number_of_atoms must be greater than zero.')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def register_md_system(
    self,
    system_name,
    system_type,
    number_of_atoms=None,
):
    """
    Add or update a system in md_systems.csv.

    Parameters
    ----------
    system_name : str
        Unique name of the prepared molecular dynamics system.

    system_type : str
        Type of system, for example:

            dry
            solvated
            solvated_ions
            melt

    number_of_atoms : int, optional
        Number of atoms in the system. If unavailable, the field is left
        blank.
    """

    allowed_system_types = {
        "dry",
        "solvated",
        "solvated_ions",
        "melt",
    }

    if not isinstance(system_name, str) or not system_name.strip():
        raise ValueError(
            "system_name must be a non-empty string."
        )

    if system_type not in allowed_system_types:
        raise ValueError(
            f"Unsupported system type: {system_type}\n"
            f"Allowed values: {sorted(allowed_system_types)}"
        )

    if number_of_atoms is not None:
        number_of_atoms = int(number_of_atoms)

        if number_of_atoms <= 0:
            raise ValueError(
                "number_of_atoms must be greater than zero."
            )

    self.ensure_md_systems_csv_exists()

    systems = self.load_md_systems()

    new_row = {
        "system_name": system_name.strip(),
        "system_type": system_type,
        "number_of_atoms": (
            str(number_of_atoms)
            if number_of_atoms is not None
            else ""
        ),
    }

    system_updated = False

    for index, row in enumerate(systems):
        if row["system_name"] == system_name:
            systems[index] = new_row
            system_updated = True
            break

    if not system_updated:
        systems.append(new_row)

    with open(
        self.md_systems_csv,
        "w",
        newline="",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "system_name",
                "system_type",
                "number_of_atoms",
            ],
        )

        writer.writeheader()
        writer.writerows(systems)

    action = "Updated" if system_updated else "Registered"

    print(
        f"{action} MD system: "
        f"{system_name} "
        f"({system_type}, "
        f"{number_of_atoms or 'unknown'} atoms)"
    )

    return new_row
```

</details>

<a id="definition-825"></a>

## `PHAFileManager.get_md_system_files`

Source lines 825–912. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_md_system_files(self, system_name, system_type): ...
```

### Purpose and original contract

Return the main files and directories for a registered MD system.

Parameters
----------
system_name : str
    Full registered system name.

    Examples
    --------
    P3HB_10_dry
    P3HB_10_solvated
    P3HB_10_solvated_KCl_0_15
    25_P3HB_10_melt

system_type : str
    One of:

        dry
        solvated
        solvated_ions
        melt

Returns
-------
dict
    System directory, topology file, coordinate file, simulations
    directory, resuable workflow directory and input format.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| system_name | not annotated | required |
| system_type | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `sorted`.

Explicit return expressions; different branches may return different objects:

```python
{'system_name': system_name, 'system_type': system_type, 'system_dir': system_dir, 'topology_file': topology_file, 'coordinate_file': coordinate_file, 'simulations_dir': simulations_dir, 'workflows_dir': workflows_dir, 'topology_format': topology_format}
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError(f'Unsupported MD system type: {system_type}\nAllowed values: {sorted(allowed_system_types)}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_md_system_files(
    self,
    system_name,
    system_type,
):
    """
    Return the main files and directories for a registered MD system.

    Parameters
    ----------
    system_name : str
        Full registered system name.

        Examples
        --------
        P3HB_10_dry
        P3HB_10_solvated
        P3HB_10_solvated_KCl_0_15
        25_P3HB_10_melt

    system_type : str
        One of:

            dry
            solvated
            solvated_ions
            melt

    Returns
    -------
    dict
        System directory, topology file, coordinate file, simulations
        directory, resuable workflow directory and input format.
    """

    allowed_system_types = {
        "dry",
        "solvated",
        "solvated_ions",
        "melt",
    }

    if system_type not in allowed_system_types:
        raise ValueError(
            f"Unsupported MD system type: {system_type}\n"
            f"Allowed values: {sorted(allowed_system_types)}"
        )

    if system_type == "dry":
        system_dir = self.PHA_dry_dir / system_name
        topology_file = system_dir / f"{system_name}.prmtop"
        coordinate_file = system_dir / f"{system_name}.rst7"
        simulations_dir = system_dir / "simulations"
        topology_format = "amber"

    elif system_type == "solvated":
        system_dir = self.PHA_solvated_dir / system_name
        topology_file = system_dir / f"{system_name}.prmtop"
        coordinate_file = system_dir / f"{system_name}.rst7"
        simulations_dir = system_dir / "simulations"
        topology_format = "amber"

    elif system_type == "solvated_ions":
        system_dir = self.PHA_solvated_ions_dir / system_name
        topology_file = system_dir / f"{system_name}.prmtop"
        coordinate_file = system_dir / f"{system_name}.rst7"
        simulations_dir = system_dir / "simulations"
        topology_format = "amber"

    elif system_type == "melt":
        system_dir = self.PHA_melts_dir / system_name
        topology_file = system_dir / f"{system_name}.top"
        coordinate_file = system_dir / f"{system_name}.gro"
        simulations_dir = system_dir / "simulations"
        topology_format = "gromacs"

    workflows_dir = system_dir / "simulation_workflows"

    return {
        "system_name": system_name,
        "system_type": system_type,
        "system_dir": system_dir,
        "topology_file": topology_file,
        "coordinate_file": coordinate_file,
        "simulations_dir": simulations_dir,
        "workflows_dir": workflows_dir,
        "topology_format": topology_format,
    }
```

</details>

<a id="definition-918"></a>

## `PHAFileManager.get_md_system_workflows_dir`

Source lines 918–962. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_md_system_workflows_dir(self, system_name, system_type, create=False): ...
```

### Purpose and original contract

Return the reusable simulation-workflow directory for an MD system.

Parameters
----------
system_name : str
    Registered MD system name.

system_type : str
    Registered MD system type.

create : bool, optional
    If True, create the workflow directory if required.

Returns
-------
pathlib.Path
    Path to the system's simulation_workflows directory.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| system_name | not annotated | required |
| system_type | not annotated | required |
| create | not annotated | False |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.get_md_system_files`, `workflows_dir.mkdir`.

Explicit return expressions; different branches may return different objects:

```python
workflows_dir
```

Calls worth inspecting for I/O, state changes or delegated execution: `workflows_dir.mkdir`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_md_system_workflows_dir(
    self,
    system_name,
    system_type,
    create=False,
):
    """
    Return the reusable simulation-workflow directory for an MD system.

    Parameters
    ----------
    system_name : str
        Registered MD system name.

    system_type : str
        Registered MD system type.

    create : bool, optional
        If True, create the workflow directory if required.

    Returns
    -------
    pathlib.Path
        Path to the system's simulation_workflows directory.
    """

    system_files = self.get_md_system_files(
        system_name=system_name,
        system_type=system_type,
    )

    workflows_dir = (
        system_files[
            "workflows_dir"
        ]
    )

    if create:

        workflows_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    return workflows_dir
```

</details>

<a id="definition-964"></a>

## `PHAFileManager.get_md_system_workflow_path`

Source lines 964–1045. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_md_system_workflow_path(self, system_name, system_type, workflow_name, create_directory=False): ...
```

### Purpose and original contract

Return the standard JSON path for a reusable simulation workflow.

Parameters
----------
system_name : str
    Registered MD system name.

system_type : str
    Registered MD system type.

workflow_name : str
    Human-readable workflow name.

create_directory : bool, optional
    If True, create the simulation_workflows directory.

Returns
-------
pathlib.Path
    Path to the workflow JSON file.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| system_name | not annotated | required |
| system_type | not annotated | required |
| workflow_name | not annotated | required |
| create_directory | not annotated | False |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `isinstance`, `re.sub`, `self.get_md_system_workflows_dir`, `workflow_label.strip`, `workflow_name.strip`.

Explicit return expressions; different branches may return different objects:

```python
workflows_dir / f'{workflow_label}.workflow.json'
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('workflow_name must be a non-empty string.')
ValueError('workflow_name does not contain any valid filename characters.')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_md_system_workflow_path(
    self,
    system_name,
    system_type,
    workflow_name,
    create_directory=False,
):
    """
    Return the standard JSON path for a reusable simulation workflow.

    Parameters
    ----------
    system_name : str
        Registered MD system name.

    system_type : str
        Registered MD system type.

    workflow_name : str
        Human-readable workflow name.

    create_directory : bool, optional
        If True, create the simulation_workflows directory.

    Returns
    -------
    pathlib.Path
        Path to the workflow JSON file.
    """

    if (
        not isinstance(
            workflow_name,
            str,
        )
        or not workflow_name.strip()
    ):
        raise ValueError(
            "workflow_name must be a non-empty string."
        )


    workflow_label = (
        workflow_name
        .strip()
    )


    workflow_label = re.sub(
        r"[^A-Za-z0-9._-]+",
        "_",
        workflow_label,
    )


    workflow_label = (
        workflow_label
        .strip("._-")
    )


    if not workflow_label:

        raise ValueError(
            "workflow_name does not contain any "
            "valid filename characters."
        )


    workflows_dir = (
        self.get_md_system_workflows_dir(
            system_name=system_name,
            system_type=system_type,
            create=create_directory,
        )
    )


    return (
        workflows_dir
        / f"{workflow_label}.workflow.json"
    )
```

</details>

<a id="definition-1047"></a>

## `PHAFileManager.list_md_system_workflows`

Source lines 1047–1087. Named callable; inspect its callers before treating it as a stable public API.

```python
def list_md_system_workflows(self, system_name, system_type): ...
```

### Purpose and original contract

Return all saved reusable workflows for an MD system.

Parameters
----------
system_name : str
    Registered MD system name.

system_type : str
    Registered MD system type.

Returns
-------
list[pathlib.Path]
    Saved workflow JSON files, sorted by filename.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| system_name | not annotated | required |
| system_type | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.get_md_system_workflows_dir`, `sorted`, `workflows_dir.exists`, `workflows_dir.glob`.

Explicit return expressions; different branches may return different objects:

```python
[]
sorted(workflows_dir.glob('*.workflow.json'))
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def list_md_system_workflows(
    self,
    system_name,
    system_type,
):
    """
    Return all saved reusable workflows for an MD system.

    Parameters
    ----------
    system_name : str
        Registered MD system name.

    system_type : str
        Registered MD system type.

    Returns
    -------
    list[pathlib.Path]
        Saved workflow JSON files, sorted by filename.
    """

    workflows_dir = (
        self.get_md_system_workflows_dir(
            system_name=system_name,
            system_type=system_type,
            create=False,
        )
    )


    if not workflows_dir.exists():

        return []


    return sorted(
        workflows_dir.glob(
            "*.workflow.json"
        )
    )
```

</details>

<a id="definition-1089"></a>

## `PHAFileManager.create_named_md_system_simulation_run_dir`

Source lines 1089–1147. Named callable; inspect its callers before treating it as a stable public API.

```python
def create_named_md_system_simulation_run_dir(self, system_name, system_type, run_name): ...
```

### Purpose and original contract

Create a numbered simulation directory for any registered MD system.

Examples
--------
run_name="Test"

    Test_01
    Test_02
    Test_03

run_name="Tg"

    Tg_01
    Tg_02

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| system_name | not annotated | required |
| system_type | not annotated | required |
| run_name | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `candidate_dir.exists`, `candidate_dir.mkdir`, `run_name.strip`, `run_name.strip().replace`, `self.get_md_system_files`, `simulations_dir.mkdir`.

Explicit return expressions; different branches may return different objects:

```python
candidate_dir
```

Calls worth inspecting for I/O, state changes or delegated execution: `candidate_dir.mkdir`, `simulations_dir.mkdir`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError('run_name cannot be empty.')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def create_named_md_system_simulation_run_dir(
    self,
    system_name,
    system_type,
    run_name,
):
    """
    Create a numbered simulation directory for any registered MD system.

    Examples
    --------
    run_name="Test"

        Test_01
        Test_02
        Test_03

    run_name="Tg"

        Tg_01
        Tg_02
    """

    system_files = self.get_md_system_files(
        system_name=system_name,
        system_type=system_type,
    )

    simulations_dir = system_files["simulations_dir"]

    simulations_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    run_name = run_name.strip().replace(" ", "_")

    if not run_name:
        raise ValueError(
            "run_name cannot be empty."
        )

    counter = 1

    while True:
        candidate_dir = (
            simulations_dir
            / f"{run_name}_{counter:02d}"
        )

        if not candidate_dir.exists():
            candidate_dir.mkdir(
                parents=True,
                exist_ok=False,
            )

            return candidate_dir

        counter += 1
```

</details>

<a id="definition-1149"></a>

## `PHAFileManager.validate_md_system_files`

Source lines 1149–1183. Named callable; inspect its callers before treating it as a stable public API.

```python
def validate_md_system_files(self, system_name, system_type): ...
```

### Purpose and original contract

Check that the topology and coordinate files exist.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| system_name | not annotated | required |
| system_type | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `'\n'.join`, `FileNotFoundError`, `file_path.exists`, `missing_files.append`, `self.get_md_system_files`, `str`.

Explicit return expressions; different branches may return different objects:

```python
system_files
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
FileNotFoundError('Missing MD system files:\n' + '\n'.join((str(path) for path in missing_files)))
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def validate_md_system_files(
    self,
    system_name,
    system_type,
):
    """
    Check that the topology and coordinate files exist.
    """

    system_files = self.get_md_system_files(
        system_name=system_name,
        system_type=system_type,
    )

    missing_files = []

    for key in [
        "topology_file",
        "coordinate_file",
    ]:
        file_path = system_files[key]

        if not file_path.exists():
            missing_files.append(file_path)

    if missing_files:
        raise FileNotFoundError(
            "Missing MD system files:\n"
            + "\n".join(
                str(path)
                for path in missing_files
            )
        )

    return system_files
```

</details>

<a id="definition-1189"></a>

## `PHAFileManager.find_file`

Source lines 1189–1199. Named callable; inspect its callers before treating it as a stable public API.

```python
def find_file(self, directory, extension): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| directory | not annotated | required |
| extension | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `Path`, `directory.glob`, `sorted`.

Explicit return expressions; different branches may return different objects:

```python
None
files[0]
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def find_file(self, directory, extension):
    directory = Path(directory)

    files = sorted(
        directory.glob(f"*.{extension}")
    )

    if not files:
        return None

    return files[0]
```

</details>

<a id="definition-1201"></a>

## `PHAFileManager.find_files`

Source lines 1201–1206. Named callable; inspect its callers before treating it as a stable public API.

```python
def find_files(self, directory, extension): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| directory | not annotated | required |
| extension | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `Path`, `directory.glob`, `sorted`.

Explicit return expressions; different branches may return different objects:

```python
sorted(directory.glob(f'*.{extension}'))
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def find_files(self, directory, extension):
    directory = Path(directory)

    return sorted(
        directory.glob(f"*.{extension}")
    )
```

</details>

<a id="definition-1208"></a>

## `PHAFileManager.count_atoms_from_amber_topology`

Source lines 1208–1224. Named callable; inspect its callers before treating it as a stable public API.

```python
def count_atoms_from_amber_topology(self, prmtop_path): ...
```

### Purpose and original contract

Return the number of atoms stored in an Amber topology.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| prmtop_path | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `FileNotFoundError`, `Path`, `len`, `pmd.load_file`, `prmtop_path.exists`, `str`.

Explicit return expressions; different branches may return different objects:

```python
len(structure.atoms)
```

Calls worth inspecting for I/O, state changes or delegated execution: `pmd.load_file`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
FileNotFoundError(f'Amber topology file not found:\n{prmtop_path}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def count_atoms_from_amber_topology(self, prmtop_path):
    """
    Return the number of atoms stored in an Amber topology.
    """

    prmtop_path = Path(prmtop_path)

    if not prmtop_path.exists():
        raise FileNotFoundError(
            f"Amber topology file not found:\n{prmtop_path}"
            )

    structure = pmd.load_file(
        str(prmtop_path)
        )

    return len(structure.atoms)
```

</details>

<a id="definition-1226"></a>

## `PHAFileManager.count_atoms_from_gromacs_gro`

Source lines 1226–1285. Named callable; inspect its callers before treating it as a stable public API.

```python
def count_atoms_from_gromacs_gro(self, gro_path): ...
```

### Purpose and original contract

Count atoms in a GROMACS GRO coordinate file.

The second line of a GRO file contains the total number of atoms.

Parameters
----------
gro_path : str or pathlib.Path
    Path to the GROMACS GRO coordinate file.

Returns
-------
int
    Number of atoms in the system.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| gro_path | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `FileNotFoundError`, `Path`, `ValueError`, `atom_count_line.strip`, `file.readline`, `gro_path.exists`, `int`, `open`, `print`.

Explicit return expressions; different branches may return different objects:

```python
number_of_atoms
```

Calls worth inspecting for I/O, state changes or delegated execution: `file.readline`, `open`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
FileNotFoundError(f'GROMACS coordinate file not found:\n{gro_path}')
ValueError(f'GROMACS GRO file is incomplete:\n{gro_path}')
ValueError(f'Could not read the atom count from the second line of:\n{gro_path}')
ValueError(f'Invalid atom count in GRO file: {number_of_atoms}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def count_atoms_from_gromacs_gro(
    self,
    gro_path,
):
    """
    Count atoms in a GROMACS GRO coordinate file.

    The second line of a GRO file contains the total number of atoms.

    Parameters
    ----------
    gro_path : str or pathlib.Path
        Path to the GROMACS GRO coordinate file.

    Returns
    -------
    int
        Number of atoms in the system.
    """

    gro_path = Path(gro_path)

    if not gro_path.exists():
        raise FileNotFoundError(
            f"GROMACS coordinate file not found:\n{gro_path}"
        )

    with open(
        gro_path,
        "r",
        encoding="utf-8",
        errors="replace",
    ) as file:
        title_line = file.readline()
        atom_count_line = file.readline()

    if not title_line or not atom_count_line:
        raise ValueError(
            f"GROMACS GRO file is incomplete:\n{gro_path}"
        )

    try:
        number_of_atoms = int(
            atom_count_line.strip()
        )

    except ValueError as error:
        raise ValueError(
            "Could not read the atom count from the second "
            f"line of:\n{gro_path}"
        ) from error

    if number_of_atoms <= 0:
        raise ValueError(
            f"Invalid atom count in GRO file: {number_of_atoms}"
        )

    print(f"Number of atoms: {number_of_atoms}")

    return number_of_atoms
```

</details>

<a id="definition-1311"></a>

## `PHAResidueCodeManager.__init__`

Source lines 1311–1322. Internal helper/protocol method.

```python
def __init__(self, paths): ...
```

### Purpose and original contract

Initialise the residue code manager.

Parameters
----------
paths : PHAFileManager
    Filepath manager instance.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| paths | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self._ensure_csv_exists`, `self.paths.get_residue_codes_csv`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Instance/class attributes assigned directly: `self.csv_path`, `self.paths`.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def __init__(self, paths):
    """
    Initialise the residue code manager.

    Parameters
    ----------
    paths : PHAFileManager
        Filepath manager instance.
    """
    self.paths = paths
    self.csv_path = self.paths.get_residue_codes_csv()
    self._ensure_csv_exists()
```

</details>

<a id="definition-1324"></a>

## `PHAResidueCodeManager._ensure_csv_exists`

Source lines 1324–1332. Internal helper/protocol method.

```python
def _ensure_csv_exists(self): ...
```

### Purpose and original contract

Create residue_codes.csv if it does not already exist.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `csv.writer`, `open`, `self.csv_path.exists`, `self.csv_path.parent.mkdir`, `writer.writerow`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Calls worth inspecting for I/O, state changes or delegated execution: `csv.writer`, `open`, `self.csv_path.parent.mkdir`, `writer.writerow`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def _ensure_csv_exists(self):
    """
    Create residue_codes.csv if it does not already exist.
    """
    if not self.csv_path.exists():
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.header)
```

</details>

<a id="definition-1334"></a>

## `PHAResidueCodeManager.load_rows`

Source lines 1334–1345. Named callable; inspect its callers before treating it as a stable public API.

```python
def load_rows(self): ...
```

### Purpose and original contract

Load all rows from residue_codes.csv.

Returns
-------
list[dict]
    List of CSV entries.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `csv.DictReader`, `list`, `open`.

Explicit return expressions; different branches may return different objects:

```python
list(reader)
```

Calls worth inspecting for I/O, state changes or delegated execution: `csv.DictReader`, `open`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def load_rows(self):
    """
    Load all rows from residue_codes.csv.

    Returns
    -------
    list[dict]
        List of CSV entries.
    """
    with open(self.csv_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)
```

</details>

<a id="definition-1347"></a>

## `PHAResidueCodeManager.get_used_codes`

Source lines 1347–1357. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_used_codes(self): ...
```

### Purpose and original contract

Return all residue codes currently stored in the CSV.

Returns
-------
set
    Set of used residue codes.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.load_rows`.

Explicit return expressions; different branches may return different objects:

```python
{row['residue_code'] for row in rows}
```

Calls worth inspecting for I/O, state changes or delegated execution: `self.load_rows`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_used_codes(self):
    """
    Return all residue codes currently stored in the CSV.

    Returns
    -------
    set
        Set of used residue codes.
    """
    rows = self.load_rows()
    return {row['residue_code'] for row in rows}
```

</details>

<a id="definition-1359"></a>

## `PHAResidueCodeManager.PHA_type_exists`

Source lines 1359–1372. Named callable; inspect its callers before treating it as a stable public API.

```python
def PHA_type_exists(self, PHA_type): ...
```

### Purpose and original contract

Check whether a PHA type has already been registered.

Parameters
----------
PHA_type : str

Returns
-------
bool

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| PHA_type | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `any`, `self.load_rows`.

Explicit return expressions; different branches may return different objects:

```python
any((row['PHA_type'] == PHA_type for row in rows))
```

Calls worth inspecting for I/O, state changes or delegated execution: `self.load_rows`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def PHA_type_exists(self, PHA_type):
    """
    Check whether a PHA type has already been registered.

    Parameters
    ----------
    PHA_type : str

    Returns
    -------
    bool
    """
    rows = self.load_rows()
    return any((row['PHA_type'] == PHA_type for row in rows))
```

</details>

<a id="definition-1374"></a>

## `PHAResidueCodeManager.get_code`

Source lines 1374–1398. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_code(self, PHA_type, component): ...
```

### Purpose and original contract

Return the residue code for a given PHA component.

Parameters
----------
PHA_type : str

component : str
    One of:

        trimer
        head
        mainchain
        tail

Returns
-------
str or None

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| PHA_type | not annotated | required |
| component | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `self.load_rows`.

Explicit return expressions; different branches may return different objects:

```python
row['residue_code']
None
```

Calls worth inspecting for I/O, state changes or delegated execution: `self.load_rows`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def get_code(self, PHA_type, component):
    """
    Return the residue code for a given PHA component.

    Parameters
    ----------
    PHA_type : str

    component : str
        One of:

            trimer
            head
            mainchain
            tail

    Returns
    -------
    str or None
    """
    rows = self.load_rows()
    for row in rows:
        if row['PHA_type'] == PHA_type and row['component'] == component:
            return row['residue_code']
    return None
```

</details>

<a id="definition-1400"></a>

## `PHAResidueCodeManager.generate_unique_codes`

Source lines 1400–1442. Named callable; inspect its callers before treating it as a stable public API.

```python
def generate_unique_codes(self, number_of_codes): ...
```

### Purpose and original contract

Generate multiple unique residue codes.

Examples
--------

Existing CSV:

    AAA
    AAB

generate_unique_codes(4)

Returns:

    AAC
    AAD
    AAE
    AAF

Parameters
----------
number_of_codes : int

Returns
-------
list[str]

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| number_of_codes | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `''.join`, `RuntimeError`, `itertools.product`, `len`, `new_codes.append`, `self.get_used_codes`.

Explicit return expressions; different branches may return different objects:

```python
new_codes
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
RuntimeError(f'Could not generate {number_of_codes} unique residue codes.')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def generate_unique_codes(self, number_of_codes):
    """
    Generate multiple unique residue codes.

    Examples
    --------

    Existing CSV:

        AAA
        AAB

    generate_unique_codes(4)

    Returns:

        AAC
        AAD
        AAE
        AAF

    Parameters
    ----------
    number_of_codes : int

    Returns
    -------
    list[str]
    """
    used_codes = self.get_used_codes()
    new_codes = []
    for letters in itertools.product('ABCDEFGHIJKLMNOPQRSTUVWXYZ', repeat=3):
        code = ''.join(letters)
        if code in used_codes:
            continue
        if code in new_codes:
            continue
        if code in self.forbidden_codes:
            continue
        new_codes.append(code)
        if len(new_codes) == number_of_codes:
            return new_codes
    raise RuntimeError(f'Could not generate {number_of_codes} unique residue codes.')
```

</details>

<a id="definition-1444"></a>

## `PHAResidueCodeManager.register_PHA_type`

Source lines 1444–1488. Named callable; inspect its callers before treating it as a stable public API.

```python
def register_PHA_type(self, PHA_type, trimer_name, trimer_smiles, monomer_smiles): ...
```

### Purpose and original contract

Register a new PHA type.

Creates four residue entries:

    trimer
    head
    mainchain
    tail

Example
-------

PHA_type = "3HB"

trimer_name = "P3HB_3"

Generates:

    AAA  trimer
    AAB  head
    AAC  mainchain
    AAD  tail

Parameters
----------
PHA_type : str

trimer_name : str

trimer_smiles : str

monomer_smiles : str

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| PHA_type | not annotated | required |
| trimer_name | not annotated | required |
| trimer_smiles | not annotated | required |
| monomer_smiles | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `csv.DictWriter`, `open`, `print`, `self.PHA_type_exists`, `self.generate_unique_codes`, `writer.writerow`.

Explicit return expressions; different branches may return different objects:

```python
None
```

Calls worth inspecting for I/O, state changes or delegated execution: `csv.DictWriter`, `open`, `writer.writerow`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def register_PHA_type(self, PHA_type, trimer_name, trimer_smiles, monomer_smiles):
    """
    Register a new PHA type.

    Creates four residue entries:

        trimer
        head
        mainchain
        tail

    Example
    -------

    PHA_type = "3HB"

    trimer_name = "P3HB_3"

    Generates:

        AAA  trimer
        AAB  head
        AAC  mainchain
        AAD  tail

    Parameters
    ----------
    PHA_type : str

    trimer_name : str

    trimer_smiles : str

    monomer_smiles : str
    """
    if self.PHA_type_exists(PHA_type):
        print(f'PHA type {PHA_type} already exists in residue code CSV.')
        return
    trimer_code, head_code, mainchain_code, tail_code = self.generate_unique_codes(4)
    entries = [{'PHA_type': PHA_type, 'component': 'trimer', 'readable_name': trimer_name, 'residue_code': trimer_code, 'smiles': trimer_smiles}, {'PHA_type': PHA_type, 'component': 'head', 'readable_name': f'hP{PHA_type}', 'residue_code': head_code, 'smiles': monomer_smiles}, {'PHA_type': PHA_type, 'component': 'mainchain', 'readable_name': f'mP{PHA_type}', 'residue_code': mainchain_code, 'smiles': monomer_smiles}, {'PHA_type': PHA_type, 'component': 'tail', 'readable_name': f'tP{PHA_type}', 'residue_code': tail_code, 'smiles': monomer_smiles}]
    with open(self.csv_path, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=self.header)
        for entry in entries:
            writer.writerow(entry)
    print(f'Registered residue codes for {PHA_type}.')
```

</details>
