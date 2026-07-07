#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import json
import subprocess
import sys
import os

import pandas as pd
import streamlit as st
from rdkit import Chem
from rdkit.Chem import Draw


STRUCTURE_DATABASE = Path("structure_database")
RESIDUE_CODES_CSV = STRUCTURE_DATABASE / "residue_codes.csv"
AMBERTOOLS_PYTHON = Path.home() / "miniconda3/envs/AmberTools23/bin/python"


st.set_page_config(
    page_title="iPHAsimulatorV2 - PHA Builder",
    layout="wide",
)

st.title("iPHAsimulatorV2 - PHA Polymer Builder")


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
    if len(sequence) == 0:
        return None

    unique_units = []

    for unit in sequence:
        if unit not in unique_units:
            unique_units.append(unit)

    if len(unique_units) == 1:
        return f"P{unique_units[0]}_{len(sequence)}"

    return (
        "co_"
        + "_".join([f"P{unit}" for unit in unique_units])
        + f"_custom_{len(sequence)}"
    )


def generate_polymer_smiles_from_sequence(sequence, smiles_lookup):
    if len(sequence) == 0:
        return None

    polymer_smiles = ""

    for i, pha_type in enumerate(sequence):
        smiles = smiles_lookup[pha_type]

        if i == len(sequence) - 1:
            polymer_smiles += smiles
        else:
            polymer_smiles += smiles[:-1]

    return polymer_smiles


def draw_monomer(pha_type):
    smiles = monomer_smiles[pha_type]
    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        return None

    return Draw.MolToImage(
        mol,
        size=(350, 250),
        legend=pha_type,
    )


def draw_polymer(polymer_smiles, polymer_name):
    mol = Chem.MolFromSmiles(polymer_smiles)

    if mol is None:
        return None

    return Draw.MolToImage(
        mol,
        size=(900, 300),
        legend=polymer_name,
    )


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

    output = builder.build_PHA_polymer(
        PHA_type=PHA_type,
        length=length,
    )

else:
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    if len(unique_units) > len(letters):
        raise ValueError(
            "Too many unique monomer types for automatic pattern naming."
        )

    unit_to_letter = {
        unit: letters[i]
        for i, unit in enumerate(unique_units)
    }

    pattern = "".join(
        unit_to_letter[unit]
        for unit in sequence
    )

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
        raise FileNotFoundError(
            f"Could not find AmberTools23 Python:\n{AMBERTOOLS_PYTHON}"
        )

    command = [
        str(AMBERTOOLS_PYTHON),
        "-c",
        build_code,
        str(STRUCTURE_DATABASE),
        json.dumps(sequence),
    ]

    ambertools_bin = AMBERTOOLS_PYTHON.parent

    env = dict(**os.environ)
    env["PATH"] = f"{ambertools_bin}:{env.get('PATH', '')}"

    result = subprocess.run(
        command,
        cwd=Path.cwd(),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result


with st.sidebar:
    st.header("Project paths")

    st.write("Structure database:")
    st.code(str(STRUCTURE_DATABASE))

    st.write("Residue code CSV:")
    st.code(str(RESIDUE_CODES_CSV))

    st.write("Build Python:")
    st.code(str(AMBERTOOLS_PYTHON))

    st.divider()

    st.header("Available data")
    st.write(f"Available PHA monomers: {len(available_phas)}")

    with st.expander("Show residue table"):
        st.dataframe(mainchain_df)


left_col, right_col = st.columns([2, 1])


with left_col:
    st.header("Available PHA Monomer Units")

    cols = st.columns(5)

    for i, pha in enumerate(available_phas):
        with cols[i % 5]:
            if st.button(
                pha,
                use_container_width=True,
            ):
                st.session_state.sequence.append(pha)
                st.session_state.preview_PHA = pha

    st.header("Current Polymer Sequence")

    if st.session_state.sequence:
        st.write(" → ".join(st.session_state.sequence))
    else:
        st.info("Click monomer buttons to build a polymer sequence.")

    st.write(f"Length: {len(st.session_state.sequence)}")

    control_cols = st.columns(3)

    with control_cols[0]:
        if st.button("Remove last"):
            if st.session_state.sequence:
                st.session_state.sequence.pop()

    with control_cols[1]:
        if st.button("Clear sequence"):
            st.session_state.sequence = []
            st.session_state.preview_PHA = None

    with control_cols[2]:
        build_clicked = st.button("Build polymer")


with right_col:
    st.header("Selected Monomer Preview")

    if st.session_state.preview_PHA is None:
        st.info("Click a monomer to preview its structure.")
    else:
        pha = st.session_state.preview_PHA
        smiles = monomer_smiles[pha]

        img = draw_monomer(pha)

        if img is None:
            st.error(f"Could not draw monomer: {pha}")
            st.code(smiles)
        else:
            st.image(img)
            st.subheader(pha)
            st.code(smiles)


polymer_name = get_polymer_name(st.session_state.sequence)

polymer_smiles = generate_polymer_smiles_from_sequence(
    st.session_state.sequence,
    monomer_smiles,
)

st.divider()

if polymer_name is not None:
    st.subheader("Generated Polymer Name")
    st.code(polymer_name)

if polymer_smiles is not None:
    st.subheader("Generated Polymer SMILES")
    st.code(polymer_smiles)

    polymer_img = draw_polymer(
        polymer_smiles,
        polymer_name,
    )

    if polymer_img is not None:
        st.subheader("Polymer Preview")
        st.image(polymer_img)
    else:
        st.warning("RDKit could not render the generated polymer SMILES.")


if build_clicked:
    if not st.session_state.sequence:
        st.error("No monomers selected.")
    else:
        st.info("Launching polymer build in AmberTools23 environment...")

        with st.spinner("Building polymer with PHAPolymerBuilder..."):
            try:
                result = build_polymer_subprocess(
                    st.session_state.sequence
                )
            except Exception as error:
                st.error("Could not launch build subprocess.")
                st.code(str(error))
                st.stop()

        if result.returncode == 0:
            st.success("Polymer build complete.")

            if result.stdout:
                st.subheader("Build output")
                st.code(result.stdout)

        else:
            st.error("Polymer build failed.")

            if result.stdout:
                st.subheader("STDOUT")
                st.code(result.stdout)

            if result.stderr:
                st.subheader("STDERR")
                st.code(result.stderr)