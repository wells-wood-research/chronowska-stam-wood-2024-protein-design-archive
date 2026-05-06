#!/usr/bin/env python3

import argparse
import requests
import pandas as pd
import os
from datetime import datetime

SEARCH_URL = "https://search.rcsb.org/rcsbsearch/v2/query"
GRAPHQL_URL = "https://data.rcsb.org/graphql"

OUTPUT_CSV = "/home/mchrnwsk/pda-destress-analysis/data/all_pdb_release_dates.csv"


def format_date(date_str):
    """Convert YYYYMMDD -> YYYY-MM-DD"""
    return datetime.strptime(date_str, "%Y%m%d").strftime("%Y-%m-%d")


def get_entry_ids(prev_date, next_date):
    """Fetch PDB IDs released between dates"""
    print(f"[INFO] Fetching PDB IDs between {prev_date} and {next_date}...")

    query = {
        "query": {
            "type": "group",
            "logical_operator": "and",
            "nodes": [
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "rcsb_entry_info.structure_determination_methodology",
                        "operator": "exact_match",
                        "value": "experimental"
                    }
                },
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "rcsb_accession_info.initial_release_date",
                        "operator": "greater",
                        "value": prev_date
                    }
                },
                {
                    "type": "terminal",
                    "service": "text",
                    "parameters": {
                        "attribute": "rcsb_accession_info.initial_release_date",
                        "operator": "less_or_equal",
                        "value": next_date
                    }
                }
            ]
        },
        "return_type": "entry",
        "request_options": {
            "return_all_hits": True
        }
    }

    res = requests.post(SEARCH_URL, json=query)
    res.raise_for_status()
    data = res.json()

    ids = [r["identifier"] for r in data.get("result_set", [])]

    print(f"[INFO] Found {len(ids)} new entries")
    return ids


def chunked(lst, size=1000):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def fetch_release_dates(entry_ids):
    """Fetch release dates via GraphQL"""
    query = """
    query ($ids: [String!]!) {
      entries(entry_ids: $ids) {
        rcsb_id
        rcsb_accession_info {
          initial_release_date
        }
      }
    }
    """

    res = requests.post(GRAPHQL_URL, json={
        "query": query,
        "variables": {"ids": entry_ids}
    })
    res.raise_for_status()

    return res.json()["data"]["entries"]


def get_release_dates(entry_ids):
    """Batch fetch with progress output"""
    results = []

    for i, chunk in enumerate(chunked(entry_ids, 1000), start=1):
        print(f"[INFO] Fetching chunk {i} ({len(chunk)} IDs)...")
        results.extend(fetch_release_dates(chunk))

    print(f"[INFO] Retrieved {len(results)} release dates")
    return results


def load_existing_csv():
    """Load existing CSV or create empty DataFrame"""
    if os.path.exists(OUTPUT_CSV):
        print("[INFO] Loading existing CSV...")
        df = pd.read_csv(OUTPUT_CSV)
    else:
        print("[INFO] No existing CSV found, creating new one...")
        df = pd.DataFrame(columns=["Entry ID", "Release Date"])

    return df


def prepare_new_data(results):
    """Convert API results to DataFrame"""
    rows = []

    for entry in results:
        if entry is None:
            continue

        pdb_id = entry["rcsb_id"].lower()
        date = entry["rcsb_accession_info"]["initial_release_date"]

        # Convert ISO → YYYY-MM-DD
        date = date.split("T")[0]

        rows.append({
            "Entry ID": pdb_id,
            "Release Date": date
        })

    return pd.DataFrame(rows)


def update_csv(new_df):
    """Append + deduplicate"""
    existing_df = load_existing_csv()

    combined = pd.concat([existing_df, new_df], ignore_index=True)

    before = len(combined)
    combined = combined.drop_duplicates(subset="Entry ID", keep="last")
    after = len(combined)

    combined.to_csv(OUTPUT_CSV, index=False)

    print(f"[INFO] CSV updated: {after} total entries ({before - after} duplicates removed)")
    print(f"[INFO] Saved to {OUTPUT_CSV}")


def main(prev, next_):
    prev_fmt = format_date(prev)
    next_fmt = format_date(next_)

    entry_ids = get_entry_ids(prev_fmt, next_fmt)

    if not entry_ids:
        print("[INFO] No new entries found. Nothing to update.")
        return

    results = get_release_dates(entry_ids)
    new_df = prepare_new_data(results)

    update_csv(new_df)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update PDB release dates")
    parser.add_argument("--prev", required=True, help="Previous date (YYYYMMDD)")
    parser.add_argument("--next", required=True, help="Next date (YYYYMMDD)")

    args = parser.parse_args()

    main(args.prev, args.next)