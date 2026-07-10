import pytest

from iphasimulator.naming import (
    canonical_monomer_code,
    monomer_to_polymer_code,
    multi_chain_system_name,
    oligomer_name,
    residue_variant_name,
    residue_variant_names,
    validate_monomer_code,
    validate_oligomer_name,
    validate_pha_name,
    validate_polymer_code,
    validate_system_name,
)


def test_monomer_to_polymer_code_uses_canonical_codes():
    assert monomer_to_polymer_code("3HB") == "P3HB"
    assert monomer_to_polymer_code("3HO") == "P3HO"
    assert monomer_to_polymer_code("3HDD") == "P3HDD"


def test_legacy_monomer_aliases_convert_to_canonical_codes():
    assert canonical_monomer_code("PHB") == "3HB"
    assert canonical_monomer_code("PHO") == "3HO"
    assert canonical_monomer_code("PHDD") == "3HDD"


def test_oligomer_and_multi_chain_system_names():
    assert oligomer_name("3HB", 4) == "P3HB_4"
    assert oligomer_name("PHO", 8) == "P3HO_8"
    assert multi_chain_system_name(25, "3HB", 3) == "25_P3HB_3"
    assert multi_chain_system_name(10, oligomer="P3HO_8") == "10_P3HO_8"


def test_residue_variant_names():
    assert residue_variant_names("3HB") == ("3HB_H", "3HB_M", "3HB_T")
    assert residue_variant_name("3HO", "head") == "3HO_H"
    assert residue_variant_name("3HDD", "M") == "3HDD_M"


@pytest.mark.parametrize(
    ("validator", "value", "expected"),
    [
        (validate_monomer_code, "3HB", "3HB"),
        (validate_polymer_code, "P3HB", "P3HB"),
        (validate_oligomer_name, "P3HB_4", "P3HB_4"),
        (validate_system_name, "25_P3HB_3", "25_P3HB_3"),
        (validate_pha_name, "P3HDD_8", "P3HDD_8"),
    ],
)
def test_validators_return_canonical_names(validator, value, expected):
    assert validator(value) == expected


@pytest.mark.parametrize(
    ("validator", "value"),
    [
        (validate_monomer_code, "PHB"),
        (validate_oligomer_name, "PHB4"),
        (validate_oligomer_name, "P3HB_0"),
        (validate_system_name, "0_P3HB_3"),
    ],
)
def test_validators_reject_noncanonical_or_invalid_names(validator, value):
    with pytest.raises(ValueError):
        validator(value)
