from iphasimulator.workflows import (
    load_workflow_config,
    render_slurm_script,
    target_stage_name,
    targets_from_config,
    workflow_plan,
)


def test_load_workflow_config_applies_defaults(tmp_path):
    config_path = tmp_path / "workflow.yaml"
    config_path.write_text(
        "\n".join(
            [
                "targets:",
                "  - monomer: PHB",
                "    degree: 4",
                "stages:",
                "  build: true",
                "  gaff2: false",
                "  openmm: false",
                "",
            ]
        )
    )

    config = load_workflow_config(config_path)

    assert config["gaff2"]["charge_method"] == "gas"
    assert config["openmm"]["nvt_steps"] == 100
    assert config["stages"]["gaff2"] is False


def test_targets_from_config_and_stage_name():
    config = {
        "targets": [
            {"monomer": "PHB", "degree": 4, "stereochemistry": "R"},
        ]
    }

    targets = targets_from_config(config)

    assert targets[0].name == "PHB4_R"
    assert target_stage_name(targets[0]) == "PHB4"


def test_workflow_plan_respects_enabled_stages():
    config = {
        "output_root": "examples/output",
        "targets": [{"monomer": "PHB", "degree": 4}],
        "stages": {"build": True, "gaff2": False, "openmm": True},
    }

    plan = workflow_plan(config)

    assert plan == [
        "build PHB4_R -> examples/output/polymer_structures/PHB4_R.sdf",
        "openmm dry PHB4 -> examples/output/md_tests/PHB4/openmm/dry_polymer",
    ]


def test_render_slurm_script_contains_configured_command(tmp_path):
    config_path = tmp_path / "workflow.yaml"
    config_path.write_text("targets:\n  - monomer: PHB\n    degree: 4\n")
    config = load_workflow_config(config_path)

    script = render_slurm_script(
        config_path=config_path,
        repo_root="/repo/ipha",
        config=config,
    )

    assert "#SBATCH --job-name=ipha_validation" in script
    assert "cd /repo/ipha" in script
    assert f"--config {config_path}" in script
