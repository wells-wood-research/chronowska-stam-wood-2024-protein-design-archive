import pandas as pd
import argparse

def get_prev_and_next_design(df):
    df = df.sort_values("pdb").reset_index(drop=True)
    for i in range(len(df)):
        previous_index = i - 1 if i > 0 else (len(df) - 1)
        next_index = i + 1 if i < (len(df) - 1) else 0
        
        df.at[i, "previous_design"] = df.at[previous_index, "pdb"]
        df.at[i, "next_design"] = df.at[next_index, "pdb"]
    return df

def main(next_date, input_type, output_type):
    base_dir_data = "/home/mchrnwsk/pda-destress-analysis/data"
    base_dir_git = "/home/mchrnwsk/chronowska-stam-wood-2024-protein-design-archive"
    data = pd.read_json(base_dir_data+"/"+next_date+"_data_"+input_type+".json")

    filename_pdb_codes_to_manually_remove = f"{base_dir_git}/entries_to_manually_exclude.csv"
    pdb_codes_to_manually_remove = pd.read_csv(filename_pdb_codes_to_manually_remove, sep=",", header=None).reset_index(drop=True)

    data.drop_duplicates(subset="pdb", inplace=True)
    data = data[~data["pdb"].isin(pdb_codes_to_manually_remove[0])]
    data.sort_values(by="pdb", inplace=True)
    data.reset_index(drop=True, inplace=True)
    data["formula_weight"] = data["formula_weight"].astype(float)

    reordered_data = get_prev_and_next_design(data)

    data_result = reordered_data.to_json(base_dir_data+"/"+next_date+"_data_"+output_type+".json", orient="records", indent=4)

if __name__ == "__main__":
   # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Remove entries labelled for extraction')
    parser.add_argument('--next', required=True, help='Next date (e.g., 20240930)')
    parser.add_argument("-i", "--input", default="similarity", type=str, required=True, help="Label of data input (just \"similarity\" for \"20240930_data_similarity.json\")")
    parser.add_argument("-o", "--output", default="reordered", type=str, required=True, help="Label of data output (just \"reordered\" for \"20240930_data_reordered.json\")")
    args = parser.parse_args()
    
    next_date = args.next
    input_type = args.input
    output_type = args.output

    main(next_date, input_type, output_type)