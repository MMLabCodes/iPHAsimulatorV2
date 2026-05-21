from types import SimpleNamespace

import pytest

from iphasimulator.system_builders import (
    build_packmol_solvated_system,
    estimate_ion_pairs,
    estimate_tip3p_water_count,
)


POLYMER_PDB = """\
HETATM    1  C1  PHA A   1       0.000   0.000   0.000  1.00  0.00           C
HETATM    2  O1  PHA A   1       0.120   0.000   0.000  1.00  0.00           O
END
"""


def test_estimate_tip3p_water_count_uses_cubic_box_volume():
    assert estimate_tip3p_water_count(3.0) == 901


def test_estimate_ion_pairs_from_molarity_and_box_volume():
    assert estimate_ion_pairs(10.0, 0.15) == 90
    assert estimate_ion_pairs(3.0, 0.0) == 0


def test_build_packmol_solvated_system_writes_input_without_running(tmp_path):
    polymer_path = tmp_path / "PHB4.pdb"
    polymer_path.write_text(POLYMER_PDB)

    outputs = build_packmol_solvated_system(
        [polymer_path],
        tmp_path / "packmol",
        box_size_nm=3.0,
        nacl_concentration_molar=0.15,
        num_polymers=2,
        polymer_spacing_nm=0.8,
        run_packmol=False,
    )

    assert outputs.solvated_pdb_path == tmp_path / "packmol" / "solvated_system.pdb"
    assert outputs.packmol_input_path.exists()
    assert outputs.packmol_log_path.exists()
    assert outputs.copied_polymer_paths[0].exists()
    assert {path.name for path in outputs.support_structure_paths} == {
        "tip3p_water.pdb",
        "sodium_ion.pdb",
        "chloride_ion.pdb",
    }
    assert outputs.water_count == 901
    assert outputs.sodium_count == 2
    assert outputs.chloride_count == 2
    assert outputs.polymer_counts == (2,)

    packmol_input = outputs.packmol_input_path.read_text()
    assert "output solvated_system.pdb" in packmol_input
    assert "structure polymer_1.pdb" in packmol_input
    assert "  number 2" in packmol_input
    assert "structure tip3p_water.pdb" in packmol_input
    assert "structure sodium_ion.pdb" in packmol_input
    assert "structure chloride_ion.pdb" in packmol_input
    assert "  inside box 8.000 8.000 8.000 22.000 22.000 22.000" in packmol_input


def test_build_packmol_solvated_system_runs_packmol_with_stdin(tmp_path):
    polymer_path = tmp_path / "PHB4.pdb"
    polymer_path.write_text(POLYMER_PDB)
    calls = []

    def fake_runner(command, **kwargs):
        calls.append((command, kwargs))
        (kwargs["cwd"] / "solvated_system.pdb").write_text(POLYMER_PDB)
        return SimpleNamespace(returncode=0, stdout="success", stderr="")

    outputs = build_packmol_solvated_system(
        [polymer_path],
        tmp_path / "packmol",
        box_size_nm=4.0,
        nacl_concentration_molar=0.0,
        runner=fake_runner,
    )

    assert calls[0][0] == ["packmol"]
    assert calls[0][1]["cwd"] == tmp_path / "packmol"
    assert "structure tip3p_water.pdb" in calls[0][1]["input"]
    assert "STDOUT:\nsuccess" in outputs.packmol_log_path.read_text()
    assert outputs.solvated_pdb_path.read_text().startswith("CRYST1   40.000")


def test_build_packmol_solvated_system_accepts_multiple_polymer_structures(tmp_path):
    polymer_1 = tmp_path / "PHB4.pdb"
    polymer_2 = tmp_path / "PHO4.pdb"
    polymer_1.write_text(POLYMER_PDB)
    polymer_2.write_text(POLYMER_PDB)

    outputs = build_packmol_solvated_system(
        [polymer_1, polymer_2],
        tmp_path / "packmol",
        box_size_nm=5.0,
        num_polymers=(1, 3),
        run_packmol=False,
    )

    assert outputs.polymer_counts == (1, 3)
    packmol_input = outputs.packmol_input_path.read_text()
    assert "structure polymer_1.pdb" in packmol_input
    assert "structure polymer_2.pdb" in packmol_input


def test_build_packmol_solvated_system_rejects_unsupported_water_model(tmp_path):
    polymer_path = tmp_path / "PHB4.pdb"
    polymer_path.write_text(POLYMER_PDB)

    with pytest.raises(ValueError, match="tip3p"):
        build_packmol_solvated_system(
            [polymer_path],
            tmp_path / "packmol",
            box_size_nm=3.0,
            water_model="spce",
            run_packmol=False,
        )
