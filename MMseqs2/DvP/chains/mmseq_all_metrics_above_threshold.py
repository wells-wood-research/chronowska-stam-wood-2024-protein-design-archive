import pandas as pd
import json
import datetime

# Struct or chain
analysis_type = "dvp, chains"
result_dir = "/home/mchrnwsk/personal/pda-destress-analysis/similarity/mmseq/try4/d-v-p/chains/"
output_dir = "/home/mchrnwsk/chronowska-stam-wood-2024-protein-design-archive/MMseqs2/DvP/chains/"
data_dir = "/home/mchrnwsk/personal/pda-destress-analysis/data/"

# Define the metrics
metrics = ["pident", "bits"]

# Dynamically create file paths and dictionaries for each metric
output_files = {
    metric: output_dir + f"mm_related_by_{metric}.json"
    for metric in metrics
}
dicts = {
    metric: {}
    for metric in metrics
}

# Load data
file_name = pd.read_csv(result_dir + "results.m8", sep="\t", header=None, index_col=False, names=["query_name", "query_length", "target_name", "target_length", "bits", "pident", "raw", "cigar", "fragment_of_query_covered_by_target", "fragment_of_target_covered_by_query"])
data = pd.read_json(data_dir + "20240827_data.json")
pdb_release = pd.read_csv(data_dir + "pdb_release_dates/combined.csv")

# Preprocess data into dictionaries for faster lookup
data_dict = dict(zip(data["pdb"].str.lower(), data["release_date"]))
pdb_release_dict = dict(zip(pdb_release["Entry ID"].str.lower(), pdb_release["Release Date"]))
excluded_pdbs = set(data["pdb"].str.lower())

# Iterate through file_name DataFrame
for i, row in file_name.iterrows():
    if i % 1000 == 0:
        print(f"{analysis_type}: {i}/{len(file_name)}")
        
    query_name = row["query_name"][:4].lower()
    target_name = row["target_name"][:4].lower()
    
    if query_name == target_name or target_name in excluded_pdbs:
        continue

    try:
        query_release = datetime.date.fromisoformat(data_dict[query_name])
        target_release = datetime.date.fromisoformat(pdb_release_dict.get(target_name, "1900-01-01"))
    except KeyError as e:
        print(f"Error at query: {query_name}. Missing release date for target: {target_name}")
        continue

    if query_release < target_release:
        continue

    # Iterate over each metric and update the respective dictionary
    sim_pident = row["pident"]
    if query_name not in dicts["pident"]:
        dicts["pident"][query_name] = []
    if sim_pident > 90:
        dicts["pident"][query_name].append({"sim": sim_pident, "partner": target_name})

    sim_bits = row["bits"]
    if query_name not in dicts["bits"]:
        dicts["bits"][query_name] = []
    if sim_bits > 300:
        dicts["bits"][query_name].append({"sim": sim_bits, "partner": target_name})

# Save the results as JSON for each metric
for metric in metrics:
    with open(output_files[metric], "w") as outfile:
        json.dump(dicts[metric], outfile)