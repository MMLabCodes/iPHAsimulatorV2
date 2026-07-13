#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Build dry, solvated, and ionised single-chain PHA systems from already-built
PHA polymers.
"""

from pathlib import Path
import subprocess

from src.iphasimulator.pha_filepath_manager import PHAFileManager


AVOGADRO = 6.02214076e23


def run_tleap(
    intleap_file,
    workdir,
    log_file,
):
    """
    Run tleap and save captured stdout/stderr to a specified log file.
    """

    intleap_file = Path(intleap_file).resolve()
    workdir = Path(workdir).resolve()
    log_file = Path(log_file).resolve()

    command = [
        "tleap",
        "-f",
        str(intleap_file),
    ]

    print("\nRunning tleap:")
    print(" ".join(command))
    print("Working directory:", workdir)

    result = subprocess.run(
        command,
        cwd=workdir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    log_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(log_file, "w") as output:
        output.write("STDOUT\n")
        output.write(result.stdout)

        output.write("\n\nSTDERR\n")
        output.write(result.stderr)

    print("Return code:", result.returncode)
    print("Log file:", log_file)

    if result.returncode != 0:
        raise RuntimeError(
            f"tleap failed. See log file:\n{log_file}"
        )

    return result


def write_tleap_file(path, content):
    """
    Write a tleap input file.
    """

    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(path, "w") as file:
        file.write(content.strip() + "\n")

    return path


def check_required_files(file_dict, keys):
    """
    Confirm that the requested paths exist.
    """

    missing = []

    for key in keys:
        path = Path(file_dict[key])

        if not path.exists():
            missing.append(path)

    if missing:
        raise FileNotFoundError(
            "Missing required files:\n"
            + "\n".join(str(path) for path in missing)
        )


def calculate_ion_pairs_from_rst7(
    rst7_path,
    concentration_molar,
):
    """
    Calculate the number of ion pairs required for a target concentration.

    The final line of the Amber rst7 file is expected to contain:

        lx ly lz alpha beta gamma

    Box lengths are interpreted as Angstrom.
    """

    rst7_path = Path(rst7_path)

    with open(rst7_path, "r") as file:
        lines = file.readlines()

    if not lines:
        raise ValueError(
            f"RST7 file is empty:\n{rst7_path}"
        )

    box_line = lines[-1].split()

    if len(box_line) < 3:
        raise ValueError(
            f"Could not read box dimensions from:\n{rst7_path}"
        )

    lx = float(box_line[0])
    ly = float(box_line[1])
    lz = float(box_line[2])

    volume_litres = lx * ly * lz * 1e-27

    n_pairs = round(
        float(concentration_molar)
        * AVOGADRO
        * volume_litres
    )

    print(
        f"Box dimensions: "
        f"{lx:.3f} x {ly:.3f} x {lz:.3f} Å"
    )
    print(f"Volume: {volume_litres:.3e} L")
    print(f"Ion pairs: {n_pairs}")

    return n_pairs


def prepare_single_system_inputs(
    paths,
    polymer_name,
):
    """
    Locate the built polymer and parameter files.

    No files are copied. Absolute paths are returned for use inside tleap.
    """

    PHA_type, length = paths.parse_built_PHA_name(
        polymer_name
    )

    built_files = paths.get_built_PHA_amber_files(
        polymer_name
    )

    parameter_files = paths.get_PHA_monomer_unit_files(
        PHA_type
    )

    check_required_files(
        built_files,
        [
            "pdb",
            "prmtop",
            "rst7",
        ],
    )

    check_required_files(
        parameter_files,
        [
            "head_prepin",
            "mainchain_prepin",
            "tail_prepin",
            "frcmod",
        ],
    )

    resolved_built_files = {
        key: Path(value).resolve()
        for key, value in built_files.items()
    }

    resolved_parameter_files = {
        key: Path(value).resolve()
        for key, value in parameter_files.items()
    }

    return {
        "PHA_type": PHA_type,
        "length": length,
        "built_files": resolved_built_files,
        "parameter_files": resolved_parameter_files,
    }


def build_dry_PHA(
    polymer_name,
    root_dir="structure_database",
    forcefield="gaff2",
    box_radius=20.0,
):
    """
    Build a dry single-chain PHA system from an already-built polymer.

    Final files are written to:

        PHA_dry/<polymer_name>_dry/

    tleap inputs and logs are written to:

        PHA_dry/<polymer_name>_dry/inputs/
    """

    if not isinstance(box_radius, float):
        raise TypeError(
            "box_radius must be a float, e.g. 20.0"
        )

    paths = PHAFileManager(root_dir)

    system_name = paths.get_dry_PHA_system_name(
        polymer_name
    )

    output_dir = paths.create_dry_PHA_dir(
        polymer_name
    ).resolve()

    inputs_dir = paths.get_dry_PHA_inputs_dir(
        polymer_name
    ).resolve()

    prepared = prepare_single_system_inputs(
        paths=paths,
        polymer_name=polymer_name,
    )

    built_files = prepared["built_files"]
    params = prepared["parameter_files"]

    prmtop = output_dir / f"{system_name}.prmtop"
    rst7 = output_dir / f"{system_name}.rst7"
    pdb = output_dir / f"{system_name}.pdb"

    intleap = inputs_dir / f"{system_name}.intleap"
    log_file = inputs_dir / f"{system_name}.log"

    tleap_content = f"""
source leaprc.{forcefield}

loadamberprep {params["head_prepin"]}
loadamberprep {params["mainchain_prepin"]}
loadamberprep {params["tail_prepin"]}
loadamberparams {params["frcmod"]}

polymer = loadpdb {built_files["pdb"]}

setBox polymer centers {box_radius}

saveamberparm polymer {prmtop} {rst7}
savepdb polymer {pdb}

quit
"""

    write_tleap_file(
        intleap,
        tleap_content,
    )

    run_tleap(
        intleap_file=intleap,
        workdir=inputs_dir,
        log_file=log_file,
    )

    return {
        "system_name": system_name,
        "system_type": "dry",
        "output_dir": output_dir,
        "inputs_dir": inputs_dir,
        "input_polymer": polymer_name,
        "input_polymer_pdb": built_files["pdb"],
        "pdb": pdb,
        "prmtop": prmtop,
        "rst7": rst7,
        "intleap": intleap,
        "log_file": log_file,
        "box_radius": box_radius,
    }


def build_solvated_PHA(
    polymer_name,
    root_dir="structure_database",
    forcefield="gaff2",
    water_leaprc="water.tip3p",
    water_box="TIP3PBOX",
    box_radius=20.0,
):
    """
    Build a solvated single-chain PHA system.

    Final files are written to:

        PHA_solvated/<polymer_name>_solvated/

    tleap inputs and logs are written to:

        PHA_solvated/<polymer_name>_solvated/inputs/
    """

    if not isinstance(box_radius, float):
        raise TypeError(
            "box_radius must be a float, e.g. 20.0"
        )

    paths = PHAFileManager(root_dir)

    system_name = paths.get_solvated_PHA_system_name(
        polymer_name
    )

    output_dir = paths.create_solvated_PHA_dir(
        polymer_name
    ).resolve()

    inputs_dir = paths.get_solvated_PHA_inputs_dir(
        polymer_name
    ).resolve()

    prepared = prepare_single_system_inputs(
        paths=paths,
        polymer_name=polymer_name,
    )

    built_files = prepared["built_files"]
    params = prepared["parameter_files"]

    prmtop = output_dir / f"{system_name}.prmtop"
    rst7 = output_dir / f"{system_name}.rst7"
    pdb = output_dir / f"{system_name}.pdb"

    intleap = inputs_dir / f"{system_name}.intleap"
    log_file = inputs_dir / f"{system_name}.log"

    tleap_content = f"""
source leaprc.{forcefield}
source leaprc.{water_leaprc}

loadamberprep {params["head_prepin"]}
loadamberprep {params["mainchain_prepin"]}
loadamberprep {params["tail_prepin"]}
loadamberparams {params["frcmod"]}

polymer = loadpdb {built_files["pdb"]}

solvatebox polymer {water_box} {box_radius}

saveamberparm polymer {prmtop} {rst7}
savepdb polymer {pdb}

quit
"""

    write_tleap_file(
        intleap,
        tleap_content,
    )

    run_tleap(
        intleap_file=intleap,
        workdir=inputs_dir,
        log_file=log_file,
    )

    return {
        "system_name": system_name,
        "system_type": "solvated",
        "output_dir": output_dir,
        "inputs_dir": inputs_dir,
        "input_polymer": polymer_name,
        "input_polymer_pdb": built_files["pdb"],
        "pdb": pdb,
        "prmtop": prmtop,
        "rst7": rst7,
        "intleap": intleap,
        "log_file": log_file,
        "water_leaprc": water_leaprc,
        "water_box": water_box,
        "box_radius": box_radius,
    }


def build_solvated_PHA_ions(
    polymer_name,
    root_dir="structure_database",
    forcefield="gaff2",
    water_leaprc="water.tip3p",
    water_box="TIP3PBOX",
    box_radius=20.0,
    salt="KCl",
    pos_ion="K+",
    neg_ion="Cl-",
    ion_conc=0.15,
):
    """
    Build a solvated single-chain PHA system containing ions.

    A two-pass tleap workflow is used:

    1. Build a temporary solvated system.
    2. Calculate the required ion count from its box volume.
    3. Rebuild the system with the requested number of ion pairs.

    Final files are written to the system root. Temporary files, tleap inputs,
    and logs are written to the inputs subdirectory.
    """

    if not isinstance(box_radius, float):
        raise TypeError(
            "box_radius must be a float, e.g. 20.0"
        )

    if float(ion_conc) < 0:
        raise ValueError(
            "ion_conc cannot be negative."
        )

    paths = PHAFileManager(root_dir)


    system_name = paths.get_solvated_ions_PHA_system_name(
        polymer_name=polymer_name,
        salt=salt,
        ion_concentration=ion_conc,
    )

    output_dir = paths.create_solvated_ions_PHA_dir(
        polymer_name=polymer_name,
        salt=salt,
        ion_concentration=ion_conc).resolve()

    inputs_dir = paths.get_solvated_ions_PHA_inputs_dir(
        polymer_name=polymer_name,
        salt=salt,
        ion_concentration=ion_conc).resolve()

    prepared = prepare_single_system_inputs(
        paths=paths,
        polymer_name=polymer_name,
    )

    built_files = prepared["built_files"]
    params = prepared["parameter_files"]

    temp_name = f"{system_name}_temp_solvated"

    temp_prmtop = inputs_dir / f"{temp_name}.prmtop"
    temp_rst7 = inputs_dir / f"{temp_name}.rst7"
    temp_pdb = inputs_dir / f"{temp_name}.pdb"
    temp_intleap = inputs_dir / f"{temp_name}.intleap"
    temp_log_file = inputs_dir / f"{temp_name}.log"

    prmtop = output_dir / f"{system_name}.prmtop"
    rst7 = output_dir / f"{system_name}.rst7"
    pdb = output_dir / f"{system_name}.pdb"

    intleap = inputs_dir / f"{system_name}.intleap"
    log_file = inputs_dir / f"{system_name}.log"

    temp_tleap_content = f"""
source leaprc.{forcefield}
source leaprc.{water_leaprc}

loadamberprep {params["head_prepin"]}
loadamberprep {params["mainchain_prepin"]}
loadamberprep {params["tail_prepin"]}
loadamberparams {params["frcmod"]}

polymer = loadpdb {built_files["pdb"]}

solvatebox polymer {water_box} {box_radius}

saveamberparm polymer {temp_prmtop} {temp_rst7}
savepdb polymer {temp_pdb}

quit
"""

    write_tleap_file(
        temp_intleap,
        temp_tleap_content,
    )

    print(
        "Running first tleap pass: "
        "solvation only."
    )

    run_tleap(
        intleap_file=temp_intleap,
        workdir=inputs_dir,
        log_file=temp_log_file,
    )

    num_ion_pairs = calculate_ion_pairs_from_rst7(
        temp_rst7,
        ion_conc,
    )

    final_tleap_content = f"""
source leaprc.{forcefield}
source leaprc.{water_leaprc}

loadamberprep {params["head_prepin"]}
loadamberprep {params["mainchain_prepin"]}
loadamberprep {params["tail_prepin"]}
loadamberparams {params["frcmod"]}

polymer = loadpdb {built_files["pdb"]}

solvatebox polymer {water_box} {box_radius}

addIonsRand polymer {pos_ion} {num_ion_pairs}
addIonsRand polymer {neg_ion} {num_ion_pairs}

saveamberparm polymer {prmtop} {rst7}
savepdb polymer {pdb}

quit
"""

    write_tleap_file(
        intleap,
        final_tleap_content,
    )

    print(
        "Running second tleap pass: "
        "solvation with ions."
    )

    run_tleap(
        intleap_file=intleap,
        workdir=inputs_dir,
        log_file=log_file,
    )

    return {
        "system_name": system_name,
        "system_type": "solvated_ions",
        "output_dir": output_dir,
        "inputs_dir": inputs_dir,
        "input_polymer": polymer_name,
        "input_polymer_pdb": built_files["pdb"],
        "pdb": pdb,
        "prmtop": prmtop,
        "rst7": rst7,
        "intleap": intleap,
        "log_file": log_file,
        "temp_pdb": temp_pdb,
        "temp_prmtop": temp_prmtop,
        "temp_rst7": temp_rst7,
        "temp_intleap": temp_intleap,
        "temp_log_file": temp_log_file,
        "water_leaprc": water_leaprc,
        "water_box": water_box,
        "box_radius": box_radius,
        "salt": salt,
        "pos_ion": pos_ion,
        "neg_ion": neg_ion,
        "ion_conc": ion_conc,
        "num_ion_pairs": num_ion_pairs,
    }