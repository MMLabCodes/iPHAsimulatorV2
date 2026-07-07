#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import json
import os
import subprocess

import pandas as pd
import streamlit as st
from rdkit import Chem
from rdkit.Chem import Draw


STRUCTURE_DATABASE = Path("structure_database")
RESIDUE_CODES_CSV = STRUCTURE_DATABASE / "residue_codes.csv"
AMBERTOOLS_PYTHON = Path.home() / "miniconda3/envs/AmberTools23/bin/python"


st.set_page_config(
    page_title="iPHAsimulatorV2",
    page_icon="🧬",
    layout="wide",
)


st.markdown(
    """
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #111827 45%, #172554 100%);
    color: #e5e7eb;
}
.main-title {
    font-size: 3.2rem;
    font-weight: 900;
    background: linear-gradient(90deg, #67e8f9, #a78bfa, #f472b6);
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
    box-shadow: 0 12px 35px rgba(0,0,0,0.25);
}
.sequence-chip {
    display: inline-block;
    padding: 0.35rem 0.7rem;
    margin: 0.2rem;
    border-radius: 999px;
    background: linear-gradient(90deg, #0891b2, #7c3aed);
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
    background: rgba(34,197,94,0.12);
    padding: 0.8rem 1rem;
    border-radius: 12px;
}
.warn-box {
    border-left: 5px solid #f59e0b;
    background: rgba(245,158,11,0.12);
    padding: 0.8rem 1rem;
    border-radius: 12px;
}
div.stButton > button {
    border-radius: 999px;
    font-weight: 700;
    border: 1px solid rgba(103,232,249,0.45);
    background: rgba(15,23,42,0.75);
    color: #e0f2fe;
}
div.stButton > button:hover {
    border-color: #f472b6;
    color: white;
    transform: scale(1.02);
}
</style>
""",
    unsafe_allow_html=True,
)


st.markdown('<div class="main-title">🧬 iPHAsimulatorV2</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Interactive PHA polymer construction, SMILES preview, and AmberTools-backed building.</div>',
    unsafe_allow_html=True,
)


@st.cache_data
def load_available_PHA_monomers(residue_codes_csv):
    df = pd.read_csv(residue_codes_csv)
    mainchain_df = df[df["component"] == "mainchain"].copy()
    mainchain_df = mainchain_df.dropna(subset=["PHA_type", "smiles"])
    mainchain_df = mainchain_df[
        mainchain_df["smiles"].astype(str).str.strip() != ""
    ]

    available_phas = sorted(mainchain_df["PHA_type"].unique())
    monomer_smiles = {
        row["PHA_type"]: row["smiles"]
        for _, row in mainchain_df.iterrows()
    }

    return available_phas, monomer_smiles, mainchain_df


try:
    available_phas, monomer_smiles, mainchain_df = load_available_PHA_monomers(
        RESIDUE_CODES_CSV
    )
except Exception as error:
    st.error("Could not load available PHA monomers.")
    st.code(str(error))
    st.stop()


if "sequence" not in st.session_state:
    st.session_state.sequence = []

if "preview_PHA" not in st.session_state:
    st.session_state.preview_PHA = None


def get_polymer_name(sequence):
    if not sequence:
        return None

    unique_units = []
    for unit in sequence:
        if unit not in unique_units:
            unique_units.append(unit)

    if len(unique_units) == 1:
        return f"P{unique_units[0]}_{len(sequence)}"

    return "co_" + "_".join([f"P{unit}" for unit in unique_units]) + f"_custom_{len(sequence)}"


def generate_polymer_smiles_from_sequence(sequence, smiles_lookup):
    if not sequence:
        return None

    polymer_smiles = ""
    for i, pha_type in enumerate(sequence):
        smiles = smiles_lookup[pha_type]
        polymer_smiles += smiles if i == len(sequence) - 1 else smiles[:-1]

    return polymer_smiles


def draw_monomer(pha_type):
    mol = Chem.MolFromSmiles(monomer_smiles[pha_type])
    if mol is None:
        return None
    return Draw.MolToImage(mol, size=(420, 300), legend=pha_type)


def draw_polymer(polymer_smiles, polymer_name):
    mol = Chem.MolFromSmiles(polymer_smiles)
    if mol is None:
        return None
    return Draw.MolToImage(mol, size=(1200, 360), legend=polymer_name)


def build_polymer_subprocess(sequence):
    build_code = r"""
import sys
import json
from src.iphasimulator.build_pha import PHAPolymerBuilder

root_dir = sys.argv[1]
sequence = json.loads(sys.argv[2])

builder = PHAPolymerBuilder(root_dir)

unique_units = []
for unit in sequence:
    if unit not in unique_units:
        unique_units.append(unit)

if len(unique_units) == 1:
    PHA_type = unique_units[0]
    length = len(sequence)
    print(f"Building homopolymer: P{PHA_type}_{length}")
    output = builder.build_PHA_polymer(PHA_type=PHA_type, length=length)

else:
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if len(unique_units) > len(letters):
        raise ValueError("Too many unique monomer types.")

    unit_to_letter = {unit: letters[i] for i, unit in enumerate(unique_units)}
    pattern = "".join(unit_to_letter[unit] for unit in sequence)
    length = len(sequence)

    print("Building copolymer.")
    print("PHA types:", unique_units)
    print("Pattern:", pattern)
    print("Length:", length)

    output = builder.build_PHA_copolymer(
        PHA_types=unique_units,
        pattern=pattern,
        length=length,
    )

print("Build complete.")
print(output)
"""

    if not AMBERTOOLS_PYTHON.exists():
        raise FileNotFoundError(f"Could not find AmberTools23 Python:\n{AMBERTOOLS_PYTHON}")

    ambertools_bin = AMBERTOOLS_PYTHON.parent
    env = dict(**os.environ)
    env["PATH"] = f"{ambertools_bin}:{env.get('PATH', '')}"

    command = [
        str(AMBERTOOLS_PYTHON),
        "-c",
        build_code,
        str(STRUCTURE_DATABASE),
        json.dumps(sequence),
    ]

    return subprocess.run(
        command,
        cwd=Path.cwd(),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


polymer_name = get_polymer_name(st.session_state.sequence)
polymer_smiles = generate_polymer_smiles_from_sequence(
    st.session_state.sequence,
    monomer_smiles,
)


with st.sidebar:
    st.markdown("## ⚙️ Control Centre")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("Structure database")
    st.code(str(STRUCTURE_DATABASE))
    st.write("AmberTools Python")
    st.code(str(AMBERTOOLS_PYTHON))
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("## 📊 Database")
    st.metric("Available monomers", len(available_phas))
    st.metric("Current length", len(st.session_state.sequence))
    st.metric("Unique units", len(set(st.session_state.sequence)))

    with st.expander("Show monomer table"):
        st.dataframe(mainchain_df, use_container_width=True)


tab_builder, tab_preview, tab_logs = st.tabs(
    ["🧱 Polymer Builder", "🔬 Molecular Preview", "🖥 Build Console"]
)


with tab_builder:
    top_metrics = st.columns(4)
    top_metrics[0].metric("Sequence length", len(st.session_state.sequence))
    top_metrics[1].metric("Unique monomers", len(set(st.session_state.sequence)))
    top_metrics[2].metric("Mode", "Homo" if len(set(st.session_state.sequence)) <= 1 else "Co")
    top_metrics[3].metric("Build env", "AmberTools23")

    st.markdown("### Available PHA Monomer Units")

    search = st.text_input("Filter monomers", placeholder="Try 3HB, 4HB, phenyl, fluor...")
    filtered_phas = [
        pha for pha in available_phas
        if search.lower() in pha.lower()
    ]

    cols = st.columns(6)
    for i, pha in enumerate(filtered_phas):
        with cols[i % 6]:
            if st.button(f"➕ {pha}", use_container_width=True):
                st.session_state.sequence.append(pha)
                st.session_state.preview_PHA = pha
                st.rerun()

    st.markdown("### Current Sequence")

    if st.session_state.sequence:
        chip_html = "".join(
            [f'<span class="sequence-chip">{unit}</span>' for unit in st.session_state.sequence]
        )
        st.markdown(chip_html, unsafe_allow_html=True)
    else:
        st.markdown(
            '<div class="warn-box">Click monomer buttons above to start building a polymer sequence.</div>',
            unsafe_allow_html=True,
        )

    control_cols = st.columns([1, 1, 1, 2])

    with control_cols[0]:
        if st.button("↩️ Remove last", use_container_width=True):
            if st.session_state.sequence:
                st.session_state.sequence.pop()
                st.rerun()

    with control_cols[1]:
        if st.button("🧹 Clear", use_container_width=True):
            st.session_state.sequence = []
            st.session_state.preview_PHA = None
            st.rerun()

    with control_cols[2]:
        duplicate_n = st.number_input("Repeat current sequence", min_value=1, max_value=20, value=1)

    with control_cols[3]:
        if st.button("🔁 Apply repeat", use_container_width=True):
            if st.session_state.sequence:
                original = list(st.session_state.sequence)
                st.session_state.sequence = original * int(duplicate_n)
                st.rerun()

    st.divider()

    if polymer_name:
        st.markdown("### Generated Build Target")
        st.code(polymer_name)

    if polymer_smiles:
        st.markdown("### Generated Polymer SMILES")
        st.code(polymer_smiles)


with tab_preview:
    col_a, col_b = st.columns([1, 2])

    with col_a:
        st.markdown("### Selected Monomer")
        if st.session_state.preview_PHA is None:
            st.info("Click a monomer to preview it.")
        else:
            pha = st.session_state.preview_PHA
            img = draw_monomer(pha)
            if img is None:
                st.error(f"Could not draw {pha}")
            else:
                st.image(img)
                st.markdown(f"### `{pha}`")
                st.code(monomer_smiles[pha])

    with col_b:
        st.markdown("### Polymer Preview")
        if polymer_smiles is None:
            st.info("No polymer sequence yet.")
        else:
            img = draw_polymer(polymer_smiles, polymer_name)
            if img is None:
                st.warning("RDKit could not render this polymer SMILES.")
            else:
                st.image(img, use_container_width=True)

            st.markdown("### Polymer Summary")
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.write(f"**Name:** `{polymer_name}`")
            st.write(f"**Length:** `{len(st.session_state.sequence)}`")
            st.write(f"**Unique monomers:** `{', '.join(sorted(set(st.session_state.sequence)))}`")
            st.write(f"**SMILES characters:** `{len(polymer_smiles)}`")
            st.markdown("</div>", unsafe_allow_html=True)


with tab_logs:
    st.markdown("### Build Polymer")

    st.markdown(
        """
<div class="small-muted">
This launches the backend builder in the AmberTools23 environment. 
The GUI environment only runs Streamlit and RDKit rendering.
</div>
""",
        unsafe_allow_html=True,
    )

    build_clicked = st.button("🚀 Build polymer now", use_container_width=True)

    if build_clicked:
        if not st.session_state.sequence:
            st.error("No monomers selected.")
        else:
            st.info("Launching polymer build in AmberTools23 environment...")

            progress = st.progress(0)
            status = st.empty()

            with st.spinner("Building polymer with PHAPolymerBuilder..."):
                try:
                    status.write("Preparing subprocess...")
                    progress.progress(15)

                    result = build_polymer_subprocess(st.session_state.sequence)

                    progress.progress(85)
                    status.write("Build subprocess finished.")

                except Exception as error:
                    progress.progress(100)
                    st.error("Could not launch build subprocess.")
                    st.code(str(error))
                    st.stop()

            progress.progress(100)

            if result.returncode == 0:
                st.success("Polymer build complete.")
                st.balloons()

                st.markdown('<div class="good-box">Backend returned success.</div>', unsafe_allow_html=True)

                if result.stdout:
                    st.subheader("STDOUT")
                    st.code(result.stdout)

            else:
                st.error("Polymer build failed.")

                if result.stdout:
                    st.subheader("STDOUT")
                    st.code(result.stdout)

                if result.stderr:
                    st.subheader("STDERR")
                    st.code(result.stderr)

    st.divider()

    st.markdown("### Current command context")
    st.write("AmberTools Python:")
    st.code(str(AMBERTOOLS_PYTHON))
    st.write("Working directory:")
    st.code(str(Path.cwd()))