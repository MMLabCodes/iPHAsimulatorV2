"""Advanced Packmol-based solvated-system builder.

This module is intentionally separate from the simple GROMACS solvate/genion
route. It prepares Packmol inputs for future realistic polymer simulations while
keeping the quick validation workflow lightweight.
"""

"""
Dan comments:
    
Will leave this here, not sure what this builds yet - I havent gotten that far
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from collections.abc import Sequence
import shutil
import subprocess


AVOGADRO_CONSTANT = 6.02214076e23
LITERS_PER_NM3 = 1e-24
TIP3P_WATER_DENSITY_PER_NM3 = 33.367


TIP3P_WATER_PDB = """\
HETATM    1  O   WAT A   1       0.000   0.000   0.000  1.00  0.00           O
HETATM    2  H1  WAT A   1       0.096   0.000   0.000  1.00  0.00           H
HETATM    3  H2  WAT A   1      -0.024   0.093   0.000  1.00  0.00           H
END
"""


SODIUM_PDB = """\
HETATM    1 NA   NA  A   1       0.000   0.000   0.000  1.00  0.00          Na
END
"""


CHLORIDE_PDB = """\
HETATM    1 CL   CL  A   1       0.000   0.000   0.000  1.00  0.00          Cl
END
"""


@dataclass(frozen=True)
class PackmolBuildResult:
    """Files and counts produced by the Packmol solvated-system builder."""

    output_dir: Path
    solvated_pdb_path: Path
    packmol_input_path: Path
    packmol_log_path: Path
    copied_polymer_paths: tuple[Path, ...]
    support_structure_paths: tuple[Path, ...]
    box_size_nm: float
    water_count: int
    sodium_count: int
    chloride_count: int
    polymer_counts: tuple[int, ...]


def estimate_tip3p_water_count(box_size_nm: float) -> int:
    """Estimate the number of TIP3P waters for a cubic box at bulk density."""

    if box_size_nm <= 0:
        raise ValueError("box_size_nm must be positive")
    return max(1, round(TIP3P_WATER_DENSITY_PER_NM3 * box_size_nm**3))


def estimate_ion_pairs(box_size_nm: float, nacl_concentration_molar: float) -> int:
    """Estimate NaCl ion pairs from molarity and cubic box volume."""

    if box_size_nm <= 0:
        raise ValueError("box_size_nm must be positive")
    if nacl_concentration_molar < 0:
        raise ValueError("nacl_concentration_molar must be non-negative")
    if nacl_concentration_molar == 0:
        return 0

    box_volume_liters = box_size_nm**3 * LITERS_PER_NM3
    ion_pairs = round(nacl_concentration_molar * box_volume_liters * AVOGADRO_CONSTANT)
    return max(1, ion_pairs)


def _normalise_polymer_counts(
    polymer_count: int,
    num_polymers: int | Sequence[int],
) -> tuple[int, ...]:
    if isinstance(num_polymers, int):
        if num_polymers <= 0:
            raise ValueError("num_polymers must be positive")
        return tuple(num_polymers for _ in range(polymer_count))

    counts = tuple(num_polymers)
    if len(counts) != polymer_count:
        raise ValueError(
            "num_polymers must be an integer or a sequence matching polymer_structures"
        )
    if any(count <= 0 for count in counts):
        raise ValueError("all polymer counts must be positive")
    return counts


def _copy_polymer_structures(
    polymer_structures: Sequence[str | Path],
    output_dir: Path,
) -> tuple[Path, ...]:
    copied_paths: list[Path] = []
    for index, polymer_structure in enumerate(polymer_structures, start=1):
        source = Path(polymer_structure)
        if not source.exists():
            raise FileNotFoundError(f"Polymer structure not found: {source}")
        destination = output_dir / f"polymer_{index}{source.suffix or '.pdb'}"
        shutil.copy2(source, destination)
        copied_paths.append(destination)
    return tuple(copied_paths)


def _write_support_structures(output_dir: Path, water_model: str) -> tuple[Path, ...]:
    if water_model.lower() != "tip3p":
        raise ValueError("Only water_model='tip3p' is currently supported")

    water_path = output_dir / "tip3p_water.pdb"
    sodium_path = output_dir / "sodium_ion.pdb"
    chloride_path = output_dir / "chloride_ion.pdb"
    water_path.write_text(TIP3P_WATER_PDB)
    sodium_path.write_text(SODIUM_PDB)
    chloride_path.write_text(CHLORIDE_PDB)
    return water_path, sodium_path, chloride_path


def _structure_block(
    structure_path: Path,
    number: int,
    *,
    box_size_angstrom: float,
    margin_angstrom: float,
    comment: str,
) -> str:
    return "\n".join(
        [
            f"# {comment}",
            f"structure {structure_path.name}",
            f"  number {number}",
            (
                "  inside box "
                f"{margin_angstrom:.3f} {margin_angstrom:.3f} {margin_angstrom:.3f} "
                f"{box_size_angstrom - margin_angstrom:.3f} "
                f"{box_size_angstrom - margin_angstrom:.3f} "
                f"{box_size_angstrom - margin_angstrom:.3f}"
            ),
            "end structure",
            "",
        ]
    )


def _write_packmol_input(
    output_dir: Path,
    solvated_pdb_path: Path,
    copied_polymer_paths: Sequence[Path],
    polymer_counts: Sequence[int],
    water_path: Path,
    sodium_path: Path,
    chloride_path: Path,
    *,
    box_size_nm: float,
    polymer_spacing_nm: float,
    water_count: int,
    sodium_count: int,
    chloride_count: int,
) -> tuple[Path, str]:
    box_size_angstrom = box_size_nm * 10.0
    polymer_margin_angstrom = polymer_spacing_nm * 10.0
    if polymer_margin_angstrom * 2 >= box_size_angstrom:
        raise ValueError("polymer_spacing_nm leaves no usable space inside the box")

    lines = [
        "# Packmol input generated by iPHASimulator.",
        "# Advanced route for PHA oligomer + TIP3P water + NaCl systems.",
        "tolerance 2.0",
        "filetype pdb",
        f"output {solvated_pdb_path.name}",
        "",
    ]

    for index, (polymer_path, count) in enumerate(
        zip(copied_polymer_paths, polymer_counts, strict=True),
        start=1,
    ):
        lines.append(
            _structure_block(
                polymer_path,
                count,
                box_size_angstrom=box_size_angstrom,
                margin_angstrom=polymer_margin_angstrom,
                comment=f"Polymer component {index}",
            )
        )

    for path, count, comment in (
        (water_path, water_count, "TIP3P water"),
        (sodium_path, sodium_count, "Na+ ions"),
        (chloride_path, chloride_count, "Cl- ions"),
    ):
        if count == 0:
            continue
        lines.append(
            _structure_block(
                path,
                count,
                box_size_angstrom=box_size_angstrom,
                margin_angstrom=0.0,
                comment=comment,
            )
        )

    packmol_input = "\n".join(lines)
    packmol_input_path = output_dir / "packmol_input.inp"
    packmol_input_path.write_text(packmol_input)
    return packmol_input_path, packmol_input


def _ensure_cryst1_record(pdb_path: Path, box_size_nm: float) -> None:
    lines = pdb_path.read_text().splitlines()
    if lines and lines[0].startswith("CRYST1"):
        return
    box_size_angstrom = box_size_nm * 10.0
    cryst1 = (
        f"CRYST1{box_size_angstrom:9.3f}{box_size_angstrom:9.3f}"
        f"{box_size_angstrom:9.3f}{90.0:7.2f}{90.0:7.2f}{90.0:7.2f} P 1           1"
    )
    pdb_path.write_text("\n".join([cryst1, *lines]) + "\n")


def build_packmol_solvated_system(
    polymer_structures: Sequence[str | Path],
    output_dir: str | Path,
    *,
    box_size_nm: float,
    water_model: str = "tip3p",
    nacl_concentration_molar: float = 0.15,
    num_polymers: int | Sequence[int] = 1,
    polymer_spacing_nm: float = 1.0,
    packmol_command: str = "packmol",
    run_packmol: bool = True,
    runner=subprocess.run,
) -> PackmolBuildResult:
    """Build an advanced solvated PHA/TIP3P/NaCl initial PDB using Packmol.

    This route does not replace the standard GROMACS solvate/genion workflow.
    It is an advanced builder for future realistic polymer simulations and can
    later be extended to enzyme/polymer systems. Membranes are intentionally not
    implemented here yet.
    """

    if not polymer_structures:
        raise ValueError("At least one polymer structure is required")
    if box_size_nm <= 0:
        raise ValueError("box_size_nm must be positive")
    if polymer_spacing_nm < 0:
        raise ValueError("polymer_spacing_nm must be non-negative")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    polymer_counts = _normalise_polymer_counts(len(polymer_structures), num_polymers)
    copied_polymer_paths = _copy_polymer_structures(polymer_structures, output_path)
    water_path, sodium_path, chloride_path = _write_support_structures(
        output_path,
        water_model,
    )

    water_count = estimate_tip3p_water_count(box_size_nm)
    ion_pairs = estimate_ion_pairs(box_size_nm, nacl_concentration_molar)
    solvated_pdb_path = output_path / "solvated_system.pdb"
    packmol_log_path = output_path / "packmol.log"

    packmol_input_path, packmol_input = _write_packmol_input(
        output_path,
        solvated_pdb_path,
        copied_polymer_paths,
        polymer_counts,
        water_path,
        sodium_path,
        chloride_path,
        box_size_nm=box_size_nm,
        polymer_spacing_nm=polymer_spacing_nm,
        water_count=water_count,
        sodium_count=ion_pairs,
        chloride_count=ion_pairs,
    )

    if run_packmol:
        try:
            result = runner(
                [packmol_command],
                input=packmol_input,
                cwd=output_path,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except FileNotFoundError as exc:
            packmol_log_path.write_text(
                "Packmol executable not found. Install Packmol or set "
                "packmol_command to the correct executable.\n"
            )
            raise RuntimeError(
                "Packmol executable not found. Install Packmol or set "
                "packmol_command to the correct executable."
            ) from exc

        packmol_log_path.write_text(
            "STDOUT:\n"
            f"{result.stdout}\n"
            "STDERR:\n"
            f"{result.stderr}\n"
        )
        if result.returncode != 0:
            raise RuntimeError(
                "Packmol failed while building solvated_system.pdb with return "
                f"code {result.returncode}. See {packmol_log_path}."
            )
        if not solvated_pdb_path.exists():
            raise FileNotFoundError(f"Packmol did not write: {solvated_pdb_path}")
        _ensure_cryst1_record(solvated_pdb_path, box_size_nm)
    else:
        packmol_log_path.write_text(
            "Packmol was not run. Generated packmol_input.inp only.\n"
        )

    return PackmolBuildResult(
        output_dir=output_path,
        solvated_pdb_path=solvated_pdb_path,
        packmol_input_path=packmol_input_path,
        packmol_log_path=packmol_log_path,
        copied_polymer_paths=copied_polymer_paths,
        support_structure_paths=(water_path, sodium_path, chloride_path),
        box_size_nm=box_size_nm,
        water_count=water_count,
        sodium_count=ion_pairs,
        chloride_count=ion_pairs,
        polymer_counts=polymer_counts,
    )
