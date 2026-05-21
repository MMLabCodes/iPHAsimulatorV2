import pytest
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

from iphasimulator.build import (
    ESTER_BOND,
    build_custom_pha,
    build_pha_by_sidechain,
    build_pha_chain,
)


def _chiral_centres(mol):
    Chem.AssignStereochemistry(mol, cleanIt=True, force=True)
    return Chem.FindMolChiralCenters(mol, includeUnassigned=True)


def _carbon_count(mol):
    return sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)


def _assert_valid_chain(mol, n, stereochemistry, side_chain_carbons):
    centres = _chiral_centres(mol)

    assert isinstance(mol, Chem.Mol)
    assert len(centres) == n
    assert all(label == stereochemistry for _, label in centres)
    assert len(mol.GetSubstructMatches(ESTER_BOND)) == n - 1
    assert _carbon_count(mol) - (3 * n) == side_chain_carbons * n


@pytest.mark.parametrize(
    ("n", "formula"),
    [
        (4, "C16H26O9"),
        (8, "C32H50O17"),
    ],
)
def test_build_phb_r_chain(n, formula):
    mol = build_pha_chain("PHB", n)

    _assert_valid_chain(mol, n, "R", side_chain_carbons=1)
    assert rdMolDescriptors.CalcMolFormula(mol) == formula


@pytest.mark.parametrize(
    ("monomer", "n", "side_chain_carbons"),
    [
        ("PHB", 4, 1),
        ("PHB", 8, 1),
        ("PHO", 4, 5),
        ("PHO", 8, 5),
        ("PHDD", 4, 9),
        ("PHDD", 8, 9),
    ],
)
def test_build_picture_polymer_r_chains(monomer, n, side_chain_carbons):
    mol = build_pha_chain(monomer, n, "R")

    _assert_valid_chain(mol, n, "R", side_chain_carbons)


@pytest.mark.parametrize(
    ("monomer", "side_chain_carbons"),
    [
        ("PHB", 1),
        ("PHV", 2),
        ("PHHx", 3),
        ("PHHep", 4),
        ("PHO", 5),
        ("PHN", 6),
        ("PHD", 7),
        ("PHDD", 9),
    ],
)
def test_build_curated_common_pha_library(monomer, side_chain_carbons):
    mol = build_pha_chain(monomer, 4)

    _assert_valid_chain(mol, 4, "R", side_chain_carbons)


@pytest.mark.parametrize("side_chain_carbons", [1, 5, 9, 12])
def test_build_pha_by_sidechain_generates_linear_r_chains(side_chain_carbons):
    mol = build_pha_by_sidechain(side_chain_carbons, 4)

    _assert_valid_chain(mol, 4, "R", side_chain_carbons)


def test_build_pha_by_sidechain_matches_curated_pho():
    generic = build_pha_by_sidechain(5, 4)
    curated = build_pha_chain("PHO", 4)

    assert Chem.MolToSmiles(generic, isomericSmiles=True) == Chem.MolToSmiles(
        curated, isomericSmiles=True
    )


@pytest.mark.parametrize(
    "monomer_smiles",
    [
        "CC(C)[C@H](O)CC(=O)O",
        "C=C[C@H](O)CC(=O)O",
        "COC[C@H](O)CC(=O)O",
    ],
)
def test_build_custom_pha_accepts_branched_unsaturated_and_functionalised_monomers(
    monomer_smiles,
):
    mol = build_custom_pha(monomer_smiles, 3, "custom")
    centres = _chiral_centres(mol)

    assert isinstance(mol, Chem.Mol)
    assert len(mol.GetSubstructMatches(ESTER_BOND)) == 2
    assert len(centres) == 3
    assert all(label == "R" for _, label in centres)


@pytest.mark.parametrize("n", [0, -1, 1.5, True])
def test_build_phb_rejects_invalid_repeat_units(n):
    with pytest.raises(ValueError, match="repeat units"):
        build_pha_chain("PHB", n)


def test_build_rejects_invalid_monomer_name():
    with pytest.raises(ValueError, match="Unknown monomer"):
        build_pha_chain("PLA", 4)


def test_build_rejects_invalid_stereochemistry():
    with pytest.raises(ValueError, match="Stereochemistry must be R or S"):
        build_pha_chain("PHB", 4, "racemic")


@pytest.mark.parametrize("side_chain_carbons", [0, -1, 1.5, True])
def test_build_pha_by_sidechain_rejects_invalid_side_chain_lengths(side_chain_carbons):
    with pytest.raises(ValueError, match="Side-chain carbons"):
        build_pha_by_sidechain(side_chain_carbons, 4)


def test_build_custom_pha_rejects_non_r_monomer():
    with pytest.raises(ValueError, match="must be R"):
        build_custom_pha("CC(C)[C@@H](O)CC(=O)O", 3, "custom")
