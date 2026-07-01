#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""

PHA visualisation utilities.

This module contains helper functions for visualising available PHA monomer

units and generated polymers.

It currently uses RDKit to render 2D molecular depictions from SMILES strings.

"""

from pathlib import Path

import csv

from rdkit import Chem

from rdkit.Chem import Draw

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

            f"{residue_codes_csv}"

        )

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