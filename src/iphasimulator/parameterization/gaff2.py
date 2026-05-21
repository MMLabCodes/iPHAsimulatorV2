"""GAFF2 parameterisation workflow using AmberTools."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil
import shlex
import subprocess
import time
from collections.abc import Sequence

from rdkit import Chem

from iphasimulator.export import prepare_molecule_3d


@dataclass(frozen=True)
class Gaff2Outputs:
    """Files produced by the GAFF2/AmberTools workflow."""

    output_dir: Path
    mol2_path: Path
    frcmod_path: Path
    tleap_input_path: Path
    prmtop_path: Path
    inpcrd_path: Path
    pdb_path: Path
    antechamber_log: Path
    raw_antechamber_log: Path
    sqm_log: Path
    parmchk2_log: Path
    tleap_log: Path
    timing_log: Path
    antechamber_seconds: float
    parmchk2_seconds: float
    tleap_seconds: float


class AmberToolsError(RuntimeError):
    """Raised when AmberTools is unavailable or a command fails."""


def ambertools_available() -> bool:
    """Return True when the required AmberTools executables are on PATH."""

    return all(shutil.which(command) for command in ("antechamber", "parmchk2", "tleap"))


def require_ambertools() -> None:
    """Raise a clear error if AmberTools executables are not available."""

    missing = [
        command
        for command in ("antechamber", "parmchk2", "tleap")
        if shutil.which(command) is None
    ]
    if missing:
        raise AmberToolsError(
            "AmberTools executables not found on PATH: " + ", ".join(missing)
        )


def _run_command(
    command: Sequence[str],
    cwd: Path,
    log_path: Path,
    *,
    stage_name: str,
    raw_log_path: Path | None = None,
    verbose: bool = False,
    runner=subprocess.run,
) -> float:
    command_text = shlex.join(command)
    if verbose:
        print(f"[GAFF2:{stage_name}] Running: {command_text}")

    start = time.perf_counter()
    result = runner(
        list(command),
        cwd=str(cwd),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    elapsed_seconds = time.perf_counter() - start

    output = result.stdout or ""
    if raw_log_path is not None:
        raw_log_path.write_text(output)
        log_path.write_text(
            "\n".join(
                [
                    f"Stage: {stage_name}",
                    f"Command: {command_text}",
                    f"Working directory: {cwd}",
                    f"Elapsed seconds: {elapsed_seconds:.3f}",
                    f"Raw log: {raw_log_path}",
                    "",
                    output,
                ]
            )
        )
    else:
        log_path.write_text(output)

    if result.returncode != 0:
        raise AmberToolsError(
            f"Command failed with exit code {result.returncode}: {' '.join(command)}. "
            f"See {log_path}"
        )
    if verbose:
        print(f"[GAFF2:{stage_name}] Completed in {elapsed_seconds:.1f}s")
    return elapsed_seconds


def _write_tleap_input(
    path: Path,
    mol2_path: Path,
    frcmod_path: Path,
    prmtop_path: Path,
    inpcrd_path: Path,
    pdb_path: Path,
    unit_name: str,
) -> None:
    path.write_text(
        "\n".join(
            [
                "source leaprc.gaff2",
                f"loadamberparams {frcmod_path.name}",
                f"{unit_name} = loadmol2 {mol2_path.name}",
                f"check {unit_name}",
                f"saveamberparm {unit_name} {prmtop_path.name} {inpcrd_path.name}",
                f"savepdb {unit_name} {pdb_path.name}",
                "quit",
                "",
            ]
        )
    )


def _prepare_antechamber_sdf(
    input_path: Path,
    output_path: Path,
    stem: str,
) -> tuple[Path, int | None]:
    supplier = Chem.SDMolSupplier(str(input_path), removeHs=False)
    mol = next((candidate for candidate in supplier if candidate is not None), None)
    if mol is None:
        return input_path, None

    prepared_path = output_path / f"{stem}.antechamber.sdf"
    prepared = prepare_molecule_3d(mol)
    writer = Chem.SDWriter(str(prepared_path))
    try:
        writer.write(prepared)
    finally:
        writer.close()
    return prepared_path, prepared.GetNumAtoms()


def _write_timing_log(
    path: Path,
    *,
    antechamber_seconds: float,
    parmchk2_seconds: float,
    tleap_seconds: float,
) -> None:
    path.write_text(
        "\n".join(
            [
                f"antechamber_seconds={antechamber_seconds:.3f}",
                f"parmchk2_seconds={parmchk2_seconds:.3f}",
                f"tleap_seconds={tleap_seconds:.3f}",
                f"total_seconds={antechamber_seconds + parmchk2_seconds + tleap_seconds:.3f}",
                "",
            ]
        )
    )


def parameterize_gaff2(
    input_sdf: str | Path,
    output_dir: str | Path,
    *,
    name: str | None = None,
    net_charge: int = 0,
    residue_name: str = "MOL",
    charge_method: str = "bcc",
    atom_count_warning_threshold: int | None = 120,
    verbose: bool = False,
    runner=subprocess.run,
    check_tools: bool = True,
) -> Gaff2Outputs:
    """Create GAFF2 AMBER topology files from an input SDF.

    The workflow runs AmberTools in three steps:
    antechamber -> parmchk2 -> tleap.
    """

    if check_tools:
        require_ambertools()

    input_path = Path(input_sdf)
    if not input_path.exists():
        raise FileNotFoundError(f"Input SDF not found: {input_path}")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    stem = name or input_path.stem
    mol2_path = output_path / f"{stem}.gaff2.mol2"
    frcmod_path = output_path / f"{stem}.gaff2.frcmod"
    tleap_input_path = output_path / "tleap.in"
    prmtop_path = output_path / f"{stem}.prmtop"
    inpcrd_path = output_path / f"{stem}.inpcrd"
    pdb_path = output_path / f"{stem}.tleap.pdb"
    antechamber_log = output_path / "antechamber.log"
    raw_antechamber_log = output_path / "antechamber.raw.log"
    sqm_log = output_path / "sqm.raw.out"
    parmchk2_log = output_path / "parmchk2.log"
    tleap_log = output_path / "tleap.log"
    timing_log = output_path / "timing.log"
    antechamber_input_path, atom_count = _prepare_antechamber_sdf(
        input_path,
        output_path,
        stem,
    )
    if (
        atom_count_warning_threshold is not None
        and atom_count is not None
        and atom_count > atom_count_warning_threshold
    ):
        print(
            f"WARNING: {stem} has {atom_count} atoms after hydrogen addition; "
            f"AmberTools charge generation may be slow. Threshold: "
            f"{atom_count_warning_threshold} atoms."
        )

    antechamber_command = [
        "antechamber",
        "-i",
        str(antechamber_input_path.resolve()),
        "-fi",
        "sdf",
        "-o",
        mol2_path.name,
        "-fo",
        "mol2",
        "-at",
        "gaff2",
        "-c",
        charge_method,
        "-nc",
        str(net_charge),
        "-rn",
        residue_name,
        "-s",
        "2",
    ]
    generated_sqm_log = output_path / "sqm.out"
    try:
        antechamber_seconds = _run_command(
            antechamber_command,
            output_path,
            antechamber_log,
            stage_name="antechamber",
            raw_log_path=raw_antechamber_log,
            verbose=verbose,
            runner=runner,
        )
    finally:
        if generated_sqm_log.exists():
            shutil.copyfile(generated_sqm_log, sqm_log)
        elif not sqm_log.exists():
            sqm_log.write_text("sqm.out was not generated by antechamber.\n")

    parmchk2_command = [
        "parmchk2",
        "-i",
        mol2_path.name,
        "-f",
        "mol2",
        "-o",
        frcmod_path.name,
        "-s",
        "gaff2",
    ]
    parmchk2_seconds = _run_command(
        parmchk2_command,
        output_path,
        parmchk2_log,
        stage_name="parmchk2",
        verbose=verbose,
        runner=runner,
    )

    _write_tleap_input(
        tleap_input_path,
        mol2_path,
        frcmod_path,
        prmtop_path,
        inpcrd_path,
        pdb_path,
        unit_name="mol",
    )
    tleap_seconds = _run_command(
        ["tleap", "-f", tleap_input_path.name],
        output_path,
        tleap_log,
        stage_name="tleap",
        verbose=verbose,
        runner=runner,
    )
    _write_timing_log(
        timing_log,
        antechamber_seconds=antechamber_seconds,
        parmchk2_seconds=parmchk2_seconds,
        tleap_seconds=tleap_seconds,
    )

    return Gaff2Outputs(
        output_dir=output_path,
        mol2_path=mol2_path,
        frcmod_path=frcmod_path,
        tleap_input_path=tleap_input_path,
        prmtop_path=prmtop_path,
        inpcrd_path=inpcrd_path,
        pdb_path=pdb_path,
        antechamber_log=antechamber_log,
        raw_antechamber_log=raw_antechamber_log,
        sqm_log=sqm_log,
        parmchk2_log=parmchk2_log,
        tleap_log=tleap_log,
        timing_log=timing_log,
        antechamber_seconds=antechamber_seconds,
        parmchk2_seconds=parmchk2_seconds,
        tleap_seconds=tleap_seconds,
    )
