import os
import shutil
import pandas as pd
import json
import argparse

BASE = "/home/mchrnwsk/pda-destress-analysis/data"

MASTER_CSV = f"{BASE}/destress_metrics.csv"
PDB_DIR = f"{BASE}/pdb_files"
NEW_PDB_DIR = f"{BASE}/new_update_pdb"

def safe(row, key):
    if row is None:
        return None
    return row[key] if key in row and pd.notna(row[key]) else None

# ---- merge new destress output ----

DESTRESS_COLUMNS = [
    "design_name","file_name","full_sequence","dssp_assignment",
    "composition_ALA","composition_CYS","composition_ASP","composition_GLU",
    "composition_PHE","composition_GLY","composition_HIS","composition_ILE",
    "composition_LYS","composition_LEU","composition_MET","composition_ASN",
    "composition_PRO","composition_GLN","composition_ARG","composition_SER",
    "composition_THR","composition_VAL","composition_TRP","composition_UNK",
    "composition_TYR",
    "ss_prop_alpha_helix","ss_prop_beta_bridge","ss_prop_beta_strand",
    "ss_prop_3_10_helix","ss_prop_pi_helix","ss_prop_hbonded_turn",
    "ss_prop_bend","ss_prop_loop",
    "hydrophobic_fitness","isoelectric_point","charge","mass","num_residues",
    "packing_density",
    "budeff_total","budeff_steric","budeff_desolvation","budeff_charge",
    "evoef2_total","evoef2_ref_total","evoef2_intraR_total","evoef2_interS_total","evoef2_interD_total",
    "evoef2_reference_ALA","evoef2_reference_CYS","evoef2_reference_ASP","evoef2_reference_GLU",
    "evoef2_reference_PHE","evoef2_reference_GLY","evoef2_reference_HIS","evoef2_reference_ILE",
    "evoef2_reference_LYS","evoef2_reference_LEU","evoef2_reference_MET","evoef2_reference_ASN",
    "evoef2_reference_PRO","evoef2_reference_GLN","evoef2_reference_ARG","evoef2_reference_SER",
    "evoef2_reference_THR","evoef2_reference_VAL","evoef2_reference_TRP","evoef2_reference_TYR",
    "evoef2_intraR_vdwatt","evoef2_intraR_vdwrep","evoef2_intraR_electr","evoef2_intraR_deslvP",
    "evoef2_intraR_deslvH","evoef2_intraR_hbscbb_dis","evoef2_intraR_hbscbb_the",
    "evoef2_intraR_hbscbb_phi","evoef2_aapropensity","evoef2_ramachandran","evoef2_dunbrack",
    "evoef2_interS_vdwatt","evoef2_interS_vdwrep","evoef2_interS_electr","evoef2_interS_deslvP",
    "evoef2_interS_deslvH","evoef2_interS_ssbond","evoef2_interS_hbbbbb_dis",
    "evoef2_interS_hbbbbb_the","evoef2_interS_hbbbbb_phi","evoef2_interS_hbscbb_dis",
    "evoef2_interS_hbscbb_the","evoef2_interS_hbscbb_phi","evoef2_interS_hbscsc_dis",
    "evoef2_interS_hbscsc_the","evoef2_interS_hbscsc_phi",
    "evoef2_interD_vdwatt","evoef2_interD_vdwrep","evoef2_interD_electr","evoef2_interD_deslvP",
    "evoef2_interD_deslvH","evoef2_interD_ssbond","evoef2_interD_hbbbbb_dis",
    "evoef2_interD_hbbbbb_the","evoef2_interD_hbbbbb_phi","evoef2_interD_hbscbb_dis",
    "evoef2_interD_hbscbb_the","evoef2_interD_hbscbb_phi","evoef2_interD_hbscsc_dis",
    "evoef2_interD_hbscsc_the","evoef2_interD_hbscsc_phi",
    "dfire2_total",
    "rosetta_total","rosetta_fa_atr","rosetta_fa_rep","rosetta_fa_intra_rep",
    "rosetta_fa_elec","rosetta_fa_sol","rosetta_lk_ball_wtd","rosetta_fa_intra_sol_xover4",
    "rosetta_hbond_lr_bb","rosetta_hbond_sr_bb","rosetta_hbond_bb_sc","rosetta_hbond_sc",
    "rosetta_dslf_fa13","rosetta_rama_prepro","rosetta_p_aa_pp","rosetta_fa_dun",
    "rosetta_omega","rosetta_pro_close","rosetta_yhh_planarity",
    "aggrescan3d_total_value","aggrescan3d_avg_value",
    "aggrescan3d_min_value","aggrescan3d_max_value"
]

def merge_new_results():
    new_csv = f"{NEW_PDB_DIR}/design_data.csv"

    if not os.path.exists(new_csv):
        print("[WARN] No new design_data.csv found — skipping merge")
        return

    # Build expected header string
    header_line = ",".join(DESTRESS_COLUMNS)

    # Ensure master exists and has header
    if not os.path.exists(MASTER_CSV):
        print("[INFO] Master CSV does not exist — creating new one")
        with open(MASTER_CSV, "w") as f:
            f.write(header_line + "\n")

    # Optional: load existing design_names to avoid duplicates
    existing_codes = set()
    with open(MASTER_CSV) as f:
        for line in f:
            if line.startswith("design_name"):
                continue
            code = line.split(",")[0].strip().lower()
            existing_codes.add(code)

    appended = 0

    with open(new_csv) as f_in, open(MASTER_CSV, "a") as f_out:
        lines = f_in.readlines()

        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue

            # Skip header if present
            if i == 0 and line.replace('"', '') == header_line:
                print("[INFO] Skipping header in new CSV")
                continue

            code = line.split(",")[0].strip().lower()

            # Optional deduplication
            if code in existing_codes:
                continue

            f_out.write(line + "\n")
            appended += 1

    print(f"[INFO] Appended {appended} new rows to {MASTER_CSV}")

# ---- inject into JSON ----

def build_properties(row):
    return {
        "num_residues": safe(row, "num_residues"),
        "charge": safe(row, "charge"),
        "mass": safe(row, "mass"),
        "packing_density": safe(row, "packing_density"),
        "isoelectric_point": safe(row, "isoelectric_point"),
        "hydrophobic_fitness": safe(row, "hydrophobic_fitness"),

        "solubility": {
            "total_value": safe(row, "aggrescan3d_total_value"),
            "avg_value": safe(row, "aggrescan3d_avg_value"),
            "min_value": safe(row, "aggrescan3d_min_value"),
            "max_value": safe(row, "aggrescan3d_max_value")
        },

        "aa_composition": {
            k: safe(row, k) for k in [
                "composition_ALA","composition_CYS","composition_ASP","composition_GLU",
                "composition_PHE","composition_GLY","composition_HIS","composition_ILE",
                "composition_LYS","composition_LEU","composition_MET","composition_ASN",
                "composition_PRO","composition_GLN","composition_ARG","composition_SER",
                "composition_THR","composition_VAL","composition_TRP","composition_UNK",
                "composition_TYR"
            ]
        },

        "ss_composition": {
            k: safe(row, k) for k in [
                "ss_prop_alpha_helix","ss_prop_beta_bridge","ss_prop_beta_strand",
                "ss_prop_3_10_helix","ss_prop_pi_helix","ss_prop_hbonded_turn",
                "ss_prop_bend","ss_prop_loop"
            ]
        },

        "dssp": {
            "full_sequence": safe(row, "full_sequence"),
            "dssp_assignment": safe(row, "dssp_assignment")
        },

        "energy": {
            "budeff": {
                k: safe(row, k) for k in [
                    "budeff_total","budeff_steric","budeff_desolvation","budeff_charge"
                ]
            },
            "evoef2": {
                k: safe(row, k) for k in [
                    "evoef2_total","evoef2_ref_total","evoef2_intraR_total",
                    "evoef2_interS_total","evoef2_interD_total"
                ]
            },
            "dfire2": {
                "dfire2_total": safe(row, "dfire2_total")
            },
            "rosetta": {
                "rosetta_total": safe(row, "rosetta_total"),
                "rosetta_vdw_atr": safe(row, "rosetta_fa_atr"),
                "rosetta_vdw_rep": safe(row, "rosetta_fa_rep"),
                "rosetta_vdw_intra_rep": safe(row, "rosetta_fa_intra_rep"),
                "rosetta_electrostatics": safe(row, "rosetta_fa_elec"),
                "rosetta_solvation_isotropic": safe(row, "rosetta_fa_sol"),
                "rosetta_solvation_anisotropic_polar_atoms": safe(row, "rosetta_lk_ball_wtd"),
                "rosetta_solvation_isotropic_iR": safe(row, "rosetta_fa_intra_sol_xover4"),
                "rosetta_hbond_lr_bb": safe(row, "rosetta_hbond_lr_bb"),
                "rosetta_hbond_sr_bb": safe(row, "rosetta_hbond_sr_bb"),
                "rosetta_hbond_bb_sc": safe(row, "rosetta_hbond_bb_sc"),
                "rosetta_hbond_sc": safe(row, "rosetta_hbond_sc"),
                "rosetta_disulfides": safe(row, "rosetta_dslf_fa13"),
                "rosetta_backbone_torsion_preference": safe(row, "rosetta_rama_prepro"),
                "rosetta_aa_propensity": safe(row, "rosetta_p_aa_pp"),
                "rosetta_dunbrack_rotamer": safe(row, "rosetta_fa_dun"),
                "rosetta_omega": safe(row, "rosetta_omega"),
                "rosetta_pro_close": safe(row, "rosetta_pro_close"),
                "rosetta_yhh_planarity": safe(row, "rosetta_yhh_planarity")
            }
        }
    }

def update_json(next_date):
    json_path = f"{BASE}/{next_date}_data_similarity.json"

    with open(json_path) as f:
        data = json.load(f)

    df = pd.read_csv(MASTER_CSV)
    lookup = {str(row["design_name"]).lower(): row for _, row in df.iterrows()}

    updated = 0
    missing = 0

    for entry in data:
        pdb = entry.get("pdb", "").lower()

        row = lookup.get(pdb, None)

        if row is None:
            missing += 1
        else:
            updated += 1

        # 🔥 ALWAYS populate (even if row is None)
        entry["physicochemical_properties"] = build_properties(row)

    new_json_path = json_path.replace("_similarity", "_destress")

    with open(new_json_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"[INFO] Updated: {updated}")
    print(f"[INFO] Missing (filled with nulls): {missing}")


# ---- MAIN ----

def main(next_date):
    merge_new_results()
    update_json(next_date)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--next", required=True)

    args = parser.parse_args()
    main(args.next)