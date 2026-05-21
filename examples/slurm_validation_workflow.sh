#!/usr/bin/env bash
#SBATCH --job-name=ipha_validation
#SBATCH --time=02:00:00
#SBATCH --partition=standard
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --output=logs/%x-%j.out
#SBATCH --error=logs/%x-%j.err

set -euo pipefail

cd .
mkdir -p logs

# Adjust this block to match your HPC module/conda setup.
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate ipha

PYTHONPATH=src python examples/run_configured_workflow.py --config examples/hpc_validation_workflow.yaml
