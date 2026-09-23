"""Shared workshop setup, checks and presentation. No package code is changed.

Learners use the short lessons in core/ and advanced/. Imports here are lazy so
that environment diagnostics and source inspection work without scientific tools.
"""
from pathlib import Path
from types import SimpleNamespace
import importlib
import json
import os
import shutil
import sys


def check_output_files(*paths):
    """Require nonempty files and print their locations; no scientific claim."""
    for value in paths:
        path = Path(value)
        if not path.is_file() or path.stat().st_size == 0:
            raise RuntimeError(f"Missing or empty file: {path}")
        print("File found:", path)
    return tuple(Path(p) for p in paths)


def _name(value):
    if not value or value in {".", ".."} or Path(value).name != value or "\\" in value:
        raise ValueError("Use a name without directory separators: " + repr(value))
    return value


def _inside(workshop, path):
    path = Path(path).resolve()
    if not path.is_relative_to(workshop.root):
        raise RuntimeError("Use a copy inside the workshop, not a link to research files.")
    return path


def _new(path):
    if Path(path).exists():
        raise RuntimeError(f"Output already exists: {path}. Inspect it or choose a new name; it will not be replaced.")


def prepare_workshop(*, modules=(), commands=(), require_database=True):
    """Locate the checkout/workspace and check only this lesson's dependencies."""
    if sys.version_info < (3, 10):
        raise RuntimeError("Use Python 3.10 or newer in the scientific environment.")
    project = Path(__file__).resolve().parents[2]
    for path in (project, project / "src"):
        if str(path) not in sys.path:
            sys.path.insert(0, str(path))
    root = Path(os.environ.get("IPHA_WORKSHOP", str(Path.home() / "iphasimulator_workshop"))).expanduser().resolve()
    if root == project or root.is_relative_to(project / "structure_database"):
        raise RuntimeError("Choose a separate workshop directory; see tutorials/README.md.")
    workshop = SimpleNamespace(project=project, root=root, database=root / "structure_database")
    _inside(workshop, workshop.database)
    if require_database:
        check_output_files(workshop.database / "residue_codes.csv")
    for module in modules:
        try:
            importlib.import_module(module)
        except Exception as error:
            raise RuntimeError(f"Cannot load {module}. Activate the scientific environment; see tutorials/README.md. Details: {error}") from error
    for command in commands:
        if not shutil.which(command):
            raise RuntimeError(f"Cannot find {command}. Activate the scientific environment; see tutorials/README.md.")
    print("Python:", sys.executable)
    print("Workshop:", root)
    return workshop


def check_environment(workshop, *, build_tools=True, melt_tools=False, analysis=False):
    from .records_and_checks import check_environment as check
    return check(workshop, CHECK_BUILD_TOOLS=build_tools, CHECK_MELT_TOOLS=melt_tools, CHECK_ANALYSIS=analysis)


def create_workshop(workshop):
    """Copy supplied 3HB inputs once, preserving an existing workspace."""
    source = workshop.project / "structure_database"
    relative = ["residue_codes.csv", "PHA_types/3HB/trimer/P3HB_3.frcmod"]
    relative += [f"PHA_types/3HB/monomer_units/{part}P3HB.prepin" for part in "hmt"]
    check_output_files(*(source / p for p in relative))
    if not workshop.database.exists():
        workshop.database.mkdir(parents=True)
        shutil.copy2(source / "residue_codes.csv", workshop.database / "residue_codes.csv")
        shutil.copytree(source / "PHA_types/3HB", workshop.database / "PHA_types/3HB")
    else:
        print("Using existing workshop inputs; no chemistry files were replaced.")
    check_output_files(*(workshop.database / p for p in relative))
    from iphasimulator.pha_filepath_manager import PHAFileManager
    PHAFileManager(workshop.database)
    return workshop.database


def check_chemistry(workshop, chemistry):
    import csv
    _name(chemistry)
    with (workshop.database / "residue_codes.csv").open() as handle:
        rows = [r for r in csv.DictReader(handle) if r["PHA_type"] == chemistry]
    if not {"head", "mainchain", "tail"} <= {r["component"] for r in rows}:
        raise RuntimeError("Missing registered residue roles for " + chemistry)
    from iphasimulator.pha_filepath_manager import PHAFileManager
    files = PHAFileManager(workshop.database).get_PHA_monomer_unit_files(chemistry)
    check_output_files(*(files[k] for k in ("head_prepin", "mainchain_prepin", "tail_prepin", "frcmod")))
    print("Building-block files are present for", chemistry)
    return files


def prepare_polymer(workshop, chemistry, length):
    _positive_integer(length, "Chain length", minimum=2)
    check_chemistry(workshop, chemistry)
    _new(_inside(workshop, workshop.database / "built_PHAs" / f"P{chemistry}_{length}"))
    from iphasimulator.build_pha import PHAPolymerBuilder
    return PHAPolymerBuilder(workshop.database)


def _positive_integer(value, label, minimum=1):
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        raise ValueError(f"{label} must be a whole number of at least {minimum}.")


def check_chain(workshop, polymer_name, repeat_units):
    _name(polymer_name)
    from .records_and_checks import check_chain as check
    return check(workshop, POLYMER_NAME=polymer_name, EXPECTED_REPEAT_UNITS=repeat_units)


def prepare_system(workshop, polymer_name, kind, *, concentration=0.15, chains=25, density=750):
    from iphasimulator.pha_filepath_manager import PHAFileManager
    _name(polymer_name)
    paths = PHAFileManager(workshop.database)
    chain = paths.get_built_PHA_amber_files(polymer_name)
    check_output_files(*(chain[k] for k in ("pdb", "prmtop", "rst7")))
    if kind == "dry":
        name = paths.get_dry_PHA_system_name(polymer_name)
    elif kind == "solvated":
        name = paths.get_solvated_PHA_system_name(polymer_name)
    elif kind == "solvated_ions":
        if concentration <= 0:
            raise ValueError("Salt concentration must be positive, in mol/L.")
        name = paths.get_solvated_ions_PHA_system_name(polymer_name, "KCl", concentration)
    elif kind == "melt":
        _positive_integer(chains, "Number of chains", minimum=2)
        if density <= 0:
            raise ValueError("Initial density must be positive, in kg/m³.")
        name = paths.get_PHA_melt_name([polymer_name], [chains])
    else:
        raise ValueError("Unknown system type: " + kind)
    files = paths.get_md_system_files(name, kind)
    _new(_inside(workshop, files["system_dir"]))
    return SimpleNamespace(name=name, kind=kind, files=files, chain=chain, chains=chains)


def check_system(result, prepared):
    """Check Amber counts, periodic box and the expected water/salt content."""
    from collections import Counter
    from openmm.app import AmberPrmtopFile, AmberInpcrdFile
    check_output_files(*(result[k] for k in ("pdb", "prmtop", "rst7")))
    top = AmberPrmtopFile(str(result["prmtop"]))
    coords = AmberInpcrdFile(str(result["rst7"]))
    if top.topology.getNumAtoms() != len(coords.positions) or coords.boxVectors is None:
        raise RuntimeError("Atom counts disagree or the periodic box is missing.")
    counts = Counter(r.name for r in top.topology.residues())
    water = sum(n for r, n in counts.items() if r.upper() in {"WAT", "HOH", "SOL", "TIP3", "TIP3P"})
    if prepared.kind == "dry":
        original = AmberPrmtopFile(str(prepared.chain["prmtop"])).topology.getNumAtoms()
        if water or original != top.topology.getNumAtoms():
            raise RuntimeError("Dry-system composition differs from the input chain.")
    elif not water:
        raise RuntimeError("No recognised water residues were found.")
    if prepared.kind == "solvated_ions":
        positive = sum(n for r, n in counts.items() if r.upper() in {"K", "K+", "POT"})
        negative = sum(n for r, n in counts.items() if r.upper() in {"CL", "CL-", "CLA"})
        if positive != result["num_ion_pairs"] or negative != result["num_ion_pairs"]:
            raise RuntimeError("KCl counts differ from the requested ion-pair count.")
    print("Atom counts, box and composition checks passed:", dict(counts))
    return dict(counts)


def check_melt(result, prepared):
    from openmm.app import AmberPrmtopFile, GromacsTopFile, GromacsGroFile
    check_output_files(result["topology_file"], result["coordinate_file"])
    atoms = AmberPrmtopFile(str(prepared.chain["prmtop"])).topology.getNumAtoms()
    gro = GromacsGroFile(str(result["coordinate_file"]))
    top = GromacsTopFile(str(result["topology_file"]), periodicBoxVectors=gro.getPeriodicBoxVectors())
    expected = prepared.chains * atoms
    actual = len(gro.positions)
    print("Atoms requested:", expected, "Atoms produced:", actual)
    if actual != expected or top.topology.getNumAtoms() != expected:
        raise RuntimeError("Melt composition differs from the request. The current topology can include an extra chain. Keep the files for diagnosis; do not treat this as a validated melt.")
    return {"Requested atoms": expected, "Coordinate atoms": actual, "Topology atoms": top.topology.getNumAtoms()}


def find_system(workshop, system_name):
    from iphasimulator.pha_filepath_manager import PHAFileManager
    _name(system_name)
    paths = PHAFileManager(workshop.database)
    row = paths.get_md_system(system_name)
    files = paths.validate_md_system_files(system_name, row["system_type"])
    _inside(workshop, files["system_dir"])
    print("Selected system:", row)
    return SimpleNamespace(name=system_name, kind=row["system_type"], **files)


def save_protocol(workshop, protocol):
    from iphasimulator.openmmscript_builder import OpenMMScriptBuilder
    system = find_system(workshop, protocol.system_name)
    name = _name(protocol.workflow_name)
    script = _inside(workshop, workshop.root / "md_simulation_scripts" / f"{name}.py")
    definition = _inside(workshop, system.workflows_dir / f"{name}.workflow.json")
    for path in (script, definition):
        _new(path)
    protocol.validate()
    definition.parent.mkdir(parents=True, exist_ok=True)
    protocol.save_workflow(definition)
    protocol.write_script(script)
    if OpenMMScriptBuilder.load_workflow(definition).to_dict() != protocol.to_dict():
        raise RuntimeError("Saved protocol differs from the requested protocol.")
    return SimpleNamespace(script=script, definition=definition)


def run_simulation(workshop, system_name, workflow_name, platform="CPU"):
    """Run the exact saved script with the appropriate checkout/workspace paths."""
    import subprocess
    from datetime import datetime, timezone
    from iphasimulator.openmmscript_builder import OpenMMScriptBuilder
    _name(workflow_name)
    system = find_system(workshop, system_name)
    script = workshop.root / "md_simulation_scripts" / f"{workflow_name}.py"
    definition = system.workflows_dir / f"{workflow_name}.workflow.json"
    check_output_files(script, definition)
    builder = OpenMMScriptBuilder.load_workflow(definition)
    if builder.system_name != system_name or script.read_text() != builder.to_script():
        raise RuntimeError("Script and saved protocol differ. Create a matching pair with lesson 10.")
    environment = dict(os.environ)
    environment["IPHA_OPENMM_PLATFORM"] = platform
    environment["PYTHONPATH"] = os.pathsep.join([str(workshop.project), str(workshop.project / "src"), environment.get("PYTHONPATH", "")])
    before = set(system.simulations_dir.glob("*"))
    log_dir = _inside(workshop, workshop.root / "execution_logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log = log_dir / (workflow_name + datetime.now(timezone.utc).strftime("_%Y%m%dT%H%M%S%fZ.log"))
    print("Running on", platform, "— progress is recorded in", log, flush=True)
    with log.open("x") as handle:
        process = subprocess.run([sys.executable, "-u", str(script)], cwd=workshop.project, env=environment, stdout=handle, stderr=subprocess.STDOUT)
    if process.returncode:
        raise RuntimeError(f"Simulation failed. Read {log}; partial outputs may remain.")
    created = [p for p in set(system.simulations_dir.glob("*")) - before if p.is_dir()]
    if len(created) != 1:
        raise RuntimeError("Expected one new simulation folder. Inspect the execution log.")
    return SimpleNamespace(directory=created[0], name=created[0].name, log=log)


def check_simulation(loaded):
    check_output_files(loaded.topology_path, loaded.trajectory_path, loaded.data_path)
    frames, rows = len(loaded.universe.trajectory), len(loaded.data)
    if frames != rows or not frames:
        raise RuntimeError("Trajectory and state-data lengths disagree or are empty.")
    print("Frames:", frames, "Data rows:", rows)
    print("The loader checked sampled time alignment. Equilibration is a separate question.")


def replica_folder(workshop, system_name, simulation_name):
    return _inside(workshop, workshop.database / "PHA_melts" / _name(system_name) / "simulations" / _name(simulation_name) / "analysis/tg_analysis")


def prepare_replica_analysis(workshop, system_name, simulation_name):
    output = replica_folder(workshop, system_name, simulation_name)
    if not output.parent.parent.is_dir():
        raise RuntimeError("Cooling dataset is missing. Follow the prepared-data instructions in tutorials/README.md.")
    _new(output)
    return output


def read_replica_summary(workshop, system_name, simulation_name):
    folder = replica_folder(workshop, system_name, simulation_name)
    check_output_files(folder / "analysis_summary.json", folder / "tg/temperature_response.csv")
    summary = json.loads((folder / "analysis_summary.json").read_text())
    if summary.get("system") != system_name or summary.get("simulation") != simulation_name:
        raise RuntimeError("Analysis identity differs from the selected replica.")
    print("Estimated Tg (K):", summary["tg"]["tg_K"])
    return summary


def prepare_replica_comparison(workshop, system_name, simulation_names):
    import math
    if len(simulation_names) < 2 or len(set(simulation_names)) != len(simulation_names):
        raise ValueError("Choose at least two distinct independent replicas.")
    summaries = [read_replica_summary(workshop, system_name, name) for name in simulation_names]
    def key(s):
        return (s["stage"], s["temperature_assignment"], s["sampling"]["stride"], s["sampling"]["polymer_chains"], s["tg"]["observable"])
    if any(s.get("analysis_level") != "replica" or not math.isfinite(float(s["tg"]["tg_K"])) for s in summaries):
        raise RuntimeError("A replica has an invalid analysis level or Tg estimate.")
    if any(key(s) != key(summaries[0]) for s in summaries[1:]):
        raise RuntimeError("Replica schedules, sampling, composition or observables differ. Review compatibility first.")
    output = _inside(workshop, workshop.database / "PHA_melts" / _name(system_name) / "analysis/tg_analysis")
    _new(output)
    return output


def record_workflow(workshop, system_name, simulation_name, workflow_name):
    from .records_and_checks import record_run
    for value in (system_name, simulation_name, workflow_name):
        _name(value)
    return record_run(workshop, SYSTEM_NAME=system_name, SIMULATION_NAME=simulation_name, WORKFLOW_NAME=workflow_name)


def _display(image):
    """Display inline only when an interactive IPython shell is active."""
    try:
        from IPython import get_ipython
        from IPython.display import display
    except ImportError:
        return
    if get_ipython() is not None:
        display(image)


def save_picture(workshop, image, filename):
    destination = _inside(workshop, workshop.root / "figures" / _name(filename))
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination)
    check_output_files(destination)
    print("Open this picture to inspect the chemical structure. It is a 2D drawing, not the built 3D geometry.")
    return destination


def _save_plot(workshop, figure, filename):
    import matplotlib.pyplot as plt
    path = _inside(workshop, workshop.root / "figures" / _name(filename))
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.tight_layout()
    figure.savefig(path, dpi=150)
    _display(figure)
    plt.close(figure)
    check_output_files(path)
    return path


def plot_counts(workshop, counts, title, filename):
    import matplotlib.pyplot as plt
    figure, axis = plt.subplots(figsize=(8, 4))
    axis.bar(list(counts), list(counts.values()))
    axis.set(title=title, ylabel="Count")
    axis.bar_label(axis.containers[0])
    return _save_plot(workshop, figure, filename)


def plot_simulation(workshop, loaded):
    import matplotlib.pyplot as plt
    data = loaded.data
    columns = [c for c in data.columns if "Temperature" in c or "Energy" in c]
    if not columns:
        raise RuntimeError("No temperature or energy columns were found in the state-data table.")
    time = next((c for c in data.columns if "Time" in c), None)
    x = data[time] if time else range(len(data))
    figure, axes = plt.subplots(len(columns), 1, figsize=(8, 3 * len(columns)), squeeze=False)
    for axis, column in zip(axes[:, 0], columns):
        axis.plot(x, data[column])
        axis.set(xlabel=time or "Saved row", ylabel=column)
    return _save_plot(workshop, figure, loaded.simulation_directory.name + "_temperature_energy.png")


def show_saved_figures(folder, names):
    """Use existing analysis images without recalculating or silently skipping all."""
    from PIL import Image
    shown = []
    for name in names:
        matches = sorted(Path(folder).rglob(_name(name)))
        if not matches:
            print("Figure not available:", name, "— it may have been disabled or skipped by the analysis.")
        for path in matches:
            check_output_files(path)
            with Image.open(path) as image:
                _display(image.copy())
            shown.append(path)
    if not shown:
        print("No requested figures are present. Use a dataset with saved figures, or generate figures during a fresh analysis.")
    return shown


def prepare_parameterisation(workshop, experiment_name, geometry_mode):
    experiment = _inside(workshop, workshop.root / "advanced_experiments" / _name(experiment_name))
    _new(experiment)
    if geometry_mode == "quick":
        raise RuntimeError("The current quick geometry route has a caller/signature mismatch; see guide A01.")
    from iphasimulator.build_pha import PHAPolymerBuilder
    return PHAPolymerBuilder(experiment / "structure_database")


def prepare_residue_definitions(workshop, experiment_name, chemistry):
    database = _inside(workshop, workshop.root / "advanced_experiments" / _name(experiment_name) / "structure_database")
    directory = database / "PHA_types" / _name(chemistry)
    trimer = f"P{chemistry}_3"
    check_output_files(database / "residue_codes.csv", directory / "trimer" / f"{trimer}.ac")
    definitions = [directory / "input" / f"{role}_{trimer}.txt" for role in ("head", "mainchain", "tail")]
    check_output_files(*definitions)
    for path in definitions:
        print(path.name, "\n", path.read_text())
    outputs = [directory / "monomer_units" / f"{part}P{chemistry}.prepin" for part in "hmt"]
    for path in outputs:
        _new(path)
    from iphasimulator.build_pha import PHAPolymerBuilder
    return SimpleNamespace(builder=PHAPolymerBuilder(database), files=outputs)


def check_residue_files(files):
    check_output_files(*files)
    for path in files:
        if "nan" in path.read_text().lower().split():
            raise RuntimeError(f"NaN found in {path}; inspect the PREPGEN logs.")
    print("Files and basic text check passed. Review charges and connection atoms before building.")


def describe_sequence(chemistries, pattern, length):
    _positive_integer(length, "Chain length", minimum=2)
    if not 2 <= len(chemistries) <= 26 or len(set(chemistries)) != len(chemistries):
        raise ValueError("Choose 2–26 different chemistries.")
    mapping = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", chemistries))
    if not pattern or length % len(pattern) or not set(pattern) <= set(mapping):
        raise ValueError("Pattern must use the selected letters and repeat to fill the chain.")
    sequence = [mapping[c] for c in pattern * (length // len(pattern))]
    print("Sequence:", " → ".join(sequence))
    return sequence


def prepare_copolymer(workshop, chemistries, pattern, length):
    describe_sequence(chemistries, pattern, length)
    for chemistry in chemistries:
        check_chemistry(workshop, chemistry)
    name = "co_" + "_".join("P" + p for p in chemistries) + f"_{pattern}_{length}"
    _new(_inside(workshop, workshop.database / "built_PHAs" / name))
    from iphasimulator.build_pha import PHAPolymerBuilder
    return PHAPolymerBuilder(workshop.database)


def prepare_gromacs_dataset(workshop, dataset, trajectory, structure, index, groups):
    from iphasimulator.trajectory_centering import read_index
    folder = _inside(workshop, workshop.root / "datasets" / _name(dataset))
    check_output_files(*(folder / _name(name) for name in (trajectory, structure, index)))
    available = read_index(folder / index)
    print("Available atom groups:", available.names)
    for name in groups:
        if not available.has_group(name):
            raise RuntimeError(f"Missing atom group {name!r}; choose a name printed above.")
    extras = [p.name for p in folder.iterdir() if p.name not in {trajectory, structure, index}]
    if extras:
        raise RuntimeError("Use a fresh copy containing only the three input files. Extra files: " + ", ".join(extras))
    return folder


def inspect_module(workshop, relative_path):
    """Read module syntax without importing or executing the selected module."""
    import ast
    package = workshop.project / "src/iphasimulator"
    path = (package / relative_path).resolve()
    if not path.is_relative_to(package.resolve()):
        raise ValueError("Choose a Python file inside src/iphasimulator.")
    tree = ast.parse(path.read_text())
    functions = []
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            print(ast.unparse(node))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(node.name)
            print(node.name, "(", ast.unparse(node.args), ")")
    return functions


def read_cluster_example(workshop):
    """Read existing examples; avoid the currently broken legacy builder import."""
    import yaml
    configuration = workshop.project / "examples/hpc_validation_workflow.yaml"
    script = workshop.project / "examples/slurm_validation_workflow.sh"
    check_output_files(configuration, script)
    config = yaml.safe_load(configuration.read_text())
    if not isinstance(config, dict) or not {"stages", "slurm"} <= config.keys():
        raise RuntimeError("The example configuration is missing stages or Slurm settings.")
    return SimpleNamespace(settings=config, script=script.read_text())
