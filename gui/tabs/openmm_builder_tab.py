#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OpenMM Workflow Builder tab for the iPHAsimulatorV2 Streamlit GUI.

This tab allows the user to:

- select any registered MD system
- validate the system topology and coordinate files
- construct an ordered OpenMM workflow
- reorder, duplicate, and remove workflow steps
- generate an OpenMM Python script
- preview the generated script
- run the generated script in the iPHAsimulator environment
- submit the generated script to a Slurm cluster
"""

from pathlib import Path

import streamlit as st

from gui.config import MD_SCRIPT_DIR
from gui.models import GUIData
from gui.openmm_helpers import (
    add_workflow_step,
    build_openmm_script_builder,
    duplicate_workflow_step,
    format_atom_count,
    get_next_md_script_path,
    infer_input_format,
    move_workflow_step_down,
    move_workflow_step_up,
    remove_workflow_step,
    validate_workflow,
    workflow_step_label,
)
from gui.state import clear_openmm_workflow
from gui.styles import (
    render_error_box,
    render_info_box,
    render_success_box,
    render_warning_box,
)
from gui.subprocess_helpers import (
    run_python_script_with_iphasimulator,
    submit_openmm_slurm_job,
)


def _render_system_selection(
    gui_data: GUIData,
):
    """
    Render the registered MD-system selection controls.

    Parameters
    ----------
    gui_data : GUIData
        Shared GUI data containing the MD-system registry and filepath
        manager.

    Returns
    -------
    tuple
        selected_system_name, selected_system_type, selected_system_files
    """

    md_systems_df = gui_data.md_systems_df

    st.markdown(
        "### Registered MD System"
    )

    if md_systems_df.empty:
        render_warning_box(
            "No molecular-dynamics systems are registered yet. "
            "Build and register a dry, solvated, ionised, or melt system first."
        )

        return (
            None,
            None,
            None,
        )

    available_system_types = sorted(
        str(system_type)
        for system_type in (
            md_systems_df[
                "system_type"
            ]
            .dropna()
            .unique()
        )
        if str(system_type).strip()
    )

    type_filter = st.selectbox(
        "System type filter",
        [
            "All",
            *available_system_types,
        ],
        key="openmm_system_type_filter",
    )

    if type_filter == "All":
        filtered_systems_df = (
            md_systems_df.copy()
        )

    else:
        filtered_systems_df = (
            md_systems_df[
                md_systems_df[
                    "system_type"
                ]
                == type_filter
            ].copy()
        )

    if filtered_systems_df.empty:
        st.warning(
            "No systems match the selected type."
        )

        return (
            None,
            None,
            None,
        )

    selected_system_name = st.selectbox(
        "Prepared MD system",
        filtered_systems_df[
            "system_name"
        ].tolist(),
        key="openmm_selected_system",
    )

    selected_system_row = (
        filtered_systems_df[
            filtered_systems_df[
                "system_name"
            ]
            == selected_system_name
        ]
        .iloc[0]
    )

    selected_system_type = str(
        selected_system_row[
            "system_type"
        ]
    )

    selected_system_files = None
    files_valid = False
    validation_error = None

    try:
        selected_system_files = (
            gui_data.paths.validate_md_system_files(
                system_name=selected_system_name,
                system_type=selected_system_type,
            )
        )

        files_valid = True

    except Exception as error:
        validation_error = str(error)

        try:
            selected_system_files = (
                gui_data.paths.get_md_system_files(
                    system_name=selected_system_name,
                    system_type=selected_system_type,
                )
            )

        except Exception as resolution_error:
            selected_system_files = None

            validation_error = (
                f"{validation_error}\n\n"
                f"{resolution_error}"
            )

    atom_count = format_atom_count(
        selected_system_row[
            "number_of_atoms"
        ]
    )

    if selected_system_files is not None:
        input_format = infer_input_format(
            topology_file=(
                selected_system_files[
                    "topology_file"
                ]
            ),
            coordinate_file=(
                selected_system_files[
                    "coordinate_file"
                ]
            ),
        )

    else:
        input_format = "Unknown"

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True,
    )

    st.markdown(
        (
            '<span class="system-chip">'
            f"{selected_system_name}"
            "</span>"
        ),
        unsafe_allow_html=True,
    )

    st.write(
        f"**System type:** `{selected_system_type}`"
    )

    st.write(
        f"**Number of atoms:** `{atom_count}`"
    )

    st.write(
        f"**Input format:** `{input_format}`"
    )

    if selected_system_files is not None:
        st.write(
            "**System directory:**"
        )

        st.code(
            str(
                selected_system_files[
                    "system_dir"
                ]
            )
        )

        st.write(
            "**Topology file:**"
        )

        st.code(
            str(
                selected_system_files[
                    "topology_file"
                ]
            )
        )

        st.write(
            "**Coordinate file:**"
        )

        st.code(
            str(
                selected_system_files[
                    "coordinate_file"
                ]
            )
        )

        if "simulations_dir" in selected_system_files:
            st.write(
                "**Simulations directory:**"
            )

            st.code(
                str(
                    selected_system_files[
                        "simulations_dir"
                    ]
                )
            )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )

    if files_valid:
        render_success_box(
            "The required topology and coordinate files were found."
        )

    else:
        render_error_box(
            "The registry entry exists, but one or more required "
            "files are missing."
        )

        if validation_error:
            st.code(
                validation_error
            )

    return (
        selected_system_name,
        selected_system_type,
        selected_system_files,
    )


def _render_minimization_controls():
    """
    Render energy-minimisation controls.
    """

    st.caption(
        "No additional parameters are required for energy minimisation."
    )

    if st.button(
        "➕ Add minimization",
        use_container_width=True,
        key="add_minimization_step",
    ):
        add_workflow_step(
            {
                "method": "minimize_energy",
            }
        )

        st.rerun()


def _render_basic_nvt_controls():
    """
    Render Basic NVT controls.
    """

    total_steps = st.number_input(
        "Total steps",
        min_value=1,
        value=3000,
        step=1000,
        key="add_nvt_steps",
    )

    temperature = st.number_input(
        "Temperature / K",
        min_value=0.0,
        value=300.0,
        step=10.0,
        key="add_nvt_temperature",
    )

    filename = st.text_input(
        "Filename label",
        value="NVT",
        key="add_nvt_filename",
    )

    save_restart = st.checkbox(
        "Save restart",
        value=False,
        key="add_nvt_save_restart",
    )

    restart_name = st.text_input(
        "Restart name",
        value="",
        key="add_nvt_restart_name",
        disabled=not save_restart,
    )

    if st.button(
        "➕ Add Basic NVT",
        use_container_width=True,
        key="add_basic_nvt_step",
    ):
        add_workflow_step(
            {
                "method": "basic_NVT",
                "total_steps": int(
                    total_steps
                ),
                "temp": float(
                    temperature
                ),
                "filename": filename,
                "save_restart": bool(
                    save_restart
                ),
                "restart_name": (
                    restart_name.strip()
                    or None
                ),
            }
        )

        st.rerun()


def _render_basic_npt_controls():
    """
    Render Basic NPT controls.
    """

    total_steps = st.number_input(
        "Total steps",
        min_value=1,
        value=3000,
        step=1000,
        key="add_npt_steps",
    )

    temperature = st.number_input(
        "Temperature / K",
        min_value=0.0,
        value=300.0,
        step=10.0,
        key="add_npt_temperature",
    )

    pressure = st.number_input(
        "Pressure / atm",
        min_value=0.0,
        value=1.0,
        step=0.1,
        key="add_npt_pressure",
    )

    filename = st.text_input(
        "Filename label",
        value="NPT",
        key="add_npt_filename",
    )

    save_restart = st.checkbox(
        "Save restart",
        value=False,
        key="add_npt_save_restart",
    )

    restart_name = st.text_input(
        "Restart name",
        value="",
        key="add_npt_restart_name",
        disabled=not save_restart,
    )

    if st.button(
        "➕ Add Basic NPT",
        use_container_width=True,
        key="add_basic_npt_step",
    ):
        add_workflow_step(
            {
                "method": "basic_NPT",
                "total_steps": int(
                    total_steps
                ),
                "temp": float(
                    temperature
                ),
                "pressure": float(
                    pressure
                ),
                "filename": filename,
                "save_restart": bool(
                    save_restart
                ),
                "restart_name": (
                    restart_name.strip()
                    or None
                ),
            }
        )

        st.rerun()


def _render_anneal_nvt_controls():
    """
    Render Anneal NVT controls.
    """

    start_temperature = st.number_input(
        "Start temperature / K",
        min_value=0.0,
        value=300.0,
        step=10.0,
        key="add_anneal_start_temperature",
    )

    maximum_temperature = st.number_input(
        "Maximum temperature / K",
        min_value=0.0,
        value=700.0,
        step=10.0,
        key="add_anneal_maximum_temperature",
    )

    cycles = st.number_input(
        "Cycles",
        min_value=1,
        value=5,
        step=1,
        key="add_anneal_cycles",
    )

    quench_rate = st.number_input(
        "Temperature increment / K",
        min_value=1.0,
        value=10.0,
        step=1.0,
        key="add_anneal_quench_rate",
    )

    steps_per_cycle = st.number_input(
        "Steps per cycle",
        min_value=1,
        value=500000,
        step=10000,
        key="add_anneal_steps_per_cycle",
    )

    filename = st.text_input(
        "Filename label",
        value="anneal_NVT",
        key="add_anneal_filename",
    )

    save_restart = st.checkbox(
        "Save restart",
        value=False,
        key="add_anneal_save_restart",
    )

    restart_name = st.text_input(
        "Restart name",
        value="",
        key="add_anneal_restart_name",
        disabled=not save_restart,
    )

    if st.button(
        "➕ Add Anneal NVT",
        use_container_width=True,
        key="add_anneal_nvt_step",
    ):
        if maximum_temperature <= start_temperature:
            st.error(
                "Maximum temperature must be greater than "
                "the start temperature."
            )

            return

        add_workflow_step(
            {
                "method": "anneal_NVT",
                "start_temp": float(
                    start_temperature
                ),
                "max_temp": float(
                    maximum_temperature
                ),
                "cycles": int(
                    cycles
                ),
                "quench_rate": float(
                    quench_rate
                ),
                "steps_per_cycle": int(
                    steps_per_cycle
                ),
                "filename": filename,
                "save_restart": bool(
                    save_restart
                ),
                "restart_name": (
                    restart_name.strip()
                    or None
                ),
            }
        )

        st.rerun()


def _render_thermal_ramp_controls():
    """
    Render thermal-ramp controls.
    """

    direction = st.radio(
        "Ramp direction",
        [
            "Heating",
            "Cooling",
        ],
        horizontal=True,
        key="add_ramp_direction",
    )

    heating = (
        direction == "Heating"
    )

    ensemble = st.selectbox(
        "Ensemble",
        [
            "NVT",
            "NPT",
        ],
        key="add_ramp_ensemble",
    )

    default_start_temperature = (
        300.0
        if heating
        else 700.0
    )

    default_target_temperature = (
        700.0
        if heating
        else 140.0
    )

    start_temperature = st.number_input(
        "Start temperature / K",
        min_value=0.0,
        value=default_start_temperature,
        step=10.0,
        key="add_ramp_start_temperature",
    )

    target_temperature = st.number_input(
        "Target temperature / K",
        min_value=0.0,
        value=default_target_temperature,
        step=10.0,
        key="add_ramp_target_temperature",
    )

    temperature_increment = st.number_input(
        "Temperature increment / K",
        min_value=1.0,
        value=10.0,
        step=1.0,
        key="add_ramp_temperature_increment",
    )

    total_steps = st.number_input(
        "Total steps",
        min_value=1,
        value=100000,
        step=10000,
        key="add_ramp_total_steps",
    )

    pressure = st.number_input(
        "Pressure / atm",
        min_value=0.0,
        value=1.0,
        step=0.1,
        key="add_ramp_pressure",
        disabled=(
            ensemble != "NPT"
        ),
    )

    filename = st.text_input(
        "Filename label",
        value="thermal_ramp",
        key="add_ramp_filename",
    )

    save_restart = st.checkbox(
        "Save restart",
        value=False,
        key="add_ramp_save_restart",
    )

    restart_name = st.text_input(
        "Restart name",
        value="",
        key="add_ramp_restart_name",
        disabled=not save_restart,
    )

    if st.button(
        "➕ Add Thermal Ramp",
        use_container_width=True,
        key="add_thermal_ramp_step",
    ):
        if (
            heating
            and target_temperature
            <= start_temperature
        ):
            st.error(
                "For heating, the target temperature must be "
                "greater than the start temperature."
            )

            return

        if (
            not heating
            and target_temperature
            >= start_temperature
        ):
            st.error(
                "For cooling, the target temperature must be "
                "lower than the start temperature."
            )

            return

        add_workflow_step(
            {
                "method": "thermal_ramp",
                "heating": bool(
                    heating
                ),
                "ensemble": ensemble,
                "start_temp": float(
                    start_temperature
                ),
                "max_temp": float(
                    target_temperature
                ),
                "quench_rate": float(
                    temperature_increment
                ),
                "total_steps": int(
                    total_steps
                ),
                "pressure": float(
                    pressure
                ),
                "filename": filename,
                "save_restart": bool(
                    save_restart
                ),
                "restart_name": (
                    restart_name.strip()
                    or None
                ),
            }
        )

        st.rerun()


def _render_step_creation_controls():
    """
    Render controls for adding one OpenMM workflow step.
    """

    st.markdown(
        "### Add Workflow Step"
    )

    step_type = st.selectbox(
        "Step type",
        [
            "minimize_energy",
            "basic_NVT",
            "basic_NPT",
            "anneal_NVT",
            "thermal_ramp",
        ],
        key="openmm_step_type",
    )

    if step_type == "minimize_energy":
        _render_minimization_controls()

    elif step_type == "basic_NVT":
        _render_basic_nvt_controls()

    elif step_type == "basic_NPT":
        _render_basic_npt_controls()

    elif step_type == "anneal_NVT":
        _render_anneal_nvt_controls()

    elif step_type == "thermal_ramp":
        _render_thermal_ramp_controls()


def _render_current_workflow():
    """
    Render the ordered OpenMM workflow and editing controls.
    """

    steps = st.session_state.openmm_steps

    st.markdown(
        "### Current OpenMM Workflow"
    )

    if steps:
        workflow_chip_html = "".join(
            (
                '<span class="workflow-chip">'
                f"{index + 1}. "
                f"{workflow_step_label(step)}"
                "</span>"
            )
            for index, step in enumerate(
                steps
            )
        )

        st.markdown(
            workflow_chip_html,
            unsafe_allow_html=True,
        )

    else:
        render_warning_box(
            "No OpenMM workflow steps have been added. "
            "Start with minimization."
        )

    st.divider()

    for index, step in enumerate(
        steps
    ):
        with st.expander(
            (
                f"Step {index + 1}: "
                f"{workflow_step_label(step)}"
            ),
            expanded=True,
        ):
            st.json(
                step
            )

            action_columns = st.columns(4)

            with action_columns[0]:
                if st.button(
                    "⬆️ Up",
                    key=f"openmm_up_{index}",
                    use_container_width=True,
                    disabled=(
                        index == 0
                    ),
                ):
                    move_workflow_step_up(
                        index
                    )

                    st.rerun()

            with action_columns[1]:
                if st.button(
                    "⬇️ Down",
                    key=f"openmm_down_{index}",
                    use_container_width=True,
                    disabled=(
                        index
                        == len(steps) - 1
                    ),
                ):
                    move_workflow_step_down(
                        index
                    )

                    st.rerun()

            with action_columns[2]:
                if st.button(
                    "🗑 Remove",
                    key=f"openmm_remove_{index}",
                    use_container_width=True,
                ):
                    remove_workflow_step(
                        index
                    )

                    st.rerun()

            with action_columns[3]:
                if st.button(
                    "📋 Duplicate",
                    key=f"openmm_duplicate_{index}",
                    use_container_width=True,
                ):
                    duplicate_workflow_step(
                        index
                    )

                    st.rerun()


def _generate_openmm_script(
    gui_data,
    selected_system_name,
    selected_system_type,
    run_name,
):
    """
    Validate the workflow and generate an OpenMM script.

    Returns
    -------
    tuple
        output_script, script_text
    """

    if selected_system_name is None:
        raise ValueError(
            "No registered MD system has been selected."
        )

    if selected_system_type is None:
        raise ValueError(
            "The selected system does not have a valid system type."
        )

    if not str(run_name).strip():
        raise ValueError(
            "run_name cannot be empty."
        )

    gui_data.paths.validate_md_system_files(
        system_name=selected_system_name,
        system_type=selected_system_type,
    )

    validate_workflow()

    script_builder = build_openmm_script_builder(
        system_name=selected_system_name,
        system_type=selected_system_type,
        run_name=run_name,
    )

    output_script = get_next_md_script_path(
        run_name=run_name,
        system_name=selected_system_name,
    )

    script_text = script_builder.to_script()

    output_script = script_builder.write_script(
        output_script
    )

    return (
        output_script,
        script_text,
    )


def _render_generated_script_preview():
    """
    Render the currently generated script and metadata.
    """

    generated_script = (
        st.session_state
        .generated_openmm_script
    )

    if generated_script is None:
        return

    st.markdown(
        "### Generated Script Preview"
    )

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True,
    )

    st.write(
        "**System:** "
        f"`{st.session_state.generated_openmm_system_name}`"
    )

    st.write(
        "**System type:** "
        f"`{st.session_state.generated_openmm_system_type}`"
    )

    st.write(
        "**Script path:**"
    )

    st.code(
        str(
            st.session_state
            .generated_openmm_script_path
        )
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )

    st.code(
        generated_script,
        language="python",
    )


def _run_generated_script():
    """
    Run the currently generated OpenMM script.
    """

    generated_path = (
        st.session_state
        .generated_openmm_script_path
    )

    if generated_path is None:
        st.error(
            "Generate a script before trying to run it."
        )

        return

    script_path = Path(
        generated_path
    )

    if not script_path.exists():
        st.error(
            "The generated script does not exist."
        )

        st.code(
            str(script_path)
        )

        return

    st.info(
        "Running the generated OpenMM script with AmberTools23..."
    )

    st.write(
        "Generated for system:"
    )

    st.code(
        str(
            st.session_state
            .generated_openmm_system_name
        )
    )

    progress = st.progress(0)
    status = st.empty()
    result = None

    with st.spinner(
        "Running OpenMM script..."
    ):
        try:
            status.write(
                "Launching generated script..."
            )

            progress.progress(20)

            result = (
                run_python_script_with_ambertools(
                    script_path
                )
            )

            progress.progress(90)

            status.write(
                "Script finished."
            )

        except Exception as error:
            progress.progress(100)

            st.error(
                "Could not run the generated OpenMM script."
            )

            st.code(
                str(error)
            )

    if result is None:
        return

    progress.progress(100)

    if result.returncode == 0:
        st.success(
            "Generated OpenMM script finished successfully."
        )

        st.balloons()

    else:
        st.error(
            "Generated OpenMM script failed."
        )

    result_columns = st.columns(3)

    result_columns[0].metric(
        "Return code",
        result.returncode,
    )

    result_columns[1].metric(
        "STDOUT characters",
        len(
            result.stdout or ""
        ),
    )

    result_columns[2].metric(
        "STDERR characters",
        len(
            result.stderr or ""
        ),
    )

    if result.stdout:
        st.subheader(
            "STDOUT"
        )

        st.code(
            result.stdout
        )

    if result.stderr:
        st.subheader(
            (
                "STDERR / warnings"
                if result.returncode == 0
                else "STDERR"
            )
        )

        st.code(
            result.stderr
        )


def _submit_generated_script_to_slurm():
    """
    Submit the currently generated OpenMM script to Slurm.
    """

    generated_path = (
        st.session_state
        .generated_openmm_script_path
    )

    if generated_path is None:
        st.error(
            "Generate a script before trying to submit it."
        )

        return

    script_path = Path(
        generated_path
    ).expanduser().resolve()

    if not script_path.exists():
        st.error(
            "The generated OpenMM script does not exist."
        )

        st.code(
            str(script_path)
        )

        return

    if not script_path.is_file():
        st.error(
            "The generated OpenMM script path is not a file."
        )

        st.code(
            str(script_path)
        )

        return

    st.info(
        "Submitting the generated OpenMM script to Slurm..."
    )

    st.write(
        "**Generated for system:**"
    )

    st.code(
        str(
            st.session_state
            .generated_openmm_system_name
        )
    )

    st.write(
        "**Simulation script:**"
    )

    st.code(
        str(script_path)
    )

    result = None

    with st.spinner(
        "Submitting Slurm job..."
    ):
        try:
            result = submit_openmm_slurm_job(
                script_path
            )

        except Exception as error:
            st.error(
                "The GUI could not submit the Slurm job."
            )

            st.code(
                str(error)
            )

            return

    if result.returncode == 0:
        st.success(
            "The OpenMM job was submitted successfully."
        )

    else:
        st.error(
            "Slurm job submission failed."
        )

    result_columns = st.columns(3)

    result_columns[0].metric(
        "Return code",
        result.returncode,
    )

    result_columns[1].metric(
        "STDOUT characters",
        len(
            result.stdout or ""
        ),
    )

    result_columns[2].metric(
        "STDERR characters",
        len(
            result.stderr or ""
        ),
    )

    if result.stdout:
        st.subheader(
            "Slurm submission output"
        )

        st.code(
            result.stdout,
            language="text",
        )

    if result.stderr:
        st.subheader(
            (
                "Slurm submission warnings"
                if result.returncode == 0
                else "Slurm submission errors"
            )
        )

        st.code(
            result.stderr,
            language="text",
        )

def render_openmm_builder_tab(
    gui_data: GUIData,
) -> None:
    """
    Render the complete OpenMM workflow-builder tab.

    Parameters
    ----------
    gui_data : GUIData
        Shared GUI data containing the MD-system registry and filepath
        manager.
    """

    st.markdown(
        "## ⚛️ OpenMM Simulation Script Builder"
    )

    render_info_box(
        "Select any prepared system registered in md_systems.csv, "
        "construct an ordered OpenMM workflow, generate a Python script, "
        "run it locally in the iPHAsimulator environment, or submit it "
        "to Slurm."
    )

    st.divider()

    settings_column, workflow_column = st.columns(
        [
            1,
            1.4,
        ]
    )

    # ======================================================
    # System selection and step creation
    # ======================================================

    with settings_column:
        (
            selected_system_name,
            selected_system_type,
            selected_system_files,
        ) = _render_system_selection(
            gui_data
        )

        del selected_system_files

        run_name = st.text_input(
            "Run name",
            value="Test",
            help=(
                "Creates numbered simulation directories such as "
                "Test_01, Test_02, Tg_01, or Anneal_01."
            ),
            key="openmm_run_name",
        )

        st.write(
            "Generated scripts will be saved in:"
        )

        st.code(
            str(MD_SCRIPT_DIR)
        )

        st.divider()

        _render_step_creation_controls()

    # ======================================================
    # Workflow and script actions
    # ======================================================

    with workflow_column:
        _render_current_workflow()

        st.divider()

        action_columns = st.columns(4)

        with action_columns[0]:
            if st.button(
                "🧹 Clear workflow",
                use_container_width=True,
                key="clear_openmm_workflow",
            ):
                clear_openmm_workflow()

                st.rerun()

        with action_columns[1]:
            generate_clicked = st.button(
                "📝 Generate script",
                use_container_width=True,
                disabled=(
                    selected_system_name is None
                ),
                key="generate_openmm_script",
            )

        with action_columns[2]:
            run_clicked = st.button(
                "▶️ Run locally",
                use_container_width=True,
                disabled=(
                    st.session_state
                    .generated_openmm_script_path
                    is None
                ),
                key="run_openmm_script",
            )

        with action_columns[3]:
            submit_clicked = st.button(
                "🚀 Submit to Slurm",
                use_container_width=True,
                disabled=(
                    st.session_state
                    .generated_openmm_script_path
                    is None
                ),
                key="submit_openmm_slurm_job",
            )

        if generate_clicked:
            try:
                (
                    output_script,
                    script_text,
                ) = _generate_openmm_script(
                    gui_data=gui_data,
                    selected_system_name=(
                        selected_system_name
                    ),
                    selected_system_type=(
                        selected_system_type
                    ),
                    run_name=run_name,
                )

                st.session_state.generated_openmm_script = (
                    script_text
                )

                st.session_state.generated_openmm_script_path = (
                    str(output_script)
                )

                st.session_state.generated_openmm_system_name = (
                    selected_system_name
                )

                st.session_state.generated_openmm_system_type = (
                    selected_system_type
                )

                st.success(
                    "Generated OpenMM simulation script."
                )

                st.code(
                    str(output_script)
                )

            except Exception as error:
                st.error(
                    "Could not generate the OpenMM script."
                )

                st.code(
                    str(error)
                )

        _render_generated_script_preview()

        if run_clicked:
            _run_generated_script()
            
        
        if submit_clicked:
            _submit_generated_script_to_slurm()