import csv
import json
import argparse

def read_results_tsv_to_dict(path):
    data = {}

    with open(path, newline="") as f:
        reader = csv.reader(f, delimiter="\t")

        for row in reader:
            key = row[0].split("_")[0].lower()
            cath = json.loads(row[15])["cath"]

            data.setdefault(key, set()).add(cath)

    return data

def read_names_tsv_to_dict(path):
    data = {}

    with open(path, newline="") as f:
        reader = csv.reader(f, delimiter=" ")

        for row in reader:
            code = row[0]
            label = (" ").join(row[1:])

            data[code] = label

    return data

def get_code_name(lookup, code):
    if lookup.get(code, None) is not None:
        return {"code": code, "name": lookup[code]}
    return None

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Add merzio-search metadata to scraped dataset json.')
    parser.add_argument('--json', required=True, help='e.g. /home/mchrnwsk/pda/foldseek/20260202/20260202_data_scraped.json')
    parser.add_argument('--tsv', required=True, help='e.g. /home/mchrnwsk/pda/foldseek/20260202/cath_results_search.tsv')
    parser.add_argument('--out', required=True, help='e.g. /home/mchrnwsk/pda/foldseek/20260202/20260202_data_merizo.json')

    args = parser.parse_args()
    
    scraped_json_path = args.json
    merizo_results_path = args.tsv
    output_file = args.out
    merizo_name_lookup_path = "/home/mchrnwsk/pda/merizo_search/database/cath-b-newest-names"

    merizo_data = read_results_tsv_to_dict(merizo_results_path)
    with open(scraped_json_path, 'r') as f:
        json_data = json.load(f)

    merizo_results_lookup = {k: list(v) for k, v in merizo_data.items()}
    merizo_name_lookup = read_names_tsv_to_dict(merizo_name_lookup_path)
    
    for entry in json_data:
        # Always initialize — guarantees empty lists
        entry["cath_full"] = []
        entry["cath_class"] = []
        entry["cath_arch"] = []

        pdb = entry.get("pdb")
        if pdb not in merizo_results_lookup:
            continue

        full_codes = merizo_results_lookup[pdb]
        class_codes = set()
        arch_codes = set()

        for code in full_codes:
            class_codes.add(code.split(".")[0])
            arch_codes.add(".".join(code.split(".")[:2]))

        entry["cath_full"] = [
            d for code in full_codes
            if (d := get_code_name(merizo_name_lookup, code)) is not None
        ]
        entry["cath_class"] = [
            d for code in class_codes
            if (d := get_code_name(merizo_name_lookup, code)) is not None
        ]
        entry["cath_arch"] = [
            d for code in arch_codes
            if (d := get_code_name(merizo_name_lookup, code)) is not None
        ]
    
    # Save the results as JSON
    with open(output_file, "w") as outfile:
        json.dump(json_data, outfile, indent=4)