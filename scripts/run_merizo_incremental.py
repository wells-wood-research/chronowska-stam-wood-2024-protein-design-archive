import json
import os
import subprocess
import argparse
import shutil

BASE = "/home/mchrnwsk/pda"

MERIZO_DB = f"{BASE}/merizo_search/examples/database/cath"
TMP = f"{BASE}/foldseek/tmp"
CATH_URL = "ftp://orengoftp.biochem.ucl.ac.uk/cath/releases/daily-release/newest/cath-b-newest-names.gz"


def load_pdbs(path):
    with open(path) as f:
        data = json.load(f)
    return {entry["pdb"].upper() for entry in data if "pdb" in entry}


def compute_delta(prev_json, next_json):
    prev = load_pdbs(prev_json)
    nxt = load_pdbs(next_json)

    return sorted(nxt - prev)

def run(cmd):
    print(f"[RUN] {cmd}")
    subprocess.run(cmd, shell=True, check=True)


def ensure_cath_db():
    os.makedirs(f"{BASE}/merizo_search/database", exist_ok=True)

    gz = f"{BASE}/merizo_search/database/cath-b-newest-names.gz"
    out = gz.replace(".gz", "")

    if os.path.exists(out):
        print("[INFO] CATH DB exists — skipping download")
        return

    run(f"wget -O {gz} {CATH_URL}")
    run(f"gunzip -f {gz}")


def main(prev_date, next_date):
    ensure_cath_db()

    pdb_glob = f"{BASE}/foldseek/{next_date}/pdb_files"

    log = f"{BASE}/log_merizo_{next_date}.txt"
    out_dir = f"{BASE}/foldseek/{next_date}/cath_results"

    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(TMP, exist_ok=True)
   
    prev_json = f"/home/mchrnwsk/pda/foldseek/{prev_date}/{prev_date}_data_scraped.json"
    next_json = f"/home/mchrnwsk/pda/foldseek/{next_date}/{next_date}_data_scraped.json"
    pdbs = compute_delta(prev_json, next_json)
    pdb_args = " ".join([
        f"{pdb_glob}/{pdb}.pdb" for pdb in pdbs
    ])

    cmd = (
        f"python /home/mchrnwsk/pda/merizo_search/merizo_search/merizo.py easy-search "
        f"{pdb_args} "
        f"{MERIZO_DB} "
        f"{out_dir} "
        f"{TMP} "
        f"--multi_domain_search -k 100 --iterate "
        f"2>&1 | tee {log}"
    )
    
    run(cmd)

    prev_tsv = f"/home/mchrnwsk/pda/foldseek/{prev_date}/cath_results_search.tsv"
    new_tsv = f"/home/mchrnwsk/pda/foldseek/{next_date}/cath_results_search.tsv"

    if os.path.exists(prev_tsv):
        print("[INFO] Merging previous Merizo TSV results...")

        with open(prev_tsv) as f1, open(new_tsv, "a") as f2:
            shutil.copyfileobj(f1, f2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--prev", required=True)
    parser.add_argument("--next", required=True)

    args = parser.parse_args()

    main(args.prev, args.next)