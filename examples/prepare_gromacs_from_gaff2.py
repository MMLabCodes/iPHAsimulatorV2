"""Prepare self-contained GROMACS workflow folders from GAFF2 AMBER outputs."""

from __future__ import annotations

from pathlib import Path
import argparse

from iphasimulator.simulation.gromacs_runner import prepare_gromacs_run_folder


TARGETS = ("PHB4", "PHB8", "PHO4", "PHO8", "PHDD4", "PHDD8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target",
        required=True,
        choices=TARGETS,
        help="Target name with existing GAFF2 outputs, for example PHB4.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("examples/output"),
        help="Root output directory containing md_tests/<TARGET>/gaff2.",
    )
    parser.add_argument(
        "--index-file",
        type=Path,
        help="Optional existing GROMACS index file to copy into each workflow folder.",
    )
    parser.add_argument(
        "--workflow-type",
        choices=("polymer", "charmm_gui_membrane"),
        default="polymer",
        help="Compatibility option; all workflow folders are generated.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    gaff2_dir = args.output_root / "md_tests" / args.target / "gaff2"
    gromacs_dir = args.output_root / "md_tests" / args.target / "gromacs"

    outputs = prepare_gromacs_run_folder(
        gaff2_dir / f"{args.target}.prmtop",
        gaff2_dir / f"{args.target}.inpcrd",
        gromacs_dir,
        args.target,
        workflow_type=args.workflow_type,
        index_file=args.index_file,
    )

    print(f"[{args.target}] workflow {outputs.workflow_type}")
    print(f"[{args.target}] wrote workflow root {outputs.output_dir}")
    print(f"[{args.target}] wrote dry polymer folder {outputs.dry_polymer_dir}")
    print(f"[{args.target}] wrote solvated polymer folder {outputs.solvated_polymer_dir}")
    print(
        f"[{args.target}] wrote CHARMM-GUI membrane folder "
        f"{outputs.charmm_gui_membrane_dir}"
    )
    print(f"[{args.target}] wrote {outputs.step5_input_gro_path}")
    print(f"[{args.target}] wrote {outputs.topol_top_path}")
    print(f"[{args.target}] wrote {outputs.index_ndx_path}")
    for mdp_path in outputs.mdp_paths:
        print(f"[{args.target}] wrote {mdp_path}")
    print(f"[{args.target}] wrote {outputs.local_script_path}")
    print(f"[{args.target}] wrote {outputs.hpc_script_path}")
    print(f"[{args.target}] wrote {outputs.charmm_gui_membrane_hpc_script_path}")


if __name__ == "__main__":
    main()
