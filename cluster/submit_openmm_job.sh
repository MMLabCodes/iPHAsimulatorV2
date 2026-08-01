#!/bin/bash

set -euo pipefail

# =============================================================================
# Usage
# =============================================================================
#
# bash cluster/submit_openmm_job.sh \
#     /path/to/generated_openmm_script.py
#
# The generated OpenMM script should already contain:
#
# - the registered system name
# - topology and coordinate paths
# - the simulation output directory
# - simulation settings
#
# =============================================================================

if [[ $# -ne 1 ]]; then
    echo "Usage:"
    echo "  $0 <generated_openmm_script.py>"
    exit 1
fi

# =============================================================================
# Resolve paths
# =============================================================================

# Resolve the repository root relative to this launcher rather than relying
# on the directory from which the launcher is called.
SCRIPT_DIR="$(
    cd "$(dirname "${BASH_SOURCE[0]}")"
    pwd
)"

PROJECT_ROOT="$(
    cd "${SCRIPT_DIR}/.."
    pwd
)"

SIMULATION_SCRIPT="$(realpath "$1")"

if [[ ! -f "$SIMULATION_SCRIPT" ]]; then
    echo "Simulation script not found:"
    echo "$SIMULATION_SCRIPT"
    exit 1
fi

SCRIPT_NAME="$(basename "$SIMULATION_SCRIPT" .py)"
SCRIPT_DIRECTORY="$(dirname "$SIMULATION_SCRIPT")"

TIMESTAMP="$(date +"%Y%m%d_%H%M%S")"

JOB_FILE="${SCRIPT_DIRECTORY}/${SCRIPT_NAME}_${TIMESTAMP}.job"
SLURM_OUTPUT="${SCRIPT_DIRECTORY}/slurm_${SCRIPT_NAME}_%j.out"
SLURM_ERROR="${SCRIPT_DIRECTORY}/slurm_${SCRIPT_NAME}_%j.err"

# =============================================================================
# Scientific environment
# =============================================================================

IPHA_STORAGE="/scratch/s.983045/iphasimulator"
IPHA_ENV="${IPHA_STORAGE}/envs/iphasimulator"
IPHA_PYTHON="${IPHA_ENV}/bin/python"

if [[ ! -x "$IPHA_PYTHON" ]]; then
    echo "iPHAsimulator Python was not found:"
    echo "$IPHA_PYTHON"
    exit 1
fi

echo
echo "Project root      : $PROJECT_ROOT"
echo "Simulation script : $SIMULATION_SCRIPT"
echo "Script directory  : $SCRIPT_DIRECTORY"
echo "Job file          : $JOB_FILE"
echo "Environment       : $IPHA_ENV"
echo "Python executable : $IPHA_PYTHON"
echo

# =============================================================================
# Write the Slurm job
# =============================================================================

cat > "$JOB_FILE" << EOF
#!/bin/bash --login

#SBATCH --job-name=${SCRIPT_NAME}
#SBATCH --account=scw1977
#SBATCH --partition=accel_ai

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=96G
#SBATCH --time=2-00:00
#SBATCH --gres=gpu:1

#SBATCH --output=${SLURM_OUTPUT}
#SBATCH --error=${SLURM_ERROR}

set -euo pipefail

# =============================================================================
# Environment
# =============================================================================

module purge

export IPHA_STORAGE="${IPHA_STORAGE}"
export CONDA_PKGS_DIRS="\${IPHA_STORAGE}/conda-pkgs"

IPHA_ENV="${IPHA_ENV}"
IPHA_PYTHON="${IPHA_PYTHON}"

if [[ ! -x "\${IPHA_PYTHON}" ]]; then
    echo "iPHAsimulator Python executable not found:"
    echo "\${IPHA_PYTHON}"
    exit 1
fi

# Put the scientific environment first on PATH so any external commands
# launched by Python are also resolved from the correct environment.
export PATH="\${IPHA_ENV}/bin:\${PATH}"

# =============================================================================
# Job information
# =============================================================================

echo "============================================================"
echo "iPHAsimulator OpenMM job"
echo "============================================================"
echo "Slurm job ID       : \$SLURM_JOB_ID"
echo "Slurm node         : \$SLURMD_NODENAME"
echo "Submission dir     : \$SLURM_SUBMIT_DIR"
echo "Simulation script  : ${SIMULATION_SCRIPT}"
echo "Project root       : ${PROJECT_ROOT}"
echo "Python executable  : \${IPHA_PYTHON}"
echo "Python version     : \$(\"\${IPHA_PYTHON}\" --version)"
echo "ParmEd version     : \$(\"\${IPHA_PYTHON}\" -c 'import parmed; print(parmed.__version__)')"
echo "OpenMM version     : \$(\"\${IPHA_PYTHON}\" -c 'import openmm; print(openmm.__version__)')"
echo "Start time         : \$(date)"
echo "============================================================"

nvidia-smi || true

# =============================================================================
# Run simulation
# =============================================================================

cd "${PROJECT_ROOT}"

"\${IPHA_PYTHON}" -u "${SIMULATION_SCRIPT}"

echo
echo "============================================================"
echo "Simulation finished"
echo "End time: \$(date)"
echo "============================================================"
EOF

chmod +x "$JOB_FILE"

echo "Submitting job..."

SUBMISSION_OUTPUT="$(sbatch "$JOB_FILE")"
echo "$SUBMISSION_OUTPUT"