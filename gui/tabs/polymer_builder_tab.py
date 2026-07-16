#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Polymer Builder tab for the iPHAsimulatorV2 Streamlit GUI.

This tab allows the user to:

- browse registered PHA monomers
- filter available monomers
- construct an ordered polymer sequence
- remove or clear sequence entries
- repeat the current sequence
- inspect sequence details
- preview the generated polymer name
- preview the generated polymer SMILES
"""

import streamlit as st

from gui.models import GUIData
from gui.polymer_helpers import (
    draw_monomer,
    generate_polymer_smiles_from_sequence,
    get_polymer_name,
    repeat_sequence,
)
from gui.state import clear_polymer_sequence
from gui.styles import render_warning_box

def _render_monomer_card(
    pha_type,
    monomer_smiles,
):
    """
    Render a monomer preview popover and an Add button.

    Parameters
    ----------
    pha_type : str
        Short PHA monomer name, for example ``3HB``.

    monomer_smiles : dict
        Mapping of PHA names to monomer SMILES.
    """

    smiles = monomer_smiles.get(
        pha_type,
        "",
    )

    with st.popover(
        pha_type,
        use_container_width=True,
    ):
        st.markdown(
            f"### {pha_type}"
        )

        try:
            monomer_image = draw_monomer(
                pha_type=pha_type,
                monomer_smiles=monomer_smiles,
            )

        except Exception as error:
            monomer_image = None

            st.error(
                "Could not generate the monomer preview."
            )

            st.code(
                str(error)
            )

        if monomer_image is not None:
            st.image(
                monomer_image,
                use_container_width=True,
            )

        else:
            st.warning(
                "Structure preview unavailable."
            )

        st.markdown(
            "**Monomer SMILES**"
        )

        if smiles:
            st.code(
                smiles
            )

        else:
            st.caption(
                "No SMILES entry is available."
            )

        if st.button(
            f"➕ Add {pha_type}",
            use_container_width=True,
            key=f"popover_add_{pha_type}",
        ):
            st.session_state.sequence.append(
                pha_type
            )

            st.session_state.preview_PHA = (
                pha_type
            )

            st.rerun()

    if st.button(
        "➕ Add",
        use_container_width=True,
        key=f"polymer_builder_add_{pha_type}",
        help=(
            f"Add {pha_type} to the current "
            "polymer sequence."
        ),
    ):
        st.session_state.sequence.append(
            pha_type
        )

        st.session_state.preview_PHA = (
            pha_type
        )

        st.rerun()
    
def render_polymer_builder_tab(
    gui_data: GUIData,
) -> None:
    """
    Render the interactive PHA polymer-builder tab.

    Parameters
    ----------
    gui_data : GUIData
        Shared GUI data containing the available PHA monomers and the
        monomer-SMILES lookup.
    """

    available_phas = gui_data.available_phas
    monomer_smiles = gui_data.monomer_smiles

    sequence = st.session_state.sequence

    polymer_name = get_polymer_name(
        sequence
    )

    polymer_smiles = generate_polymer_smiles_from_sequence(
        sequence=sequence,
        smiles_lookup=monomer_smiles,
    )

    # ======================================================
    # Polymer summary metrics
    # ======================================================

    top_metrics = st.columns(4)

    top_metrics[0].metric(
        "Sequence length",
        len(sequence),
    )

    top_metrics[1].metric(
        "Unique monomers",
        len(set(sequence)),
    )

    if not sequence:
        polymer_mode = "None"

    elif len(set(sequence)) == 1:
        polymer_mode = "Homopolymer"

    else:
        polymer_mode = "Copolymer"

    top_metrics[2].metric(
        "Mode",
        polymer_mode,
    )

    top_metrics[3].metric(
        "Build environment",
        "AmberTools23",
    )

    # ======================================================
    # Available PHA monomers
    # ======================================================

    st.markdown(
        "### Available PHA Monomer Units"
    )

    search = st.text_input(
        "Filter monomers",
        placeholder=(
            "Try 3HB, 4HB, phenyl, fluor..."
        ),
        key="polymer_builder_monomer_search",
    )

    search_text = (
        search
        .strip()
        .lower()
    )

    filtered_phas = [
        pha_type
        for pha_type in available_phas
        if search_text in pha_type.lower()
    ]

    if not filtered_phas:
        st.info(
            "No registered PHA monomers match the current filter."
        )

    else:
        number_of_columns = 6

        monomer_columns = st.columns(
            number_of_columns
        )

        for index, pha_type in enumerate(
            filtered_phas
        ):
            with monomer_columns[
                index % number_of_columns
            ]:
                _render_monomer_card(
                    pha_type=pha_type,
                    monomer_smiles=monomer_smiles,
                )

    # ======================================================
    # Current sequence
    # ======================================================

    st.markdown(
        "### Current Sequence"
    )

    if sequence:
        sequence_chip_html = "".join(
            (
                '<span class="sequence-chip">'
                f"{index + 1}. {unit}"
                "</span>"
            )
            for index, unit
            in enumerate(sequence)
        )

        st.markdown(
            sequence_chip_html,
            unsafe_allow_html=True,
        )

    else:
        render_warning_box(
            "Click the monomer buttons above to begin "
            "building a polymer sequence."
        )

    # ======================================================
    # Sequence controls
    # ======================================================

    control_columns = st.columns(
        [
            1,
            1,
            1,
            2,
        ]
    )

    with control_columns[0]:
        remove_last_clicked = st.button(
            "↩️ Remove last",
            use_container_width=True,
            key="polymer_builder_remove_last",
        )

        if remove_last_clicked:
            if st.session_state.sequence:
                st.session_state.sequence.pop()

                if st.session_state.sequence:
                    st.session_state.preview_PHA = (
                        st.session_state.sequence[-1]
                    )

                else:
                    st.session_state.preview_PHA = None

                st.rerun()

    with control_columns[1]:
        clear_clicked = st.button(
            "🧹 Clear",
            use_container_width=True,
            key="polymer_builder_clear",
        )

        if clear_clicked:
            clear_polymer_sequence()
            st.rerun()

    with control_columns[2]:
        repeat_count = st.number_input(
            "Repeat sequence",
            min_value=1,
            max_value=20,
            value=1,
            step=1,
            key="polymer_builder_repeat_count",
        )

    with control_columns[3]:
        repeat_clicked = st.button(
            "🔁 Apply repeat",
            use_container_width=True,
            key="polymer_builder_apply_repeat",
        )

        if repeat_clicked:
            if not st.session_state.sequence:
                st.warning(
                    "Create a sequence before repeating it."
                )

            else:
                st.session_state.sequence = repeat_sequence(
                    sequence=(
                        st.session_state.sequence
                    ),
                    repetitions=repeat_count,
                )

                st.rerun()

    # ======================================================
    # Sequence details
    # ======================================================

    if sequence:
        with st.expander(
            "Show sequence details"
        ):
            sequence_rows = []

            for index, pha_type in enumerate(
                sequence,
                start=1,
            ):
                sequence_rows.append(
                    {
                        "Position": index,
                        "PHA type": pha_type,
                        "SMILES": monomer_smiles.get(
                            pha_type,
                            "",
                        ),
                    }
                )

            st.dataframe(
                sequence_rows,
                use_container_width=True,
                hide_index=True,
            )

    # ======================================================
    # Generated build target
    # ======================================================

    st.divider()

    if polymer_name is None:
        st.info(
            "A polymer build target will appear once "
            "a sequence has been created."
        )

    else:
        st.markdown(
            "### Generated Build Target"
        )

        st.code(
            polymer_name
        )

    # ======================================================
    # Generated polymer SMILES
    # ======================================================

    if polymer_smiles:
        st.markdown(
            "### Generated Polymer SMILES"
        )

        st.code(
            polymer_smiles
        )

        st.caption(
            "This SMILES is generated from the ordered "
            "monomer sequence selected above."
        )

    # ======================================================
    # Build summary
    # ======================================================

    if sequence:
        st.markdown(
            "### Build Summary"
        )

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True,
        )

        st.write(
            f"**Polymer name:** `{polymer_name}`"
        )

        st.write(
            f"**Chain length:** `{len(sequence)}`"
        )

        st.write(
            "**Unique PHA units:** "
            f"`{len(set(sequence))}`"
        )

        st.write(
            "**Sequence type:** "
            f"`{polymer_mode}`"
        )

        st.write(
            "**Ordered sequence:** "
            f"`{' - '.join(sequence)}`"
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )