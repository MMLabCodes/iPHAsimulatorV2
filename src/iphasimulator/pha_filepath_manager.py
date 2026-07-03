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

class PHAFileManager:
    """
    Manage paths for a PHA structure database.

    The expected root directory layout is:

        structure_database/
            residue_codes.csv
            temp/
            PHA_types/
                <PHA_type>/
                    input/
                    trimer/
                    monomer_units/
                    leap_templates/
            built_PHAs/
                P<PHA_type>_<length>/
                    leap/
                    amber/
            PHA_melts/
                P<PHA_type>_<length>_<number_of_chains>chains_amorph/

    Parameters
    ----------
    root_dir : str or pathlib.Path, optional
        Root directory of the structure database.
    """

    def __init__(self, root_dir='structure_database'):
        """Initialise the filepath manager and create the base database layout.

Parameters
----------
root_dir : str or pathlib.Path, optional
    Root directory for the PHA structure database."""
        self.root_dir = Path(root_dir)
        self.PHA_types_dir = self.root_dir / 'PHA_types'
        self.built_PHAs_dir = self.root_dir / 'built_PHAs'
        self.PHA_melts_dir = self.root_dir / 'PHA_melts'
        self.temp_dir = self.root_dir / 'temp'
        self.residue_codes_csv = self.root_dir / 'residue_codes.csv'
        self.polymer_smiles_csv = self.root_dir / "polymer_smiles.csv"
        self._create_base_structure()

    def _create_base_structure(self):
        """
        Create the base directory structure if it does not already exist.
        """
        self.root_dir.mkdir(exist_ok=True)
        self.PHA_types_dir.mkdir(exist_ok=True)
        self.built_PHAs_dir.mkdir(exist_ok=True)
        self.PHA_melts_dir.mkdir(exist_ok=True)
        self.temp_dir.mkdir(exist_ok=True)

    def get_root_dir(self):
        """
        Return the root structure database directory.
        """
        return self.root_dir

    def get_temp_dir(self):
        """
        Return the temporary working directory.
        """
        return self.temp_dir

    def get_residue_codes_csv(self):
        """
        Return the path to residue_codes.csv.
        """
        return self.residue_codes_csv

    def get_PHA_type_dir(self, PHA_type):
        """
        Return the directory for a parameterised PHA type.
        """
        return self.PHA_types_dir / PHA_type

    def create_PHA_type_dir(self, PHA_type):
        """
        Create the directory structure for a parameterised PHA type.
        """
        pha_dir = self.get_PHA_type_dir(PHA_type)
        subdirs = ['input', 'trimer', 'monomer_units', 'leap_templates']
        pha_dir.mkdir(exist_ok=True)
        for subdir in subdirs:
            (pha_dir / subdir).mkdir(exist_ok=True)
        return pha_dir

    def get_PHA_input_dir(self, PHA_type):
        """
        Return the input directory for a PHA type.
        """
        return self.get_PHA_type_dir(PHA_type) / 'input'

    def get_PHA_trimer_dir(self, PHA_type):
        """
        Return the trimer parameter directory for a PHA type.
        """
        return self.get_PHA_type_dir(PHA_type) / 'trimer'

    def get_PHA_monomer_units_dir(self, PHA_type):
        """
        Return the monomer unit prepin directory for a PHA type.
        """
        return self.get_PHA_type_dir(PHA_type) / 'monomer_units'

    def get_PHA_leap_template_dir(self, PHA_type):
        """
        Return the tleap template directory for a PHA type.
        """
        return self.get_PHA_type_dir(PHA_type) / 'leap_templates'

    def get_built_PHA_name(self, PHA_type, length):
        """
        Return the standard name for a built PHA polymer.
        """
        return f'P{PHA_type}_{length}'

    def get_built_PHA_dir(self, PHA_type, length):
        """
        Return the directory for a built PHA polymer.
        """
        polymer_name = self.get_built_PHA_name(PHA_type, length)
        return self.built_PHAs_dir / polymer_name

    def create_built_PHA_dir(self, PHA_type, length):
        """
        Create the directory structure for a built PHA polymer.
        """
        build_dir = self.get_built_PHA_dir(PHA_type, length)
        subdirs = ['leap', 'amber', 'gromacs']
        build_dir.mkdir(exist_ok=True)
        for subdir in subdirs:
            (build_dir / subdir).mkdir(exist_ok=True)
        return build_dir

    def get_built_PHA_leap_dir(self, PHA_type, length):
        """
        Return the tleap directory for a built PHA polymer.
        """
        return self.get_built_PHA_dir(PHA_type, length) / 'leap'

    def get_built_PHA_amber_dir(self, PHA_type, length):
        """
        Return the Amber output directory for a built PHA polymer.
        """
        return self.get_built_PHA_dir(PHA_type, length) / 'amber'

    def get_built_PHA_gromacs_dir(self, PHA_type, length):
        """
        Return the gromacs output directory for a built PHA polymer.
        """
        return self.get_built_PHA_dir(PHA_type, length) / 'gromacs'

    def get_PHA_melt_name(self, polymer_names, number_of_polymers):
        """

        Return the standard name for a PHA melt system.

        Examples

        --------

        ["P3HB_10"], [25]

            -> 25_P3HB_10_melt

        ["P3HB_10", "P4HB_10"], [25, 25]

            -> 25_P3HB_10_25_P4HB_10_melt

        """
        if len(polymer_names) != len(number_of_polymers):
            raise ValueError('polymer_names and number_of_polymers must have the same length.')
        name_parts = []
        for polymer_name, number in zip(polymer_names, number_of_polymers):
            name_parts.append(f'{number}_{polymer_name}')
        return '_'.join(name_parts) + '_melt'

    def get_PHA_melt_dir(self, polymer_names, number_of_polymers):
        """

        Return the directory for a PHA melt system.

        """
        melt_name = self.get_PHA_melt_name(polymer_names, number_of_polymers)
        return self.PHA_melts_dir / melt_name

    def create_PHA_melt_dir(self, polymer_names, number_of_polymers):
        """

        Create the directory for a PHA melt system.

        Creates:

            PHA_melts/<melt_name>/

                inputs/

                simulations/

        Timestamped simulation folders are not created here.

        """
        melt_dir = self.get_PHA_melt_dir(polymer_names, number_of_polymers)
        melt_dir.mkdir(parents=True, exist_ok=True)
        self.get_PHA_melt_inputs_dir(polymer_names, number_of_polymers).mkdir(parents=True, exist_ok=True)
        self.get_PHA_melt_simulations_dir(polymer_names, number_of_polymers).mkdir(parents=True, exist_ok=True)
        return melt_dir

    def get_PHA_melt_inputs_dir(self, polymer_names, number_of_polymers):
        """

        Return the inputs directory for a PHA melt.

        """
        return self.get_PHA_melt_dir(polymer_names, number_of_polymers) / 'inputs'

    def get_PHA_melt_simulations_dir(self, polymer_names, number_of_polymers):
        """

        Return the simulations directory for a PHA melt.

        This is the parent directory for timestamped simulation runs.

        """
        return self.get_PHA_melt_dir(polymer_names, number_of_polymers) / 'simulations'

    def create_PHA_melt_simulation_run_dir(self, polymer_names, number_of_polymers, timestamp=None):
        """

        Create a timestamped simulation run directory for a PHA melt.

        This should only be called when a simulation is actually started.

        """
        from datetime import datetime
        if timestamp is None:
            timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
        run_dir = self.get_PHA_melt_simulations_dir(polymer_names, number_of_polymers) / timestamp
        run_dir.mkdir(parents=True, exist_ok=False)
        return run_dir

    def create_named_PHA_melt_simulation_run_dir(
            self,
            polymer_names,
            number_of_polymers,
            run_name,
            ):
        """
        Create a numbered simulation run directory.

        Examples
        --------
        run_name="Tg"   -> Tg_01, Tg_02, Tg_03
        run_name="Test" -> Test_01, Test_02, Test_03
        """

        simulations_dir = self.get_PHA_melt_simulations_dir(
            polymer_names,
            number_of_polymers,
            )

        simulations_dir.mkdir(
            parents=True,
            exist_ok=True,
            )

        run_name = run_name.strip().replace(" ", "_")

        counter = 1

        while True:
            candidate_dir = simulations_dir / f"{run_name}_{counter:02d}"

            if not candidate_dir.exists():
                candidate_dir.mkdir(
                    parents=True,
                    exist_ok=False,
                    )
                return candidate_dir

            counter += 1

    def find_file(self, directory, extension):
        """
        Return the first file in a directory with the requested extension.

        Returns None if no matching file is found.
        """
        directory = Path(directory)
        files = list(directory.glob(f'*.{extension}'))
        if len(files) == 0:
            return None
        return files[0]

    def find_files(self, directory, extension):
        """
        Return all files in a directory with the requested extension.
        """
        directory = Path(directory)
        return sorted(directory.glob(f'*.{extension}'))
    
    def get_polymer_smiles_csv(self):

        """
        Return the path to polymer_smiles.csv.
        """
        return self.root_dir / "polymer_smiles.csv"

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


