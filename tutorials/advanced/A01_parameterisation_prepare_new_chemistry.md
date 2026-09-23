# A01 — Understand and prepare chemistry parameters

**Task:** follow one chemistry from SMILES to parameter files and identify which functions own each step.

**Prerequisites:** the core environment checks, AmberTools, Open Babel, RDKit, and an understanding of the supplied 3HB chemistry. Run the adjacent `.py` exercise only after reading this guide.

## Two parameterisation routes

The package has two real routes. `parameterization_gaff2.parameterize_gaff2()` starts with an SDF representing a complete molecule and produces an Amber topology/coordinate pair. `PHAPolymerBuilder.parameterise_trimer()` prepares a representative trimer whose atoms will later be divided into reusable residues. Their shared tools do not make their outputs interchangeable.

For the trimer route, the builder first initialises paths and registers the chemistry. Registration allocates readable names and internal residue codes; it does not establish that parameter generation succeeded. The geometry step writes PDB, residue renaming assigns the registered trimer code, Antechamber writes MOL2, Parmchk2 writes FRCMOD, and a further Antechamber invocation writes AC. Paths returned in the result dictionary are the contract for subsequent steps.

Read these operations in order:

1. `PHAResidueCodeManager.register_PHA_type()` and `generate_unique_codes()` establish identity.
2. `PHAPolymerBuilder.parameterise_trimer()` orchestrates the preparation.
3. `smiles_to_pdb()` selects geometry preparation.
4. `_openbabel_molecule_to_rdkit()` and `_copy_rdkit_coordinates_to_openbabel()` bridge atom coordinates between libraries.
5. `replace_pdb_residue_name()` changes the PDB residue label.
6. `run_command()` executes external tools and exposes failures.

## Geometry choices and current implementation

Read the source rather than relying solely on older docstrings. The present `none` path calls Open Babel `make3D()`; it does not mean that no three-dimensional preparation occurs. Optional RDKit optimisation is an additional step.

Two geometry helpers are defined twice in the class. The later class definitions replace the earlier ones. The active quick helper requires a random seed that its current caller does not supply. The exercise explicitly refuses that mode. Comprehensive mode uses the active later helper; this tutorial does not certify its scientific suitability or change the implementation.

Geometry, atom ordering and manual residue definitions are coupled. After regenerating a trimer, review the atom identities used by PREPGEN before reusing definitions from a previous preparation.

## Whole-molecule GAFF2 route

`parameterize_gaff2()` prepares its SDF input, runs the external stages, normalises a small charge-rounding residue in MOL2, writes LEaP input, and records outputs/timing. Its `runner` argument allows controlled command substitution in tests. Charge-rounding correction is not a replacement for choosing the correct molecular net charge or validating the charge model.

The RDKit-only chain builder, `monomers`, `stereochemistry`, `naming`, and `export` modules form the earlier route feeding this SDF workflow. They remain distinct from the residue database. The reference pages explain their public functions and private validation helpers individually.

## Exercise and evidence

Read the inputs in section 2 before running the adjacent script. Running that section performs parameterisation and writes a new database under `advanced_experiments/parameterisation_3HB_01`, separate from the research database and core workshop parameters. Choose a new experiment name for each comparison. Section 3 checks the files and saves a monomer drawing; this drawing does not validate the generated trimer geometry or charges.

Inspect generated PDB, MOL2, AC and FRCMOD files and the tool output. Identify which file contains atom identities, which contains assigned charges, and which supplies extra force-field terms. File presence is only the first check. Retain the method, geometry settings, seed, tool versions and parameter inputs with the experiment.

**Review questions:** What can be registered before a run succeeds? Why is a whole-oligomer parameterisation not the same reusable object as a mainchain residue? Which helper is actually active when a method is defined twice?

**Answers:** Registry updates occur before all external stages finish; the whole oligomer includes its own complete connectivity and ends; the last definition in the class body is active.

## Function reading

Start with [build_pha](../reference/build_pha.md), [parameterization_gaff2](../reference/parameterization_gaff2.md), and [pha_filepath_manager](../reference/pha_filepath_manager.md). Continue with [build](../reference/build.md), [monomers](../reference/monomers.md), [stereochemistry](../reference/stereochemistry.md), [naming](../reference/naming.md), and [export](../reference/export.md).
