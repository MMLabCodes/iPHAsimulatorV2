# A04 — Understand the native GROMACS and trajectory routes

**Task:** distinguish preparation, execution, and trajectory processing, then inspect a real index file.

**Inputs:** a prepared GROMACS dataset in a dedicated workshop folder. **Outputs:** an index-group inspection, processed trajectory and representative frame.

## First distinguish the engine from its files

`GromacsSimulation` in `sw_openmm.py` reads GROMACS-format input but runs OpenMM. The `simulation_gromacs_runner.py` and `trajectory_gromacs_trjconv.py` modules instead prepare or call native GROMACS commands. That distinction determines prerequisites and output formats.

The earlier preparation route calls `convert_amber_to_gromacs()` using ParmEd, writes stage templates, constructs a box, and checks topology includes/cutoffs. Solvation helpers prepare solvent/ion inputs and scripts. Validation functions check different properties: file existence, includes, molecule counts, coordinate/topology counts, or GROMACS preprocessing success. No single boolean establishes every aspect of physical validity.

`system_builder_packmol.py` is another starting-structure route. It estimates water/ion counts, writes support structures and Packmol instructions, and optionally runs Packmol. Packing coordinates is not the same as completing a force-field topology or executing dynamics.

## Index and trajectory flow

`read_index()` creates a `GromacsIndex` with named, one-based atom indices. `resolve_center_source_groups()` selects the intended groups; `merged_group_atoms()` combines them; `ensure_center_index()` creates or reuses a centring index.

`preprocess_gromacs_trajectory()` orchestrates centring/compact wrapping, optional fitting, and representative-frame extraction. It keeps the full `System` output while using selected groups to centre or fit. This preserves solvent and ions for later analysis. `run_trjconv()` supplies the command and interactive group selections through explicit input.

The wrappers `reconstruct_molecules()` and `compact_wrap()` are separately callable operations. Their presence does not mean the main workflow calls every wrapper in sequence: inspect its actual calls. Likewise, `dry_run=True` skips trajectory commands but is evaluated after centring-index preparation, so it is not a universal no-write promise.

## Exercise

Copy a small production XTC, its matching TPR, and an NDX file into `<workspace>/datasets/gromacs_example`. Preserve atom ordering and provenance. Edit the script's input filenames and source group names to match the dataset. The setup helper prints the available groups and checks the selection before processing.

Running section 2 performs processing, so use a fresh folder containing just those three inputs and ensure `gmx` is available. Afterwards inspect a representative structure, output atom count, periodic-boundary behaviour and any fitting changes. The exercise refuses a folder containing previous outputs.

**Review questions:** Why retain the full System output? Why must index groups match the trajectory atom ordering? Does `dry_run` guarantee no files are written?

**Answers:** Later analyses may need solvent/ions; indices select positions in that atom ordering; not in this implementation, because the index may be written first.

## Function reading

Read [conversion_amber_to_gromacs](../reference/conversion_amber_to_gromacs.md), [simulation_gromacs_runner](../reference/simulation_gromacs_runner.md), [system_builder_packmol](../reference/system_builder_packmol.md), [trajectory_centering](../reference/trajectory_centering.md), [trajectory_gromacs_trjconv](../reference/trajectory_gromacs_trjconv.md), [trajectory_frame_extraction](../reference/trajectory_frame_extraction.md), and [trajectory_preprocessing](../reference/trajectory_preprocessing.md).
