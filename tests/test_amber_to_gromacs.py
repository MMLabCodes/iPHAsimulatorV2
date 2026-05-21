import sys
from types import SimpleNamespace

import pytest

from iphasimulator.conversion import convert_amber_to_gromacs


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
            "PHB4",
        )


def test_convert_amber_to_gromacs_writes_top_and_gro_with_parmed(
    monkeypatch,
    tmp_path,
):
    prmtop_path = tmp_path / "PHB4.prmtop"
    inpcrd_path = tmp_path / "PHB4.inpcrd"
    prmtop_path.write_text("topology")
    inpcrd_path.write_text("coordinates")
    saved_paths = []

    class FakeStructure:
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
        "PHB4",
    )

    assert outputs.top_path == tmp_path / "gromacs" / "PHB4.top"
    assert outputs.gro_path == tmp_path / "gromacs" / "PHB4.gro"
    assert outputs.top_path.exists()
    assert outputs.gro_path.exists()
    assert saved_paths == [
        (str(outputs.top_path), True),
        (str(outputs.gro_path), True),
    ]
