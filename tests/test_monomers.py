import pytest
from rdkit import Chem

from iphasimulator.monomers import MONOMERS, Monomer, get_monomer


def test_monomer_registry_contains_v01_monomers():
    assert set(MONOMERS) == {
        "PHB",
        "PHV",
        "PHHx",
        "PHHep",
        "PHO",
        "PHN",
        "PHD",
        "PHDD",
    }
    assert all(isinstance(monomer, Monomer) for monomer in MONOMERS.values())


@pytest.mark.parametrize("code", ["PHB", "PHV", "PHHx", "PHHep", "PHO", "PHN", "PHD", "PHDD"])
def test_registered_monomers_have_valid_chiral_smiles(code):
    monomer = MONOMERS[code]
    mol = Chem.MolFromSmiles(monomer.chiral_smiles)
    centres = Chem.FindMolChiralCenters(mol, includeUnassigned=True)

    assert mol is not None
    assert len(centres) == 1
    assert centres[0][1] == monomer.expected_stereochemistry


@pytest.mark.parametrize(
    ("code", "polymer_name", "residue_code", "side_chain_length"),
    [
        ("PHB", "poly(3-hydroxybutyrate)", "PHB", 1),
        ("PHV", "poly(3-hydroxyvalerate)", "PHV", 2),
        ("PHHx", "poly(3-hydroxyhexanoate)", "PHHx", 3),
        ("PHHep", "poly(3-hydroxyheptanoate)", "PHHep", 4),
        ("PHO", "poly(3-hydroxyoctanoate)", "PHO", 5),
        ("PHN", "poly(3-hydroxynonanoate)", "PHN", 6),
        ("PHD", "poly(3-hydroxydecanoate)", "PHD", 7),
        ("PHDD", "poly(3-hydroxydodecanoate)", "PHDD", 9),
    ],
)
def test_registered_monomers_store_expected_metadata(
    code, polymer_name, residue_code, side_chain_length
):
    monomer = MONOMERS[code]

    assert monomer.polymer_name == polymer_name
    assert monomer.residue_code == residue_code
    assert monomer.side_chain_length == side_chain_length
    assert monomer.expected_stereochemistry == "R"


def test_get_monomer_is_case_insensitive():
    assert get_monomer("phb") is MONOMERS["PHB"]
    assert get_monomer("phhx") is MONOMERS["PHHx"]
    assert get_monomer("phhep") is MONOMERS["PHHep"]


def test_get_monomer_rejects_unknown_code():
    with pytest.raises(ValueError, match="Unknown monomer"):
        get_monomer("PLA")
