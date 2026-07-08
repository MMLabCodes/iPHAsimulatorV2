"""Curated PHA monomer definitions for the RDKit builder."""

from __future__ import annotations

from dataclasses import dataclass

from iphasimulator.naming import (
    canonical_monomer_code,
    residue_variant_names,
)


@dataclass(frozen=True)
class Monomer:
    """A 3-hydroxyalkanoate monomer entry.

    ``chiral_smiles`` stores the free 3-hydroxy acid with explicit R chirality.
    ``side_chain_length`` is the number of carbons in the alkyl side chain.
    """

    code: str
    polymer_name: str
    residue_code: str
    chiral_smiles: str
    side_chain_length: int
    expected_stereochemistry: str = "R"

    @property
    def side_chain(self) -> str:
        """Return the straight saturated alkyl side-chain SMILES fragment."""

        return "C" * self.side_chain_length

    @property
    def head_residue_code(self) -> str:
        """Return the head residue variant code for this monomer."""

        return residue_variant_names(self.code)[0]

    @property
    def main_residue_code(self) -> str:
        """Return the main-chain residue variant code for this monomer."""

        return residue_variant_names(self.code)[1]

    @property
    def tail_residue_code(self) -> str:
        """Return the tail residue variant code for this monomer."""

        return residue_variant_names(self.code)[2]


MONOMERS: dict[str, Monomer] = {
    "3HB": Monomer(
        code="3HB",
        polymer_name="poly(3-hydroxybutyrate)",
        residue_code="3HB",
        chiral_smiles="C[C@@H](O)CC(=O)O",
        side_chain_length=1,
    ),
    "3HV": Monomer(
        code="3HV",
        polymer_name="poly(3-hydroxyvalerate)",
        residue_code="3HV",
        chiral_smiles="CC[C@@H](O)CC(=O)O",
        side_chain_length=2,
    ),
    "3HHx": Monomer(
        code="3HHx",
        polymer_name="poly(3-hydroxyhexanoate)",
        residue_code="3HHx",
        chiral_smiles="CCC[C@@H](O)CC(=O)O",
        side_chain_length=3,
    ),
    "3HHep": Monomer(
        code="3HHep",
        polymer_name="poly(3-hydroxyheptanoate)",
        residue_code="3HHep",
        chiral_smiles="CCCC[C@@H](O)CC(=O)O",
        side_chain_length=4,
    ),
    "3HO": Monomer(
        code="3HO",
        polymer_name="poly(3-hydroxyoctanoate)",
        residue_code="3HO",
        chiral_smiles="CCCCC[C@@H](O)CC(=O)O",
        side_chain_length=5,
    ),
    "3HN": Monomer(
        code="3HN",
        polymer_name="poly(3-hydroxynonanoate)",
        residue_code="3HN",
        chiral_smiles="CCCCCC[C@@H](O)CC(=O)O",
        side_chain_length=6,
    ),
    "3HD": Monomer(
        code="3HD",
        polymer_name="poly(3-hydroxydecanoate)",
        residue_code="3HD",
        chiral_smiles="CCCCCCC[C@@H](O)CC(=O)O",
        side_chain_length=7,
    ),
    "3HDD": Monomer(
        code="3HDD",
        polymer_name="poly(3-hydroxydodecanoate)",
        residue_code="3HDD",
        chiral_smiles="CCCCCCCCC[C@@H](O)CC(=O)O",
        side_chain_length=9,
    ),
}


def get_monomer(code: str) -> Monomer:
    """Return a registered monomer by case-insensitive code."""

    if not isinstance(code, str):
        supported = ", ".join(sorted(MONOMERS))
        raise ValueError(f"Unknown monomer {code!r}. Supported monomers: {supported}")

    try:
        key = canonical_monomer_code(code)
    except ValueError as exc:
        supported = ", ".join(sorted(MONOMERS))
        raise ValueError(
            f"Unknown monomer {code!r}. Supported monomers: {supported}"
        ) from exc

    return MONOMERS[key]
