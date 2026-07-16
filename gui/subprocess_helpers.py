#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Subprocess helpers for the iPHAsimulatorV2 GUI.

This module executes backend commands but does not render Streamlit widgets.
"""

from pathlib import Path
import json
import os
import subprocess

from gui.config import (
    AMBERTOOLS_PYTHON,
    PROJECT_ROOT,
    STRUCTURE_DATABASE,
)


def validate_ambertools_python():
    """
    Check that the configured AmberTools Python executable exists.

    Returns
    -------
    pathlib.Path
        Resolved AmberTools Python path.
    """

    python_path = Path(
        AMBERTOOLS_PYTHON
    ).expanduser()

    if not python_path.exists():
        raise FileNotFoundError(
            "Could not find AmberTools Python:\n"
            f"{python_path}"
        )

    if not python_path.is_file():
        raise FileNotFoundError(
            "Configured AmberTools Python is not a file:\n"
            f"{python_path}"
        )

    return python_path.resolve()


def build_ambertools_environment():
    """
    Build the environment variables used for AmberTools subprocesses.

    Returns
    -------
    dict
        Environment dictionary suitable for subprocess.run().
    """

    python_path = validate_ambertools_python()
    ambertools_bin = python_path.parent

    environment = dict(
        os.environ
    )

    environment["PATH"] = (
        f"{ambertools_bin}:"
        f"{environment.get('PATH', '')}"
    )

    return environment


def run_subprocess(
    command,
    workdir=PROJECT_ROOT,
    environment=None,
):
    """
    Run a command and capture its output.

    Parameters
    ----------
    command : list[str]
        Command and arguments.

    workdir : str or pathlib.Path, optional
        Working directory.

    environment : dict, optional
        Environment variables. The current environment is used if omitted.

    Returns
    -------
    subprocess.CompletedProcess
        Completed subprocess result.
    """

    workdir = Path(
        workdir
    ).resolve()

    if not workdir.exists():
        raise FileNotFoundError(
            "Subprocess working directory does not exist:\n"
            f"{workdir}"
        )

    return subprocess.run(
        [
            str(item)
            for item in command
        ],
        cwd=workdir,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def build_polymer_subprocess(sequence):
    """
    Launch PHAPolymerBuilder in the AmberTools environment.

    Parameters
    ----------
    sequence : list[str]
        Ordered monomer sequence.

    Returns
    -------
    subprocess.CompletedProcess
        Build subprocess result.
    """

    if not sequence:
        raise ValueError(
            "Cannot build an empty polymer sequence."
        )

    build_code = r"""
import json
import sys

from src.iphasimulator.build_pha import PHAPolymerBuilder


root_dir = sys.argv[1]
sequence = json.loads(sys.argv[2])

builder = PHAPolymerBuilder(root_dir)

unique_units = []

for unit in sequence:
    if unit not in unique_units:
        unique_units.append(unit)

if len(unique_units) == 1:
    PHA_type = unique_units[0]
    length = len(sequence)

    print(f"Building homopolymer: P{PHA_type}_{length}")

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
        for index, unit in enumerate(unique_units)
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

print("Build complete.")
print(output)
"""

    python_path = validate_ambertools_python()

    command = [
        str(python_path),
        "-c",
        build_code,
        str(STRUCTURE_DATABASE),
        json.dumps(
            list(sequence)
        ),
    ]

    return run_subprocess(
        command=command,
        workdir=PROJECT_ROOT,
        environment=build_ambertools_environment(),
    )


def run_python_script_with_ambertools(
    script_path,
):
    """
    Run a generated Python script with AmberTools Python.

    Parameters
    ----------
    script_path : str or pathlib.Path
        Generated script to execute.

    Returns
    -------
    subprocess.CompletedProcess
        Script execution result.
    """

    script_path = Path(
        script_path
    ).resolve()

    if not script_path.exists():
        raise FileNotFoundError(
            "Generated Python script not found:\n"
            f"{script_path}"
        )

    python_path = validate_ambertools_python()

    command = [
        str(python_path),
        str(script_path),
    ]

    return run_subprocess(
        command=command,
        workdir=PROJECT_ROOT,
        environment=build_ambertools_environment(),
    )