#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Streamlit session-state management for the iPHAsimulatorV2 GUI.
"""

from copy import deepcopy

import streamlit as st


SESSION_DEFAULTS = {
    "sequence": [],
    "preview_PHA": None,

    # Current OpenMM workflow
    "openmm_steps": [],
    "openmm_workflow_name": "Test",
    "openmm_run_name": "Test",
    "openmm_loaded_workflow_path": None,

    # Generated OpenMM script
    "generated_openmm_script": None,
    "generated_openmm_script_path": None,
    "generated_openmm_system_name": None,
    "generated_openmm_system_type": None,
    "generated_openmm_workflow_name": None,
}


def initialise_session_state():
    """
    Initialise any missing Streamlit session-state values.
    """

    for key, default_value in SESSION_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = deepcopy(
                default_value
            )

def clear_polymer_sequence():
    """
    Clear the selected polymer sequence and preview.
    """

    st.session_state.sequence = []
    st.session_state.preview_PHA = None


def clear_generated_openmm_script():
    """
    Clear the generated OpenMM script information.
    """

    st.session_state.generated_openmm_script = None
    st.session_state.generated_openmm_script_path = None
    st.session_state.generated_openmm_system_name = None
    st.session_state.generated_openmm_system_type = None
    st.session_state.generated_openmm_workflow_name = None


def clear_openmm_workflow():
    """
    Clear the current OpenMM workflow and generated-script information.
    """

    st.session_state.openmm_steps = []

    st.session_state.openmm_workflow_name = "Test"
    st.session_state.openmm_run_name = "Test"

    st.session_state.openmm_loaded_workflow_path = None

    clear_generated_openmm_script()