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
# Main tab
# =============================================================================

def render_analysis_tab(
    gui_data: GUIData,
) -> None:
    """
    Render the iPHAsimulator analysis tab.

    Parameters
    ----------
    gui_data : GUIData
        Shared GUI application data.
    """

    st.markdown(
        "## 📊 Analysis"
    )


    render_info_box(
        "Select a registered molecular-dynamics system and an "
        "available analysis workflow."
    )


    st.divider()


    system_column, workflow_column = (
        st.columns(
            [
                1,
                1,
            ]
        )
    )


    # =========================================================================
    # System
    # =========================================================================

    with system_column:

        (
            selected_system_name,
            selected_system_type,
        ) = (
            _render_system_selection(
                gui_data
            )
        )


    # =========================================================================
    # Workflow
    # =========================================================================

    with workflow_column:

        (
            selected_workflow_name,
            selected_workflow_path,
        ) = (
            _render_analysis_workflow_selection()
        )


    # =========================================================================
    # Current selection
    # =========================================================================

    st.divider()

    st.markdown(
        "### Current Analysis Selection"
    )


    if (
        selected_system_name is None
        or selected_workflow_name is None
    ):

        render_info_box(
            "Select both a molecular-dynamics system "
            "and an analysis workflow."
        )

        return


    selection_columns = (
        st.columns(2)
    )


    with selection_columns[0]:

        st.write(
            "**Selected system**"
        )

        st.code(
            selected_system_name
        )

        st.write(
            "**System type**"
        )

        st.code(
            selected_system_type
        )


    with selection_columns[1]:

        st.write(
            "**Selected analysis**"
        )

        st.code(
            selected_workflow_name
        )

        st.write(
            "**Workflow**"
        )

        st.code(
            str(
                selected_workflow_path
            )
        )


    render_info_box(
        "Workflow execution controls will be added next."
    )