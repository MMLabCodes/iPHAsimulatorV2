"""Convert AMBER topology/coordinate files to GROMACS files."""

from __future__ import annotations

from dataclasses import dataclass
import math
from pathlib import Path


@dataclass(frozen=True)
class GromacsConversionOutputs:
    """Files produced by AMBER to GROMACS conversion."""

    output_dir: Path
    top_path: Path
    gro_path: Path


def _normalize_structure_charge(structure, *, max_correction: float = 0.05) -> float:
    """Remove small charge-rounding residue before writing GROMACS topology."""

    atoms = list(structure.atoms)
    if not atoms:
        raise ValueError("Cannot normalize the charge of a structure without atoms")

    total_charge = math.fsum(atom.charge for atom in atoms)
    target_charge = round(total_charge)
    correction = target_charge - total_charge
    if abs(correction) > max_correction:
        raise ValueError(
            f"Structure charge {total_charge:.8f} is too far from integer charge "
            f"{target_charge} to normalize safely"
        )
    if correction == 0:
        return total_charge

    correction_per_atom = correction / len(atoms)
    for atom in atoms:
        atom.charge += correction_per_atom
    atoms[-1].charge += target_charge - math.fsum(atom.charge for atom in atoms)
    return math.fsum(atom.charge for atom in atoms)


def convert_amber_to_gromacs(
    prmtop_file: str,
    inpcrd_file: str,
    output_dir: str,
    system_name: str,
) -> GromacsConversionOutputs:
    """Convert AMBER ``prmtop``/``inpcrd`` files to GROMACS ``top``/``gro``.

    ParmEd is required because it understands both AMBER and GROMACS topology
    formats. Install it with ``conda install -c conda-forge parmed``.
    """

    try:
        import parmed as pmd
    except ImportError as exc:
        raise ImportError(
            "ParmEd is required to convert AMBER files to GROMACS. Install it "
            "with: conda install -c conda-forge parmed"
        ) from exc

    prmtop_path = Path(prmtop_file)
    inpcrd_path = Path(inpcrd_file)
    if not prmtop_path.exists():
        raise FileNotFoundError(f"AMBER topology file not found: {prmtop_path}")
    if not inpcrd_path.exists():
        raise FileNotFoundError(f"AMBER coordinate file not found: {inpcrd_path}")
    if not system_name.strip():
        raise ValueError("system_name must be a non-empty string")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    top_path = output_path / f"{system_name}.top"
    gro_path = output_path / f"{system_name}.gro"

    structure = pmd.load_file(str(prmtop_path), str(inpcrd_path))
    _normalize_structure_charge(structure)
    structure.save(str(top_path), overwrite=True)
    structure.save(str(gro_path), overwrite=True)

    return GromacsConversionOutputs(
        output_dir=output_path,
        top_path=top_path,
        gro_path=gro_path,
    )
