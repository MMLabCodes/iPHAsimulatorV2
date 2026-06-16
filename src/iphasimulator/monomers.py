"""Curated PHA monomer definitions for the RDKit builder."""

from __future__ import annotations

from dataclasses import dataclass


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


MONOMERS: dict[str, Monomer] = {
    "PHB": Monomer(
        code="PHB",
        polymer_name="poly(3-hydroxybutyrate)",
        residue_code="PHB",
        chiral_smiles="C[C@@H](O)CC(=O)O",
        side_chain_length=1,
    ),
    "PHV": Monomer(
        code="PHV",
        polymer_name="poly(3-hydroxyvalerate)",
        residue_code="PHV",
        chiral_smiles="CC[C@@H](O)CC(=O)O",
        side_chain_length=2,
    ),
    "PHHx": Monomer(
        code="PHHx",
        polymer_name="poly(3-hydroxyhexanoate)",
        residue_code="PHHx",
        chiral_smiles="CCC[C@@H](O)CC(=O)O",
        side_chain_length=3,
    ),
    "PHHep": Monomer(
        code="PHHep",
        polymer_name="poly(3-hydroxyheptanoate)",
        residue_code="PHHep",
        chiral_smiles="CCCC[C@@H](O)CC(=O)O",
        side_chain_length=4,
    ),
    "PHO": Monomer(
        code="PHO",
        polymer_name="poly(3-hydroxyoctanoate)",
        residue_code="PHO",
        chiral_smiles="CCCCC[C@@H](O)CC(=O)O",
        side_chain_length=5,
    ),
    "PHN": Monomer(
        code="PHN",
        polymer_name="poly(3-hydroxynonanoate)",
        residue_code="PHN",
        chiral_smiles="CCCCCC[C@@H](O)CC(=O)O",
        side_chain_length=6,
    ),
    "PHD": Monomer(
        code="PHD",
        polymer_name="poly(3-hydroxydecanoate)",
        residue_code="PHD",
        chiral_smiles="CCCCCCC[C@@H](O)CC(=O)O",
        side_chain_length=7,
    ),
    "PHDD": Monomer(
        code="PHDD",
        polymer_name="poly(3-hydroxydodecanoate)",
        residue_code="PHDD",
        chiral_smiles="CCCCCCCCC[C@@H](O)CC(=O)O",
        side_chain_length=9,
    ),
}

_MONOMER_LOOKUP = {code.upper(): code for code in MONOMERS}
_MONOMER_LOOKUP.update(
    {
        "3HB": "PHB",
        "3HO": "PHO",
        "3HDD": "PHDD",
    }
)


def get_monomer(code: str) -> Monomer:
    """Return a registered monomer by case-insensitive code."""

    if not isinstance(code, str):
        supported = ", ".join(sorted(MONOMERS))
        raise ValueError(f"Unknown monomer {code!r}. Supported monomers: {supported}")

    key = _MONOMER_LOOKUP.get(code.upper())
    if key is None:
        supported = ", ".join(sorted(MONOMERS))
        raise ValueError(f"Unknown monomer {code!r}. Supported monomers: {supported}")

    return MONOMERS[key]
