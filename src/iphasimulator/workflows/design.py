"""User-facing polymer design helpers for tutorial notebooks."""

from __future__ import annotations

from dataclasses import dataclass

from rdkit import Chem

from iphasimulator.build import build_custom_pha, build_pha_by_sidechain, build_pha_chain
from iphasimulator.monomers import MONOMERS
from iphasimulator.naming import monomer_to_polymer_code, oligomer_name


@dataclass(frozen=True)
class PolymerDesign:
    """A plain-language request for one PHA oligomer.

    Use exactly one of ``common_name``, ``side_chain_carbons``, or
    ``custom_monomer_smiles``.
    """

    degree: int
    common_name: str | None = None
    side_chain_carbons: int | None = None
    custom_monomer_smiles: str | None = None
    name: str = "custom_pha"
    stereochemistry: str = "R"


def supported_polymer_table() -> list[dict[str, object]]:
    """Return curated PHA options as notebook-friendly records."""

    return [
        {
            "code": monomer.code,
            "polymer_code": monomer_to_polymer_code(monomer.code),
            "polymer_name": monomer.polymer_name,
            "residue_code": monomer.residue_code,
            "head_residue_code": monomer.head_residue_code,
            "main_residue_code": monomer.main_residue_code,
            "tail_residue_code": monomer.tail_residue_code,
            "side_chain_carbons": monomer.side_chain_length,
            "monomer_smiles": monomer.chiral_smiles,
        }
        for monomer in MONOMERS.values()
    ]


def _selected_design_modes(design: PolymerDesign) -> int:
    return sum(
        option is not None
        for option in (
            design.common_name,
            design.side_chain_carbons,
            design.custom_monomer_smiles,
        )
    )


def design_polymer(design: PolymerDesign) -> tuple[str, Chem.Mol]:
    """Build a PHA oligomer from a plain user design request."""

    selected_modes = _selected_design_modes(design)
    if selected_modes != 1:
        raise ValueError(
            "Choose exactly one design mode: common_name, side_chain_carbons, "
            "or custom_monomer_smiles."
        )

    if design.common_name is not None:
        name = oligomer_name(design.common_name, design.degree)
        return name, build_pha_chain(
            design.common_name,
            design.degree,
            design.stereochemistry,
        )

    if design.side_chain_carbons is not None:
        name = f"PHA_C{design.side_chain_carbons}_{design.degree}_R"
        return name, build_pha_by_sidechain(
            design.side_chain_carbons,
            design.degree,
        )

    name = f"{design.name}{design.degree}_R"
    return name, build_custom_pha(
        design.custom_monomer_smiles or "",
        design.degree,
        design.name,
    )
