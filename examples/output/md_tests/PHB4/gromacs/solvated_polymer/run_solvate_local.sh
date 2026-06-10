#!/usr/bin/env bash
set -euo pipefail
export GMX_MAXBACKUP=-1

fail_with_log() {
    local command_name="$1"
    local log_path="$2"
    echo "ERROR: ${command_name} failed. See ${log_path}." >&2
    if [[ -f "${log_path}" ]]; then
        echo "--- Last 50 lines of ${log_path} ---" >&2
        tail -n 50 "${log_path}" >&2 || true
        echo "--- End ${log_path} ---" >&2
    fi
    exit 1
}

run_logged() {
    local command_name="$1"
    local log_path="$2"
    shift 2
    printf '+ %q' "$@" > "${log_path}"
    printf '\n' >> "${log_path}"
    if "$@" >> "${log_path}" 2>&1; then
        echo "${command_name} completed; log: ${log_path}"
    else
        fail_with_log "${command_name}" "${log_path}"
    fi
}

run_genion_logged() {
    local log_path="genion.log"
    local genion_args=(-s ions.tpr -o system_neutralized.gro -p topol.top -neutral -pname SOD -nname CLA)
    if awk -v concentration="${ION_CONCENTRATION_MOLAR}" 'BEGIN { exit !(concentration > 0) }'; then
        genion_args+=(-conc "${ION_CONCENTRATION_MOLAR}")
    fi
    printf '+ printf %q | gmx genion' "${SOLVENT_GROUP}" > "${log_path}"
    printf ' %q' "${genion_args[@]}" >> "${log_path}"
    printf '\n' >> "${log_path}"
    if printf "%s\n" "${SOLVENT_GROUP}" | gmx genion "${genion_args[@]}" >> "${log_path}" 2>&1; then
        echo "genion completed; log: ${log_path}"
    else
        echo "ERROR: genion failed while selecting solvent group '${SOLVENT_GROUP}'." >&2
        echo "If your solvent group is not SOL, rerun this script with --solvent-group <name>." >&2
        fail_with_log "genion" "${log_path}"
    fi
}

run_stdin_logged() {
    local command_name="$1"
    local log_path="$2"
    local stdin_text="$3"
    shift 3
    printf '+ printf %q |' "${stdin_text}" > "${log_path}"
    printf ' %q' "$@" >> "${log_path}"
    printf '\n' >> "${log_path}"
    if printf "%b" "${stdin_text}" | "$@" >> "${log_path}" 2>&1; then
        echo "${command_name} completed; log: ${log_path}"
    else
        fail_with_log "${command_name}" "${log_path}"
    fi
}

clean_generated_files() {
    rm -f         step5_input_box.gro         step5_solvated.gro         step5_ions.gro         genion.tpr         mdout.mdp         editconf.log         minim_grompp_check.log         editconf_box.log         make_ndx_box.log         solvate.log         ions_grompp.log         genion.log         editconf_final.log         make_ndx_final.log         minim_grompp.log         \#*\#         \#*.\#
    for generated_path in step6.0_minimization.*; do
        [[ "${generated_path}" == "step6.0_minimization.mdp" ]] && continue
        rm -f "${generated_path}"
    done
}

reset_from_dry_polymer() {
    local dry_dir="../dry_polymer"
    if [[ -f "${dry_dir}/topol.top" && -f "${dry_dir}/step5_input.gro" ]]; then
        cp "${dry_dir}/topol.top" topol.top
        cp "${dry_dir}/step5_input.gro" step5_input.gro
        if [[ -f "${dry_dir}/index.ndx" ]]; then
            cp "${dry_dir}/index.ndx" index.ndx
        fi
        echo "Reset topol.top and step5_input.gro from ${dry_dir}."
    else
        echo "Using existing topol.top and step5_input.gro; ../dry_polymer was not found."
    fi
}

ensure_include() {
    local include_file="$1"
    if grep -Eq "^[[:space:]]*#include[[:space:]]+\"${include_file}\"" topol.top; then
        return
    fi
    if [[ ! -f "${include_file}" ]]; then
        echo "ERROR: topol.top does not include ${include_file}, and ${include_file} is missing." >&2
        exit 1
    fi

    local tmp_path="topol.top.tmp.$$"
    if awk -v include="#include \"${include_file}\"" '
        BEGIN { inserted = 0 }
        !inserted && tolower($0) ~ /^[[:space:]]*\[ moleculetype \]/ {
            print ""
            print include
            print ""
            inserted = 1
        }
        { print }
        END { if (!inserted) exit 42 }
    ' topol.top > "${tmp_path}"; then
        mv "${tmp_path}" topol.top
        echo "Added ${include_file} include to topol.top"
    else
        rm -f "${tmp_path}"
        echo "ERROR: Could not insert ${include_file}; no [ moleculetype ] section found in topol.top." >&2
        exit 1
    fi
}

topology_source_files() {
    printf '%s\n' topol.top
    sed -n 's/^[[:space:]]*#include[[:space:]]*"\([^"]*\)".*/\1/p' topol.top | while IFS= read -r include_path; do
        if [[ -f "${include_path}" ]]; then
            printf '%s\n' "${include_path}"
        fi
    done
}

has_moleculetype() {
    local molecule_name="$1"
    awk -v target="${molecule_name}" '
        BEGIN { found = 0; in_moleculetype = 0 }
        tolower($0) ~ /^[[:space:]]*\[ moleculetype \]/ { in_moleculetype = 1; next }
        /^[[:space:]]*\[/ { in_moleculetype = 0 }
        in_moleculetype {
            line = $0
            sub(/;.*/, "", line)
            gsub(/^[ \t]+|[ \t]+$/, "", line)
            split(line, fields, /[ \t]+/)
            if (toupper(fields[1]) == target) found = 1
        }
        END { exit found ? 0 : 1 }
    ' $(topology_source_files)
}

has_atomtype() {
    local atom_type="$1"
    awk -v target="${atom_type}" '
        BEGIN { found = 0; in_atomtypes = 0 }
        tolower($0) ~ /^[[:space:]]*\[ atomtypes \]/ { in_atomtypes = 1; next }
        /^[[:space:]]*\[/ { in_atomtypes = 0 }
        in_atomtypes {
            line = $0
            sub(/;.*/, "", line)
            gsub(/^[ \t]+|[ \t]+$/, "", line)
            split(line, fields, /[ \t]+/)
            if (toupper(fields[1]) == target) found = 1
        }
        END { exit found ? 0 : 1 }
    ' $(topology_source_files)
}

validate_solvation_topology() {
    echo "Inspecting topol.top after gmx solvate for water and ion topology definitions."
    ensure_include "tip3_ions_atomtypes.itp"
    ensure_include "TIP3_SOL.itp"
    ensure_include "SOD.itp"
    ensure_include "CLA.itp"

    local missing=()
    for molecule_name in SOL SOD CLA; do
        if ! has_moleculetype "${molecule_name}"; then
            missing+=("[ moleculetype ] ${molecule_name}")
        fi
    done
    for atom_type in OT HT SOD CLA; do
        if ! has_atomtype "${atom_type}"; then
            missing+=("[ atomtypes ] ${atom_type}")
        fi
    done

    if (( ${#missing[@]} > 0 )); then
        echo "ERROR: topol.top is missing water/ion topology parameters required before ions.grompp:" >&2
        printf '  - %s\n' "${missing[@]}" >&2
        echo "Expected the spc216.gro solvent route to use local includes: tip3_ions_atomtypes.itp, TIP3_SOL.itp, SOD.itp, CLA.itp." >&2
        exit 1
    fi
    echo "topol.top contains required SOL/SOD/CLA molecule definitions and OT/HT/SOD/CLA atom types."
}

validate_coordinate_topology_counts() {
    local coordinate_count
    coordinate_count="$(sed -n '2p' step5_input.gro | tr -d '[:space:]')"
    echo "Final step5_input.gro atom count: ${coordinate_count}"
    echo "Final topol.top [ molecules ] section:"
    awk '
        BEGIN { in_molecules = 0 }
        /^[[:space:]]*;/ { next }
        /^[[:space:]]*\[/ {
            in_molecules = (tolower($0) ~ /^[[:space:]]*\[ molecules \]/)
            next
        }
        in_molecules && NF >= 2 { print "  " $1, $2 }
    ' topol.top
}

SOLVENT_GROUP="SOL"
ION_CONCENTRATION_MOLAR="0.15"
while (( $# > 0 )); do
    case "$1" in
        --solvent-group)
            shift
            if (( $# == 0 )); then
                echo "ERROR: --solvent-group requires a group name." >&2
                exit 2
            fi
            SOLVENT_GROUP="$1"
            ;;
        --solvent-group=*)
            SOLVENT_GROUP="${1#*=}"
            ;;
        --overwrite|--clean)
            ;;
        *)
            echo "ERROR: Unknown argument: $1" >&2
            echo "Usage: bash run_solvate_local.sh [--solvent-group SOL|--solvent-group=SOL] [--clean|--overwrite]" >&2
            exit 2
            ;;
    esac
    shift
done

# Build the real solvated GROMACS system.
# Polymer parameters are reset from dry_polymer before GROMACS solvate/genion can update local counts.
reset_from_dry_polymer
clean_generated_files
run_logged "editconf_box" "editconf_box.log" gmx editconf -f step5_input.gro -o step5_input_box.gro -c -d 1.2 -bt cubic
run_stdin_logged "make_ndx_box" "make_ndx_box.log" "q\n" gmx make_ndx -f step5_input_box.gro -o index.ndx
run_logged "solvate" "solvate.log" gmx solvate -cp step5_input_box.gro -cs spc216.gro -p topol.top -o system_solvated.gro
validate_solvation_topology
run_logged "ions_grompp" "ions_grompp.log" gmx grompp -f ions.mdp -c system_solvated.gro -p topol.top -n index.ndx -o ions.tpr -maxwarn 1
run_genion_logged
run_logged "editconf_final" "editconf_final.log" gmx editconf -f system_neutralized.gro -o step5_input.gro
run_stdin_logged "make_ndx_final" "make_ndx_final.log" "q\n" gmx make_ndx -f step5_input.gro -o index.ndx

# Validate that the solvated/ionised coordinates can enter minimisation.
validate_coordinate_topology_counts
run_logged "minim_grompp" "minim_grompp.log" gmx grompp -f step6.0_minimization.mdp -c step5_input.gro -r step5_input.gro -p topol.top -n index.ndx -o step6.0_minimization.tpr -maxwarn 1
rm -f \#*\# \#*.\#
