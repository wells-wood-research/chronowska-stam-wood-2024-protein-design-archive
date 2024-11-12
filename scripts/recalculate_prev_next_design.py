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

def main(next_date):
    base_dir_data = "/home/mchrnwsk/pda-destress-analysis/data"
    data = pd.read_json(base_dir_data+"/"+next_date+"_data_reordered.json")
    # Tidy up
    data.drop_duplicates(subset="pdb", inplace=True)
    data.sort_values(by="pdb", inplace=True)
    data.reset_index(drop=True)
    data["formula_weight"] = data["formula_weight"].astype(float)

    reordered_data = get_prev_and_next_design(data)

    data_result = reordered_data.to_json(base_dir_data+"/"+next_date+"_data_reordered.json", orient="records", indent=4)

if __name__ == "__main__":
   # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Recalculate previous and next designs')
    parser.add_argument('--next', required=True, help='Next date (e.g., 20240930)')
    args = parser.parse_args()
    
    next_date = args.next

    main(next_date)