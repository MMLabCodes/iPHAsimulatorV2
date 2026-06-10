#!/bin/bash -l
#SBATCH --job-name=PHB4_polymer_MD
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:1
#SBATCH --mem=16G
#SBATCH --time=2-00:00
#SBATCH --output=logs/%x-%j.out
#SBATCH --error=logs/%x-%j.err

module load gromacs/2021.5-gcc-11.4.0-cuda-11.8.0

export OMP_NUM_THREADS=8

mkdir -p logs

# Step 6.1 — NVT

gmx grompp -f step6.1_nvt.mdp -o step6.1_nvt.tpr -c step6.0_minimization.gro -r step5_input.gro -p topol.top -n index.ndx -maxwarn 1

gmx mdrun -v -deffnm step6.1_nvt -pin on -nb gpu -pme gpu -bonded gpu -ntmpi 1 -ntomp 8

# Step 6.2 — NPT

gmx grompp -f step6.2_npt.mdp -o step6.2_npt.tpr -c step6.1_nvt.gro -r step5_input.gro -p topol.top -n index.ndx

gmx mdrun -v -deffnm step6.2_npt -pin on -nb gpu -pme gpu -bonded gpu -ntmpi 1 -ntomp 8

# Step 7 — Production

gmx grompp -f step7_production.mdp -o step7_production.tpr -c step6.2_npt.gro -p topol.top -n index.ndx

gmx mdrun -v -deffnm step7_production -pin on -nb gpu -pme gpu -bonded gpu -ntmpi 1 -ntomp 8
