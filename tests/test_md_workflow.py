from types import SimpleNamespace
from pathlib import Path

from iphasimulator.parameterization.gaff2 import parameterize_gaff2


def test_parameterize_gaff2_writes_expected_ambertools_inputs(tmp_path):
    input_sdf = tmp_path / "PHB4_R.sdf"
    input_sdf.write_text("test sdf\n")
    output_dir = tmp_path / "md_tests" / "PHB4" / "gaff2"
    commands = []

    def fake_runner(command, cwd, text, stdout, stderr):
        commands.append((command, cwd, text, stdout, stderr))
        if command[0] == "antechamber":
            (Path(cwd) / "sqm.out").write_text("sqm raw\n")
        return SimpleNamespace(returncode=0, stdout="ok\n")

    outputs = parameterize_gaff2(
        input_sdf,
        output_dir,
        name="PHB4",
        residue_name="PHA",
        charge_method="gas",
        runner=fake_runner,
        check_tools=False,
    )

    assert outputs.prmtop_path == output_dir / "PHB4.prmtop"
    assert outputs.inpcrd_path == output_dir / "PHB4.inpcrd"
    assert outputs.mol2_path == output_dir / "PHB4.gaff2.mol2"
    assert outputs.frcmod_path == output_dir / "PHB4.gaff2.frcmod"
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
        "PHB4.gaff2.mol2",
        "-fo",
        "mol2",
    ]
    assert "-at" in commands[0][0]
    assert "gaff2" in commands[0][0]
    assert commands[0][0][commands[0][0].index("-c") + 1] == "gas"
    assert commands[1][0] == [
        "parmchk2",
        "-i",
        "PHB4.gaff2.mol2",
        "-f",
        "mol2",
        "-o",
        "PHB4.gaff2.frcmod",
        "-s",
        "gaff2",
    ]
    assert commands[2][0] == ["tleap", "-f", "tleap.in"]

    tleap_input = outputs.tleap_input_path.read_text()
    assert "source leaprc.gaff2" in tleap_input
    assert "loadamberparams PHB4.gaff2.frcmod" in tleap_input
    assert "mol = loadmol2 PHB4.gaff2.mol2" in tleap_input
    assert "saveamberparm mol PHB4.prmtop PHB4.inpcrd" in tleap_input
