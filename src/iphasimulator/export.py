"""Export helpers for RDKit PHA molecules."""

from __future__ import annotations

from pathlib import Path

from rdkit import Chem
from rdkit.Chem import AllChem


def prepare_molecule_3d(mol: Chem.Mol) -> Chem.Mol:
    """Return a copy with explicit hydrogens and an optimized 3D conformer."""

    embedded = Chem.AddHs(Chem.Mol(mol))
    params = AllChem.ETKDGv3()
    params.randomSeed = 0xC0FFEE

    status = AllChem.EmbedMolecule(embedded, params)
    if status != 0:
        params.useRandomCoords = True
        params.randomSeed = 0xC0FFEE
        status = AllChem.EmbedMolecule(embedded, params)
    if status != 0:
        raise ValueError("RDKit ETKDG embedding failed")

    AllChem.UFFOptimizeMolecule(embedded, maxIters=200)
    return embedded


def to_sdf(mol: Chem.Mol, path: str | Path) -> None:
    """Embed an RDKit molecule with ETKDG and write it to SDF."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    embedded = prepare_molecule_3d(mol)
    writer = Chem.SDWriter(str(output_path))
    try:
        writer.write(embedded)
    finally:
        writer.close()


def to_pdb(mol: Chem.Mol, path: str | Path) -> None:
    """Embed an RDKit molecule with ETKDG and write it to PDB."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    embedded = prepare_molecule_3d(mol)
    Chem.MolToPDBFile(embedded, str(output_path))
