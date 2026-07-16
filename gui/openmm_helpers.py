#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OpenMM workflow helpers for the iPHAsimulatorV2 GUI.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

from gui.config import MD_SCRIPT_DIR
from src.iphasimulator.openmmscript_builder import OpenMMScriptBuilder


SUPPORTED_WORKFLOW_METHODS = {
    "minimize_energy",
    "basic_NVT",
    "basic_NPT",
    "anneal_NVT",
    "thermal_ramp",
}


def add_workflow_step(step):
    """
    Add one validated step to the current OpenMM workflow.
    """

    if not isinstance(step, dict):
        raise TypeError(
            "Workflow step must be a dictionary."
        )

    method = step.get(
        "method"
    )

    if method not in SUPPORTED_WORKFLOW_METHODS:
        raise ValueError(
            f"Unsupported workflow method: {method}"
        )

    st.session_state.openmm_steps.append(
        dict(step)
    )


def remove_workflow_step(index):
    """
    Remove a workflow step by index.
    """

    steps = st.session_state.openmm_steps

    if index < 0 or index >= len(steps):
        raise IndexError(
            f"Workflow step index out of range: {index}"
        )

    steps.pop(
        index
    )


def move_workflow_step_up(index):
    """
    Move a workflow step one position earlier.
    """

    steps = st.session_state.openmm_steps

    if index <= 0:
        return

    if index >= len(steps):
        raise IndexError(
            f"Workflow step index out of range: {index}"
        )

    steps[index - 1], steps[index] = (
        steps[index],
        steps[index - 1],
    )


def move_workflow_step_down(index):
    """
    Move a workflow step one position later.
    """

    steps = st.session_state.openmm_steps

    if index < 0:
        raise IndexError(
            f"Workflow step index out of range: {index}"
        )

    if index >= len(steps) - 1:
        return

    steps[index + 1], steps[index] = (
        steps[index],
        steps[index + 1],
    )


def duplicate_workflow_step(index):
    """
    Duplicate a workflow step immediately after its current position.
    """

    steps = st.session_state.openmm_steps

    if index < 0 or index >= len(steps):
        raise IndexError(
            f"Workflow step index out of range: {index}"
        )

    steps.insert(
        index + 1,
        dict(
            steps[index]
        ),
    )


def validate_workflow(
    steps=None,
):
    """
    Validate the current OpenMM workflow.

    The first stage must currently be minimisation.
    """

    if steps is None:
        steps = st.session_state.openmm_steps

    if not steps:
        raise ValueError(
            "No OpenMM workflow steps have been added."
        )

    first_method = steps[0].get(
        "method"
    )

    if first_method != "minimize_energy":
        raise ValueError(
            "The first OpenMM workflow step must be minimization."
        )

    for index, step in enumerate(
        steps,
        start=1,
    ):
        method = step.get(
            "method"
        )

        if method not in SUPPORTED_WORKFLOW_METHODS:
            raise ValueError(
                f"Unsupported method at step {index}: {method}"
            )

    return True


def build_openmm_script_builder(
    system_name,
    system_type,
    run_name,
    steps=None,
):
    """
    Construct OpenMMScriptBuilder from a GUI workflow.
    """

    if steps is None:
        steps = st.session_state.openmm_steps

    validate_workflow(
        steps
    )

    builder = OpenMMScriptBuilder(
        system_name=system_name,
        system_type=system_type,
        run_name=run_name,
    )

    for step in steps:
        method = step["method"]

        if method == "minimize_energy":
            builder.add_minimization()

        elif method == "basic_NVT":
            builder.add_basic_NVT(
                total_steps=step["total_steps"],
                temp=step["temp"],
                filename=step["filename"],
                save_restart=step["save_restart"],
                restart_name=step["restart_name"],
            )

        elif method == "basic_NPT":
            builder.add_basic_NPT(
                total_steps=step["total_steps"],
                temp=step["temp"],
                pressure=step["pressure"],
                filename=step["filename"],
                save_restart=step["save_restart"],
                restart_name=step["restart_name"],
            )

        elif method == "anneal_NVT":
            builder.add_anneal_NVT(
                start_temp=step["start_temp"],
                max_temp=step["max_temp"],
                cycles=step["cycles"],
                quench_rate=step["quench_rate"],
                steps_per_cycle=step["steps_per_cycle"],
                filename=step["filename"],
                save_restart=step["save_restart"],
                restart_name=step["restart_name"],
            )

        elif method == "thermal_ramp":
            builder.add_thermal_ramp(
                heating=step["heating"],
                ensemble=step["ensemble"],
                start_temp=step["start_temp"],
                max_temp=step["max_temp"],
                quench_rate=step["quench_rate"],
                total_steps=step["total_steps"],
                pressure=step["pressure"],
                filename=step["filename"],
                save_restart=step["save_restart"],
                restart_name=step["restart_name"],
            )

    return builder


def workflow_step_label(step):
    """
    Return a concise display label for one workflow step.
    """

    method = step["method"]

    if method == "minimize_energy":
        return "Minimization"

    if method == "basic_NVT":
        return (
            f"Basic NVT · "
            f"{step['temp']} K · "
            f"{step['total_steps']} steps"
        )

    if method == "basic_NPT":
        return (
            f"Basic NPT · "
            f"{step['temp']} K · "
            f"{step['pressure']} atm · "
            f"{step['total_steps']} steps"
        )

    if method == "anneal_NVT":
        return (
            f"Anneal NVT · "
            f"{step['start_temp']}→"
            f"{step['max_temp']} K · "
            f"{step['cycles']} cycles"
        )

    if method == "thermal_ramp":
        direction = (
            "Heat"
            if step["heating"]
            else "Cool"
        )

        return (
            f"{direction} ramp · "
            f"{step['ensemble']} · "
            f"{step['start_temp']}→"
            f"{step['max_temp']} K · "
            f"{step['quench_rate']} K"
        )

    return str(method)


def get_next_md_script_path(
    run_name,
    system_name=None,
):
    """
    Return the next unused generated-script path.
    """

    safe_run_name = (
        str(run_name)
        .strip()
        .replace(" ", "_")
    )

    if not safe_run_name:
        safe_run_name = "OpenMM_Run"

    if system_name:
        safe_system_name = (
            str(system_name)
            .strip()
            .replace(" ", "_")
        )

        script_stem = (
            f"{safe_system_name}_"
            f"{safe_run_name}"
        )

    else:
        script_stem = safe_run_name

    counter = 1

    while True:
        script_path = (
            MD_SCRIPT_DIR
            / f"{script_stem}_{counter:02d}.py"
        )

        if not script_path.exists():
            return script_path

        counter += 1


def format_atom_count(value):
    """
    Format an optional atom count for display.
    """

    if value is None:
        return "Unknown"

    try:
        if pd.isna(value):
            return "Unknown"

        return f"{int(value):,}"

    except (
        TypeError,
        ValueError,
    ):
        return "Unknown"


def infer_input_format(
    topology_file,
    coordinate_file,
):
    """
    Infer Amber or GROMACS from input file extensions.
    """

    topology_suffix = (
        Path(topology_file)
        .suffix
        .lower()
    )

    coordinate_suffix = (
        Path(coordinate_file)
        .suffix
        .lower()
    )

    if (
        topology_suffix == ".top"
        and coordinate_suffix == ".gro"
    ):
        return "GROMACS"

    if (
        topology_suffix == ".prmtop"
        and coordinate_suffix
        in {
            ".rst7",
            ".inpcrd",
        }
    ):
        return "Amber"

    return "Unknown"