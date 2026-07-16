#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Interactive molecular-viewer helpers for the iPHAsimulatorV2 GUI.
"""

from pathlib import Path

import py3Dmol


SUPPORTED_STRUCTURE_FORMATS = {
    ".pdb": "pdb",
    ".gro": "gro",
    ".mol2": "mol2",
    ".sdf": "sdf",
    ".xyz": "xyz",
}


WATER_RESIDUE_NAMES = [
    "WAT",
    "HOH",
    "SOL",
    "TIP3",
    "TIP3P",
]


def resolve_viewer_structure_file(
    system_files,
    system_name,
    prefer_pdb=True,
):
    """
    Resolve the best available coordinate file for molecular viewing.

    Parameters
    ----------
    system_files : dict
        Dictionary returned by PHAFileManager.get_md_system_files().

    system_name : str
        Full MD-system name.

    prefer_pdb : bool, optional
        Prefer a system PDB when one exists.

    Returns
    -------
    pathlib.Path
        Selected structure file.

    Notes
    -----
    Amber single-system builders normally create a PDB. Melt systems may
    only contain a GRO file.
    """

    system_dir = Path(
        system_files["system_dir"]
    )

    expected_pdb = (
        system_dir
        / f"{system_name}.pdb"
    )

    coordinate_file = Path(
        system_files["coordinate_file"]
    )

    if (
        prefer_pdb
        and expected_pdb.exists()
    ):
        return expected_pdb

    if coordinate_file.exists():
        return coordinate_file

    if expected_pdb.exists():
        return expected_pdb

    raise FileNotFoundError(
        "No viewable structure file was found.\n"
        f"Expected PDB:\n{expected_pdb}\n\n"
        f"Coordinate file:\n{coordinate_file}"
    )


def get_structure_format(
    structure_path,
):
    """
    Return the py3Dmol format for a structure file.
    """

    structure_path = Path(
        structure_path
    )

    extension = (
        structure_path
        .suffix
        .lower()
    )

    if extension not in SUPPORTED_STRUCTURE_FORMATS:
        raise ValueError(
            "Unsupported structure format: "
            f"{extension}\n"
            "Supported formats:\n"
            + "\n".join(
                sorted(
                    SUPPORTED_STRUCTURE_FORMATS
                )
            )
        )

    return SUPPORTED_STRUCTURE_FORMATS[
        extension
    ]


def get_colour_options(
    colour_scheme,
):
    """
    Convert a GUI colour name into py3Dmol style options.
    """

    if colour_scheme == "Element":
        return {
            "colorscheme": "default",
        }

    if colour_scheme == "Chain":
        return {
            "colorscheme": "chain",
        }

    if colour_scheme == "Residue":
        return {
            "colorscheme": "amino",
        }

    if colour_scheme == "Spectrum":
        return {
            "color": "spectrum",
        }

    raise ValueError(
        f"Unknown colour scheme: {colour_scheme}"
    )


def apply_viewer_style(
    viewer,
    display_style,
    colour_options,
):
    """
    Apply a selected representation to a py3Dmol viewer.
    """

    if display_style == "Ball and stick":
        viewer.setStyle(
            {},
            {
                "stick": {
                    "radius": 0.12,
                    **colour_options,
                },
                "sphere": {
                    "scale": 0.25,
                    **colour_options,
                },
            },
        )

    elif display_style == "Stick":
        viewer.setStyle(
            {},
            {
                "stick": {
                    "radius": 0.16,
                    **colour_options,
                },
            },
        )

    elif display_style == "Sphere":
        viewer.setStyle(
            {},
            {
                "sphere": {
                    "scale": 0.35,
                    **colour_options,
                },
            },
        )

    elif display_style == "Line":
        viewer.setStyle(
            {},
            {
                "line": {
                    **colour_options,
                },
            },
        )

    elif display_style == "Polymer with water lines":
        viewer.setStyle(
            {},
            {
                "stick": {
                    "radius": 0.14,
                    **colour_options,
                },
            },
        )

        for water_residue in WATER_RESIDUE_NAMES:
            viewer.setStyle(
                {
                    "resn": water_residue,
                },
                {
                    "line": {
                        "color": "#60a5fa",
                        "opacity": 0.35,
                    },
                },
            )

    elif display_style == "Surface":
        viewer.setStyle(
            {},
            {
                "stick": {
                    "radius": 0.1,
                    **colour_options,
                },
            },
        )

        viewer.addSurface(
            py3Dmol.VDW,
            {
                "opacity": 0.55,
                "color": "white",
            },
        )

    else:
        raise ValueError(
            f"Unknown display style: {display_style}"
        )


def render_structure(
    structure_path,
    display_style="Ball and stick",
    colour_scheme="Element",
    background_colour="#0f172a",
    width=1000,
    height=650,
):
    """
    Create an interactive py3Dmol viewer.

    Supported structure formats include PDB, GRO, MOL2, SDF and XYZ.

    Parameters
    ----------
    structure_path : str or pathlib.Path
        Molecular structure file.

    display_style : str, optional
        Molecular representation.

    colour_scheme : str, optional
        Colouring method.

    background_colour : str, optional
        Viewer background colour.

    width : int, optional
        Viewer width.

    height : int, optional
        Viewer height.

    Returns
    -------
    py3Dmol.view
        Configured viewer.
    """

    structure_path = Path(
        structure_path
    )

    if not structure_path.exists():
        raise FileNotFoundError(
            "Structure file not found:\n"
            f"{structure_path}"
        )

    structure_format = get_structure_format(
        structure_path
    )

    structure_text = structure_path.read_text(
        encoding="utf-8",
        errors="replace",
    )

    if not structure_text.strip():
        raise ValueError(
            "Structure file is empty:\n"
            f"{structure_path}"
        )

    viewer = py3Dmol.view(
        width=int(width),
        height=int(height),
    )

    viewer.addModel(
        structure_text,
        structure_format,
    )

    colour_options = get_colour_options(
        colour_scheme
    )

    apply_viewer_style(
        viewer=viewer,
        display_style=display_style,
        colour_options=colour_options,
    )

    viewer.setBackgroundColor(
        background_colour
    )

    viewer.zoomTo()

    return viewer


def render_pdb_structure(
    pdb_path,
    display_style="Ball and stick",
    colour_scheme="Element",
    background_colour="#0f172a",
    width=1000,
    height=650,
):
    """
    Backwards-compatible wrapper for rendering PDB files.
    """

    pdb_path = Path(
        pdb_path
    )

    if pdb_path.suffix.lower() != ".pdb":
        raise ValueError(
            "Expected a PDB file:\n"
            f"{pdb_path}"
        )

    return render_structure(
        structure_path=pdb_path,
        display_style=display_style,
        colour_scheme=colour_scheme,
        background_colour=background_colour,
        width=width,
        height=height,
    )