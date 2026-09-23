#!/usr/bin/env python3
"""Regenerate tutorial reference pages by reading package syntax, without imports.

Run from any directory with Python 3.10+. Only generated files in this directory
are written. No package functions or external scientific tools are executed.
"""
from __future__ import annotations

import ast
import hashlib
import json
import textwrap
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parents[1] / "src" / "iphasimulator"

MODULE_GUIDES = {
    "build": "Direct RDKit construction route: validate the request, derive repeat-unit chemistry, build the molecule, and check stereochemistry/connectivity. These molecules feed the older SDF-based parameterisation route; they are not the reusable PREPIN database objects.",
    "build_pha": "Database-backed construction route: register and parameterise a trimer, prepare reusable residues, then assemble homopolymers/copolymers through LEaP. The class also owns geometry preparation, command execution and SMILES persistence. Two geometry methods are defined twice: later definitions replace earlier ones. The current none mode uses Open Babel make3D despite an older ETKDG description; quick mode has a caller/signature mismatch. Treat the implementation and the A01 guide as the more precise account of those cases.",
    "build_single_PHA_systems": "System preparation around an already-built homopolymer. The common input preparation resolves residue parameters and Amber files. Dry, water and salted routes then write/run LEaP inputs, count atoms and register outputs. Salt preparation estimates pairs after an initial solvation pass. The box parameter is forwarded to Amber operations; dry setBox and solvent padding have different meanings.",
    "conversion_amber_to_gromacs": "Whole-system format conversion through ParmEd. A small charge-rounding correction precedes topology/coordinate writing. This is a representation change, not a new force-field fit or a dynamics run.",
    "export": "RDKit molecule export: prepare a hydrogen-explicit 3D conformer and write SDF/PDB. This route supports the earlier direct-molecule workflow and is distinct from LEaP residue assembly.",
    "monomers": "Curated in-code monomer definitions for the RDKit builder, with canonical names and residue-name metadata. This catalogue and the persistent residue_codes.csv database are separate representations; registration in either does not prove PREPIN readiness.",
    "naming": "Canonical naming and validation for chemistry/polymer identifiers and residue variants. Other parts of the current project still construct names independently, so this module is not yet the only naming implementation.",
    "openmmscript_builder": "Represent ordered simulation stages, validate them, serialise workflow JSON and generate executable Python. Generating code does not run dynamics. The generated script expects a workspace directory layout and still uses source-checkout imports; its first execution stage is minimisation.",
    "parameterization_gaff2": "Whole-molecule SDF-to-Amber pipeline using Antechamber, Parmchk2 and LEaP. Includes executable checks, command invocation, charge-rounding adjustment, input preparation, timing and structured outputs. It is separate from trimer-to-residue parameterisation.",
    "pha_filepath_manager": "Paths and persistent registries for chemistry, built chains, systems, protocols and runs. Constructors initialise directories/CSV files; this is not a strictly read-only path abstraction. The module imports ParmEd for atom counting. Registry identity and file existence checks do not establish scientific validity.",
    "pha_melt_builder": "Resolve built polymers, ensure GROMACS representations through ACPYPE, assemble Polyply input and generate packed coordinates. The included topology can retain a one-molecule entry in addition to the outer requested count; existing 25-chain-labelled data contain 26 chains. Verify actual composition. The optional simulation helper is separate from packing.",
    "simulation_gromacs_runner": "Native GROMACS preparation, script generation, box/solvation operations and several levels of file/topology validation. Some functions write scripts; others invoke GROMACS. Keep these effects distinct when tracing a workflow. An output dataclass reports one operation, not complete scientific readiness.",
    "simulation_openmm_amber_runner": "Earlier compact OpenMM validation route using Amber inputs. It orchestrates minimisation, NVT, periodic NPT where applicable, production and output summaries. It is not the newer OpenMMScriptBuilder/sw_openmm implementation. _temperature_schedule currently has no callers found in the inspected teaching/source routes.",
    "stereochemistry": "Validate supported stereochemistry settings and assigned chiral centres on RDKit molecules. These checks support chemical construction and are different from inspecting the geometry of a simulated trajectory.",
    "sw_openmm": "OpenMM engine implementation for Amber and GROMACS input formats. BuildSimulation owns platform/system/context creation, simulation stages, reporting, restart output and graphing. Read state transfer between stages explicitly. Restart/default-output paths still reference manager.systems_dir, which the current PHAFileManager does not expose.",
    "system_builder_packmol": "Separate Packmol route for initial solvated coordinates. Estimate counts, copy/write support structures, compose packing input and optionally invoke Packmol. Producing a packed PDB does not complete a parameterised dynamics workflow.",
    "trajectory_centering": "Parse/write GROMACS index groups, choose source groups, merge atom indices and create/reuse a centring index. Index entries use the original topology atom ordering. Some helpers write files even when called by a larger dry-run workflow.",
    "trajectory_frame_extraction": "Small GROMACS trjconv wrappers that extract a specified or first frame. The resulting frame must retain the atom ordering expected by downstream consumers.",
    "trajectory_gromacs_trjconv": "Build and execute GROMACS trajectory commands with explicit group-selection input. Dedicated wrappers express reconstruction, centring/compact wrapping and fitting. Optional runner injection supports testing command composition.",
    "trajectory_preprocessing": "Orchestrate centring-index preparation, trajectory processing, optional fitting and representative-frame extraction. The full System remains in output. dry_run skips trajectory commands after index preparation, so it can still write an index.",
    "analysis/descriptors": "Convert sampled frames into per-segment pairwise heavy-atom distances. Segment identity, original frame indices and feature count travel in the result record. Segment equals polymer-chain is an assumption; the heavy-atom selection is name-based and distances use periodic box information.",
    "analysis/pca": "Standardise each chain's descriptor matrix, fit PCA and preserve frame indices and variance information. Different chains have separate fitted transforms even if they share a selected number of components.",
    "analysis/simulation_loader": "Find one minimised PDB and stage-specific DCD/TXT pair, load MDAnalysis/pandas objects, and check lengths plus selected time checkpoints. File matching is deliberately strict; a stage with multiple matches is ambiguous.",
    "analysis/tg_analysis/clustering": "Estimate epsilon from nearest-neighbour distance curves and cluster each chain's PCA samples using DBSCAN. Return labels, noise and cluster counts with frame identity. Knee fallback and temperature-dependent trimming are part of the implemented policy.",
    "analysis/tg_analysis/glass_transition": "Build the historical mean-numeric-cluster-label response by nominal temperature, then fit a tanh-based curve and report d/s as Tg. Numeric labels are identifiers, so interpreting their average requires scientific scrutiny. The fit covariance is not returned and Tg is not bounded to the sampled temperature interval.",
    "analysis/tg_analysis/optimisation": "Two stages of parameter selection: chain PCA diagnostics/common dimension and DBSCAN parameter/stability diagnostics. Median elbow selects dimension; stability plus guardrails selects min_samples. Table builders preserve intermediate evidence for plots and later review.",
    "analysis/tg_analysis/temperature_assignment": "Assign nominal cooling temperatures using supplied total steps, reporting frequency, temperature range and step. The historical frame-zero convention is preserved. This does not infer the protocol from instantaneous temperature measurements.",
    "analysis/tg_analysis/workflow": "Replica orchestration plus output writing, plots and text reports. Load, assign temperatures, describe, optimise PCA/DBSCAN, fit, preserve conformational states, then save diagnostics. The system path currently targets PHA_melts. Summary output is written before optional plotting completes, so inspect full-run status as well as file presence.",
    "analysis/tg_analysis/system_analysis": "Consume completed replica summaries/temperature responses and aggregate independently fitted Tg values. No trajectory analysis or pooled refitting occurs. Automatic discovery can skip invalid replicas; explicit selection raises for invalid requested data. Compatibility/independence require additional review.",
    "visualisation/visualiser": "Read catalogue SMILES and draw individual or multiple monomers/polymers using RDKit. Catalogue loading, molecular parsing, drawing and notebook display are separate steps here; drawing a structure does not validate force-field readiness.",
    "workflows/design": "Translate one user design choice into the corresponding RDKit builder call. PolymerDesign holds configuration; supported_polymer_table provides catalogue records. This is a convenient orchestration layer rather than another chemistry engine.",
    "workflows/validation": "Define small benchmark targets, build RDKit molecules, describe chemistry and export SDF/PDB. These validation examples belong to the earlier direct-molecule route, not the newer MD-system registry.",
    "workflows/hpc": "Merge YAML defaults, parse targets, describe enabled stages and render a Slurm script for the older configured-workflow runner. The script is a starting template requiring site/path/log review, not a universal submission configuration.",
    "workflows/md_benchmark": "Discover validation targets and coordinate whole-molecule GAFF2, the earlier OpenMM runner and GROMACS preparation. CLI parsing and per-target failure collection belong to this orchestration layer.",
    "workflows/__init__": "Public re-exports for the earlier design, validation and HPC workflow helpers. This module contains no explicit function definitions of its own; imported functions are documented in their defining modules.",
    "__init__": "Empty top-level package initialiser. It currently provides no curated public re-export API.",
    "analysis/tg_analysis/__init__": "Empty initialiser for the Tg analysis package.",
    "analysis/tg_analysis/output": "Empty placeholder. The actual current output-writing behaviour remains in workflow.py and system_analysis.py; do not assume this module implements persistence.",
    "exceptions": "Placeholder containing a comment/docstring rather than custom exception implementations. Existing exceptions are defined in individual modules or use built-in types.",
}


def own_nodes(node):
    """Visit a definition's body while excluding bodies of nested definitions."""
    def walk(child):
        yield child
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
            return
        for grandchild in ast.iter_child_nodes(child):
            yield from walk(grandchild)
    for statement in node.body:
        yield from walk(statement)


def definitions(tree):
    found = []
    def visit(node, parents=()):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                qualname = ".".join((*parents, child.name))
                found.append((qualname, child, parents))
                visit(child, (*parents, child.name))
            else:
                visit(child, parents)
    visit(tree)
    return found


def expression(node, limit=400):
    value = ast.unparse(node) if node is not None else "None"
    return value if len(value) <= limit else value[:limit] + " … [full expression below]"


def escape(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def argument_rows(node):
    args = node.args
    positional = [*args.posonlyargs, *args.args]
    defaults = [None] * (len(positional) - len(args.defaults)) + list(args.defaults)
    rows = []
    for arg, default in zip(positional, defaults):
        role = "bound instance/class" if arg.arg in {"self", "cls"} else "required" if default is None else expression(default)
        rows.append((arg.arg, expression(arg.annotation) if arg.annotation else "not annotated", role))
    for arg, default in zip(args.kwonlyargs, args.kw_defaults):
        rows.append((arg.arg + " (keyword-only)", expression(arg.annotation) if arg.annotation else "not annotated", "required" if default is None else expression(default)))
    if args.vararg:
        rows.append(("*" + args.vararg.arg, "variadic positional", "optional"))
    if args.kwarg:
        rows.append(("**" + args.kwarg.arg, "variadic keyword", "optional"))
    return rows


def build():
    pages = []
    manifest = {"scope": "All explicit definitions in src/iphasimulator/**/*.py; third-party and GUI functions excluded", "modules": [], "functions": []}
    for path in sorted(PACKAGE.rglob("*.py")):
        relative = path.relative_to(PACKAGE)
        key = relative.with_suffix("").as_posix()
        source = path.read_text()
        tree = ast.parse(source)
        all_defs = definitions(tree)
        functions = [(q, n, parent) for q, n, parent in all_defs if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
        counts = Counter(q for q, _, _ in functions)
        last_lines = {q: n.lineno for q, n, _ in functions}
        filename = key.replace("/", "__") + ".md"
        imports = [ast.unparse(n) for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))]
        lines = [f"# {relative.as_posix()}", "", MODULE_GUIDES.get(key, "Read the contracts and implementation below to trace this module's responsibilities."), "",
                 f"[Current source](../../src/iphasimulator/{relative.as_posix()})", "",
                 "This page is generated from source syntax. Original docstrings can be incomplete or outdated; module notes above identify known discrepancies. Call/return/error lists describe direct syntax, not all behaviour inside callees. Read the source excerpt for branch order and effects. No scientific execution is implied.", "",
                 f"Explicit functions/methods/nested helpers: **{len(functions)}**.", ""]
        if imports:
            lines += ["## Module imports", "", "```python", *imports, "```", ""]
        classes = [(q, n) for q, n, _ in all_defs if isinstance(n, ast.ClassDef)]
        if classes:
            lines += ["## Classes and result records", ""]
            for q, node in classes:
                lines += [f"### `{q}`", "", ast.get_docstring(node) or "No class docstring is supplied; inspect fields and methods below.", ""]
                fields = [ast.unparse(n) for n in node.body if isinstance(n, (ast.Assign, ast.AnnAssign))]
                decorators = [ast.unparse(d) for d in node.decorator_list]
                if decorators:
                    lines += ["Decorators: " + ", ".join(f"`{d}`" for d in decorators) + ".", ""]
                if fields:
                    lines += ["Declared fields/defaults (instance state may also be set by methods):", "", "```python", *fields, "```", ""]
                if any("dataclass" in d for d in decorators):
                    lines += ["Dataclass-generated methods are implicit and are not counted as explicit function definitions.", ""]
        if functions:
            lines += ["## Function map", ""]
            for q, node, _ in functions:
                lines.append(f"- [`{q}` — source line {node.lineno}](#definition-{node.lineno})")
            lines.append("")
        else:
            lines += ["No explicit function definitions occur in this module.", ""]
        for q, node, parent in functions:
            anchor = f"definition-{node.lineno}"
            own = list(own_nodes(node))
            calls = sorted({ast.unparse(n.func) for n in own if isinstance(n, ast.Call)})
            returns = list(dict.fromkeys(expression(n.value) for n in own if isinstance(n, ast.Return)))
            raises = list(dict.fromkeys(expression(n.exc) if n.exc is not None else "re-raises the active exception" for n in own if isinstance(n, ast.Raise)))
            state = sorted({ast.unparse(n) for n in own if isinstance(n, ast.Attribute) and isinstance(n.ctx, ast.Store) and isinstance(n.value, ast.Name) and n.value.id in {"self", "cls"}})
            effect_words = ("write", "save", "mkdir", "copy", "unlink", "remove", "run_command", "subprocess", "runner", "step", "show", "register", "load", "read", "open")
            effect_calls = [c for c in calls if any(word in c.lower() for word in effect_words)]
            doc = ast.get_docstring(node)
            lines += [f'<a id="{anchor}"></a>', "", f"## `{q}`", "", f"Source lines {node.lineno}–{node.end_lineno}. " + ("Internal helper/protocol method." if node.name.startswith("_") else "Named callable; inspect its callers before treating it as a stable public API."), ""]
            if counts[q] > 1:
                status = "LATER DEFINITION: replaces the earlier class-body definition." if node.lineno == last_lines[q] else "OVERWRITTEN: a later class-body definition with the same name is active."
                lines += [f"**{status}**", ""]
            if node.decorator_list:
                lines += ["Decorators: " + ", ".join("`" + ast.unparse(d) + "`" for d in node.decorator_list) + ".", ""]
            lines += ["```python", f"{'async ' if isinstance(node, ast.AsyncFunctionDef) else ''}def {node.name}({ast.unparse(node.args)})" + (f" -> {ast.unparse(node.returns)}" if node.returns else "") + ": ...", "```", "", "### Purpose and original contract", "", doc or "No function docstring is supplied. Use the source-derived reading guide and complete implementation below; undocumented physical units or guarantees must not be assumed.", "", "### Inputs", ""]
            rows = argument_rows(node)
            if rows:
                lines += ["| Argument | Annotation | Default / requirement |", "|---|---|---|"]
                lines += ["| " + " | ".join(escape(v) for v in row) + " |" for row in rows]
                lines.append("")
            else:
                lines += ["No explicit arguments.", ""]
            lines += ["### How to read this implementation", ""]
            if calls:
                lines += ["Direct calls (sorted inventory, not execution order): " + ", ".join(f"`{c}`" for c in calls) + ".", ""]
            else:
                lines += ["No direct function calls were found in this definition's own body.", ""]
            if returns:
                lines += ["Explicit return expressions; different branches may return different objects:", "", "```python", *returns, "```", ""]
            else:
                lines += ["No explicit return statement in this body. Normal completion returns `None` unless another language mechanism, such as a yield, applies.", ""]
            if state:
                lines += ["Instance/class attributes assigned directly: " + ", ".join(f"`{x}`" for x in state) + ".", ""]
            if effect_calls:
                lines += ["Calls worth inspecting for I/O, state changes or delegated execution: " + ", ".join(f"`{x}`" for x in effect_calls) + ". This is a name-based reading aid, not a complete effect analysis.", ""]
            else:
                lines += ["No I/O-like call names were identified by the reading aid. This does not prove the function or its dependencies are side-effect free.", ""]
            if raises:
                lines += ["Explicitly raised failures in this body (callees can raise additional errors):", "", "```python", *raises, "```", ""]
            else:
                lines += ["No explicit raise statement in this body. Failures may still propagate from dependencies or operations.", ""]
            lines += ["### Implementation for study", "", "<details>", "<summary>Read the complete current definition</summary>", "", "```python", textwrap.dedent("\n".join(source.splitlines()[node.lineno-1:node.end_lineno])), "```", "", "</details>", ""]
            manifest["functions"].append({"module": relative.as_posix(), "qualified_name": q, "line": node.lineno, "end_line": node.end_lineno, "page": filename, "anchor": anchor, "duplicate_name": counts[q] > 1})
        (HERE / filename).write_text("\n".join(lines))
        manifest["modules"].append({"path": relative.as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "function_definitions": len(functions), "page": filename})
        pages.append((relative.as_posix(), filename, len(functions)))
    manifest["module_count"] = len(pages)
    manifest["function_definition_count"] = len(manifest["functions"])
    (HERE / "coverage_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    index = ["# Complete package function coverage", "", f"This source snapshot covers **{len(pages)} Python modules** and **{len(manifest['functions'])} explicit function definitions** under `src/iphasimulator`.", "",
             "Coverage includes public functions, private helpers, class methods, properties, nested functions and both occurrences of overwritten definitions. Dataclass-generated methods and third-party APIs are not explicit package-source definitions and are not counted. GUI code is outside this reference's exhaustive scope.", "",
             "The advanced guides explain the major scientific and architectural flows. This reference adds source-derived contracts and implementation excerpts for every definition. An entry is documentation coverage, not a passing test or independent scientific validation. Existing docstrings are preserved and can contain historical discrepancies; module notes flag known cases.", "",
             "## Module reading map", "", "| Source module | Explicit definitions | Reference |", "|---|---:|---|"]
    index += [f"| `{name}` | {count} | [Read module]({filename}) |" for name, filename, count in pages]
    index += ["", "## Every explicit definition", "", "| Module | Function / method | Source line | Entry |", "|---|---|---:|---|"]
    index += [f"| `{f['module']}` | `{f['qualified_name']}` | {f['line']} | [Read]({f['page']}#{f['anchor']}) |" for f in manifest["functions"]]
    index += ["", "## Maintain this reference", "", "[coverage_manifest.json](coverage_manifest.json) stores the source hashes and exact definition inventory. It allows coverage to be checked without importing scientific dependencies.", "", "After package changes, regenerate these tutorial reference pages with:", "", "```bash", "python tutorials/reference/build_reference.py", "```", "", "The generator only reads package syntax and writes tutorial reference pages. Review its human-written module notes when behaviour changes; regenerated source inventories do not automatically update those interpretations.", ""]
    (HERE / "coverage_index.md").write_text("\n".join(index))
    print(f"Documented {len(manifest['functions'])} explicit definitions in {len(pages)} modules.")


if __name__ == "__main__":
    build()
