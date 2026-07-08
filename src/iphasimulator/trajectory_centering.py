"""Index-file helpers for reusable GROMACS centering groups."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


GROUP_HEADER_PATTERN = re.compile(r"^\s*\[\s*([^\]]+?)\s*\]\s*$")

DEFAULT_CENTER_GROUP = "center"

WORKFLOW_CENTER_SOURCES: dict[str, tuple[str, ...]] = {
    "polymer": ("PHA",),
    "polymer_only": ("PHA",),
    "enzyme": ("Protein",),
    "membrane": ("MEMB", "Protein"),
    "complex": ("Protein", "PHA"),
    "protein_polymer": ("Protein", "PHA"),
}


@dataclass(frozen=True)
class GromacsIndex:
    """Parsed GROMACS index groups, preserving group order."""

    groups: dict[str, tuple[int, ...]]

    @property
    def names(self) -> tuple[str, ...]:
        return tuple(self.groups)

    def has_group(self, name: str) -> bool:
        return _canonical_group_name(name) in {
            _canonical_group_name(group_name) for group_name in self.groups
        }

    def group(self, name: str) -> tuple[int, ...]:
        canonical = _canonical_group_name(name)
        for group_name, atoms in self.groups.items():
            if _canonical_group_name(group_name) == canonical:
                return atoms
        raise KeyError(f"Index group not found: {name}")


@dataclass(frozen=True)
class CenterIndexResult:
    """Result from creating or reusing a dedicated centering index."""

    index_path: Path
    center_group: str
    source_groups: tuple[str, ...]
    created: bool
    reused_existing_center: bool


def _canonical_group_name(name: str) -> str:
    return " ".join(name.strip().lower().split())


def read_index(index_path: str | Path) -> GromacsIndex:
    """Read a GROMACS ``.ndx`` file into named atom groups."""

    path = Path(index_path)
    groups: dict[str, list[int]] = {}
    current_name: str | None = None

    for line_number, line in enumerate(path.read_text().splitlines(), start=1):
        header_match = GROUP_HEADER_PATTERN.match(line)
        if header_match:
            current_name = header_match.group(1).strip()
            if not current_name:
                raise ValueError(f"Empty index group name in {path}:{line_number}")
            groups.setdefault(current_name, [])
            continue

        stripped = line.strip()
        if not stripped:
            continue
        if current_name is None:
            raise ValueError(
                f"Atom numbers appear before any index group in {path}:{line_number}"
            )
        try:
            groups[current_name].extend(int(value) for value in stripped.split())
        except ValueError as exc:
            raise ValueError(
                f"Invalid atom number in index group {current_name!r} "
                f"at {path}:{line_number}"
            ) from exc

    return GromacsIndex({name: tuple(atoms) for name, atoms in groups.items()})


def write_index(index: GromacsIndex, index_path: str | Path) -> Path:
    """Write a GROMACS index file with stable 15-atom line wrapping."""

    path = Path(index_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []

    for group_name, atoms in index.groups.items():
        lines.append(f"[ {group_name} ]")
        atom_text = [str(atom) for atom in atoms]
        for start in range(0, len(atom_text), 15):
            lines.append(" ".join(atom_text[start : start + 15]))
        lines.append("")

    path.write_text("\n".join(lines))
    return path


def resolve_center_source_groups(
    index: GromacsIndex,
    *,
    workflow_type: str = "polymer",
    source_groups: tuple[str, ...] | list[str] | None = None,
) -> tuple[str, ...]:
    """Return source groups for a workflow, filtering to groups present in the index."""

    requested = tuple(source_groups) if source_groups is not None else None
    if requested is None:
        try:
            requested = WORKFLOW_CENTER_SOURCES[workflow_type]
        except KeyError as exc:
            valid = ", ".join(sorted(WORKFLOW_CENTER_SOURCES))
            raise ValueError(
                f"Unknown centering workflow type {workflow_type!r}. "
                f"Known workflow types: {valid}. Pass source_groups for custom systems."
            ) from exc

    present: list[str] = []
    for group_name in requested:
        if index.has_group(group_name):
            present.append(group_name)

    if present:
        return tuple(present)

    missing = ", ".join(requested)
    available = ", ".join(index.names)
    raise ValueError(
        f"Cannot create [ {DEFAULT_CENTER_GROUP} ] group; none of the requested "
        f"source groups exist: {missing}. Available groups: {available}"
    )


def merged_group_atoms(index: GromacsIndex, group_names: tuple[str, ...]) -> tuple[int, ...]:
    """Merge one or more index groups into a sorted unique atom list."""

    atom_numbers: set[int] = set()
    for group_name in group_names:
        atom_numbers.update(index.group(group_name))
    return tuple(sorted(atom_numbers))


def ensure_center_index(
    source_index: str | Path,
    output_index: str | Path | None = None,
    *,
    workflow_type: str = "polymer",
    source_groups: tuple[str, ...] | list[str] | None = None,
    center_group: str = DEFAULT_CENTER_GROUP,
) -> CenterIndexResult:
    """Create or reuse a GROMACS index file containing a dedicated ``center`` group.

    Existing ``[ center ]`` groups are reused. Otherwise the group is generated from
    the workflow source groups, currently ``PHA`` for polymer-only systems.
    """

    source_path = Path(source_index)
    output_path = Path(output_index) if output_index is not None else source_path

    if output_path.exists():
        output = read_index(output_path)
        if output.has_group(center_group):
            return CenterIndexResult(
                index_path=output_path,
                center_group=center_group,
                source_groups=(center_group,),
                created=False,
                reused_existing_center=True,
            )
    else:
        output = read_index(source_path)

    if not output_path.exists() or output_path != source_path:
        index = read_index(source_path)
    else:
        index = output

    if index.has_group(center_group):
        if output_path != source_path:
            write_index(index, output_path)
        return CenterIndexResult(
            index_path=output_path,
            center_group=center_group,
            source_groups=(center_group,),
            created=output_path != source_path,
            reused_existing_center=True,
        )

    resolved_sources = resolve_center_source_groups(
        index,
        workflow_type=workflow_type,
        source_groups=source_groups,
    )
    atoms = merged_group_atoms(index, resolved_sources)
    groups = dict(index.groups)
    groups[center_group] = atoms
    write_index(GromacsIndex(groups), output_path)

    return CenterIndexResult(
        index_path=output_path,
        center_group=center_group,
        source_groups=resolved_sources,
        created=True,
        reused_existing_center=False,
    )

