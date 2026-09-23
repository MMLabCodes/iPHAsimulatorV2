"""Detailed checks and record keeping used by workshop_helpers."""
from pathlib import Path
import os
import sys
from .workshop_helpers import check_output_files as require_files

def check_environment(workshop, CHECK_BUILD_TOOLS=True, CHECK_MELT_TOOLS=False, CHECK_ANALYSIS=False):
    PROJECT_ROOT = workshop.project
    WORKSPACE = workshop.root
    DATABASE = workshop.database
    import importlib
    import shutil
    print("Python:", sys.executable)
    print("Workshop workspace:", WORKSPACE)
    modules = ["iphasimulator", "numpy", "pandas", "rdkit", "parmed", "openmm", "openbabel.pybel", "matplotlib"]
    if CHECK_ANALYSIS:
        modules += ["MDAnalysis", "sklearn", "kneed", "scipy", "matplotlib"]
    failed = []
    for name in modules:
        try:
            importlib.import_module(name)
            print("PASS — import", name)
        except Exception as error:
            failed.append(name)
            print("FAIL —", name, error)
    commands = ["tleap"] if CHECK_BUILD_TOOLS else []
    if CHECK_MELT_TOOLS:
        commands += ["acpype", "polyply"]
    for command in commands:
        found = shutil.which(command)
        print("PASS —" if found else "FAIL —", command, found or "not on PATH")
        if not found:
            failed.append(command)
    if failed:
        raise RuntimeError("Missing requirements: " + ", ".join(failed) + ". See ../README.md.")
    print("PASS — selected requirements are importable/findable. No workload was executed.")
    return True

def check_chain(workshop, POLYMER_NAME='P3HB_10', EXPECTED_REPEAT_UNITS=10):
    PROJECT_ROOT = workshop.project
    WORKSPACE = workshop.root
    DATABASE = workshop.database
    require_files(DATABASE / "residue_codes.csv")
    from iphasimulator.pha_filepath_manager import PHAFileManager
    from openmm.app import AmberPrmtopFile, AmberInpcrdFile, PDBFile
    files = PHAFileManager(DATABASE).get_built_PHA_amber_files(POLYMER_NAME)
    require_files(files["pdb"], files["prmtop"], files["rst7"])
    topology = AmberPrmtopFile(str(files["prmtop"])).topology
    coordinates = AmberInpcrdFile(str(files["rst7"]))
    pdb = PDBFile(str(files["pdb"]))
    counts = [topology.getNumAtoms(), len(coordinates.positions), pdb.topology.getNumAtoms()]
    print("Atom counts (topology, coordinates, PDB):", counts)
    if len(set(counts)) != 1:
        raise RuntimeError("Atom counts disagree; do not use these files together.")
    residues = list(topology.residues())
    if len(residues) != EXPECTED_REPEAT_UNITS:
        raise RuntimeError(f"Expected {EXPECTED_REPEAT_UNITS} residues, found {len(residues)}.")
    print("PASS — atom counts and expected repeat-unit count agree.")
    print("Residue sequence:", " ".join(r.name for r in residues))
    print("VISUAL CHECK STILL REQUIRED —", files["pdb"])
    return files

def record_run(workshop, SYSTEM_NAME='P3HB_10_dry', SIMULATION_NAME='workshop_short_01', WORKFLOW_NAME='workshop_short', HASH_TRAJECTORIES=False, WRITE_RECORD=True):
    PROJECT_ROOT = workshop.project
    WORKSPACE = workshop.root
    DATABASE = workshop.database
    import hashlib
    import json
    import platform
    import subprocess
    from datetime import datetime, timezone
    from importlib.metadata import version, PackageNotFoundError
    require_files(DATABASE / "residue_codes.csv")
    from iphasimulator.pha_filepath_manager import PHAFileManager
    paths = PHAFileManager(DATABASE)
    row = paths.get_md_system(SYSTEM_NAME)
    files = paths.validate_md_system_files(SYSTEM_NAME, row["system_type"])
    run = files["simulations_dir"] / SIMULATION_NAME
    if not run.is_dir():
        raise RuntimeError(f"Simulation directory is missing: {run}")
    definition = files["workflows_dir"] / f"{WORKFLOW_NAME}.workflow.json"
    script = WORKSPACE / "md_simulation_scripts" / f"{WORKFLOW_NAME}.py"
    require_files(definition, script)
    if not WRITE_RECORD:
        print("SKIPPED — set WRITE_RECORD = True to save a provenance record for", run)
        return
    def checksum(path):
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for block in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(block)
        return digest.hexdigest()
    selected = [files["topology_file"], files["coordinate_file"], definition, script]
    selected += sorted(p for p in run.rglob("*") if p.is_file())
    records = []
    for path in selected:
        large_trajectory = path.suffix.lower() in {".dcd", ".xtc", ".trr"}
        records.append({"path": str(path.relative_to(WORKSPACE)), "bytes": path.stat().st_size,
                        "sha256": checksum(path) if HASH_TRAJECTORIES or not large_trajectory else None})
    versions = {}
    for package in ("iphasimulator", "openmm", "parmed", "rdkit", "numpy", "MDAnalysis", "scikit-learn", "kneed"):
        try:
            versions[package] = version(package)
        except PackageNotFoundError:
            versions[package] = "not installed as a distribution"
    def git_output(arguments):
        try:
            result = subprocess.run(["git", "--no-optional-locks", *arguments], cwd=PROJECT_ROOT, capture_output=True, text=True)
            return result.stdout.strip() if result.returncode == 0 else "unavailable"
        except OSError:
            return "unavailable"
    record = {"recorded_at_utc": datetime.now(timezone.utc).isoformat(), "system": row,
              "simulation": SIMULATION_NAME, "python": sys.version, "python_executable": sys.executable,
              "platform": platform.platform(), "package_versions": versions,
              "source_commit": git_output(["rev-parse", "HEAD"]),
              "source_working_tree_status": git_output(["status", "--short"]),
              "workflow": json.loads(definition.read_text()), "files": records,
              "limitations": "Does not prove this protocol generated these outputs. Dirty source changes and external-tool versions must be preserved separately."}
    destination = WORKSPACE / "study_records"
    destination.mkdir(parents=True, exist_ok=True)
    output = destination / (SIMULATION_NAME + "_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + ".json")
    with output.open("x") as handle:
        json.dump(record, handle, indent=2)
    print("PASS — wrote provenance snapshot:", output)
    return output

