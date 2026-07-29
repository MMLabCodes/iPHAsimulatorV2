"""
GUI tab for constructing molecular dynamics systems.

Supported systems
-----------------
• Dry PHA
• Solvated PHA
• Solvated PHA with ions
• Polymer melt
"""

from __future__ import annotations
from pathlib import Path

import streamlit as st

from gui.md_system_helpers import get_available_built_polymers


def render():

    st.header("MD System Builder")

    st.write(
        """
Build molecular dynamics systems from previously constructed PHA polymers.

Supported system types include:

- Dry polymer
- Solvated polymer
- Solvated polymer with ions
- Polymer melt
"""
    )

    # ------------------------------------------------------------
    # Polymer selection
    # ------------------------------------------------------------
    project_root = Path(__file__).resolve().parents[2]
    structure_database = project_root / "structure_database"

    polymers = get_available_built_polymers()

    if not polymers:
        st.warning("No built polymers were found.")
        st.info("Please build a polymer first.")
        return

    polymer_name = st.selectbox(
        "Built polymer",
        polymers,
    )

    # ------------------------------------------------------------
    # MD system type
    # ------------------------------------------------------------

    system_type = st.selectbox(
        "MD system type",
        [
            "Dry PHA",
            "Solvated PHA",
            "Solvated PHA with ions",
            "Polymer melt",
        ],
    )

    st.divider()

    # ------------------------------------------------------------
    # Dry polymer
    # ------------------------------------------------------------

    if system_type == "Dry PHA":

        st.subheader("Dry PHA")

        forcefield = st.selectbox(
            "Force field",
            [
                "gaff2",
            ],
        )

        box_radius = st.number_input(
            "Box radius (Å)",
            value=20.0,
            min_value=5.0,
        )

    # ------------------------------------------------------------
    # Solvated polymer
    # ------------------------------------------------------------

    elif system_type == "Solvated PHA":

        st.subheader("Solvated PHA")

        forcefield = st.selectbox(
            "Force field",
            [
                "gaff2",
            ],
        )

        water_model = st.selectbox(
            "Water model",
            [
                "TIP3P",
            ],
        )

        box_radius = st.number_input(
            "Box radius (Å)",
            value=20.0,
            min_value=5.0,
        )

    # ------------------------------------------------------------
    # Solvated polymer + ions
    # ------------------------------------------------------------

    elif system_type == "Solvated PHA with ions":

        st.subheader("Solvated PHA with ions")

        forcefield = st.selectbox(
            "Force field",
            [
                "gaff2",
            ],
        )

        water_model = st.selectbox(
            "Water model",
            [
                "TIP3P",
            ],
        )

        ion_concentration = st.number_input(
            "Ion concentration (M)",
            value=0.15,
            min_value=0.0,
        )

        positive_ion = st.selectbox(
            "Positive ion",
            [
                "K+",
                "Na+",
            ],
        )

        negative_ion = st.selectbox(
            "Negative ion",
            [
                "Cl-",
            ],
        )

        box_radius = st.number_input(
            "Box radius (Å)",
            value=20.0,
            min_value=5.0,
        )

    # ------------------------------------------------------------
    # Polymer melt
    # ------------------------------------------------------------

    elif system_type == "Polymer melt":

        st.subheader("Polymer melt")

        number_of_polymers = st.number_input(
            "Number of polymer chains",
            value=25,
            min_value=1,
        )

        density = st.number_input(
            "Target density (kg/m³)",
            value=750,
            min_value=100,
        )

    st.divider()

    build_clicked = st.button(
        "Build MD System",
        use_container_width=True,
    )

    if build_clicked:
        st.info("MD system building will be connected in the next step.")