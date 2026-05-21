import os
from pathlib import Path
from types import SimpleNamespace

import pytest

from iphasimulator.simulation.gromacs_runner import (
    GROMACS_MDP_TEMPLATE_NAMES,
    check_gromacs_minimization_inputs,
    create_gromacs_simulation_box,
    prepare_gromacs_run_folder,
    run_gromacs_local_minimization,
    validate_gromacs_box_against_mdp,
    validate_gromacs_run_folder,
    validate_gromacs_coordinate_topology_counts,
    validate_gromacs_solvated_topology,
    validate_gromacs_solvation_grompp,
    write_gromacs_run_files,
    write_gromacs_solvation_files,
)


def _fake_editconf_runner(command, **kwargs):
    cwd = kwargs["cwd"]
    input_path = cwd / command[command.index("-f") + 1]
    output_path = cwd / command[command.index("-o") + 1]
    lines = input_path.read_text().splitlines()
    lines[-1] = "   3.00000   3.00000   3.00000"
    output_path.write_text("\n".join(lines) + "\n")
    return SimpleNamespace(returncode=0, stdout="boxed", stderr="")


def test_write_gromacs_run_files_writes_mdp_and_script(tmp_path):
    outputs = write_gromacs_run_files(tmp_path, system_name="system")

    assert outputs.minim_mdp_path.exists()
    assert outputs.nvt_mdp_path.exists()
    assert outputs.npt_mdp_path.exists()
    assert outputs.production_mdp_path.exists()
    assert outputs.run_script_path.exists()
    assert os.access(outputs.run_script_path, os.X_OK)

    assert "integrator      = steep" in outputs.minim_mdp_path.read_text()
    assert "tcoupl                  = V-rescale" in outputs.nvt_mdp_path.read_text()
    assert "pcoupl                  = C-rescale" in outputs.npt_mdp_path.read_text()
    assert "nstxout-compressed" in outputs.production_mdp_path.read_text()

    script = outputs.run_script_path.read_text()
    assert "gmx grompp -f minim.mdp -c system.gro -p system.top -o minim.tpr" in script
    assert "gmx mdrun -deffnm minim" in script
    assert "gmx grompp -f nvt.mdp -c minim.gro -p system.top -o nvt.tpr" in script
    assert "gmx mdrun -deffnm nvt" in script
    assert "gmx grompp -f npt.mdp -c nvt.gro -p system.top -o npt.tpr" in script
    assert "gmx mdrun -deffnm npt" in script
    assert (
        "gmx grompp -f production.mdp -c npt.gro -p system.top -o production.tpr"
        in script
    )
    assert "gmx mdrun -deffnm production" in script


def test_write_gromacs_run_files_rejects_empty_system_name(tmp_path):
    with pytest.raises(ValueError, match="system_name"):
        write_gromacs_run_files(tmp_path, system_name=" ")


def test_prepare_gromacs_run_folder_writes_default_polymer_folder(
    monkeypatch,
    tmp_path,
):
    prmtop_path = tmp_path / "PHB4.prmtop"
    inpcrd_path = tmp_path / "PHB4.inpcrd"
    prmtop_path.write_text("topology")
    inpcrd_path.write_text("coordinates")
    output_dir = tmp_path / "gromacs"

    def fake_convert_amber_to_gromacs(prmtop_file, inpcrd_file, output_dir, system_name):
        output_path = Path(output_dir)
        top_path = output_path / f"{system_name}.top"
        gro_path = output_path / f"{system_name}.gro"
        output_path.mkdir(parents=True, exist_ok=True)
        top_path.write_text("[ system ]\nPHB4\n")
        gro_path.write_text("PHB4\n3\n    1PHA      C1    1   0.0   0.0   0.0\n    1PHA      C2    2   0.1   0.0   0.0\n    1PHA      O1    3   0.2   0.0   0.0\n   1.0   1.0   1.0\n")
        return SimpleNamespace(top_path=top_path, gro_path=gro_path)

    monkeypatch.setattr(
        "iphasimulator.simulation.gromacs_runner.convert_amber_to_gromacs",
        fake_convert_amber_to_gromacs,
    )

    outputs = prepare_gromacs_run_folder(
        prmtop_path,
        inpcrd_path,
        output_dir,
        "PHB4",
        runner=_fake_editconf_runner,
    )

    assert outputs.workflow_type == "polymer"
    assert outputs.output_dir == output_dir
    assert outputs.dry_polymer_dir == output_dir / "dry_polymer"
    assert outputs.solvated_polymer_dir == output_dir / "solvated_polymer"
    assert outputs.charmm_gui_membrane_dir == output_dir / "charmm_gui_membrane"
    assert outputs.step5_input_gro_path == output_dir / "dry_polymer" / "step5_input.gro"
    assert outputs.topol_top_path == output_dir / "dry_polymer" / "topol.top"
    assert outputs.index_ndx_path == output_dir / "dry_polymer" / "index.ndx"
    assert outputs.step5_input_gro_path.exists()
    assert outputs.topol_top_path.exists()
    assert outputs.index_ndx_path.read_text() == "[ System ]\n1 2 3\n"
    assert set(GROMACS_MDP_TEMPLATE_NAMES) <= {path.name for path in outputs.mdp_paths}
    assert "step6.6_equilibration.mdp" in {path.name for path in outputs.mdp_paths}
    assert outputs.local_script_path.exists()
    assert outputs.hpc_script_path.exists()
    assert outputs.charmm_gui_membrane_hpc_script_path.exists()
    assert os.access(outputs.local_script_path, os.X_OK)
    assert os.access(outputs.hpc_script_path, os.X_OK)
    assert os.access(outputs.charmm_gui_membrane_hpc_script_path, os.X_OK)

    local_script = outputs.local_script_path.read_text()
    assert (
        "gmx grompp -f step6.0_minimization.mdp -c step5_input.gro -r step5_input.gro "
        "-p topol.top -n index.ndx -o step6.0_minimization.tpr"
    ) in local_script

    hpc_script = outputs.hpc_script_path.read_text()
    assert "# - timestep: 0.002 ps (2 fs)" in hpc_script
    assert (
        "# step6.1_nvt: 100 ps NVT at 300 K; V-rescale thermostat; "
        "no pressure coupling; generates initial velocities."
    ) in hpc_script
    assert (
        "# step7_production: 100 ns production MD at 300 K and 1 bar; "
        "isotropic C-rescale pressure coupling."
    ) in hpc_script
    assert (
        "gmx grompp -f step6.1_nvt.mdp -c step6.0_minimization.gro "
        "-r step5_input.gro -p topol.top -n index.ndx -o step6.1_nvt.tpr"
    ) in hpc_script
    assert (
        "gmx grompp -f step6.2_npt.mdp -c step6.1_nvt.gro "
        "-r step5_input.gro -p topol.top -n index.ndx -o step6.2_npt.tpr"
    ) in hpc_script
    assert (
        "gmx grompp -f step7_production.mdp -c step6.2_npt.gro "
        "-r step5_input.gro -p topol.top -n index.ndx -o step7_production.tpr"
    ) in hpc_script
    assert "step6.3_equilibration" not in hpc_script

    charmm_hpc_script = outputs.charmm_gui_membrane_hpc_script_path.read_text()
    assert "# Workflow type: charmm_gui_membrane" in charmm_hpc_script
    assert "step6.1_equilibration.mdp" in charmm_hpc_script
    assert "step6.6_equilibration.mdp" in charmm_hpc_script
    assert (outputs.solvated_polymer_dir / "topol.top").exists()
    assert (outputs.solvated_polymer_dir / "step5_input.gro").exists()
    assert (outputs.solvated_polymer_dir / "index.ndx").exists()
    assert (outputs.charmm_gui_membrane_dir / "topol.top").exists()


def test_prepare_gromacs_run_folder_copies_existing_index(monkeypatch, tmp_path):
    prmtop_path = tmp_path / "PHB4.prmtop"
    inpcrd_path = tmp_path / "PHB4.inpcrd"
    index_path = tmp_path / "custom.ndx"
    prmtop_path.write_text("topology")
    inpcrd_path.write_text("coordinates")
    index_path.write_text("[ Custom ]\n1\n")

    def fake_convert_amber_to_gromacs(prmtop_file, inpcrd_file, output_dir, system_name):
        output_path = Path(output_dir)
        top_path = output_path / f"{system_name}.top"
        gro_path = output_path / f"{system_name}.gro"
        output_path.mkdir(parents=True, exist_ok=True)
        top_path.write_text("[ system ]\nPHB4\n")
        gro_path.write_text("PHB4\n1\n    1PHA      C1    1   0.0   0.0   0.0\n   1.0   1.0   1.0\n")
        return SimpleNamespace(top_path=top_path, gro_path=gro_path)

    monkeypatch.setattr(
        "iphasimulator.simulation.gromacs_runner.convert_amber_to_gromacs",
        fake_convert_amber_to_gromacs,
    )

    outputs = prepare_gromacs_run_folder(
        prmtop_path,
        inpcrd_path,
        tmp_path / "gromacs",
        "PHB4",
        index_file=index_path,
        runner=_fake_editconf_runner,
    )

    assert outputs.index_ndx_path.read_text() == "[ Custom ]\n1\n"


def test_prepare_gromacs_run_folder_writes_charmm_gui_membrane_workflow(
    monkeypatch,
    tmp_path,
):
    prmtop_path = tmp_path / "PHB4.prmtop"
    inpcrd_path = tmp_path / "PHB4.inpcrd"
    prmtop_path.write_text("topology")
    inpcrd_path.write_text("coordinates")

    def fake_convert_amber_to_gromacs(prmtop_file, inpcrd_file, output_dir, system_name):
        output_path = Path(output_dir)
        top_path = output_path / f"{system_name}.top"
        gro_path = output_path / f"{system_name}.gro"
        output_path.mkdir(parents=True, exist_ok=True)
        top_path.write_text("[ system ]\nPHB4\n")
        gro_path.write_text("PHB4\n1\n    1PHA      C1    1   0.0   0.0   0.0\n   1.0   1.0   1.0\n")
        return SimpleNamespace(top_path=top_path, gro_path=gro_path)

    monkeypatch.setattr(
        "iphasimulator.simulation.gromacs_runner.convert_amber_to_gromacs",
        fake_convert_amber_to_gromacs,
    )

    outputs = prepare_gromacs_run_folder(
        prmtop_path,
        inpcrd_path,
        tmp_path / "gromacs",
        "PHB4",
        workflow_type="charmm_gui_membrane",
        runner=_fake_editconf_runner,
    )

    assert outputs.workflow_type == "charmm_gui_membrane"
    assert "step6.6_equilibration.mdp" in {path.name for path in outputs.mdp_paths}
    hpc_script = outputs.hpc_script_path.read_text()
    assert "# Workflow type: charmm_gui_membrane" in hpc_script
    assert "step6.1_equilibration.mdp" in hpc_script
    assert "step6.1_nvt.mdp" not in hpc_script
    assert outputs.charmm_gui_membrane_hpc_script_path.exists()


def test_prepare_gromacs_run_folder_rejects_unknown_workflow(tmp_path):
    with pytest.raises(ValueError, match="workflow_type"):
        prepare_gromacs_run_folder(
            tmp_path / "PHB4.prmtop",
            tmp_path / "PHB4.inpcrd",
            tmp_path / "gromacs",
            "PHB4",
            workflow_type="unknown",
        )


def test_validate_gromacs_run_folder_treats_no_includes_as_standalone(tmp_path):
    topol_path = tmp_path / "topol.top"
    topol_path.write_text(
        "\n".join(
            [
                "; This is a standalone topology file",
                "[ defaults ]",
                "1 2 yes 0.5 0.83333333",
                "",
            ]
        )
    )

    validation = validate_gromacs_run_folder(tmp_path)

    assert validation.valid
    assert validation.is_standalone
    assert validation.included_files == ()
    assert validation.missing_files == ()


def test_validate_gromacs_run_folder_accepts_existing_includes(tmp_path):
    toppar_dir = tmp_path / "toppar"
    toppar_dir.mkdir()
    included_path = toppar_dir / "polymer.itp"
    included_path.write_text("[ moleculetype ]\n")
    (tmp_path / "topol.top").write_text('#include "toppar/polymer.itp"\n')

    validation = validate_gromacs_run_folder(tmp_path)

    assert validation.valid
    assert not validation.is_standalone
    assert validation.included_files == (included_path,)
    assert validation.missing_files == ()


def test_validate_gromacs_run_folder_reports_missing_includes(tmp_path):
    missing_path = tmp_path / "toppar" / "missing.itp"
    (tmp_path / "topol.top").write_text('#include "toppar/missing.itp"\n')

    validation = validate_gromacs_run_folder(tmp_path)

    assert not validation.valid
    assert not validation.is_standalone
    assert validation.missing_files == (missing_path,)


def test_prepare_gromacs_run_folder_raises_for_missing_topology_include(
    monkeypatch,
    tmp_path,
):
    prmtop_path = tmp_path / "PHB4.prmtop"
    inpcrd_path = tmp_path / "PHB4.inpcrd"
    prmtop_path.write_text("topology")
    inpcrd_path.write_text("coordinates")

    def fake_convert_amber_to_gromacs(prmtop_file, inpcrd_file, output_dir, system_name):
        output_path = Path(output_dir)
        top_path = output_path / f"{system_name}.top"
        gro_path = output_path / f"{system_name}.gro"
        output_path.mkdir(parents=True, exist_ok=True)
        top_path.write_text('#include "toppar/missing.itp"\n')
        gro_path.write_text("PHB4\n1\n    1PHA      C1    1   0.0   0.0   0.0\n   1.0   1.0   1.0\n")
        return SimpleNamespace(top_path=top_path, gro_path=gro_path)

    monkeypatch.setattr(
        "iphasimulator.simulation.gromacs_runner.convert_amber_to_gromacs",
        fake_convert_amber_to_gromacs,
    )

    with pytest.raises(FileNotFoundError, match="missing files"):
        prepare_gromacs_run_folder(
            prmtop_path,
            inpcrd_path,
            tmp_path / "gromacs",
            "PHB4",
            runner=_fake_editconf_runner,
        )


def test_check_gromacs_minimization_inputs_reports_ready_folder(tmp_path):
    for filename in (
        "step5_input.gro",
        "topol.top",
        "index.ndx",
        "step6.0_minimization.mdp",
        "run_step6_local.sh",
    ):
        (tmp_path / filename).write_text("")

    check = check_gromacs_minimization_inputs(tmp_path)

    assert check.output_dir == tmp_path.resolve()
    assert check.ready
    assert check.missing_files == ()
    assert check.command == ("bash", "run_step6_local.sh")
    assert check.command_text == "bash run_step6_local.sh"


def test_check_gromacs_minimization_inputs_reports_missing_files(tmp_path):
    (tmp_path / "topol.top").write_text("")

    check = check_gromacs_minimization_inputs(tmp_path)

    assert not check.ready
    assert tmp_path.resolve() / "step5_input.gro" in check.missing_files
    assert tmp_path.resolve() / "run_step6_local.sh" in check.missing_files


def test_run_gromacs_local_minimization_runs_from_gromacs_folder(tmp_path):
    for filename in (
        "step5_input.gro",
        "topol.top",
        "index.ndx",
        "step6.0_minimization.mdp",
        "run_step6_local.sh",
    ):
        (tmp_path / filename).write_text("")

    calls = []

    def fake_runner(command, **kwargs):
        calls.append((command, kwargs))
        return SimpleNamespace(returncode=0, stdout="done", stderr="")

    result = run_gromacs_local_minimization(tmp_path, runner=fake_runner)

    assert result.stdout == "done"
    assert calls == [
        (
            ["bash", "run_step6_local.sh"],
            {
                "cwd": tmp_path.resolve(),
                "text": True,
                "stdout": -1,
                "stderr": -1,
            },
        )
    ]


def test_run_gromacs_local_minimization_raises_if_inputs_missing(tmp_path):
    with pytest.raises(FileNotFoundError, match="Cannot run GROMACS minimisation"):
        run_gromacs_local_minimization(tmp_path)


def test_create_gromacs_simulation_box_runs_editconf_from_output_folder(tmp_path):
    input_gro = tmp_path / "step5_input.gro"
    output_gro = tmp_path / "step5_input_box.gro"
    input_gro.write_text(
        "PHB4\n1\n    1PHA      C1    1   0.0   0.0   0.0\n   1.0   1.0   1.0\n"
    )
    calls = []

    def fake_runner(command, **kwargs):
        calls.append((command, kwargs))
        return _fake_editconf_runner(command, **kwargs)

    created = create_gromacs_simulation_box(input_gro, output_gro, runner=fake_runner)

    assert created == output_gro
    assert output_gro.exists()
    assert calls[0][0] == [
        "gmx",
        "editconf",
        "-f",
        "step5_input.gro",
        "-o",
        "step5_input_box.gro",
        "-c",
        "-d",
        "3.0",
        "-bt",
        "cubic",
    ]
    assert calls[0][1]["cwd"] == tmp_path


def test_validate_gromacs_box_against_mdp_warns_when_cutoff_too_large(tmp_path):
    gro_path = tmp_path / "small.gro"
    mdp_path = tmp_path / "minim.mdp"
    gro_path.write_text(
        "PHB4\n1\n    1PHA      C1    1   0.0   0.0   0.0\n   1.5   2.4   2.4\n"
    )
    mdp_path.write_text("rlist = 1.0\nrcoulomb = 1.0\nrvdw = 1.0\n")

    with pytest.warns(UserWarning, match="box may be too small"):
        validation = validate_gromacs_box_against_mdp(gro_path, mdp_path)

    assert validation.shortest_box_vector_nm == 1.5
    assert validation.max_cutoff_nm == 1.0
    assert not validation.valid


def test_write_gromacs_solvation_files_writes_standard_solvate_workflow(tmp_path):
    (tmp_path / "topol.top").write_text(
        "\n".join(
            [
                "[ defaults ]",
                "1 2 yes 0.5 0.83333333",
                "",
                "[ atomtypes ]",
                "c3 6 12.01 0.0 A 0.3 0.4",
                "",
                "[ moleculetype ]",
                "PHA 3",
                "",
            ]
        )
    )

    outputs = write_gromacs_solvation_files(tmp_path, workflow_type="polymer")

    assert outputs.ions_mdp_path.exists()
    assert outputs.solvent_itp_path.exists()
    assert outputs.cation_itp_path.exists()
    assert outputs.anion_itp_path.exists()
    assert outputs.solvate_script_path.exists()
    assert outputs.local_script_path.exists()
    assert outputs.hpc_script_path.exists()
    assert os.access(outputs.solvate_script_path, os.X_OK)

    assert "integrator    = steep" in outputs.ions_mdp_path.read_text()
    assert "[ moleculetype ]" in outputs.solvent_itp_path.read_text()
    assert "SOL     2" in outputs.solvent_itp_path.read_text()
    assert "SOD" in outputs.cation_itp_path.read_text()
    topol_text = (tmp_path / "topol.top").read_text()
    assert '#include "tip3_ions_atomtypes.itp"' in topol_text
    assert '#include "TIP3_SOL.itp"' in topol_text
    assert '#include "SOD.itp"' in topol_text
    assert '#include "CLA.itp"' in topol_text
    solvate_script = outputs.solvate_script_path.read_text()
    assert (
        "gmx editconf -f step5_input.gro -o step5_input_box.gro -c -d 1.2 -bt cubic"
        in solvate_script
    )
    assert "reset_from_dry_polymer" in solvate_script
    assert "clean_generated_files" in solvate_script
    assert 'run_logged "editconf_box" "editconf_box.log" gmx editconf' in solvate_script
    assert 'run_stdin_logged "make_ndx_box" "make_ndx_box.log" "q\\n" gmx make_ndx' in solvate_script
    assert 'run_logged "solvate" "solvate.log" gmx solvate' in solvate_script
    assert (
        'run_logged "ions_grompp" "ions_grompp.log" gmx grompp'
        in solvate_script
    )
    assert 'local log_path="genion.log"' in solvate_script
    assert (
        'run_logged "minim_grompp" "minim_grompp.log" gmx grompp'
        in solvate_script
    )
    assert 'tail -n 50 "${log_path}"' in solvate_script
    assert "validate_solvation_topology" in solvate_script
    solvate_call_index = solvate_script.index(
        'run_logged "solvate" "solvate.log"'
    )
    validation_call_index = solvate_script.rindex("validate_solvation_topology")
    assert solvate_call_index < validation_call_index
    assert validation_call_index < solvate_script.index(
        'run_logged "ions_grompp" "ions_grompp.log"'
    )
    assert 'ensure_include "TIP3_SOL.itp"' in solvate_script
    assert 'ensure_include "SOD.itp"' in solvate_script
    assert 'has_moleculetype "${molecule_name}"' in solvate_script
    assert 'has_atomtype "${atom_type}"' in solvate_script
    assert (
        "gmx solvate -cp step5_input_box.gro -cs spc216.gro -p topol.top "
        "-o step5_solvated.gro"
    ) in solvate_script
    assert (
        "gmx grompp -f ions.mdp -c step5_solvated.gro -p topol.top "
        "-n index.ndx -o genion.tpr -maxwarn 1"
    ) in solvate_script
    assert "gmx genion" in solvate_script
    assert "genion_args=(-s genion.tpr -o system_neutralized.gro -p topol.top -neutral -pname SOD -nname CLA)" in solvate_script
    assert '-conc "${ION_CONCENTRATION_MOLAR}"' in solvate_script
    assert 'ION_CONCENTRATION_MOLAR="0.15"' in solvate_script
    assert "gmx editconf -f system_neutralized.gro -o step5_input.gro" in solvate_script
    assert 'run_stdin_logged "make_ndx_final" "make_ndx_final.log" "q\\n" gmx make_ndx' in solvate_script
    assert "cp step5_ions.gro step5_input.gro" not in solvate_script
    assert "step5_ions.gro -r step5_ions.gro" not in solvate_script
    assert (
        "gmx grompp -f step6.0_minimization.mdp -c step5_input.gro "
        "-r step5_input.gro -p topol.top -n index.ndx -o step6.0_minimization.tpr"
    ) in outputs.local_script_path.read_text()
    assert "-r step5_input.gro" in outputs.hpc_script_path.read_text()
    assert "step5_ions.gro" not in outputs.hpc_script_path.read_text()


def test_validate_gromacs_solvated_topology_counts_water_and_ions(tmp_path):
    (tmp_path / "topol.top").write_text(
        "\n".join(
            [
                "[ molecules ]",
                "; Compound  #mols",
                "PHA         1",
                "SOL         1200",
                "POT         5",
                "CLA         5",
                "",
            ]
        )
    )

    validation = validate_gromacs_solvated_topology(tmp_path)

    assert validation.has_water
    assert validation.has_ions
    assert validation.water_count == 1200
    assert validation.cation_count == 5
    assert validation.anion_count == 5


def test_validate_gromacs_solvation_grompp_runs_ion_and_minimization_checks(tmp_path):
    calls = []

    def fake_runner(command, **kwargs):
        calls.append((command, kwargs))
        return SimpleNamespace(returncode=0, stdout="ok", stderr="")

    validations = validate_gromacs_solvation_grompp(tmp_path, runner=fake_runner)

    assert len(validations) == 2
    assert all(validation.ok for validation in validations)
    assert calls[0][0] == [
        "gmx",
        "grompp",
        "-f",
        "ions.mdp",
        "-c",
        "step5_solvated.gro",
        "-p",
        "topol.top",
        "-n",
        "index.ndx",
        "-o",
        "genion.tpr",
        "-maxwarn",
        "1",
    ]
    assert calls[1][0] == [
        "gmx",
        "grompp",
        "-f",
        "step6.0_minimization.mdp",
        "-c",
        "step5_input.gro",
        "-r",
        "step5_input.gro",
        "-p",
        "topol.top",
        "-n",
        "index.ndx",
        "-o",
        "step6.0_minimization.tpr",
    ]


def test_validate_gromacs_coordinate_topology_counts_matches_gro_atoms(tmp_path):
    (tmp_path / "SOL.itp").write_text(
        "\n".join(
            [
                "[ moleculetype ]",
                "SOL 2",
                "",
                "[ atoms ]",
                "1 OT 1 SOL OW 1 -0.834 15.9994",
                "2 HT 1 SOL HW1 1 0.417 1.008",
                "3 HT 1 SOL HW2 1 0.417 1.008",
                "",
            ]
        )
    )
    (tmp_path / "topol.top").write_text(
        "\n".join(
            [
                '#include "SOL.itp"',
                "",
                "[ moleculetype ]",
                "PHA 3",
                "",
                "[ atoms ]",
                "1 c3 1 PHA C1 1 0 12.01",
                "2 c3 1 PHA C2 1 0 12.01",
                "",
                "[ molecules ]",
                "PHA 1",
                "SOL 2",
                "",
            ]
        )
    )
    (tmp_path / "step5_input.gro").write_text("test\n8\n")

    validation = validate_gromacs_coordinate_topology_counts(tmp_path)

    assert validation.coordinate_atom_count == 8
    assert validation.expected_atom_count == 8
    assert validation.valid
