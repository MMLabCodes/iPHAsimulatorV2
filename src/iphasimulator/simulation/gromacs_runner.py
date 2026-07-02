"""Generate GROMACS run folders and command templates."""

"""
Dan comments:
  
This could be useful if we use GROMACS for anything.

However, if a GROMACS task can be carried out in openmm, i suggest we do that. Openmm is compatible with
GROMACS files so this is not required unless we need to run a type of simulation only GROMACS can run.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib import resources
from pathlib import Path
import shutil
import stat
import re
import subprocess
import warnings

from iphasimulator.conversion import convert_amber_to_gromacs


@dataclass(frozen=True)
class GromacsRunFiles:
    """Files generated for a staged GROMACS run."""

    output_dir: Path
    minim_mdp_path: Path
    nvt_mdp_path: Path
    npt_mdp_path: Path
    production_mdp_path: Path
    run_script_path: Path


@dataclass(frozen=True)
class GromacsPreparedRunFolder:
    """Files generated for a GROMACS run folder."""

    output_dir: Path
    workflow_type: str
    dry_polymer_dir: Path
    solvated_polymer_dir: Path
    charmm_gui_membrane_dir: Path
    step5_input_gro_path: Path
    topol_top_path: Path
    index_ndx_path: Path
    mdp_paths: tuple[Path, ...]
    local_script_path: Path
    hpc_script_path: Path
    charmm_gui_membrane_hpc_script_path: Path


@dataclass(frozen=True)
class GromacsTopologyValidation:
    """Validation result for GROMACS topology include files."""

    topol_top_path: Path
    is_standalone: bool
    included_files: tuple[Path, ...]
    missing_files: tuple[Path, ...]

    @property
    def valid(self) -> bool:
        return not self.missing_files


@dataclass(frozen=True)
class GromacsLocalMinimizationCheck:
    """Files and command needed to run local GROMACS minimisation."""

    output_dir: Path
    required_files: tuple[Path, ...]
    missing_files: tuple[Path, ...]
    command: tuple[str, ...]

    @property
    def ready(self) -> bool:
        return not self.missing_files

    @property
    def command_text(self) -> str:
        return " ".join(self.command)


@dataclass(frozen=True)
class GromacsBoxValidation:
    """Box-size validation against GROMACS nonbonded cutoffs."""

    gro_path: Path
    mdp_path: Path
    box_vectors_nm: tuple[float, ...]
    shortest_box_vector_nm: float
    cutoffs_nm: dict[str, float]

    @property
    def max_cutoff_nm(self) -> float | None:
        if not self.cutoffs_nm:
            return None
        return max(self.cutoffs_nm.values())

    @property
    def valid(self) -> bool:
        if self.max_cutoff_nm is None:
            return True
        return self.shortest_box_vector_nm > 2 * self.max_cutoff_nm


@dataclass(frozen=True)
class GromacsSolvationFiles:
    """Files generated for the standard GROMACS solvate/genion workflow."""

    output_dir: Path
    ions_mdp_path: Path
    solvation_itp_paths: tuple[Path, ...]
    solvent_itp_path: Path
    cation_itp_path: Path
    anion_itp_path: Path
    solvate_script_path: Path
    local_script_path: Path
    hpc_script_path: Path
    charmm_gui_membrane_hpc_script_path: Path

    @property
    def tip3p_ions_itp_path(self) -> Path:
        """Backward-compatible alias for older callers."""

        return self.solvent_itp_path


@dataclass(frozen=True)
class GromacsSolvatedTopologyValidation:
    """Water and ion molecule counts parsed from a GROMACS topology."""

    topol_top_path: Path
    molecule_counts: dict[str, int]
    water_count: int
    cation_count: int
    anion_count: int

    @property
    def sodium_count(self) -> int:
        """Backward-compatible alias; may include POT/K in newer workflows."""

        return self.cation_count

    @property
    def chloride_count(self) -> int:
        """Backward-compatible alias for anion count."""

        return self.anion_count

    @property
    def has_water(self) -> bool:
        return self.water_count > 0

    @property
    def has_ions(self) -> bool:
        return self.cation_count + self.anion_count > 0


@dataclass(frozen=True)
class GromacsGromppValidation:
    """Result of a lightweight GROMACS ``grompp`` validation command."""

    command: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0


@dataclass(frozen=True)
class GromacsCoordinateTopologyValidation:
    """Atom-count comparison between a GRO coordinate file and topology."""

    gro_path: Path
    topol_top_path: Path
    coordinate_atom_count: int
    molecule_counts: dict[str, int]
    molecule_atom_counts: dict[str, int]
    expected_atom_count: int | None

    @property
    def can_compare(self) -> bool:
        return self.expected_atom_count is not None

    @property
    def valid(self) -> bool:
        return self.expected_atom_count == self.coordinate_atom_count


GROMACS_POLYMER_MDP_TEMPLATE_NAMES = (
    "step6.0_minimization.mdp",
    "step6.1_nvt.mdp",
    "step6.2_npt.mdp",
    "step7_production.mdp",
)


GROMACS_CHARMM_GUI_MEMBRANE_MDP_TEMPLATE_NAMES = (
    "step6.0_minimization.mdp",
    "step6.1_equilibration.mdp",
    "step6.2_equilibration.mdp",
    "step6.3_equilibration.mdp",
    "step6.4_equilibration.mdp",
    "step6.5_equilibration.mdp",
    "step6.6_equilibration.mdp",
    "step7_production.mdp",
)


GROMACS_MDP_TEMPLATE_NAMES = GROMACS_POLYMER_MDP_TEMPLATE_NAMES


GROMACS_ALL_MDP_TEMPLATE_NAMES = tuple(
    dict.fromkeys(
        GROMACS_POLYMER_MDP_TEMPLATE_NAMES
        + GROMACS_CHARMM_GUI_MEMBRANE_MDP_TEMPLATE_NAMES
    )
)


GROMACS_WORKFLOW_MDP_TEMPLATE_NAMES = {
    "polymer": GROMACS_POLYMER_MDP_TEMPLATE_NAMES,
    "charmm_gui_membrane": GROMACS_CHARMM_GUI_MEMBRANE_MDP_TEMPLATE_NAMES,
}


INCLUDE_PATTERN = re.compile(r'^\s*#include\s+"([^"]+)"')


LOCAL_MINIMIZATION_REQUIRED_FILENAMES = (
    "step5_input.gro",
    "topol.top",
    "index.ndx",
    "step6.0_minimization.mdp",
    "run_step6_local.sh",
)


MDP_CUTOFF_KEYS = ("rlist", "rcoulomb", "rvdw")

WATER_MOLECULE_NAMES = ("SOL", "WAT", "TIP3", "TIP3P", "HOH")
CATION_MOLECULE_NAMES = ("SOD", "NA", "NA+", "POT", "K", "K+")
ANION_MOLECULE_NAMES = ("CLA", "CL", "CL-")

GROMACS_SOLVATION_TEMPLATE_DIR = "data/gromacs_solvation"
GROMACS_SOLVATION_TEMPLATE_NAMES = (
    "ions.mdp",
    "tip3_ions_atomtypes.itp",
    "TIP3_SOL.itp",
    "TIP3.itp",
    "SOD.itp",
    "POT.itp",
    "CLA.itp",
)
GROMACS_SOLVATION_TOPOLOGY_INCLUDE_NAMES = (
    "tip3_ions_atomtypes.itp",
    "TIP3_SOL.itp",
    "SOD.itp",
    "CLA.itp",
)


MINIM_MDP = """; Energy minimisation
integrator      = steep
emtol           = 1000.0
emstep          = 0.01
nsteps          = 5000
cutoff-scheme   = Verlet
coulombtype     = PME
rcoulomb        = 1.0
rvdw            = 1.0
pbc             = xyz
"""

NVT_MDP = """; NVT equilibration
integrator              = md
nsteps                  = 50000
dt                      = 0.002
continuation            = no
constraint_algorithm    = lincs
constraints             = h-bonds
cutoff-scheme           = Verlet
coulombtype             = PME
rcoulomb                = 1.0
rvdw                    = 1.0
tcoupl                  = V-rescale
tc-grps                 = System
tau_t                   = 1.0
ref_t                   = 300
pcoupl                  = no
pbc                     = xyz
gen_vel                 = yes
gen_temp                = 300
gen_seed                = -1
"""

NPT_MDP = """; NPT equilibration
integrator              = md
nsteps                  = 50000
dt                      = 0.002
continuation            = yes
constraint_algorithm    = lincs
constraints             = h-bonds
cutoff-scheme           = Verlet
coulombtype             = PME
rcoulomb                = 1.0
rvdw                    = 1.0
tcoupl                  = V-rescale
tc-grps                 = System
tau_t                   = 1.0
ref_t                   = 300
pcoupl                  = C-rescale
pcoupltype              = isotropic
tau_p                   = 5.0
ref_p                   = 1.0
compressibility         = 4.5e-5
pbc                     = xyz
gen_vel                 = no
"""

PRODUCTION_MDP = """; Production MD
integrator              = md
nsteps                  = 500000
dt                      = 0.002
continuation            = yes
constraint_algorithm    = lincs
constraints             = h-bonds
cutoff-scheme           = Verlet
coulombtype             = PME
rcoulomb                = 1.0
rvdw                    = 1.0
tcoupl                  = V-rescale
tc-grps                 = System
tau_t                   = 1.0
ref_t                   = 300
pcoupl                  = C-rescale
pcoupltype              = isotropic
tau_p                   = 5.0
ref_p                   = 1.0
compressibility         = 4.5e-5
pbc                     = xyz
gen_vel                 = no
nstxout-compressed      = 1000
nstenergy               = 1000
nstlog                  = 1000
"""


def _run_script(system_name: str) -> str:
    return "\n".join(
        [
            "#!/usr/bin/env bash",
            "set -euo pipefail",
            "",
            f"gmx grompp -f minim.mdp -c {system_name}.gro -p {system_name}.top -o minim.tpr",
            "gmx mdrun -deffnm minim",
            "",
            f"gmx grompp -f nvt.mdp -c minim.gro -p {system_name}.top -o nvt.tpr",
            "gmx mdrun -deffnm nvt",
            "",
            f"gmx grompp -f npt.mdp -c nvt.gro -p {system_name}.top -o npt.tpr",
            "gmx mdrun -deffnm npt",
            "",
            f"gmx grompp -f production.mdp -c npt.gro -p {system_name}.top -o production.tpr",
            "gmx mdrun -deffnm production",
            "",
        ]
    )


def write_gromacs_run_files(
    output_dir: str | Path,
    system_name: str = "system",
) -> GromacsRunFiles:
    """Write basic GROMACS ``mdp`` files and a staged run script."""

    if not system_name.strip():
        raise ValueError("system_name must be a non-empty string")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    minim_mdp_path = output_path / "minim.mdp"
    nvt_mdp_path = output_path / "nvt.mdp"
    npt_mdp_path = output_path / "npt.mdp"
    production_mdp_path = output_path / "production.mdp"
    run_script_path = output_path / "run_gromacs.sh"

    minim_mdp_path.write_text(MINIM_MDP)
    nvt_mdp_path.write_text(NVT_MDP)
    npt_mdp_path.write_text(NPT_MDP)
    production_mdp_path.write_text(PRODUCTION_MDP)
    run_script_path.write_text(_run_script(system_name))
    run_script_path.chmod(run_script_path.stat().st_mode | stat.S_IXUSR)

    return GromacsRunFiles(
        output_dir=output_path,
        minim_mdp_path=minim_mdp_path,
        nvt_mdp_path=nvt_mdp_path,
        npt_mdp_path=npt_mdp_path,
        production_mdp_path=production_mdp_path,
        run_script_path=run_script_path,
    )


def _copy_mdp_templates(
    output_dir: Path,
    template_names: tuple[str, ...],
) -> tuple[Path, ...]:
    template_root = resources.files("iphasimulator").joinpath("data/gromacs_mdp")
    written: list[Path] = []
    for template_name in template_names:
        destination = output_dir / template_name
        source = template_root.joinpath(template_name)
        destination.write_text(source.read_text())
        written.append(destination)
    return tuple(written)


def _copy_workflow_inputs(
    source_dir: Path,
    destination_dir: Path,
    *,
    overwrite: bool = True,
) -> tuple[Path, Path, Path]:
    """Copy canonical GROMACS input files into a self-contained workflow dir."""

    destination_dir.mkdir(parents=True, exist_ok=True)
    copied_paths: list[Path] = []
    for filename in ("step5_input.gro", "topol.top", "index.ndx"):
        source = source_dir / filename
        destination = destination_dir / filename
        if not source.exists():
            raise FileNotFoundError(f"Required workflow input is missing: {source}")
        if overwrite or not destination.exists():
            shutil.copy2(source, destination)
        copied_paths.append(destination)
    return copied_paths[0], copied_paths[1], copied_paths[2]


def _copy_solvation_templates(
    output_dir: Path,
    template_names: tuple[str, ...] = GROMACS_SOLVATION_TEMPLATE_NAMES,
) -> tuple[Path, ...]:
    template_root = resources.files("iphasimulator").joinpath(
        GROMACS_SOLVATION_TEMPLATE_DIR
    )
    written: list[Path] = []
    for template_name in template_names:
        destination = output_dir / template_name
        source = template_root.joinpath(template_name)
        destination.write_text(source.read_text())
        written.append(destination)
    return tuple(written)


def _read_gro_atom_count(gro_path: Path) -> int:
    lines = gro_path.read_text().splitlines()
    if len(lines) < 2:
        raise ValueError(f"Invalid GRO file, missing atom-count line: {gro_path}")
    try:
        return int(lines[1].strip())
    except ValueError as exc:
        raise ValueError(f"Invalid GRO atom count in {gro_path}: {lines[1]!r}") from exc


def _write_default_index(gro_path: Path, index_path: Path) -> None:
    atom_count = _read_gro_atom_count(gro_path)
    atom_numbers = [str(number) for number in range(1, atom_count + 1)]
    lines = ["[ System ]"]
    for start in range(0, atom_count, 15):
        lines.append(" ".join(atom_numbers[start : start + 15]))
    lines.append("")
    index_path.write_text("\n".join(lines))


def _read_gro_box_vectors(gro_path: Path) -> tuple[float, ...]:
    lines = [line for line in gro_path.read_text().splitlines() if line.strip()]
    if len(lines) < 3:
        raise ValueError(f"Invalid GRO file, missing box-vector line: {gro_path}")
    try:
        box_vectors = tuple(float(value) for value in lines[-1].split())
    except ValueError as exc:
        raise ValueError(
            f"Invalid GRO box-vector line in {gro_path}: {lines[-1]!r}"
        ) from exc
    if len(box_vectors) not in {3, 9}:
        raise ValueError(
            f"Invalid GRO box-vector count in {gro_path}: expected 3 or 9 values"
        )
    return box_vectors


def _read_mdp_cutoffs(mdp_path: Path) -> dict[str, float]:
    cutoffs: dict[str, float] = {}
    for line in mdp_path.read_text().splitlines():
        setting = line.split(";", 1)[0].strip()
        if "=" not in setting:
            continue
        key, raw_value = (part.strip() for part in setting.split("=", 1))
        key = key.lower()
        if key not in MDP_CUTOFF_KEYS:
            continue
        try:
            cutoffs[key] = float(raw_value.split()[0])
        except (IndexError, ValueError):
            continue
    return cutoffs


def create_gromacs_simulation_box(
    input_gro: str | Path,
    output_gro: str | Path,
    *,
    padding_nm: float = 3.0,
    box_type: str = "cubic",
    gmx_command: str = "gmx",
    runner=subprocess.run,
) -> Path:
    """Create a centered GROMACS simulation box with ``gmx editconf``."""

    input_path = Path(input_gro)
    output_path = Path(output_gro)
    command = [
        gmx_command,
        "editconf",
        "-f",
        input_path.name,
        "-o",
        output_path.name,
        "-c",
        "-d",
        str(padding_nm),
        "-bt",
        box_type,
    ]
    try:
        result = runner(
            command,
            cwd=input_path.parent,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except FileNotFoundError as exc:
        raise RuntimeError(
            "GROMACS executable was not found while creating the simulation box. "
            "Install GROMACS or make sure the 'gmx' command is on PATH."
        ) from exc

    if result.returncode != 0:
        raise RuntimeError(
            "GROMACS editconf failed while creating the simulation box with "
            f"return code {result.returncode}.\nSTDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )
    if not output_path.exists():
        raise FileNotFoundError(f"GROMACS editconf did not write: {output_path}")
    return output_path


def validate_gromacs_box_against_mdp(
    gro_file: str | Path,
    mdp_file: str | Path,
) -> GromacsBoxValidation:
    """Warn when a GRO box is too small for the MDP nonbonded cutoffs."""

    gro_path = Path(gro_file)
    mdp_path = Path(mdp_file)
    box_vectors = _read_gro_box_vectors(gro_path)
    shortest_box_vector = min(box_vectors[:3])
    cutoffs = _read_mdp_cutoffs(mdp_path)
    validation = GromacsBoxValidation(
        gro_path=gro_path,
        mdp_path=mdp_path,
        box_vectors_nm=box_vectors,
        shortest_box_vector_nm=shortest_box_vector,
        cutoffs_nm=cutoffs,
    )
    max_cutoff = validation.max_cutoff_nm
    if max_cutoff is not None and shortest_box_vector <= 2 * max_cutoff:
        warnings.warn(
            "GROMACS box may be too small for the nonbonded cutoff: "
            f"shortest box vector is {shortest_box_vector:.4f} nm, "
            f"max cutoff is {max_cutoff:.4f} nm, and GROMACS needs more than "
            f"{2 * max_cutoff:.4f} nm.",
            UserWarning,
            stacklevel=2,
        )
    return validation


def _write_local_minimization_script(
    path: Path,
    *,
    coordinate_input: str = "step5_input.gro",
) -> None:
    path.write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "set -euo pipefail",
                "",
                f"gmx grompp -f step6.0_minimization.mdp -c {coordinate_input} -r {coordinate_input} -p topol.top -n index.ndx -o step6.0_minimization.tpr -maxwarn 1",
                "gmx mdrun -deffnm step6.0_minimization",
                "",
            ]
        )
    )
    path.chmod(path.stat().st_mode | stat.S_IXUSR)


GROMACS_WORKFLOW_HPC_STEPS = {
    "polymer": (
        (
            "step6.1_nvt",
            "step6.0_minimization.gro",
            "100 ps NVT at 300 K; V-rescale thermostat; no pressure coupling; generates initial velocities.",
        ),
        (
            "step6.2_npt",
            "step6.1_nvt.gro",
            "500 ps NPT at 300 K and 1 bar; isotropic C-rescale pressure coupling.",
        ),
        (
            "step7_production",
            "step6.2_npt.gro",
            "100 ns production MD at 300 K and 1 bar; isotropic C-rescale pressure coupling.",
        ),
    ),
    "charmm_gui_membrane": (
        (
            "step6.1_equilibration",
            "step6.0_minimization.gro",
            "50 ps NVT at 300 K; V-rescale thermostat; no pressure coupling; generates initial velocities.",
        ),
        (
            "step6.2_equilibration",
            "step6.1_equilibration.gro",
            "50 ps NPT at 300 K and 1 bar; V-rescale thermostat; Berendsen pressure coupling.",
        ),
        (
            "step6.3_equilibration",
            "step6.2_equilibration.gro",
            "100 ps NPT at 300 K and 1 bar; V-rescale thermostat; Berendsen pressure coupling.",
        ),
        (
            "step6.4_equilibration",
            "step6.3_equilibration.gro",
            "100 ps NPT at 300 K and 1 bar; V-rescale thermostat; Berendsen pressure coupling.",
        ),
        (
            "step6.5_equilibration",
            "step6.4_equilibration.gro",
            "200 ps NPT at 300 K and 1 bar; V-rescale thermostat; C-rescale pressure coupling.",
        ),
        (
            "step6.6_equilibration",
            "step6.5_equilibration.gro",
            "200 ps NPT at 300 K and 1 bar; V-rescale thermostat; C-rescale pressure coupling.",
        ),
        (
            "step7_production",
            "step6.6_equilibration.gro",
            "100 ns production at 300 K and 1 bar; V-rescale thermostat; C-rescale pressure coupling.",
        ),
    ),
}


def _write_hpc_equilibration_script(
    path: Path,
    *,
    job_name: str,
    workflow_type: str,
    reference_structure: str = "step5_input.gro",
) -> None:
    if workflow_type == "polymer":
        _write_kcl_polymer_hpc_script(path, job_name=job_name)
        return

    steps = GROMACS_WORKFLOW_HPC_STEPS[workflow_type]
    lines = [
        "#!/usr/bin/env bash",
        f"#SBATCH --job-name={job_name}_gmx",
        "#SBATCH --time=24:00:00",
        "#SBATCH --partition=standard",
        "#SBATCH --cpus-per-task=8",
        "#SBATCH --mem=16G",
        "#SBATCH --output=logs/%x-%j.out",
        "#SBATCH --error=logs/%x-%j.err",
        "",
        "set -euo pipefail",
        "mkdir -p logs",
        "",
        "# Adjust module/environment commands for your HPC system.",
        "# module load gromacs",
        "",
        f"# Workflow type: {workflow_type}",
        "# Common MD settings from the generated .mdp files:",
        "# - timestep: 0.002 ps (2 fs)",
        "# - constraints: h-bonds with LINCS",
        "# - periodic boundary conditions: xyz",
        "# - PME electrostatics",
        "# - nonbonded cutoffs: rlist/rcoulomb/rvdw = 1.0 nm",
        "",
    ]
    for step_name, coordinate_input, description in steps:
        lines.extend(
            [
                f"# {step_name}: {description}",
                f"gmx grompp -f {step_name}.mdp -c {coordinate_input} -r {reference_structure} -p topol.top -n index.ndx -o {step_name}.tpr",
                f"gmx mdrun -deffnm {step_name}",
                "",
            ]
        )
    path.write_text("\n".join(lines))
    path.chmod(path.stat().st_mode | stat.S_IXUSR)


def _write_kcl_polymer_hpc_script(path: Path, *, job_name: str) -> None:
    lines = [
        "#!/bin/bash -l",
        f"#SBATCH --job-name={job_name}_polymer_MD",
        "#SBATCH --partition=gpu",
        "#SBATCH --nodes=1",
        "#SBATCH --ntasks=1",
        "#SBATCH --cpus-per-task=8",
        "#SBATCH --gres=gpu:1",
        "#SBATCH --mem=16G",
        "#SBATCH --time=2-00:00",
        "#SBATCH --output=logs/%x-%j.out",
        "#SBATCH --error=logs/%x-%j.err",
        "",
        "module load gromacs/2021.5-gcc-11.4.0-cuda-11.8.0",
        "",
        "export OMP_NUM_THREADS=8",
        "",
        "mkdir -p logs",
        "",
        "# Step 6.1 — NVT",
        "",
        "gmx grompp -f step6.1_nvt.mdp -o step6.1_nvt.tpr -c step6.0_minimization.gro -r step5_input.gro -p topol.top -n index.ndx -maxwarn 1",
        "",
        "gmx mdrun -v -deffnm step6.1_nvt -pin on -nb gpu -pme gpu -bonded gpu -ntmpi 1 -ntomp 8",
        "",
        "# Step 6.2 — NPT",
        "",
        "gmx grompp -f step6.2_npt.mdp -o step6.2_npt.tpr -c step6.1_nvt.gro -r step5_input.gro -p topol.top -n index.ndx",
        "",
        "gmx mdrun -v -deffnm step6.2_npt -pin on -nb gpu -pme gpu -bonded gpu -ntmpi 1 -ntomp 8",
        "",
        "# Step 7 — Production",
        "",
        "gmx grompp -f step7_production.mdp -o step7_production.tpr -c step6.2_npt.gro -p topol.top -n index.ndx",
        "",
        "gmx mdrun -v -deffnm step7_production -pin on -nb gpu -pme gpu -bonded gpu -ntmpi 1 -ntomp 8",
    ]
    path.write_text("\n".join(lines) + "\n")
    path.chmod(path.stat().st_mode | stat.S_IXUSR)


def _infer_polymer_hpc_job_name(output_path: Path) -> str:
    if output_path.name == "solvated_polymer" and output_path.parent.name == "gromacs":
        return output_path.parent.parent.name or "gromacs"
    return output_path.parent.name or "gromacs"


def _write_solvate_script(
    path: Path,
    *,
    box_padding_nm: float,
    ion_concentration_molar: float,
) -> None:
    script = """#!/usr/bin/env bash
set -euo pipefail
export GMX_MAXBACKUP=-1

fail_with_log() {
    local command_name="$1"
    local log_path="$2"
    echo "ERROR: ${command_name} failed. See ${log_path}." >&2
    if [[ -f "${log_path}" ]]; then
        echo "--- Last 50 lines of ${log_path} ---" >&2
        tail -n 50 "${log_path}" >&2 || true
        echo "--- End ${log_path} ---" >&2
    fi
    exit 1
}

run_logged() {
    local command_name="$1"
    local log_path="$2"
    shift 2
    printf '+ %q' "$@" > "${log_path}"
    printf '\\n' >> "${log_path}"
    if "$@" >> "${log_path}" 2>&1; then
        echo "${command_name} completed; log: ${log_path}"
    else
        fail_with_log "${command_name}" "${log_path}"
    fi
}

run_genion_logged() {
    local log_path="genion.log"
    local genion_args=(-s ions.tpr -o system_neutralized.gro -p topol.top -neutral -pname SOD -nname CLA)
    if awk -v concentration="${ION_CONCENTRATION_MOLAR}" 'BEGIN { exit !(concentration > 0) }'; then
        genion_args+=(-conc "${ION_CONCENTRATION_MOLAR}")
    fi
    printf '+ printf %q | gmx genion' "${SOLVENT_GROUP}" > "${log_path}"
    printf ' %q' "${genion_args[@]}" >> "${log_path}"
    printf '\\n' >> "${log_path}"
    if printf "%s\\n" "${SOLVENT_GROUP}" | gmx genion "${genion_args[@]}" >> "${log_path}" 2>&1; then
        echo "genion completed; log: ${log_path}"
    else
        echo "ERROR: genion failed while selecting solvent group '${SOLVENT_GROUP}'." >&2
        echo "If your solvent group is not SOL, rerun this script with --solvent-group <name>." >&2
        fail_with_log "genion" "${log_path}"
    fi
}

run_stdin_logged() {
    local command_name="$1"
    local log_path="$2"
    local stdin_text="$3"
    shift 3
    printf '+ printf %q |' "${stdin_text}" > "${log_path}"
    printf ' %q' "$@" >> "${log_path}"
    printf '\\n' >> "${log_path}"
    if printf "%b" "${stdin_text}" | "$@" >> "${log_path}" 2>&1; then
        echo "${command_name} completed; log: ${log_path}"
    else
        fail_with_log "${command_name}" "${log_path}"
    fi
}

clean_generated_files() {
    rm -f \
        step5_input_box.gro \
        step5_solvated.gro \
        step5_ions.gro \
        genion.tpr \
        mdout.mdp \
        editconf.log \
        minim_grompp_check.log \
        editconf_box.log \
        make_ndx_box.log \
        solvate.log \
        ions_grompp.log \
        genion.log \
        editconf_final.log \
        make_ndx_final.log \
        minim_grompp.log \
        \\#*\\# \
        \\#*.\\#
    for generated_path in step6.0_minimization.*; do
        [[ "${generated_path}" == "step6.0_minimization.mdp" ]] && continue
        rm -f "${generated_path}"
    done
}

reset_from_dry_polymer() {
    local dry_dir="../dry_polymer"
    if [[ -f "${dry_dir}/topol.top" && -f "${dry_dir}/step5_input.gro" ]]; then
        cp "${dry_dir}/topol.top" topol.top
        cp "${dry_dir}/step5_input.gro" step5_input.gro
        if [[ -f "${dry_dir}/index.ndx" ]]; then
            cp "${dry_dir}/index.ndx" index.ndx
        fi
        echo "Reset topol.top and step5_input.gro from ${dry_dir}."
    else
        echo "Using existing topol.top and step5_input.gro; ../dry_polymer was not found."
    fi
}

ensure_include() {
    local include_file="$1"
    if grep -Eq "^[[:space:]]*#include[[:space:]]+\\"${include_file}\\"" topol.top; then
        return
    fi
    if [[ ! -f "${include_file}" ]]; then
        echo "ERROR: topol.top does not include ${include_file}, and ${include_file} is missing." >&2
        exit 1
    fi

    local tmp_path="topol.top.tmp.$$"
    if awk -v include="#include \\"${include_file}\\"" '
        BEGIN { inserted = 0 }
        !inserted && tolower($0) ~ /^[[:space:]]*\\[ moleculetype \\]/ {
            print ""
            print include
            print ""
            inserted = 1
        }
        { print }
        END { if (!inserted) exit 42 }
    ' topol.top > "${tmp_path}"; then
        mv "${tmp_path}" topol.top
        echo "Added ${include_file} include to topol.top"
    else
        rm -f "${tmp_path}"
        echo "ERROR: Could not insert ${include_file}; no [ moleculetype ] section found in topol.top." >&2
        exit 1
    fi
}

topology_source_files() {
    printf '%s\\n' topol.top
    sed -n 's/^[[:space:]]*#include[[:space:]]*"\\([^"]*\\)".*/\\1/p' topol.top | while IFS= read -r include_path; do
        if [[ -f "${include_path}" ]]; then
            printf '%s\\n' "${include_path}"
        fi
    done
}

has_moleculetype() {
    local molecule_name="$1"
    awk -v target="${molecule_name}" '
        BEGIN { found = 0; in_moleculetype = 0 }
        tolower($0) ~ /^[[:space:]]*\\[ moleculetype \\]/ { in_moleculetype = 1; next }
        /^[[:space:]]*\\[/ { in_moleculetype = 0 }
        in_moleculetype {
            line = $0
            sub(/;.*/, "", line)
            gsub(/^[ \\t]+|[ \\t]+$/, "", line)
            split(line, fields, /[ \\t]+/)
            if (toupper(fields[1]) == target) found = 1
        }
        END { exit found ? 0 : 1 }
    ' $(topology_source_files)
}

has_atomtype() {
    local atom_type="$1"
    awk -v target="${atom_type}" '
        BEGIN { found = 0; in_atomtypes = 0 }
        tolower($0) ~ /^[[:space:]]*\\[ atomtypes \\]/ { in_atomtypes = 1; next }
        /^[[:space:]]*\\[/ { in_atomtypes = 0 }
        in_atomtypes {
            line = $0
            sub(/;.*/, "", line)
            gsub(/^[ \\t]+|[ \\t]+$/, "", line)
            split(line, fields, /[ \\t]+/)
            if (toupper(fields[1]) == target) found = 1
        }
        END { exit found ? 0 : 1 }
    ' $(topology_source_files)
}

validate_solvation_topology() {
    echo "Inspecting topol.top after gmx solvate for water and ion topology definitions."
    ensure_include "tip3_ions_atomtypes.itp"
    ensure_include "TIP3_SOL.itp"
    ensure_include "SOD.itp"
    ensure_include "CLA.itp"

    local missing=()
    for molecule_name in SOL SOD CLA; do
        if ! has_moleculetype "${molecule_name}"; then
            missing+=("[ moleculetype ] ${molecule_name}")
        fi
    done
    for atom_type in OT HT SOD CLA; do
        if ! has_atomtype "${atom_type}"; then
            missing+=("[ atomtypes ] ${atom_type}")
        fi
    done

    if (( ${#missing[@]} > 0 )); then
        echo "ERROR: topol.top is missing water/ion topology parameters required before ions.grompp:" >&2
        printf '  - %s\\n' "${missing[@]}" >&2
        echo "Expected the spc216.gro solvent route to use local includes: tip3_ions_atomtypes.itp, TIP3_SOL.itp, SOD.itp, CLA.itp." >&2
        exit 1
    fi
    echo "topol.top contains required SOL/SOD/CLA molecule definitions and OT/HT/SOD/CLA atom types."
}

validate_coordinate_topology_counts() {
    local coordinate_count
    coordinate_count="$(sed -n '2p' step5_input.gro | tr -d '[:space:]')"
    echo "Final step5_input.gro atom count: ${coordinate_count}"
    echo "Final topol.top [ molecules ] section:"
    awk '
        BEGIN { in_molecules = 0 }
        /^[[:space:]]*;/ { next }
        /^[[:space:]]*\\[/ {
            in_molecules = (tolower($0) ~ /^[[:space:]]*\\[ molecules \\]/)
            next
        }
        in_molecules && NF >= 2 { print "  " $1, $2 }
    ' topol.top
}

SOLVENT_GROUP="SOL"
ION_CONCENTRATION_MOLAR="__ION_CONCENTRATION__"
while (( $# > 0 )); do
    case "$1" in
        --solvent-group)
            shift
            if (( $# == 0 )); then
                echo "ERROR: --solvent-group requires a group name." >&2
                exit 2
            fi
            SOLVENT_GROUP="$1"
            ;;
        --solvent-group=*)
            SOLVENT_GROUP="${1#*=}"
            ;;
        --overwrite|--clean)
            ;;
        *)
            echo "ERROR: Unknown argument: $1" >&2
            echo "Usage: bash run_solvate_local.sh [--solvent-group SOL|--solvent-group=SOL] [--clean|--overwrite]" >&2
            exit 2
            ;;
    esac
    shift
done

# Build the real solvated GROMACS system.
# Polymer parameters are reset from dry_polymer before GROMACS solvate/genion can update local counts.
reset_from_dry_polymer
clean_generated_files
run_logged "editconf_box" "editconf_box.log" gmx editconf -f step5_input.gro -o step5_input_box.gro -c -d __BOX_PADDING__ -bt cubic
run_stdin_logged "make_ndx_box" "make_ndx_box.log" "q\\n" gmx make_ndx -f step5_input_box.gro -o index.ndx
run_logged "solvate" "solvate.log" gmx solvate -cp step5_input_box.gro -cs spc216.gro -p topol.top -o system_solvated.gro
validate_solvation_topology
run_logged "ions_grompp" "ions_grompp.log" gmx grompp -f ions.mdp -c system_solvated.gro -p topol.top -n index.ndx -o ions.tpr -maxwarn 1
run_genion_logged
run_logged "editconf_final" "editconf_final.log" gmx editconf -f system_neutralized.gro -o step5_input.gro
run_stdin_logged "make_ndx_final" "make_ndx_final.log" "q\\n" gmx make_ndx -f step5_input.gro -o index.ndx

# Validate that the solvated/ionised coordinates can enter minimisation.
validate_coordinate_topology_counts
run_logged "minim_grompp" "minim_grompp.log" gmx grompp -f step6.0_minimization.mdp -c step5_input.gro -r step5_input.gro -p topol.top -n index.ndx -o step6.0_minimization.tpr -maxwarn 1
rm -f \\#*\\# \\#*.\\#
"""
    path.write_text(
        script.replace("__BOX_PADDING__", f"{box_padding_nm:g}").replace(
            "__ION_CONCENTRATION__",
            f"{ion_concentration_molar:g}",
        )
    )
    path.chmod(path.stat().st_mode | stat.S_IXUSR)


def _ensure_topology_include(
    topology_path: Path,
    include_filename: str,
) -> None:
    include_line = f'#include "{include_filename}"'
    lines = topology_path.read_text().splitlines()
    if any(line.strip() == include_line for line in lines):
        return

    for index, line in enumerate(lines):
        if line.strip().lower() == "[ moleculetype ]":
            lines.insert(index, "")
            lines.insert(index + 1, include_line)
            lines.insert(index + 2, "")
            topology_path.write_text("\n".join(lines) + "\n")
            return

    raise ValueError(
        f"Could not insert {include_line}; no [ moleculetype ] section found in {topology_path}"
    )


def _write_solvation_topology_templates(
    output_dir: Path,
    topology_path: Path,
) -> tuple[Path, ...]:
    template_paths = _copy_solvation_templates(output_dir)
    for include_name in GROMACS_SOLVATION_TOPOLOGY_INCLUDE_NAMES:
        _ensure_topology_include(topology_path, include_name)
    return template_paths


def _read_topology_molecule_counts(topology_path: Path) -> dict[str, int]:
    molecule_counts: dict[str, int] = {}
    in_molecules_section = False
    for raw_line in topology_path.read_text().splitlines():
        line = raw_line.split(";", 1)[0].strip()
        if not line:
            continue
        if line.startswith("[") and line.endswith("]"):
            in_molecules_section = line.strip("[]").strip().lower() == "molecules"
            continue
        if not in_molecules_section:
            continue
        fields = line.split()
        if len(fields) < 2:
            continue
        try:
            molecule_counts[fields[0]] = molecule_counts.get(fields[0], 0) + int(
                fields[1]
            )
        except ValueError:
            continue
    return molecule_counts


def _topology_source_paths(topology_path: Path) -> tuple[Path, ...]:
    paths = [topology_path]
    for line in topology_path.read_text().splitlines():
        match = INCLUDE_PATTERN.match(line)
        if match is None:
            continue
        include_path = Path(match.group(1))
        if not include_path.is_absolute():
            include_path = topology_path.parent / include_path
        if include_path.exists():
            paths.append(include_path)
    return tuple(paths)


def _read_moleculetype_atom_counts(topology_path: Path) -> dict[str, int]:
    atom_counts: dict[str, int] = {}
    for source_path in _topology_source_paths(topology_path):
        current_molecule: str | None = None
        in_moleculetype = False
        in_atoms = False
        for raw_line in source_path.read_text().splitlines():
            line = raw_line.split(";", 1)[0].strip()
            if not line:
                continue
            if line.startswith("[") and line.endswith("]"):
                section_name = line.strip("[]").strip().lower()
                in_moleculetype = section_name == "moleculetype"
                in_atoms = section_name == "atoms"
                continue
            fields = line.split()
            if in_moleculetype and fields:
                current_molecule = fields[0]
                atom_counts.setdefault(current_molecule, 0)
                in_moleculetype = False
                continue
            if in_atoms and current_molecule is not None and fields:
                try:
                    int(fields[0])
                except ValueError:
                    continue
                atom_counts[current_molecule] = atom_counts.get(current_molecule, 0) + 1
    return atom_counts


def count_gro_atoms(gro_path: str | Path) -> int:
    """Read the atom count from the second line of a GROMACS ``.gro`` file."""

    path = Path(gro_path)
    lines = path.read_text().splitlines()
    if len(lines) < 2:
        raise ValueError(f"GRO file is too short to contain an atom count: {path}")
    try:
        return int(lines[1].strip())
    except ValueError as exc:
        raise ValueError(f"Could not parse GRO atom count from {path}") from exc


def validate_gromacs_coordinate_topology_counts(
    output_dir: str | Path,
    *,
    coordinate_name: str = "step5_input.gro",
    topology_name: str = "topol.top",
) -> GromacsCoordinateTopologyValidation:
    """Compare final coordinate atoms with topology molecule atom counts."""

    output_path = Path(output_dir)
    gro_path = output_path / coordinate_name
    topology_path = output_path / topology_name
    if not gro_path.exists():
        raise FileNotFoundError(f"GROMACS coordinate file not found: {gro_path}")
    if not topology_path.exists():
        raise FileNotFoundError(f"GROMACS topology not found: {topology_path}")

    coordinate_atom_count = count_gro_atoms(gro_path)
    molecule_counts = _read_topology_molecule_counts(topology_path)
    molecule_atom_counts = _read_moleculetype_atom_counts(topology_path)
    expected_atom_count: int | None = 0
    for molecule_name, molecule_count in molecule_counts.items():
        atom_count = molecule_atom_counts.get(molecule_name)
        if atom_count is None:
            expected_atom_count = None
            break
        expected_atom_count += molecule_count * atom_count

    return GromacsCoordinateTopologyValidation(
        gro_path=gro_path,
        topol_top_path=topology_path,
        coordinate_atom_count=coordinate_atom_count,
        molecule_counts=molecule_counts,
        molecule_atom_counts=molecule_atom_counts,
        expected_atom_count=expected_atom_count,
    )


def _sum_named_molecule_counts(
    molecule_counts: dict[str, int],
    names: tuple[str, ...],
) -> int:
    normalised_names = {name.upper() for name in names}
    return sum(
        count for name, count in molecule_counts.items() if name.upper() in normalised_names
    )


def _resolve_solvated_polymer_dir(output_dir: str | Path) -> Path:
    output_path = Path(output_dir)
    if output_path.name == "solvated_polymer":
        return output_path
    dry_dir = output_path / "dry_polymer"
    if dry_dir.exists() or output_path.name == "gromacs":
        return output_path / "solvated_polymer"
    return output_path


def _populate_solvated_polymer_inputs(output_path: Path) -> None:
    if output_path.name != "solvated_polymer":
        return
    dry_dir = output_path.parent / "dry_polymer"
    if not dry_dir.exists():
        return
    _copy_workflow_inputs(dry_dir, output_path, overwrite=True)
    for template_name in GROMACS_POLYMER_MDP_TEMPLATE_NAMES:
        source = dry_dir / template_name
        destination = output_path / template_name
        if source.exists() and not destination.exists():
            shutil.copy2(source, destination)


def _clean_solvated_polymer_generated_files(output_path: Path) -> None:
    for filename in (
        "step5_input_box.gro",
        "step5_solvated.gro",
        "step5_ions.gro",
        "genion.tpr",
        "mdout.mdp",
        "editconf.log",
        "minim_grompp_check.log",
        "editconf_box.log",
        "make_ndx_box.log",
        "solvate.log",
        "ions_grompp.log",
        "genion.log",
        "editconf_final.log",
        "make_ndx_final.log",
        "minim_grompp.log",
    ):
        (output_path / filename).unlink(missing_ok=True)
    for pattern in (
        "step6.0_minimization.*",
        "#*#",
        "#*.#",
    ):
        for path in output_path.glob(pattern):
            if path.name == "step6.0_minimization.mdp":
                continue
            if path.is_file():
                path.unlink()


def write_gromacs_solvation_files(
    output_dir: str | Path,
    *,
    workflow_type: str = "polymer",
    box_padding_nm: float = 1.2,
    ion_concentration_molar: float = 0.15,
    clean: bool = False,
    overwrite: bool = False,
) -> GromacsSolvationFiles:
    """Write files for the standard GROMACS solvate/genion workflow.

    This keeps the polymer GAFF2 topology unchanged and only adds the simulation
    environment: box, TIP3P-compatible water from GROMACS, and neutralising NaCl ions.
    """

    if workflow_type not in GROMACS_WORKFLOW_MDP_TEMPLATE_NAMES:
        valid = ", ".join(sorted(GROMACS_WORKFLOW_MDP_TEMPLATE_NAMES))
        raise ValueError(f"workflow_type must be one of: {valid}")

    output_path = _resolve_solvated_polymer_dir(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    if clean or overwrite:
        _clean_solvated_polymer_generated_files(output_path)
    _populate_solvated_polymer_inputs(output_path)

    topology_path = output_path / "topol.top"
    if not topology_path.exists():
        raise FileNotFoundError(f"GROMACS topology not found: {topology_path}")

    solvation_itp_paths = _write_solvation_topology_templates(
        output_path,
        topology_path,
    )
    ions_mdp_path = output_path / "ions.mdp"
    solvate_script_path = output_path / "run_solvate_local.sh"
    local_script_path = output_path / "run_step6_local.sh"
    hpc_script_path = output_path / "run_hpc_equilibration_production.slurm"

    _write_solvate_script(
        solvate_script_path,
        box_padding_nm=box_padding_nm,
        ion_concentration_molar=ion_concentration_molar,
    )
    _write_local_minimization_script(local_script_path)
    _write_hpc_equilibration_script(
        hpc_script_path,
        job_name=_infer_polymer_hpc_job_name(output_path),
        workflow_type=workflow_type,
    )

    return GromacsSolvationFiles(
        output_dir=output_path,
        ions_mdp_path=ions_mdp_path,
        solvation_itp_paths=solvation_itp_paths,
        solvent_itp_path=output_path / "TIP3_SOL.itp",
        cation_itp_path=output_path / "SOD.itp",
        anion_itp_path=output_path / "CLA.itp",
        solvate_script_path=solvate_script_path,
        local_script_path=local_script_path,
        hpc_script_path=hpc_script_path,
        charmm_gui_membrane_hpc_script_path=output_path.parent
        / "charmm_gui_membrane"
        / "run_hpc_charmm_gui_membrane.slurm",
    )


def validate_gromacs_solvated_topology(
    output_dir: str | Path,
    *,
    topology_name: str = "topol.top",
) -> GromacsSolvatedTopologyValidation:
    """Validate that topology molecule counts include solvent and ions."""

    topol_top_path = Path(output_dir) / topology_name
    if not topol_top_path.exists():
        raise FileNotFoundError(f"GROMACS topology not found: {topol_top_path}")
    molecule_counts = _read_topology_molecule_counts(topol_top_path)
    return GromacsSolvatedTopologyValidation(
        topol_top_path=topol_top_path,
        molecule_counts=molecule_counts,
        water_count=_sum_named_molecule_counts(molecule_counts, WATER_MOLECULE_NAMES),
        cation_count=_sum_named_molecule_counts(molecule_counts, CATION_MOLECULE_NAMES),
        anion_count=_sum_named_molecule_counts(
            molecule_counts,
            ANION_MOLECULE_NAMES,
        ),
    )


def validate_gromacs_solvation_grompp(
    output_dir: str | Path,
    *,
    gmx_command: str = "gmx",
    runner=subprocess.run,
) -> tuple[GromacsGromppValidation, GromacsGromppValidation]:
    """Run the two ``grompp`` checks required by the solvation workflow."""

    output_path = Path(output_dir)
    commands = (
        (
            gmx_command,
            "grompp",
            "-f",
            "ions.mdp",
            "-c",
            "system_solvated.gro",
            "-p",
            "topol.top",
            "-n",
            "index.ndx",
            "-o",
            "ions.tpr",
            "-maxwarn",
            "1",
        ),
        (
            gmx_command,
            "grompp",
            "-f",
            "step6.0_minimization.mdp",
            "-c",
            "step5_input.gro",
            "-r",
            "step5_input.gro",
            "-p",
            "topol.top",
            "-n",
            "index.ndx",
            "-o",
            "step6.0_minimization.tpr",
        ),
    )
    validations: list[GromacsGromppValidation] = []
    for command in commands:
        result = runner(
            list(command),
            cwd=output_path,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        validations.append(
            GromacsGromppValidation(
                command=command,
                returncode=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
            )
        )
    return tuple(validations)  # type: ignore[return-value]


def validate_gromacs_run_folder(
    output_dir: str | Path,
    *,
    topology_name: str = "topol.top",
) -> GromacsTopologyValidation:
    """Validate external include files referenced by a GROMACS topology.

    ParmEd GAFF2 conversion often writes a standalone topology with all molecule
    definitions in ``topol.top``. In that case there are no ``#include`` lines
    and no ``toppar`` directory is required.
    """

    output_path = Path(output_dir)
    topol_top_path = output_path / topology_name
    if not topol_top_path.exists():
        raise FileNotFoundError(f"GROMACS topology not found: {topol_top_path}")

    included_files: list[Path] = []
    for line in topol_top_path.read_text().splitlines():
        match = INCLUDE_PATTERN.match(line)
        if match is None:
            continue
        include_path = Path(match.group(1))
        if not include_path.is_absolute():
            include_path = output_path / include_path
        included_files.append(include_path)

    missing_files = tuple(path for path in included_files if not path.exists())
    return GromacsTopologyValidation(
        topol_top_path=topol_top_path,
        is_standalone=not included_files,
        included_files=tuple(included_files),
        missing_files=missing_files,
    )


def check_gromacs_minimization_inputs(
    output_dir: str | Path,
) -> GromacsLocalMinimizationCheck:
    """Check the files needed before running local GROMACS minimisation."""

    output_path = Path(output_dir).expanduser().resolve()
    required_files = tuple(
        output_path / filename for filename in LOCAL_MINIMIZATION_REQUIRED_FILENAMES
    )
    missing_files = tuple(path for path in required_files if not path.exists())
    return GromacsLocalMinimizationCheck(
        output_dir=output_path,
        required_files=required_files,
        missing_files=missing_files,
        command=("bash", "run_step6_local.sh"),
    )


def run_gromacs_local_minimization(
    output_dir: str | Path,
    *,
    runner=subprocess.run,
) -> subprocess.CompletedProcess:
    """Run the local minimisation script from inside the GROMACS folder."""

    check = check_gromacs_minimization_inputs(output_dir)
    if not check.ready:
        missing = ", ".join(str(path) for path in check.missing_files)
        raise FileNotFoundError(
            f"Cannot run GROMACS minimisation; missing files: {missing}"
        )

    result = runner(
        list(check.command),
        cwd=check.output_dir,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise RuntimeError(
            "GROMACS local minimisation failed with return code "
            f"{result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return result


def prepare_gromacs_run_folder(
    prmtop_file: str | Path,
    inpcrd_file: str | Path,
    output_dir: str | Path,
    system_name: str,
    *,
    workflow_type: str = "polymer",
    index_file: str | Path | None = None,
    gmx_command: str = "gmx",
    runner=subprocess.run,
) -> GromacsPreparedRunFolder:
    """Prepare self-contained GROMACS workflow folders from AMBER files.

    ``output_dir`` is the system-level ``gromacs`` directory. This function
    writes independent ``dry_polymer``, ``solvated_polymer`` and
    ``charmm_gui_membrane`` subdirectories so one workflow cannot overwrite
    another workflow's inputs or outputs.
    """

    if not system_name.strip():
        raise ValueError("system_name must be a non-empty string")
    if workflow_type not in GROMACS_WORKFLOW_MDP_TEMPLATE_NAMES:
        valid = ", ".join(sorted(GROMACS_WORKFLOW_MDP_TEMPLATE_NAMES))
        raise ValueError(f"workflow_type must be one of: {valid}")

    output_path = Path(output_dir)
    dry_polymer_dir = output_path / "dry_polymer"
    solvated_polymer_dir = output_path / "solvated_polymer"
    charmm_gui_membrane_dir = output_path / "charmm_gui_membrane"
    dry_polymer_dir.mkdir(parents=True, exist_ok=True)
    solvated_polymer_dir.mkdir(parents=True, exist_ok=True)
    charmm_gui_membrane_dir.mkdir(parents=True, exist_ok=True)

    converted = convert_amber_to_gromacs(
        str(prmtop_file),
        str(inpcrd_file),
        str(dry_polymer_dir),
        system_name,
    )
    topol_top_path = dry_polymer_dir / "topol.top"
    raw_step5_input_gro_path = dry_polymer_dir / "step5_input_raw.gro"
    step5_input_gro_path = dry_polymer_dir / "step5_input.gro"
    converted.top_path.replace(topol_top_path)
    converted.gro_path.replace(raw_step5_input_gro_path)
    create_gromacs_simulation_box(
        raw_step5_input_gro_path,
        step5_input_gro_path,
        padding_nm=3.0,
        box_type="cubic",
        gmx_command=gmx_command,
        runner=runner,
    )
    raw_step5_input_gro_path.unlink(missing_ok=True)

    index_ndx_path = dry_polymer_dir / "index.ndx"
    if index_file is not None and Path(index_file).exists():
        shutil.copy2(index_file, index_ndx_path)
    else:
        _write_default_index(step5_input_gro_path, index_ndx_path)

    dry_mdp_paths = _copy_mdp_templates(
        dry_polymer_dir,
        ("step6.0_minimization.mdp",),
    )
    validate_gromacs_box_against_mdp(
        step5_input_gro_path,
        dry_polymer_dir / "step6.0_minimization.mdp",
    )
    validation = validate_gromacs_run_folder(dry_polymer_dir)
    if not validation.valid:
        missing = ", ".join(str(path) for path in validation.missing_files)
        raise FileNotFoundError(
            f"GROMACS topology includes missing files: {missing}"
        )

    local_script_path = dry_polymer_dir / "run_step6_local.sh"
    _write_local_minimization_script(local_script_path)

    _copy_workflow_inputs(dry_polymer_dir, solvated_polymer_dir)
    solvated_mdp_paths = _copy_mdp_templates(
        solvated_polymer_dir,
        GROMACS_POLYMER_MDP_TEMPLATE_NAMES,
    )
    solvated_local_script_path = solvated_polymer_dir / "run_step6_local.sh"
    hpc_script_path = solvated_polymer_dir / "run_hpc_equilibration_production.slurm"
    _write_local_minimization_script(solvated_local_script_path)
    _write_hpc_equilibration_script(
        hpc_script_path,
        job_name=system_name,
        workflow_type="polymer",
    )

    _copy_workflow_inputs(dry_polymer_dir, charmm_gui_membrane_dir)
    charmm_mdp_paths = _copy_mdp_templates(
        charmm_gui_membrane_dir,
        GROMACS_CHARMM_GUI_MEMBRANE_MDP_TEMPLATE_NAMES,
    )
    charmm_local_script_path = charmm_gui_membrane_dir / "run_step6_local.sh"
    charmm_gui_membrane_hpc_script_path = (
        charmm_gui_membrane_dir / "run_hpc_charmm_gui_membrane.slurm"
    )
    _write_local_minimization_script(charmm_local_script_path)
    _write_hpc_equilibration_script(
        charmm_gui_membrane_hpc_script_path,
        job_name=f"{system_name}_charmm_gui_membrane",
        workflow_type="charmm_gui_membrane",
    )

    return GromacsPreparedRunFolder(
        output_dir=output_path,
        workflow_type=workflow_type,
        dry_polymer_dir=dry_polymer_dir,
        solvated_polymer_dir=solvated_polymer_dir,
        charmm_gui_membrane_dir=charmm_gui_membrane_dir,
        step5_input_gro_path=step5_input_gro_path,
        topol_top_path=topol_top_path,
        index_ndx_path=index_ndx_path,
        mdp_paths=dry_mdp_paths + solvated_mdp_paths + charmm_mdp_paths,
        local_script_path=local_script_path,
        hpc_script_path=(
            charmm_gui_membrane_hpc_script_path
            if workflow_type == "charmm_gui_membrane"
            else hpc_script_path
        ),
        charmm_gui_membrane_hpc_script_path=charmm_gui_membrane_hpc_script_path,
    )
