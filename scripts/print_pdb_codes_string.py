import pandas as pd
import json
import argparse

def get_pdb_codes_from_json(file_path, uppercase_print):
    with open(file_path, 'r') as file:
        data = json.load(file)
    if uppercase_print:
        return [entry['pdb'].upper() for entry in data]
    else:
        return [entry['pdb'] for entry in data]

def get_pdb_codes_from_csv(file_path, uppercase_print):
    df = pd.read_csv(file_path, header=None)
    if uppercase_print:
        return [code.upper() for code in df[0].tolist()]
    else:
        return df[0].tolist()

def get_pdb_codes_from_txt(file_path, uppercase_print):
    with open(file_path, 'r') as file:
        # Read the file, split by commas, and strip any whitespace from each entry
        codes = [code.strip() for code in file.read().split(',')]
    if uppercase_print:
        return [code.upper() for code in codes]
    else:
        return codes

def get_pdb_codes(file_path, uppercase_print):
    if file_path.endswith('.json'):
        return get_pdb_codes_from_json(file_path, uppercase_print)
    elif file_path.endswith('.csv'):
        return get_pdb_codes_from_csv(file_path, uppercase_print)
    elif file_path.endswith('.txt'):
        return get_pdb_codes_from_txt(file_path, uppercase_print)
    else:
        raise ValueError("Unsupported file type")

def output_codes(result_codes, output_file):
    output_string = ", ".join(result_codes)
    if output_file:
        with open(output_file, 'w') as file:
            file.write(output_string)
    else:
        print(output_string)
        print("Number of new codes:", len(result_codes))

def main(file_to_print, file_to_exclude, uppercase_print, output_file):
    codes_to_print = set(get_pdb_codes(file_to_print, uppercase_print))

    if file_to_exclude:
        codes_to_exclude = set(get_pdb_codes(file_to_exclude, uppercase_print))
        result_codes = {code.upper() for code in codes_to_print} - {code.upper() for code in codes_to_exclude}
    else:
        result_codes = codes_to_print

    output_codes(result_codes, output_file)

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Print PDB codes as "code, code, code" etc.; Example usage: python print_pdb_codes_string.py --file path_to_print --exclude path_to_exclude --uppercase True')
    parser.add_argument('--file', required=True, help='File from which to print PDB codes, can be .CSV, .JSON, or .TXT')
    parser.add_argument('--exclude', default=None, help='If PDB code found in this file, don\'t print; can be .CSV, .JSON, or .TXT')
    parser.add_argument('--uppercase', action='store_true', help='Whether to print codes in uppercase')
    parser.add_argument('--output', default=None, help='File to save the output; prints to command line if not specified')
    args = parser.parse_args()
    
    file_to_print = args.file
    file_to_exclude = args.exclude
    uppercase_print = args.uppercase   
    output_file = args.output
    
    main(file_to_print, file_to_exclude, uppercase_print, output_file)
