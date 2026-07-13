#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PHA structure database management.

This module provides lightweight management classes for a PHA-specific
structure database.

Classes
-------
PHAFileManager
    Handles directory creation, filepath construction and simple file lookup.

PHAResidueCodeManager
    Handles the residue code registry stored in residue_codes.csv.

Notes
-----
This module should not contain chemistry-building logic. Parameterisation,
prepin generation and polymer construction should live in the polymer builder
layer.
"""
from pathlib import Path
import csv
import itertools
import re
import parmed as pmd

class PHAFileManager:
    """
    Manage paths for the PHA structure database.

    This class is the central source of truth for directory names,
    system names, and file locations.
    """

    def __init__(self, root_dir="structure_database"):
        self.root_dir = Path(root_dir)

        # Main database directories
        self.PHA_types_dir = self.root_dir / "PHA_types"
        self.built_PHAs_dir = self.root_dir / "built_PHAs"
        self.PHA_melts_dir = self.root_dir / "PHA_melts"

        self.PHA_dry_dir = self.root_dir / "PHA_dry"
        self.PHA_solvated_dir = self.root_dir / "PHA_solvated"
        self.PHA_solvated_ions_dir = self.root_dir / "PHA_solvated_ions"

        self.temp_dir = self.root_dir / "temp"

        # Database files
        self.residue_codes_csv = self.root_dir / "residue_codes.csv"
        self.polymer_smiles_csv = self.root_dir / "polymer_smiles.csv"
        self.md_systems_csv = self.root_dir / "md_systems.csv"

        self._create_base_structure()

    def _create_base_structure(self):
        """
        Create the main structure-database directories.
        """

        for directory in [
            self.root_dir,
            self.PHA_types_dir,
            self.built_PHAs_dir,
            self.PHA_melts_dir,
            self.PHA_dry_dir,
            self.PHA_solvated_dir,
            self.PHA_solvated_ions_dir,
            self.temp_dir,
        ]:
            directory.mkdir(
                parents=True,
                exist_ok=True,
            )

    # ======================================================
    # Base files and directories
    # ======================================================

    def get_root_dir(self):
        return self.root_dir

    def get_temp_dir(self):
        return self.temp_dir

    def get_residue_codes_csv(self):
        return self.residue_codes_csv

    def get_polymer_smiles_csv(self):
        return self.polymer_smiles_csv
    
    def get_md_systems_csv(self):
        """
        Return the path to md_systems.csv.
        """
        return self.md_systems_csv

    # ======================================================
    # PHA type and parameterisation directories
    # ======================================================

    def get_PHA_type_dir(self, PHA_type):
        return self.PHA_types_dir / PHA_type

    def create_PHA_type_dir(self, PHA_type):
        pha_dir = self.get_PHA_type_dir(PHA_type)

        for subdir in [
            "input",
            "trimer",
            "monomer_units",
            "leap_templates",
        ]:
            (pha_dir / subdir).mkdir(
                parents=True,
                exist_ok=True,
            )

        return pha_dir

    def get_PHA_input_dir(self, PHA_type):
        return self.get_PHA_type_dir(PHA_type) / "input"

    def get_PHA_trimer_dir(self, PHA_type):
        return self.get_PHA_type_dir(PHA_type) / "trimer"

    def get_PHA_monomer_units_dir(self, PHA_type):
        return self.get_PHA_type_dir(PHA_type) / "monomer_units"

    def get_PHA_leap_template_dir(self, PHA_type):
        return self.get_PHA_type_dir(PHA_type) / "leap_templates"

    def get_PHA_monomer_unit_files(self, PHA_type):
        """
        Return the parameter files for one PHA chemistry.
        """

        monomer_units_dir = self.get_PHA_monomer_units_dir(PHA_type)
        trimer_dir = self.get_PHA_trimer_dir(PHA_type)

        return {
            "monomer_units_dir": monomer_units_dir,
            "head_prepin": monomer_units_dir / f"hP{PHA_type}.prepin",
            "mainchain_prepin": monomer_units_dir / f"mP{PHA_type}.prepin",
            "tail_prepin": monomer_units_dir / f"tP{PHA_type}.prepin",
            "frcmod": trimer_dir / f"P{PHA_type}_3.frcmod",
        }

    # ======================================================
    # Built single-chain PHA polymers
    # ======================================================

    def get_built_PHA_name(self, PHA_type, length):
        return f"P{PHA_type}_{length}"

    def parse_built_PHA_name(self, polymer_name):
        """
        Parse a polymer name such as P3HB_10.

        Returns
        -------
        tuple
            PHA type and polymer length.
        """

        match = re.fullmatch(r"P(.+)_(\d+)", polymer_name)

        if match is None:
            raise ValueError(
                f"Invalid polymer name: {polymer_name}\n"
                "Expected format like: P3HB_10"
            )

        PHA_type = match.group(1)
        length = int(match.group(2))

        return PHA_type, length

    def get_built_PHA_dir(self, PHA_type, length):
        polymer_name = self.get_built_PHA_name(
            PHA_type,
            length,
        )

        return self.built_PHAs_dir / polymer_name

    def create_built_PHA_dir(self, PHA_type, length):
        build_dir = self.get_built_PHA_dir(
            PHA_type,
            length,
        )

        for subdir in [
            "leap",
            "amber",
            "gromacs",
        ]:
            (build_dir / subdir).mkdir(
                parents=True,
                exist_ok=True,
            )

        return build_dir

    def get_built_PHA_leap_dir(self, PHA_type, length):
        return self.get_built_PHA_dir(PHA_type, length) / "leap"

    def get_built_PHA_amber_dir(self, PHA_type, length):
        return self.get_built_PHA_dir(PHA_type, length) / "amber"

    def get_built_PHA_gromacs_dir(self, PHA_type, length):
        return self.get_built_PHA_dir(PHA_type, length) / "gromacs"

    def get_built_PHA_amber_files(self, polymer_name):
        """
        Return expected Amber files for an already-built polymer.
        """

        PHA_type, length = self.parse_built_PHA_name(polymer_name)

        amber_dir = self.get_built_PHA_amber_dir(
            PHA_type,
            length,
        )

        return {
            "amber_dir": amber_dir,
            "pdb": amber_dir / f"{polymer_name}.pdb",
            "prmtop": amber_dir / f"{polymer_name}.prmtop",
            "rst7": amber_dir / f"{polymer_name}.rst7",
        }

    # ======================================================
    # Dry single-chain PHA systems
    # ======================================================

    def get_PHA_dry_dir(self):
        """
        Return the parent directory for all dry PHA systems.
        """

        return self.PHA_dry_dir

    def get_dry_PHA_system_name(self, polymer_name):
        return f"{polymer_name}_dry"

    def get_dry_PHA_dir(self, polymer_name):
        system_name = self.get_dry_PHA_system_name(polymer_name)

        return self.get_PHA_dry_dir() / system_name

    def get_dry_PHA_inputs_dir(self, polymer_name):
        return self.get_dry_PHA_dir(polymer_name) / "inputs"

    def get_dry_PHA_simulations_dir(self, polymer_name):
        return self.get_dry_PHA_dir(polymer_name) / "simulations"

    def create_dry_PHA_dir(self, polymer_name):
        system_dir = self.get_dry_PHA_dir(polymer_name)

        system_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.get_dry_PHA_inputs_dir(polymer_name).mkdir(
            parents=True,
            exist_ok=True,
        )

        self.get_dry_PHA_simulations_dir(polymer_name).mkdir(
            parents=True,
            exist_ok=True,
        )

        return system_dir

    # ======================================================
    # Solvated single-chain PHA systems
    # ======================================================

    def get_PHA_solvated_dir(self):
        """
        Return the parent directory for all solvated PHA systems.
        """

        return self.PHA_solvated_dir

    def get_solvated_PHA_system_name(self, polymer_name):
        return f"{polymer_name}_solvated"

    def get_solvated_PHA_dir(self, polymer_name):
        system_name = self.get_solvated_PHA_system_name(polymer_name)

        return self.get_PHA_solvated_dir() / system_name

    def get_solvated_PHA_inputs_dir(self, polymer_name):
        return self.get_solvated_PHA_dir(polymer_name) / "inputs"

    def get_solvated_PHA_simulations_dir(self, polymer_name):
        return self.get_solvated_PHA_dir(polymer_name) / "simulations"

    def create_solvated_PHA_dir(self, polymer_name):
        system_dir = self.get_solvated_PHA_dir(polymer_name)

        system_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.get_solvated_PHA_inputs_dir(polymer_name).mkdir(
            parents=True,
            exist_ok=True,
        )

        self.get_solvated_PHA_simulations_dir(polymer_name).mkdir(
            parents=True,
            exist_ok=True,
        )

        return system_dir

    # ======================================================
    # Solvated + ionised single-chain PHA systems
    # ======================================================

    def get_PHA_solvated_ions_dir(self):
        """
        Return the parent directory containing all solvated + ionised PHA systems.
        """
        return self.PHA_solvated_ions_dir

    def format_concentration_label(self, ion_concentration):
        """
        Convert an ion concentration into a filename-safe label.

        Example
        -------
        0.15 -> 0_15
        """
        return str(ion_concentration).replace(".", "_")

    def get_solvated_ions_PHA_system_name(
        self,
        polymer_name,
        salt,
        ion_concentration,
    ):
        """
        Return the standard name for a solvated + ionised PHA system.

        Example
        -------
        P3HB_10_solvated_KCl_0_15
        """
        concentration_label = self.format_concentration_label(
            ion_concentration
        )

        return (
            f"{polymer_name}_solvated_"
            f"{salt}_{concentration_label}"
        )

    def get_solvated_ions_PHA_dir(
        self,
        polymer_name,
        salt,
        ion_concentration,
    ):
        """
        Return the directory for a solvated + ionised PHA system.
        """
        system_name = self.get_solvated_ions_PHA_system_name(
            polymer_name=polymer_name,
            salt=salt,
            ion_concentration=ion_concentration,
        )

        return self.get_PHA_solvated_ions_dir() / system_name

    def get_solvated_ions_PHA_inputs_dir(
        self,
        polymer_name,
        salt,
        ion_concentration,
    ):
        """
        Return the inputs directory for a solvated + ionised PHA system.
        """
        return (
            self.get_solvated_ions_PHA_dir(
                polymer_name=polymer_name,
                salt=salt,
                ion_concentration=ion_concentration,
            )
            / "inputs"
        )

    def get_solvated_ions_PHA_simulations_dir(
        self,
        polymer_name,
        salt,
        ion_concentration,
    ):
        """
        Return the simulations directory for a solvated + ionised PHA system.
        """
        return (
            self.get_solvated_ions_PHA_dir(
                polymer_name=polymer_name,
                salt=salt,
                ion_concentration=ion_concentration,
            )
            / "simulations"
        )

    def create_solvated_ions_PHA_dir(
        self,
        polymer_name,
        salt,
        ion_concentration,
    ):
        """
        Create the directory structure for a solvated + ionised PHA system.
        """
        system_dir = self.get_solvated_ions_PHA_dir(
            polymer_name=polymer_name,
            salt=salt,
            ion_concentration=ion_concentration,
        )

        system_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.get_solvated_ions_PHA_inputs_dir(
            polymer_name=polymer_name,
            salt=salt,
            ion_concentration=ion_concentration,
        ).mkdir(
            parents=True,
            exist_ok=True,
        )

        self.get_solvated_ions_PHA_simulations_dir(
            polymer_name=polymer_name,
            salt=salt,
            ion_concentration=ion_concentration,
        ).mkdir(
            parents=True,
            exist_ok=True,
        )

        return system_dir
    # ======================================================
    # PHA melts
    # ======================================================

    def get_PHA_melt_name(
        self,
        polymer_names,
        number_of_polymers,
    ):
        if len(polymer_names) != len(number_of_polymers):
            raise ValueError(
                "polymer_names and number_of_polymers must have "
                "the same length."
            )

        name_parts = []

        for polymer_name, number in zip(
            polymer_names,
            number_of_polymers,
        ):
            name_parts.append(
                f"{number}_{polymer_name}"
            )

        return "_".join(name_parts) + "_melt"

    def get_PHA_melt_dir(
        self,
        polymer_names,
        number_of_polymers,
    ):
        melt_name = self.get_PHA_melt_name(
            polymer_names,
            number_of_polymers,
        )

        return self.PHA_melts_dir / melt_name

    def create_PHA_melt_dir(
        self,
        polymer_names,
        number_of_polymers,
    ):
        melt_dir = self.get_PHA_melt_dir(
            polymer_names,
            number_of_polymers,
        )

        melt_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.get_PHA_melt_inputs_dir(
            polymer_names,
            number_of_polymers,
        ).mkdir(
            parents=True,
            exist_ok=True,
        )

        self.get_PHA_melt_simulations_dir(
            polymer_names,
            number_of_polymers,
        ).mkdir(
            parents=True,
            exist_ok=True,
        )

        return melt_dir

    def get_PHA_melt_inputs_dir(
        self,
        polymer_names,
        number_of_polymers,
    ):
        return (
            self.get_PHA_melt_dir(
                polymer_names,
                number_of_polymers,
            )
            / "inputs"
        )

    def get_PHA_melt_simulations_dir(
        self,
        polymer_names,
        number_of_polymers,
    ):
        return (
            self.get_PHA_melt_dir(
                polymer_names,
                number_of_polymers,
            )
            / "simulations"
        )

    def create_PHA_melt_simulation_run_dir(
        self,
        polymer_names,
        number_of_polymers,
        timestamp=None,
    ):
        from datetime import datetime

        if timestamp is None:
            timestamp = datetime.now().strftime(
                "%Y-%m-%d_%H%M%S"
            )

        run_dir = (
            self.get_PHA_melt_simulations_dir(
                polymer_names,
                number_of_polymers,
            )
            / timestamp
        )

        run_dir.mkdir(
            parents=True,
            exist_ok=False,
        )

        return run_dir

    def create_named_PHA_melt_simulation_run_dir(
        self,
        polymer_names,
        number_of_polymers,
        run_name,
    ):
        simulations_dir = self.get_PHA_melt_simulations_dir(
            polymer_names,
            number_of_polymers,
        )

        simulations_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        run_name = run_name.strip().replace(" ", "_")

        if not run_name:
            raise ValueError("run_name cannot be empty.")

        counter = 1

        while True:
            candidate_dir = (
                simulations_dir
                / f"{run_name}_{counter:02d}"
            )

            if not candidate_dir.exists():
                candidate_dir.mkdir(
                    parents=True,
                    exist_ok=False,
                )

                return candidate_dir

            counter += 1

    # ======================================================
    # Molecular dynamics system registry
    # ======================================================

    def ensure_md_systems_csv_exists(self):
        """
        Create md_systems.csv if it does not already exist.
        """

        header = [
            "system_name",
            "system_type",
            "number_of_atoms",
        ]

        if not self.md_systems_csv.exists():
            self.md_systems_csv.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            with open(
                self.md_systems_csv,
                "w",
                newline="",
            ) as file:
                writer = csv.writer(file)
                writer.writerow(header)

        return self.md_systems_csv

    def load_md_systems(self):
        """
        Load all registered molecular dynamics systems.

        Returns
        -------
        list[dict]
            Rows from md_systems.csv.
        """

        self.ensure_md_systems_csv_exists()

        with open(
            self.md_systems_csv,
            "r",
            newline="",
        ) as file:
            reader = csv.DictReader(file)
            return list(reader)

    def md_system_exists(self, system_name):
        """
        Check whether a molecular dynamics system is already registered.
        """

        systems = self.load_md_systems()

        return any(
            row["system_name"] == system_name
            for row in systems
        )

    def register_md_system(
        self,
        system_name,
        system_type,
        number_of_atoms=None,
    ):
        """
        Add or update a system in md_systems.csv.

        Parameters
        ----------
        system_name : str
            Unique name of the prepared molecular dynamics system.

        system_type : str
            Type of system, for example:

                dry
                solvated
                solvated_ions
                melt

        number_of_atoms : int, optional
            Number of atoms in the system. If unavailable, the field is left
            blank.
        """

        allowed_system_types = {
            "dry",
            "solvated",
            "solvated_ions",
            "melt",
        }

        if not isinstance(system_name, str) or not system_name.strip():
            raise ValueError(
                "system_name must be a non-empty string."
            )

        if system_type not in allowed_system_types:
            raise ValueError(
                f"Unsupported system type: {system_type}\n"
                f"Allowed values: {sorted(allowed_system_types)}"
            )

        if number_of_atoms is not None:
            number_of_atoms = int(number_of_atoms)

            if number_of_atoms <= 0:
                raise ValueError(
                    "number_of_atoms must be greater than zero."
                )

        self.ensure_md_systems_csv_exists()

        systems = self.load_md_systems()

        new_row = {
            "system_name": system_name.strip(),
            "system_type": system_type,
            "number_of_atoms": (
                str(number_of_atoms)
                if number_of_atoms is not None
                else ""
            ),
        }

        system_updated = False

        for index, row in enumerate(systems):
            if row["system_name"] == system_name:
                systems[index] = new_row
                system_updated = True
                break

        if not system_updated:
            systems.append(new_row)

        with open(
            self.md_systems_csv,
            "w",
            newline="",
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "system_name",
                    "system_type",
                    "number_of_atoms",
                ],
            )

            writer.writeheader()
            writer.writerows(systems)

        action = "Updated" if system_updated else "Registered"

        print(
            f"{action} MD system: "
            f"{system_name} "
            f"({system_type}, "
            f"{number_of_atoms or 'unknown'} atoms)"
        )

        return new_row
    
    # ======================================================
    # General helpers
    # ======================================================

    def find_file(self, directory, extension):
        directory = Path(directory)

        files = sorted(
            directory.glob(f"*.{extension}")
        )

        if not files:
            return None

        return files[0]

    def find_files(self, directory, extension):
        directory = Path(directory)

        return sorted(
            directory.glob(f"*.{extension}")
        )
    
    def count_atoms_from_amber_topology(self, prmtop_path):
        """
        Return the number of atoms stored in an Amber topology.
        """

        prmtop_path = Path(prmtop_path)

        if not prmtop_path.exists():
            raise FileNotFoundError(
                f"Amber topology file not found:\n{prmtop_path}"
                )

        structure = pmd.load_file(
            str(prmtop_path)
            )

        return len(structure.atoms)
    
    def count_atoms_from_gromacs_gro(
        self,
        gro_path,
    ):
        """
        Count atoms in a GROMACS GRO coordinate file.

        The second line of a GRO file contains the total number of atoms.

        Parameters
        ----------
        gro_path : str or pathlib.Path
            Path to the GROMACS GRO coordinate file.

        Returns
        -------
        int
            Number of atoms in the system.
        """

        gro_path = Path(gro_path)

        if not gro_path.exists():
            raise FileNotFoundError(
                f"GROMACS coordinate file not found:\n{gro_path}"
            )

        with open(
            gro_path,
            "r",
            encoding="utf-8",
            errors="replace",
        ) as file:
            title_line = file.readline()
            atom_count_line = file.readline()

        if not title_line or not atom_count_line:
            raise ValueError(
                f"GROMACS GRO file is incomplete:\n{gro_path}"
            )

        try:
            number_of_atoms = int(
                atom_count_line.strip()
            )

        except ValueError as error:
            raise ValueError(
                "Could not read the atom count from the second "
                f"line of:\n{gro_path}"
            ) from error

        if number_of_atoms <= 0:
            raise ValueError(
                f"Invalid atom count in GRO file: {number_of_atoms}"
            )

        print(f"Number of atoms: {number_of_atoms}")

        return number_of_atoms

class PHAResidueCodeManager:
    """
    Manage the PHA residue code registry.

    The residue code CSV links user-facing PHA names to internal Amber-style
    residue codes.

    Expected CSV format:

        PHA_type,component,readable_name,residue_code,smiles

        3HB,trimer,P3HB_3,AAA,...
        3HB,head,hP3HB,AAB,...
        3HB,mainchain,mP3HB,AAC,...
        3HB,tail,tP3HB,AAD,...

    Parameters
    ----------
    paths : PHAFileManager
        Filepath manager used to locate residue_codes.csv.
    """
    forbidden_codes = {'UNL', 'ALA', 'ARG', 'ASN', 'ASP', 'ASX', 'CYS', 'GLU', 'GLN', 'GLX', 'HIS', 'ILE', 'LEU', 'LYS', 'MET', 'PHE', 'PRO', 'SER', 'THR', 'SEC', 'TRP', 'TYR', 'VAL'}
    header = ['PHA_type', 'component', 'readable_name', 'residue_code', 'smiles']

    def __init__(self, paths):
        """
        Initialise the residue code manager.

        Parameters
        ----------
        paths : PHAFileManager
            Filepath manager instance.
        """
        self.paths = paths
        self.csv_path = self.paths.get_residue_codes_csv()
        self._ensure_csv_exists()

    def _ensure_csv_exists(self):
        """
        Create residue_codes.csv if it does not already exist.
        """
        if not self.csv_path.exists():
            self.csv_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.csv_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.header)

    def load_rows(self):
        """
        Load all rows from residue_codes.csv.

        Returns
        -------
        list[dict]
            List of CSV entries.
        """
        with open(self.csv_path, 'r', newline='') as f:
            reader = csv.DictReader(f)
            return list(reader)

    def get_used_codes(self):
        """
        Return all residue codes currently stored in the CSV.

        Returns
        -------
        set
            Set of used residue codes.
        """
        rows = self.load_rows()
        return {row['residue_code'] for row in rows}

    def PHA_type_exists(self, PHA_type):
        """
        Check whether a PHA type has already been registered.

        Parameters
        ----------
        PHA_type : str

        Returns
        -------
        bool
        """
        rows = self.load_rows()
        return any((row['PHA_type'] == PHA_type for row in rows))

    def get_code(self, PHA_type, component):
        """
        Return the residue code for a given PHA component.

        Parameters
        ----------
        PHA_type : str

        component : str
            One of:

                trimer
                head
                mainchain
                tail

        Returns
        -------
        str or None
        """
        rows = self.load_rows()
        for row in rows:
            if row['PHA_type'] == PHA_type and row['component'] == component:
                return row['residue_code']
        return None

    def generate_unique_codes(self, number_of_codes):
        """
        Generate multiple unique residue codes.

        Examples
        --------

        Existing CSV:

            AAA
            AAB

        generate_unique_codes(4)

        Returns:

            AAC
            AAD
            AAE
            AAF

        Parameters
        ----------
        number_of_codes : int

        Returns
        -------
        list[str]
        """
        used_codes = self.get_used_codes()
        new_codes = []
        for letters in itertools.product('ABCDEFGHIJKLMNOPQRSTUVWXYZ', repeat=3):
            code = ''.join(letters)
            if code in used_codes:
                continue
            if code in new_codes:
                continue
            if code in self.forbidden_codes:
                continue
            new_codes.append(code)
            if len(new_codes) == number_of_codes:
                return new_codes
        raise RuntimeError(f'Could not generate {number_of_codes} unique residue codes.')

    def register_PHA_type(self, PHA_type, trimer_name, trimer_smiles, monomer_smiles):
        """
        Register a new PHA type.

        Creates four residue entries:

            trimer
            head
            mainchain
            tail

        Example
        -------

        PHA_type = "3HB"

        trimer_name = "P3HB_3"

        Generates:

            AAA  trimer
            AAB  head
            AAC  mainchain
            AAD  tail

        Parameters
        ----------
        PHA_type : str

        trimer_name : str

        trimer_smiles : str

        monomer_smiles : str
        """
        if self.PHA_type_exists(PHA_type):
            print(f'PHA type {PHA_type} already exists in residue code CSV.')
            return
        trimer_code, head_code, mainchain_code, tail_code = self.generate_unique_codes(4)
        entries = [{'PHA_type': PHA_type, 'component': 'trimer', 'readable_name': trimer_name, 'residue_code': trimer_code, 'smiles': trimer_smiles}, {'PHA_type': PHA_type, 'component': 'head', 'readable_name': f'hP{PHA_type}', 'residue_code': head_code, 'smiles': monomer_smiles}, {'PHA_type': PHA_type, 'component': 'mainchain', 'readable_name': f'mP{PHA_type}', 'residue_code': mainchain_code, 'smiles': monomer_smiles}, {'PHA_type': PHA_type, 'component': 'tail', 'readable_name': f'tP{PHA_type}', 'residue_code': tail_code, 'smiles': monomer_smiles}]
        with open(self.csv_path, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.header)
            for entry in entries:
                writer.writerow(entry)
        print(f'Registered residue codes for {PHA_type}.')


