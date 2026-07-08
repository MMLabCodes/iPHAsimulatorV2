import pytest
from rdkit import Chem

from iphasimulator.monomers import MONOMERS, Monomer, get_monomer


def test_monomer_registry_contains_canonical_monomers():
    assert set(MONOMERS) == {
        "3HB",
        "3HV",
        "3HHx",
        "3HHep",
        "3HO",
        "3HN",
        "3HD",
        "3HDD",
    }
    assert all(isinstance(monomer, Monomer) for monomer in MONOMERS.values())


@pytest.mark.parametrize(
    "code", ["3HB", "3HV", "3HHx", "3HHep", "3HO", "3HN", "3HD", "3HDD"]
)
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
        ("3HB", "poly(3-hydroxybutyrate)", "3HB", 1),
        ("3HV", "poly(3-hydroxyvalerate)", "3HV", 2),
        ("3HHx", "poly(3-hydroxyhexanoate)", "3HHx", 3),
        ("3HHep", "poly(3-hydroxyheptanoate)", "3HHep", 4),
        ("3HO", "poly(3-hydroxyoctanoate)", "3HO", 5),
        ("3HN", "poly(3-hydroxynonanoate)", "3HN", 6),
        ("3HD", "poly(3-hydroxydecanoate)", "3HD", 7),
        ("3HDD", "poly(3-hydroxydodecanoate)", "3HDD", 9),
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


def test_registered_monomers_store_head_main_tail_residue_codes():
    monomer = MONOMERS["3HB"]

    assert monomer.head_residue_code == "3HB_H"
    assert monomer.main_residue_code == "3HB_M"
    assert monomer.tail_residue_code == "3HB_T"


def test_get_monomer_is_case_insensitive():
    assert get_monomer("3hb") is MONOMERS["3HB"]
    assert get_monomer("3hhx") is MONOMERS["3HHx"]
    assert get_monomer("3hhep") is MONOMERS["3HHep"]


@pytest.mark.parametrize(
    ("legacy_name", "registry_code"),
    [("PHB", "3HB"), ("PHO", "3HO"), ("PHDD", "3HDD")],
)
def test_get_monomer_accepts_legacy_common_names(legacy_name, registry_code):
    assert get_monomer(legacy_name) is MONOMERS[registry_code]


def test_get_monomer_rejects_unknown_code():
    with pytest.raises(ValueError, match="Unknown monomer"):
        get_monomer("PLA")
