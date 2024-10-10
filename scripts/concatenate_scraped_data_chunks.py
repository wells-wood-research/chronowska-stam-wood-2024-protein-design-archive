import pandas as pd

update_date = "20240930"
previous_update_date = "20240827"

base_dir_data = "/home/mchrnwsk/pda-destress-analysis/data"
base_dir_git = "/home/mchrnwsk/chronowska-stam-wood-2024-protein-design-archive"
data = pd.read_json(base_dir_data+"/"+update_date+"_data.json")

# Filenames:
filename_old_pdb_codes = f"{base_dir_data}/{previous_update_date}_pdb_codes.csv"
filename_new_pdb_codes = f"{base_dir_git}/data/{update_date}_pdb_codes.csv"
filename_pdb_codes_to_manually_add = f"{base_dir_git}/entries_to_manually_include.csv"
filename_pdb_codes_to_manually_remove = f"{base_dir_git}/entries_to_manually_exclude.csv"
filename_output = f"{base_dir_data}/{update_date}_data"


chunk_size = 100
num_chunks = len(data) // chunk_size + 1

new_data_column_names = ["pdb","picture_path", "chains", "authors", "classification", "classification_suggested", "classification_suggested_reason", "subtitle", "tags", "keywords", "release_date", "publication", "publication_ref",  "publication_country", "abstract", "crystal_structure", "symmetry", "exptl_method", "formula_weight", "synthesis_comment", "review", "previous_design", "next_design"]
new_data = pd.DataFrame(columns=new_data_column_names)

for i in range(num_chunks):
    path = f"{filename_output}_{i}"
    df = pd.read_json(path)
    new_data = pd.concat([new_data, df])

def get_prev_and_next_design(df):
    df = df.sort_values("pdb").reset_index(drop=True)
    for i in range(len(df)):
        previous_index = i - 1 if i > 0 else (len(df) - 1)
        next_index = i + 1 if i < (len(df) - 1) else 0
        
        df.at[i, "previous_design"] = df.at[previous_index, "pdb"]
        df.at[i, "next_design"] = df.at[next_index, "pdb"]
    return df

# Tidy up
tidy_data = data.drop_duplicates(subset="pdb")
tidy_data.sort_values(by="pdb", inplace=True)
tidy_data.reset_index(drop=True)
tidy_data["formula_weight"] = tidy_data["formula_weight"].astype(float)

reordered_data = get_prev_and_next_design(tidy_data)

data_result = reordered_data.to_json(base_dir_data+"/"+update_date+"_data_reordered.json", orient="records", indent=4)