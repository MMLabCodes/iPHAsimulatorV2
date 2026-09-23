# visualisation/visualiser.py

Read catalogue SMILES and draw individual or multiple monomers/polymers using RDKit. Catalogue loading, molecular parsing, drawing and notebook display are separate steps here; drawing a structure does not validate force-field readiness.

[Current source](../../src/iphasimulator/visualisation/visualiser.py)

This page is generated from source syntax. Original docstrings can be incomplete or outdated; module notes above identify known discrepancies. Call/return/error lists describe direct syntax, not all behaviour inside callees. Read the source excerpt for branch order and effects. No scientific execution is implied.

Explicit functions/methods/nested helpers: **9**.

## Module imports

```python
from pathlib import Path
import csv
from rdkit import Chem
from rdkit.Chem import Draw
```

## Function map

- [`load_available_PHA_monomers` — source line 16](#definition-16)
- [`smiles_to_mol` — source line 67](#definition-67)
- [`plot_available_PHA_monomers` — source line 102](#definition-102)
- [`show_available_PHA_monomers` — source line 185](#definition-185)
- [`show_PHA_monomer` — source line 234](#definition-234)
- [`load_polymer_smiles` — source line 312](#definition-312)
- [`plot_available_PHA_polymers` — source line 377](#definition-377)
- [`show_available_PHA_polymers` — source line 433](#definition-433)
- [`show_PHA_polymer` — source line 486](#definition-486)

<a id="definition-16"></a>

## `load_available_PHA_monomers`

Source lines 16–65. Named callable; inspect its callers before treating it as a stable public API.

```python
def load_available_PHA_monomers(residue_codes_csv): ...
```

### Purpose and original contract

Load available PHA monomer units from residue_codes.csv.

Parameters
----------

residue_codes_csv : str or pathlib.Path
    Path to the residue code CSV file.

Returns
-------

list[tuple[str, str]]
    List of ``(PHA_type, smiles)`` tuples for each available mainchain
    monomer unit.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| residue_codes_csv | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `FileNotFoundError`, `Path`, `csv.DictReader`, `monomers.append`, `open`, `residue_codes_csv.exists`, `smiles.strip`, `sorted`.

Explicit return expressions; different branches may return different objects:

```python
sorted(monomers, key=lambda item: item[0])
```

Calls worth inspecting for I/O, state changes or delegated execution: `csv.DictReader`, `open`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
FileNotFoundError(f'Could not find residue code CSV:\n{residue_codes_csv}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def load_available_PHA_monomers(residue_codes_csv):
    """
    Load available PHA monomer units from residue_codes.csv.

    Parameters
    ----------

    residue_codes_csv : str or pathlib.Path
        Path to the residue code CSV file.

    Returns
    -------

    list[tuple[str, str]]
        List of ``(PHA_type, smiles)`` tuples for each available mainchain
        monomer unit.
    """

    residue_codes_csv = Path(residue_codes_csv)

    if not residue_codes_csv.exists():
        raise FileNotFoundError(
            f"Could not find residue code CSV:\n"
            f"{residue_codes_csv}")

    monomers = []

    with open(residue_codes_csv, "r", newline="") as f:

        reader = csv.DictReader(f)
        for row in reader:
            if row["component"] != "mainchain":
                continue

            PHA_type = row["PHA_type"]
            smiles = row["smiles"]
            if smiles is None or smiles.strip() == "":
                continue

            monomers.append(
                (
                    PHA_type,
                    smiles,
                )
            )

    return sorted(
        monomers,
        key=lambda item: item[0],
    )
```

</details>

<a id="definition-67"></a>

## `smiles_to_mol`

Source lines 67–100. Named callable; inspect its callers before treating it as a stable public API.

```python
def smiles_to_mol(smiles, name=None): ...
```

### Purpose and original contract

Convert a SMILES string into an RDKit molecule.

Parameters
----------

smiles : str
    SMILES string to convert.

name : str, optional
    Optional molecule name used only for clearer error messages.

Returns
-------

rdkit.Chem.rdchem.Mol
    RDKit molecule object.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| smiles | not annotated | required |
| name | not annotated | None |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `Chem.MolFromSmiles`, `ValueError`.

Explicit return expressions; different branches may return different objects:

```python
mol
```

No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError(f'Could not parse SMILES:\n{smiles}')
ValueError(f'Could not parse SMILES for {name}:\n{smiles}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def smiles_to_mol(smiles, name=None):

    """
    Convert a SMILES string into an RDKit molecule.

    Parameters
    ----------

    smiles : str
        SMILES string to convert.

    name : str, optional
        Optional molecule name used only for clearer error messages.

    Returns
    -------

    rdkit.Chem.rdchem.Mol
        RDKit molecule object.
    """

    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        if name is None:
            raise ValueError(
                f"Could not parse SMILES:\n{smiles}"
            )

        raise ValueError(
            f"Could not parse SMILES for {name}:\n{smiles}"
        )

    return mol
```

</details>

<a id="definition-102"></a>

## `plot_available_PHA_monomers`

Source lines 102–182. Named callable; inspect its callers before treating it as a stable public API.

```python
def plot_available_PHA_monomers(residue_codes_csv='structure_database/residue_codes.csv', output_file='available_PHA_monomers.png', mols_per_row=4, image_size=(300, 220)): ...
```

### Purpose and original contract

Plot all available PHA monomer units from residue_codes.csv.
The function reads the mainchain monomer SMILES for each registered PHA
type, converts each SMILES string to an RDKit molecule and writes a grid
image to disk.

Parameters
----------

residue_codes_csv : str or pathlib.Path, optional
    Path to residue_codes.csv.

output_file : str or pathlib.Path, optional
    Path where the output image should be written.

mols_per_row : int, optional
    Number of structures shown per row.

image_size : tuple[int, int], optional
    Size of each molecule panel in pixels.

Returns
-------

pathlib.Path
    Path to the generated image.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| residue_codes_csv | not annotated | 'structure_database/residue_codes.csv' |
| output_file | not annotated | 'available_PHA_monomers.png' |
| mols_per_row | not annotated | 4 |
| image_size | not annotated | (300, 220) |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `Draw.MolsToGridImage`, `Path`, `RuntimeError`, `image.save`, `len`, `load_available_PHA_monomers`, `mols.append`, `names.append`, `output_file.parent.mkdir`, `print`, `smiles_to_mol`.

Explicit return expressions; different branches may return different objects:

```python
output_file
```

Calls worth inspecting for I/O, state changes or delegated execution: `image.save`, `load_available_PHA_monomers`, `output_file.parent.mkdir`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
RuntimeError('No valid PHA monomer SMILES found.')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def plot_available_PHA_monomers(
    residue_codes_csv="structure_database/residue_codes.csv",
    output_file="available_PHA_monomers.png",
    mols_per_row=4,
    image_size=(300, 220),
):

    """
    Plot all available PHA monomer units from residue_codes.csv.
    The function reads the mainchain monomer SMILES for each registered PHA
    type, converts each SMILES string to an RDKit molecule and writes a grid
    image to disk.

    Parameters
    ----------

    residue_codes_csv : str or pathlib.Path, optional
        Path to residue_codes.csv.

    output_file : str or pathlib.Path, optional
        Path where the output image should be written.

    mols_per_row : int, optional
        Number of structures shown per row.

    image_size : tuple[int, int], optional
        Size of each molecule panel in pixels.

    Returns
    -------

    pathlib.Path
        Path to the generated image.

    """

    output_file = Path(output_file)

    monomers = load_available_PHA_monomers(
        residue_codes_csv
    )

    if len(monomers) == 0:
        raise RuntimeError(
            "No valid PHA monomer SMILES found."
        )

    names = []

    mols = []

    for PHA_type, smiles in monomers:
        mol = smiles_to_mol(
            smiles,
            name=PHA_type,
        )

        names.append(PHA_type)

        mols.append(mol)

    image = Draw.MolsToGridImage(
        mols,
        molsPerRow=mols_per_row,
        subImgSize=image_size,
        legends=names,
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    image.save(output_file)

    print(
        f"Saved PHA monomer overview to:\n"
        f"{output_file}"
    )

    return output_file
```

</details>

<a id="definition-185"></a>

## `show_available_PHA_monomers`

Source lines 185–232. Named callable; inspect its callers before treating it as a stable public API.

```python
def show_available_PHA_monomers(residue_codes_csv='structure_database/residue_codes.csv', mols_per_row=4): ...
```

### Purpose and original contract

Display all available PHA monomer units.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| residue_codes_csv | not annotated | 'structure_database/residue_codes.csv' |
| mols_per_row | not annotated | 4 |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `Chem.MolFromSmiles`, `Draw.MolsToGridImage`, `display`, `load_available_PHA_monomers`, `mols.append`, `names.append`, `plt.axis`, `plt.figure`, `plt.imshow`, `plt.show`.

No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.

Calls worth inspecting for I/O, state changes or delegated execution: `load_available_PHA_monomers`, `plt.imshow`, `plt.show`. This is a name-based reading aid, not a complete effect analysis.

No explicit raise statement in this body. Failures may still propagate from dependencies or operations.

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def show_available_PHA_monomers(

    residue_codes_csv="structure_database/residue_codes.csv",
    mols_per_row=4,

):

    """

    Display all available PHA monomer units.

    """

    monomers = load_available_PHA_monomers(
        residue_codes_csv
    )

    mols = []
    names = []

    for pha_type, smiles in monomers:

        mols.append(
            Chem.MolFromSmiles(smiles)
        )

        names.append(
            pha_type
        )

    img = Draw.MolsToGridImage(
        mols,
        molsPerRow=mols_per_row,
        legends=names,
        subImgSize=(300,220),
    )

    try:
        from IPython.display import display
        display(img)

    except Exception:
        import matplotlib.pyplot as plt

        plt.figure(figsize=(12,10))
        plt.imshow(img)
        plt.axis("off")
        plt.show()
```

</details>

<a id="definition-234"></a>

## `show_PHA_monomer`

Source lines 234–306. Named callable; inspect its callers before treating it as a stable public API.

```python
def show_PHA_monomer(PHA_type, residue_codes_csv='structure_database/residue_codes.csv', image_size=(300, 220)): ...
```

### Purpose and original contract

Display one PHA monomer structure from residue_codes.csv.

Parameters
----------

PHA_type : str
    PHA type to display, e.g. "3HB" or "4HB".

residue_codes_csv : str or pathlib.Path, optional
    Path to residue_codes.csv.

image_size : tuple[int, int], optional
    Size of the rendered molecule image.

Returns
-------

PIL.Image.Image
    Rendered RDKit molecule image.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| PHA_type | not annotated | required |
| residue_codes_csv | not annotated | 'structure_database/residue_codes.csv' |
| image_size | not annotated | (300, 220) |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `', '.join`, `Draw.MolToImage`, `ValueError`, `display`, `load_available_PHA_monomers`, `monomer_dict.keys`, `plt.axis`, `plt.figure`, `plt.imshow`, `plt.show`, `smiles_to_mol`, `sorted`.

Explicit return expressions; different branches may return different objects:

```python
img
```

Calls worth inspecting for I/O, state changes or delegated execution: `load_available_PHA_monomers`, `plt.imshow`, `plt.show`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError(f'PHA type not found: {PHA_type}\n\nAvailable PHA types:\n{available}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def show_PHA_monomer(
    PHA_type,
    residue_codes_csv="structure_database/residue_codes.csv",
    image_size=(300, 220),
):

    """

    Display one PHA monomer structure from residue_codes.csv.

    Parameters
    ----------

    PHA_type : str
        PHA type to display, e.g. "3HB" or "4HB".

    residue_codes_csv : str or pathlib.Path, optional
        Path to residue_codes.csv.

    image_size : tuple[int, int], optional
        Size of the rendered molecule image.

    Returns
    -------

    PIL.Image.Image
        Rendered RDKit molecule image.

    """

    monomers = load_available_PHA_monomers(
        residue_codes_csv
    )

    monomer_dict = {
        name: smiles
        for name, smiles in monomers
    }

    if PHA_type not in monomer_dict:
        available = ", ".join(sorted(monomer_dict.keys()))

        raise ValueError(
            f"PHA type not found: {PHA_type}\n\n"
            f"Available PHA types:\n{available}"
        )

    smiles = monomer_dict[PHA_type]

    mol = smiles_to_mol(
        smiles,
        name=PHA_type,
    )

    img = Draw.MolToImage(
        mol,
        size=image_size,
        legend=PHA_type,
    )

    try:
        from IPython.display import display
        display(img)

    except Exception:
        import matplotlib.pyplot as plt

        plt.figure(figsize=(5, 4))
        plt.imshow(img)
        plt.axis("off")
        plt.show()

    return img
```

</details>

<a id="definition-312"></a>

## `load_polymer_smiles`

Source lines 312–374. Named callable; inspect its callers before treating it as a stable public API.

```python
def load_polymer_smiles(polymer_smiles_csv): ...
```

### Purpose and original contract

Load polymer SMILES from polymer_smiles.csv.

Parameters
----------

polymer_smiles_csv : str or pathlib.Path
    Path to polymer_smiles.csv.

Returns
-------

list[tuple[str, str]]
    List of ``(polymer_name, smiles)`` tuples.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| polymer_smiles_csv | not annotated | required |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `FileNotFoundError`, `Path`, `csv.DictReader`, `open`, `polymer_name.strip`, `polymer_smiles_csv.exists`, `polymers.append`, `row.get`, `smiles.strip`, `sorted`.

Explicit return expressions; different branches may return different objects:

```python
sorted(polymers, key=lambda item: item[0])
```

Calls worth inspecting for I/O, state changes or delegated execution: `csv.DictReader`, `open`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
FileNotFoundError(f'Could not find polymer SMILES CSV:\n{polymer_smiles_csv}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def load_polymer_smiles(polymer_smiles_csv):
    """
    Load polymer SMILES from polymer_smiles.csv.

    Parameters
    ----------

    polymer_smiles_csv : str or pathlib.Path
        Path to polymer_smiles.csv.

    Returns
    -------

    list[tuple[str, str]]
        List of ``(polymer_name, smiles)`` tuples.
    """

    polymer_smiles_csv = Path(polymer_smiles_csv)

    if not polymer_smiles_csv.exists():
        raise FileNotFoundError(
            f"Could not find polymer SMILES CSV:\n"
            f"{polymer_smiles_csv}"
        )

    polymers = []

    with open(polymer_smiles_csv, "r", newline="") as f:

        reader = csv.DictReader(f)

        for row in reader:

            polymer_name = (
                row.get("polymer_name")
                or row.get("name")
                or row.get("Name")
                or row.get("polymer")
            )

            smiles = (
                row.get("smiles")
                or row.get("SMILES")
                or row.get("polymer_smiles")
            )

            if polymer_name is None or smiles is None:
                continue

            if polymer_name.strip() == "" or smiles.strip() == "":
                continue

            polymers.append(
                (
                    polymer_name.strip(),
                    smiles.strip(),
                )
            )

    return sorted(
        polymers,
        key=lambda item: item[0],
    )
```

</details>

<a id="definition-377"></a>

## `plot_available_PHA_polymers`

Source lines 377–430. Named callable; inspect its callers before treating it as a stable public API.

```python
def plot_available_PHA_polymers(polymer_smiles_csv='structure_database/polymer_smiles.csv', output_file='available_PHA_polymers.png', mols_per_row=3, image_size=(500, 280)): ...
```

### Purpose and original contract

Plot all available PHA polymers from polymer_smiles.csv.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| polymer_smiles_csv | not annotated | 'structure_database/polymer_smiles.csv' |
| output_file | not annotated | 'available_PHA_polymers.png' |
| mols_per_row | not annotated | 3 |
| image_size | not annotated | (500, 280) |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `Draw.MolsToGridImage`, `Path`, `RuntimeError`, `image.save`, `len`, `load_polymer_smiles`, `mols.append`, `names.append`, `output_file.parent.mkdir`, `print`, `smiles_to_mol`.

Explicit return expressions; different branches may return different objects:

```python
output_file
```

Calls worth inspecting for I/O, state changes or delegated execution: `image.save`, `load_polymer_smiles`, `output_file.parent.mkdir`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
RuntimeError('No valid polymer SMILES found.')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def plot_available_PHA_polymers(
    polymer_smiles_csv="structure_database/polymer_smiles.csv",
    output_file="available_PHA_polymers.png",
    mols_per_row=3,
    image_size=(500, 280),
):
    """
    Plot all available PHA polymers from polymer_smiles.csv.
    """

    output_file = Path(output_file)

    polymers = load_polymer_smiles(
        polymer_smiles_csv
    )

    if len(polymers) == 0:
        raise RuntimeError(
            "No valid polymer SMILES found."
        )

    names = []
    mols = []

    for polymer_name, smiles in polymers:

        mol = smiles_to_mol(
            smiles,
            name=polymer_name,
        )

        names.append(polymer_name)
        mols.append(mol)

    image = Draw.MolsToGridImage(
        mols,
        molsPerRow=mols_per_row,
        subImgSize=image_size,
        legends=names,
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    image.save(output_file)

    print(
        f"Saved PHA polymer overview to:\n"
        f"{output_file}"
    )

    return output_file
```

</details>

<a id="definition-433"></a>

## `show_available_PHA_polymers`

Source lines 433–483. Named callable; inspect its callers before treating it as a stable public API.

```python
def show_available_PHA_polymers(polymer_smiles_csv='structure_database/polymer_smiles.csv', mols_per_row=3, image_size=(500, 280)): ...
```

### Purpose and original contract

Display all available PHA polymers from polymer_smiles.csv.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| polymer_smiles_csv | not annotated | 'structure_database/polymer_smiles.csv' |
| mols_per_row | not annotated | 3 |
| image_size | not annotated | (500, 280) |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `Draw.MolsToGridImage`, `RuntimeError`, `display`, `len`, `load_polymer_smiles`, `mols.append`, `names.append`, `plt.axis`, `plt.figure`, `plt.imshow`, `plt.show`, `smiles_to_mol`.

Explicit return expressions; different branches may return different objects:

```python
img
```

Calls worth inspecting for I/O, state changes or delegated execution: `load_polymer_smiles`, `plt.imshow`, `plt.show`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
RuntimeError('No valid polymer SMILES found.')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def show_available_PHA_polymers(
    polymer_smiles_csv="structure_database/polymer_smiles.csv",
    mols_per_row=3,
    image_size=(500, 280),
):
    """
    Display all available PHA polymers from polymer_smiles.csv.
    """

    polymers = load_polymer_smiles(
        polymer_smiles_csv
    )

    if len(polymers) == 0:
        raise RuntimeError(
            "No valid polymer SMILES found."
        )

    names = []
    mols = []

    for polymer_name, smiles in polymers:

        mol = smiles_to_mol(
            smiles,
            name=polymer_name,
        )

        names.append(polymer_name)
        mols.append(mol)

    img = Draw.MolsToGridImage(
        mols,
        molsPerRow=mols_per_row,
        subImgSize=image_size,
        legends=names,
    )

    try:
        from IPython.display import display
        display(img)

    except Exception:
        import matplotlib.pyplot as plt

        plt.figure(figsize=(14, 10))
        plt.imshow(img)
        plt.axis("off")
        plt.show()

    return img
```

</details>

<a id="definition-486"></a>

## `show_PHA_polymer`

Source lines 486–540. Named callable; inspect its callers before treating it as a stable public API.

```python
def show_PHA_polymer(polymer_name, polymer_smiles_csv='structure_database/polymer_smiles.csv', image_size=(900, 300)): ...
```

### Purpose and original contract

Display one PHA polymer structure from polymer_smiles.csv.

### Inputs

| Argument | Annotation | Default / requirement |
|---|---|---|
| polymer_name | not annotated | required |
| polymer_smiles_csv | not annotated | 'structure_database/polymer_smiles.csv' |
| image_size | not annotated | (900, 300) |

### How to read this implementation

Direct calls (sorted inventory, not execution order): `', '.join`, `Draw.MolToImage`, `ValueError`, `display`, `load_polymer_smiles`, `plt.axis`, `plt.figure`, `plt.imshow`, `plt.show`, `polymer_dict.keys`, `smiles_to_mol`, `sorted`.

Explicit return expressions; different branches may return different objects:

```python
img
```

Calls worth inspecting for I/O, state changes or delegated execution: `load_polymer_smiles`, `plt.imshow`, `plt.show`. This is a name-based reading aid, not a complete effect analysis.

Explicitly raised failures in this body (callees can raise additional errors):

```python
ValueError(f'Polymer not found: {polymer_name}\n\nAvailable polymers:\n{available}')
```

### Implementation for study

<details>
<summary>Read the complete current definition</summary>

```python
def show_PHA_polymer(
    polymer_name,
    polymer_smiles_csv="structure_database/polymer_smiles.csv",
    image_size=(900, 300),
):
    """
    Display one PHA polymer structure from polymer_smiles.csv.
    """

    polymers = load_polymer_smiles(
        polymer_smiles_csv
    )

    polymer_dict = {
        name: smiles
        for name, smiles in polymers
    }

    if polymer_name not in polymer_dict:

        available = ", ".join(
            sorted(polymer_dict.keys())
        )

        raise ValueError(
            f"Polymer not found: {polymer_name}\n\n"
            f"Available polymers:\n{available}"
        )

    smiles = polymer_dict[polymer_name]

    mol = smiles_to_mol(
        smiles,
        name=polymer_name,
    )

    img = Draw.MolToImage(
        mol,
        size=image_size,
        legend=polymer_name,
    )

    try:
        from IPython.display import display
        display(img)

    except Exception:
        import matplotlib.pyplot as plt

        plt.figure(figsize=(12, 4))
        plt.imshow(img)
        plt.axis("off")
        plt.show()

    return img
```

</details>
