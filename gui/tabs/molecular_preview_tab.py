#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Molecular Preview tab for the iPHAsimulatorV2 Streamlit GUI.

This tab provides:

- a summary of the current polymer
- a 2D RDKit structure preview
- calculated molecular descriptors
- monomer-composition analysis
- polymer-architecture classification
- an ordered sequence diagram
- parameterisation and build-readiness checks
- optional display of an already-built 3D polymer structure
- sequence, SMILES, and image downloads
"""

from collections import Counter
from io import BytesIO
from pathlib import Path

import pandas as pd
import streamlit as st
from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem.rdMolDescriptors import (
    CalcMolFormula,
    CalcNumHBA,
    CalcNumHBD,
    CalcNumHeavyAtoms,
    CalcNumRings,
    CalcNumRotatableBonds,
    CalcTPSA,
)

from gui.models import GUIData
from gui.polymer_helpers import (
    draw_monomer,
    draw_polymer,
    generate_polymer_smiles_from_sequence,
    get_polymer_name,
)


# ==========================================================
# General helpers
# ==========================================================

def _ordered_unique(sequence):
    """
    Return unique sequence entries while preserving their order.
    """

    unique_units = []

    for unit in sequence:
        if unit not in unique_units:
            unique_units.append(unit)

    return unique_units


def _get_polymer_mode(sequence):
    """
    Return a broad polymer classification.
    """

    if not sequence:
        return "No polymer"

    if len(set(sequence)) == 1:
        return "Homopolymer"

    return "Copolymer"


def _is_strictly_alternating(sequence):
    """
    Check whether a two-component sequence is strictly alternating.

    Examples
    --------
    A-B-A-B-A-B
    B-A-B-A-B-A
    """

    unique_units = set(sequence)

    if len(unique_units) != 2:
        return False

    return all(
        sequence[index] != sequence[index - 1]
        for index in range(1, len(sequence))
    )


def _count_blocks(sequence):
    """
    Count contiguous monomer blocks in a sequence.

    Examples
    --------
    A-A-A-B-B -> 2 blocks
    A-B-A-B   -> 4 blocks
    """

    if not sequence:
        return 0

    block_count = 1

    for previous, current in zip(
        sequence,
        sequence[1:],
    ):
        if current != previous:
            block_count += 1

    return block_count


def _classify_polymer_architecture(sequence):
    """
    Infer a simple polymer-architecture description.

    This is a sequence-pattern classification rather than a formal
    statistical assignment.
    """

    if not sequence:
        return "No polymer"

    unique_units = _ordered_unique(sequence)

    if len(unique_units) == 1:
        return "Homopolymer"

    if _is_strictly_alternating(sequence):
        return "Alternating copolymer"

    block_count = _count_blocks(sequence)

    # A small number of relatively long contiguous sections is treated
    # as a block-like sequence.
    if block_count <= len(unique_units) + 1:
        return "Block copolymer"

    # Detect a rough gradient by checking whether the fraction of the
    # first unit decreases from the first half to the second half.
    if len(unique_units) == 2 and len(sequence) >= 6:
        first_unit = sequence[0]
        midpoint = len(sequence) // 2

        first_half = sequence[:midpoint]
        second_half = sequence[midpoint:]

        first_fraction = (
            first_half.count(first_unit)
            / len(first_half)
        )

        second_fraction = (
            second_half.count(first_unit)
            / len(second_half)
        )

        if abs(
            first_fraction
            - second_fraction
        ) >= 0.35:
            return "Gradient-like copolymer"

    return "Mixed/custom copolymer"


def _get_sequence_pattern(sequence):
    """
    Convert the sequence into a concise letter pattern.

    Example
    -------
    ["3HB", "3HB", "4HB", "4HB"] -> AABB
    """

    unique_units = _ordered_unique(sequence)

    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    unit_to_letter = {
        unit: letters[index]
        for index, unit in enumerate(unique_units)
    }

    pattern = "".join(
        unit_to_letter[unit]
        for unit in sequence
    )

    return pattern, unit_to_letter


def _calculate_molecular_properties(polymer_smiles):
    """
    Calculate RDKit descriptors from the generated polymer SMILES.

    Returns
    -------
    dict
        Molecular properties. Values are None when the SMILES cannot
        be interpreted by RDKit.
    """

    empty_properties = {
        "formula": None,
        "molecular_weight": None,
        "heavy_atoms": None,
        "rotatable_bonds": None,
        "rings": None,
        "h_bond_donors": None,
        "h_bond_acceptors": None,
        "tpsa": None,
        "logp": None,
    }

    if not polymer_smiles:
        return empty_properties

    molecule = Chem.MolFromSmiles(
        polymer_smiles
    )

    if molecule is None:
        return empty_properties

    return {
        "formula": CalcMolFormula(
            molecule
        ),
        "molecular_weight": Descriptors.MolWt(
            molecule
        ),
        "heavy_atoms": CalcNumHeavyAtoms(
            molecule
        ),
        "rotatable_bonds": CalcNumRotatableBonds(
            molecule
        ),
        "rings": CalcNumRings(
            molecule
        ),
        "h_bond_donors": CalcNumHBD(
            molecule
        ),
        "h_bond_acceptors": CalcNumHBA(
            molecule
        ),
        "tpsa": CalcTPSA(
            molecule
        ),
        "logp": Descriptors.MolLogP(
            molecule
        ),
    }


def _format_descriptor(
    value,
    decimals=2,
    suffix="",
):
    """
    Format an optional molecular descriptor.
    """

    if value is None:
        return "Unavailable"

    if isinstance(value, int):
        return f"{value}{suffix}"

    return f"{value:.{decimals}f}{suffix}"


# ==========================================================
# Parameterisation checks
# ==========================================================

def _check_monomer_readiness(
    pha_type,
    gui_data,
):
    """
    Check whether the required files exist for a PHA chemistry.
    """

    try:
        parameter_files = (
            gui_data.paths.get_PHA_monomer_unit_files(
                pha_type
            )
        )

    except Exception as error:
        return {
            "PHA_type": pha_type,
            "head": False,
            "mainchain": False,
            "tail": False,
            "frcmod": False,
            "ready": False,
            "error": str(error),
        }

    head_exists = Path(
        parameter_files["head_prepin"]
    ).exists()

    mainchain_exists = Path(
        parameter_files["mainchain_prepin"]
    ).exists()

    tail_exists = Path(
        parameter_files["tail_prepin"]
    ).exists()

    frcmod_exists = Path(
        parameter_files["frcmod"]
    ).exists()

    return {
        "PHA_type": pha_type,
        "head": head_exists,
        "mainchain": mainchain_exists,
        "tail": tail_exists,
        "frcmod": frcmod_exists,
        "ready": all(
            [
                head_exists,
                mainchain_exists,
                tail_exists,
                frcmod_exists,
            ]
        ),
        "error": None,
    }


def _check_polymer_readiness(
    sequence,
    gui_data,
):
    """
    Check build readiness for every unique monomer in the sequence.
    """

    readiness_rows = [
        _check_monomer_readiness(
            pha_type=pha_type,
            gui_data=gui_data,
        )
        for pha_type in _ordered_unique(
            sequence
        )
    ]

    polymer_ready = (
        bool(readiness_rows)
        and all(
            row["ready"]
            for row in readiness_rows
        )
    )

    return polymer_ready, readiness_rows


# ==========================================================
# Optional built-polymer lookup
# ==========================================================

def _find_built_polymer_pdb(
    sequence,
    polymer_name,
    gui_data,
):
    """
    Locate a previously built homopolymer PDB where possible.

    Custom copolymer naming and storage may differ, so this lookup is
    currently restricted to standard homopolymer names.
    """

    if not sequence:
        return None

    if len(set(sequence)) != 1:
        return None

    try:
        amber_files = (
            gui_data.paths.get_built_PHA_amber_files(
                polymer_name
            )
        )

    except Exception:
        return None

    pdb_path = Path(
        amber_files["pdb"]
    )

    if pdb_path.exists():
        return pdb_path

    return None


# ==========================================================
# Download helpers
# ==========================================================

def _image_to_png_bytes(image):
    """
    Convert a PIL image to PNG bytes.
    """

    if image is None:
        return None

    buffer = BytesIO()

    image.save(
        buffer,
        format="PNG",
    )

    return buffer.getvalue()


def _build_sequence_download(sequence):
    """
    Build a simple text representation of the sequence.
    """

    lines = [
        f"{index},{pha_type}"
        for index, pha_type in enumerate(
            sequence,
            start=1,
        )
    ]

    return (
        "position,PHA_type\n"
        + "\n".join(lines)
        + "\n"
    )


# ==========================================================
# UI sections
# ==========================================================

def _render_page_guidance():
    """
    Render concise instructions for the preview page.
    """

    st.markdown(
        "## 🔬 Molecular Preview"
    )

    st.markdown(
        """
<div class="info-box">
Inspect the molecular structure, composition, sequence architecture,
calculated descriptors, and build readiness of the polymer currently
defined in the Polymer Builder.
</div>
""",
        unsafe_allow_html=True,
    )

    with st.expander(
        "📘 How to use this page",
        expanded=False,
    ):
        st.markdown(
            """
1. Create or edit a sequence in the **Polymer Builder** tab.
2. Review the automatically generated polymer summary and composition.
3. Inspect the 2D molecular structure and calculated RDKit descriptors.
4. Check that every selected monomer is fully parameterised.
5. Download the generated SMILES, sequence, or structure image.
6. When the polymer is ready, continue to the **Build Console** tab.

The architecture label is inferred from the selected monomer pattern.
It is intended as a helpful sequence description rather than a formal
experimental classification.
"""
        )


def _render_polymer_summary(
    sequence,
    polymer_name,
    architecture,
    properties,
):
    """
    Render high-level polymer summary metrics.
    """

    unique_units = _ordered_unique(
        sequence
    )

    summary_columns = st.columns(5)

    summary_columns[0].metric(
        "Polymer name",
        polymer_name,
    )

    summary_columns[1].metric(
        "Chain length",
        len(sequence),
    )

    summary_columns[2].metric(
        "Unique units",
        len(unique_units),
    )

    summary_columns[3].metric(
        "Architecture",
        architecture,
    )

    summary_columns[4].metric(
        "Estimated MW",
        _format_descriptor(
            properties["molecular_weight"],
            decimals=1,
            suffix=" g/mol",
        ),
    )


def _render_sequence_architecture(
    sequence,
):
    """
    Render sequence chips and a concise letter pattern.
    """

    st.markdown(
        "### Polymer Architecture"
    )

    pattern, unit_to_letter = (
        _get_sequence_pattern(
            sequence
        )
    )

    architecture = (
        _classify_polymer_architecture(
            sequence
        )
    )

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True,
    )

    st.write(
        f"**Classification:** `{architecture}`"
    )

    st.write(
        f"**Number of contiguous blocks:** "
        f"`{_count_blocks(sequence)}`"
    )

    mapping_text = ", ".join(
        f"{letter} = {unit}"
        for unit, letter
        in unit_to_letter.items()
    )

    st.write(
        f"**Pattern key:** `{mapping_text}`"
    )

    # Avoid producing an enormous unbroken line for very long polymers.
    displayed_pattern = (
        pattern
        if len(pattern) <= 120
        else (
            pattern[:117]
            + "..."
        )
    )

    st.write(
        f"**Letter pattern:** `{displayed_pattern}`"
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )

    chip_html = "".join(
        (
            '<span class="sequence-chip">'
            f"{index + 1}. {unit}"
            "</span>"
        )
        for index, unit
        in enumerate(sequence)
    )

    st.markdown(
        chip_html,
        unsafe_allow_html=True,
    )


def _render_composition(
    sequence,
):
    """
    Render monomer counts and fractions.
    """

    st.markdown(
        "### Monomer Composition"
    )

    counts = Counter(
        sequence
    )

    total_units = len(
        sequence
    )

    composition_rows = []

    for pha_type, count in counts.items():
        fraction = (
            count
            / total_units
        )

        composition_rows.append(
            {
                "PHA type": pha_type,
                "Count": count,
                "Fraction": fraction,
                "Percentage": (
                    100.0
                    * fraction
                ),
            }
        )

        st.write(
            f"**{pha_type} — "
            f"{count} unit(s), "
            f"{100.0 * fraction:.1f}%**"
        )

        st.progress(
            fraction
        )

    composition_df = pd.DataFrame(
        composition_rows
    )

    with st.expander(
        "Show composition table"
    ):
        display_df = composition_df.copy()

        display_df["Fraction"] = (
            display_df["Fraction"]
            .map(
                lambda value: f"{value:.4f}"
            )
        )

        display_df["Percentage"] = (
            display_df["Percentage"]
            .map(
                lambda value: f"{value:.2f}%"
            )
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
        )


def _render_molecular_properties(
    properties,
):
    """
    Render calculated RDKit molecular descriptors.
    """

    st.markdown(
        "### Calculated Molecular Properties"
    )

    property_columns = st.columns(3)

    with property_columns[0]:
        st.write(
            "**Molecular formula**"
        )

        st.code(
            properties["formula"]
            or "Unavailable"
        )

        st.write(
            "**Estimated molecular weight**"
        )

        st.code(
            _format_descriptor(
                properties["molecular_weight"],
                decimals=3,
                suffix=" g mol⁻¹",
            )
        )

        st.write(
            "**Heavy atoms**"
        )

        st.code(
            _format_descriptor(
                properties["heavy_atoms"]
            )
        )

    with property_columns[1]:
        st.write(
            "**Rotatable bonds**"
        )

        st.code(
            _format_descriptor(
                properties["rotatable_bonds"]
            )
        )

        st.write(
            "**Ring count**"
        )

        st.code(
            _format_descriptor(
                properties["rings"]
            )
        )

        st.write(
            "**Topological polar surface area**"
        )

        st.code(
            _format_descriptor(
                properties["tpsa"],
                decimals=2,
                suffix=" Å²",
            )
        )

    with property_columns[2]:
        st.write(
            "**Hydrogen-bond donors**"
        )

        st.code(
            _format_descriptor(
                properties["h_bond_donors"]
            )
        )

        st.write(
            "**Hydrogen-bond acceptors**"
        )

        st.code(
            _format_descriptor(
                properties["h_bond_acceptors"]
            )
        )

        st.write(
            "**Calculated LogP**"
        )

        st.code(
            _format_descriptor(
                properties["logp"],
                decimals=2,
            )
        )

    st.caption(
        "These descriptors are calculated from the generated RDKit "
        "molecule. For large polymers, they should be treated as "
        "structure-derived estimates rather than experimental values."
    )


def _render_build_readiness(
    polymer_ready,
    readiness_rows,
):
    """
    Render per-monomer parameterisation status.
    """

    st.markdown(
        "### Build Readiness"
    )

    if polymer_ready:
        st.success(
            "All monomers in the sequence have the required prepin "
            "and force-field parameter files."
        )

    else:
        st.error(
            "One or more monomers are missing required parameter files."
        )

    readiness_df = pd.DataFrame(
        [
            {
                "PHA type": row["PHA_type"],
                "Head prepin": (
                    "✓"
                    if row["head"]
                    else "✗"
                ),
                "Mainchain prepin": (
                    "✓"
                    if row["mainchain"]
                    else "✗"
                ),
                "Tail prepin": (
                    "✓"
                    if row["tail"]
                    else "✗"
                ),
                "FRCMOD": (
                    "✓"
                    if row["frcmod"]
                    else "✗"
                ),
                "Ready": (
                    "Yes"
                    if row["ready"]
                    else "No"
                ),
            }
            for row in readiness_rows
        ]
    )

    st.dataframe(
        readiness_df,
        use_container_width=True,
        hide_index=True,
    )


def _render_downloads(
    polymer_name,
    polymer_smiles,
    sequence,
    polymer_image,
):
    """
    Render export buttons.
    """

    st.markdown(
        "### Export"
    )

    download_columns = st.columns(3)

    with download_columns[0]:
        st.download_button(
            label="⬇️ Download SMILES",
            data=(
                polymer_smiles
                + "\n"
            ),
            file_name=(
                f"{polymer_name}.smiles"
            ),
            mime="text/plain",
            use_container_width=True,
        )

    with download_columns[1]:
        st.download_button(
            label="⬇️ Download sequence",
            data=_build_sequence_download(
                sequence
            ),
            file_name=(
                f"{polymer_name}_sequence.csv"
            ),
            mime="text/csv",
            use_container_width=True,
        )

    with download_columns[2]:
        image_bytes = _image_to_png_bytes(
            polymer_image
        )

        st.download_button(
            label="⬇️ Download 2D image",
            data=(
                image_bytes
                or b""
            ),
            file_name=(
                f"{polymer_name}_2D.png"
            ),
            mime="image/png",
            use_container_width=True,
            disabled=(
                image_bytes is None
            ),
        )


# ==========================================================
# Main tab
# ==========================================================

def render_molecular_preview_tab(
    gui_data: GUIData,
) -> None:
    """
    Render the enhanced molecular-preview tab.

    Parameters
    ----------
    gui_data : GUIData
        Shared GUI data containing monomer information and the central
        filepath manager.
    """

    _render_page_guidance()

    sequence = list(
        st.session_state.sequence
    )

    if not sequence:
        st.markdown(
            """
<div class="warn-box">
No polymer sequence has been created. Return to the Polymer Builder
tab and add one or more monomer units.
</div>
""",
            unsafe_allow_html=True,
        )

        return

    monomer_smiles = (
        gui_data.monomer_smiles
    )

    polymer_name = get_polymer_name(
        sequence
    )

    polymer_smiles = (
        generate_polymer_smiles_from_sequence(
            sequence=sequence,
            smiles_lookup=monomer_smiles,
        )
    )

    architecture = (
        _classify_polymer_architecture(
            sequence
        )
    )

    properties = (
        _calculate_molecular_properties(
            polymer_smiles
        )
    )

    polymer_ready, readiness_rows = (
        _check_polymer_readiness(
            sequence=sequence,
            gui_data=gui_data,
        )
    )

    # ======================================================
    # Polymer summary
    # ======================================================

    _render_polymer_summary(
        sequence=sequence,
        polymer_name=polymer_name,
        architecture=architecture,
        properties=properties,
    )

    st.divider()

    # ======================================================
    # Structure and composition
    # ======================================================

    structure_column, information_column = (
        st.columns(
            [
                1.6,
                1,
            ]
        )
    )

    polymer_image = None

    with structure_column:
        st.markdown(
            "### 2D Polymer Structure"
        )

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
                "RDKit could not render the generated polymer SMILES."
            )

        else:
            st.image(
                polymer_image,
                use_container_width=True,
            )

        with st.expander(
            "Show generated polymer SMILES"
        ):
            st.code(
                polymer_smiles
            )

    with information_column:
        _render_composition(
            sequence
        )

    st.divider()

    # ======================================================
    # Architecture and descriptors
    # ======================================================

    _render_sequence_architecture(
        sequence
    )

    st.divider()

    _render_molecular_properties(
        properties
    )

    st.divider()

    # ======================================================
    # Build readiness
    # ======================================================

    _render_build_readiness(
        polymer_ready=polymer_ready,
        readiness_rows=readiness_rows,
    )

    st.divider()

    # ======================================================
    # Existing built structure
    # ======================================================

    built_pdb = (
        _find_built_polymer_pdb(
            sequence=sequence,
            polymer_name=polymer_name,
            gui_data=gui_data,
        )
    )

    st.markdown(
        "### Built 3D Structure"
    )

    if built_pdb is None:
        st.info(
            "No matching built homopolymer PDB was found. "
            "Use the Build Console to generate the polymer structure."
        )

    else:
        st.success(
            "A previously built polymer PDB was found."
        )

        st.code(
            str(built_pdb)
        )

        st.caption(
            "The complete interactive 3D system can also be inspected "
            "in the MD System Viewer after an MD system has been prepared."
        )

    st.divider()

    # ======================================================
    # Downloads and next step
    # ======================================================

    _render_downloads(
        polymer_name=polymer_name,
        polymer_smiles=polymer_smiles,
        sequence=sequence,
        polymer_image=polymer_image,
    )

    st.markdown(
        "### Next Step"
    )

    if polymer_ready:
        st.success(
            "The selected monomers are parameterised. "
            "Continue to the Build Console to construct the polymer."
        )

    else:
        st.warning(
            "Resolve the missing parameter files before attempting "
            "to build this polymer."
        )