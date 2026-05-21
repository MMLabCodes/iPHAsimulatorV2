import pytest
from rdkit import Chem

from iphasimulator.stereochemistry import (
    validate_chiral_centres,
    validate_r_chiral_centres,
    validate_stereochemistry_option,
)


def test_validate_stereochemistry_option_accepts_r_and_s_case_insensitive():
    assert validate_stereochemistry_option("R") == "R"
    assert validate_stereochemistry_option("r") == "R"
    assert validate_stereochemistry_option("S") == "S"
    assert validate_stereochemistry_option("s") == "S"


@pytest.mark.parametrize("stereochemistry", ["racemic", ""])
def test_validate_stereochemistry_option_rejects_unsupported_values(stereochemistry):
    with pytest.raises(ValueError, match="Stereochemistry must be R or S"):
        validate_stereochemistry_option(stereochemistry)


def test_validate_r_chiral_centres_accepts_expected_r_centres():
    mol = Chem.MolFromSmiles("C[C@@H](O)CC(=O)O")

    validate_r_chiral_centres(mol, expected_count=1)


def test_validate_r_chiral_centres_rejects_wrong_count():
    mol = Chem.MolFromSmiles("C[C@@H](O)CC(=O)O")

    with pytest.raises(ValueError, match="Expected 2 chiral centres"):
        validate_r_chiral_centres(mol, expected_count=2)


def test_validate_r_chiral_centres_rejects_s_centres():
    mol = Chem.MolFromSmiles("C[C@H](O)CC(=O)O")

    with pytest.raises(ValueError, match="Expected all chiral centres to be R"):
        validate_r_chiral_centres(mol, expected_count=1)


def test_validate_r_chiral_centres_rejects_unassigned_centres():
    mol = Chem.MolFromSmiles("CC(O)CC(=O)O")

    with pytest.raises(ValueError, match="Expected all chiral centres to be R"):
        validate_r_chiral_centres(mol, expected_count=1)


def test_validate_chiral_centres_accepts_expected_s_centres():
    mol = Chem.MolFromSmiles("C[C@H](O)CC(=O)O")

    validate_chiral_centres(mol, expected_count=1, stereochemistry="S")
