import sys
from types import SimpleNamespace

import pytest

from iphasimulator.conversion_amber_to_gromacs import convert_amber_to_gromacs
from iphasimulator.conversion_amber_to_gromacs import _normalize_structure_charge


def test_convert_amber_to_gromacs_raises_clear_error_without_parmed(
    monkeypatch,
    tmp_path,
):
    monkeypatch.setitem(sys.modules, "parmed", None)

    with pytest.raises(ImportError, match="ParmEd is required"):
        convert_amber_to_gromacs(
            str(tmp_path / "missing.prmtop"),
            str(tmp_path / "missing.inpcrd"),
            str(tmp_path / "gromacs"),
            "P3HB_4",
        )


def test_convert_amber_to_gromacs_writes_top_and_gro_with_parmed(
    monkeypatch,
    tmp_path,
):
    prmtop_path = tmp_path / "P3HB_4.prmtop"
    inpcrd_path = tmp_path / "P3HB_4.inpcrd"
    prmtop_path.write_text("topology")
    inpcrd_path.write_text("coordinates")
    saved_paths = []

    class FakeStructure:
        atoms = [
            SimpleNamespace(charge=-0.500),
            SimpleNamespace(charge=0.499),
        ]

        def save(self, path, overwrite):
            saved_paths.append((path, overwrite))
            with open(path, "w") as handle:
                handle.write(f"saved {path}")

    def fake_load_file(prmtop, inpcrd):
        assert prmtop == str(prmtop_path)
        assert inpcrd == str(inpcrd_path)
        return FakeStructure()

    monkeypatch.setitem(
        sys.modules,
        "parmed",
        SimpleNamespace(load_file=fake_load_file),
    )

    outputs = convert_amber_to_gromacs(
        str(prmtop_path),
        str(inpcrd_path),
        str(tmp_path / "gromacs"),
        "P3HB_4",
    )

    assert outputs.top_path == tmp_path / "gromacs" / "P3HB_4.top"
    assert outputs.gro_path == tmp_path / "gromacs" / "P3HB_4.gro"
    assert outputs.top_path.exists()
    assert outputs.gro_path.exists()
    assert saved_paths == [
        (str(outputs.top_path), True),
        (str(outputs.gro_path), True),
    ]
    assert sum(atom.charge for atom in FakeStructure.atoms) == pytest.approx(0.0)


def test_normalize_structure_charge_distributes_small_rounding_residue():
    structure = SimpleNamespace(
        atoms=[
            SimpleNamespace(charge=-0.500),
            SimpleNamespace(charge=0.493001),
        ]
    )

    normalized_charge = _normalize_structure_charge(structure)

    assert normalized_charge == pytest.approx(0.0, abs=1e-12)
    assert sum(atom.charge for atom in structure.atoms) == pytest.approx(0.0, abs=1e-12)


def test_normalize_structure_charge_rejects_large_correction():
    structure = SimpleNamespace(
        atoms=[
            SimpleNamespace(charge=-0.500),
            SimpleNamespace(charge=0.300),
        ]
    )

    with pytest.raises(ValueError, match="too far from integer charge"):
        _normalize_structure_charge(structure)
