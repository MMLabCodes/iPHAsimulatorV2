"""Stereochemistry validation helpers."""

from __future__ import annotations

from rdkit import Chem


def validate_stereochemistry_option(stereochemistry: str) -> str:
    """Validate and normalize the requested stereochemistry."""

    if not isinstance(stereochemistry, str):
        raise ValueError("Stereochemistry must be R or S")

    normalized = stereochemistry.upper()
    if normalized not in {"R", "S"}:
        raise ValueError("Stereochemistry must be R or S")
    return normalized


def validate_chiral_centres(
    mol: Chem.Mol, expected_count: int, stereochemistry: str
) -> None:
    """Ensure every repeat unit has one assigned chiral centre."""

    expected_label = validate_stereochemistry_option(stereochemistry)

    Chem.AssignStereochemistry(mol, cleanIt=True, force=True)
    centres = Chem.FindMolChiralCenters(mol, includeUnassigned=True)

    if len(centres) != expected_count:
        raise ValueError(
            f"Expected {expected_count} chiral centres, found {len(centres)}"
        )

    mismatched = [
        (atom_idx, label) for atom_idx, label in centres if label != expected_label
    ]
    if mismatched:
        details = ", ".join(f"atom {atom_idx}: {label}" for atom_idx, label in mismatched)
        raise ValueError(
            f"Expected all chiral centres to be {expected_label}; found {details}"
        )


def validate_r_chiral_centres(mol: Chem.Mol, expected_count: int) -> None:
    """Ensure every repeat unit has one assigned R chiral centre."""

    validate_chiral_centres(mol, expected_count=expected_count, stereochemistry="R")
