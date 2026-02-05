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

def format_codes(codes, newline_every):
    codes = list(codes)
    if not newline_every or newline_every <= 0:
        return ",".join(codes)

    lines = [
        ",".join(codes[i:i + newline_every])
        for i in range(0, len(codes), newline_every)
    ]
    return "\n\n".join(lines)

def output_codes(result_codes, output_file, newline_every):
    output_string = format_codes(result_codes, newline_every)

    if output_file:
        with open(output_file, 'w') as file:
            file.write(output_string)
    else:
        print(output_string)
        print("Number of new codes:", len(result_codes))

def main(file_to_print, file_to_exclude, uppercase_print, output_file, newline_every):
    codes_to_print = set(get_pdb_codes(file_to_print, uppercase_print))

    if file_to_exclude:
        codes_to_exclude = set(get_pdb_codes(file_to_exclude, uppercase_print))
        result_codes = {code.upper() for code in codes_to_print} - {code.upper() for code in codes_to_exclude}
        common_codes = {code.upper() for code in codes_to_print} & {code.upper() for code in codes_to_exclude}
        print("In common (e.g. newly excluded or previously manually added): ", common_codes)
    else:
        result_codes = codes_to_print

    output_codes(result_codes, output_file, newline_every)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Print PDB codes as "code, code, code"; optionally insert newlines.'
    )
    parser.add_argument('--file', required=True, help='File from which to print PDB codes')
    parser.add_argument('--exclude', default=None, help='File of PDB codes to exclude')
    parser.add_argument('--uppercase', action='store_true', help='Print codes in uppercase')
    parser.add_argument('--output', default=None, help='File to save the output')
    parser.add_argument(
        '--newline-every', '-n',
        type=int,
        default=None,
        help='Insert a newline after every N codes'
    )

    args = parser.parse_args()

    main(
        file_to_print=args.file,
        file_to_exclude=args.exclude,
        uppercase_print=args.uppercase,
        output_file=args.output,
        newline_every=args.newline_every
    )
