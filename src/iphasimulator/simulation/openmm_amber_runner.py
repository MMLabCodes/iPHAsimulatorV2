"""OpenMM runner for AMBER topology files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import time


@dataclass(frozen=True)
class OpenMMOutputs:
    """Files produced by an OpenMM AMBER-topology run."""

    output_dir: Path
    minimized_pdb_path: Path
    trajectory_path: Path
    state_xml_path: Path
    log_path: Path
    nvt_trajectory_path: Path
    nvt_log_path: Path
    npt_trajectory_path: Path
    npt_log_path: Path
    production_trajectory_path: Path
    production_log_path: Path
    final_pdb_path: Path
    summary_log_path: Path


@dataclass(frozen=True)
class OpenMMStageTimings:
    """Wall-clock timings for an OpenMM AMBER workflow."""

    minimization_seconds: float
    nvt_seconds: float
    npt_seconds: float
    production_seconds: float


class OpenMMRunnerError(RuntimeError):
    """Raised when OpenMM is unavailable or simulation setup fails."""


def openmm_available() -> bool:
    """Return True when OpenMM can be imported."""

    try:
        import openmm  # noqa: F401
        import openmm.app  # noqa: F401
    except ImportError:
        return False
    return True


def _platform(mm, platform_name: str | None, precision: str | None):
    if platform_name is None:
        return None
    platform = mm.Platform.getPlatformByName(platform_name)
    if precision is not None:
        try:
            platform.setPropertyDefaultValue("Precision", precision)
        except Exception:
            pass
    return platform


def _simulation(app, topology, system, integrator, platform):
    if platform is None:
        return app.Simulation(topology, system, integrator)
    return app.Simulation(topology, system, integrator, platform)


def _write_pdb(app, topology, positions, output_path: Path) -> None:
    with output_path.open("w") as handle:
        app.PDBFile.writeFile(topology, positions, handle)


def _append_stage_reporters(
    app,
    simulation,
    trajectory_path: Path,
    log_path: Path,
    interval: int,
    *,
    total_steps: int,
    include_box_data: bool,
) -> None:
    simulation.reporters.append(app.DCDReporter(str(trajectory_path), interval))
    simulation.reporters.append(
        app.StateDataReporter(
            str(log_path),
            interval,
            step=True,
            potentialEnergy=True,
            kineticEnergy=True,
            totalEnergy=True,
            temperature=True,
            volume=include_box_data,
            density=include_box_data,
            speed=True,
            remainingTime=True,
            totalSteps=total_steps,
            separator=",",
        )
    )


def _run_stage(simulation, steps: int) -> float:
    start = time.perf_counter()
    if steps > 0:
        simulation.step(steps)
    return time.perf_counter() - start


def _write_summary(path: Path, *, timings: OpenMMStageTimings, npt_ran: bool) -> None:
    path.write_text(
        "\n".join(
            [
                f"minimization_seconds={timings.minimization_seconds:.3f}",
                f"nvt_seconds={timings.nvt_seconds:.3f}",
                f"npt_seconds={timings.npt_seconds:.3f}",
                f"production_seconds={timings.production_seconds:.3f}",
                f"npt_ran={npt_ran}",
                "",
            ]
        )
    )


def _temperature_schedule(
    *,
    start_kelvin: float,
    target_kelvin: float,
    increment_kelvin: float,
) -> list[float]:
    """Return inclusive thermal-ramp temperatures."""

    if increment_kelvin <= 0:
        raise ValueError("Temperature increment must be positive")
    if start_kelvin == target_kelvin:
        return [start_kelvin]

    direction = 1.0 if target_kelvin > start_kelvin else -1.0
    temperatures = [start_kelvin]
    current = start_kelvin
    while (current + direction * increment_kelvin - target_kelvin) * direction < 0:
        current += direction * increment_kelvin
        temperatures.append(current)
    if temperatures[-1] != target_kelvin:
        temperatures.append(target_kelvin)
    return temperatures


def run_openmm_with_amber_topology(
    prmtop_path: str | Path,
    inpcrd_path: str | Path,
    output_dir: str | Path,
    *,
    temperature_kelvin: float = 300.0,
    friction_per_picosecond: float = 1.0,
    timestep_femtoseconds: float = 2.0,
    minimization_max_iterations: int = 200,
    simulation_steps: int = 100,
    nvt_steps: int | None = None,
    npt_steps: int = 100,
    production_steps: int = 100,
    report_interval: int = 10,
    pressure_bar: float = 1.0,
    nonbonded_cutoff_nanometers: float = 1.0,
    platform_name: str | None = None,
    platform_precision: str | None = "mixed",
) -> OpenMMOutputs:
    """Run minimization, NVT, NPT when periodic, and production from AMBER files."""

    try:
        import openmm as mm
        from openmm import app, unit
        from openmm import XmlSerializer
    except ImportError as exc:
        raise OpenMMRunnerError(
            "OpenMM is not installed. Install OpenMM before running Stage 2."
        ) from exc

    prmtop = Path(prmtop_path)
    inpcrd = Path(inpcrd_path)
    if not prmtop.exists():
        raise FileNotFoundError(f"AMBER topology not found: {prmtop}")
    if not inpcrd.exists():
        raise FileNotFoundError(f"AMBER coordinates not found: {inpcrd}")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    minimized_pdb_path = output_path / "minimized.pdb"
    trajectory_path = output_path / "production.dcd"
    state_xml_path = output_path / "state.xml"
    log_path = output_path / "production.log"
    nvt_trajectory_path = output_path / "nvt.dcd"
    nvt_log_path = output_path / "nvt.log"
    npt_trajectory_path = output_path / "npt.dcd"
    npt_log_path = output_path / "npt.log"
    production_trajectory_path = output_path / "production.dcd"
    production_log_path = output_path / "production.log"
    final_pdb_path = output_path / "final.pdb"
    summary_log_path = output_path / "openmm_summary.log"

    amber_prmtop = app.AmberPrmtopFile(str(prmtop))
    amber_inpcrd = app.AmberInpcrdFile(str(inpcrd))
    is_periodic = amber_inpcrd.boxVectors is not None
    nonbonded_method = app.PME if is_periodic else app.NoCutoff
    nvt_steps = simulation_steps if nvt_steps is None else nvt_steps
    platform = _platform(mm, platform_name, platform_precision)

    def create_system(*, with_barostat: bool):
        system = amber_prmtop.createSystem(
            nonbondedMethod=nonbonded_method,
            nonbondedCutoff=nonbonded_cutoff_nanometers * unit.nanometers,
            constraints=app.HBonds,
        )
        if with_barostat:
            system.addForce(
                mm.MonteCarloBarostat(
                    pressure_bar * unit.bar,
                    temperature_kelvin * unit.kelvin,
                )
            )
        return system

    def create_integrator():
        return mm.LangevinMiddleIntegrator(
            temperature_kelvin * unit.kelvin,
            friction_per_picosecond / unit.picosecond,
            timestep_femtoseconds * unit.femtoseconds,
        )

    def set_initial_context(simulation) -> None:
        if is_periodic:
            simulation.context.setPeriodicBoxVectors(*amber_inpcrd.boxVectors)
        simulation.context.setPositions(amber_inpcrd.positions)

    simulation = _simulation(
        app,
        amber_prmtop.topology,
        create_system(with_barostat=False),
        create_integrator(),
        platform,
    )
    set_initial_context(simulation)
    min_start = time.perf_counter()
    simulation.minimizeEnergy(maxIterations=minimization_max_iterations)
    minimization_seconds = time.perf_counter() - min_start
    state = simulation.context.getState(getPositions=True, getEnergy=True)
    _write_pdb(app, amber_prmtop.topology, state.getPositions(), minimized_pdb_path)

    simulation.context.setVelocitiesToTemperature(temperature_kelvin * unit.kelvin)
    _append_stage_reporters(
        app,
        simulation,
        nvt_trajectory_path,
        nvt_log_path,
        report_interval,
        total_steps=nvt_steps,
        include_box_data=is_periodic,
    )
    nvt_seconds = _run_stage(simulation, nvt_steps)

    state = simulation.context.getState(getPositions=True, getVelocities=True, getEnergy=True)
    positions = state.getPositions()
    velocities = state.getVelocities()
    box_vectors = state.getPeriodicBoxVectors() if is_periodic else None

    npt_ran = is_periodic and npt_steps > 0
    if npt_ran:
        npt_simulation = _simulation(
            app,
            amber_prmtop.topology,
            create_system(with_barostat=True),
            create_integrator(),
            platform,
        )
        npt_simulation.context.setPeriodicBoxVectors(*box_vectors)
        npt_simulation.context.setPositions(positions)
        npt_simulation.context.setVelocities(velocities)
        _append_stage_reporters(
            app,
            npt_simulation,
            npt_trajectory_path,
            npt_log_path,
            report_interval,
            total_steps=npt_steps,
            include_box_data=True,
        )
        npt_seconds = _run_stage(npt_simulation, npt_steps)
        simulation = npt_simulation
        state = simulation.context.getState(getPositions=True, getVelocities=True, getEnergy=True)
        positions = state.getPositions()
        velocities = state.getVelocities()
        box_vectors = state.getPeriodicBoxVectors()
    else:
        npt_seconds = 0.0
        npt_log_path.write_text(
            "NPT skipped: AMBER coordinates do not contain periodic box vectors.\n"
            if not is_periodic
            else "NPT skipped: npt_steps is 0.\n"
        )

    production_simulation = _simulation(
        app,
        amber_prmtop.topology,
        create_system(with_barostat=is_periodic),
        create_integrator(),
        platform,
    )
    if is_periodic:
        production_simulation.context.setPeriodicBoxVectors(*box_vectors)
    production_simulation.context.setPositions(positions)
    production_simulation.context.setVelocities(velocities)
    _append_stage_reporters(
        app,
        production_simulation,
        production_trajectory_path,
        production_log_path,
        report_interval,
        total_steps=production_steps,
        include_box_data=is_periodic,
    )
    production_seconds = _run_stage(production_simulation, production_steps)

    final_state = production_simulation.context.getState(
        getPositions=True,
        getVelocities=True,
        getEnergy=True,
    )
    _write_pdb(app, amber_prmtop.topology, final_state.getPositions(), final_pdb_path)
    state_xml_path.write_text(XmlSerializer.serialize(final_state))

    timings = OpenMMStageTimings(
        minimization_seconds=minimization_seconds,
        nvt_seconds=nvt_seconds,
        npt_seconds=npt_seconds,
        production_seconds=production_seconds,
    )
    _write_summary(summary_log_path, timings=timings, npt_ran=npt_ran)

    return OpenMMOutputs(
        output_dir=output_path,
        minimized_pdb_path=minimized_pdb_path,
        trajectory_path=trajectory_path,
        state_xml_path=state_xml_path,
        log_path=log_path,
        nvt_trajectory_path=nvt_trajectory_path,
        nvt_log_path=nvt_log_path,
        npt_trajectory_path=npt_trajectory_path,
        npt_log_path=npt_log_path,
        production_trajectory_path=production_trajectory_path,
        production_log_path=production_log_path,
        final_pdb_path=final_pdb_path,
        summary_log_path=summary_log_path,
    )
