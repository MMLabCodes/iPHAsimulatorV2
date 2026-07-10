"""Run an iPHASimulator workflow from a YAML config."""

from __future__ import annotations

from pathlib import Path
import argparse

from iphasimulator.export import to_pdb, to_sdf
from iphasimulator.build import build_pha_chain
from iphasimulator.parameterization_gaff2 import parameterize_gaff2
from iphasimulator.simulation_openmm_amber_runner import run_openmm_with_amber_topology
from iphasimulator.workflows import (
    load_workflow_config,
    render_slurm_script,
    target_stage_name,
    targets_from_config,
    workflow_plan,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("examples/hpc_validation_workflow.yaml"),
        help="YAML workflow configuration.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned actions without running AmberTools or OpenMM.",
    )
    parser.add_argument(
        "--write-slurm",
        type=Path,
        help="Write a SLURM submission script for this config and exit.",
    )
    return parser.parse_args()


def _structure_root(output_root: Path) -> Path:
    return output_root / "polymer_structures"


def _build_target(target, output_root: Path) -> tuple[Path, Path]:
    mol = build_pha_chain(target.monomer, target.degree, target.stereochemistry)
    structure_root = _structure_root(output_root)
    structure_root.mkdir(parents=True, exist_ok=True)
    sdf_path = structure_root / f"{target.name}.sdf"
    pdb_path = structure_root / f"{target.name}.pdb"
    to_sdf(mol, sdf_path)
    to_pdb(mol, pdb_path)
    return sdf_path, pdb_path


def run_configured_workflow(config: dict, *, dry_run: bool = False) -> None:
    if dry_run:
        print("Workflow plan:")
        for item in workflow_plan(config):
            print(f"- {item}")
        return

    output_root = Path(config["output_root"])
    output_root.mkdir(parents=True, exist_ok=True)
    stages = config["stages"]
    gaff2_config = config["gaff2"]
    openmm_config = config["openmm"]

    for target in targets_from_config(config):
        stage_name = target_stage_name(target)
        sdf_path = _structure_root(output_root) / f"{target.name}.sdf"

        if stages.get("build", False):
            sdf_path, pdb_path = _build_target(target, output_root)
            print(f"[{target.name}] wrote {sdf_path}")
            print(f"[{target.name}] wrote {pdb_path}")

        if stages.get("gaff2", False):
            gaff2_dir = output_root / "md_tests" / stage_name / "gaff2"
            gaff2_outputs = parameterize_gaff2(
                sdf_path,
                gaff2_dir,
                name=stage_name,
                net_charge=gaff2_config["net_charge"],
                residue_name=gaff2_config["residue_name"],
                charge_method=gaff2_config["charge_method"],
                atom_count_warning_threshold=gaff2_config[
                    "atom_count_warning_threshold"
                ],
                verbose=True,
            )
            print(f"[{stage_name}] wrote {gaff2_outputs.prmtop_path}")
            print(f"[{stage_name}] wrote {gaff2_outputs.inpcrd_path}")

        if stages.get("openmm", False):
            gaff2_dir = output_root / "md_tests" / stage_name / "gaff2"
            openmm_dir = output_root / "md_tests" / stage_name / "openmm" / "dry_polymer"
            openmm_outputs = run_openmm_with_amber_topology(
                gaff2_dir / f"{stage_name}.prmtop",
                gaff2_dir / f"{stage_name}.inpcrd",
                openmm_dir,
                **openmm_config,
            )
            print(f"[{stage_name}] wrote {openmm_outputs.final_pdb_path}")
            print(f"[{stage_name}] summary {openmm_outputs.summary_log_path}")


def main() -> None:
    args = parse_args()
    config = load_workflow_config(args.config)

    if args.write_slurm:
        script = render_slurm_script(config_path=args.config, config=config)
        args.write_slurm.parent.mkdir(parents=True, exist_ok=True)
        args.write_slurm.write_text(script)
        print(f"Wrote {args.write_slurm}")
        return

    run_configured_workflow(config, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
