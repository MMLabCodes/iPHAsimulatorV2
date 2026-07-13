#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate readable OpenMM workflow scripts for registered MD systems.

The generated scripts can run any supported system type registered in
md_systems.csv, including:

    dry
    solvated
    solvated_ions
    melt

PHAFileManager is responsible for locating the correct topology and
coordinate files for each system type.
"""

from pathlib import Path
import textwrap


class OpenMMScriptBuilder:
    """
    Build OpenMM workflow scripts for iPHAsimulator.

    Parameters
    ----------
    system_name : str
        Name of the registered MD system.

        Examples:

            P3HB_10_dry
            P3HB_10_solvated
            P3HB_10_solvated_KCl_0_15
            25_P3HB_10_melt

    system_type : str
        Registered system type.

        Supported values:

            dry
            solvated
            solvated_ions
            melt

    run_name : str, optional
        Base name used for the numbered simulation directory.

        Examples:

            Test       -> Test_01
            Tg         -> Tg_01
            Annealing  -> Annealing_01
    """

    supported_system_types = {
        "dry",
        "solvated",
        "solvated_ions",
        "melt",
    }

    def __init__(
        self,
        system_name,
        system_type,
        run_name="Test",
    ):
        if not isinstance(system_name, str) or not system_name.strip():
            raise ValueError(
                "system_name must be a non-empty string."
            )

        if system_type not in self.supported_system_types:
            raise ValueError(
                f"Unsupported system type: {system_type}\n"
                f"Supported values: "
                f"{sorted(self.supported_system_types)}"
            )

        if not isinstance(run_name, str) or not run_name.strip():
            raise ValueError(
                "run_name must be a non-empty string."
            )

        self.system_name = system_name.strip()
        self.system_type = system_type
        self.run_name = run_name.strip()
        self.steps = []

    # ======================================================
    # Workflow construction
    # ======================================================

    def add_minimization(self):
        """
        Add an energy-minimisation step.
        """

        self.steps.append(
            {
                "method": "minimize_energy",
            }
        )

    def add_basic_NVT(
        self,
        total_steps=3000,
        temp=300,
        filename="NVT",
        save_restart=False,
        restart_name=None,
    ):
        """
        Add a constant-volume, constant-temperature simulation.
        """

        self.steps.append(
            {
                "method": "basic_NVT",
                "total_steps": total_steps,
                "temp": temp,
                "filename": filename,
                "save_restart": save_restart,
                "restart_name": restart_name,
            }
        )

    def add_basic_NPT(
        self,
        total_steps=3000,
        temp=300,
        pressure=1,
        filename="NPT",
        save_restart=False,
        restart_name=None,
    ):
        """
        Add a constant-pressure, constant-temperature simulation.
        """

        self.steps.append(
            {
                "method": "basic_NPT",
                "total_steps": total_steps,
                "temp": temp,
                "pressure": pressure,
                "filename": filename,
                "save_restart": save_restart,
                "restart_name": restart_name,
            }
        )

    def add_anneal_NVT(
        self,
        start_temp=300,
        max_temp=700,
        cycles=5,
        quench_rate=10,
        steps_per_cycle=500000,
        filename="anneal_NVT",
        save_restart=False,
        restart_name=None,
    ):
        """
        Add an NVT annealing workflow.
        """

        self.steps.append(
            {
                "method": "anneal_NVT",
                "start_temp": start_temp,
                "max_temp": max_temp,
                "cycles": cycles,
                "quench_rate": quench_rate,
                "steps_per_cycle": steps_per_cycle,
                "filename": filename,
                "save_restart": save_restart,
                "restart_name": restart_name,
            }
        )

    def add_thermal_ramp(
        self,
        heating=True,
        ensemble="NPT",
        start_temp=300,
        max_temp=700,
        quench_rate=10,
        total_steps=100000,
        pressure=1,
        filename="thermal_ramp",
        save_restart=False,
        restart_name=None,
    ):
        """
        Add a heating or cooling ramp.
        """

        self.steps.append(
            {
                "method": "thermal_ramp",
                "heating": heating,
                "ensemble": ensemble,
                "start_temp": start_temp,
                "max_temp": max_temp,
                "quench_rate": quench_rate,
                "total_steps": total_steps,
                "pressure": pressure,
                "filename": filename,
                "save_restart": save_restart,
                "restart_name": restart_name,
            }
        )

    # ======================================================
    # Script output
    # ======================================================

    def write_script(self, output_script):
        """
        Write the generated workflow to a Python file.

        Parameters
        ----------
        output_script : str or pathlib.Path
            Destination path for the generated Python script.

        Returns
        -------
        pathlib.Path
            Path to the generated script.
        """

        output_script = Path(output_script)

        output_script.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        script_text = self.to_script()

        with open(
            output_script,
            "w",
            encoding="utf-8",
        ) as file:
            file.write(script_text)

        print(
            "OpenMM script written to:\n"
            f"{output_script}"
        )

        return output_script

    def to_script(self):
        """
        Return the complete generated OpenMM Python script.
        """

        step_code = self._build_steps_code()

        return f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generated OpenMM simulation script.

Generated automatically by OpenMMScriptBuilder.

System name:
    {self.system_name}

System type:
    {self.system_type}

Run name:
    {self.run_name}
"""

from pathlib import Path
import sys


# ==========================================================
# Project paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
STRUCTURE_DATABASE = PROJECT_ROOT / "structure_database"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ==========================================================
# iPHAsimulator imports
# ==========================================================

from src.iphasimulator.pha_filepath_manager import PHAFileManager
from src.iphasimulator.sw_openmm import (
    AmberSimulation,
    GromacsSimulation,
)


if __name__ == "__main__":

    # ======================================================
    # Load the selected MD system
    # ======================================================

    paths = PHAFileManager(
        STRUCTURE_DATABASE
    )

    system_name = {self.system_name!r}
    system_type = {self.system_type!r}
    run_name = {self.run_name!r}

    system_files = paths.get_md_system_files(
        system_name=system_name,
        system_type=system_type,
    )

    system_dir = Path(
        system_files["system_dir"]
    )

    topology_file = Path(
        system_files["topology_file"]
    )

    coordinate_file = Path(
        system_files["coordinate_file"]
    )

    simulations_dir = Path(
        system_files["simulations_dir"]
    )

    run_dir = paths.create_named_md_system_simulation_run_dir(
        system_name=system_name,
        system_type=system_type,
        run_name=run_name,
    )

    print("=" * 80)
    print("OpenMM simulation workflow")
    print("=" * 80)
    print("Project root:           ", PROJECT_ROOT)
    print("Structure database:     ", STRUCTURE_DATABASE)
    print("System name:            ", system_name)
    print("System type:            ", system_type)
    print("System directory:       ", system_dir)
    print("Simulations directory:  ", simulations_dir)
    print("Topology file:          ", topology_file)
    print("Coordinate file:        ", coordinate_file)
    print("OpenMM output directory:", run_dir)
    print("=" * 80)

    if not topology_file.exists():
        raise FileNotFoundError(
            f"Topology file not found:\\n{{topology_file}}"
        )

    if not coordinate_file.exists():
        raise FileNotFoundError(
            f"Coordinate file not found:\\n{{coordinate_file}}"
        )

    # ======================================================
    # Detect Amber or GROMACS input format
    # ======================================================

    topology_suffix = topology_file.suffix.lower()
    coordinate_suffix = coordinate_file.suffix.lower()

    if (
        topology_suffix == ".top"
        and coordinate_suffix == ".gro"
    ):
        simulation_class = GromacsSimulation
        simulation_format = "GROMACS"

    elif (
        topology_suffix == ".prmtop"
        and coordinate_suffix in {{
            ".rst7",
            ".inpcrd",
        }}
    ):
        simulation_class = AmberSimulation
        simulation_format = "Amber"

    else:
        raise ValueError(
            "Could not infer the OpenMM simulation class from "
            "the input file extensions.\\n"
            f"Topology: {{topology_file}}\\n"
            f"Coordinates: {{coordinate_file}}"
        )

    print("Detected input format:", simulation_format)

    # ======================================================
    # Create the OpenMM simulation object
    # ======================================================

    sim = simulation_class(
        paths,
        str(topology_file),
        str(coordinate_file),
        output_dir=str(run_dir),
    )

    print(sim)

    data_files = []

{step_code}

    # ======================================================
    # Workflow complete
    # ======================================================

    print("=" * 80)
    print("Simulation workflow finished.")
    print("Final output directory:", sim.output_dir)
    print("=" * 80)

    if data_files:
        print("State-data files generated:")

        for data_file in data_files:
            print("  ", data_file)

        for data_file in data_files:
            try:
                print(
                    "Generating state-data graph for:",
                    data_file,
                )

                sim.graph_state_data(
                    data_file
                )

            except Exception as error:
                print(
                    "Could not graph state-data file:",
                    data_file,
                )
                print("Reason:", error)

    else:
        print(
            "No state-data files were generated. "
            "This is expected for a minimisation-only workflow."
        )
'''

    # ======================================================
    # Workflow code generation
    # ======================================================

    def _build_steps_code(self):
        """
        Convert configured workflow steps into executable Python code.
        """

        if len(self.steps) == 0:
            return textwrap.indent(
                'print("No simulation steps were added.")',
                "    ",
            )

        lines = []
        has_current_sim = False

        for index, step in enumerate(
            self.steps,
            start=1,
        ):
            method = step["method"]

            lines.append("")
            lines.append("#" * 60)
            lines.append(f"# Step {index}: {method}")
            lines.append("#" * 60)
            lines.append(
                f'print("Running step {index}: {method}")'
            )

            if method == "minimize_energy":
                lines.append(
                    "current_sim = sim.minimize_energy()"
                )

                has_current_sim = True

            else:
                if not has_current_sim:
                    raise ValueError(
                        "The first workflow step must currently "
                        "be minimization."
                    )

                if method == "basic_NVT":
                    lines.extend(
                        self._format_basic_NVT(step)
                    )

                elif method == "basic_NPT":
                    lines.extend(
                        self._format_basic_NPT(step)
                    )

                elif method == "anneal_NVT":
                    lines.extend(
                        self._format_anneal_NVT(step)
                    )

                elif method == "thermal_ramp":
                    lines.extend(
                        self._format_thermal_ramp(step)
                    )

                else:
                    raise ValueError(
                        "Unknown OpenMM workflow method: "
                        f"{method}"
                    )

        return textwrap.indent(
            "\n".join(lines),
            "    ",
        )

    def _format_basic_NVT(self, step):
        """
        Format a basic NVT workflow step.
        """

        return [
            "current_sim, data_file = sim.basic_NVT(",
            "    current_sim,",
            f"    total_steps={step['total_steps']},",
            f"    temp={step['temp']},",
            f"    filename={step['filename']!r},",
            f"    save_restart={step['save_restart']},",
            f"    restart_name={step['restart_name']!r},",
            ")",
            "data_files.append(data_file)",
        ]

    def _format_basic_NPT(self, step):
        """
        Format a basic NPT workflow step.
        """

        return [
            "current_sim, data_file = sim.basic_NPT(",
            "    current_sim,",
            f"    total_steps={step['total_steps']},",
            f"    temp={step['temp']},",
            f"    pressure={step['pressure']},",
            f"    filename={step['filename']!r},",
            f"    save_restart={step['save_restart']},",
            f"    restart_name={step['restart_name']!r},",
            ")",
            "data_files.append(data_file)",
        ]

    def _format_anneal_NVT(self, step):
        """
        Format an NVT annealing workflow step.
        """

        return [
            "current_sim, data_file = sim.anneal_NVT(",
            "    current_sim,",
            f"    start_temp={step['start_temp']},",
            f"    max_temp={step['max_temp']},",
            f"    cycles={step['cycles']},",
            f"    quench_rate={step['quench_rate']},",
            f"    steps_per_cycle={step['steps_per_cycle']},",
            f"    filename={step['filename']!r},",
            f"    save_restart={step['save_restart']},",
            f"    restart_name={step['restart_name']!r},",
            ")",
            "data_files.append(data_file)",
        ]

    def _format_thermal_ramp(self, step):
        """
        Format a heating or cooling ramp workflow step.
        """

        return [
            "current_sim, data_file = sim.thermal_ramp(",
            "    current_sim,",
            f"    heating={step['heating']},",
            f"    ensemble={step['ensemble']!r},",
            f"    start_temp={step['start_temp']},",
            f"    max_temp={step['max_temp']},",
            f"    quench_rate={step['quench_rate']},",
            f"    total_steps={step['total_steps']},",
            f"    pressure={step['pressure']},",
            f"    filename={step['filename']!r},",
            f"    save_restart={step['save_restart']},",
            f"    restart_name={step['restart_name']!r},",
            ")",
            "data_files.append(data_file)",
        ]