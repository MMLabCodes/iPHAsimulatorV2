"""Canonical PHA naming helpers."""

from __future__ import annotations

from typing import Literal


ResidueRole = Literal["H", "M", "T", "head", "main", "tail"]

MONOMER_TO_POLYMER: dict[str, str] = {
    "3HB": "P3HB",
    "3HV": "P3HV",
    "3HHx": "P3HHx",
    "3HHep": "P3HHep",
    "3HO": "P3HO",
    "3HN": "P3HN",
    "3HD": "P3HD",
    "3HDD": "P3HDD",
}

POLYMER_TO_MONOMER: dict[str, str] = {
    polymer: monomer for monomer, polymer in MONOMER_TO_POLYMER.items()
}

LEGACY_MONOMER_ALIASES: dict[str, str] = {
    "PHB": "3HB",
    "PHV": "3HV",
    "PHHx": "3HHx",
    "PHHep": "3HHep",
    "PHO": "3HO",
    "PHN": "3HN",
    "PHD": "3HD",
    "PHDD": "3HDD",
}

RESIDUE_ROLE_SUFFIXES: tuple[str, str, str] = ("H", "M", "T")

_MONOMER_LOOKUP = {code.upper(): code for code in MONOMER_TO_POLYMER}
_MONOMER_LOOKUP.update(
    {alias.upper(): canonical for alias, canonical in LEGACY_MONOMER_ALIASES.items()}
)
_POLYMER_LOOKUP = {code.upper(): code for code in POLYMER_TO_MONOMER}
_ROLE_LOOKUP = {
    "H": "H",
    "HEAD": "H",
    "M": "M",
    "MAIN": "M",
    "T": "T",
    "TAIL": "T",
}


def _require_text(value: str, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    return value.strip()


def _require_positive_int(value: int, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"{label} must be an integer")
    if value < 1:
        raise ValueError(f"{label} must be at least 1")
    return value


def canonical_monomer_code(code: str) -> str:
    """Return the canonical monomer/residue code, accepting legacy aliases."""

    text = _require_text(code, "monomer code")
    canonical = _MONOMER_LOOKUP.get(text.upper())
    if canonical is None:
        supported = ", ".join(sorted(MONOMER_TO_POLYMER))
        raise ValueError(f"Unknown monomer code {code!r}. Supported monomers: {supported}")
    return canonical


def validate_monomer_code(code: str) -> str:
    """Validate and return a canonical monomer/residue code such as ``3HB``."""

    text = _require_text(code, "monomer code")
    canonical = MONOMER_TO_POLYMER.get(text)
    if canonical is None:
        supported = ", ".join(sorted(MONOMER_TO_POLYMER))
        raise ValueError(f"Invalid monomer code {code!r}. Expected one of: {supported}")
    return text


def monomer_to_polymer_code(monomer_code: str) -> str:
    """Convert a monomer/residue code such as ``3HB`` to ``P3HB``."""

    return MONOMER_TO_POLYMER[canonical_monomer_code(monomer_code)]


def validate_polymer_code(code: str) -> str:
    """Validate and return a polymer code such as ``P3HB``."""

    text = _require_text(code, "polymer code")
    canonical = _POLYMER_LOOKUP.get(text.upper())
    if canonical is None:
        supported = ", ".join(sorted(POLYMER_TO_MONOMER))
        raise ValueError(f"Invalid polymer code {code!r}. Expected one of: {supported}")
    return canonical


def oligomer_name(monomer_code: str, repeat_units: int) -> str:
    """Return a single-chain oligomer name such as ``P3HB_4``."""

    repeat_units = _require_positive_int(repeat_units, "repeat units")
    return f"{monomer_to_polymer_code(monomer_code)}_{repeat_units}"


def validate_oligomer_name(name: str) -> str:
    """Validate and return a single-chain oligomer name such as ``P3HO_8``."""

    text = _require_text(name, "oligomer name")
    try:
        polymer_code, repeat_text = text.rsplit("_", 1)
    except ValueError as exc:
        raise ValueError(
            f"Invalid oligomer name {name!r}. Expected format P3HB_4"
        ) from exc

    polymer_code = validate_polymer_code(polymer_code)
    try:
        repeat_units = int(repeat_text)
    except ValueError as exc:
        raise ValueError(
            f"Invalid oligomer name {name!r}. Repeat units must be an integer"
        ) from exc
    repeat_units = _require_positive_int(repeat_units, "repeat units")
    return f"{polymer_code}_{repeat_units}"


def multi_chain_system_name(
    chain_count: int,
    monomer_code: str | None = None,
    repeat_units: int | None = None,
    *,
    oligomer: str | None = None,
) -> str:
    """Return a multi-chain system name such as ``25_P3HB_3``."""

    chain_count = _require_positive_int(chain_count, "chain count")
    if oligomer is None:
        if monomer_code is None or repeat_units is None:
            raise ValueError(
                "monomer_code and repeat_units are required when oligomer is not set"
            )
        oligomer = oligomer_name(monomer_code, repeat_units)
    else:
        oligomer = validate_oligomer_name(oligomer)
    return f"{chain_count}_{oligomer}"


def validate_system_name(name: str) -> str:
    """Validate and return a multi-chain system name such as ``25_P3HB_3``."""

    text = _require_text(name, "system name")
    try:
        chain_text, oligomer = text.split("_", 1)
    except ValueError as exc:
        raise ValueError(
            f"Invalid system name {name!r}. Expected format 25_P3HB_3"
        ) from exc

    try:
        chain_count = int(chain_text)
    except ValueError as exc:
        raise ValueError(
            f"Invalid system name {name!r}. Chain count must be an integer"
        ) from exc
    chain_count = _require_positive_int(chain_count, "chain count")
    return f"{chain_count}_{validate_oligomer_name(oligomer)}"


def residue_variant_name(monomer_code: str, role: ResidueRole) -> str:
    """Return a head/main/tail residue name such as ``3HB_H``."""

    monomer_code = canonical_monomer_code(monomer_code)
    role_text = _require_text(role, "residue role")
    suffix = _ROLE_LOOKUP.get(role_text.upper())
    if suffix is None:
        raise ValueError("residue role must be H, M, T, head, main, or tail")
    return f"{monomer_code}_{suffix}"


def residue_variant_names(monomer_code: str) -> tuple[str, str, str]:
    """Return head, main, and tail residue names for one monomer code."""

    monomer_code = canonical_monomer_code(monomer_code)
    return tuple(f"{monomer_code}_{suffix}" for suffix in RESIDUE_ROLE_SUFFIXES)


def validate_pha_name(name: str) -> str:
    """Validate any canonical PHA monomer, polymer, oligomer, or system name."""

    validators = (
        validate_system_name,
        validate_oligomer_name,
        validate_polymer_code,
        validate_monomer_code,
    )
    for validator in validators:
        try:
            return validator(name)
        except ValueError:
            continue
    raise ValueError(
        f"Invalid PHA name {name!r}. Expected 3HB, P3HB, P3HB_4, or 25_P3HB_3"
    )
