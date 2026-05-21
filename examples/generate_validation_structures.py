"""Generate validation PHA oligomer structures as SDF and PDB files."""

from __future__ import annotations

from pathlib import Path
import argparse

from iphasimulator.workflows import (
    DEFAULT_VALIDATION_TARGETS,
    LARGE_VALIDATION_TARGETS,
    build_validation_molecules,
    export_molecules,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--include-large",
        action="store_true",
        help="Also build the n=8 validation systems.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("examples/output"),
        help="Directory for generated SDF and PDB files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    targets = DEFAULT_VALIDATION_TARGETS
    if args.include_large:
        targets = targets + LARGE_VALIDATION_TARGETS

    molecules = build_validation_molecules(targets)
    for path in export_molecules(molecules, args.output_dir):
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
