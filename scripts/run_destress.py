import os
import shutil
import pandas as pd
import json
import argparse

BASE = "/home/mchrnwsk/pda-destress-analysis/data"

MASTER_CSV = f"{BASE}/destress_metrics_backup.csv"
PDB_DIR = f"{BASE}/pdb_files"
NEW_PDB_DIR = f"{BASE}/new_update_pdb"

def safe(row, key):
    if row is None:
        return None
    return row[key] if key in row and pd.notna(row[key]) else None

# ---- STEP 1: identify new PDBs ----

def get_existing_codes():
    if not os.path.exists(MASTER_CSV):
        return set()

    df = pd.read_csv(MASTER_CSV)
    return {str(x).lower() for x in df["design_name"]}

def get_all_pdb_files():
    files = []
    for f in os.listdir(PDB_DIR):
        if f.endswith(".pdb"):
            files.append(f)
    return files

def extract_code(filename):
    return filename.split(".")[0].lower()

def copy_new_pdbs():
    os.makedirs(NEW_PDB_DIR, exist_ok=True)

    existing = get_existing_codes()
    pdb_files = get_all_pdb_files()

    new_files = []

    for f in pdb_files:
        code = extract_code(f)

        if code not in existing:
            src = os.path.join(PDB_DIR, f)
            dst = os.path.join(NEW_PDB_DIR, f)
            shutil.copy2(src, dst)
            new_files.append(code)

    print(f"[INFO] {len(new_files)} new PDBs copied to {NEW_PDB_DIR}")
    return new_files

# ---- MAIN ----

def main():
    copy_new_pdbs()

    print("\n[INFO] Run de-stress manually:")
    print(f"cd /home/mchrnwsk/bin/de-stress/ && python run_destress_headless.py --i {NEW_PDB_DIR}\n")


if __name__ == "__main__":
    main()