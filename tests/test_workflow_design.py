import pytest
from rdkit import Chem

from iphasimulator.workflows import PolymerDesign, design_polymer, supported_polymer_table


def test_supported_polymer_table_contains_curated_names():
    rows = supported_polymer_table()

    assert {row["code"] for row in rows} >= {"PHB", "PHO", "PHDD"}
    assert all("polymer_name" in row for row in rows)


def test_design_polymer_builds_common_name():
    name, mol = design_polymer(PolymerDesign(common_name="PHB", degree=4))

    assert name == "PHB4_R"
    assert isinstance(mol, Chem.Mol)


def test_design_polymer_builds_generic_side_chain():
    name, mol = design_polymer(PolymerDesign(side_chain_carbons=5, degree=4))

    assert name == "PHA_C5_4_R"
    assert isinstance(mol, Chem.Mol)


def test_design_polymer_builds_custom_monomer():
    name, mol = design_polymer(
        PolymerDesign(
            custom_monomer_smiles="C=C[C@H](O)CC(=O)O",
            degree=3,
            name="unsaturated_pha",
        )
    )

    assert name == "unsaturated_pha3_R"
    assert isinstance(mol, Chem.Mol)


def test_design_polymer_requires_one_mode():
    with pytest.raises(ValueError, match="exactly one"):
        design_polymer(PolymerDesign(common_name="PHB", side_chain_carbons=1, degree=4))
