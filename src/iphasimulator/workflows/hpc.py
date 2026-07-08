"""Config-driven workflow helpers for scripted and HPC runs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from iphasimulator.workflows.validation import ValidationTarget


DEFAULT_WORKFLOW_CONFIG: dict[str, Any] = {
    "output_root": "examples/output",
    "targets": [
        {"monomer": "3HB", "degree": 4, "stereochemistry": "R"},
        {"monomer": "3HO", "degree": 4, "stereochemistry": "R"},
        {"monomer": "3HDD", "degree": 4, "stereochemistry": "R"},
    ],
    "stages": {
        "build": True,
        "gaff2": True,
        "openmm": True,
    },
    "gaff2": {
        "charge_method": "abcg2",
        "net_charge": 0,
        "residue_name": "PHA",
        "atom_count_warning_threshold": 120,
    },
    "openmm": {
        "minimization_max_iterations": 200,
        "nvt_steps": 100,
        "npt_steps": 100,
        "production_steps": 100,
        "report_interval": 10,
        "temperature_kelvin": 300.0,
        "pressure_bar": 1.0,
        "platform_name": None,
        "platform_precision": "mixed",
    },
    "slurm": {
        "job_name": "ipha_validation",
        "time": "02:00:00",
        "partition": "standard",
        "cpus_per_task": 4,
        "mem": "8G",
        "conda_env": "ipha",
    },
}


def _deep_merge(base: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_workflow_config(path: str | Path) -> dict[str, Any]:
    """Load a YAML workflow config and apply defaults."""

    config_path = Path(path)
    with config_path.open() as handle:
        loaded = yaml.safe_load(handle) or {}
    if not isinstance(loaded, dict):
        raise ValueError(f"Workflow config must be a YAML mapping: {config_path}")
    return _deep_merge(DEFAULT_WORKFLOW_CONFIG, loaded)


def targets_from_config(config: dict[str, Any]) -> tuple[ValidationTarget, ...]:
    """Parse validation targets from workflow config."""

    targets = config.get("targets", [])
    if not isinstance(targets, list) or not targets:
        raise ValueError("Workflow config must define a non-empty targets list")

    parsed: list[ValidationTarget] = []
    for target in targets:
        if not isinstance(target, dict):
            raise ValueError("Each target must be a mapping")
        parsed.append(
            ValidationTarget(
                monomer=target["monomer"],
                degree=int(target["degree"]),
                stereochemistry=target.get("stereochemistry", "R"),
            )
        )
    return tuple(parsed)


def target_stage_name(target: ValidationTarget) -> str:
    """Return the short target name used for MD output directories."""

    return target.name


def workflow_plan(config: dict[str, Any]) -> list[str]:
    """Return human-readable planned workflow actions."""

    stages = config["stages"]
    output_root = Path(config["output_root"])
    plan: list[str] = []
    structure_root = output_root / "polymer_structures"
    for target in targets_from_config(config):
        stage_name = target_stage_name(target)
        if stages.get("build", False):
            plan.append(
                f"build {target.name} -> {structure_root / (target.name + '.sdf')}"
            )
        if stages.get("gaff2", False):
            plan.append(
                f"gaff2 {target.name} -> "
                f"{output_root / 'md_tests' / stage_name / 'gaff2'}"
            )
        if stages.get("openmm", False):
            plan.append(
                f"openmm dry {stage_name} -> "
                f"{output_root / 'md_tests' / stage_name / 'openmm' / 'dry_polymer'}"
            )
    return plan


def render_slurm_script(
    *,
    config_path: str | Path,
    repo_root: str | Path = ".",
    config: dict[str, Any] | None = None,
) -> str:
    """Render a SLURM submission script for a configured workflow."""

    workflow_config = config or load_workflow_config(config_path)
    slurm = workflow_config["slurm"]
    repo_path = Path(repo_root)
    config_path = Path(config_path)

    return "\n".join(
        [
            "#!/usr/bin/env bash",
            f"#SBATCH --job-name={slurm['job_name']}",
            f"#SBATCH --time={slurm['time']}",
            f"#SBATCH --partition={slurm['partition']}",
            f"#SBATCH --cpus-per-task={slurm['cpus_per_task']}",
            f"#SBATCH --mem={slurm['mem']}",
            "#SBATCH --output=logs/%x-%j.out",
            "#SBATCH --error=logs/%x-%j.err",
            "",
            "set -euo pipefail",
            "",
            f"cd {repo_path}",
            "mkdir -p logs",
            "",
            "# Adjust this block to match your HPC module/conda setup.",
            "source \"$(conda info --base)/etc/profile.d/conda.sh\"",
            f"conda activate {slurm['conda_env']}",
            "",
            f"PYTHONPATH=src python examples/run_configured_workflow.py --config {config_path}",
            "",
        ]
    )
