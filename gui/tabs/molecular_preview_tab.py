#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Molecular Preview tab for the iPHAsimulatorV2 Streamlit GUI.

This tab displays:

- the currently selected PHA monomer
- the monomer SMILES
- the generated polymer structure
- a concise polymer summary
"""

import streamlit as st

from gui.models import GUIData
from gui.polymer_helpers import (
    draw_monomer,
    draw_polymer,
    generate_polymer_smiles_from_sequence,
    get_polymer_name,
)


def render_molecular_preview_tab(
    gui_data: GUIData,
) -> None:
    """
    Render the molecular preview tab.

    Parameters
    ----------
    gui_data : GUIData
        Shared GUI data containing the monomer SMILES lookup.
    """

    monomer_smiles = gui_data.monomer_smiles
    sequence = st.session_state.sequence

    polymer_name = get_polymer_name(
        sequence
    )

    polymer_smiles = generate_polymer_smiles_from_sequence(
        sequence=sequence,
        smiles_lookup=monomer_smiles,
    )

    monomer_column, polymer_column = st.columns(
        [
            1,
            2,
        ]
    )

    # ======================================================
    # Selected monomer preview
    # ======================================================

    with monomer_column:
        st.markdown(
            "### Selected Monomer"
        )

        selected_pha = (
            st.session_state.preview_PHA
        )

        if selected_pha is None:
            st.info(
                "Click a monomer in the Polymer Builder "
                "tab to preview it."
            )

        elif selected_pha not in monomer_smiles:
            st.error(
                "The selected monomer is not present in "
                "the current residue-code database."
            )

            st.code(
                str(selected_pha)
            )

        else:
            monomer_image = None

            try:
                monomer_image = draw_monomer(
                    pha_type=selected_pha,
                    monomer_smiles=monomer_smiles,
                )

            except Exception as error:
                st.error(
                    f"Could not load {selected_pha}."
                )

                st.code(
                    str(error)
                )

            if monomer_image is None:
                st.warning(
                    f"RDKit could not render {selected_pha}."
                )

            else:
                st.image(
                    monomer_image,
                    use_container_width=True,
                )

                st.markdown(
                    f"### `{selected_pha}`"
                )

                st.markdown(
                    "#### Monomer SMILES"
                )

                st.code(
                    monomer_smiles[
                        selected_pha
                    ]
                )

                st.markdown(
                    '<div class="card">',
                    unsafe_allow_html=True,
                )

                st.write(
                    f"**PHA type:** `{selected_pha}`"
                )

                st.write(
                    "**SMILES length:** "
                    f"`{len(monomer_smiles[selected_pha])}`"
                )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True,
                )

    # ======================================================
    # Generated polymer preview
    # ======================================================

    with polymer_column:
        st.markdown(
            "### Polymer Preview"
        )

        if not sequence:
            st.info(
                "No polymer sequence has been created yet."
            )

            return

        if polymer_smiles is None:
            st.error(
                "The polymer SMILES could not be generated."
            )

            return

        polymer_image = None

        try:
            polymer_image = draw_polymer(
                polymer_smiles=polymer_smiles,
                polymer_name=polymer_name,
            )

        except Exception as error:
            st.error(
                "Could not generate the polymer preview."
            )

            st.code(
                str(error)
            )

        if polymer_image is None:
            st.warning(
                "RDKit could not render the generated "
                "polymer SMILES."
            )

        else:
            st.image(
                polymer_image,
                use_container_width=True,
            )

        # ==================================================
        # Polymer details
        # ==================================================

        st.markdown(
            "### Polymer Summary"
        )

        unique_units = sorted(
            set(sequence)
        )

        polymer_mode = (
            "Homopolymer"
            if len(unique_units) == 1
            else "Copolymer"
        )

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True,
        )

        st.write(
            f"**Name:** `{polymer_name}`"
        )

        st.write(
            f"**Chain length:** `{len(sequence)}`"
        )

        st.write(
            "**Polymer type:** "
            f"`{polymer_mode}`"
        )

        st.write(
            "**Unique monomers:** "
            f"`{', '.join(unique_units)}`"
        )

        st.write(
            "**Number of unique monomers:** "
            f"`{len(unique_units)}`"
        )

        st.write(
            "**SMILES characters:** "
            f"`{len(polymer_smiles)}`"
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

        # ==================================================
        # Ordered sequence
        # ==================================================

        with st.expander(
            "Show ordered polymer sequence"
        ):
            sequence_rows = []

            for position, pha_type in enumerate(
                sequence,
                start=1,
            ):
                sequence_rows.append(
                    {
                        "Position": position,
                        "PHA type": pha_type,
                        "Monomer SMILES": (
                            monomer_smiles.get(
                                pha_type,
                                "",
                            )
                        ),
                    }
                )

            st.dataframe(
                sequence_rows,
                use_container_width=True,
                hide_index=True,
            )

        # ==================================================
        # Generated polymer SMILES
        # ==================================================

        with st.expander(
            "Show generated polymer SMILES"
        ):
            st.code(
                polymer_smiles
            )