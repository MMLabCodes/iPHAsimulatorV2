#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 16:25:33 2026

@author: daniel

Analysis tab for the iPHAsimulatorV2 Streamlit GUI.

This tab currently allows the user to:

- select a registered molecular-dynamics system
- discover available analysis workflows
- select an analysis workflow
- inspect the workflow filepath

Analysis workflows are discovered automatically from:

    src/iphasimulator/analysis/<analysis_name>/workflow.py

Workflow execution will be added later.
"""

from __future__ import annotations

from pathlib import Path
import importlib.util

import streamlit as st

from gui.models import GUIData
from gui.styles import (
    render_info_box,
    render_warning_box,
)


# =============================================================================
# Analysis workflow discovery
# =============================================================================

def get_analysis_root() -> Path:
    """
    Return the src/iphasimulator/analysis directory.
    """

    project_root = (
        Path(__file__)
        .resolve()
        .parents[2]
    )

    analysis_root = (
        project_root
        / "src"
        / "iphasimulator"
        / "analysis"
    )

    return analysis_root


def discover_analysis_workflows() -> dict[str, Path]:
    """
    Discover available analysis workflow.py files.
    """

    analysis_root = (
        get_analysis_root()
    )

    workflows = {}

    if not analysis_root.is_dir():

        return workflows

    for workflow_path in sorted(
        analysis_root.rglob(
            "workflow.py"
        )
    ):

        relative_parent = (
            workflow_path
            .parent
            .relative_to(
                analysis_root
            )
        )

        workflow_name = (
            str(
                relative_parent
            )
            .replace(
                "/",
                "_",
            )
            .replace(
                "\\",
                "_",
            )
        )

        workflows[
            workflow_name
        ] = workflow_path

    return workflows


# =============================================================================
# System selection
# =============================================================================

def _render_system_selection(
    gui_data: GUIData,
):
    """
    Render MD-system selection controls.

    Parameters
    ----------
    gui_data : GUIData
        Shared GUI data.

    Returns
    -------
    tuple
        selected_system_name, selected_system_type
    """

    md_systems_df = (
        gui_data.md_systems_df
    )


    st.markdown(
        "### Registered MD System"
    )


    if md_systems_df.empty:

        render_warning_box(
            "No molecular-dynamics systems are registered yet."
        )

        return (
            None,
            None,
        )


    # -------------------------------------------------------------------------
    # System-type filter
    # -------------------------------------------------------------------------

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
        key="analysis_system_type_filter",
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
            ]
            .copy()
        )


    if filtered_systems_df.empty:

        render_warning_box(
            "No systems match the selected system type."
        )

        return (
            None,
            None,
        )


    # -------------------------------------------------------------------------
    # System selection
    # -------------------------------------------------------------------------

    selected_system_name = st.selectbox(
        "Prepared MD system",
        filtered_systems_df[
            "system_name"
        ].tolist(),
        key="analysis_selected_system",
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


    # -------------------------------------------------------------------------
    # Display selected system
    # -------------------------------------------------------------------------

    st.write(
        f"**System:** `{selected_system_name}`"
    )

    st.write(
        f"**System type:** `{selected_system_type}`"
    )


    try:

        system_files = (
            gui_data.paths.get_md_system_files(
                system_name=(
                    selected_system_name
                ),
                system_type=(
                    selected_system_type
                ),
            )
        )


        system_directory = (
            system_files[
                "system_dir"
            ]
        )


        st.write(
            "**System directory:**"
        )

        st.code(
            str(
                system_directory
            )
        )


    except Exception as error:

        render_warning_box(
            "The selected system is registered, but its "
            "system directory could not be resolved."
        )

        st.code(
            str(error)
        )


    return (
        selected_system_name,
        selected_system_type,
    )


# =============================================================================
# Analysis workflow selection
# =============================================================================

def _render_analysis_workflow_selection():
    """
    Render controls for selecting an available analysis workflow.

    Returns
    -------
    tuple
        selected_workflow_name, selected_workflow_path
    """

    st.markdown(
        "### Analysis Workflow"
    )


    workflows = (
        discover_analysis_workflows()
    )


    if not workflows:

        render_warning_box(
            "No analysis workflows were found beneath "
            "src/iphasimulator/analysis/."
        )

        return (
            None,
            None,
        )


    workflow_names = sorted(
        workflows
    )


    selected_workflow_name = (
        st.selectbox(
            "Available analysis workflow",
            workflow_names,
            key="analysis_selected_workflow",
            format_func=lambda name: (
                name
                .replace(
                    "_",
                    " ",
                )
                .title()
            ),
        )
    )


    selected_workflow_path = (
        workflows[
            selected_workflow_name
        ]
    )


    st.write(
        "**Workflow:**"
    )

    st.code(
        selected_workflow_name
    )


    st.write(
        "**Workflow file:**"
    )

    st.code(
        str(
            selected_workflow_path
        )
    )


    return (
        selected_workflow_name,
        selected_workflow_path,
    )

# =============================================================================
# Workflow loading
# =============================================================================

def load_analysis_workflow_module(
    workflow_path: Path,
):
    """
    Dynamically load an analysis workflow.py module.

    Parameters
    ----------
    workflow_path : pathlib.Path
        Path to the selected workflow.py file.

    Returns
    -------
    module
        Imported Python module.
    """

    workflow_path = (
        Path(workflow_path)
        .expanduser()
        .resolve()
    )


    if not workflow_path.is_file():

        raise FileNotFoundError(
            "Analysis workflow was not found:\n"
            f"{workflow_path}"
        )


    module_name = (
        "iphasimulator_gui_analysis_"
        f"{workflow_path.parent.name}"
    )


    specification = (
        importlib.util.spec_from_file_location(
            module_name,
            workflow_path,
        )
    )


    if (
        specification is None
        or specification.loader is None
    ):

        raise ImportError(
            "Could not construct an import specification for:\n"
            f"{workflow_path}"
        )


    module = (
        importlib.util.module_from_spec(
            specification
        )
    )


    specification.loader.exec_module(
        module
    )


    return module

# =============================================================================
# Simulation selection
# =============================================================================

def _render_simulation_selection(
    gui_data: GUIData,
    selected_system_name,
    selected_system_type,
):
    """
    Render available simulation replicas for the selected MD system.

    Returns
    -------
    str or None
        Selected simulation directory name.
    """

    st.markdown(
        "### Simulation / Replica"
    )


    if (
        selected_system_name is None
        or selected_system_type is None
    ):

        render_info_box(
            "Select a molecular-dynamics system first."
        )

        return None


    try:

        system_files = (
            gui_data.paths.get_md_system_files(
                system_name=(
                    selected_system_name
                ),
                system_type=(
                    selected_system_type
                ),
            )
        )


        simulations_directory = (
            Path(
                system_files[
                    "simulations_dir"
                ]
            )
        )


    except Exception as error:

        render_warning_box(
            "Could not resolve the simulations directory "
            "for the selected system."
        )

        st.code(
            str(error)
        )

        return None


    if not simulations_directory.is_dir():

        render_warning_box(
            "The selected system does not currently have "
            "a simulations directory."
        )

        return None


    simulation_directories = sorted(
        path
        for path in (
            simulations_directory.iterdir()
        )
        if path.is_dir()
    )


    if not simulation_directories:

        render_warning_box(
            "No simulation replicas were found for "
            "the selected system."
        )

        return None


    selected_simulation = (
        st.selectbox(
            "Simulation replica",
            simulation_directories,
            format_func=lambda path: (
                path.name
            ),
            key="analysis_selected_simulation",
        )
    )


    st.write(
        "**Simulation directory:**"
    )

    st.code(
        str(
            selected_simulation
        )
    )


    return (
        selected_simulation.name
    )

# =============================================================================
# Workflow execution
# =============================================================================

def run_selected_analysis_workflow(
    workflow_path,
    selected_system_name,
    selected_simulation_name,
):
    """
    Execute the selected replica-level analysis workflow.

    Currently supported workflow entry point:

        run_tg_analysis(...)
    """

    module = (
        load_analysis_workflow_module(
            workflow_path
        )
    )


    # -------------------------------------------------------------------------
    # Tg analysis
    # -------------------------------------------------------------------------

    if hasattr(
        module,
        "run_tg_analysis",
    ):

        return (
            module.run_tg_analysis(
                system_name=(
                    selected_system_name
                ),
                simulation_name=(
                    selected_simulation_name
                ),
                generate_figures=True,
            )
        )


    # -------------------------------------------------------------------------
    # Unsupported workflow
    # -------------------------------------------------------------------------

    raise AttributeError(
        "The selected workflow does not expose a supported "
        "analysis entry point.\n\n"
        "Expected one of:\n"
        "    run_tg_analysis(...)"
    )

# =============================================================================
# Main tab
# =============================================================================

def render_analysis_tab(
    gui_data: GUIData,
) -> None:
    """
    Render the iPHAsimulator analysis tab.

    The tab allows the user to:

    - select a registered MD system
    - select an available analysis workflow
    - select a simulation replica
    - execute the selected analysis workflow
    - inspect the returned analysis result
    """

    # =========================================================================
    # Header
    # =========================================================================

    st.markdown(
        "## 📊 Analysis"
    )


    render_info_box(
        "Select a registered molecular-dynamics system, "
        "choose an analysis workflow, select a simulation "
        "replica, and run the analysis."
    )


    st.divider()


    # =========================================================================
    # System and workflow selection
    # =========================================================================

    system_column, workflow_column = (
        st.columns(
            [
                1,
                1,
            ]
        )
    )


    # -------------------------------------------------------------------------
    # System selection
    # -------------------------------------------------------------------------

    with system_column:

        (
            selected_system_name,
            selected_system_type,
        ) = (
            _render_system_selection(
                gui_data
            )
        )


    # -------------------------------------------------------------------------
    # Analysis workflow selection
    # -------------------------------------------------------------------------

    with workflow_column:

        (
            selected_workflow_name,
            selected_workflow_path,
        ) = (
            _render_analysis_workflow_selection()
        )


    st.divider()


    # =========================================================================
    # Simulation / replica selection
    # =========================================================================

    selected_simulation_name = (
        _render_simulation_selection(
            gui_data=(
                gui_data
            ),
            selected_system_name=(
                selected_system_name
            ),
            selected_system_type=(
                selected_system_type
            ),
        )
    )


    st.divider()


    # =========================================================================
    # Current analysis selection
    # =========================================================================

    st.markdown(
        "### Current Analysis Selection"
    )


    selection_columns = (
        st.columns(
            [
                1,
                1,
                1,
            ]
        )
    )


    # -------------------------------------------------------------------------
    # Selected system
    # -------------------------------------------------------------------------

    with selection_columns[0]:

        st.write(
            "**System**"
        )

        st.code(
            (
                selected_system_name
                if selected_system_name
                is not None
                else "Not selected"
            )
        )


        st.write(
            "**System type**"
        )

        st.code(
            (
                selected_system_type
                if selected_system_type
                is not None
                else "Not selected"
            )
        )


    # -------------------------------------------------------------------------
    # Selected simulation
    # -------------------------------------------------------------------------

    with selection_columns[1]:

        st.write(
            "**Simulation / Replica**"
        )

        st.code(
            (
                selected_simulation_name
                if selected_simulation_name
                is not None
                else "Not selected"
            )
        )


    # -------------------------------------------------------------------------
    # Selected analysis workflow
    # -------------------------------------------------------------------------

    with selection_columns[2]:

        st.write(
            "**Analysis workflow**"
        )

        st.code(
            (
                selected_workflow_name
                if selected_workflow_name
                is not None
                else "Not selected"
            )
        )


        if (
            selected_workflow_path
            is not None
        ):

            st.write(
                "**Workflow file**"
            )

            st.code(
                str(
                    selected_workflow_path
                )
            )


    st.divider()


    # =========================================================================
    # Run analysis
    # =========================================================================

    st.markdown(
        "### Run Analysis"
    )


    ready_to_run = (
        selected_system_name
        is not None
        and selected_system_type
        is not None
        and selected_simulation_name
        is not None
        and selected_workflow_name
        is not None
        and selected_workflow_path
        is not None
    )


    if not ready_to_run:

        render_info_box(
            "Select a system, simulation replica, "
            "and analysis workflow before running the analysis."
        )


    run_clicked = (
        st.button(
            "▶️ Run analysis",
            use_container_width=True,
            disabled=(
                not ready_to_run
            ),
            key="run_analysis_workflow",
        )
    )


    # =========================================================================
    # Execute selected workflow
    # =========================================================================

    if run_clicked:

        st.info(
            "Running the selected analysis workflow. "
            "This may take some time."
        )


        try:

            with st.spinner(
                "Running analysis workflow..."
            ):

                result = (
                    run_selected_analysis_workflow(
                        workflow_path=(
                            selected_workflow_path
                        ),
                        selected_system_name=(
                            selected_system_name
                        ),
                        selected_simulation_name=(
                            selected_simulation_name
                        ),
                    )
                )


            # =================================================================
            # Successful analysis
            # =================================================================

            st.success(
                "Analysis completed successfully."
            )


            # -----------------------------------------------------------------
            # Display Tg if available
            # -----------------------------------------------------------------

            if isinstance(
                result,
                dict,
            ):

                st.divider()

                st.markdown(
                    "### Analysis Result"
                )


                result_columns = (
                    st.columns(
                        [
                            1,
                            1,
                            1,
                        ]
                    )
                )


                # -------------------------------------------------------------
                # System
                # -------------------------------------------------------------

                with result_columns[0]:

                    st.metric(
                        "System",
                        str(
                            result.get(
                                "system_name",
                                selected_system_name,
                            )
                        ),
                    )


                # -------------------------------------------------------------
                # Replica
                # -------------------------------------------------------------

                with result_columns[1]:

                    st.metric(
                        "Simulation",
                        str(
                            result.get(
                                "simulation_name",
                                selected_simulation_name,
                            )
                        ),
                    )


                # -------------------------------------------------------------
                # Tg
                # -------------------------------------------------------------

                with result_columns[2]:

                    tg_value = (
                        result.get(
                            "tg_K"
                        )
                    )


                    if tg_value is not None:

                        st.metric(
                            "Estimated Tg",
                            f"{float(tg_value):.2f} K",
                        )

                    else:

                        st.metric(
                            "Estimated Tg",
                            "N/A",
                        )


                # -------------------------------------------------------------
                # Output directory
                # -------------------------------------------------------------

                analysis_directory = (
                    result.get(
                        "analysis_directory"
                    )
                )


                if analysis_directory is not None:

                    st.write(
                        "**Analysis output directory:**"
                    )

                    st.code(
                        str(
                            analysis_directory
                        )
                    )


                # -------------------------------------------------------------
                # Full returned result
                # -------------------------------------------------------------

                with st.expander(
                    "Show full analysis result"
                ):

                    st.json(
                        result
                    )


            else:

                st.write(
                    "The workflow completed but did not return "
                    "a dictionary result."
                )

                st.write(
                    result
                )


        # =====================================================================
        # Failed analysis
        # =====================================================================

        except Exception as error:

            st.error(
                "Analysis workflow failed."
            )

            st.code(
                str(
                    error
                )
            )