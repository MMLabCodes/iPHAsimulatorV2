#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Visual styling for the iPHAsimulatorV2 Streamlit GUI.
"""

import streamlit as st


APP_CSS = """
<style>
.stApp {
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #111827 45%,
        #172554 100%
    );
    color: #e5e7eb;
}

.main-title {
    font-size: 3.2rem;
    font-weight: 900;
    background: linear-gradient(
        90deg,
        #67e8f9,
        #a78bfa,
        #f472b6
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: -0.4rem;
}

.subtitle {
    color: #cbd5e1;
    font-size: 1.1rem;
    margin-bottom: 1.5rem;
}

.card {
    background: rgba(15, 23, 42, 0.78);
    border: 1px solid rgba(148, 163, 184, 0.28);
    border-radius: 22px;
    padding: 1.2rem;
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.25);
}

.sequence-chip {
    display: inline-block;
    padding: 0.35rem 0.7rem;
    margin: 0.2rem;
    border-radius: 999px;
    background: linear-gradient(
        90deg,
        #0891b2,
        #7c3aed
    );
    color: white;
    font-weight: 700;
    font-size: 0.9rem;
}

.workflow-chip {
    display: inline-block;
    padding: 0.4rem 0.8rem;
    margin: 0.25rem;
    border-radius: 999px;
    background: linear-gradient(
        90deg,
        #0f766e,
        #2563eb
    );
    color: white;
    font-weight: 700;
    font-size: 0.9rem;
}

.system-chip {
    display: inline-block;
    padding: 0.4rem 0.8rem;
    margin: 0.25rem;
    border-radius: 999px;
    background: linear-gradient(
        90deg,
        #7c3aed,
        #db2777
    );
    color: white;
    font-weight: 700;
    font-size: 0.9rem;
}

.small-muted {
    color: #94a3b8;
    font-size: 0.9rem;
}

.good-box {
    border-left: 5px solid #22c55e;
    background: rgba(34, 197, 94, 0.12);
    padding: 0.8rem 1rem;
    border-radius: 12px;
}

.warn-box {
    border-left: 5px solid #f59e0b;
    background: rgba(245, 158, 11, 0.12);
    padding: 0.8rem 1rem;
    border-radius: 12px;
}

.info-box {
    border-left: 5px solid #38bdf8;
    background: rgba(56, 189, 248, 0.12);
    padding: 0.8rem 1rem;
    border-radius: 12px;
}

.error-box {
    border-left: 5px solid #ef4444;
    background: rgba(239, 68, 68, 0.12);
    padding: 0.8rem 1rem;
    border-radius: 12px;
}

div.stButton > button {
    border-radius: 999px;
    font-weight: 700;
    border: 1px solid rgba(103, 232, 249, 0.45);
    background: rgba(15, 23, 42, 0.75);
    color: #e0f2fe;
}

div.stButton > button:hover {
    border-color: #f472b6;
    color: white;
    transform: scale(1.02);
}
</style>
"""


def configure_page():
    """
    Configure the Streamlit page.
    """

    st.set_page_config(
        page_title="iPHAsimulatorV2",
        page_icon="🧬",
        layout="wide",
    )


def apply_styles():
    """
    Apply the custom application CSS.
    """

    st.markdown(
        APP_CSS,
        unsafe_allow_html=True,
    )


def render_header():
    """
    Render the application title and subtitle.
    """

    st.markdown(
        '<div class="main-title">🧬 iPHAsimulatorV2</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="subtitle">
Interactive PHA polymer construction, registered MD-system selection,
molecular visualisation, OpenMM workflow design, and script generation.
</div>
""",
        unsafe_allow_html=True,
    )


def render_info_box(message):
    st.markdown(
        f'<div class="info-box">{message}</div>',
        unsafe_allow_html=True,
    )


def render_success_box(message):
    st.markdown(
        f'<div class="good-box">{message}</div>',
        unsafe_allow_html=True,
    )


def render_warning_box(message):
    st.markdown(
        f'<div class="warn-box">{message}</div>',
        unsafe_allow_html=True,
    )


def render_error_box(message):
    st.markdown(
        f'<div class="error-box">{message}</div>',
        unsafe_allow_html=True,
    )