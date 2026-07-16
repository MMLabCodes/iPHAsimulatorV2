#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Interactive MD System Viewer tab for iPHAsimulatorV2.

This tab allows the user to:

- filter registered MD systems by system type
- select a prepared MD system
- resolve its coordinate file through PHAFileManager
- display system metadata
- render PDB or GRO coordinate files interactively
- change molecular representation, colouring and background
"""

from pathlib import Path

import streamlit as st
from stmol import showmol

from gui.models import GUIData
from gui.openmm_helpers import format_atom_count
from gui.styles import (
    render_info_box,
    render_success_box,
    render_warning_box,
)
from gui.viewer_helpers import (
    render_structure,
    resolve_viewer_structure_file,
)


BACKGROUND_COLOURS = {
    "Dark": "#0f172a",
    "White": "#ffffff",
    "Black": "#000000",
    "Light grey": "#e5e7eb",
}


DISPLAY_STYLES = [
    "Ball and stick",
    "Stick",
    "Sphere",
    "Line",
    "Polymer with water lines",
    "Surface",
]


COLOUR_SCHEMES = [
    "Element",
    "Chain",
    "Residue",
    "Spectrum",
]


def _get_filtered_systems(
    md_systems_df,
    system_type,
):
    """
    Filter the MD-system registry by system type.

    Parameters
    ----------
    md_systems_df : pandas.DataFrame
        Registered molecular-dynamics systems.

    system_type : str
        Selected type filter or ``All``.

    Returns
    -------
    pandas.DataFrame
        Filtered system registry.
    """

    if system_type == "All":
        return md_systems_df.copy()

    return md_systems_df[
        md_systems_df["system_type"] == system_type
    ].copy()


def _resolve_selected_system(
    gui_data,
    system_name,
    system_type,
):
    """
    Resolve the registered files and best viewer coordinate file.

    Parameters
    ----------
    gui_data : GUIData
        Shared GUI data.

    system_name : str
        Registered MD-system name.

    system_type : str
        Registered MD-system type.

    Returns
    -------
    tuple
        system_files, structure_file
    """

    system_files = gui_data.paths.get_md_system_files(
        system_name=system_name,
        system_type=system_type,
    )

    structure_file = resolve_viewer_structure_file(
        system_files=system_files,
        system_name=system_name,
    )

    return (
        system_files,
        Path(structure_file),
    )


def render_system_viewer_tab(
    gui_data: GUIData,
) -> None:
    """
    Render the interactive molecular-system viewer.

    Parameters
    ----------
    gui_data : GUIData
        Shared GUI data containing the MD-system registry and filepath
        manager.
    """

    st.markdown(
        "## 🧬 Interactive MD System Viewer"
    )

    render_info_box(
        "Select a registered molecular-dynamics system and inspect its "
        "coordinates interactively. Drag to rotate, scroll to zoom, and "
        "right-drag to translate the structure."
    )

    st.divider()

    md_systems_df = gui_data.md_systems_df

    if md_systems_df.empty:
        render_warning_box(
            "No molecular-dynamics systems are registered in "
            "md_systems.csv. Build and register a system before using "
            "the viewer."
        )

        return

    controls_column, viewer_column = st.columns(
        [
            1,
            2.5,
        ]
    )

    selected_system_name = None
    selected_system_type = None
    selected_system_row = None
    selected_system_files = None
    selected_structure_file = None
    resolution_error = None

    display_style = "Ball and stick"
    colour_scheme = "Element"
    background_choice = "Dark"
    viewer_height = 650

    # ======================================================
    # Viewer controls
    # ======================================================

    with controls_column:
        st.markdown(
            "### Viewer Controls"
        )

        system_types = sorted(
            str(system_type)
            for system_type in (
                md_systems_df["system_type"]
                .dropna()
                .unique()
            )
            if str(system_type).strip()
        )

        selected_type_filter = st.selectbox(
            "System type",
            [
                "All",
                *system_types,
            ],
            key="viewer_system_type_filter",
        )

        filtered_systems_df = _get_filtered_systems(
            md_systems_df=md_systems_df,
            system_type=selected_type_filter,
        )

        if filtered_systems_df.empty:
            st.warning(
                "No registered systems match the selected type."
            )

        else:
            selected_system_name = st.selectbox(
                "MD system",
                filtered_systems_df[
                    "system_name"
                ].tolist(),
                key="viewer_selected_system",
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

            try:
                (
                    selected_system_files,
                    selected_structure_file,
                ) = _resolve_selected_system(
                    gui_data=gui_data,
                    system_name=selected_system_name,
                    system_type=selected_system_type,
                )

            except Exception as error:
                resolution_error = str(error)

            st.divider()

            display_style = st.selectbox(
                "Display style",
                DISPLAY_STYLES,
                key="viewer_display_style",
            )

            colour_scheme = st.selectbox(
                "Colour scheme",
                COLOUR_SCHEMES,
                key="viewer_colour_scheme",
            )

            background_choice = st.selectbox(
                "Background",
                list(
                    BACKGROUND_COLOURS.keys()
                ),
                key="viewer_background_colour",
            )

            viewer_height = st.slider(
                "Viewer height",
                min_value=400,
                max_value=900,
                value=650,
                step=50,
                key="viewer_height",
            )

            # ==================================================
            # System information
            # ==================================================

            st.divider()

            st.markdown(
                "### System Information"
            )

            atom_count = format_atom_count(
                selected_system_row[
                    "number_of_atoms"
                ]
            )

            st.markdown(
                '<div class="card">',
                unsafe_allow_html=True,
            )

            st.write(
                f"**Name:** `{selected_system_name}`"
            )

            st.write(
                f"**Type:** `{selected_system_type}`"
            )

            st.write(
                f"**Atoms:** `{atom_count}`"
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

            if selected_structure_file is not None:
                st.write(
                    "**Viewer structure file:**"
                )

                st.code(
                    str(
                        selected_structure_file
                    )
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True,
            )

            if resolution_error is not None:
                st.error(
                    "The selected system was found in the registry, "
                    "but its structure file could not be resolved."
                )

                st.code(
                    resolution_error
                )

            elif (
                selected_structure_file is not None
                and selected_structure_file.exists()
            ):
                render_success_box(
                    "The structure file was found and is ready to render."
                )

            else:
                render_warning_box(
                    "No usable structure file was found for this system."
                )

    # ======================================================
    # Structure display
    # ======================================================

    with viewer_column:
        st.markdown(
            "### Structure"
        )

        if selected_system_name is None:
            st.info(
                "Select a registered MD system to display."
            )

        elif resolution_error is not None:
            st.error(
                "The selected system cannot currently be displayed."
            )

        elif selected_structure_file is None:
            st.info(
                "No structure file could be resolved for this system."
            )

        elif not selected_structure_file.exists():
            st.error(
                "The selected structure file does not exist."
            )

            st.code(
                str(
                    selected_structure_file
                )
            )

        else:
            try:
                viewer = render_structure(
                    structure_path=(
                        selected_structure_file
                    ),
                    display_style=display_style,
                    colour_scheme=colour_scheme,
                    background_colour=(
                        BACKGROUND_COLOURS[
                            background_choice
                        ]
                    ),
                    width=1000,
                    height=viewer_height,
                )

                showmol(
                    viewer,
                    height=viewer_height,
                    width=1000,
                )

            except Exception as error:
                st.error(
                    "Could not render the selected molecular system."
                )

                st.code(
                    str(error)
                )

        # ==================================================
        # Viewer guidance
        # ==================================================

        st.divider()

        with st.expander(
            "Viewer controls and representation guide"
        ):
            st.markdown(
                """
**Mouse controls**

- Drag with the left mouse button to rotate.
- Scroll to zoom.
- Right-drag to translate the structure.

**Representations**

- **Ball and stick** shows atoms and bonds clearly.
- **Stick** is useful for inspecting polymer connectivity.
- **Sphere** displays a space-filling representation.
- **Line** is faster for large systems.
- **Polymer with water lines** reduces the visual dominance of water.
- **Surface** displays a translucent van der Waals surface.

Large solvated or melt systems may render more smoothly using the
**Line** representation.
"""
            )