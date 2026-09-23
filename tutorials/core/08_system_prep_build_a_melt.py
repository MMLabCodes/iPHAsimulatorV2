"""Pack several polymer chains into a starting melt structure.
The current backend can add an extra chain. The final check stops if that happens.
"""

# %% 1. Get ready
from workshop_helpers import prepare_workshop, prepare_system, check_melt, plot_counts
workshop = prepare_workshop(modules=("openmm", "parmed", "matplotlib"), commands=("acpype", "polyply"))
from iphasimulator.pha_melt_builder import PHAMeltBuilder

# %% 2. Pack our chains
# Inputs: the built chain, number of copies, and initial density in kg/m³.
# 750 kg/m³ is 0.75 g/cm³. This is starting packing, not an equilibrated melt.
polymer_name = "P3HB_10"
number_of_chains = 25
initial_density = 750.0
prepared = prepare_system(workshop, polymer_name, "melt", chains=number_of_chains, density=initial_density)
builder = PHAMeltBuilder(workshop.database)

# Output: GROMACS topology (.top/.itp) and coordinates (.gro).
result = builder.generate_polymer_melt(
    polymer_names=[polymer_name],
    number_of_polymers=[number_of_chains],
    density=initial_density,
)

# %% 3. Check the result
# Compare requested atoms with atoms in the coordinates and topology.
# If the counts differ, keep the files for diagnosis and stop before simulation.
counts = check_melt(result, prepared)
plot_counts(workshop, counts, "Melt atom-count check", "08_melt_atom_counts.png")
# All three bars should agree. Packing still needs a 3D inspection and equilibration.
print("Coordinates for your molecular viewer:", result["coordinate_file"])
