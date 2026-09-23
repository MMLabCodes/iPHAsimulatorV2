# pha_melt_builder.py

Resolve built polymers, ensure GROMACS representations through ACPYPE, assemble Polyply input and generate packed coordinates. The included topology can retain a one-molecule entry in addition to the outer requested count; existing 25-chain-labelled data contain 26 chains. Verify actual composition. The optional simulation helper is separate from packing.

[Current source](../../src/iphasimulator/pha_melt_builder.py)

This page is generated from source syntax. Original docstrings can be incomplete or outdated; module notes above identify known discrepancies. Call/return/error lists describe direct syntax, not all behaviour inside callees. Read the source excerpt for branch order and effects. No scientific execution is implied.

Explicit functions/methods/nested helpers: **14**.

## Module imports

```python
import re
import shutil
import subprocess
from pathlib import Path
from src.iphasimulator.pha_filepath_manager import PHAFileManager
from src.iphasimulator.build_pha import PHAPolymerBuilder
```

## Classes and result records

### `PHAMeltBuilder`

Build amorphous PHA melt systems.

## Function map

- [`PHAMeltBuilder.__init__` — source line 37](#definition-37)
- [`PHAMeltBuilder.run_command` — source line 41](#definition-41)
- [`PHAMeltBuilder.parse_polymer_name` — source line 71](#definition-71)
- [`PHAMeltBuilder.get_melt_name` — source line 82](#definition-82)
- [`PHAMeltBuilder.validate_melt_inputs` — source line 95](#definition-95)
- [`PHAMeltBuilder.ensure_built_polymer_exists` — source line 120](#definition-120)
- [`PHAMeltBuilder.ensure_gromacs_polymer_exists` — source line 163](#definition-163)
- [`PHAMeltBuilder.generate_polymer_melt` — source line 204](#definition-204)
- [`PHAMeltBuilder.run_acpype` — source line 291](#definition-291)
- [`PHAMeltBuilder.prepare_polyply_inputs` — source line 420](#definition-420)
- [`PHAMeltBuilder.run_polyply` — source line 503](#definition-503)
- [`PHAMeltBuilder.combine_itps` — source line 568](#definition-568)
- [`PHAMeltBuilder.edit_acpype_topology_for_polyply` — source line 612](#definition-612)
- [`PHAMeltBuilder.test_polymer_melt_simulation` — source line 671](#definition-671)

<a id="definition-37"></a>

## `PHAMeltBuilder.__init__`

Source lines 37–39. Internal helper/protocol method.

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

Direct calls (sorted inventory, not execution order): `PHAFileManager`, `PHAPolymerBuilder`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Instance/class attributes assigned directly: `self.paths`, `self.polymer_builder`.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def __init__(self, root_dir="structure_database"):
    self.paths = PHAFileManager(root_dir)
    self.polymer_builder = PHAPolymerBuilder(root_dir)
```

</details>

<a id="definition-41"></a>

## `PHAMeltBuilder.run_command`

Source lines 41–69. Named callable; inspect its callers before treating it as a stable public API.

```python
def run_command(self, command, workdir=None): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| command | not annotated | required |
| workdir | not annotated | None |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `RuntimeError`, `print`, `subprocess.run`.

Explicit return expressions; different branches may return different objects:

```python
result
```

Calls worth inspecting for I/O, state changes or delegated execution: `subprocess.run`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
RuntimeError(f'Command failed:\n{command}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def run_command(self, command, workdir=None):
    print("\nRunning command:")
    print(command)

    result = subprocess.run(
        command,
        shell=True,
        cwd=workdir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    print("Return code:", result.returncode)

    if result.stdout:
        print("STDOUT:")
        print(result.stdout)

    if result.stderr:
        print("STDERR:")
        print(result.stderr)

    if result.returncode != 0:
        raise RuntimeError(f"Command failed:\n{command}")

    return result
```

</details>

<a id="definition-71"></a>

## `PHAMeltBuilder.parse_polymer_name`

Source lines 71–80. Named callable; inspect its callers before treating it as a stable public API.

```python
def parse_polymer_name(self, polymer_name): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| polymer_name | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `ValueError`, `int`, `match.group`, `re.fullmatch`.

Explicit return expressions; different branches may return different objects:

```python
(match.group(1), int(match.group(2)))
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
def parse_polymer_name(self, polymer_name):
    match = re.fullmatch(r"P(.+)_(\d+)", polymer_name)

    if match is None:
        raise ValueError(
            f"Invalid polymer name: {polymer_name}\n"
            f"Expected format like: P3HB_10"
        )

    return match.group(1), int(match.group(2))
```

</details>

<a id="definition-82"></a>

## `PHAMeltBuilder.get_melt_name`

Source lines 82–93. Named callable; inspect its callers before treating it as a stable public API.

```python
def get_melt_name(self, polymer_names, number_of_polymers): ...
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

Direct calls (sorted inventory, not execution order): `'_'.join`, `ValueError`, `len`, `zip`.

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
def get_melt_name(self, polymer_names, number_of_polymers):
    if len(polymer_names) != len(number_of_polymers):
        raise ValueError(
            "polymer_names and number_of_polymers must have the same length."
        )

    name_parts = [
        f"{number}_{polymer_name}"
        for polymer_name, number in zip(polymer_names, number_of_polymers)
    ]

    return "_".join(name_parts) + "_melt"
```

</details>

<a id="definition-95"></a>

## `PHAMeltBuilder.validate_melt_inputs`

Source lines 95–118. Named callable; inspect its callers before treating it as a stable public API.

```python
def validate_melt_inputs(self, polymer_names, number_of_polymers): ...
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

Direct calls (sorted inventory, not execution order): `TypeError`, `ValueError`, `isinstance`, `len`, `self.parse_polymer_name`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
TypeError('polymer_names must be a list.')
TypeError('number_of_polymers must be a list.')
ValueError('polymer_names cannot be empty.')
ValueError('polymer_names and number_of_polymers must have the same length.')
TypeError('All polymer counts must be integers.')
ValueError('All polymer counts must be greater than zero.')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def validate_melt_inputs(self, polymer_names, number_of_polymers):
    if not isinstance(polymer_names, list):
        raise TypeError("polymer_names must be a list.")

    if not isinstance(number_of_polymers, list):
        raise TypeError("number_of_polymers must be a list.")

    if len(polymer_names) == 0:
        raise ValueError("polymer_names cannot be empty.")

    if len(polymer_names) != len(number_of_polymers):
        raise ValueError(
            "polymer_names and number_of_polymers must have the same length."
        )

    for polymer_name in polymer_names:
        self.parse_polymer_name(polymer_name)

    for number in number_of_polymers:
        if not isinstance(number, int):
            raise TypeError("All polymer counts must be integers.")

        if number <= 0:
            raise ValueError("All polymer counts must be greater than zero.")
```

</details>

<a id="definition-120"></a>

## `PHAMeltBuilder.ensure_built_polymer_exists`

Source lines 120–161. Named callable; inspect its callers before treating it as a stable public API.

```python
def ensure_built_polymer_exists(self, polymer_name): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| polymer_name | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `FileNotFoundError`, `pdb.exists`, `print`, `prmtop.exists`, `rst7.exists`, `self.parse_polymer_name`, `self.paths.get_built_PHA_amber_dir`, `self.polymer_builder.build_PHA_polymer`.

Explicit return expressions; different branches may return different objects:

```python
{'PHA_type': PHA_type, 'length': length, 'prmtop': prmtop, 'rst7': rst7, 'pdb': pdb}
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
FileNotFoundError(f'Failed to locate built polymer files for {polymer_name}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def ensure_built_polymer_exists(self, polymer_name):
    PHA_type, length = self.parse_polymer_name(polymer_name)

    amber_dir = self.paths.get_built_PHA_amber_dir(
        PHA_type,
        length,
    )

    prmtop = amber_dir / f"{polymer_name}.prmtop"
    rst7 = amber_dir / f"{polymer_name}.rst7"
    pdb = amber_dir / f"{polymer_name}.pdb"

    if prmtop.exists() and rst7.exists() and pdb.exists():
        print(f"Built polymer already exists: {polymer_name}")

        return {
            "PHA_type": PHA_type,
            "length": length,
            "prmtop": prmtop,
            "rst7": rst7,
            "pdb": pdb,
        }

    print(f"Built polymer missing. Building: {polymer_name}")

    self.polymer_builder.build_PHA_polymer(
        PHA_type=PHA_type,
        length=length,
    )

    if not prmtop.exists() or not rst7.exists() or not pdb.exists():
        raise FileNotFoundError(
            f"Failed to locate built polymer files for {polymer_name}"
        )

    return {
        "PHA_type": PHA_type,
        "length": length,
        "prmtop": prmtop,
        "rst7": rst7,
        "pdb": pdb,
    }
```

</details>

<a id="definition-163"></a>

## `PHAMeltBuilder.ensure_gromacs_polymer_exists`

Source lines 163–202. Named callable; inspect its callers before treating it as a stable public API.

```python
def ensure_gromacs_polymer_exists(self, polymer_name): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| polymer_name | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `expected_gro.exists`, `expected_top.exists`, `gromacs_dir.glob`, `gromacs_dir.mkdir`, `print`, `self.ensure_built_polymer_exists`, `self.parse_polymer_name`, `self.paths.get_built_PHA_gromacs_dir`, `self.run_acpype`, `sorted`.

Explicit return expressions; different branches may return different objects:

```python
{'gro': expected_gro, 'top': expected_top, 'itp_files': existing_itp_files}
{'gro': acpype_result['gro'], 'top': acpype_result['top'], 'itp_files': acpype_result['itp_files']}
```

Calls worth inspecting for I/O, state changes or delegated execution: `gromacs_dir.mkdir`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def ensure_gromacs_polymer_exists(self, polymer_name):
    PHA_type, length = self.parse_polymer_name(polymer_name)

    gromacs_dir = self.paths.get_built_PHA_gromacs_dir(
        PHA_type,
        length,
    )

    gromacs_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    expected_gro = gromacs_dir / f"{polymer_name}.gro"
    expected_top = gromacs_dir / f"{polymer_name}.top"
    existing_itp_files = sorted(gromacs_dir.glob("*.itp"))

    if expected_gro.exists() and expected_top.exists():
        print(f"GROMACS files already exist: {polymer_name}")

        return {
            "gro": expected_gro,
            "top": expected_top,
            "itp_files": existing_itp_files,
        }

    self.ensure_built_polymer_exists(polymer_name)

    print(
        f"GROMACS files missing for {polymer_name}. "
        f"Running ACPYPE conversion."
    )

    acpype_result = self.run_acpype(polymer_name)

    return {
        "gro": acpype_result["gro"],
        "top": acpype_result["top"],
        "itp_files": acpype_result["itp_files"],
    }
```

</details>

<a id="definition-204"></a>

## `PHAMeltBuilder.generate_polymer_melt`

Source lines 204–289. Named callable; inspect its callers before treating it as a stable public API.

```python
def generate_polymer_melt(self, polymer_names, number_of_polymers, density=750): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| polymer_names | not annotated | required |
| number_of_polymers | not annotated | required |
| density | not annotated | 750 |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `print`, `self.ensure_gromacs_polymer_exists`, `self.get_melt_name`, `self.paths.count_atoms_from_gromacs_gro`, `self.paths.create_PHA_melt_dir`, `self.paths.get_PHA_melt_inputs_dir`, `self.paths.get_PHA_melt_simulations_dir`, `self.paths.register_md_system`, `self.run_polyply`, `self.validate_melt_inputs`.

Explicit return expressions; different branches may return different objects:

```python
{'melt_name': melt_name, 'system_type': 'melt', 'melt_dir': melt_dir, 'inputs_dir': inputs_dir, 'simulations_dir': simulations_dir, 'topology_file': polyply_result['top'], 'coordinate_file': polyply_result['gro'], 'itp_file': polyply_result['itp'], 'polymer_names': polymer_names, 'number_of_polymers': number_of_polymers, 'density': density, 'number_of_atoms': number_of_atoms, 'polymer_gromacs_file … [full expression below]
```

Calls worth inspecting for I/O, state changes or delegated execution: `self.paths.register_md_system`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def generate_polymer_melt(
    self,
    polymer_names,
    number_of_polymers,
    density=750,
):
    self.validate_melt_inputs(
        polymer_names,
        number_of_polymers,
    )

    melt_name = self.get_melt_name(
        polymer_names,
        number_of_polymers,
    )

    melt_dir = self.paths.create_PHA_melt_dir(
        polymer_names,
        number_of_polymers,
    )

    inputs_dir = self.paths.get_PHA_melt_inputs_dir(
        polymer_names,
        number_of_polymers,
    )

    simulations_dir = self.paths.get_PHA_melt_simulations_dir(
        polymer_names,
        number_of_polymers,
    )

    polymer_gromacs_files = {}

    for polymer_name in polymer_names:
        polymer_gromacs_files[polymer_name] = (
            self.ensure_gromacs_polymer_exists(polymer_name)
        )

    print("\nPolymer melt setup complete.")
    print("Melt name:       ", melt_name)
    print("Melt dir:        ", melt_dir)
    print("Inputs dir:      ", inputs_dir)
    print("Simulations dir: ", simulations_dir)
    print("Density:         ", density)

    polyply_result = self.run_polyply(
        polymer_names=polymer_names,
        number_of_polymers=number_of_polymers,
        polymer_gromacs_files=polymer_gromacs_files,
        melt_dir=melt_dir,
        melt_name=melt_name,
        density=density,
    )

    number_of_atoms = self.paths.count_atoms_from_gromacs_gro(
        polyply_result["gro"]
    )

    self.paths.register_md_system(
        system_name=melt_name,
        system_type="melt",
        number_of_atoms=number_of_atoms,
    )

    print("\nPolymer melt generation complete.")
    print("Melt name:       ", melt_name)
    print("Melt dir:        ", melt_dir)
    print("Density:         ", density)
    print("Number of atoms: ", number_of_atoms)

    return {
        "melt_name": melt_name,
        "system_type": "melt",
        "melt_dir": melt_dir,
        "inputs_dir": inputs_dir,
        "simulations_dir": simulations_dir,
        "topology_file": polyply_result["top"],
        "coordinate_file": polyply_result["gro"],
        "itp_file": polyply_result["itp"],
        "polymer_names": polymer_names,
        "number_of_polymers": number_of_polymers,
        "density": density,
        "number_of_atoms": number_of_atoms,
        "polymer_gromacs_files": polymer_gromacs_files,
        "polyply_result": polyply_result,
    }
```

</details>

<a id="definition-291"></a>

## `PHAMeltBuilder.run_acpype`

Source lines 291–418. Named callable; inspect its callers before treating it as a stable public API.

```python
def run_acpype(self, polymer_name): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| polymer_name | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `FileNotFoundError`, `acpype_output_dir.exists`, `acpype_output_dir.glob`, `acpype_workdir.exists`, `acpype_workdir.mkdir`, `final_itp_files.append`, `generated_gro.exists`, `generated_top.exists`, `gromacs_dir.mkdir`, `print`, `prmtop_file.exists`, `rst7_file.exists`, `self.edit_acpype_topology_for_polyply`, `self.parse_polymer_name`, `self.paths.get_built_PHA_amber_dir`, `self.paths.get_built_PHA_amber_dir(PHA_type, length).resolve`, `self.paths.get_built_PHA_gromacs_dir`, `self.paths.get_built_PHA_gromacs_dir(PHA_type, length).resolve`, `self.paths.get_temp_dir`, `self.paths.get_temp_dir().resolve`, `self.run_command`, `shutil.copyfile`, `shutil.rmtree`, `sorted`, `temp_dir.mkdir`.

Explicit return expressions; different branches may return different objects:

```python
{'polymer_name': polymer_name, 'gro': final_gro, 'top': final_top, 'itp_files': final_itp_files, 'acpype_workdir': acpype_workdir, 'acpype_output_dir': acpype_output_dir}
```

Calls worth inspecting for I/O, state changes or delegated execution: `acpype_workdir.mkdir`, `gromacs_dir.mkdir`, `self.run_command`, `shutil.copyfile`, `temp_dir.mkdir`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
FileNotFoundError(f'Amber topology file not found:\n{prmtop_file}')
FileNotFoundError(f'Amber coordinate file not found:\n{rst7_file}')
FileNotFoundError(f'ACPYPE output directory not found:\n{acpype_output_dir}')
FileNotFoundError(f'Expected ACPYPE GRO file not found:\n{generated_gro}')
FileNotFoundError(f'Expected ACPYPE TOP file not found:\n{generated_top}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def run_acpype(self, polymer_name):
    PHA_type, length = self.parse_polymer_name(polymer_name)

    amber_dir = self.paths.get_built_PHA_amber_dir(
        PHA_type,
        length,
    ).resolve()

    gromacs_dir = self.paths.get_built_PHA_gromacs_dir(
        PHA_type,
        length,
    ).resolve()

    temp_dir = self.paths.get_temp_dir().resolve()

    gromacs_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    temp_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    prmtop_file = amber_dir / f"{polymer_name}.prmtop"
    rst7_file = amber_dir / f"{polymer_name}.rst7"

    if not prmtop_file.exists():
        raise FileNotFoundError(
            f"Amber topology file not found:\n{prmtop_file}"
        )

    if not rst7_file.exists():
        raise FileNotFoundError(
            f"Amber coordinate file not found:\n{rst7_file}"
        )

    acpype_workdir = temp_dir / f"{polymer_name}_acpype"

    if acpype_workdir.exists():
        shutil.rmtree(acpype_workdir)

    acpype_workdir.mkdir(
        parents=True,
        exist_ok=True,
    )

    temp_prmtop = acpype_workdir / prmtop_file.name
    temp_rst7 = acpype_workdir / rst7_file.name

    shutil.copyfile(prmtop_file, temp_prmtop)
    shutil.copyfile(rst7_file, temp_rst7)

    acpype_command = (
        f"acpype "
        f"-p {temp_prmtop.name} "
        f"-x {temp_rst7.name} "
        f"-b {polymer_name}"
    )

    self.run_command(
        acpype_command,
        workdir=acpype_workdir,
    )

    acpype_output_dir = acpype_workdir / f"{polymer_name}.amb2gmx"

    if not acpype_output_dir.exists():
        raise FileNotFoundError(
            f"ACPYPE output directory not found:\n{acpype_output_dir}"
        )

    generated_gro = acpype_output_dir / f"{polymer_name}_GMX.gro"
    generated_top = acpype_output_dir / f"{polymer_name}_GMX.top"

    if not generated_gro.exists():
        raise FileNotFoundError(
            f"Expected ACPYPE GRO file not found:\n{generated_gro}"
        )

    if not generated_top.exists():
        raise FileNotFoundError(
            f"Expected ACPYPE TOP file not found:\n{generated_top}"
        )

    generated_itp_files = sorted(acpype_output_dir.glob("*.itp"))

    final_gro = gromacs_dir / f"{polymer_name}.gro"
    final_top = gromacs_dir / f"{polymer_name}.top"

    shutil.copyfile(generated_gro, final_gro)
    shutil.copyfile(generated_top, final_top)

    self.edit_acpype_topology_for_polyply(final_top)

    final_itp_files = []

    for generated_itp in generated_itp_files:
        final_itp = gromacs_dir / generated_itp.name

        shutil.copyfile(
            generated_itp,
            final_itp,
        )

        final_itp_files.append(final_itp)

    print("\nACPYPE conversion complete.")
    print("Polymer name: ", polymer_name)
    print("GRO:          ", final_gro)
    print("TOP:          ", final_top)

    if final_itp_files:
        print("ITP files:")
        for file_path in final_itp_files:
            print("  ", file_path)
    else:
        print("ITP files:    None generated")

    return {
        "polymer_name": polymer_name,
        "gro": final_gro,
        "top": final_top,
        "itp_files": final_itp_files,
        "acpype_workdir": acpype_workdir,
        "acpype_output_dir": acpype_output_dir,
    }
```

</details>

<a id="definition-420"></a>

## `PHAMeltBuilder.prepare_polyply_inputs`

Source lines 420–501. Named callable; inspect its callers before treating it as a stable public API.

```python
def prepare_polyply_inputs(self, polymer_names, number_of_polymers, polymer_gromacs_files, melt_dir, melt_name): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| polymer_names | not annotated | required |
| number_of_polymers | not annotated | required |
| polymer_gromacs_files | not annotated | required |
| melt_dir | not annotated | required |
| melt_name | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `' '.join`, `'\n'.join`, `Path`, `Path(melt_dir).resolve`, `copied_topology_files.append`, `f.write`, `files.get`, `inputs_dir.mkdir`, `len`, `melt_dir.mkdir`, `open`, `range`, `self.combine_itps`, `shutil.copyfile`.

Explicit return expressions; different branches may return different objects:

```python
{'melt_dir': melt_dir, 'inputs_dir': inputs_dir, 'system_itp': system_itp_file, 'system_top': system_top_file, 'copied_topology_files': copied_topology_files}
```

Calls worth inspecting for I/O, state changes or delegated execution: `f.write`, `inputs_dir.mkdir`, `melt_dir.mkdir`, `open`, `shutil.copyfile`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
    def prepare_polyply_inputs(
        self,
        polymer_names,
        number_of_polymers,
        polymer_gromacs_files,
        melt_dir,
        melt_name,
    ):
        melt_dir = Path(melt_dir).resolve()
        inputs_dir = melt_dir / "inputs"

        melt_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        inputs_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        copied_topology_files = []

        for polymer_name in polymer_names:
            files = polymer_gromacs_files[polymer_name]

            source_top = files["top"]
            source_gro = files["gro"]

            copied_top = inputs_dir / f"{polymer_name}.top"
            copied_gro = inputs_dir / f"{polymer_name}.gro"

            shutil.copyfile(source_top, copied_top)
            shutil.copyfile(source_gro, copied_gro)

            copied_topology_files.append(copied_top)

            for itp_file in files.get("itp_files", []):
                copied_itp = inputs_dir / itp_file.name

                shutil.copyfile(
                    itp_file,
                    copied_itp,
                )

        system_itp_file = inputs_dir / f"{melt_name}.itp"
        system_top_file = inputs_dir / f"{melt_name}.top"

        self.combine_itps(
            itp_files=copied_topology_files,
            output_file=system_itp_file,
        )

        molecule_statements = "\n".join(
            [
                f"{polymer_names[i]} {number_of_polymers[i]}"
                for i in range(len(polymer_names))
            ]
        )

        system_top_contents = f"""
#include "{system_itp_file.name}"

[ system ]

Packed {' '.join(polymer_names)}

[ molecules ]

{molecule_statements}
"""

        with open(system_top_file, "w") as f:
            f.write(system_top_contents)

        return {
            "melt_dir": melt_dir,
            "inputs_dir": inputs_dir,
            "system_itp": system_itp_file,
            "system_top": system_top_file,
            "copied_topology_files": copied_topology_files,
        }
```

</details>

<a id="definition-503"></a>

## `PHAMeltBuilder.run_polyply`

Source lines 503–566. Named callable; inspect its callers before treating it as a stable public API.

```python
def run_polyply(self, polymer_names, number_of_polymers, polymer_gromacs_files, melt_dir, melt_name, density=750): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| polymer_names | not annotated | required |
| number_of_polymers | not annotated | required |
| polymer_gromacs_files | not annotated | required |
| melt_dir | not annotated | required |
| melt_name | not annotated | required |
| density | not annotated | 750 |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `FileNotFoundError`, `output_gro_in_inputs.exists`, `print`, `self.prepare_polyply_inputs`, `self.run_command`, `shutil.copyfile`.

Explicit return expressions; different branches may return different objects:

```python
{'melt_name': melt_name, 'melt_dir': melt_dir, 'inputs_dir': inputs_dir, 'top': final_top, 'gro': final_gro, 'itp': final_itp, 'density': density}
```

Calls worth inspecting for I/O, state changes or delegated execution: `self.run_command`, `shutil.copyfile`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
FileNotFoundError(f'Expected Polyply output not found:\n{output_gro_in_inputs}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def run_polyply(
    self,
    polymer_names,
    number_of_polymers,
    polymer_gromacs_files,
    melt_dir,
    melt_name,
    density=750,
):
    polyply_inputs = self.prepare_polyply_inputs(
        polymer_names=polymer_names,
        number_of_polymers=number_of_polymers,
        polymer_gromacs_files=polymer_gromacs_files,
        melt_dir=melt_dir,
        melt_name=melt_name,
    )

    melt_dir = polyply_inputs["melt_dir"]
    inputs_dir = polyply_inputs["inputs_dir"]
    system_top = polyply_inputs["system_top"]
    system_itp = polyply_inputs["system_itp"]

    output_gro_in_inputs = inputs_dir / f"{melt_name}.gro"

    final_gro = melt_dir / f"{melt_name}.gro"
    final_top = melt_dir / f"{melt_name}.top"
    final_itp = melt_dir / f"{melt_name}.itp"

    polyply_command = (
        f"polyply gen_coords "
        f"-p {system_top.name} "
        f"-o {output_gro_in_inputs.name} "
        f"-dens {density}"
    )

    self.run_command(
        polyply_command,
        workdir=inputs_dir,
    )

    if not output_gro_in_inputs.exists():
        raise FileNotFoundError(
            f"Expected Polyply output not found:\n{output_gro_in_inputs}"
        )

    shutil.copyfile(output_gro_in_inputs, final_gro)
    shutil.copyfile(system_top, final_top)
    shutil.copyfile(system_itp, final_itp)

    print("\nPolyply melt generation complete.")
    print("Melt name: ", melt_name)
    print("TOP:       ", final_top)
    print("GRO:       ", final_gro)
    print("ITP:       ", final_itp)

    return {
        "melt_name": melt_name,
        "melt_dir": melt_dir,
        "inputs_dir": inputs_dir,
        "top": final_top,
        "gro": final_gro,
        "itp": final_itp,
        "density": density,
    }
```

</details>

<a id="definition-568"></a>

## `PHAMeltBuilder.combine_itps`

Source lines 568–610. Named callable; inspect its callers before treating it as a stable public API.

```python
def combine_itps(self, itp_files, output_file): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| itp_files | not annotated | required |
| output_file | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `any`, `enumerate`, `infile.readlines`, `len`, `line.strip`, `line.strip().lower`, `open`, `outfile.write`, `print`, `stripped.endswith`, `stripped.startswith`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Calls worth inspecting for I/O, state changes or delegated execution: `infile.readlines`, `open`, `outfile.write`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def combine_itps(
    self,
    itp_files,
    output_file,
):
    skip_sections = {
        "[ defaults ]",
        "[ atomtypes ]",
    }

    with open(output_file, "w") as outfile:
        for idx, file_path in enumerate(itp_files):
            with open(file_path, "r") as infile:
                lines = infile.readlines()

            copy_block = True

            for line in lines:
                stripped = line.strip().lower()

                if any(
                    stripped.startswith(section)
                    for section in skip_sections
                ):
                    if idx > 0:
                        copy_block = False
                        continue

                if (
                    stripped.startswith("[")
                    and stripped.endswith("]")
                    and stripped not in skip_sections
                ):
                    copy_block = True

                if copy_block:
                    outfile.write(line)

            outfile.write("\n\n")

    print(
        f"Combined {len(itp_files)} topology files into {output_file}"
    )
```

</details>

<a id="definition-612"></a>

## `PHAMeltBuilder.edit_acpype_topology_for_polyply`

Source lines 612–669. Named callable; inspect its callers before treating it as a stable public API.

```python
def edit_acpype_topology_for_polyply(self, topology_file): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| topology_file | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `''.join`, `Path`, `f.writelines`, `len`, `line.replace`, `line.rstrip`, `line.strip`, `new_lines.append`, `open`, `print`, `range`, `re.split`, `stripped.startswith`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Calls worth inspecting for I/O, state changes or delegated execution: `f.writelines`, `open`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def edit_acpype_topology_for_polyply(self, topology_file):
    topology_file = Path(topology_file)
    inside_atomtypes = False
    new_lines = []

    with open(topology_file, "r") as f:
        for line in f:
            stripped = line.strip()

            if stripped.startswith("[ atomtypes ]"):
                inside_atomtypes = True
                new_lines.append(line)
                continue

            if (
                inside_atomtypes
                and stripped.startswith("[")
                and not stripped.startswith("[ atomtypes ]")
            ):
                inside_atomtypes = False

            if inside_atomtypes and stripped:
                if stripped.startswith(";"):
                    new_lines.append(
                        line.replace(
                            "bond_type",
                            " " * len("bond_type"),
                        )
                    )

                else:
                    parts = re.split(
                        r"(\s+)",
                        line.rstrip("\n"),
                    )

                    words = [
                        i
                        for i in range(0, len(parts), 2)
                    ]

                    if len(words) > 2:
                        second_word_index = words[2]
                        word = parts[second_word_index]
                        parts[second_word_index] = " " * len(word)

                    new_lines.append("".join(parts) + "\n")

            else:
                new_lines.append(line)

    with open(topology_file, "w") as f:
        f.writelines(new_lines)

    print(
        "Edited ACPYPE topology for Polyply compatibility: "
        f"{topology_file}"
    )
```

</details>

<a id="definition-671"></a>

## `PHAMeltBuilder.test_polymer_melt_simulation`

Source lines 671–775. Named callable; inspect its callers before treating it as a stable public API.

```python
def test_polymer_melt_simulation(self, melt_name, topology_file, coordinate_file, run_name='Test', test_steps=1000, temperature=300, timestep=1.0): ...
```

### Purpose and original contract

No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| self | not annotated | bound instance/class |
| melt_name | not annotated | required |
| topology_file | not annotated | required |
| coordinate_file | not annotated | required |
| run_name | not annotated | 'Test' |
| test_steps | not annotated | 1000 |
| temperature | not annotated | 300 |
| timestep | not annotated | 1.0 |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `FileNotFoundError`, `GromacsSimulation`, `Path`, `Path(coordinate_file).resolve`, `Path(topology_file).resolve`, `coordinate_file.exists`, `print`, `run_name.strip`, `run_name.strip().replace`, `sim.basic_NVT`, `sim.minimize_energy`, `sim.set_temperature`, `sim.set_timestep`, `sim.set_total_steps`, `simulation_run_dir.exists`, `simulation_run_dir.mkdir`, `simulations_dir.mkdir`, `str`, `topology_file.exists`.

Explicit return expressions; different branches may return different objects:

```python
{'melt_name': melt_name, 'success': success, 'simulation_dir': simulation_run_dir, 'topology_file': topology_file, 'coordinate_file': coordinate_file, 'minimized_sim': min_sim, 'test_sim': test_sim, 'test_data': test_data, 'error_message': error_message}
```

Calls worth inspecting for I/O, state changes or delegated execution: `sim.set_timestep`, `sim.set_total_steps`, `simulation_run_dir.mkdir`, `simulations_dir.mkdir`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
FileNotFoundError(f'Melt topology file not found:\n{topology_file}')
FileNotFoundError(f'Melt coordinate file not found:\n{coordinate_file}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def test_polymer_melt_simulation(
    self,
    melt_name,
    topology_file,
    coordinate_file,
    run_name="Test",
    test_steps=1000,
    temperature=300,
    timestep=1.0,
):
    from src.iphasimulator.sw_openmm import GromacsSimulation

    topology_file = Path(topology_file).resolve()
    coordinate_file = Path(coordinate_file).resolve()

    if not topology_file.exists():
        raise FileNotFoundError(
            f"Melt topology file not found:\n{topology_file}"
        )

    if not coordinate_file.exists():
        raise FileNotFoundError(
            f"Melt coordinate file not found:\n{coordinate_file}"
        )

    simulations_dir = (
        self.paths.PHA_melts_dir
        / melt_name
        / "simulations"
    )

    simulations_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    run_name = run_name.strip().replace(" ", "_")

    counter = 1

    while True:
        simulation_run_dir = simulations_dir / f"{run_name}_{counter:02d}"

        if not simulation_run_dir.exists():
            simulation_run_dir.mkdir(
                parents=True,
                exist_ok=False,
            )
            break

        counter += 1

    sim = GromacsSimulation(
        self.paths,
        str(topology_file),
        str(coordinate_file),
        output_dir=str(simulation_run_dir),
    )

    sim.run_name = simulation_run_dir.name

    sim.set_total_steps(test_steps)
    sim.set_temperature(temperature)
    sim.set_timestep(timestep)

    try:
        min_sim = sim.minimize_energy()

        test_sim, test_data = sim.basic_NVT(
            min_sim,
            total_steps=test_steps,
            temp=temperature,
            filename=run_name,
        )

        success = True
        error_message = None

    except Exception as error:
        success = False
        min_sim = None
        test_sim = None
        test_data = None
        error_message = str(error)

    print("\nPolymer melt simulation test complete.")
    print("Melt name:      ", melt_name)
    print("Success:        ", success)
    print("Simulation dir: ", simulation_run_dir)

    if error_message is not None:
        print("Error:")
        print(error_message)

    return {
        "melt_name": melt_name,
        "success": success,
        "simulation_dir": simulation_run_dir,
        "topology_file": topology_file,
        "coordinate_file": coordinate_file,
        "minimized_sim": min_sim,
        "test_sim": test_sim,
        "test_data": test_data,
        "error_message": error_message,
    }
```

</details>
