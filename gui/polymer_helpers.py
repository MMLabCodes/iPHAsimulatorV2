#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Polymer display and sequence helpers for the iPHAsimulatorV2 GUI.

This module contains lightweight GUI calculations. Polymer construction
and parameterisation remain in the iPHAsimulator backend modules.
"""

from rdkit import Chem
from rdkit.Chem import Draw


def get_polymer_name(sequence):
    """
    Generate a standard polymer name from a monomer sequence.

    Parameters
    ----------
    sequence : list[str]
        Ordered PHA monomer sequence.

    Returns
    -------
    str or None
        Generated polymer name, or None for an empty sequence.

    Examples
    --------
    ["3HB"] * 10

        -> P3HB_10

    ["3HB", "4HB", "3HB", "4HB"]

        -> co_P3HB_P4HB_custom_4
    """

    if not sequence:
        return None

    unique_units = []

    for unit in sequence:
        if unit not in unique_units:
            unique_units.append(unit)

    if len(unique_units) == 1:
        return (
            f"P{unique_units[0]}_"
            f"{len(sequence)}"
        )

    unique_name = "_".join(
        f"P{unit}"
        for unit in unique_units
    )

    return (
        f"co_{unique_name}_"
        f"custom_{len(sequence)}"
    )


def generate_polymer_smiles_from_sequence(
    sequence,
    smiles_lookup,
):
    """
    Generate a polymer SMILES string from an ordered PHA sequence.

    Parameters
    ----------
    sequence : list[str]
        Ordered PHA monomer sequence.

    smiles_lookup : dict[str, str]
        Mapping from PHA type to monomer SMILES.

    Returns
    -------
    str or None
        Generated polymer SMILES, or None for an empty sequence.
    """

    if not sequence:
        return None

    missing_types = [
        pha_type
        for pha_type in sequence
        if pha_type not in smiles_lookup
    ]

    if missing_types:
        raise KeyError(
            "Missing monomer SMILES for:\n"
            + "\n".join(
                sorted(
                    set(missing_types)
                )
            )
        )

    polymer_smiles_parts = []

    for index, pha_type in enumerate(sequence):
        smiles = str(
            smiles_lookup[pha_type]
        ).strip()

        if not smiles:
            raise ValueError(
                f"Empty monomer SMILES for {pha_type}"
            )

        if index == len(sequence) - 1:
            polymer_smiles_parts.append(
                smiles
            )

        else:
            polymer_smiles_parts.append(
                smiles[:-1]
            )

    return "".join(
        polymer_smiles_parts
    )


def draw_monomer(
    pha_type,
    monomer_smiles,
    width=420,
    height=300,
):
    """
    Draw one PHA monomer with RDKit.

    Parameters
    ----------
    pha_type : str
        Registered PHA type.

    monomer_smiles : dict[str, str]
        Mapping from PHA type to monomer SMILES.

    width : int, optional
        Image width.

    height : int, optional
        Image height.

    Returns
    -------
    PIL.Image.Image or None
        Rendered image, or None if RDKit cannot parse the SMILES.
    """

    if pha_type not in monomer_smiles:
        raise KeyError(
            f"No monomer SMILES registered for {pha_type}"
        )

    smiles = monomer_smiles[
        pha_type
    ]

    molecule = Chem.MolFromSmiles(
        smiles
    )

    if molecule is None:
        return None

    return Draw.MolToImage(
        molecule,
        size=(
            width,
            height,
        ),
        legend=pha_type,
    )


def draw_polymer(
    polymer_smiles,
    polymer_name,
    width=1200,
    height=360,
):
    """
    Draw a generated polymer with RDKit.

    Parameters
    ----------
    polymer_smiles : str
        Polymer SMILES to render.

    polymer_name : str
        Label displayed beneath the molecule.

    width : int, optional
        Image width.

    height : int, optional
        Image height.

    Returns
    -------
    PIL.Image.Image or None
        Rendered image, or None if RDKit cannot parse the SMILES.
    """

    if not polymer_smiles:
        return None

    molecule = Chem.MolFromSmiles(
        polymer_smiles
    )

    if molecule is None:
        return None

    return Draw.MolToImage(
        molecule,
        size=(
            width,
            height,
        ),
        legend=polymer_name or "",
    )


def get_unique_sequence_units(sequence):
    """
    Return unique monomers while preserving sequence order.
    """

    unique_units = []

    for unit in sequence:
        if unit not in unique_units:
            unique_units.append(unit)

    return unique_units


def repeat_sequence(
    sequence,
    repetitions,
):
    """
    Return a repeated copy of a polymer sequence.
    """

    repetitions = int(
        repetitions
    )

    if repetitions < 1:
        raise ValueError(
            "repetitions must be at least 1."
        )

    return list(sequence) * repetitions