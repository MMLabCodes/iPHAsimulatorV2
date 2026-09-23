"""Load shared workshop support. Learners do not need to edit this file."""
from pathlib import Path
import sys

_tutorials = str(Path(__file__).resolve().parents[1])
if _tutorials not in sys.path:
    sys.path.insert(0, _tutorials)
from _support.workshop_helpers import *
