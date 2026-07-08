from types import SimpleNamespace
from pathlib import Path
from decimal import Decimal

from iphasimulator.parameterization_gaff2 import (
    _normalize_mol2_charges,
    parameterize_gaff2,
)


def test_parameterize_gaff2_writes_expected_ambertools_inputs(tmp_path):
    input_sdf = tmp_path / "P3HB_4.sdf"
    input_sdf.write_text("test sdf\n")
    output_dir = tmp_path / "md_tests" / "P3HB_4" / "gaff2"
    commands = []

    def fake_runner(command, cwd, text, stdout, stderr):
        commands.append((command, cwd, text, stdout, stderr))
        if command[0] == "antechamber":
            (Path(cwd) / "sqm.out").write_text("sqm raw\n")
        return SimpleNamespace(returncode=0, stdout="ok\n")

    outputs = parameterize_gaff2(
        input_sdf,
        output_dir,
        name="P3HB_4",
        residue_name="PHA",
        charge_method="gas",
        runner=fake_runner,
        check_tools=False,
    )

    assert outputs.prmtop_path == output_dir / "P3HB_4.prmtop"
    assert outputs.inpcrd_path == output_dir / "P3HB_4.inpcrd"
    assert outputs.mol2_path == output_dir / "P3HB_4.gaff2.mol2"
    assert outputs.frcmod_path == output_dir / "P3HB_4.gaff2.frcmod"
    assert outputs.tleap_input_path.exists()
    assert outputs.raw_antechamber_log.read_text() == "ok\n"
    assert "Command: antechamber" in outputs.antechamber_log.read_text()
    assert outputs.sqm_log.read_text() == "sqm raw\n"
    assert outputs.parmchk2_log.read_text() == "ok\n"
    assert outputs.tleap_log.read_text() == "ok\n"
    assert "antechamber_seconds=" in outputs.timing_log.read_text()
    assert outputs.antechamber_seconds >= 0
    assert outputs.parmchk2_seconds >= 0
    assert outputs.tleap_seconds >= 0

    assert commands[0][0][:9] == [
        "antechamber",
        "-i",
        str(input_sdf.resolve()),
        "-fi",
        "sdf",
        "-o",
        "P3HB_4.gaff2.mol2",
        "-fo",
        "mol2",
    ]
    assert "-at" in commands[0][0]
    assert "gaff2" in commands[0][0]
    assert commands[0][0][commands[0][0].index("-c") + 1] == "gas"
    assert commands[1][0] == [
        "parmchk2",
        "-i",
        "P3HB_4.gaff2.mol2",
        "-f",
        "mol2",
        "-o",
        "P3HB_4.gaff2.frcmod",
        "-s",
        "gaff2",
    ]
    assert commands[2][0] == ["tleap", "-f", "tleap.in"]

    tleap_input = outputs.tleap_input_path.read_text()
    assert "source leaprc.gaff2" in tleap_input
    assert "loadamberparams P3HB_4.gaff2.frcmod" in tleap_input
    assert "mol = loadmol2 P3HB_4.gaff2.mol2" in tleap_input
    assert "saveamberparm mol P3HB_4.prmtop P3HB_4.inpcrd" in tleap_input


def test_normalize_mol2_charges_removes_rounding_residue(tmp_path):
    mol2_path = tmp_path / "P3HDD_4.gaff2.mol2"
    mol2_path.write_text(
        "\n".join(
            [
                "@<TRIPOS>MOLECULE",
                "P3HDD_4",
                "@<TRIPOS>ATOM",
                "      1 C1          0.0 0.0 0.0 c3 1 PHA -0.503500",
                "      2 H1          0.0 0.0 0.0 hc 1 PHA  0.496501",
                "@<TRIPOS>BOND",
                "     1    1    2 1",
                "",
            ]
        )
    )

    original_charge, normalized_charge = _normalize_mol2_charges(
        mol2_path,
        net_charge=0,
    )

    assert original_charge == Decimal("-0.006999")
    assert normalized_charge == Decimal("0")
    atom_charges = [
        Decimal(line.split()[8])
        for line in mol2_path.read_text().splitlines()
        if line.strip().startswith(("1 C1", "2 H1"))
    ]
    assert sum(atom_charges) == Decimal("0")
