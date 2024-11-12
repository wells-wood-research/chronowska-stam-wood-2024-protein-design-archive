import os
import argparse
import pandas as pd

def main(next_date, to_delete_path):
    # Set the directory path and CSV file path
    base_dir = "/home/mchrnwsk/pda-destress-analysis"
    base_dir_data = f"{base_dir}/data"
    data = pd.read_json(f"{base_dir_data}/{next_date}_data.json")

    # Iterate over files in the directory
    for filename in os.listdir(to_delete_path):
        filepath = os.path.join(to_delete_path, filename)
        if os.path.isfile(filepath):
            name_without_extension = os.path.splitext(filename)[0]
            name_without_chain_label = name_without_extension.split("_")[0]
            if name_without_chain_label.lower() not in data["pdb"].values:
                os.remove(filepath)
                print(f"Deleted: {filename}")

if __name__ == "__main__":
   # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Remove files from PDB if not found in dataset')
    parser.add_argument('--next', required=True, help='Next date (e.g., 20240930)')
    parser.add_argument('--dir', required=True, help='Path to directory from which to delete files')
    args = parser.parse_args()
    
    next_date = args.next
    to_delete_path = args.dir

    main(next_date, to_delete_path)