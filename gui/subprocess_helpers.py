#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Subprocess helpers for the iPHAsimulatorV2 GUI.

The Streamlit GUI runs in a separate, lightweight environment.

Scientific backend operations are executed using the Python interpreter from
the dedicated iPHAsimulator environment. This keeps AmberTools, OpenBabel,
OpenMM, ACPYPE, Polyply, and related scientific dependencies isolated from
the GUI environment.
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Mapping, Sequence

from gui.config import (
    IPHASIMULATOR_PYTHON,
    PROJECT_ROOT,
    STRUCTURE_DATABASE,
)


def validate_iphasimulator_python() -> Path:
    """
    Check that the configured iPHAsimulator Python executable exists.

    Returns
    -------
    pathlib.Path
        Resolved Python executable belonging to the scientific environment.

    Raises
    ------
    FileNotFoundError
        If the configured executable does not exist or is not a file.
    """

    python_path = Path(
        IPHASIMULATOR_PYTHON
    ).expanduser()

    if not python_path.exists():
        raise FileNotFoundError(
            "Could not find the iPHAsimulator Python executable:\n"
            f"{python_path}"
        )

    if not python_path.is_file():
        raise FileNotFoundError(
            "Configured iPHAsimulator Python path is not a file:\n"
            f"{python_path}"
        )

    return python_path.resolve()


def build_iphasimulator_environment() -> dict[str, str]:
    """
    Build environment variables for scientific backend subprocesses.

    The scientific environment's ``bin`` directory is placed first in PATH so
    external commands such as tleap, antechamber, ACPYPE, and Polyply can be
    located by backend Python code.

    Returns
    -------
    dict[str, str]
        Environment dictionary suitable for ``subprocess.run``.
    """

    python_path = validate_iphasimulator_python()
    environment_bin = python_path.parent

    environment = dict(
        os.environ
    )

    existing_path = environment.get(
        "PATH",
        "",
    )

    environment["PATH"] = (
        f"{environment_bin}{os.pathsep}{existing_path}"
        if existing_path
        else str(environment_bin)
    )

    # Helps child processes identify the active scientific environment.
    environment["IPHASIMULATOR_PYTHON"] = str(
        python_path
    )

    return environment


def run_subprocess(
    command: Sequence[str | Path],
    workdir: str | Path = PROJECT_ROOT,
    environment: Mapping[str, str] | None = None,
    timeout: float | None = None,
) -> subprocess.CompletedProcess[str]:
    """
    Run a command and capture its standard output and standard error.

    Parameters
    ----------
    command : sequence of str or pathlib.Path
        Command and arguments.

    workdir : str or pathlib.Path, optional
        Working directory used by the subprocess.

    environment : mapping, optional
        Environment variables. The current process environment is used if
        omitted.

    timeout : float, optional
        Maximum execution time in seconds. No timeout is applied when omitted.

    Returns
    -------
    subprocess.CompletedProcess[str]
        Completed subprocess result.

    Raises
    ------
    ValueError
        If the command is empty.

    FileNotFoundError
        If the working directory does not exist.
    """

    if not command:
        raise ValueError(
            "Subprocess command cannot be empty."
        )

    workdir = Path(
        workdir
    ).expanduser().resolve()

    if not workdir.exists():
        raise FileNotFoundError(
            "Subprocess working directory does not exist:\n"
            f"{workdir}"
        )

    if not workdir.is_dir():
        raise NotADirectoryError(
            "Subprocess working directory is not a directory:\n"
            f"{workdir}"
        )

    command_strings = [
        str(item)
        for item in command
    ]

    return subprocess.run(
        command_strings,
        cwd=workdir,
        env=(
            dict(environment)
            if environment is not None
            else None
        ),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        check=False,
    )


def build_polymer_subprocess(
    sequence: Sequence[str],
) -> subprocess.CompletedProcess[str]:
    """
    Launch ``PHAPolymerBuilder`` in the iPHAsimulator environment.

    Homopolymer sequences are passed to ``build_PHA_polymer``. Sequences
    containing multiple PHA types are passed to ``build_PHA_copolymer``.

    Parameters
    ----------
    sequence : sequence of str
        Ordered monomer sequence.

    Returns
    -------
    subprocess.CompletedProcess[str]
        Build subprocess result.
    """

    sequence = [
        str(unit).strip()
        for unit in sequence
    ]

    if not sequence:
        raise ValueError(
            "Cannot build an empty polymer sequence."
        )

    if any(not unit for unit in sequence):
        raise ValueError(
            "Polymer sequence contains an empty PHA type."
        )

    build_code = r"""
import json
import sys
import traceback

from iphasimulator.build_pha import PHAPolymerBuilder


root_dir = sys.argv[1]
sequence = json.loads(sys.argv[2])

try:
    builder = PHAPolymerBuilder(
        root_dir
    )

    unique_units = []

    for unit in sequence:
        if unit not in unique_units:
            unique_units.append(unit)

    if len(unique_units) == 1:
        PHA_type = unique_units[0]
        length = len(sequence)

        print(
            f"Building homopolymer: "
            f"P{PHA_type}_{length}"
        )

        output = builder.build_PHA_polymer(
            PHA_type=PHA_type,
            length=length,
        )

    else:
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        if len(unique_units) > len(letters):
            raise ValueError(
                "Too many unique monomer types."
            )

        unit_to_letter = {
            unit: letters[index]
            for index, unit in enumerate(
                unique_units
            )
        }

        pattern = "".join(
            unit_to_letter[unit]
            for unit in sequence
        )

        length = len(sequence)

        print("Building copolymer.")
        print("PHA types:", unique_units)
        print("Pattern:", pattern)
        print("Length:", length)

        output = builder.build_PHA_copolymer(
            PHA_types=unique_units,
            pattern=pattern,
            length=length,
        )

    print("\nPOLYMER_BUILD_RESULT")
    print(
        json.dumps(
            output,
            default=str,
            indent=2,
        )
    )

except Exception:
    print(
        "\nPolymer build failed.",
        file=sys.stderr,
    )

    traceback.print_exc(
        file=sys.stderr
    )

    sys.exit(1)
"""

    python_path = validate_iphasimulator_python()

    command = [
        python_path,
        "-c",
        build_code,
        STRUCTURE_DATABASE,
        json.dumps(
            sequence
        ),
    ]

    return run_subprocess(
        command=command,
        workdir=PROJECT_ROOT,
        environment=build_iphasimulator_environment(),
    )


def run_python_script_with_iphasimulator(
    script_path: str | Path,
    arguments: Sequence[str | Path] | None = None,
    workdir: str | Path = PROJECT_ROOT,
    timeout: float | None = None,
) -> subprocess.CompletedProcess[str]:
    """
    Run a Python script using the iPHAsimulator environment.

    Parameters
    ----------
    script_path : str or pathlib.Path
        Python script to execute.

    arguments : sequence of str or pathlib.Path, optional
        Positional arguments supplied to the script.

    workdir : str or pathlib.Path, optional
        Subprocess working directory.

    timeout : float, optional
        Maximum execution time in seconds.

    Returns
    -------
    subprocess.CompletedProcess[str]
        Script execution result.
    """

    script_path = Path(
        script_path
    ).expanduser().resolve()

    if not script_path.exists():
        raise FileNotFoundError(
            "Generated Python script not found:\n"
            f"{script_path}"
        )

    if not script_path.is_file():
        raise FileNotFoundError(
            "Generated Python script path is not a file:\n"
            f"{script_path}"
        )

    if script_path.suffix.lower() != ".py":
        raise ValueError(
            "Expected a Python script ending in '.py':\n"
            f"{script_path}"
        )

    python_path = validate_iphasimulator_python()

    command: list[str | Path] = [
        python_path,
        "-u",
        script_path,
    ]

    if arguments is not None:
        command.extend(
            arguments
        )

    return run_subprocess(
        command=command,
        workdir=workdir,
        environment=build_iphasimulator_environment(),
        timeout=timeout,
    )


def run_python_module_with_iphasimulator(
    module_name: str,
    arguments: Sequence[str | Path] | None = None,
    workdir: str | Path = PROJECT_ROOT,
    timeout: float | None = None,
) -> subprocess.CompletedProcess[str]:
    """
    Run an installed Python module in the iPHAsimulator environment.

    This executes the equivalent of:

        python -m <module_name>

    Parameters
    ----------
    module_name : str
        Importable module name.

    arguments : sequence of str or pathlib.Path, optional
        Arguments supplied after the module name.

    workdir : str or pathlib.Path, optional
        Subprocess working directory.

    timeout : float, optional
        Maximum execution time in seconds.

    Returns
    -------
    subprocess.CompletedProcess[str]
        Module execution result.
    """

    module_name = str(
        module_name
    ).strip()

    if not module_name:
        raise ValueError(
            "module_name cannot be empty."
        )

    python_path = validate_iphasimulator_python()

    command: list[str | Path] = [
        python_path,
        "-u",
        "-m",
        module_name,
    ]

    if arguments is not None:
        command.extend(
            arguments
        )

    return run_subprocess(
        command=command,
        workdir=workdir,
        environment=build_iphasimulator_environment(),
        timeout=timeout,
    )


# ==========================================================
# Temporary backwards-compatibility aliases
# ==========================================================

def validate_ambertools_python() -> Path:
    """
    Deprecated compatibility wrapper.

    Use ``validate_iphasimulator_python`` instead.
    """

    return validate_iphasimulator_python()


def build_ambertools_environment() -> dict[str, str]:
    """
    Deprecated compatibility wrapper.

    Use ``build_iphasimulator_environment`` instead.
    """

    return build_iphasimulator_environment()


def run_python_script_with_ambertools(
    script_path: str | Path,
) -> subprocess.CompletedProcess[str]:
    """
    Deprecated compatibility wrapper.

    Use ``run_python_script_with_iphasimulator`` instead.
    """

    return run_python_script_with_iphasimulator(
        script_path=script_path,
    )