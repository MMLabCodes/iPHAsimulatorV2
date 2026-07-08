from iphasimulator.build import build_pha_chain
from iphasimulator.export import to_pdb, to_sdf
from rdkit import Chem


def test_export_sdf_writes_file(tmp_path):
    mol = build_pha_chain("3HB", 4, "R")
    output_path = tmp_path / "P3HB_4.sdf"

    to_sdf(mol, output_path)

    assert output_path.exists()
    assert output_path.stat().st_size > 0
    exported = Chem.SDMolSupplier(str(output_path), removeHs=False)[0]
    assert exported.GetNumAtoms() > mol.GetNumAtoms()
    assert exported.GetConformer().Is3D()


def test_export_pdb_handles_long_side_chain_pha(tmp_path):
    mol = build_pha_chain("3HDD", 4, "R")
    output_path = tmp_path / "P3HDD_4.pdb"

    to_pdb(mol, output_path)

    assert output_path.exists()
    assert output_path.stat().st_size > 0
