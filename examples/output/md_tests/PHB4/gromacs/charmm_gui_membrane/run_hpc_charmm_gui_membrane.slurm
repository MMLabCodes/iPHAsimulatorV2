#!/usr/bin/env bash
#SBATCH --job-name=PHB4_charmm_gui_membrane_gmx
#SBATCH --time=24:00:00
#SBATCH --partition=standard
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G
#SBATCH --output=logs/%x-%j.out
#SBATCH --error=logs/%x-%j.err

set -euo pipefail
mkdir -p logs

# Adjust module/environment commands for your HPC system.
# module load gromacs

# Workflow type: charmm_gui_membrane
# Common MD settings from the generated .mdp files:
# - timestep: 0.002 ps (2 fs)
# - constraints: h-bonds with LINCS
# - periodic boundary conditions: xyz
# - PME electrostatics
# - nonbonded cutoffs: rlist/rcoulomb/rvdw = 1.0 nm

# step6.1_equilibration: 50 ps NVT at 300 K; V-rescale thermostat; no pressure coupling; generates initial velocities.
gmx grompp -f step6.1_equilibration.mdp -c step6.0_minimization.gro -r step5_input.gro -p topol.top -n index.ndx -o step6.1_equilibration.tpr
gmx mdrun -deffnm step6.1_equilibration

# step6.2_equilibration: 50 ps NPT at 300 K and 1 bar; V-rescale thermostat; Berendsen pressure coupling.
gmx grompp -f step6.2_equilibration.mdp -c step6.1_equilibration.gro -r step5_input.gro -p topol.top -n index.ndx -o step6.2_equilibration.tpr
gmx mdrun -deffnm step6.2_equilibration

# step6.3_equilibration: 100 ps NPT at 300 K and 1 bar; V-rescale thermostat; Berendsen pressure coupling.
gmx grompp -f step6.3_equilibration.mdp -c step6.2_equilibration.gro -r step5_input.gro -p topol.top -n index.ndx -o step6.3_equilibration.tpr
gmx mdrun -deffnm step6.3_equilibration

# step6.4_equilibration: 100 ps NPT at 300 K and 1 bar; V-rescale thermostat; Berendsen pressure coupling.
gmx grompp -f step6.4_equilibration.mdp -c step6.3_equilibration.gro -r step5_input.gro -p topol.top -n index.ndx -o step6.4_equilibration.tpr
gmx mdrun -deffnm step6.4_equilibration

# step6.5_equilibration: 200 ps NPT at 300 K and 1 bar; V-rescale thermostat; C-rescale pressure coupling.
gmx grompp -f step6.5_equilibration.mdp -c step6.4_equilibration.gro -r step5_input.gro -p topol.top -n index.ndx -o step6.5_equilibration.tpr
gmx mdrun -deffnm step6.5_equilibration

# step6.6_equilibration: 200 ps NPT at 300 K and 1 bar; V-rescale thermostat; C-rescale pressure coupling.
gmx grompp -f step6.6_equilibration.mdp -c step6.5_equilibration.gro -r step5_input.gro -p topol.top -n index.ndx -o step6.6_equilibration.tpr
gmx mdrun -deffnm step6.6_equilibration

# step7_production: 100 ns production at 300 K and 1 bar; V-rescale thermostat; C-rescale pressure coupling.
gmx grompp -f step7_production.mdp -c step6.6_equilibration.gro -r step5_input.gro -p topol.top -n index.ndx -o step7_production.tpr
gmx mdrun -deffnm step7_production
