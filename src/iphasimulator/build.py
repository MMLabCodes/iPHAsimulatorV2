"""RDKit-based PHA chain builder."""

"""
Dan's comments:
    
I don't think we require any of these functions to build the polymers at the current point in time.

I like the idea of validating the sterochemistry and counting specifc carbons/functionalities/etc..
"""



from __future__ import annotations

from rdkit import Chem

from iphasimulator.monomers import Monomer, get_monomer
from iphasimulator.stereochemistry import validate_stereochemistry_option

ESTER_BOND = Chem.MolFromSmarts("[CX3](=O)[OX2][#6]")


def _validate_repeat_units(n: int) -> None:
    if not isinstance(n, int) or isinstance(n, bool):
        raise ValueError("Number of repeat units must be an integer")
    if n < 1:
        raise ValueError("Number of repeat units must be at least 1")


def _validate_side_chain_carbons(side_chain_carbons: int) -> None:
    if not isinstance(side_chain_carbons, int) or isinstance(side_chain_carbons, bool):
        raise ValueError("Side-chain carbons must be an integer")
    if side_chain_carbons < 1:
        raise ValueError("Side-chain carbons must be at least 1")


def _build_oligomer_smiles(side_chain: str, n: int, chiral_tag: str) -> str:
    """Build HO-terminated/carboxy-terminated PHA oligomer SMILES."""

    repeat = f"O[C{chiral_tag}H]({side_chain})CC(=O)"
    return (repeat * n) + "O"


def _sanitize_molecule(mol: Chem.Mol | None, name: str, n: int) -> Chem.Mol:
    if mol is None:
        raise ValueError(f"Failed to build RDKit molecule for {name} n={n}")

    try:
        Chem.SanitizeMol(mol)
    except Chem.AtomValenceException as exc:
        raise ValueError(f"RDKit sanitisation failed for {name} n={n}: {exc}") from exc
    except Chem.KekulizeException as exc:
        raise ValueError(f"RDKit sanitisation failed for {name} n={n}: {exc}") from exc

    return mol


def _count_carbons(mol: Chem.Mol) -> int:
    return sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == 6)


def _validate_ester_bond_count(mol: Chem.Mol, n: int) -> None:
    ester_count = len(mol.GetSubstructMatches(ESTER_BOND))
    expected_count = n - 1
    if ester_count != expected_count:
        raise ValueError(
            f"Expected {expected_count} ester bonds, found {ester_count}"
        )


def _has_hydroxy_neighbor(atom: Chem.Atom) -> bool:
    for neighbor in atom.GetNeighbors():
        bond = atom.GetOwningMol().GetBondBetweenAtoms(atom.GetIdx(), neighbor.GetIdx())
        if neighbor.GetAtomicNum() == 8 and bond.GetBondType() == Chem.BondType.SINGLE:
            return True
    return False


def _is_carboxyl_carbon(atom: Chem.Atom) -> bool:
    if atom.GetAtomicNum() != 6:
        return False

    has_double_o = False
    has_single_o = False
    for neighbor in atom.GetNeighbors():
        bond = atom.GetOwningMol().GetBondBetweenAtoms(atom.GetIdx(), neighbor.GetIdx())
        if neighbor.GetAtomicNum() != 8:
            continue
        if bond.GetBondType() == Chem.BondType.DOUBLE:
            has_double_o = True
        elif bond.GetBondType() == Chem.BondType.SINGLE:
            has_single_o = True
    return has_double_o and has_single_o


def _is_backbone_methylene(atom: Chem.Atom, chiral_idx: int) -> bool:
    if atom.GetAtomicNum() != 6:
        return False

    for neighbor in atom.GetNeighbors():
        if neighbor.GetIdx() != chiral_idx and _is_carboxyl_carbon(neighbor):
            return True
    return False


def _pha_chiral_atom_indices(mol: Chem.Mol) -> list[int]:
    indices: list[int] = []
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() != 6 or not _has_hydroxy_neighbor(atom):
            continue

        backbone_neighbors = [
            neighbor
            for neighbor in atom.GetNeighbors()
            if _is_backbone_methylene(neighbor, atom.GetIdx())
        ]
        if len(backbone_neighbors) == 1:
            indices.append(atom.GetIdx())
    return indices


def _validate_pha_stereochemistry(
    mol: Chem.Mol, expected_count: int, stereochemistry: str
) -> None:
    expected_label = validate_stereochemistry_option(stereochemistry)

    Chem.AssignStereochemistry(mol, cleanIt=True, force=True)
    centres = dict(Chem.FindMolChiralCenters(mol, includeUnassigned=True))
    pha_centres = _pha_chiral_atom_indices(mol)

    if len(pha_centres) != expected_count:
        raise ValueError(
            f"Expected {expected_count} PHA chiral centres, found {len(pha_centres)}"
        )

    mismatched = [
        (atom_idx, centres.get(atom_idx, "unassigned"))
        for atom_idx in pha_centres
        if centres.get(atom_idx) != expected_label
    ]
    if mismatched:
        details = ", ".join(f"atom {atom_idx}: {label}" for atom_idx, label in mismatched)
        raise ValueError(
            f"Expected all PHA chiral centres to be {expected_label}; found {details}"
        )


def _validate_side_chain_carbon_count(
    mol: Chem.Mol, side_chain_length: int, n: int
) -> None:
    expected_side_chain_carbons = side_chain_length * n
    observed_side_chain_carbons = _count_carbons(mol) - (3 * n)

    if observed_side_chain_carbons != expected_side_chain_carbons:
        raise ValueError(
            "Expected "
            f"{expected_side_chain_carbons} side-chain carbons, "
            f"found {observed_side_chain_carbons}"
        )


def validate_pha_chain(
    mol: Chem.Mol | None, monomer: Monomer, n: int, stereochemistry: str
) -> Chem.Mol:
    """Validate core chemistry invariants for a generated PHA oligomer."""

    mol = _sanitize_molecule(mol, monomer.code, n)
    _validate_pha_stereochemistry(mol, expected_count=n, stereochemistry=stereochemistry)
    _validate_ester_bond_count(mol, n)
    _validate_side_chain_carbon_count(mol, monomer.side_chain_length, n)
    return mol


def _build_validated_pha_from_side_chain(
    side_chain: str,
    degree: int,
    stereochemistry: str,
    name: str,
    side_chain_length: int | None = None,
    validate_ester_count: bool = False,
) -> Chem.Mol:
    errors: list[str] = []
    for chiral_tag in ("@", "@@"):
        smiles = _build_oligomer_smiles(side_chain, degree, chiral_tag)
        try:
            mol = _sanitize_molecule(Chem.MolFromSmiles(smiles), name, degree)
            _validate_pha_stereochemistry(
                mol, expected_count=degree, stereochemistry=stereochemistry
            )
            if validate_ester_count:
                _validate_ester_bond_count(mol, degree)
            if side_chain_length is not None:
                _validate_side_chain_carbon_count(mol, side_chain_length, degree)
            return mol
        except ValueError as exc:
            errors.append(str(exc))

    details = "; ".join(errors)
    raise ValueError(f"Failed to build {stereochemistry} PHA for {name}: {details}")


def _validate_custom_name(name: str) -> str:
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Custom PHA name must be a non-empty string")
    return name.strip()


def _side_chain_from_monomer_smiles(monomer_smiles: str, name: str) -> str:
    if not isinstance(monomer_smiles, str) or not monomer_smiles.strip():
        raise ValueError("Custom monomer SMILES must be a non-empty string")

    mol = Chem.MolFromSmiles(monomer_smiles)
    mol = _sanitize_molecule(mol, name, 1)
    Chem.AssignStereochemistry(mol, cleanIt=True, force=True)

    pha_centres = _pha_chiral_atom_indices(mol)
    if len(pha_centres) != 1:
        raise ValueError(
            "Custom monomer must be a chiral 3-hydroxyalkanoic acid with one "
            "PHA backbone stereocentre"
        )

    chiral_atom = mol.GetAtomWithIdx(pha_centres[0])
    if not chiral_atom.HasProp("_CIPCode") or chiral_atom.GetProp("_CIPCode") != "R":
        raise ValueError("Custom monomer PHA stereocentre must be R")

    excluded = {chiral_atom.GetIdx()}
    side_neighbors = [
        neighbor
        for neighbor in chiral_atom.GetNeighbors()
        if neighbor.GetAtomicNum() != 8
        and not _is_backbone_methylene(neighbor, chiral_atom.GetIdx())
    ]
    if len(side_neighbors) != 1:
        raise ValueError("Custom monomer must have exactly one side chain")

    side_root = side_neighbors[0].GetIdx()
    stack = [side_root]
    side_atoms: set[int] = set()
    while stack:
        atom_idx = stack.pop()
        if atom_idx in side_atoms or atom_idx in excluded:
            continue
        side_atoms.add(atom_idx)
        atom = mol.GetAtomWithIdx(atom_idx)
        stack.extend(neighbor.GetIdx() for neighbor in atom.GetNeighbors())

    return Chem.MolFragmentToSmiles(
        mol,
        atomsToUse=sorted(side_atoms),
        rootedAtAtom=side_root,
        isomericSmiles=True,
        canonical=False,
    )


def build_pha_chain(monomer: str, n: int, stereochemistry: str = "R") -> Chem.Mol:
    """Build a minimal RDKit molecule for a homopolymeric PHA oligomer.

    The returned molecule is capped as the linear hydroxy acid oligomer:
    HO-[CH(R)-CH2-C(=O)-O]n-H, represented with implicit hydrogens.
    """

    _validate_repeat_units(n)
    stereochemistry = validate_stereochemistry_option(stereochemistry)

    monomer_entry = get_monomer(monomer)
    return _build_validated_pha_from_side_chain(
        side_chain=monomer_entry.side_chain,
        degree=n,
        stereochemistry=stereochemistry,
        name=monomer_entry.code,
        side_chain_length=monomer_entry.side_chain_length,
        validate_ester_count=True,
    )


def build_pha_by_sidechain(side_chain_carbons: int, degree: int) -> Chem.Mol:
    """Build a linear R-PHA oligomer from an alkyl side-chain length."""

    _validate_side_chain_carbons(side_chain_carbons)
    _validate_repeat_units(degree)

    side_chain = "C" * side_chain_carbons
    name = f"PHA-C{side_chain_carbons}"
    return _build_validated_pha_from_side_chain(
        side_chain=side_chain,
        degree=degree,
        stereochemistry="R",
        name=name,
        side_chain_length=side_chain_carbons,
        validate_ester_count=True,
    )


def build_custom_pha(monomer_smiles: str, degree: int, name: str) -> Chem.Mol:
    """Build an R-PHA oligomer from a user-defined 3-hydroxy acid monomer."""

    name = _validate_custom_name(name)
    _validate_repeat_units(degree)

    side_chain = _side_chain_from_monomer_smiles(monomer_smiles, name)
    return _build_validated_pha_from_side_chain(
        side_chain=side_chain,
        degree=degree,
        stereochemistry="R",
        name=name,
    )
