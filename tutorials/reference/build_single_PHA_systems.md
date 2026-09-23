# build_single_PHA_systems.py

System preparation around an already-built homopolymer. The common input preparation resolves residue parameters and Amber files. Dry, water and salted routes then write/run LEaP inputs, count atoms and register outputs. Salt preparation estimates pairs after an initial solvation pass. The box parameter is forwarded to Amber operations; dry setBox and solvent padding have different meanings.

[Current source](../../src/iphasimulator/build_single_PHA_systems.py)

This page is generated from source syntax. Original docstrings can be incomplete or outdated; module notes above identify known discrepancies. Call/return/error lists describe direct syntax, not all behaviour inside callees. Read the source excerpt for branch order and effects. No scientific execution is implied.

Explicit functions/methods/nested helpers: **8**.

## Module imports

```python
from pathlib import Path
import subprocess
from .pha_filepath_manager import PHAFileManager
```

## Function map

- [`run_tleap` — source line 18](#definition-18)
- [`write_tleap_file` — source line 74](#definition-74)
- [`check_required_files` — source line 92](#definition-92)
- [`calculate_ion_pairs_from_rst7` — source line 112](#definition-112)
- [`prepare_single_system_inputs` — source line 165](#definition-165)
- [`build_dry_PHA` — source line 224](#definition-224)
- [`build_solvated_PHA` — source line 330](#definition-330)
- [`build_solvated_PHA_ions` — source line 441](#definition-441)

<a id="definition-18"></a>

## `run_tleap`

Source lines 18–71. Named callable; inspect its callers before treating it as a stable public API.

```python
def run_tleap(intleap_file, workdir, log_file): ...
```

### Purpose and original contract

Run tleap and save captured stdout/stderr to a specified log file.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| intleap_file | not annotated | required |
| workdir | not annotated | required |
| log_file | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `' '.join`, `Path`, `Path(intleap_file).resolve`, `Path(log_file).resolve`, `Path(workdir).resolve`, `RuntimeError`, `log_file.parent.mkdir`, `open`, `output.write`, `print`, `str`, `subprocess.run`.

Explicit return expressions; different branches may return different objects:

```python
result
```

Calls worth inspecting for I/O, state changes or delegated execution: `log_file.parent.mkdir`, `open`, `output.write`, `subprocess.run`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
RuntimeError(f'tleap failed. See log file:\n{log_file}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def run_tleap(
    intleap_file,
    workdir,
    log_file,
):
    """
    Run tleap and save captured stdout/stderr to a specified log file.
    """

    intleap_file = Path(intleap_file).resolve()
    workdir = Path(workdir).resolve()
    log_file = Path(log_file).resolve()

    command = [
        "tleap",
        "-f",
        str(intleap_file),
    ]

    print("\nRunning tleap:")
    print(" ".join(command))
    print("Working directory:", workdir)

    result = subprocess.run(
        command,
        cwd=workdir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    log_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(log_file, "w") as output:
        output.write("STDOUT\n")
        output.write(result.stdout)

        output.write("\n\nSTDERR\n")
        output.write(result.stderr)

    print("Return code:", result.returncode)
    print("Log file:", log_file)

    if result.returncode != 0:
        raise RuntimeError(
            f"tleap failed. See log file:\n{log_file}"
        )

    return result
```

</details>

<a id="definition-74"></a>

## `write_tleap_file`

Source lines 74–89. Named callable; inspect its callers before treating it as a stable public API.

```python
def write_tleap_file(path, content): ...
```

### Purpose and original contract

Write a tleap input file.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| path | not annotated | required |
| content | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `Path`, `content.strip`, `file.write`, `open`, `path.parent.mkdir`.

Explicit return expressions; different branches may return different objects:

```python
path
```

Calls worth inspecting for I/O, state changes or delegated execution: `file.write`, `open`, `path.parent.mkdir`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def write_tleap_file(path, content):
    """
    Write a tleap input file.
    """

    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(path, "w") as file:
        file.write(content.strip() + "\n")

    return path
```

</details>

<a id="definition-92"></a>

## `check_required_files`

Source lines 92–109. Named callable; inspect its callers before treating it as a stable public API.

```python
def check_required_files(file_dict, keys): ...
```

### Purpose and original contract

Confirm that the requested paths exist.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| file_dict | not annotated | required |
| keys | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `'\n'.join`, `FileNotFoundError`, `Path`, `missing.append`, `path.exists`, `str`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
FileNotFoundError('Missing required files:\n' + '\n'.join((str(path) for path in missing)))
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def check_required_files(file_dict, keys):
    """
    Confirm that the requested paths exist.
    """

    missing = []

    for key in keys:
        path = Path(file_dict[key])

        if not path.exists():
            missing.append(path)

    if missing:
        raise FileNotFoundError(
            "Missing required files:\n"
            + "\n".join(str(path) for path in missing)
        )
```

</details>

<a id="definition-112"></a>

## `calculate_ion_pairs_from_rst7`

Source lines 112–162. Named callable; inspect its callers before treating it as a stable public API.

```python
def calculate_ion_pairs_from_rst7(rst7_path, concentration_molar): ...
```

### Purpose and original contract

Calculate the number of ion pairs required for a target concentration.

The final line of the Amber rst7 file is expected to contain:

    lx ly lz alpha beta gamma

Box lengths are interpreted as Angstrom.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| rst7_path | not annotated | required |
| concentration_molar | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `Path`, `ValueError`, `file.readlines`, `float`, `len`, `lines[-1].split`, `open`, `print`, `round`.

Explicit return expressions; different branches may return different objects:

```python
n_pairs
```

Calls worth inspecting for I/O, state changes or delegated execution: `file.readlines`, `open`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError(f'RST7 file is empty:\n{rst7_path}')
ValueError(f'Could not read box dimensions from:\n{rst7_path}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def calculate_ion_pairs_from_rst7(
    rst7_path,
    concentration_molar,
):
    """
    Calculate the number of ion pairs required for a target concentration.

    The final line of the Amber rst7 file is expected to contain:

        lx ly lz alpha beta gamma

    Box lengths are interpreted as Angstrom.
    """

    rst7_path = Path(rst7_path)

    with open(rst7_path, "r") as file:
        lines = file.readlines()

    if not lines:
        raise ValueError(
            f"RST7 file is empty:\n{rst7_path}"
        )

    box_line = lines[-1].split()

    if len(box_line) < 3:
        raise ValueError(
            f"Could not read box dimensions from:\n{rst7_path}"
        )

    lx = float(box_line[0])
    ly = float(box_line[1])
    lz = float(box_line[2])

    volume_litres = lx * ly * lz * 1e-27

    n_pairs = round(
        float(concentration_molar)
        * AVOGADRO
        * volume_litres
    )

    print(
        f"Box dimensions: "
        f"{lx:.3f} x {ly:.3f} x {lz:.3f} Å"
    )
    print(f"Volume: {volume_litres:.3e} L")
    print(f"Ion pairs: {n_pairs}")

    return n_pairs
```

</details>

<a id="definition-165"></a>

## `prepare_single_system_inputs`

Source lines 165–221. Named callable; inspect its callers before treating it as a stable public API.

```python
def prepare_single_system_inputs(paths, polymer_name): ...
```

### Purpose and original contract

Locate the built polymer and parameter files.

No files are copied. Absolute paths are returned for use inside tleap.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| paths | not annotated | required |
| polymer_name | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `Path`, `Path(value).resolve`, `built_files.items`, `check_required_files`, `parameter_files.items`, `paths.get_PHA_monomer_unit_files`, `paths.get_built_PHA_amber_files`, `paths.parse_built_PHA_name`.

Explicit return expressions; different branches may return different objects:

```python
{'PHA_type': PHA_type, 'length': length, 'built_files': resolved_built_files, 'parameter_files': resolved_parameter_files}
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def prepare_single_system_inputs(
    paths,
    polymer_name,
):
    """
    Locate the built polymer and parameter files.

    No files are copied. Absolute paths are returned for use inside tleap.
    """

    PHA_type, length = paths.parse_built_PHA_name(
        polymer_name
    )

    built_files = paths.get_built_PHA_amber_files(
        polymer_name
    )

    parameter_files = paths.get_PHA_monomer_unit_files(
        PHA_type
    )

    check_required_files(
        built_files,
        [
            "pdb",
            "prmtop",
            "rst7",
        ],
    )

    check_required_files(
        parameter_files,
        [
            "head_prepin",
            "mainchain_prepin",
            "tail_prepin",
            "frcmod",
        ],
    )

    resolved_built_files = {
        key: Path(value).resolve()
        for key, value in built_files.items()
    }

    resolved_parameter_files = {
        key: Path(value).resolve()
        for key, value in parameter_files.items()
    }

    return {
        "PHA_type": PHA_type,
        "length": length,
        "built_files": resolved_built_files,
        "parameter_files": resolved_parameter_files,
    }
```

</details>

<a id="definition-224"></a>

## `build_dry_PHA`

Source lines 224–327. Named callable; inspect its callers before treating it as a stable public API.

```python
def build_dry_PHA(polymer_name, root_dir='structure_database', forcefield='gaff2', box_radius=20.0): ...
```

### Purpose and original contract

Build a dry single-chain PHA system from an already-built polymer.

Final files are written to:

    PHA_dry/<polymer_name>_dry/

tleap inputs and logs are written to:

    PHA_dry/<polymer_name>_dry/inputs/

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| polymer_name | not annotated | required |
| root_dir | not annotated | 'structure_database' |
| forcefield | not annotated | 'gaff2' |
| box_radius | not annotated | 20.0 |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `PHAFileManager`, `TypeError`, `isinstance`, `paths.count_atoms_from_amber_topology`, `paths.create_dry_PHA_dir`, `paths.create_dry_PHA_dir(polymer_name).resolve`, `paths.get_dry_PHA_inputs_dir`, `paths.get_dry_PHA_inputs_dir(polymer_name).resolve`, `paths.get_dry_PHA_system_name`, `paths.register_md_system`, `prepare_single_system_inputs`, `run_tleap`, `write_tleap_file`.

Explicit return expressions; different branches may return different objects:

```python
{'system_name': system_name, 'system_type': 'dry', 'output_dir': output_dir, 'inputs_dir': inputs_dir, 'input_polymer': polymer_name, 'input_polymer_pdb': built_files['pdb'], 'pdb': pdb, 'prmtop': prmtop, 'rst7': rst7, 'intleap': intleap, 'log_file': log_file, 'box_radius': box_radius, 'number_of_atoms': number_of_atoms}
```

Calls worth inspecting for I/O, state changes or delegated execution: `paths.register_md_system`, `write_tleap_file`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
TypeError('box_radius must be a float, e.g. 20.0')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def build_dry_PHA(
    polymer_name,
    root_dir="structure_database",
    forcefield="gaff2",
    box_radius=20.0,
):
    """
    Build a dry single-chain PHA system from an already-built polymer.

    Final files are written to:

        PHA_dry/<polymer_name>_dry/

    tleap inputs and logs are written to:

        PHA_dry/<polymer_name>_dry/inputs/
    """

    if not isinstance(box_radius, float):
        raise TypeError(
            "box_radius must be a float, e.g. 20.0"
        )

    paths = PHAFileManager(root_dir)

    system_name = paths.get_dry_PHA_system_name(
        polymer_name
    )

    output_dir = paths.create_dry_PHA_dir(
        polymer_name
    ).resolve()

    inputs_dir = paths.get_dry_PHA_inputs_dir(
        polymer_name
    ).resolve()

    prepared = prepare_single_system_inputs(
        paths=paths,
        polymer_name=polymer_name,
    )

    built_files = prepared["built_files"]
    params = prepared["parameter_files"]

    prmtop = output_dir / f"{system_name}.prmtop"
    rst7 = output_dir / f"{system_name}.rst7"
    pdb = output_dir / f"{system_name}.pdb"

    intleap = inputs_dir / f"{system_name}.intleap"
    log_file = inputs_dir / f"{system_name}.log"

    tleap_content = f"""
source leaprc.{forcefield}

loadamberprep {params["head_prepin"]}
loadamberprep {params["mainchain_prepin"]}
loadamberprep {params["tail_prepin"]}
loadamberparams {params["frcmod"]}

polymer = loadpdb {built_files["pdb"]}

setBox polymer centers {box_radius}

saveamberparm polymer {prmtop} {rst7}
savepdb polymer {pdb}

quit
"""

    write_tleap_file(
        intleap,
        tleap_content,
    )

    run_tleap(
        intleap_file=intleap,
        workdir=inputs_dir,
        log_file=log_file,
    )

    number_of_atoms = paths.count_atoms_from_amber_topology(prmtop)

    paths.register_md_system(
        system_name=system_name,
        system_type="dry",
        number_of_atoms=number_of_atoms,
        )

    return {
        "system_name": system_name,
        "system_type": "dry",
        "output_dir": output_dir,
        "inputs_dir": inputs_dir,
        "input_polymer": polymer_name,
        "input_polymer_pdb": built_files["pdb"],
        "pdb": pdb,
        "prmtop": prmtop,
        "rst7": rst7,
        "intleap": intleap,
        "log_file": log_file,
        "box_radius": box_radius,
        "number_of_atoms": number_of_atoms,
    }
```

</details>

<a id="definition-330"></a>

## `build_solvated_PHA`

Source lines 330–438. Named callable; inspect its callers before treating it as a stable public API.

```python
def build_solvated_PHA(polymer_name, root_dir='structure_database', forcefield='gaff2', water_leaprc='water.tip3p', water_box='TIP3PBOX', box_radius=20.0): ...
```

### Purpose and original contract

Build a solvated single-chain PHA system.

Final files are written to:

    PHA_solvated/<polymer_name>_solvated/

tleap inputs and logs are written to:

    PHA_solvated/<polymer_name>_solvated/inputs/

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| polymer_name | not annotated | required |
| root_dir | not annotated | 'structure_database' |
| forcefield | not annotated | 'gaff2' |
| water_leaprc | not annotated | 'water.tip3p' |
| water_box | not annotated | 'TIP3PBOX' |
| box_radius | not annotated | 20.0 |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `PHAFileManager`, `TypeError`, `isinstance`, `paths.count_atoms_from_amber_topology`, `paths.create_solvated_PHA_dir`, `paths.create_solvated_PHA_dir(polymer_name).resolve`, `paths.get_solvated_PHA_inputs_dir`, `paths.get_solvated_PHA_inputs_dir(polymer_name).resolve`, `paths.get_solvated_PHA_system_name`, `paths.register_md_system`, `prepare_single_system_inputs`, `run_tleap`, `write_tleap_file`.

Explicit return expressions; different branches may return different objects:

```python
{'system_name': system_name, 'system_type': 'solvated', 'output_dir': output_dir, 'inputs_dir': inputs_dir, 'input_polymer': polymer_name, 'input_polymer_pdb': built_files['pdb'], 'pdb': pdb, 'prmtop': prmtop, 'rst7': rst7, 'intleap': intleap, 'log_file': log_file, 'water_leaprc': water_leaprc, 'water_box': water_box, 'box_radius': box_radius, 'number_of_atoms': number_of_atoms}
```

Calls worth inspecting for I/O, state changes or delegated execution: `paths.register_md_system`, `write_tleap_file`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
TypeError('box_radius must be a float, e.g. 20.0')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def build_solvated_PHA(
    polymer_name,
    root_dir="structure_database",
    forcefield="gaff2",
    water_leaprc="water.tip3p",
    water_box="TIP3PBOX",
    box_radius=20.0,
):
    """
    Build a solvated single-chain PHA system.

    Final files are written to:

        PHA_solvated/<polymer_name>_solvated/

    tleap inputs and logs are written to:

        PHA_solvated/<polymer_name>_solvated/inputs/
    """

    if not isinstance(box_radius, float):
        raise TypeError(
            "box_radius must be a float, e.g. 20.0"
        )

    paths = PHAFileManager(root_dir)

    system_name = paths.get_solvated_PHA_system_name(
        polymer_name
    )

    output_dir = paths.create_solvated_PHA_dir(
        polymer_name
    ).resolve()

    inputs_dir = paths.get_solvated_PHA_inputs_dir(
        polymer_name
    ).resolve()

    prepared = prepare_single_system_inputs(
        paths=paths,
        polymer_name=polymer_name,
    )

    built_files = prepared["built_files"]
    params = prepared["parameter_files"]

    prmtop = output_dir / f"{system_name}.prmtop"
    rst7 = output_dir / f"{system_name}.rst7"
    pdb = output_dir / f"{system_name}.pdb"

    intleap = inputs_dir / f"{system_name}.intleap"
    log_file = inputs_dir / f"{system_name}.log"

    tleap_content = f"""
source leaprc.{forcefield}
source leaprc.{water_leaprc}

loadamberprep {params["head_prepin"]}
loadamberprep {params["mainchain_prepin"]}
loadamberprep {params["tail_prepin"]}
loadamberparams {params["frcmod"]}

polymer = loadpdb {built_files["pdb"]}

solvatebox polymer {water_box} {box_radius}

saveamberparm polymer {prmtop} {rst7}
savepdb polymer {pdb}

quit
"""

    write_tleap_file(
        intleap,
        tleap_content,
    )

    run_tleap(
        intleap_file=intleap,
        workdir=inputs_dir,
        log_file=log_file,
    )

    number_of_atoms = paths.count_atoms_from_amber_topology(prmtop)

    paths.register_md_system(
        system_name=system_name,
        system_type="solvated",
        number_of_atoms=number_of_atoms,
        )

    return {
        "system_name": system_name,
        "system_type": "solvated",
        "output_dir": output_dir,
        "inputs_dir": inputs_dir,
        "input_polymer": polymer_name,
        "input_polymer_pdb": built_files["pdb"],
        "pdb": pdb,
        "prmtop": prmtop,
        "rst7": rst7,
        "intleap": intleap,
        "log_file": log_file,
        "water_leaprc": water_leaprc,
        "water_box": water_box,
        "box_radius": box_radius,
        "number_of_atoms": number_of_atoms,
    }
```

</details>

<a id="definition-441"></a>

## `build_solvated_PHA_ions`

Source lines 441–630. Named callable; inspect its callers before treating it as a stable public API.

```python
def build_solvated_PHA_ions(polymer_name, root_dir='structure_database', forcefield='gaff2', water_leaprc='water.tip3p', water_box='TIP3PBOX', box_radius=20.0, salt='KCl', pos_ion='K+', neg_ion='Cl-', ion_conc=0.15): ...
```

### Purpose and original contract

Build a solvated single-chain PHA system containing ions.

A two-pass tleap workflow is used:

1. Build a temporary solvated system.
2. Calculate the required ion count from its box volume.
3. Rebuild the system with the requested number of ion pairs.

Final files are written to the system root. Temporary files, tleap inputs,
and logs are written to the inputs subdirectory.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| polymer_name | not annotated | required |
| root_dir | not annotated | 'structure_database' |
| forcefield | not annotated | 'gaff2' |
| water_leaprc | not annotated | 'water.tip3p' |
| water_box | not annotated | 'TIP3PBOX' |
| box_radius | not annotated | 20.0 |
| salt | not annotated | 'KCl' |
| pos_ion | not annotated | 'K+' |
| neg_ion | not annotated | 'Cl-' |
| ion_conc | not annotated | 0.15 |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `PHAFileManager`, `TypeError`, `ValueError`, `calculate_ion_pairs_from_rst7`, `float`, `isinstance`, `paths.count_atoms_from_amber_topology`, `paths.create_solvated_ions_PHA_dir`, `paths.create_solvated_ions_PHA_dir(polymer_name=polymer_name, salt=salt, ion_concentration=ion_conc).resolve`, `paths.get_solvated_ions_PHA_inputs_dir`, `paths.get_solvated_ions_PHA_inputs_dir(polymer_name=polymer_name, salt=salt, ion_concentration=ion_conc).resolve`, `paths.get_solvated_ions_PHA_system_name`, `paths.register_md_system`, `prepare_single_system_inputs`, `print`, `run_tleap`, `write_tleap_file`.

Explicit return expressions; different branches may return different objects:

```python
{'system_name': system_name, 'system_type': 'solvated_ions', 'output_dir': output_dir, 'inputs_dir': inputs_dir, 'input_polymer': polymer_name, 'input_polymer_pdb': built_files['pdb'], 'pdb': pdb, 'prmtop': prmtop, 'rst7': rst7, 'intleap': intleap, 'log_file': log_file, 'temp_pdb': temp_pdb, 'temp_prmtop': temp_prmtop, 'temp_rst7': temp_rst7, 'temp_intleap': temp_intleap, 'temp_log_file': temp_log … [full expression below]
```

Calls worth inspecting for I/O, state changes or delegated execution: `paths.register_md_system`, `write_tleap_file`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
TypeError('box_radius must be a float, e.g. 20.0')
ValueError('ion_conc cannot be negative.')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def build_solvated_PHA_ions(
    polymer_name,
    root_dir="structure_database",
    forcefield="gaff2",
    water_leaprc="water.tip3p",
    water_box="TIP3PBOX",
    box_radius=20.0,
    salt="KCl",
    pos_ion="K+",
    neg_ion="Cl-",
    ion_conc=0.15,
):
    """
    Build a solvated single-chain PHA system containing ions.

    A two-pass tleap workflow is used:

    1. Build a temporary solvated system.
    2. Calculate the required ion count from its box volume.
    3. Rebuild the system with the requested number of ion pairs.

    Final files are written to the system root. Temporary files, tleap inputs,
    and logs are written to the inputs subdirectory.
    """

    if not isinstance(box_radius, float):
        raise TypeError(
            "box_radius must be a float, e.g. 20.0"
        )

    if float(ion_conc) < 0:
        raise ValueError(
            "ion_conc cannot be negative."
        )

    paths = PHAFileManager(root_dir)


    system_name = paths.get_solvated_ions_PHA_system_name(
        polymer_name=polymer_name,
        salt=salt,
        ion_concentration=ion_conc,
    )

    output_dir = paths.create_solvated_ions_PHA_dir(
        polymer_name=polymer_name,
        salt=salt,
        ion_concentration=ion_conc).resolve()

    inputs_dir = paths.get_solvated_ions_PHA_inputs_dir(
        polymer_name=polymer_name,
        salt=salt,
        ion_concentration=ion_conc).resolve()

    prepared = prepare_single_system_inputs(
        paths=paths,
        polymer_name=polymer_name,
    )

    built_files = prepared["built_files"]
    params = prepared["parameter_files"]

    temp_name = f"{system_name}_temp_solvated"

    temp_prmtop = inputs_dir / f"{temp_name}.prmtop"
    temp_rst7 = inputs_dir / f"{temp_name}.rst7"
    temp_pdb = inputs_dir / f"{temp_name}.pdb"
    temp_intleap = inputs_dir / f"{temp_name}.intleap"
    temp_log_file = inputs_dir / f"{temp_name}.log"

    prmtop = output_dir / f"{system_name}.prmtop"
    rst7 = output_dir / f"{system_name}.rst7"
    pdb = output_dir / f"{system_name}.pdb"

    intleap = inputs_dir / f"{system_name}.intleap"
    log_file = inputs_dir / f"{system_name}.log"

    temp_tleap_content = f"""
source leaprc.{forcefield}
source leaprc.{water_leaprc}

loadamberprep {params["head_prepin"]}
loadamberprep {params["mainchain_prepin"]}
loadamberprep {params["tail_prepin"]}
loadamberparams {params["frcmod"]}

polymer = loadpdb {built_files["pdb"]}

solvatebox polymer {water_box} {box_radius}

saveamberparm polymer {temp_prmtop} {temp_rst7}
savepdb polymer {temp_pdb}

quit
"""

    write_tleap_file(
        temp_intleap,
        temp_tleap_content,
    )

    print(
        "Running first tleap pass: "
        "solvation only."
    )

    run_tleap(
        intleap_file=temp_intleap,
        workdir=inputs_dir,
        log_file=temp_log_file,
    )

    num_ion_pairs = calculate_ion_pairs_from_rst7(
        temp_rst7,
        ion_conc,
    )

    final_tleap_content = f"""
source leaprc.{forcefield}
source leaprc.{water_leaprc}

loadamberprep {params["head_prepin"]}
loadamberprep {params["mainchain_prepin"]}
loadamberprep {params["tail_prepin"]}
loadamberparams {params["frcmod"]}

polymer = loadpdb {built_files["pdb"]}

solvatebox polymer {water_box} {box_radius}

addIonsRand polymer {pos_ion} {num_ion_pairs}
addIonsRand polymer {neg_ion} {num_ion_pairs}

saveamberparm polymer {prmtop} {rst7}
savepdb polymer {pdb}

quit
"""

    write_tleap_file(
        intleap,
        final_tleap_content,
    )

    print(
        "Running second tleap pass: "
        "solvation with ions."
    )

    run_tleap(
        intleap_file=intleap,
        workdir=inputs_dir,
        log_file=log_file,
    )

    number_of_atoms = paths.count_atoms_from_amber_topology(prmtop)

    paths.register_md_system(
        system_name=system_name,
        system_type="solvated_ions",
        number_of_atoms=number_of_atoms,
        )

    return {
        "system_name": system_name,
        "system_type": "solvated_ions",
        "output_dir": output_dir,
        "inputs_dir": inputs_dir,
        "input_polymer": polymer_name,
        "input_polymer_pdb": built_files["pdb"],
        "pdb": pdb,
        "prmtop": prmtop,
        "rst7": rst7,
        "intleap": intleap,
        "log_file": log_file,
        "temp_pdb": temp_pdb,
        "temp_prmtop": temp_prmtop,
        "temp_rst7": temp_rst7,
        "temp_intleap": temp_intleap,
        "temp_log_file": temp_log_file,
        "water_leaprc": water_leaprc,
        "water_box": water_box,
        "box_radius": box_radius,
        "salt": salt,
        "pos_ion": pos_ion,
        "neg_ion": neg_ion,
        "ion_conc": ion_conc,
        "num_ion_pairs": num_ion_pairs,
        "number_of_atoms": number_of_atoms,
    }
```

</details>
