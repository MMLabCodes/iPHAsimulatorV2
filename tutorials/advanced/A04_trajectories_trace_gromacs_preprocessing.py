"""Centre a native GROMACS trajectory and extract a frame. Read the A04 guide.
Use a fresh dataset copy containing only the three input files listed below.
"""

# %% 1. Get ready
from workshop_helpers import prepare_workshop, prepare_gromacs_dataset, check_output_files
workshop = prepare_workshop(commands=("gmx",), require_database=False)
from iphasimulator.trajectory_preprocessing import preprocess_gromacs_trajectory

# %% 2. Process our trajectory
# Inputs: trajectory, matching structure, and an index defining atom groups.
# 'Polymer' must exactly match a group in your index; the helper prints available groups.
trajectory = "step7_production.xtc"
structure = "step7_production.tpr"
index = "index.ndx"
groups = ["Polymer"]
folder = prepare_gromacs_dataset(workshop, "gromacs_example", trajectory, structure, index, groups)

# Output: a centred trajectory plus one representative structure to inspect.
result = preprocess_gromacs_trajectory(
    folder, trajectory=trajectory, structure=structure, index=index,
    source_groups=groups, fit=False, extract_representative_frame=True,
)

# %% 3. Check the outputs
check_output_files(result.analysis_trajectory_path, result.representative_frame_path)
print("Open this frame in your molecular viewer:", result.representative_frame_path)
# Check that the polymer is whole and centred, and that atom ordering is still correct.
# This route processes GROMACS data; it is not the OpenMM DCD route used in lesson 12.
