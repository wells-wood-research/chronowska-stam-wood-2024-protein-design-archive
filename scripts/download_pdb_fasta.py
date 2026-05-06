#!/usr/bin/env python3

import requests
import gzip
import shutil
import os

URL = "https://files.wwpdb.org/pub/pdb/derived_data/pdb_seqres.txt.gz"
OUTPUT_PATH = "/home/mchrnwsk/pda-destress-analysis/data/pdb_seqres.txt"


def download_file(url, dest):
    print(f"[INFO] Downloading {url} ...")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"[INFO] Download complete: {dest}")


def decompress_gzip(gz_path, out_path):
    print(f"[INFO] Decompressing {gz_path} ...")
    with gzip.open(gz_path, "rb") as f_in:
        with open(out_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    print(f"[INFO] Decompressed to: {out_path}")


def main():
    gz_path = OUTPUT_PATH + ".gz"

    download_file(URL, gz_path)
    decompress_gzip(gz_path, OUTPUT_PATH)

    os.remove(gz_path)
    print("[INFO] Cleanup complete")


if __name__ == "__main__":
    main()