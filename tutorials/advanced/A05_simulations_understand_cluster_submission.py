"""Read the supplied cluster settings and job script. No job is submitted."""

# %% 1. Get ready
from workshop_helpers import prepare_workshop, read_cluster_example
workshop = prepare_workshop(modules=("yaml",), require_database=False)

# %% 2. Read the cluster example
# Inputs: the existing example YAML settings and Slurm shell script.
# Output: their contents, ready to inspect; no script is generated or executed.
# The older workflow has an import error, so this lesson reads the files directly.
example = read_cluster_example(workshop)

# %% 3. Inspect the preview
print("Configured stages:", example.settings["stages"])
print("Requested cluster resources:", example.settings["slurm"])
print(example.script)
# Check account, partition, Python environment and every path with your cluster team.
# The example can reference research paths: prepare a dedicated cluster workspace first.
print("Preview complete. Nothing was submitted.")
