# A02 — Define reusable head, middle and tail residues

**Task:** understand how the package turns a parameterised trimer into reusable residue inputs.

**Inputs:** A01's experiment database, the trimer AC file, and manually reviewed head/mainchain/tail definition files. **Outputs:** three PREPIN files. New force-field fitting is not performed here.

## Why this is a separate stage

`generate_polymer_prepins()` needs both chemistry identity and an explicit atom partition. The registry supplies the Amber residue codes. The definition files tell PREPGEN which atoms participate in each unit and its connections. The Python method checks that the files exist; it does not derive or scientifically validate those definitions for you.

The helper constructs the expected names, copies AC and definition inputs into the experiment's temporary directory, runs PREPGEN three times, and copies the results into `monomer_units`. It returns paths and residue-code information. The result must remain consistent with the force-field parameters derived from the trimer.

## Follow the functions

- `get_PHA_input_dir()`, `get_PHA_trimer_dir()` and `get_PHA_monomer_units_dir()` identify different stages of the chemistry record.
- `PHAResidueCodeManager.get_code()` supplies the registered role-specific codes.
- `generate_polymer_prepins()` assembles commands and coordinates the three residue outputs.
- `build_PHA_polymer()` later creates a head + repeated-middle + tail LEaP sequence. For a length-two chain there are no middle residues.
- `get_monomer_smiles()`, `generate_polymer_smiles_from_sequence()` and `save_polymer_smiles()` maintain the associated textual representation. This is another output path, not a replacement for topology validation.

## Prepare the exercise

After A01, place the three reviewed definition files in the experiment's `PHA_types/3HB/input/` folder. The filenames are `head_P3HB_3.txt`, `mainchain_P3HB_3.txt`, and `tail_P3HB_3.txt`.

The repository's supplied 3HB definitions are a reading example. Do not automatically assume they match a newly regenerated trimer. Compare atom identities and connections in your own AC file before copying or adapting definitions. Developing definitions for an unfamiliar chemistry requires a separate chemical review; this guide does not invent atom maps.

Review the definition files before running the adjacent exercise. Its setup helper prints the supplied definitions, requires PREPGEN, and refuses any existing PREPIN outputs. The next function call generates the residues. The final check confirms files exist and performs a basic NaN-token check. It does not validate all numerical fields, total residue charge, end-group chemistry or connection geometry.

## Validation exercise

Build a very short polymer using the experiment database only, once the parameter set has been reviewed. Trace the residue sequence to the generated LEaP file. Inspect bond connections, end groups, atom counts and total charge in the resulting topology. Then compare a second length: the middle-unit count changes while the same parameter files are reused.

Do not replace the core workshop parameters automatically. A successful external command and a chemically acceptable reusable residue are different outcomes.

**Review questions:** Why does a registry code not prove a residue is ready? What must change between a two-unit and a ten-unit chain? Why can changing atom ordering invalidate otherwise familiar definition files?

**Answers:** Registration contains identity rather than generated parameters; eight middle residues are added; the definitions refer to specific atom identities/connections in their source trimer.

## Function reading

See [build_pha](../reference/build_pha.md) and [pha_filepath_manager](../reference/pha_filepath_manager.md), including private helpers and constructor side effects. [build_single_PHA_systems](../reference/build_single_PHA_systems.md) shows how those same parameter files are subsequently reused for system preparation.
