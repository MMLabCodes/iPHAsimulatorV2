# Workshop support

Learners can leave this directory alone. The lessons keep the package calls and
their inputs visible while these helpers handle repeated setup, output protection,
file checks, records and presentation. No package implementation is replaced.

`workshop_helpers.py` is shared by both courses. The small same-named files in
`core/` and `advanced/` load it when a saved lesson is run as a script.
`records_and_checks.py` holds the more detailed environment, chain-consistency and
provenance operations. Scientific imports are delayed until they are needed.

The default output root is `~/iphasimulator_workshop`, overridable with
`IPHA_WORKSHOP`. Mutation helpers protect existing build/analysis destinations.
New simulation executions create numbered runs. Derived drawings and plots can
be regenerated at the same filename. Figures are saved even without an inline
display; helpers do not open external applications or submit cluster jobs.

To maintain a lesson, keep its three cells readable and move repetitive mechanics
here. Preserve meaningful checks, show units next to inputs, and explain what a
successful check does and does not establish. Keep the function reference separate
from the beginner exercises.
