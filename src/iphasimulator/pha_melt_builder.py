#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PHA polymer melt construction tools.

This module builds amorphous PHA melt systems from previously built
single-chain PHA polymers.

Workflow
--------
1. Validate polymer names and polymer counts.
2. Locate or generate required single-chain PHA files.
3. Convert Amber topologies to GROMACS format using ACPYPE.
4. Build amorphous polymer melts using Polyply.
5. Save final melt outputs into structure_database/PHA_melts/.

Notes
-----
This module is deliberately separate from pha_builder.py because melt
construction is a system-building task rather than a single-polymer
parameterisation task.
"""

import re
import subprocess
from pathlib import Path

from src.iphasimulator.pha_filepath_manager import PHAFileManager
from src.iphasimulator.build_pha import PHAPolymerBuilder


class PHAMeltBuilder:
    """
    Build amorphous PHA melt systems.

    Parameters
    ----------
    root_dir : str or pathlib.Path, optional
        Root directory of the PHA structure database.

    Notes
    -----
    The main user-facing function should be:

        generate_polymer_melt(polymer_names, number_of_polymers)

    where, for example:

        polymer_names = ["P3HB_10"]
        number_of_polymers = [25]
    """

    def __init__(self, root_dir="structure_database"):
        self.paths = PHAFileManager(root_dir)
        self.polymer_builder = PHAPolymerBuilder(root_dir)

    def run_command(self, command, workdir=None):

        """

        Run a shell command and report stdout/stderr.

        Uses UTF-8 decoding with replacement so progress bars or special

        characters from external programs do not crash Python.

        """

        import subprocess

        print("\nRunning command:")
        print(command)

        result = subprocess.run(
            command,
            shell=True,
            cwd=workdir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        print("Return code:", result.returncode)

        if result.stdout:
            print("STDOUT:")
            print(result.stdout)

        if result.stderr:
            print("STDERR:")
            print(result.stderr)

        if result.returncode != 0:
            raise RuntimeError(f"Command failed:\n{command}")

        return result

    def parse_polymer_name(self, polymer_name):
        """
        Parse a built PHA polymer name.

        Example
        -------
        P3HB_10

        returns:

            PHA_type = "3HB"
            length = 10
        """

        match = re.fullmatch(r"P(.+)_(\d+)", polymer_name)

        if match is None:
            raise ValueError(
                f"Invalid polymer name: {polymer_name}\n"
                f"Expected format like: P3HB_10"
            )

        PHA_type = match.group(1)
        length = int(match.group(2))

        return PHA_type, length

    def get_melt_name(self, polymer_names, number_of_polymers):
        """
        Return the standard melt name.

        Examples
        --------
        ["P3HB_10"], [25]
            -> 25_P3HB_10_melt

        ["P3HB_10", "P4HB_10"], [25, 25]
            -> 25_P3HB_10_25_P4HB_10_melt
        """

        if len(polymer_names) != len(number_of_polymers):
            raise ValueError(
                "polymer_names and number_of_polymers must have the same length."
            )

        name_parts = []

        for polymer_name, number in zip(polymer_names, number_of_polymers):
            name_parts.append(f"{number}_{polymer_name}")

        return "_".join(name_parts) + "_melt"

    def validate_melt_inputs(self, polymer_names, number_of_polymers):
        """
        Validate user inputs for melt construction.
        """

        if not isinstance(polymer_names, list):
            raise TypeError("polymer_names must be a list.")

        if not isinstance(number_of_polymers, list):
            raise TypeError("number_of_polymers must be a list.")

        if len(polymer_names) == 0:
            raise ValueError("polymer_names cannot be empty.")

        if len(polymer_names) != len(number_of_polymers):
            raise ValueError(
                "polymer_names and number_of_polymers must have the same length."
            )

        for polymer_name in polymer_names:
            self.parse_polymer_name(polymer_name)

        for number in number_of_polymers:
            if not isinstance(number, int):
                raise TypeError("All polymer counts must be integers.")

            if number <= 0:
                raise ValueError("All polymer counts must be greater than zero.")

    def ensure_built_polymer_exists(self, polymer_name):
        """
        Ensure the Amber files for a built polymer exist.

        If missing, this method attempts to call PHAPolymerBuilder.

        Notes
        -----
        This assumes the PHA type has already been parameterised and has valid
        prepin files.
        """

        PHA_type, length = self.parse_polymer_name(polymer_name)

        amber_dir = self.paths.get_built_PHA_amber_dir(
            PHA_type,
            length,
        )

        prmtop = amber_dir / f"{polymer_name}.prmtop"
        rst7 = amber_dir / f"{polymer_name}.rst7"
        pdb = amber_dir / f"{polymer_name}.pdb"

        if prmtop.exists() and rst7.exists() and pdb.exists():
            print(f"Built polymer already exists: {polymer_name}")
            return {
                "PHA_type": PHA_type,
                "length": length,
                "prmtop": prmtop,
                "rst7": rst7,
                "pdb": pdb,
            }

        print(f"Built polymer missing. Building: {polymer_name}")

        self.polymer_builder.build_PHA_polymer(
            PHA_type=PHA_type,
            length=length,
        )

        if not prmtop.exists() or not rst7.exists() or not pdb.exists():
            raise FileNotFoundError(
                f"Failed to locate built polymer files for {polymer_name}"
            )

        return {
            "PHA_type": PHA_type,
            "length": length,
            "prmtop": prmtop,
            "rst7": rst7,
            "pdb": pdb,
        }

    def ensure_gromacs_polymer_exists(self, polymer_name):

        """

        Ensure GROMACS files exist for a built polymer.

        If the GROMACS files are missing, run ACPYPE conversion.

        """

        PHA_type, length = self.parse_polymer_name(polymer_name)

        gromacs_dir = self.paths.get_built_PHA_gromacs_dir(
            PHA_type,
            length,
        )

        gromacs_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        expected_gro = gromacs_dir / f"{polymer_name}.gro"
        expected_top = gromacs_dir / f"{polymer_name}.top"
        existing_itp_files = sorted(gromacs_dir.glob("*.itp"))

        if expected_gro.exists() and expected_top.exists():
            print(
                f"GROMACS files already exist: "
                f"{polymer_name}"
            )

            return {
                "gro": expected_gro,
                "top": expected_top,
                "itp_files": existing_itp_files,
            }

        self.ensure_built_polymer_exists(polymer_name)

        print(
            f"GROMACS files missing for {polymer_name}. "
            f"Running ACPYPE conversion."
        )

        acpype_result = self.run_acpype(polymer_name)

        return {
            "gro": acpype_result["gro"],
            "top": acpype_result["top"],
            "itp_files": acpype_result["itp_files"],
        }

    def generate_polymer_melt(

        self,

        polymer_names,

        number_of_polymers,

        density=750,

    ):

        """

        Generate an amorphous PHA polymer melt.

        Creates the melt directory, inputs directory and simulations parent

        directory. Timestamped simulation folders are created later by the

        simulation layer.

        """

        self.validate_melt_inputs(
            polymer_names,
            number_of_polymers,
        )

        melt_name = self.get_melt_name(
            polymer_names,
            number_of_polymers,
        )

        melt_dir = self.paths.create_PHA_melt_dir(
            polymer_names,
            number_of_polymers,

        )

        inputs_dir = self.paths.get_PHA_melt_inputs_dir(
            polymer_names,
            number_of_polymers,
        )

        simulations_dir = self.paths.get_PHA_melt_simulations_dir(
            polymer_names,
            number_of_polymers,
        )

        polymer_gromacs_files = {}

        for polymer_name in polymer_names:
            polymer_gromacs_files[polymer_name] = (
                self.ensure_gromacs_polymer_exists(polymer_name)
            )

        print("\nPolymer melt setup complete.")
        print("Melt name:       ", melt_name)
        print("Melt dir:        ", melt_dir)
        print("Inputs dir:      ", inputs_dir)
        print("Simulations dir: ", simulations_dir)
        print("Density:         ", density)

        polyply_result = self.run_polyply(
            polymer_names=polymer_names,
            number_of_polymers=number_of_polymers,
            polymer_gromacs_files=polymer_gromacs_files,
            melt_dir=melt_dir,
            melt_name=melt_name,
            density=density,
        )

        print("\nPolymer melt generation complete.")
        print("Melt name: ", melt_name)
        print("Melt dir:  ", melt_dir)
        print("Density:   ", density)

        return {
            "melt_name": melt_name,
            "melt_dir": melt_dir,
            "inputs_dir": inputs_dir,
            "simulations_dir": simulations_dir,
            "topology_file": polyply_result["top"],
            "coordinate_file": polyply_result["gro"],
            "itp_file": polyply_result["itp"],
            "polymer_names": polymer_names,
            "number_of_polymers": number_of_polymers,
            "density": density,
            "polymer_gromacs_files": polymer_gromacs_files,
            "polyply_result": polyply_result,
        }
    
    def run_acpype(self, polymer_name):

        """

        Convert a built PHA polymer from Amber format to GROMACS format

        using ACPYPE.

        This method also edits the ACPYPE-generated topology so that the

        [ atomtypes ] section is compatible with Polyply.

        """

        import shutil

        PHA_type, length = self.parse_polymer_name(polymer_name)
        
        amber_dir = self.paths.get_built_PHA_amber_dir(
            PHA_type,
            length,

        ).resolve()

        gromacs_dir = self.paths.get_built_PHA_gromacs_dir(
            PHA_type,
            length,
        ).resolve()

        temp_dir = self.paths.get_temp_dir().resolve()

        gromacs_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        temp_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        prmtop_file = amber_dir / f"{polymer_name}.prmtop"
        rst7_file = amber_dir / f"{polymer_name}.rst7"

        if not prmtop_file.exists():
            raise FileNotFoundError(
                f"Amber topology file not found:\n"
                f"{prmtop_file}"
            )

        if not rst7_file.exists():
            raise FileNotFoundError(
                f"Amber coordinate file not found:\n"
                f"{rst7_file}"
            )

        acpype_workdir = temp_dir / f"{polymer_name}_acpype"

        if acpype_workdir.exists():
            shutil.rmtree(acpype_workdir)

        acpype_workdir.mkdir(
            parents=True,
            exist_ok=True,
        )

        temp_prmtop = acpype_workdir / prmtop_file.name
        temp_rst7 = acpype_workdir / rst7_file.name

        shutil.copyfile(prmtop_file, temp_prmtop)
        shutil.copyfile(rst7_file, temp_rst7)

        acpype_command = (
            f"acpype "
            f"-p {temp_prmtop.name} "
            f"-x {temp_rst7.name} "
            f"-b {polymer_name}"
        )

        self.run_command(
            acpype_command,
            workdir=acpype_workdir,
        )

        acpype_output_dir = (
            acpype_workdir /
            f"{polymer_name}.amb2gmx"
        )

        if not acpype_output_dir.exists():
            raise FileNotFoundError(
                f"ACPYPE output directory not found:\n"
                f"{acpype_output_dir}"
            )

        generated_gro = (
            acpype_output_dir /
            f"{polymer_name}_GMX.gro"
        )

        generated_top = (
            acpype_output_dir /
            f"{polymer_name}_GMX.top"
        )

        if not generated_gro.exists():
            raise FileNotFoundError(
                f"Expected ACPYPE GRO file not found:\n"
                f"{generated_gro}"
            )

        if not generated_top.exists():
            raise FileNotFoundError(
                f"Expected ACPYPE TOP file not found:\n"
                f"{generated_top}"
            )

        generated_itp_files = sorted(
            acpype_output_dir.glob("*.itp")
        )

        final_gro = gromacs_dir / f"{polymer_name}.gro"
        final_top = gromacs_dir / f"{polymer_name}.top"

        shutil.copyfile(generated_gro, final_gro)
        shutil.copyfile(generated_top, final_top)

        self.edit_acpype_topology_for_polyply(
            final_top
        )

        final_itp_files = []

        for generated_itp in generated_itp_files:
            final_itp = gromacs_dir / generated_itp.name
            shutil.copyfile(
                generated_itp,
                final_itp,
            )

            final_itp_files.append(final_itp)

        print("\nACPYPE conversion complete.")
        print("Polymer name: ", polymer_name)
        print("GRO:          ", final_gro)
        print("TOP:          ", final_top)

        if final_itp_files:
            print("ITP files:")
            for file_path in final_itp_files:
                print("  ", file_path)
        else:
            print("ITP files:    None generated")
        return {
            "polymer_name": polymer_name,
            "gro": final_gro,
            "top": final_top,
            "itp_files": final_itp_files,
            "acpype_workdir": acpype_workdir,
            "acpype_output_dir": acpype_output_dir,
        }
    
    def prepare_polyply_inputs(

        self,

        polymer_names,

        number_of_polymers,

        polymer_gromacs_files,

        melt_dir,

        melt_name,

    ):

        """

        Prepare system-level topology files for Polyply.

        Copied polymer inputs and generated topology inputs are written to:

            PHA_melts/<melt_name>/inputs/

        Final Polyply outputs are written to:

            PHA_melts/<melt_name>/

        """

        import shutil

        melt_dir = Path(melt_dir).resolve()

        inputs_dir = melt_dir / "inputs"

        melt_dir.mkdir(

            parents=True,

            exist_ok=True,

        )

        inputs_dir.mkdir(

            parents=True,

            exist_ok=True,

        )

        copied_topology_files = []

        for polymer_name in polymer_names:

            files = polymer_gromacs_files[polymer_name]

            source_top = files["top"]

            source_gro = files["gro"]

            copied_top = inputs_dir / f"{polymer_name}.top"

            copied_gro = inputs_dir / f"{polymer_name}.gro"

            shutil.copyfile(source_top, copied_top)

            shutil.copyfile(source_gro, copied_gro)

            copied_topology_files.append(copied_top)

            for itp_file in files.get("itp_files", []):

                copied_itp = inputs_dir / itp_file.name

                shutil.copyfile(

                    itp_file,

                    copied_itp,

                )

        system_itp_file = inputs_dir / f"{melt_name}.itp"

        system_top_file = inputs_dir / f"{melt_name}.top"

        self.combine_itps(

            itp_files=copied_topology_files,

            output_file=system_itp_file,

        )

        molecule_statements = "\n".join(

            [

                f"{polymer_names[i]} {number_of_polymers[i]}"

                for i in range(len(polymer_names))

            ]

        )

        system_top_contents = f"""

#include "{system_itp_file.name}"

[ system ]

Packed {' '.join(polymer_names)}

[ molecules ]

{molecule_statements}

"""

        with open(system_top_file, "w") as f:

            f.write(system_top_contents)

        return {

            "melt_dir": melt_dir,

            "inputs_dir": inputs_dir,

            "system_itp": system_itp_file,

            "system_top": system_top_file,

            "copied_topology_files": copied_topology_files,

        }

    def run_polyply(

        self,

        polymer_names,

        number_of_polymers,

        polymer_gromacs_files,

        melt_dir,

        melt_name,

        density=750,

    ):

        """

        Run Polyply using a generated system-level topology file.

        Polyply is run inside the melt inputs directory, but final files are

        copied to the melt root directory.

        """

        import shutil

        polyply_inputs = self.prepare_polyply_inputs(

            polymer_names=polymer_names,

            number_of_polymers=number_of_polymers,

            polymer_gromacs_files=polymer_gromacs_files,

            melt_dir=melt_dir,

            melt_name=melt_name,

        )

        melt_dir = polyply_inputs["melt_dir"]

        inputs_dir = polyply_inputs["inputs_dir"]

        system_top = polyply_inputs["system_top"]

        system_itp = polyply_inputs["system_itp"]

        output_gro_in_inputs = inputs_dir / f"{melt_name}.gro"

        final_gro = melt_dir / f"{melt_name}.gro"

        final_top = melt_dir / f"{melt_name}.top"

        final_itp = melt_dir / f"{melt_name}.itp"

        polyply_command = (

            f"polyply gen_coords "

            f"-p {system_top.name} "

            f"-o {output_gro_in_inputs.name} "

            f"-dens {density}"

        )

        self.run_command(

            polyply_command,

            workdir=inputs_dir,

        )

        if not output_gro_in_inputs.exists():

            raise FileNotFoundError(

                f"Expected Polyply output not found:\n"

                f"{output_gro_in_inputs}"

            )

        shutil.copyfile(

            output_gro_in_inputs,

            final_gro,

        )

        shutil.copyfile(

            system_top,

            final_top,

        )

        shutil.copyfile(

            system_itp,

            final_itp,

        )

        print("\nPolyply melt generation complete.")

        print("Melt name: ", melt_name)

        print("TOP:       ", final_top)

        print("GRO:       ", final_gro)

        print("ITP:       ", final_itp)

        return {

            "melt_name": melt_name,

            "melt_dir": melt_dir,

            "inputs_dir": inputs_dir,

            "top": final_top,

            "gro": final_gro,

            "itp": final_itp,

            "density": density,

        }
    
    def combine_itps(

        self,

        itp_files,

        output_file,

    ):

        """

        Combine multiple ITP/TOP-like files into one system-level ITP file.

        Only the first file contributes [ defaults ] and [ atomtypes ] sections.

        This mirrors the behaviour of the original PolymerSimulator code.

        """

        skip_sections = {

            "[ defaults ]",

            "[ atomtypes ]",

        }

        with open(output_file, "w") as outfile:

            for idx, file_path in enumerate(itp_files):

                with open(file_path, "r") as infile:

                    lines = infile.readlines()

                copy_block = True

                for line in lines:

                    stripped = line.strip().lower()

                    if any(

                        stripped.startswith(section)

                        for section in skip_sections

                    ):

                        if idx > 0:

                            copy_block = False

                            continue

                    if (

                        stripped.startswith("[")

                        and stripped.endswith("]")

                        and stripped not in skip_sections

                    ):

                        copy_block = True

                    if copy_block:

                        outfile.write(line)

                outfile.write("\n\n")

        print(

            f"Combined {len(itp_files)} topology files into "

            f"{output_file}"

        )
        
    def edit_acpype_topology_for_polyply(self, topology_file):

        """

        Edit an ACPYPE-generated GROMACS topology so Polyply can parse it.

        ACPYPE can write a bond_type column inside the [ atomtypes ] section.

        Polyply may interpret this extra string column as a numeric field and

        fail with errors such as:

            ValueError: could not convert string to float: 'c3'

        This method removes the second word column from [ atomtypes ], matching

        the behaviour used in the original PolymerSimulator workflow.

        """

        import re

        topology_file = Path(topology_file)

        inside_atomtypes = False

        new_lines = []

        with open(topology_file, "r") as f:

            for line in f:

                stripped = line.strip()

                if stripped.startswith("[ atomtypes ]"):

                    inside_atomtypes = True

                    new_lines.append(line)

                    continue

                if (

                    inside_atomtypes

                    and stripped.startswith("[")

                    and not stripped.startswith("[ atomtypes ]")

                ):

                    inside_atomtypes = False

                if inside_atomtypes and stripped:

                    if stripped.startswith(";"):

                        new_line = line.replace(

                            "bond_type",

                            " " * len("bond_type"),

                        )

                        new_lines.append(new_line)

                    else:

                        parts = re.split(

                            r"(\s+)",

                            line.rstrip("\n"),

                        )

                        words = [

                            i

                            for i in range(0, len(parts), 2)

                        ]

                        if len(words) > 2:

                            second_word_index = words[2]

                            word = parts[second_word_index]

                            parts[second_word_index] = (

                                " " * len(word)

                            )

                        new_line = "".join(parts) + "\n"

                        new_lines.append(new_line)

                else:

                    new_lines.append(line)

        with open(topology_file, "w") as f:

            f.writelines(new_lines)

        print(

            "Edited ACPYPE topology for Polyply compatibility: "

            f"{topology_file}"

        )
        
    def test_polymer_melt_simulation(

        self,

        melt_name,

        topology_file,

        coordinate_file,

        test_steps=1000,

        temperature=300,

        timestep=1.0,

    ):

        """

        Test whether a generated polymer melt can survive a short OpenMM run.

        This method is intended to catch bad Polyply starting structures that

        produce NaN coordinates or extreme forces.

        Parameters

        ----------

        melt_name : str

            Name of the melt system, e.g. "25_P3HB_10_melt".

        topology_file : str or pathlib.Path

            GROMACS topology file for the melt.

        coordinate_file : str or pathlib.Path

            GROMACS coordinate file for the melt.

        test_steps : int, optional

            Number of OpenMM MD steps for the short stability test.

        temperature : float, optional

            Test simulation temperature in Kelvin.

        timestep : float, optional

            Test simulation timestep in femtoseconds.

        Returns

        -------

        dict

            Test result information.

        """

        from pathlib import Path

        from datetime import datetime

        from modules.sw_openmm import GromacsSimulation

        topology_file = Path(topology_file).resolve()

        coordinate_file = Path(coordinate_file).resolve()

        if not topology_file.exists():

            raise FileNotFoundError(

                f"Melt topology file not found:\n"

                f"{topology_file}"

            )

        if not coordinate_file.exists():

            raise FileNotFoundError(

                f"Melt coordinate file not found:\n"

                f"{coordinate_file}"

            )

        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")

        simulations_dir = (

            self.paths.PHA_melts_dir /

            melt_name /

            "simulations"

        )

        simulation_run_dir = simulations_dir / timestamp

        simulation_run_dir.mkdir(

            parents=True,

            exist_ok=False,

        )

        # ------------------------------------------------------

        # Minimal manager shim for compatibility with old

        # GromacsSimulation interface.

        # ------------------------------------------------------

        class PHAMeltSimulationManager:

            def __init__(self, systems_dir):

                self.systems_dir = Path(systems_dir)

        manager = PHAMeltSimulationManager(

            systems_dir=simulations_dir

        )

        sim = GromacsSimulation(

            manager,

            topology_file,

            coordinate_file,

        )

        # Force the output directory to the clean melt simulation folder.

        sim.output_dir = simulation_run_dir

        sim.set_total_steps(test_steps)

        sim.set_temperature(temperature)

        sim.set_timestep(timestep)

        try:

            min_sim = sim.minimize_energy()

            test_sim, test_data = sim.basic_NVT(

                min_sim

            )

            success = True

            error_message = None

        except Exception as error:

            success = False

            min_sim = None

            test_sim = None

            test_data = None

            error_message = str(error)

        print("\nPolymer melt simulation test complete.")

        print("Melt name:      ", melt_name)

        print("Success:        ", success)

        print("Simulation dir: ", simulation_run_dir)

        if error_message is not None:

            print("Error:")

            print(error_message)
            
        # Remove empty compatibility directories created by the old simulation class.
        for child in simulations_dir.iterdir():

            if child == simulation_run_dir:
                continue

            if not child.is_dir():
                continue

            files_inside = [
                path
                for path in child.rglob("*")
                if path.is_file()
            ]

        if len(files_inside) == 0:
            import shutil
        shutil.rmtree(child)

        return {

            "melt_name": melt_name,

            "success": success,

            "simulation_dir": simulation_run_dir,

            "topology_file": topology_file,

            "coordinate_file": coordinate_file,

            "minimized_sim": min_sim,

            "test_sim": test_sim,

            "test_data": test_data,

            "error_message": error_message,

        }