# Complete package function coverage

This source snapshot covers **39 Python modules** and **417 explicit function definitions** under `src/iphasimulator`.

Coverage includes public functions, private helpers, class methods, properties, nested functions and both occurrences of overwritten definitions. Dataclass-generated methods and third-party APIs are not explicit package-source definitions and are not counted. GUI code is outside this reference's exhaustive scope.

The advanced guides explain the major scientific and architectural flows. This reference adds source-derived contracts and implementation excerpts for every definition. An entry is documentation coverage, not a passing test or independent scientific validation. Existing docstrings are preserved and can contain historical discrepancies; module notes flag known cases.

## Module reading map

| Source module | Explicit definitions | Reference |
|---|---:|---|
| `__init__.py` | 0 | [Read module](__init__.md) |
| `analysis/descriptors.py` | 5 | [Read module](analysis__descriptors.md) |
| `analysis/pca.py` | 2 | [Read module](analysis__pca.md) |
| `analysis/simulation_loader.py` | 3 | [Read module](analysis__simulation_loader.md) |
| `analysis/tg_analysis/__init__.py` | 0 | [Read module](analysis__tg_analysis____init__.md) |
| `analysis/tg_analysis/clustering.py` | 3 | [Read module](analysis__tg_analysis__clustering.md) |
| `analysis/tg_analysis/glass_transition.py` | 3 | [Read module](analysis__tg_analysis__glass_transition.md) |
| `analysis/tg_analysis/optimisation.py` | 22 | [Read module](analysis__tg_analysis__optimisation.md) |
| `analysis/tg_analysis/output.py` | 0 | [Read module](analysis__tg_analysis__output.md) |
| `analysis/tg_analysis/system_analysis.py` | 14 | [Read module](analysis__tg_analysis__system_analysis.md) |
| `analysis/tg_analysis/temperature_assignment.py` | 1 | [Read module](analysis__tg_analysis__temperature_assignment.md) |
| `analysis/tg_analysis/workflow.py` | 17 | [Read module](analysis__tg_analysis__workflow.md) |
| `build.py` | 19 | [Read module](build.md) |
| `build_pha.py` | 18 | [Read module](build_pha.md) |
| `build_single_PHA_systems.py` | 8 | [Read module](build_single_PHA_systems.md) |
| `conversion_amber_to_gromacs.py` | 2 | [Read module](conversion_amber_to_gromacs.md) |
| `exceptions.py` | 0 | [Read module](exceptions.md) |
| `export.py` | 3 | [Read module](export.md) |
| `monomers.py` | 5 | [Read module](monomers.md) |
| `naming.py` | 13 | [Read module](naming.md) |
| `openmmscript_builder.py` | 18 | [Read module](openmmscript_builder.md) |
| `parameterization_gaff2.py` | 8 | [Read module](parameterization_gaff2.md) |
| `pha_filepath_manager.py` | 71 | [Read module](pha_filepath_manager.md) |
| `pha_melt_builder.py` | 14 | [Read module](pha_melt_builder.md) |
| `simulation_gromacs_runner.py` | 47 | [Read module](simulation_gromacs_runner.md) |
| `simulation_openmm_amber_runner.py` | 12 | [Read module](simulation_openmm_amber_runner.md) |
| `stereochemistry.py` | 3 | [Read module](stereochemistry.md) |
| `sw_openmm.py` | 40 | [Read module](sw_openmm.md) |
| `system_builder_packmol.py` | 9 | [Read module](system_builder_packmol.md) |
| `trajectory_centering.py` | 9 | [Read module](trajectory_centering.md) |
| `trajectory_frame_extraction.py` | 2 | [Read module](trajectory_frame_extraction.md) |
| `trajectory_gromacs_trjconv.py` | 7 | [Read module](trajectory_gromacs_trjconv.md) |
| `trajectory_preprocessing.py` | 3 | [Read module](trajectory_preprocessing.md) |
| `visualisation/visualiser.py` | 9 | [Read module](visualisation__visualiser.md) |
| `workflows/__init__.py` | 0 | [Read module](workflows____init__.md) |
| `workflows/design.py` | 3 | [Read module](workflows__design.md) |
| `workflows/hpc.py` | 6 | [Read module](workflows__hpc.md) |
| `workflows/md_benchmark.py` | 14 | [Read module](workflows__md_benchmark.md) |
| `workflows/validation.py` | 4 | [Read module](workflows__validation.md) |

## Every explicit definition

| Module | Function / method | Source line | Entry |
|---|---|---:|---|
| `analysis/descriptors.py` | `get_polymer_segments` | 83 | [Read](analysis__descriptors.md#definition-83) |
| `analysis/descriptors.py` | `get_segment_heavy_atoms` | 124 | [Read](analysis__descriptors.md#definition-124) |
| `analysis/descriptors.py` | `get_chain_analysis_id` | 168 | [Read](analysis__descriptors.md#definition-168) |
| `analysis/descriptors.py` | `calculate_chain_distance_descriptors` | 204 | [Read](analysis__descriptors.md#definition-204) |
| `analysis/descriptors.py` | `calculate_all_chain_distance_descriptors` | 433 | [Read](analysis__descriptors.md#definition-433) |
| `analysis/pca.py` | `calculate_chain_pca` | 75 | [Read](analysis__pca.md#definition-75) |
| `analysis/pca.py` | `calculate_all_chain_pca` | 183 | [Read](analysis__pca.md#definition-183) |
| `analysis/simulation_loader.py` | `_find_single_file` | 71 | [Read](analysis__simulation_loader.md#definition-71) |
| `analysis/simulation_loader.py` | `validate_frame_data_alignment` | 134 | [Read](analysis__simulation_loader.md#definition-134) |
| `analysis/simulation_loader.py` | `load_simulation` | 266 | [Read](analysis__simulation_loader.md#definition-266) |
| `analysis/tg_analysis/clustering.py` | `estimate_dbscan_eps` | 105 | [Read](analysis__tg_analysis__clustering.md#definition-105) |
| `analysis/tg_analysis/clustering.py` | `cluster_chain_pca` | 262 | [Read](analysis__tg_analysis__clustering.md#definition-262) |
| `analysis/tg_analysis/clustering.py` | `cluster_all_chain_pca` | 310 | [Read](analysis__tg_analysis__clustering.md#definition-310) |
| `analysis/tg_analysis/glass_transition.py` | `calculate_historical_cluster_response` | 36 | [Read](analysis__tg_analysis__glass_transition.md#definition-36) |
| `analysis/tg_analysis/glass_transition.py` | `_historical_transition_function` | 118 | [Read](analysis__tg_analysis__glass_transition.md#definition-118) |
| `analysis/tg_analysis/glass_transition.py` | `fit_historical_tg` | 131 | [Read](analysis__tg_analysis__glass_transition.md#definition-131) |
| `analysis/tg_analysis/optimisation.py` | `_calculate_scree_elbow` | 188 | [Read](analysis__tg_analysis__optimisation.md#definition-188) |
| `analysis/tg_analysis/optimisation.py` | `_calculate_participation_ratio` | 233 | [Read](analysis__tg_analysis__optimisation.md#definition-233) |
| `analysis/tg_analysis/optimisation.py` | `_calculate_effective_rank` | 278 | [Read](analysis__tg_analysis__optimisation.md#definition-278) |
| `analysis/tg_analysis/optimisation.py` | `analyse_chain_pca_dimensionality` | 332 | [Read](analysis__tg_analysis__optimisation.md#definition-332) |
| `analysis/tg_analysis/optimisation.py` | `analyse_all_chain_pca_dimensionality` | 455 | [Read](analysis__tg_analysis__optimisation.md#definition-455) |
| `analysis/tg_analysis/optimisation.py` | `pca_spectra_to_dataframe` | 497 | [Read](analysis__tg_analysis__optimisation.md#definition-497) |
| `analysis/tg_analysis/optimisation.py` | `pca_dimensionality_to_dataframe` | 563 | [Read](analysis__tg_analysis__optimisation.md#definition-563) |
| `analysis/tg_analysis/optimisation.py` | `summarise_pca_spectrum` | 613 | [Read](analysis__tg_analysis__optimisation.md#definition-613) |
| `analysis/tg_analysis/optimisation.py` | `summarise_pca_dimensionality` | 658 | [Read](analysis__tg_analysis__optimisation.md#definition-658) |
| `analysis/tg_analysis/optimisation.py` | `optimise_pca_dimensionality` | 724 | [Read](analysis__tg_analysis__optimisation.md#definition-724) |
| `analysis/tg_analysis/optimisation.py` | `calculate_optimised_pca` | 883 | [Read](analysis__tg_analysis__optimisation.md#definition-883) |
| `analysis/tg_analysis/optimisation.py` | `get_dbscan_neighbor_rank` | 932 | [Read](analysis__tg_analysis__optimisation.md#definition-932) |
| `analysis/tg_analysis/optimisation.py` | `analyse_chain_dbscan_parameters` | 954 | [Read](analysis__tg_analysis__optimisation.md#definition-954) |
| `analysis/tg_analysis/optimisation.py` | `analyse_all_chain_dbscan_parameters` | 1064 | [Read](analysis__tg_analysis__optimisation.md#definition-1064) |
| `analysis/tg_analysis/optimisation.py` | `dbscan_parameters_to_dataframe` | 1121 | [Read](analysis__tg_analysis__optimisation.md#definition-1121) |
| `analysis/tg_analysis/optimisation.py` | `compare_adjacent_min_samples` | 1192 | [Read](analysis__tg_analysis__optimisation.md#definition-1192) |
| `analysis/tg_analysis/optimisation.py` | `calculate_all_chain_dbscan_stability` | 1324 | [Read](analysis__tg_analysis__optimisation.md#definition-1324) |
| `analysis/tg_analysis/optimisation.py` | `summarise_dbscan_parameters` | 1374 | [Read](analysis__tg_analysis__optimisation.md#definition-1374) |
| `analysis/tg_analysis/optimisation.py` | `summarise_dbscan_stability` | 1537 | [Read](analysis__tg_analysis__optimisation.md#definition-1537) |
| `analysis/tg_analysis/optimisation.py` | `build_dbscan_optimisation_summary` | 1616 | [Read](analysis__tg_analysis__optimisation.md#definition-1616) |
| `analysis/tg_analysis/optimisation.py` | `select_dbscan_min_samples` | 1697 | [Read](analysis__tg_analysis__optimisation.md#definition-1697) |
| `analysis/tg_analysis/optimisation.py` | `optimise_dbscan` | 1855 | [Read](analysis__tg_analysis__optimisation.md#definition-1855) |
| `analysis/tg_analysis/system_analysis.py` | `_save_figure` | 95 | [Read](analysis__tg_analysis__system_analysis.md#definition-95) |
| `analysis/tg_analysis/system_analysis.py` | `_load_json` | 126 | [Read](analysis__tg_analysis__system_analysis.md#definition-126) |
| `analysis/tg_analysis/system_analysis.py` | `discover_completed_replica_analyses` | 148 | [Read](analysis__tg_analysis__system_analysis.md#definition-148) |
| `analysis/tg_analysis/system_analysis.py` | `load_replica_analysis` | 209 | [Read](analysis__tg_analysis__system_analysis.md#definition-209) |
| `analysis/tg_analysis/system_analysis.py` | `build_replica_summary_dataframe` | 357 | [Read](analysis__tg_analysis__system_analysis.md#definition-357) |
| `analysis/tg_analysis/system_analysis.py` | `build_temperature_response_dataframe` | 559 | [Read](analysis__tg_analysis__system_analysis.md#definition-559) |
| `analysis/tg_analysis/system_analysis.py` | `build_pca_summary_dataframe` | 614 | [Read](analysis__tg_analysis__system_analysis.md#definition-614) |
| `analysis/tg_analysis/system_analysis.py` | `build_dbscan_summary_dataframe` | 640 | [Read](analysis__tg_analysis__system_analysis.md#definition-640) |
| `analysis/tg_analysis/system_analysis.py` | `calculate_system_tg_statistics` | 672 | [Read](analysis__tg_analysis__system_analysis.md#definition-672) |
| `analysis/tg_analysis/system_analysis.py` | `plot_tg_by_replica` | 764 | [Read](analysis__tg_analysis__system_analysis.md#definition-764) |
| `analysis/tg_analysis/system_analysis.py` | `plot_temperature_response_by_replica` | 876 | [Read](analysis__tg_analysis__system_analysis.md#definition-876) |
| `analysis/tg_analysis/system_analysis.py` | `plot_metric_by_replica` | 948 | [Read](analysis__tg_analysis__system_analysis.md#definition-948) |
| `analysis/tg_analysis/system_analysis.py` | `generate_system_figures` | 1063 | [Read](analysis__tg_analysis__system_analysis.md#definition-1063) |
| `analysis/tg_analysis/system_analysis.py` | `run_system_tg_analysis` | 1299 | [Read](analysis__tg_analysis__system_analysis.md#definition-1299) |
| `analysis/tg_analysis/temperature_assignment.py` | `assign_nominal_temperatures` | 26 | [Read](analysis__tg_analysis__temperature_assignment.md#definition-26) |
| `analysis/tg_analysis/workflow.py` | `_save_figure` | 108 | [Read](analysis__tg_analysis__workflow.md#definition-108) |
| `analysis/tg_analysis/workflow.py` | `plot_temperature_block_agreement` | 143 | [Read](analysis__tg_analysis__workflow.md#definition-143) |
| `analysis/tg_analysis/workflow.py` | `plot_pca_scree` | 297 | [Read](analysis__tg_analysis__workflow.md#definition-297) |
| `analysis/tg_analysis/workflow.py` | `plot_pca_elbow_distribution` | 396 | [Read](analysis__tg_analysis__workflow.md#definition-396) |
| `analysis/tg_analysis/workflow.py` | `_summarise_dbscan_parameter` | 499 | [Read](analysis__tg_analysis__workflow.md#definition-499) |
| `analysis/tg_analysis/workflow.py` | `plot_dbscan_noise` | 536 | [Read](analysis__tg_analysis__workflow.md#definition-536) |
| `analysis/tg_analysis/workflow.py` | `plot_dbscan_clusters` | 611 | [Read](analysis__tg_analysis__workflow.md#definition-611) |
| `analysis/tg_analysis/workflow.py` | `plot_dbscan_ari` | 686 | [Read](analysis__tg_analysis__workflow.md#definition-686) |
| `analysis/tg_analysis/workflow.py` | `_historical_tg_model` | 806 | [Read](analysis__tg_analysis__workflow.md#definition-806) |
| `analysis/tg_analysis/workflow.py` | `plot_tg_fit` | 843 | [Read](analysis__tg_analysis__workflow.md#definition-843) |
| `analysis/tg_analysis/workflow.py` | `build_conformational_state_dataframe` | 953 | [Read](analysis__tg_analysis__workflow.md#definition-953) |
| `analysis/tg_analysis/workflow.py` | `plot_chain_pca_temperature` | 1185 | [Read](analysis__tg_analysis__workflow.md#definition-1185) |
| `analysis/tg_analysis/workflow.py` | `plot_chain_pca_dbscan` | 1272 | [Read](analysis__tg_analysis__workflow.md#definition-1272) |
| `analysis/tg_analysis/workflow.py` | `generate_chain_pca_figures` | 1386 | [Read](analysis__tg_analysis__workflow.md#definition-1386) |
| `analysis/tg_analysis/workflow.py` | `generate_analysis_figures` | 1516 | [Read](analysis__tg_analysis__workflow.md#definition-1516) |
| `analysis/tg_analysis/workflow.py` | `write_analysis_report` | 1767 | [Read](analysis__tg_analysis__workflow.md#definition-1767) |
| `analysis/tg_analysis/workflow.py` | `run_tg_analysis` | 2029 | [Read](analysis__tg_analysis__workflow.md#definition-2029) |
| `build.py` | `_validate_repeat_units` | 23 | [Read](build.md#definition-23) |
| `build.py` | `_validate_side_chain_carbons` | 30 | [Read](build.md#definition-30) |
| `build.py` | `_build_oligomer_smiles` | 37 | [Read](build.md#definition-37) |
| `build.py` | `_sanitize_molecule` | 44 | [Read](build.md#definition-44) |
| `build.py` | `_count_carbons` | 58 | [Read](build.md#definition-58) |
| `build.py` | `_validate_ester_bond_count` | 62 | [Read](build.md#definition-62) |
| `build.py` | `_has_hydroxy_neighbor` | 71 | [Read](build.md#definition-71) |
| `build.py` | `_is_carboxyl_carbon` | 79 | [Read](build.md#definition-79) |
| `build.py` | `_is_backbone_methylene` | 96 | [Read](build.md#definition-96) |
| `build.py` | `_pha_chiral_atom_indices` | 106 | [Read](build.md#definition-106) |
| `build.py` | `_validate_pha_stereochemistry` | 122 | [Read](build.md#definition-122) |
| `build.py` | `_validate_side_chain_carbon_count` | 148 | [Read](build.md#definition-148) |
| `build.py` | `validate_pha_chain` | 162 | [Read](build.md#definition-162) |
| `build.py` | `_build_validated_pha_from_side_chain` | 174 | [Read](build.md#definition-174) |
| `build.py` | `_validate_custom_name` | 202 | [Read](build.md#definition-202) |
| `build.py` | `_side_chain_from_monomer_smiles` | 208 | [Read](build.md#definition-208) |
| `build.py` | `build_pha_chain` | 257 | [Read](build.md#definition-257) |
| `build.py` | `build_pha_by_sidechain` | 278 | [Read](build.md#definition-278) |
| `build.py` | `build_custom_pha` | 296 | [Read](build.md#definition-296) |
| `build_pha.py` | `PHAPolymerBuilder.__init__` | 62 | [Read](build_pha.md#definition-62) |
| `build_pha.py` | `PHAPolymerBuilder.parameterise_trimer` | 72 | [Read](build_pha.md#definition-72) |
| `build_pha.py` | `PHAPolymerBuilder.generate_polymer_prepins` | 211 | [Read](build_pha.md#definition-211) |
| `build_pha.py` | `PHAPolymerBuilder.build_PHA_polymer` | 309 | [Read](build_pha.md#definition-309) |
| `build_pha.py` | `PHAPolymerBuilder.smiles_to_pdb` | 427 | [Read](build_pha.md#definition-427) |
| `build_pha.py` | `PHAPolymerBuilder._openbabel_molecule_to_rdkit` | 616 | [Read](build_pha.md#definition-616) |
| `build_pha.py` | `PHAPolymerBuilder._copy_rdkit_coordinates_to_openbabel` | 719 | [Read](build_pha.md#definition-719) |
| `build_pha.py` | `PHAPolymerBuilder._prepare_single_conformer_optimized` | 808 | [Read](build_pha.md#definition-808) |
| `build_pha.py` | `PHAPolymerBuilder._prepare_comprehensive_conformer_search` | 903 | [Read](build_pha.md#definition-903) |
| `build_pha.py` | `PHAPolymerBuilder.replace_pdb_residue_name` | 1127 | [Read](build_pha.md#definition-1127) |
| `build_pha.py` | `PHAPolymerBuilder.run_command` | 1160 | [Read](build_pha.md#definition-1160) |
| `build_pha.py` | `PHAPolymerBuilder.build_PHA_copolymer` | 1201 | [Read](build_pha.md#definition-1201) |
| `build_pha.py` | `PHAPolymerBuilder._ensure_polymer_smiles_csv_exists` | 1568 | [Read](build_pha.md#definition-1568) |
| `build_pha.py` | `PHAPolymerBuilder.get_monomer_smiles` | 1592 | [Read](build_pha.md#definition-1592) |
| `build_pha.py` | `PHAPolymerBuilder.generate_polymer_smiles_from_sequence` | 1609 | [Read](build_pha.md#definition-1609) |
| `build_pha.py` | `PHAPolymerBuilder.save_polymer_smiles` | 1649 | [Read](build_pha.md#definition-1649) |
| `build_pha.py` | `PHAPolymerBuilder._prepare_single_conformer_optimized` | 1700 | [Read](build_pha.md#definition-1700) |
| `build_pha.py` | `PHAPolymerBuilder._prepare_comprehensive_conformer_search` | 1816 | [Read](build_pha.md#definition-1816) |
| `build_single_PHA_systems.py` | `run_tleap` | 18 | [Read](build_single_PHA_systems.md#definition-18) |
| `build_single_PHA_systems.py` | `write_tleap_file` | 74 | [Read](build_single_PHA_systems.md#definition-74) |
| `build_single_PHA_systems.py` | `check_required_files` | 92 | [Read](build_single_PHA_systems.md#definition-92) |
| `build_single_PHA_systems.py` | `calculate_ion_pairs_from_rst7` | 112 | [Read](build_single_PHA_systems.md#definition-112) |
| `build_single_PHA_systems.py` | `prepare_single_system_inputs` | 165 | [Read](build_single_PHA_systems.md#definition-165) |
| `build_single_PHA_systems.py` | `build_dry_PHA` | 224 | [Read](build_single_PHA_systems.md#definition-224) |
| `build_single_PHA_systems.py` | `build_solvated_PHA` | 330 | [Read](build_single_PHA_systems.md#definition-330) |
| `build_single_PHA_systems.py` | `build_solvated_PHA_ions` | 441 | [Read](build_single_PHA_systems.md#definition-441) |
| `conversion_amber_to_gromacs.py` | `_normalize_structure_charge` | 30 | [Read](conversion_amber_to_gromacs.md#definition-30) |
| `conversion_amber_to_gromacs.py` | `convert_amber_to_gromacs` | 55 | [Read](conversion_amber_to_gromacs.md#definition-55) |
| `export.py` | `prepare_molecule_3d` | 21 | [Read](export.md#definition-21) |
| `export.py` | `to_sdf` | 40 | [Read](export.md#definition-40) |
| `export.py` | `to_pdb` | 54 | [Read](export.md#definition-54) |
| `monomers.py` | `Monomer.side_chain` | 35 | [Read](monomers.md#definition-35) |
| `monomers.py` | `Monomer.head_residue_code` | 41 | [Read](monomers.md#definition-41) |
| `monomers.py` | `Monomer.main_residue_code` | 47 | [Read](monomers.md#definition-47) |
| `monomers.py` | `Monomer.tail_residue_code` | 53 | [Read](monomers.md#definition-53) |
| `monomers.py` | `get_monomer` | 119 | [Read](monomers.md#definition-119) |
| `naming.py` | `_require_text` | 53 | [Read](naming.md#definition-53) |
| `naming.py` | `_require_positive_int` | 59 | [Read](naming.md#definition-59) |
| `naming.py` | `canonical_monomer_code` | 67 | [Read](naming.md#definition-67) |
| `naming.py` | `validate_monomer_code` | 78 | [Read](naming.md#definition-78) |
| `naming.py` | `monomer_to_polymer_code` | 89 | [Read](naming.md#definition-89) |
| `naming.py` | `validate_polymer_code` | 95 | [Read](naming.md#definition-95) |
| `naming.py` | `oligomer_name` | 106 | [Read](naming.md#definition-106) |
| `naming.py` | `validate_oligomer_name` | 113 | [Read](naming.md#definition-113) |
| `naming.py` | `multi_chain_system_name` | 135 | [Read](naming.md#definition-135) |
| `naming.py` | `validate_system_name` | 156 | [Read](naming.md#definition-156) |
| `naming.py` | `residue_variant_name` | 177 | [Read](naming.md#definition-177) |
| `naming.py` | `residue_variant_names` | 188 | [Read](naming.md#definition-188) |
| `naming.py` | `validate_pha_name` | 195 | [Read](naming.md#definition-195) |
| `openmmscript_builder.py` | `OpenMMScriptBuilder.__init__` | 69 | [Read](openmmscript_builder.md#definition-69) |
| `openmmscript_builder.py` | `OpenMMScriptBuilder.add_minimization` | 166 | [Read](openmmscript_builder.md#definition-166) |
| `openmmscript_builder.py` | `OpenMMScriptBuilder.add_basic_NVT` | 177 | [Read](openmmscript_builder.md#definition-177) |
| `openmmscript_builder.py` | `OpenMMScriptBuilder.add_basic_NPT` | 200 | [Read](openmmscript_builder.md#definition-200) |
| `openmmscript_builder.py` | `OpenMMScriptBuilder.add_anneal_NVT` | 225 | [Read](openmmscript_builder.md#definition-225) |
| `openmmscript_builder.py` | `OpenMMScriptBuilder.add_thermal_ramp` | 254 | [Read](openmmscript_builder.md#definition-254) |
| `openmmscript_builder.py` | `OpenMMScriptBuilder.to_dict` | 291 | [Read](openmmscript_builder.md#definition-291) |
| `openmmscript_builder.py` | `OpenMMScriptBuilder.from_dict` | 328 | [Read](openmmscript_builder.md#definition-328) |
| `openmmscript_builder.py` | `OpenMMScriptBuilder.save_workflow` | 460 | [Read](openmmscript_builder.md#definition-460) |
| `openmmscript_builder.py` | `OpenMMScriptBuilder.load_workflow` | 522 | [Read](openmmscript_builder.md#definition-522) |
| `openmmscript_builder.py` | `OpenMMScriptBuilder.validate` | 577 | [Read](openmmscript_builder.md#definition-577) |
| `openmmscript_builder.py` | `OpenMMScriptBuilder.write_script` | 854 | [Read](openmmscript_builder.md#definition-854) |
| `openmmscript_builder.py` | `OpenMMScriptBuilder.to_script` | 892 | [Read](openmmscript_builder.md#definition-892) |
| `openmmscript_builder.py` | `OpenMMScriptBuilder._build_steps_code` | 1109 | [Read](openmmscript_builder.md#definition-1109) |
| `openmmscript_builder.py` | `OpenMMScriptBuilder._format_basic_NVT` | 1182 | [Read](openmmscript_builder.md#definition-1182) |
| `openmmscript_builder.py` | `OpenMMScriptBuilder._format_basic_NPT` | 1199 | [Read](openmmscript_builder.md#definition-1199) |
| `openmmscript_builder.py` | `OpenMMScriptBuilder._format_anneal_NVT` | 1217 | [Read](openmmscript_builder.md#definition-1217) |
| `openmmscript_builder.py` | `OpenMMScriptBuilder._format_thermal_ramp` | 1237 | [Read](openmmscript_builder.md#definition-1237) |
| `parameterization_gaff2.py` | `_normalize_mol2_charges` | 58 | [Read](parameterization_gaff2.md#definition-58) |
| `parameterization_gaff2.py` | `ambertools_available` | 132 | [Read](parameterization_gaff2.md#definition-132) |
| `parameterization_gaff2.py` | `require_ambertools` | 138 | [Read](parameterization_gaff2.md#definition-138) |
| `parameterization_gaff2.py` | `_run_command` | 152 | [Read](parameterization_gaff2.md#definition-152) |
| `parameterization_gaff2.py` | `_write_tleap_input` | 205 | [Read](parameterization_gaff2.md#definition-205) |
| `parameterization_gaff2.py` | `_prepare_antechamber_sdf` | 230 | [Read](parameterization_gaff2.md#definition-230) |
| `parameterization_gaff2.py` | `_write_timing_log` | 250 | [Read](parameterization_gaff2.md#definition-250) |
| `parameterization_gaff2.py` | `parameterize_gaff2` | 270 | [Read](parameterization_gaff2.md#definition-270) |
| `pha_filepath_manager.py` | `PHAFileManager.__init__` | 38 | [Read](pha_filepath_manager.md#definition-38) |
| `pha_filepath_manager.py` | `PHAFileManager._create_base_structure` | 59 | [Read](pha_filepath_manager.md#definition-59) |
| `pha_filepath_manager.py` | `PHAFileManager.get_root_dir` | 84 | [Read](pha_filepath_manager.md#definition-84) |
| `pha_filepath_manager.py` | `PHAFileManager.get_temp_dir` | 87 | [Read](pha_filepath_manager.md#definition-87) |
| `pha_filepath_manager.py` | `PHAFileManager.get_residue_codes_csv` | 90 | [Read](pha_filepath_manager.md#definition-90) |
| `pha_filepath_manager.py` | `PHAFileManager.get_polymer_smiles_csv` | 93 | [Read](pha_filepath_manager.md#definition-93) |
| `pha_filepath_manager.py` | `PHAFileManager.get_md_systems_csv` | 96 | [Read](pha_filepath_manager.md#definition-96) |
| `pha_filepath_manager.py` | `PHAFileManager.get_PHA_type_dir` | 106 | [Read](pha_filepath_manager.md#definition-106) |
| `pha_filepath_manager.py` | `PHAFileManager.create_PHA_type_dir` | 109 | [Read](pha_filepath_manager.md#definition-109) |
| `pha_filepath_manager.py` | `PHAFileManager.get_PHA_input_dir` | 125 | [Read](pha_filepath_manager.md#definition-125) |
| `pha_filepath_manager.py` | `PHAFileManager.get_PHA_trimer_dir` | 128 | [Read](pha_filepath_manager.md#definition-128) |
| `pha_filepath_manager.py` | `PHAFileManager.get_PHA_monomer_units_dir` | 131 | [Read](pha_filepath_manager.md#definition-131) |
| `pha_filepath_manager.py` | `PHAFileManager.get_PHA_leap_template_dir` | 134 | [Read](pha_filepath_manager.md#definition-134) |
| `pha_filepath_manager.py` | `PHAFileManager.get_PHA_monomer_unit_files` | 137 | [Read](pha_filepath_manager.md#definition-137) |
| `pha_filepath_manager.py` | `PHAFileManager.get_built_PHA_name` | 157 | [Read](pha_filepath_manager.md#definition-157) |
| `pha_filepath_manager.py` | `PHAFileManager.parse_built_PHA_name` | 160 | [Read](pha_filepath_manager.md#definition-160) |
| `pha_filepath_manager.py` | `PHAFileManager.get_built_PHA_dir` | 183 | [Read](pha_filepath_manager.md#definition-183) |
| `pha_filepath_manager.py` | `PHAFileManager.create_built_PHA_dir` | 191 | [Read](pha_filepath_manager.md#definition-191) |
| `pha_filepath_manager.py` | `PHAFileManager.get_built_PHA_leap_dir` | 209 | [Read](pha_filepath_manager.md#definition-209) |
| `pha_filepath_manager.py` | `PHAFileManager.get_built_PHA_amber_dir` | 212 | [Read](pha_filepath_manager.md#definition-212) |
| `pha_filepath_manager.py` | `PHAFileManager.get_built_PHA_gromacs_dir` | 215 | [Read](pha_filepath_manager.md#definition-215) |
| `pha_filepath_manager.py` | `PHAFileManager.get_built_PHA_amber_files` | 218 | [Read](pha_filepath_manager.md#definition-218) |
| `pha_filepath_manager.py` | `PHAFileManager.get_PHA_dry_dir` | 241 | [Read](pha_filepath_manager.md#definition-241) |
| `pha_filepath_manager.py` | `PHAFileManager.get_dry_PHA_system_name` | 248 | [Read](pha_filepath_manager.md#definition-248) |
| `pha_filepath_manager.py` | `PHAFileManager.get_dry_PHA_dir` | 251 | [Read](pha_filepath_manager.md#definition-251) |
| `pha_filepath_manager.py` | `PHAFileManager.get_dry_PHA_inputs_dir` | 256 | [Read](pha_filepath_manager.md#definition-256) |
| `pha_filepath_manager.py` | `PHAFileManager.get_dry_PHA_simulations_dir` | 259 | [Read](pha_filepath_manager.md#definition-259) |
| `pha_filepath_manager.py` | `PHAFileManager.create_dry_PHA_dir` | 262 | [Read](pha_filepath_manager.md#definition-262) |
| `pha_filepath_manager.py` | `PHAFileManager.get_PHA_solvated_dir` | 286 | [Read](pha_filepath_manager.md#definition-286) |
| `pha_filepath_manager.py` | `PHAFileManager.get_solvated_PHA_system_name` | 293 | [Read](pha_filepath_manager.md#definition-293) |
| `pha_filepath_manager.py` | `PHAFileManager.get_solvated_PHA_dir` | 296 | [Read](pha_filepath_manager.md#definition-296) |
| `pha_filepath_manager.py` | `PHAFileManager.get_solvated_PHA_inputs_dir` | 301 | [Read](pha_filepath_manager.md#definition-301) |
| `pha_filepath_manager.py` | `PHAFileManager.get_solvated_PHA_simulations_dir` | 304 | [Read](pha_filepath_manager.md#definition-304) |
| `pha_filepath_manager.py` | `PHAFileManager.create_solvated_PHA_dir` | 307 | [Read](pha_filepath_manager.md#definition-307) |
| `pha_filepath_manager.py` | `PHAFileManager.get_PHA_solvated_ions_dir` | 331 | [Read](pha_filepath_manager.md#definition-331) |
| `pha_filepath_manager.py` | `PHAFileManager.format_concentration_label` | 337 | [Read](pha_filepath_manager.md#definition-337) |
| `pha_filepath_manager.py` | `PHAFileManager.get_solvated_ions_PHA_system_name` | 347 | [Read](pha_filepath_manager.md#definition-347) |
| `pha_filepath_manager.py` | `PHAFileManager.get_solvated_ions_PHA_dir` | 369 | [Read](pha_filepath_manager.md#definition-369) |
| `pha_filepath_manager.py` | `PHAFileManager.get_solvated_ions_PHA_inputs_dir` | 386 | [Read](pha_filepath_manager.md#definition-386) |
| `pha_filepath_manager.py` | `PHAFileManager.get_solvated_ions_PHA_simulations_dir` | 404 | [Read](pha_filepath_manager.md#definition-404) |
| `pha_filepath_manager.py` | `PHAFileManager.create_solvated_ions_PHA_dir` | 422 | [Read](pha_filepath_manager.md#definition-422) |
| `pha_filepath_manager.py` | `PHAFileManager.get_PHA_melt_name` | 465 | [Read](pha_filepath_manager.md#definition-465) |
| `pha_filepath_manager.py` | `PHAFileManager.get_PHA_melt_dir` | 488 | [Read](pha_filepath_manager.md#definition-488) |
| `pha_filepath_manager.py` | `PHAFileManager.create_PHA_melt_dir` | 500 | [Read](pha_filepath_manager.md#definition-500) |
| `pha_filepath_manager.py` | `PHAFileManager.get_PHA_melt_inputs_dir` | 533 | [Read](pha_filepath_manager.md#definition-533) |
| `pha_filepath_manager.py` | `PHAFileManager.get_PHA_melt_simulations_dir` | 546 | [Read](pha_filepath_manager.md#definition-546) |
| `pha_filepath_manager.py` | `PHAFileManager.create_PHA_melt_simulation_run_dir` | 559 | [Read](pha_filepath_manager.md#definition-559) |
| `pha_filepath_manager.py` | `PHAFileManager.create_named_PHA_melt_simulation_run_dir` | 587 | [Read](pha_filepath_manager.md#definition-587) |
| `pha_filepath_manager.py` | `PHAFileManager.ensure_md_systems_csv_exists` | 630 | [Read](pha_filepath_manager.md#definition-630) |
| `pha_filepath_manager.py` | `PHAFileManager.load_md_systems` | 657 | [Read](pha_filepath_manager.md#definition-657) |
| `pha_filepath_manager.py` | `PHAFileManager.get_md_system` | 677 | [Read](pha_filepath_manager.md#definition-677) |
| `pha_filepath_manager.py` | `PHAFileManager.md_system_exists` | 707 | [Read](pha_filepath_manager.md#definition-707) |
| `pha_filepath_manager.py` | `PHAFileManager.register_md_system` | 719 | [Read](pha_filepath_manager.md#definition-719) |
| `pha_filepath_manager.py` | `PHAFileManager.get_md_system_files` | 825 | [Read](pha_filepath_manager.md#definition-825) |
| `pha_filepath_manager.py` | `PHAFileManager.get_md_system_workflows_dir` | 918 | [Read](pha_filepath_manager.md#definition-918) |
| `pha_filepath_manager.py` | `PHAFileManager.get_md_system_workflow_path` | 964 | [Read](pha_filepath_manager.md#definition-964) |
| `pha_filepath_manager.py` | `PHAFileManager.list_md_system_workflows` | 1047 | [Read](pha_filepath_manager.md#definition-1047) |
| `pha_filepath_manager.py` | `PHAFileManager.create_named_md_system_simulation_run_dir` | 1089 | [Read](pha_filepath_manager.md#definition-1089) |
| `pha_filepath_manager.py` | `PHAFileManager.validate_md_system_files` | 1149 | [Read](pha_filepath_manager.md#definition-1149) |
| `pha_filepath_manager.py` | `PHAFileManager.find_file` | 1189 | [Read](pha_filepath_manager.md#definition-1189) |
| `pha_filepath_manager.py` | `PHAFileManager.find_files` | 1201 | [Read](pha_filepath_manager.md#definition-1201) |
| `pha_filepath_manager.py` | `PHAFileManager.count_atoms_from_amber_topology` | 1208 | [Read](pha_filepath_manager.md#definition-1208) |
| `pha_filepath_manager.py` | `PHAFileManager.count_atoms_from_gromacs_gro` | 1226 | [Read](pha_filepath_manager.md#definition-1226) |
| `pha_filepath_manager.py` | `PHAResidueCodeManager.__init__` | 1311 | [Read](pha_filepath_manager.md#definition-1311) |
| `pha_filepath_manager.py` | `PHAResidueCodeManager._ensure_csv_exists` | 1324 | [Read](pha_filepath_manager.md#definition-1324) |
| `pha_filepath_manager.py` | `PHAResidueCodeManager.load_rows` | 1334 | [Read](pha_filepath_manager.md#definition-1334) |
| `pha_filepath_manager.py` | `PHAResidueCodeManager.get_used_codes` | 1347 | [Read](pha_filepath_manager.md#definition-1347) |
| `pha_filepath_manager.py` | `PHAResidueCodeManager.PHA_type_exists` | 1359 | [Read](pha_filepath_manager.md#definition-1359) |
| `pha_filepath_manager.py` | `PHAResidueCodeManager.get_code` | 1374 | [Read](pha_filepath_manager.md#definition-1374) |
| `pha_filepath_manager.py` | `PHAResidueCodeManager.generate_unique_codes` | 1400 | [Read](pha_filepath_manager.md#definition-1400) |
| `pha_filepath_manager.py` | `PHAResidueCodeManager.register_PHA_type` | 1444 | [Read](pha_filepath_manager.md#definition-1444) |
| `pha_melt_builder.py` | `PHAMeltBuilder.__init__` | 37 | [Read](pha_melt_builder.md#definition-37) |
| `pha_melt_builder.py` | `PHAMeltBuilder.run_command` | 41 | [Read](pha_melt_builder.md#definition-41) |
| `pha_melt_builder.py` | `PHAMeltBuilder.parse_polymer_name` | 71 | [Read](pha_melt_builder.md#definition-71) |
| `pha_melt_builder.py` | `PHAMeltBuilder.get_melt_name` | 82 | [Read](pha_melt_builder.md#definition-82) |
| `pha_melt_builder.py` | `PHAMeltBuilder.validate_melt_inputs` | 95 | [Read](pha_melt_builder.md#definition-95) |
| `pha_melt_builder.py` | `PHAMeltBuilder.ensure_built_polymer_exists` | 120 | [Read](pha_melt_builder.md#definition-120) |
| `pha_melt_builder.py` | `PHAMeltBuilder.ensure_gromacs_polymer_exists` | 163 | [Read](pha_melt_builder.md#definition-163) |
| `pha_melt_builder.py` | `PHAMeltBuilder.generate_polymer_melt` | 204 | [Read](pha_melt_builder.md#definition-204) |
| `pha_melt_builder.py` | `PHAMeltBuilder.run_acpype` | 291 | [Read](pha_melt_builder.md#definition-291) |
| `pha_melt_builder.py` | `PHAMeltBuilder.prepare_polyply_inputs` | 420 | [Read](pha_melt_builder.md#definition-420) |
| `pha_melt_builder.py` | `PHAMeltBuilder.run_polyply` | 503 | [Read](pha_melt_builder.md#definition-503) |
| `pha_melt_builder.py` | `PHAMeltBuilder.combine_itps` | 568 | [Read](pha_melt_builder.md#definition-568) |
| `pha_melt_builder.py` | `PHAMeltBuilder.edit_acpype_topology_for_polyply` | 612 | [Read](pha_melt_builder.md#definition-612) |
| `pha_melt_builder.py` | `PHAMeltBuilder.test_polymer_melt_simulation` | 671 | [Read](pha_melt_builder.md#definition-671) |
| `simulation_gromacs_runner.py` | `GromacsTopologyValidation.valid` | 66 | [Read](simulation_gromacs_runner.md#definition-66) |
| `simulation_gromacs_runner.py` | `GromacsLocalMinimizationCheck.ready` | 80 | [Read](simulation_gromacs_runner.md#definition-80) |
| `simulation_gromacs_runner.py` | `GromacsLocalMinimizationCheck.command_text` | 84 | [Read](simulation_gromacs_runner.md#definition-84) |
| `simulation_gromacs_runner.py` | `GromacsBoxValidation.max_cutoff_nm` | 99 | [Read](simulation_gromacs_runner.md#definition-99) |
| `simulation_gromacs_runner.py` | `GromacsBoxValidation.valid` | 105 | [Read](simulation_gromacs_runner.md#definition-105) |
| `simulation_gromacs_runner.py` | `GromacsSolvationFiles.tip3p_ions_itp_path` | 127 | [Read](simulation_gromacs_runner.md#definition-127) |
| `simulation_gromacs_runner.py` | `GromacsSolvatedTopologyValidation.sodium_count` | 144 | [Read](simulation_gromacs_runner.md#definition-144) |
| `simulation_gromacs_runner.py` | `GromacsSolvatedTopologyValidation.chloride_count` | 150 | [Read](simulation_gromacs_runner.md#definition-150) |
| `simulation_gromacs_runner.py` | `GromacsSolvatedTopologyValidation.has_water` | 156 | [Read](simulation_gromacs_runner.md#definition-156) |
| `simulation_gromacs_runner.py` | `GromacsSolvatedTopologyValidation.has_ions` | 160 | [Read](simulation_gromacs_runner.md#definition-160) |
| `simulation_gromacs_runner.py` | `GromacsGromppValidation.ok` | 174 | [Read](simulation_gromacs_runner.md#definition-174) |
| `simulation_gromacs_runner.py` | `GromacsCoordinateTopologyValidation.can_compare` | 190 | [Read](simulation_gromacs_runner.md#definition-190) |
| `simulation_gromacs_runner.py` | `GromacsCoordinateTopologyValidation.valid` | 194 | [Read](simulation_gromacs_runner.md#definition-194) |
| `simulation_gromacs_runner.py` | `_run_script` | 357 | [Read](simulation_gromacs_runner.md#definition-357) |
| `simulation_gromacs_runner.py` | `write_gromacs_run_files` | 379 | [Read](simulation_gromacs_runner.md#definition-379) |
| `simulation_gromacs_runner.py` | `_copy_mdp_templates` | 414 | [Read](simulation_gromacs_runner.md#definition-414) |
| `simulation_gromacs_runner.py` | `_copy_workflow_inputs` | 428 | [Read](simulation_gromacs_runner.md#definition-428) |
| `simulation_gromacs_runner.py` | `_copy_solvation_templates` | 449 | [Read](simulation_gromacs_runner.md#definition-449) |
| `simulation_gromacs_runner.py` | `_read_gro_atom_count` | 465 | [Read](simulation_gromacs_runner.md#definition-465) |
| `simulation_gromacs_runner.py` | `_write_default_index` | 475 | [Read](simulation_gromacs_runner.md#definition-475) |
| `simulation_gromacs_runner.py` | `_read_gro_box_vectors` | 485 | [Read](simulation_gromacs_runner.md#definition-485) |
| `simulation_gromacs_runner.py` | `_read_mdp_cutoffs` | 502 | [Read](simulation_gromacs_runner.md#definition-502) |
| `simulation_gromacs_runner.py` | `create_gromacs_simulation_box` | 519 | [Read](simulation_gromacs_runner.md#definition-519) |
| `simulation_gromacs_runner.py` | `validate_gromacs_box_against_mdp` | 570 | [Read](simulation_gromacs_runner.md#definition-570) |
| `simulation_gromacs_runner.py` | `_write_local_minimization_script` | 601 | [Read](simulation_gromacs_runner.md#definition-601) |
| `simulation_gromacs_runner.py` | `_write_hpc_equilibration_script` | 679 | [Read](simulation_gromacs_runner.md#definition-679) |
| `simulation_gromacs_runner.py` | `_write_kcl_polymer_hpc_script` | 729 | [Read](simulation_gromacs_runner.md#definition-729) |
| `simulation_gromacs_runner.py` | `_infer_polymer_hpc_job_name` | 771 | [Read](simulation_gromacs_runner.md#definition-771) |
| `simulation_gromacs_runner.py` | `_write_solvate_script` | 777 | [Read](simulation_gromacs_runner.md#definition-777) |
| `simulation_gromacs_runner.py` | `_ensure_topology_include` | 1055 | [Read](simulation_gromacs_runner.md#definition-1055) |
| `simulation_gromacs_runner.py` | `_write_solvation_topology_templates` | 1077 | [Read](simulation_gromacs_runner.md#definition-1077) |
| `simulation_gromacs_runner.py` | `_read_topology_molecule_counts` | 1087 | [Read](simulation_gromacs_runner.md#definition-1087) |
| `simulation_gromacs_runner.py` | `_topology_source_paths` | 1111 | [Read](simulation_gromacs_runner.md#definition-1111) |
| `simulation_gromacs_runner.py` | `_read_moleculetype_atom_counts` | 1125 | [Read](simulation_gromacs_runner.md#definition-1125) |
| `simulation_gromacs_runner.py` | `count_gro_atoms` | 1155 | [Read](simulation_gromacs_runner.md#definition-1155) |
| `simulation_gromacs_runner.py` | `validate_gromacs_coordinate_topology_counts` | 1168 | [Read](simulation_gromacs_runner.md#definition-1168) |
| `simulation_gromacs_runner.py` | `_sum_named_molecule_counts` | 1205 | [Read](simulation_gromacs_runner.md#definition-1205) |
| `simulation_gromacs_runner.py` | `_resolve_solvated_polymer_dir` | 1215 | [Read](simulation_gromacs_runner.md#definition-1215) |
| `simulation_gromacs_runner.py` | `_populate_solvated_polymer_inputs` | 1225 | [Read](simulation_gromacs_runner.md#definition-1225) |
| `simulation_gromacs_runner.py` | `_clean_solvated_polymer_generated_files` | 1239 | [Read](simulation_gromacs_runner.md#definition-1239) |
| `simulation_gromacs_runner.py` | `write_gromacs_solvation_files` | 1270 | [Read](simulation_gromacs_runner.md#definition-1270) |
| `simulation_gromacs_runner.py` | `validate_gromacs_solvated_topology` | 1336 | [Read](simulation_gromacs_runner.md#definition-1336) |
| `simulation_gromacs_runner.py` | `validate_gromacs_solvation_grompp` | 1359 | [Read](simulation_gromacs_runner.md#definition-1359) |
| `simulation_gromacs_runner.py` | `validate_gromacs_run_folder` | 1422 | [Read](simulation_gromacs_runner.md#definition-1422) |
| `simulation_gromacs_runner.py` | `check_gromacs_minimization_inputs` | 1458 | [Read](simulation_gromacs_runner.md#definition-1458) |
| `simulation_gromacs_runner.py` | `run_gromacs_local_minimization` | 1476 | [Read](simulation_gromacs_runner.md#definition-1476) |
| `simulation_gromacs_runner.py` | `prepare_gromacs_run_folder` | 1505 | [Read](simulation_gromacs_runner.md#definition-1505) |
| `simulation_openmm_amber_runner.py` | `openmm_available` | 49 | [Read](simulation_openmm_amber_runner.md#definition-49) |
| `simulation_openmm_amber_runner.py` | `_platform` | 60 | [Read](simulation_openmm_amber_runner.md#definition-60) |
| `simulation_openmm_amber_runner.py` | `_simulation` | 72 | [Read](simulation_openmm_amber_runner.md#definition-72) |
| `simulation_openmm_amber_runner.py` | `_write_pdb` | 78 | [Read](simulation_openmm_amber_runner.md#definition-78) |
| `simulation_openmm_amber_runner.py` | `_append_stage_reporters` | 83 | [Read](simulation_openmm_amber_runner.md#definition-83) |
| `simulation_openmm_amber_runner.py` | `_run_stage` | 113 | [Read](simulation_openmm_amber_runner.md#definition-113) |
| `simulation_openmm_amber_runner.py` | `_write_summary` | 120 | [Read](simulation_openmm_amber_runner.md#definition-120) |
| `simulation_openmm_amber_runner.py` | `_temperature_schedule` | 135 | [Read](simulation_openmm_amber_runner.md#definition-135) |
| `simulation_openmm_amber_runner.py` | `run_openmm_with_amber_topology` | 159 | [Read](simulation_openmm_amber_runner.md#definition-159) |
| `simulation_openmm_amber_runner.py` | `run_openmm_with_amber_topology.create_system` | 219 | [Read](simulation_openmm_amber_runner.md#definition-219) |
| `simulation_openmm_amber_runner.py` | `run_openmm_with_amber_topology.create_integrator` | 234 | [Read](simulation_openmm_amber_runner.md#definition-234) |
| `simulation_openmm_amber_runner.py` | `run_openmm_with_amber_topology.set_initial_context` | 241 | [Read](simulation_openmm_amber_runner.md#definition-241) |
| `stereochemistry.py` | `validate_stereochemistry_option` | 14 | [Read](stereochemistry.md#definition-14) |
| `stereochemistry.py` | `validate_chiral_centres` | 26 | [Read](stereochemistry.md#definition-26) |
| `stereochemistry.py` | `validate_r_chiral_centres` | 51 | [Read](stereochemistry.md#definition-51) |
| `sw_openmm.py` | `DcdWriter.__init__` | 23 | [Read](sw_openmm.md#definition-23) |
| `sw_openmm.py` | `DataWriter.__init__` | 34 | [Read](sw_openmm.md#definition-34) |
| `sw_openmm.py` | `BuildSimulation.__init__` | 94 | [Read](sw_openmm.md#definition-94) |
| `sw_openmm.py` | `BuildSimulation.type_of_simulation` | 135 | [Read](sw_openmm.md#definition-135) |
| `sw_openmm.py` | `BuildSimulation.get_platform` | 147 | [Read](sw_openmm.md#definition-147) |
| `sw_openmm.py` | `BuildSimulation.get_platform.configure_platform` | 195 | [Read](sw_openmm.md#definition-195) |
| `sw_openmm.py` | `BuildSimulation.create_openmm_system` | 286 | [Read](sw_openmm.md#definition-286) |
| `sw_openmm.py` | `BuildSimulation.create_openmm_simulation` | 328 | [Read](sw_openmm.md#definition-328) |
| `sw_openmm.py` | `BuildSimulation.minimize_energy` | 356 | [Read](sw_openmm.md#definition-356) |
| `sw_openmm.py` | `BuildSimulation.minimize_energy_help` | 416 | [Read](sw_openmm.md#definition-416) |
| `sw_openmm.py` | `BuildSimulation.anneal_NVT` | 419 | [Read](sw_openmm.md#definition-419) |
| `sw_openmm.py` | `BuildSimulation.anneal_NVT.cycle` | 556 | [Read](sw_openmm.md#definition-556) |
| `sw_openmm.py` | `BuildSimulation.anneal_help` | 637 | [Read](sw_openmm.md#definition-637) |
| `sw_openmm.py` | `BuildSimulation.basic_NPT` | 642 | [Read](sw_openmm.md#definition-642) |
| `sw_openmm.py` | `BuildSimulation.basic_NPT_help` | 820 | [Read](sw_openmm.md#definition-820) |
| `sw_openmm.py` | `BuildSimulation.basic_NVT` | 825 | [Read](sw_openmm.md#definition-825) |
| `sw_openmm.py` | `BuildSimulation.thermal_ramp` | 981 | [Read](sw_openmm.md#definition-981) |
| `sw_openmm.py` | `BuildSimulation.save_rst` | 1199 | [Read](sw_openmm.md#definition-1199) |
| `sw_openmm.py` | `BuildSimulation.restrain_heavy_atoms` | 1261 | [Read](sw_openmm.md#definition-1261) |
| `sw_openmm.py` | `BuildSimulation.__repr__` | 1292 | [Read](sw_openmm.md#definition-1292) |
| `sw_openmm.py` | `BuildSimulation.__str__` | 1317 | [Read](sw_openmm.md#definition-1317) |
| `sw_openmm.py` | `BuildSimulation.display_start_time` | 1321 | [Read](sw_openmm.md#definition-1321) |
| `sw_openmm.py` | `BuildSimulation.savepdb_trajectories` | 1328 | [Read](sw_openmm.md#definition-1328) |
| `sw_openmm.py` | `BuildSimulation.set_temperature` | 1346 | [Read](sw_openmm.md#definition-1346) |
| `sw_openmm.py` | `BuildSimulation.set_pressure` | 1356 | [Read](sw_openmm.md#definition-1356) |
| `sw_openmm.py` | `BuildSimulation.set_timestep` | 1366 | [Read](sw_openmm.md#definition-1366) |
| `sw_openmm.py` | `BuildSimulation.set_friction_coeff` | 1375 | [Read](sw_openmm.md#definition-1375) |
| `sw_openmm.py` | `BuildSimulation.set_total_steps` | 1384 | [Read](sw_openmm.md#definition-1384) |
| `sw_openmm.py` | `BuildSimulation.set_reporter_freq` | 1393 | [Read](sw_openmm.md#definition-1393) |
| `sw_openmm.py` | `BuildSimulation.set_nonbondedcutoff` | 1403 | [Read](sw_openmm.md#definition-1403) |
| `sw_openmm.py` | `BuildSimulation.set_anneal_parameters` | 1417 | [Read](sw_openmm.md#definition-1417) |
| `sw_openmm.py` | `BuildSimulation.set_anneal_parameters_help` | 1438 | [Read](sw_openmm.md#definition-1438) |
| `sw_openmm.py` | `BuildSimulation.graph_state_data` | 1442 | [Read](sw_openmm.md#definition-1442) |
| `sw_openmm.py` | `BuildSimulation.graph_state_data_help` | 1516 | [Read](sw_openmm.md#definition-1516) |
| `sw_openmm.py` | `GromacsSimulation.__new__` | 1528 | [Read](sw_openmm.md#definition-1528) |
| `sw_openmm.py` | `GromacsSimulation.__init__` | 1552 | [Read](sw_openmm.md#definition-1552) |
| `sw_openmm.py` | `GromacsSimulation.__str__` | 1602 | [Read](sw_openmm.md#definition-1602) |
| `sw_openmm.py` | `AmberSimulation.__new__` | 1612 | [Read](sw_openmm.md#definition-1612) |
| `sw_openmm.py` | `AmberSimulation.__init__` | 1626 | [Read](sw_openmm.md#definition-1626) |
| `sw_openmm.py` | `AmberSimulation.__str__` | 1657 | [Read](sw_openmm.md#definition-1657) |
| `system_builder_packmol.py` | `estimate_tip3p_water_count` | 65 | [Read](system_builder_packmol.md#definition-65) |
| `system_builder_packmol.py` | `estimate_ion_pairs` | 73 | [Read](system_builder_packmol.md#definition-73) |
| `system_builder_packmol.py` | `_normalise_polymer_counts` | 88 | [Read](system_builder_packmol.md#definition-88) |
| `system_builder_packmol.py` | `_copy_polymer_structures` | 107 | [Read](system_builder_packmol.md#definition-107) |
| `system_builder_packmol.py` | `_write_support_structures` | 122 | [Read](system_builder_packmol.md#definition-122) |
| `system_builder_packmol.py` | `_structure_block` | 135 | [Read](system_builder_packmol.md#definition-135) |
| `system_builder_packmol.py` | `_write_packmol_input` | 161 | [Read](system_builder_packmol.md#definition-161) |
| `system_builder_packmol.py` | `_ensure_cryst1_record` | 227 | [Read](system_builder_packmol.md#definition-227) |
| `system_builder_packmol.py` | `build_packmol_solvated_system` | 239 | [Read](system_builder_packmol.md#definition-239) |
| `trajectory_centering.py` | `GromacsIndex.names` | 31 | [Read](trajectory_centering.md#definition-31) |
| `trajectory_centering.py` | `GromacsIndex.has_group` | 34 | [Read](trajectory_centering.md#definition-34) |
| `trajectory_centering.py` | `GromacsIndex.group` | 39 | [Read](trajectory_centering.md#definition-39) |
| `trajectory_centering.py` | `_canonical_group_name` | 58 | [Read](trajectory_centering.md#definition-58) |
| `trajectory_centering.py` | `read_index` | 62 | [Read](trajectory_centering.md#definition-62) |
| `trajectory_centering.py` | `write_index` | 96 | [Read](trajectory_centering.md#definition-96) |
| `trajectory_centering.py` | `resolve_center_source_groups` | 114 | [Read](trajectory_centering.md#definition-114) |
| `trajectory_centering.py` | `merged_group_atoms` | 149 | [Read](trajectory_centering.md#definition-149) |
| `trajectory_centering.py` | `ensure_center_index` | 158 | [Read](trajectory_centering.md#definition-158) |
| `trajectory_frame_extraction.py` | `extract_frame` | 11 | [Read](trajectory_frame_extraction.md#definition-11) |
| `trajectory_frame_extraction.py` | `extract_first_frame` | 45 | [Read](trajectory_frame_extraction.md#definition-45) |
| `trajectory_gromacs_trjconv.py` | `TrjconvResult.ok` | 26 | [Read](trajectory_gromacs_trjconv.md#definition-26) |
| `trajectory_gromacs_trjconv.py` | `_selection_input` | 30 | [Read](trajectory_gromacs_trjconv.md#definition-30) |
| `trajectory_gromacs_trjconv.py` | `run_trjconv` | 34 | [Read](trajectory_gromacs_trjconv.md#definition-34) |
| `trajectory_gromacs_trjconv.py` | `center_and_compact_wrap` | 88 | [Read](trajectory_gromacs_trjconv.md#definition-88) |
| `trajectory_gromacs_trjconv.py` | `reconstruct_molecules` | 115 | [Read](trajectory_gromacs_trjconv.md#definition-115) |
| `trajectory_gromacs_trjconv.py` | `compact_wrap` | 141 | [Read](trajectory_gromacs_trjconv.md#definition-141) |
| `trajectory_gromacs_trjconv.py` | `fit_trajectory` | 167 | [Read](trajectory_gromacs_trjconv.md#definition-167) |
| `trajectory_preprocessing.py` | `TrajectoryPreprocessingOutputs.analysis_trajectory_path` | 35 | [Read](trajectory_preprocessing.md#definition-35) |
| `trajectory_preprocessing.py` | `_resolve_existing_path` | 39 | [Read](trajectory_preprocessing.md#definition-39) |
| `trajectory_preprocessing.py` | `preprocess_gromacs_trajectory` | 47 | [Read](trajectory_preprocessing.md#definition-47) |
| `visualisation/visualiser.py` | `load_available_PHA_monomers` | 16 | [Read](visualisation__visualiser.md#definition-16) |
| `visualisation/visualiser.py` | `smiles_to_mol` | 67 | [Read](visualisation__visualiser.md#definition-67) |
| `visualisation/visualiser.py` | `plot_available_PHA_monomers` | 102 | [Read](visualisation__visualiser.md#definition-102) |
| `visualisation/visualiser.py` | `show_available_PHA_monomers` | 185 | [Read](visualisation__visualiser.md#definition-185) |
| `visualisation/visualiser.py` | `show_PHA_monomer` | 234 | [Read](visualisation__visualiser.md#definition-234) |
| `visualisation/visualiser.py` | `load_polymer_smiles` | 312 | [Read](visualisation__visualiser.md#definition-312) |
| `visualisation/visualiser.py` | `plot_available_PHA_polymers` | 377 | [Read](visualisation__visualiser.md#definition-377) |
| `visualisation/visualiser.py` | `show_available_PHA_polymers` | 433 | [Read](visualisation__visualiser.md#definition-433) |
| `visualisation/visualiser.py` | `show_PHA_polymer` | 486 | [Read](visualisation__visualiser.md#definition-486) |
| `workflows/design.py` | `supported_polymer_table` | 30 | [Read](workflows__design.md#definition-30) |
| `workflows/design.py` | `_selected_design_modes` | 49 | [Read](workflows__design.md#definition-49) |
| `workflows/design.py` | `design_polymer` | 60 | [Read](workflows__design.md#definition-60) |
| `workflows/hpc.py` | `_deep_merge` | 53 | [Read](workflows__hpc.md#definition-53) |
| `workflows/hpc.py` | `load_workflow_config` | 63 | [Read](workflows__hpc.md#definition-63) |
| `workflows/hpc.py` | `targets_from_config` | 74 | [Read](workflows__hpc.md#definition-74) |
| `workflows/hpc.py` | `target_stage_name` | 95 | [Read](workflows__hpc.md#definition-95) |
| `workflows/hpc.py` | `workflow_plan` | 101 | [Read](workflows__hpc.md#definition-101) |
| `workflows/hpc.py` | `render_slurm_script` | 127 | [Read](workflows__hpc.md#definition-127) |
| `workflows/md_benchmark.py` | `BenchmarkTarget.gaff2_dir` | 38 | [Read](workflows__md_benchmark.md#definition-38) |
| `workflows/md_benchmark.py` | `BenchmarkTarget.prmtop_path` | 42 | [Read](workflows__md_benchmark.md#definition-42) |
| `workflows/md_benchmark.py` | `BenchmarkTarget.inpcrd_path` | 46 | [Read](workflows__md_benchmark.md#definition-46) |
| `workflows/md_benchmark.py` | `BenchmarkTarget.openmm_dir` | 50 | [Read](workflows__md_benchmark.md#definition-50) |
| `workflows/md_benchmark.py` | `BenchmarkTarget.gromacs_dir` | 54 | [Read](workflows__md_benchmark.md#definition-54) |
| `workflows/md_benchmark.py` | `_find_sdf` | 58 | [Read](workflows__md_benchmark.md#definition-58) |
| `workflows/md_benchmark.py` | `discover_targets` | 72 | [Read](workflows__md_benchmark.md#definition-72) |
| `workflows/md_benchmark.py` | `selected_system_names` | 100 | [Read](workflows__md_benchmark.md#definition-100) |
| `workflows/md_benchmark.py` | `_run_gaff2` | 112 | [Read](workflows__md_benchmark.md#definition-112) |
| `workflows/md_benchmark.py` | `_run_openmm` | 145 | [Read](workflows__md_benchmark.md#definition-145) |
| `workflows/md_benchmark.py` | `_prepare_gromacs` | 168 | [Read](workflows__md_benchmark.md#definition-168) |
| `workflows/md_benchmark.py` | `run_benchmark` | 193 | [Read](workflows__md_benchmark.md#definition-193) |
| `workflows/md_benchmark.py` | `parse_args` | 258 | [Read](workflows__md_benchmark.md#definition-258) |
| `workflows/md_benchmark.py` | `main` | 356 | [Read](workflows__md_benchmark.md#definition-356) |
| `workflows/validation.py` | `ValidationTarget.name` | 24 | [Read](workflows__validation.md#definition-24) |
| `workflows/validation.py` | `build_validation_molecules` | 41 | [Read](workflows__validation.md#definition-41) |
| `workflows/validation.py` | `describe_molecules` | 56 | [Read](workflows__validation.md#definition-56) |
| `workflows/validation.py` | `export_molecules` | 76 | [Read](workflows__validation.md#definition-76) |

## Maintain this reference

[coverage_manifest.json](coverage_manifest.json) stores the source hashes and exact definition inventory. It allows coverage to be checked without importing scientific dependencies.

After package changes, regenerate these tutorial reference pages with:

```bash
python tutorials/reference/build_reference.py
```

The generator only reads package syntax and writes tutorial reference pages. Review its human-written module notes when behaviour changes; regenerated source inventories do not automatically update those interpretations.
