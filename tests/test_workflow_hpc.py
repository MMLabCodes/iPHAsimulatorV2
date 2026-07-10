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
                "  - monomer: 3HB",
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

    assert config["gaff2"]["charge_method"] == "abcg2"
    assert config["openmm"]["nvt_steps"] == 100
    assert config["stages"]["gaff2"] is False


def test_targets_from_config_and_stage_name():
    config = {
        "targets": [
            {"monomer": "3HB", "degree": 4, "stereochemistry": "R"},
        ]
    }

    targets = targets_from_config(config)

    assert targets[0].name == "P3HB_4"
    assert target_stage_name(targets[0]) == "P3HB_4"


def test_workflow_plan_respects_enabled_stages():
    config = {
        "output_root": "examples/output",
        "targets": [{"monomer": "3HB", "degree": 4}],
        "stages": {"build": True, "gaff2": False, "openmm": True},
    }

    plan = workflow_plan(config)

    assert plan == [
        "build P3HB_4 -> examples/output/polymer_structures/P3HB_4.sdf",
        "openmm dry P3HB_4 -> examples/output/md_tests/P3HB_4/openmm/dry_polymer",
    ]


def test_render_slurm_script_contains_configured_command(tmp_path):
    config_path = tmp_path / "workflow.yaml"
    config_path.write_text("targets:\n  - monomer: 3HB\n    degree: 4\n")
    config = load_workflow_config(config_path)

    script = render_slurm_script(
        config_path=config_path,
        repo_root="/repo/ipha",
        config=config,
    )

    assert "#SBATCH --job-name=ipha_validation" in script
    assert "cd /repo/ipha" in script
    assert f"--config {config_path}" in script
