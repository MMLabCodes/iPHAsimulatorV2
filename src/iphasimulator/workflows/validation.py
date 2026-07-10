"""Reusable validation workflows for tutorial notebooks and examples."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from rdkit import Chem

from iphasimulator.build import build_pha_chain
from iphasimulator.export import to_pdb, to_sdf
from iphasimulator.naming import oligomer_name


@dataclass(frozen=True)
class ValidationTarget:
    """A named PHA oligomer used for quick build validation."""

    monomer: str
    degree: int
    stereochemistry: str = "R"

    @property
    def name(self) -> str:
        return oligomer_name(self.monomer, self.degree)


DEFAULT_VALIDATION_TARGETS: tuple[ValidationTarget, ...] = (
    ValidationTarget("3HB", 4),
    ValidationTarget("3HO", 4),
    ValidationTarget("3HDD", 4),
)

LARGE_VALIDATION_TARGETS: tuple[ValidationTarget, ...] = (
    ValidationTarget("3HB", 8),
    ValidationTarget("3HO", 8),
    ValidationTarget("3HDD", 8),
)


def build_validation_molecules(
    targets: tuple[ValidationTarget, ...] = DEFAULT_VALIDATION_TARGETS,
) -> dict[str, Chem.Mol]:
    """Build the requested validation PHA oligomers."""

    return {
        target.name: build_pha_chain(
            target.monomer,
            target.degree,
            target.stereochemistry,
        )
        for target in targets
    }


def describe_molecules(molecules: dict[str, Chem.Mol]) -> list[dict[str, object]]:
    """Return SMILES and chiral-centre summaries for built molecules."""

    rows: list[dict[str, object]] = []
    for name, mol in molecules.items():
        Chem.AssignStereochemistry(mol, cleanIt=True, force=True)
        rows.append(
            {
                "name": name,
                "atoms": mol.GetNumAtoms(),
                "smiles": Chem.MolToSmiles(mol, isomericSmiles=True),
                "chiral_centres": Chem.FindMolChiralCenters(
                    mol,
                    includeUnassigned=True,
                ),
            }
        )
    return rows


def export_molecules(
    molecules: dict[str, Chem.Mol],
    output_dir: str | Path,
) -> list[Path]:
    """Export molecules to SDF and PDB files."""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    for name, mol in molecules.items():
        sdf_path = output_path / f"{name}.sdf"
        pdb_path = output_path / f"{name}.pdb"
        to_sdf(mol, sdf_path)
        to_pdb(mol, pdb_path)
        written.extend([sdf_path, pdb_path])
    return written
