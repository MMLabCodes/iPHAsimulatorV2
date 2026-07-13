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
    path = Path(path)

    with open(path, "w") as f:
        f.write(content.strip() + "\n")

    return path


def check_required_files(file_dict, keys):
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


def calculate_ion_pairs_from_rst7(rst7_path, concentration_molar):
    rst7_path = Path(rst7_path)

    with open(rst7_path, "r") as f:
        lines = f.readlines()

    box_line = lines[-1].split()

    lx = float(box_line[0])
    ly = float(box_line[1])
    lz = float(box_line[2])

    volume_litres = lx * ly * lz * 1e-27

    n_pairs = round(
        float(concentration_molar)
        * AVOGADRO
        * volume_litres
    )

    print(f"Box dimensions: {lx:.3f} x {ly:.3f} x {lz:.3f} Å")
    print(f"Volume: {volume_litres:.3e} L")
    print(f"Ion pairs: {n_pairs}")

    return n_pairs


def prepare_single_system_inputs(paths, polymer_name):
    """
    Locate the built polymer and parameter files.

    Files are not copied. Absolute paths are returned for use inside tleap.
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

    return {
        "PHA_type": PHA_type,
        "length": length,
        "built_files": {
            key: Path(value).resolve()
            for key, value in built_files.items()
        },
        "parameter_files": {
            key: Path(value).resolve()
            for key, value in parameter_files.items()
        },
    }


def build_dry_PHA(
    polymer_name,
    root_dir="structure_database",
    forcefield="gaff2",
    box_radius=20.0,
):
    """
    Build a dry single-chain PHA system from an already-built polymer.

    Output name:
        {polymer_name}_dry
    """

    if not isinstance(box_radius, float):
        raise TypeError("box_radius must be a float, e.g. 20.0")

    paths = PHAFileManager(root_dir)

    system_name = paths.get_dry_PHA_system_name(polymer_name)

    output_dir = paths.create_dry_PHA_dir(polymer_name)

    prepared = prepare_single_system_inputs(
        paths=paths,
        polymer_name=polymer_name,
        output_dir=output_dir,
    )

    local_pdb = prepared["local_pdb"]
    params = prepared["local_parameter_files"]

    prmtop = output_dir / f"{system_name}.prmtop"
    rst7 = output_dir / f"{system_name}.rst7"
    pdb = output_dir / f"{system_name}.pdb"
    intleap = output_dir / f"{system_name}.intleap"

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

    write_tleap_file(intleap, tleap_content)

    run_tleap(
        intleap,
        workdir=output_dir,
    )

    return {
        "system_name": system_name,
        "system_type": "dry",
        "output_dir": output_dir,
        "input_polymer": polymer_name,
        "pdb": pdb,
        "prmtop": prmtop,
        "rst7": rst7,
        "intleap": intleap,
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
    Build a solvated single-chain PHA system from an already-built polymer.

    Output name:
        {polymer_name}_solvated
    """

    if not isinstance(box_radius, float):
        raise TypeError("box_radius must be a float, e.g. 20.0")

    paths = PHAFileManager(root_dir)

    system_name = paths.get_solvated_PHA_system_name(polymer_name)

    output_dir = paths.create_solvated_PHA_dir(polymer_name)

    prepared = prepare_single_system_inputs(
        paths=paths,
        polymer_name=polymer_name,
        output_dir=output_dir,
    )

    local_pdb = prepared["local_pdb"]
    params = prepared["local_parameter_files"]

    prmtop = output_dir / f"{system_name}.prmtop"
    rst7 = output_dir / f"{system_name}.rst7"
    pdb = output_dir / f"{system_name}.pdb"
    intleap = output_dir / f"{system_name}.intleap"

    tleap_content = f"""
source leaprc.{forcefield}
source leaprc.{water_leaprc}

loadamberprep {params["head_prepin"].name}
loadamberprep {params["mainchain_prepin"].name}
loadamberprep {params["tail_prepin"].name}
loadamberparams {params["frcmod"].name}

polymer = loadpdb {local_pdb.name}

solvatebox polymer {water_box} {box_radius}

saveamberparm polymer {prmtop.name} {rst7.name}
savepdb polymer {pdb.name}

quit
"""

    write_tleap_file(intleap, tleap_content)

    run_tleap(
        intleap,
        workdir=output_dir,
    )

    return {
        "system_name": system_name,
        "system_type": "solvated",
        "output_dir": output_dir,
        "input_polymer": polymer_name,
        "pdb": pdb,
        "prmtop": prmtop,
        "rst7": rst7,
        "intleap": intleap,
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
    Build a solvated single-chain PHA system with ions.

    Output name:
        {polymer_name}_solvated_{ion_names}_{ion_concentration}
    """

    if not isinstance(box_radius, float):
        raise TypeError("box_radius must be a float, e.g. 20.0")

    paths = PHAFileManager(root_dir)

    ion_names = f"{pos_ion}{neg_ion}"

    system_name = paths.get_solvated_ions_PHA_system_name(
        polymer_name=polymer_name,
        ion_names=ion_names,
        ion_concentration=ion_conc,
    )

    output_dir = paths.create_solvated_ions_PHA_dir(
        polymer_name=polymer_name,
        ion_names=ion_names,
        ion_concentration=ion_conc,
    )

    prepared = prepare_single_system_inputs(
        paths=paths,
        polymer_name=polymer_name,
        output_dir=output_dir,
    )

    local_pdb = prepared["local_pdb"]
    params = prepared["local_parameter_files"]

    temp_name = f"{system_name}_temp_solvated"

    temp_prmtop = output_dir / f"{temp_name}.prmtop"
    temp_rst7 = output_dir / f"{temp_name}.rst7"
    temp_pdb = output_dir / f"{temp_name}.pdb"
    temp_intleap = output_dir / f"{temp_name}.intleap"

    prmtop = output_dir / f"{system_name}.prmtop"
    rst7 = output_dir / f"{system_name}.rst7"
    pdb = output_dir / f"{system_name}.pdb"
    intleap = output_dir / f"{system_name}.intleap"

    temp_tleap_content = f"""
source leaprc.{forcefield}
source leaprc.{water_leaprc}

loadamberprep {params["head_prepin"].name}
loadamberprep {params["mainchain_prepin"].name}
loadamberprep {params["tail_prepin"].name}
loadamberparams {params["frcmod"].name}

polymer = loadpdb {local_pdb.name}

solvatebox polymer {water_box} {box_radius}

saveamberparm polymer {temp_prmtop.name} {temp_rst7.name}
savepdb polymer {temp_pdb.name}

quit
"""

    write_tleap_file(temp_intleap, temp_tleap_content)

    print("Running first tleap pass: solvation only.")

    run_tleap(
        temp_intleap,
        workdir=output_dir,
    )

    num_ion_pairs = calculate_ion_pairs_from_rst7(
        temp_rst7,
        ion_conc,
    )

    final_tleap_content = f"""
source leaprc.{forcefield}
source leaprc.{water_leaprc}

loadamberprep {params["head_prepin"].name}
loadamberprep {params["mainchain_prepin"].name}
loadamberprep {params["tail_prepin"].name}
loadamberparams {params["frcmod"].name}

polymer = loadpdb {local_pdb.name}

solvatebox polymer {water_box} {box_radius}

addIonsRand polymer {pos_ion} {num_ion_pairs}
addIonsRand polymer {neg_ion} {num_ion_pairs}

saveamberparm polymer {prmtop.name} {rst7.name}
savepdb polymer {pdb.name}

quit
"""

    write_tleap_file(intleap, final_tleap_content)

    print("Running second tleap pass: solvation with ions.")

    run_tleap(
        intleap,
        workdir=output_dir,
    )

    return {
        "system_name": system_name,
        "system_type": "solvated_ions",
        "output_dir": output_dir,
        "input_polymer": polymer_name,
        "pdb": pdb,
        "prmtop": prmtop,
        "rst7": rst7,
        "intleap": intleap,
        "temp_pdb": temp_pdb,
        "temp_prmtop": temp_prmtop,
        "temp_rst7": temp_rst7,
        "temp_intleap": temp_intleap,
        "water_leaprc": water_leaprc,
        "water_box": water_box,
        "box_radius": box_radius,
        "salt": salt,
        "pos_ion": pos_ion,
        "neg_ion": neg_ion,
        "ion_conc": ion_conc,
        "num_ion_pairs": num_ion_pairs,
    }