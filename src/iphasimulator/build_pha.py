#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 15:15:00 2026

@author: daniel

PHA polymer construction tools.

This module provides the main builder class for a PHA-specific structure
database. It currently supports three stages of the AmberTools-based PHA
construction workflow:

1. Parameterise a PHA trimer from a SMILES string.
2. Generate head, mainchain and tail prepin files from manual prepgen
   definition files.
3. Build a polymer of a chosen length using tleap.

The class relies on:

    PHAFileManager
        Handles directory creation and path construction.

    PHAResidueCodeManager
        Handles residue code assignment and lookup.

External programs required:

    - OpenBabel / pybel
    - AmberTools: antechamber, parmchk2, prepgen, tleap
"""
import subprocess
from pathlib import Path
import shutil
from openbabel import pybel
from modules.pha_filepath_manager import PHAFileManager, PHAResidueCodeManager

class PHAPolymerBuilder:
    """
    Main interface for building PHA structures.

    Parameters
    ----------
    root_dir : str or pathlib.Path, optional
        Root directory of the PHA structure database.

    Notes
    -----
    This class coordinates chemistry-building tasks, but delegates all
    path handling to `PHAFileManager` and all residue-code handling to
    `PHAResidueCodeManager`.
    """

    def __init__(self, root_dir='structure_database'):
        """Initialise the polymer builder.

Parameters
----------
root_dir : str or pathlib.Path, optional
    Root directory of the PHA structure database."""
        self.paths = PHAFileManager(root_dir)
        self.residue_codes = PHAResidueCodeManager(self.paths)

    def parameterise_trimer(self, PHA_type, trimer_name, trimer_smiles, monomer_smiles, forcefield='gaff2', charge_model='abcg2'):
        """
        Parameterise a PHA trimer using AmberTools.

        Parameters
        ----------
        PHA_type : str
            PHA type name, e.g. "3HB".

        trimer_name : str
            Name of the trimer, e.g. "P3HB_3".

        trimer_smiles : str
            SMILES string for the trimer.

        monomer_smiles : str
            SMILES string for the monomer unit. This is stored in the residue
            code database for the head, mainchain and tail components.

        forcefield : str, optional
            Amber atom type set to use with antechamber.

        charge_model : str, optional
            Charge model to use with antechamber.

        Returns
        -------
        dict
            Paths to the generated trimer files and residue information.
        """
        self.paths.create_PHA_type_dir(PHA_type)
        self.residue_codes.register_PHA_type(PHA_type=PHA_type, trimer_name=trimer_name, trimer_smiles=trimer_smiles, monomer_smiles=monomer_smiles)
       
        trimer_code = self.residue_codes.get_code(PHA_type, 'trimer')
        if trimer_code is None:
            raise RuntimeError(f'No trimer residue code found for {PHA_type}')
        
        trimer_dir = self.paths.get_PHA_trimer_dir(PHA_type)
        pdb_file = (trimer_dir / f'{trimer_name}.pdb').resolve()
        mol2_file = (trimer_dir / f'{trimer_name}.mol2').resolve()
        frcmod_file = (trimer_dir / f'{trimer_name}.frcmod').resolve()
        ac_file = (trimer_dir / f'{trimer_name}.ac').resolve()
        
        temp_dir = self.paths.get_temp_dir().resolve()
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        self.smiles_to_pdb(trimer_smiles, pdb_file)
        self.replace_pdb_residue_name(pdb_file=pdb_file, old_resname='UNL', new_resname=trimer_code)
        
        antechamber_mol2_command = f'antechamber -i {pdb_file} -fi pdb -o {mol2_file} -fo mol2 -c {charge_model.lower()} -at {forcefield.lower()} -s 2'
        self.run_command(antechamber_mol2_command, workdir=temp_dir)
        
        parmchk_command = f'parmchk2 -i {mol2_file} -f mol2 -o {frcmod_file}'
        self.run_command(parmchk_command, workdir=temp_dir)
        
        antechamber_ac_command = f'antechamber -fi mol2 -fo ac -i {mol2_file} -o {ac_file} -c {charge_model.lower()} -s 2'
        self.run_command(antechamber_ac_command, workdir=temp_dir)
        
        print('\nTrimer parameterisation complete.')
        print('PHA type:     ', PHA_type)
        print('Trimer name:  ', trimer_name)
        print('Trimer code:  ', trimer_code)
        print('PDB:          ', pdb_file)
        print('MOL2:         ', mol2_file)
        print('FRCMOD:       ', frcmod_file)
        print('AC:           ', ac_file)
        print('Temp dir:     ', temp_dir)
        return {'PHA_type': PHA_type, 'trimer_name': trimer_name, 'trimer_code': trimer_code, 'pdb_file': pdb_file, 'mol2_file': mol2_file, 'frcmod_file': frcmod_file, 'ac_file': ac_file, 'temp_dir': temp_dir}

    def generate_polymer_prepins(self, PHA_type):
        """
        Generate head, mainchain and tail prepin files for a PHA type.

        Parameters
        ----------
        PHA_type : str
            PHA type name, e.g. "3HB".

        Returns
        -------
        dict
            Paths to the generated prepin files and associated residue codes.

        Notes
        -----
        Manual prepgen definition files must already exist in:

            structure_database/PHA_types/<PHA_type>/input/

        For PHA_type="3HB", the expected files are:

            head_P3HB_3.txt
            mainchain_P3HB_3.txt
            tail_P3HB_3.txt
        """
        self.paths.create_PHA_type_dir(PHA_type)
        input_dir = self.paths.get_PHA_input_dir(PHA_type).resolve()
        trimer_dir = self.paths.get_PHA_trimer_dir(PHA_type).resolve()
        monomer_units_dir = self.paths.get_PHA_monomer_units_dir(PHA_type).resolve()
        temp_dir = self.paths.get_temp_dir().resolve()
        
        monomer_units_dir.mkdir(parents=True, exist_ok=True)
        temp_dir.mkdir(parents=True, exist_ok=True)
        trimer_name = f'P{PHA_type}_3'
        
        head_definition_file = input_dir / f'head_{trimer_name}.txt'
        mainchain_definition_file = input_dir / f'mainchain_{trimer_name}.txt'
        tail_definition_file = input_dir / f'tail_{trimer_name}.txt'
        
        for file_path in [head_definition_file, mainchain_definition_file, tail_definition_file]:
            if not file_path.exists():
                raise FileNotFoundError(f'Required definition file not found:\n{file_path}\n\nPut this file in:\n{input_dir}')
        ac_file = trimer_dir / f'{trimer_name}.ac'
       
        if not ac_file.exists():
            raise FileNotFoundError(f'Trimer .ac file not found:\n{ac_file}\n\nRun parameterise_trimer() first.')
        
        head_code = self.residue_codes.get_code(PHA_type, 'head')
        mainchain_code = self.residue_codes.get_code(PHA_type, 'mainchain')
        tail_code = self.residue_codes.get_code(PHA_type, 'tail')
        
        if head_code is None:
            raise RuntimeError(f'No head residue code found for {PHA_type}')
        
        if mainchain_code is None:
            raise RuntimeError(f'No mainchain residue code found for {PHA_type}')
       
        if tail_code is None:
            raise RuntimeError(f'No tail residue code found for {PHA_type}')
        head_prepin = monomer_units_dir / f'hP{PHA_type}.prepin'
        mainchain_prepin = monomer_units_dir / f'mP{PHA_type}.prepin'
        tail_prepin = monomer_units_dir / f'tP{PHA_type}.prepin'
        
        temp_ac_file = temp_dir / ac_file.name
        temp_head_definition_file = temp_dir / head_definition_file.name
        temp_mainchain_definition_file = temp_dir / mainchain_definition_file.name
        temp_tail_definition_file = temp_dir / tail_definition_file.name
        
        shutil.copyfile(ac_file, temp_ac_file)
        shutil.copyfile(head_definition_file, temp_head_definition_file)
        shutil.copyfile(mainchain_definition_file, temp_mainchain_definition_file)
        shutil.copyfile(tail_definition_file, temp_tail_definition_file)
        
        head_command = f'prepgen -i {temp_ac_file.name} -o {head_prepin.name} -f prepi -m {temp_head_definition_file.name} -rn {head_code} -rf {head_code}.res'
        mainchain_command = f'prepgen -i {temp_ac_file.name} -o {mainchain_prepin.name} -f prepi -m {temp_mainchain_definition_file.name} -rn {mainchain_code} -rf {mainchain_code}.res'
        tail_command = f'prepgen -i {temp_ac_file.name} -o {tail_prepin.name} -f prepi -m {temp_tail_definition_file.name} -rn {tail_code} -rf {tail_code}.res'
        
        self.run_command(head_command, workdir=temp_dir)
        self.run_command(mainchain_command, workdir=temp_dir)
        self.run_command(tail_command, workdir=temp_dir)
        
        generated_head_prepin = temp_dir / head_prepin.name
        generated_mainchain_prepin = temp_dir / mainchain_prepin.name
        generated_tail_prepin = temp_dir / tail_prepin.name
        
        shutil.copyfile(generated_head_prepin, head_prepin)
        shutil.copyfile(generated_mainchain_prepin, mainchain_prepin)
        shutil.copyfile(generated_tail_prepin, tail_prepin)
        
        print('\nPolymer prepin generation complete.')
        print('PHA type:         ', PHA_type)
        print('Trimer name:      ', trimer_name)
        print('Head prepin:      ', head_prepin)
        print('Mainchain prepin: ', mainchain_prepin)
        print('Tail prepin:      ', tail_prepin)
        return {'PHA_type': PHA_type, 'trimer_name': trimer_name, 'head_code': head_code, 'mainchain_code': mainchain_code, 'tail_code': tail_code, 'head_prepin': head_prepin, 'mainchain_prepin': mainchain_prepin, 'tail_prepin': tail_prepin, 'head_definition': head_definition_file, 'mainchain_definition': mainchain_definition_file, 'tail_definition': tail_definition_file}

    def build_PHA_polymer(self, PHA_type, length, forcefield='gaff2'):
        """
        Build a PHA polymer using existing monomer prepin files.

        Parameters
        ----------
        PHA_type : str
            PHA type name, e.g. "3HB".

        length : int
            Number of repeat units in the polymer.

        forcefield : str, optional
            Amber forcefield leaprc suffix.

        Returns
        -------
        dict
            Paths to generated Amber files and sequence information.

        Notes
        -----
        For length 10, this constructs:

            head + 8 mainchain units + tail

        Required files:

            hP<PHA_type>.prepin
            mP<PHA_type>.prepin
            tP<PHA_type>.prepin
            P<PHA_type>_3.frcmod
        """
        if length < 2:
            raise ValueError('PHA polymer length must be at least 2 so the polymer can have a head and tail unit.')
        self.paths.create_PHA_type_dir(PHA_type)
        self.paths.create_built_PHA_dir(PHA_type, length)
        trimer_name = f'P{PHA_type}_3'
        built_name = self.paths.get_built_PHA_name(PHA_type, length)
        
        monomer_smiles = self.get_monomer_smiles(PHA_type)

        polymer_smiles = self.generate_polymer_smiles_from_sequence(
            [monomer_smiles] * length
        )

        self.save_polymer_smiles(
            polymer_name=built_name,
        smiles=polymer_smiles,
        )
        
        monomer_units_dir = self.paths.get_PHA_monomer_units_dir(PHA_type).resolve()
        trimer_dir = self.paths.get_PHA_trimer_dir(PHA_type).resolve()
        built_leap_dir = self.paths.get_built_PHA_leap_dir(PHA_type, length).resolve()
        built_amber_dir = self.paths.get_built_PHA_amber_dir(PHA_type, length).resolve()
        
        built_leap_dir.mkdir(parents=True, exist_ok=True)
        built_amber_dir.mkdir(parents=True, exist_ok=True)
        
        head_code = self.residue_codes.get_code(PHA_type, 'head')
        mainchain_code = self.residue_codes.get_code(PHA_type, 'mainchain')
        tail_code = self.residue_codes.get_code(PHA_type, 'tail')
        
        if head_code is None:
            raise RuntimeError(f'No head residue code found for {PHA_type}')
        
        if mainchain_code is None:
            raise RuntimeError(f'No mainchain residue code found for {PHA_type}')
        
        if tail_code is None:
            raise RuntimeError(f'No tail residue code found for {PHA_type}')
        head_prepin = monomer_units_dir / f'hP{PHA_type}.prepin'
        mainchain_prepin = monomer_units_dir / f'mP{PHA_type}.prepin'
        tail_prepin = monomer_units_dir / f'tP{PHA_type}.prepin'
        
        frcmod_file = trimer_dir / f'{trimer_name}.frcmod'
        
        required_files = [head_prepin, mainchain_prepin, tail_prepin, frcmod_file]
        
        for file_path in required_files:
            if not file_path.exists():
                raise FileNotFoundError(f'Required file not found:\n{file_path}')
        
        prmtop_file = built_amber_dir / f'{built_name}.prmtop'
        rst7_file = built_amber_dir / f'{built_name}.rst7'
        pdb_file = built_amber_dir / f'{built_name}.pdb'
        leap_file = built_leap_dir / f'build_{built_name}.in'
        leap_log = built_leap_dir / f'leap_{built_name}.log'
        
        sequence_codes = [head_code] + [mainchain_code] * (length - 2) + [tail_code]
        sequence_string = ' '.join(sequence_codes)
        
        leap_contents = f'\nsource leaprc.{forcefield}\n\nloadamberprep {head_prepin}\nloadamberprep {mainchain_prepin}\nloadamberprep {tail_prepin}\n\nloadamberparams {frcmod_file}\n\npolymer = sequence {{ {sequence_string} }}\n\ncheck polymer\n\nsaveamberparm polymer {prmtop_file} {rst7_file}\nsavepdb polymer {pdb_file}\n\nquit\n'
        with open(leap_file, 'w') as f:
            f.write(leap_contents)
        
        tleap_command = f'tleap -f {leap_file} > {leap_log}'
        self.run_command(tleap_command, workdir=built_leap_dir)
        
        print('\nPHA polymer build complete.')
        print('PHA type:   ', PHA_type)
        print('Length:     ', length)
        print('Built name: ', built_name)
        print('Sequence:   ', sequence_string)
        print('Leap file:  ', leap_file)
        print('PRMTOP:     ', prmtop_file)
        print('RST7:       ', rst7_file)
        print('PDB:        ', pdb_file)
        return {'PHA_type': PHA_type, 'length': length, 'built_name': built_name, 'sequence_codes': sequence_codes, 'sequence_string': sequence_string, 'leap_file': leap_file, 'leap_log': leap_log, 'prmtop_file': prmtop_file, 'rst7_file': rst7_file, 'pdb_file': pdb_file}

    def smiles_to_pdb(self, smiles, output_pdb):
        """
        Convert a SMILES string into a 3D PDB structure.

        Parameters
        ----------
        smiles : str
            Input SMILES string.

        output_pdb : str or pathlib.Path
            Path where the generated PDB file should be written.

        Returns
        -------
        pathlib.Path
            Path to the generated PDB file.
        """
        output_pdb = Path(output_pdb)
        molecule = pybel.readstring('smi', smiles)
        molecule.make3D()
        pdb_string = molecule.write('pdb')
        
        with open(output_pdb, 'w') as f:
            f.write(pdb_string)
        return output_pdb

    def replace_pdb_residue_name(self, pdb_file, old_resname, new_resname):
        """
        Replace residue names in a PDB file.

        Parameters
        ----------
        pdb_file : str or pathlib.Path
            PDB file to modify.

        old_resname : str
            Existing residue name to replace.

        new_resname : str
            New residue name to write.

        Notes
        -----
        OpenBabel commonly writes generated structures using the residue name
        `UNL`. AmberTools workflows usually need this to be replaced with the
        assigned trimer residue code.
        """
        pdb_file = Path(pdb_file)
        
        with open(pdb_file, 'r') as f:
            lines = f.readlines()
        
        new_lines = []
        for line in lines:
            new_lines.append(line.replace(f' {old_resname}', f' {new_resname}'))
       
        with open(pdb_file, 'w') as f:
            f.writelines(new_lines)

    def run_command(self, command, workdir=None):
        """
        Run a shell command and report its output.

        Parameters
        ----------
        command : str
            Command to execute.

        workdir : str or pathlib.Path, optional
            Working directory in which to run the command.

        Returns
        -------
        subprocess.CompletedProcess
            Completed subprocess result.

        Raises
        ------
        RuntimeError
            Raised if the command exits with a non-zero return code.
        """
        print('\nRunning command:')
        print(command)
       
        result = subprocess.run(command, shell=True, cwd=workdir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print('Return code:', result.returncode)
       
        if result.stdout:
            print('STDOUT:')
            print(result.stdout)
       
        if result.stderr:
            print('STDERR:')
            print(result.stderr)
       
        if result.returncode != 0:
            raise RuntimeError(f'Command failed:\n{command}')
        
        return result
    
    def build_PHA_copolymer(
        self,
        PHA_types,
        length,
        pattern=None,
        sequence_mode="pattern",
        forcefield="gaff2",
        random_seed=None,
    ):
        """
        Build a PHA copolymer from existing PHA monomer-unit prepins.

        Examples
        --------
        Patterned AB copolymer:

            build_PHA_copolymer(
                PHA_types=["3HB", "4HB"],
                length=10,
                pattern="AB",
                sequence_mode="pattern",
            )

        Random copolymer:

            build_PHA_copolymer(
                PHA_types=["3HB", "4HB"],
                length=10,
                sequence_mode="random",
            )

        Output names
        ------------
        Patterned:
            co_P3HB_P4HB_AB

        Random:
            co_P3HB_P4HB_rand
        """

        import random

        if not isinstance(PHA_types, list):
            raise TypeError("PHA_types must be a list.")

        if len(PHA_types) < 2:
            raise ValueError("At least two PHA types are required.")

        if length < 2:
            raise ValueError(
                "Copolymer length must be at least 2 "
                "so the polymer can have a head and tail."
            )

        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        if len(PHA_types) > len(alphabet):
            raise ValueError("Too many PHA types for single-letter pattern labels.")

        label_to_PHA = {
            alphabet[i]: PHA_types[i]
            for i in range(len(PHA_types))
        }

        # ------------------------------------------------------
        # Generate the copolymer unit sequence
        # ------------------------------------------------------

        if sequence_mode == "pattern":

            if pattern is None:
                raise ValueError(
                    "pattern must be provided when sequence_mode='pattern'."
                )

            for letter in pattern:
                if letter not in label_to_PHA:
                    raise ValueError(
                        f"Pattern letter {letter} has no matching PHA type."
                    )

            if len(pattern) == length:
                expanded_pattern = pattern

            elif (length / len(pattern)).is_integer():
                expanded_pattern = pattern * int(length / len(pattern))

            else:
                raise ValueError(
                    "Pattern and length are incompatible. "
                    "The length must be equal to the pattern length or "
                    "a multiple of it."
                )

            sequence_PHA_types = [
                label_to_PHA[letter]
                for letter in expanded_pattern
            ]

            pattern_label = pattern

        elif sequence_mode == "random":

            if random_seed is not None:
                random.seed(random_seed)

            sequence_PHA_types = [
                random.choice(PHA_types)
                for _ in range(length)
            ]

            pattern_label = "rand"

        else:
            raise ValueError(
                "sequence_mode must be either 'pattern' or 'random'."
            )

        # ------------------------------------------------------
        # Construct output name and directories
        # ------------------------------------------------------

        copolymer_prefix = "_".join(
            [f"P{PHA_type}" for PHA_type in PHA_types]
        )

        copolymer_name = f"co_{copolymer_prefix}_{pattern_label}_{length}"
        
        monomer_smiles_sequence = [
            self.get_monomer_smiles(PHA_type)
            for PHA_type in sequence_PHA_types
        ]

        copolymer_smiles = self.generate_polymer_smiles_from_sequence(       
            monomer_smiles_sequence
        )

        self.save_polymer_smiles(
            polymer_name=copolymer_name,
            smiles=copolymer_smiles,
        )

        built_dir = self.paths.built_PHAs_dir / copolymer_name
        built_leap_dir = built_dir / "leap"
        built_amber_dir = built_dir / "amber"
        built_gromacs_dir = built_dir / "gromacs"

        built_leap_dir.mkdir(parents=True, exist_ok=True)
        built_amber_dir.mkdir(parents=True, exist_ok=True)
        built_gromacs_dir.mkdir(parents=True, exist_ok=True)

        # ------------------------------------------------------
        # Locate prepins, frcmods and residue codes
        # ------------------------------------------------------

        prepin_files = []
        frcmod_files = []

        residue_code_lookup = {}

        for PHA_type in PHA_types:

            self.paths.create_PHA_type_dir(PHA_type)

            monomer_units_dir = (
                self.paths.get_PHA_monomer_units_dir(PHA_type)
                .resolve()
            )

            trimer_dir = (
                self.paths.get_PHA_trimer_dir(PHA_type)
                .resolve()
            )

            trimer_name = f"P{PHA_type}_3"

            head_prepin = monomer_units_dir / f"hP{PHA_type}.prepin"
            mainchain_prepin = monomer_units_dir / f"mP{PHA_type}.prepin"
            tail_prepin = monomer_units_dir / f"tP{PHA_type}.prepin"
            frcmod_file = trimer_dir / f"{trimer_name}.frcmod"

            for file_path in [
                head_prepin,
                mainchain_prepin,
                tail_prepin,
                frcmod_file,
            ]:
                if not file_path.exists():
                    raise FileNotFoundError(
                        f"Required file not found for {PHA_type}:\n"
                        f"{file_path}"
                    )

            prepin_files.extend(
                [
                    head_prepin,
                    mainchain_prepin,
                    tail_prepin,
                ]
            )

            frcmod_files.append(frcmod_file)

            head_code = self.residue_codes.get_code(
                PHA_type,
                "head",
            )

            mainchain_code = self.residue_codes.get_code(
                PHA_type,
                "mainchain",
            )

            tail_code = self.residue_codes.get_code(
                PHA_type,
                "tail",
            )

            if head_code is None:
                raise RuntimeError(
                    f"No head residue code found for {PHA_type}"
                )

            if mainchain_code is None:
                raise RuntimeError(
                    f"No mainchain residue code found for {PHA_type}"
                )

            if tail_code is None:
                raise RuntimeError(
                    f"No tail residue code found for {PHA_type}"
                )

            residue_code_lookup[PHA_type] = {
                "head": head_code,
                "mainchain": mainchain_code,
                "tail": tail_code,
            }

        # ------------------------------------------------------
        # Convert PHA sequence into tleap residue-code sequence
        # ------------------------------------------------------

        sequence_codes = []

        for i, PHA_type in enumerate(sequence_PHA_types):

            if i == 0:
                sequence_codes.append(
                    residue_code_lookup[PHA_type]["head"]
                )

            elif i == length - 1:
                sequence_codes.append(
                    residue_code_lookup[PHA_type]["tail"]
                )

            else:
                sequence_codes.append(
                    residue_code_lookup[PHA_type]["mainchain"]
                )

        sequence_string = " ".join(sequence_codes)

        # ------------------------------------------------------
        # Write and run tleap input
        # ------------------------------------------------------

        prmtop_file = (
            built_amber_dir /
            f"{copolymer_name}.prmtop"
        ).resolve()

        rst7_file = (
            built_amber_dir /
            f"{copolymer_name}.rst7"
        ).resolve()

        pdb_file = (
            built_amber_dir /
            f"{copolymer_name}.pdb"
        ).resolve()

        leap_file = (
            built_leap_dir /
            f"build_{copolymer_name}.in"
        ).resolve()

        leap_log = (
            built_leap_dir /
            f"leap_{copolymer_name}.log"
        ).resolve()

        prepin_load_lines = "\n".join(
            [
                f"loadamberprep {prepin_file}"
                for prepin_file in prepin_files
            ]
        )

        frcmod_load_lines = "\n".join(
            [
                f"loadamberparams {frcmod_file}"
                for frcmod_file in frcmod_files
            ]
        )

        leap_contents = f"""
source leaprc.{forcefield}

{prepin_load_lines}

{frcmod_load_lines}

polymer = sequence {{ {sequence_string} }}

check polymer

saveamberparm polymer {prmtop_file} {rst7_file}
savepdb polymer {pdb_file}

quit
"""

        with open(leap_file, "w") as f:
            f.write(leap_contents)

        tleap_command = (
            f"tleap "
            f"-f {leap_file.name} "
            f"> {leap_log.name}"
        )

        self.run_command(
            tleap_command,
            workdir=built_leap_dir,
        )

        print("\nPHA copolymer build complete.")
        print("Copolymer name: ", copolymer_name)
        print("PHA types:      ", PHA_types)
        print("Length:         ", length)
        print("Sequence:       ", sequence_PHA_types)
        print("Residue codes:  ", sequence_string)
        print("PRMTOP:         ", prmtop_file)
        print("RST7:           ", rst7_file)
        print("PDB:            ", pdb_file)

        return {
            "copolymer_name": copolymer_name,
            "PHA_types": PHA_types,
            "length": length,
            "pattern": pattern,
            "sequence_mode": sequence_mode,
            "sequence_PHA_types": sequence_PHA_types,
            "sequence_codes": sequence_codes,
            "sequence_string": sequence_string,
            "leap_file": leap_file,
            "leap_log": leap_log,
            "prmtop_file": prmtop_file,
            "rst7_file": rst7_file,
            "pdb_file": pdb_file,
            "built_dir": built_dir,
            "amber_dir": built_amber_dir,
            "gromacs_dir": built_gromacs_dir,
        }
    
    def _ensure_polymer_smiles_csv_exists(self):

        """
        Create polymer_smiles.csv if it does not exist.
        """

        import csv
        csv_path = self.paths.get_polymer_smiles_csv()
        if not csv_path.exists():
            csv_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            with open(csv_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        "polymer_name",
                        "smiles",
                    ]
                )
        return csv_path
    
    def get_monomer_smiles(self, PHA_type):

        """
        Get the monomer SMILES for a PHA type from residue_codes.csv.
        """

        rows = self.residue_codes.load_rows()
        for row in rows:
            if (
                row["PHA_type"] == PHA_type
                and row["component"] == "mainchain"
            ):
                return row["smiles"]
        raise RuntimeError(
            f"No monomer SMILES found for {PHA_type}."
        )

    def generate_polymer_smiles_from_sequence(
        self,
        monomer_smiles_sequence,
    ):

        """
        Generate a polymer SMILES string from monomer SMILES.
        Rule

        ----

        For every monomer except the final one, remove the trailing character
        before joining.
        
        Example

        -------

        ["OCCCC(=O)O", "OCCCC(=O)O", "OCCCC(=O)O"]
        
        becomes:

            OCCCC(=O)OCCCC(=O)OCCCC(=O)O

        """

        if len(monomer_smiles_sequence) == 0:
            raise ValueError(
                "monomer_smiles_sequence cannot be empty."
            )

        polymer_smiles = ""

        for i, monomer_smiles in enumerate(monomer_smiles_sequence):
            if i == len(monomer_smiles_sequence) - 1:
                polymer_smiles += monomer_smiles
            else:
                polymer_smiles += monomer_smiles[:-1]
        return polymer_smiles

    def save_polymer_smiles(
        self,
        polymer_name,
        smiles,
    ):

        """
        Save or update a polymer SMILES entry in polymer_smiles.csv.

        """

        import csv

        csv_path = self._ensure_polymer_smiles_csv_exists()
        rows = []
        with open(csv_path, "r", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        updated = False
        for row in rows:
            if row["polymer_name"] == polymer_name:
                row["smiles"] = smiles
                updated = True
        if not updated:
            rows.append(
                {
                    "polymer_name": polymer_name,
                    "smiles": smiles,
                }
            )

        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "polymer_name",
                    "smiles",
                ],
            )

            writer.writeheader()
            writer.writerows(rows)

        print(
            f"Saved polymer SMILES for {polymer_name}."
        )

        return csv_path