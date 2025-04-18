import pandas as pd
import json
import datetime

# Struct or chains
anal_type = "struct"
base_dir = f"/home/mchrnwsk/fs5/{anal_type}/"

# Define the metrics
metrics = ["prob", "lddt", "alntmscore", "evalue"]

# Dynamically create file paths and dictionaries for each metric
output_files = {
    metric: base_dir + f"analysis/foldseek_related_by_{metric}.json"
    for metric in metrics
}
dicts = {
    metric: {}
    for metric in metrics
}

# Load data
data = pd.read_json(base_dir + "analysis/20240827_data.json")
pdb_release = pd.read_csv(base_dir + "analysis/combined.csv")

# Preprocess data into dictionaries for faster lookup
data_dict = dict(zip(data["pdb"].str.lower(), data["release_date"]))
pdb_release_dict = dict(zip(pdb_release["Entry ID"].str.lower(), pdb_release["Release Date"]))
excluded_pdbs = set(data["pdb"].str.lower())
dict_name = {}

chunksize = 10000
for chunk in pd.read_csv(base_dir + "output/resultDB", sep="\t", header=None, names=[
    "query_name", "query_length", "target_name", "target_length", 
    "prob", "lddt", "pident", "cigar", 
    "fragment_of+query_covered_by_target", "fragment_of_target_covered_by_query", 
	"alntmscore", "lddt_1", "evalue", "bits"], chunksize=chunksize, dtype={
        "prob": "float32", "lddt": "float32", "pident": "float32", 
        "alntmscore": "float32", "evalue": "float32", "bits": "float32"}):

    # Iterate through file_name DataFrame
    for i, row in chunk.iterrows():
        if i % 1000 == 0:
            print(f"{anal_type}: {i}/{len(chunk)}")
        
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
        for metric in metrics:
            similarity = row[metric]
            if query_name not in dicts[metric]:
                dicts[metric][query_name] = []
            if similarity > 0.9:
                dicts[metric][query_name].append({"sim": similarity, "partner": target_name})

# Save the results as JSON for each metric
for metric in metrics:
    with open(output_files[metric], "w") as outfile:
        json.dump(dicts[metric], outfile)
