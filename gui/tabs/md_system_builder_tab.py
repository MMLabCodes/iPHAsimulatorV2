"""
GUI tab for constructing molecular dynamics systems.

Supported systems
-----------------
- Dry PHA
- Solvated PHA
- Solvated PHA with ions
- Polymer melt
"""

from __future__ import annotations

import contextlib
import io
from pathlib import Path
from typing import Any

import streamlit as st

from gui.md_system_helpers import (
    build_dry_system,
    build_melt_system,
    build_solvated_ions_system,
    build_solvated_system,
    get_available_built_polymers,
    get_salt_name,
    get_water_model_settings,
)


def _display_build_result(
    result: dict[str, Any],
) -> None:
    """Display a summary of a completed MD-system build."""

    st.success(
        f"Successfully built: {result.get('system_name') or result.get('melt_name')}"
    )

    summary_fields = {
        "System name": (
            result.get("system_name")
            or result.get("melt_name")
        ),
        "System type": result.get("system_type"),
        "Number of atoms": result.get("number_of_atoms"),
        "Output directory": (
            result.get("output_dir")
            or result.get("melt_dir")
        ),
        "Topology": (
            result.get("prmtop")
            or result.get("topology_file")
        ),
        "Coordinates": (
            result.get("rst7")
            or result.get("coordinate_file")
        ),
        "PDB": result.get("pdb"),
        "Input directory": result.get("inputs_dir"),
        "Simulation directory": result.get("simulations_dir"),
        "Ion pairs": result.get("num_ion_pairs"),
    }

    for label, value in summary_fields.items():
        if value is not None:
            st.write(f"**{label}:** `{value}`")


def _run_build(
    build_function,
    **kwargs,
) -> tuple[dict[str, Any], str]:
    """
    Run a backend builder while capturing its console output.
    """

    console_buffer = io.StringIO()

    with contextlib.redirect_stdout(console_buffer):
        result = build_function(**kwargs)

    return result, console_buffer.getvalue()


def render() -> None:
    """Render the MD System Builder tab."""

    st.header("MD System Builder")

    project_root = Path(__file__).resolve().parents[2]
    structure_database = project_root / "structure_database"

    st.write(
        """
Build simulation-ready molecular dynamics systems from previously constructed
PHA polymers.

The completed system is stored in the structure database and registered in
`md_systems.csv`.
"""
    )

    st.caption(
        f"Structure database: {structure_database}"
    )

    polymers = get_available_built_polymers(
        structure_database=structure_database,
    )

    if not polymers:
        st.warning(
            "No complete built polymers were found."
        )
        st.info(
            "Build a polymer before creating an MD system."
        )
        return

    system_type = st.selectbox(
        "MD system type",
        [
            "Dry PHA",
            "Solvated PHA",
            "Solvated PHA with ions",
            "Polymer melt",
        ],
        key="md_system_type",
    )

    st.divider()

    # Values populated by the active build form.
    build_function = None
    build_arguments: dict[str, Any] = {}

    # ============================================================
    # Dry PHA
    # ============================================================

    if system_type == "Dry PHA":
        st.subheader("Dry single-chain PHA")

        polymer_name = st.selectbox(
            "Built polymer",
            polymers,
            key="dry_polymer_name",
        )

        forcefield = st.selectbox(
            "Force field",
            ["gaff2"],
            key="dry_forcefield",
        )

        box_radius = st.number_input(
            "Box radius (Å)",
            value=20.0,
            min_value=5.0,
            step=1.0,
            key="dry_box_radius",
        )

        proposed_name = f"{polymer_name}_dry"

        st.info(
            f"Proposed system name: `{proposed_name}`"
        )

        build_function = build_dry_system

        build_arguments = {
            "structure_database": structure_database,
            "polymer_name": polymer_name,
            "forcefield": forcefield,
            "box_radius": box_radius,
        }

    # ============================================================
    # Solvated PHA
    # ============================================================

    elif system_type == "Solvated PHA":
        st.subheader("Solvated single-chain PHA")

        polymer_name = st.selectbox(
            "Built polymer",
            polymers,
            key="solvated_polymer_name",
        )

        forcefield = st.selectbox(
            "Force field",
            ["gaff2"],
            key="solvated_forcefield",
        )

        water_model = st.selectbox(
            "Water model",
            ["TIP3P"],
            key="solvated_water_model",
        )

        box_radius = st.number_input(
            "Solvent box radius (Å)",
            value=20.0,
            min_value=5.0,
            step=1.0,
            key="solvated_box_radius",
        )

        water_leaprc, water_box = (
            get_water_model_settings(
                water_model
            )
        )

        proposed_name = f"{polymer_name}_solvated"

        st.info(
            f"Proposed system name: `{proposed_name}`"
        )

        build_function = build_solvated_system

        build_arguments = {
            "structure_database": structure_database,
            "polymer_name": polymer_name,
            "forcefield": forcefield,
            "water_leaprc": water_leaprc,
            "water_box": water_box,
            "box_radius": box_radius,
        }

    # ============================================================
    # Solvated PHA with ions
    # ============================================================

    elif system_type == "Solvated PHA with ions":
        st.subheader(
            "Solvated single-chain PHA with ions"
        )

        polymer_name = st.selectbox(
            "Built polymer",
            polymers,
            key="ions_polymer_name",
        )

        forcefield = st.selectbox(
            "Force field",
            ["gaff2"],
            key="ions_forcefield",
        )

        water_model = st.selectbox(
            "Water model",
            ["TIP3P"],
            key="ions_water_model",
        )

        box_radius = st.number_input(
            "Solvent box radius (Å)",
            value=20.0,
            min_value=5.0,
            step=1.0,
            key="ions_box_radius",
        )

        ion_concentration = st.number_input(
            "Ion concentration (M)",
            value=0.15,
            min_value=0.0,
            step=0.05,
            format="%.3f",
            key="ion_concentration",
        )

        column_1, column_2 = st.columns(2)

        with column_1:
            positive_ion = st.selectbox(
                "Positive ion",
                [
                    "K+",
                    "Na+",
                ],
                key="positive_ion",
            )

        with column_2:
            negative_ion = st.selectbox(
                "Negative ion",
                [
                    "Cl-",
                ],
                key="negative_ion",
            )

        water_leaprc, water_box = (
            get_water_model_settings(
                water_model
            )
        )

        salt = get_salt_name(
            positive_ion,
            negative_ion,
        )

        concentration_label = str(
            ion_concentration
        ).replace(".", "_")

        proposed_name = (
            f"{polymer_name}_solvated_"
            f"{salt}_{concentration_label}"
        )

        st.info(
            f"Proposed system name: `{proposed_name}`"
        )

        build_function = build_solvated_ions_system

        build_arguments = {
            "structure_database": structure_database,
            "polymer_name": polymer_name,
            "forcefield": forcefield,
            "water_leaprc": water_leaprc,
            "water_box": water_box,
            "box_radius": box_radius,
            "salt": salt,
            "positive_ion": positive_ion,
            "negative_ion": negative_ion,
            "ion_concentration": ion_concentration,
        }

    # ============================================================
    # Polymer melt
    # ============================================================

    elif system_type == "Polymer melt":
        st.subheader("Amorphous polymer melt")

        st.caption(
            "This first GUI version builds a melt containing one polymer type."
        )

        polymer_name = st.selectbox(
            "Built polymer",
            polymers,
            key="melt_polymer_name",
        )

        number_of_polymers = st.number_input(
            "Number of polymer chains",
            value=25,
            min_value=1,
            step=1,
            key="melt_number_of_polymers",
        )

        density = st.number_input(
            "Target density (kg/m³)",
            value=750.0,
            min_value=100.0,
            step=10.0,
            key="melt_density",
        )

        proposed_name = (
            f"{int(number_of_polymers)}_"
            f"{polymer_name}_melt"
        )

        st.info(
            f"Proposed system name: `{proposed_name}`"
        )

        build_function = build_melt_system

        build_arguments = {
            "structure_database": structure_database,
            "polymer_names": [polymer_name],
            "number_of_polymers": [
                int(number_of_polymers)
            ],
            "density": density,
        }

    # ============================================================
    # Build button
    # ============================================================

    st.divider()

    build_clicked = st.button(
        "Build MD System",
        type="primary",
        use_container_width=True,
        key="build_md_system",
    )

    if build_clicked:
        if build_function is None:
            st.error(
                "No build function was selected."
            )
            return

        try:
            with st.spinner(
                f"Building {system_type}..."
            ):
                result, console_output = _run_build(
                    build_function,
                    **build_arguments,
                )

            st.session_state[
                "last_md_system_build_result"
            ] = result

            st.session_state[
                "last_md_system_build_console"
            ] = console_output

        except Exception as error:
            st.error(
                "The MD system build failed."
            )
            st.exception(error)
            return

    # ============================================================
    # Display latest result
    # ============================================================

    result = st.session_state.get(
        "last_md_system_build_result"
    )

    console_output = st.session_state.get(
        "last_md_system_build_console"
    )

    if result is not None:
        st.divider()
        st.subheader("Build result")
        _display_build_result(result)

    if console_output:
        with st.expander(
            "Build console output",
            expanded=False,
        ):
            st.code(
                console_output,
                language="text",
            )