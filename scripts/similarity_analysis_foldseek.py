import pandas as pd
import json
import datetime
import argparse
import gc
import statistics

# Setup argument parser
parser = argparse.ArgumentParser(description="Process Foldseek analysis")
parser.add_argument("-d", "--date", type=str, required=True, help="Update date in iso format (20240930)")
parser.add_argument("-a", "--analysis_type", type=str, required=True, help="Analysis type (DvD or DvP)")
parser.add_argument("-m", "--metric", default="lddt", type=str, required=True, help="Metric to use (lddt)")
parser.add_argument("-t", "--threshold", default=0.9, type=float, required=True, help="Threshold for metric similarity (0.9)")
args = parser.parse_args()

# Assign command-line arguments to variables
update_date = args.date
analysis_type = args.analysis_type
metric = args.metric
threshold = args.threshold

# Define paths for Foldseek output files
base_dir = "/home/mchrnwsk/pda/foldseek"
base_dir_current = base_dir+"/"+update_date
current_dir_foldseek = base_dir_current+"/"+analysis_type
current_dir_foldseek_analysis = current_dir_foldseek+"/"+"analysis"
output_file = base_dir_current+"/"+analysis_type+"_related_structure"+"_"+str(metric)+"_"+str(round(threshold*100))

# Load data
data = pd.read_json(current_dir_foldseek_analysis+"/"+update_date+"_data.json")
pdb_release = pd.read_csv(current_dir_foldseek_analysis+"/"+"all_pdb_release_dates.csv")

# Preprocess data into dictionaries for faster lookup
data_dict = dict(zip(data["pdb"].str.lower(), data["release_date"]))
results = pd.read_csv(current_dir_foldseek+"/"+"output/resultDB", sep="\t")
pdb_release_dict = dict(zip(pdb_release["Entry ID"].str.lower(), pdb_release["Release Date"]))
if analysis_type != "DvD":
    excluded_pdbs = set(data["pdb"].str.lower())
metric_dict = {}

chunksize = 10000
for chunk in pd.read_csv(current_dir_foldseek+"/"+"output/resultDB", sep="\t", header=None, names=[
    "query","qlen","target","tlen","prob","lddt","pident","cigar","qcov","tcov","alntmscore","lddt1","evalue","bits"], chunksize=chunksize, dtype={
        "prob": "float32", "lddt": "float32", "pident": "float32", 
        "alntmscore": "float32", "evalue": "float32", "bits": "float32"}):

    for i, row in chunk.iterrows():
        if i % 1000 == 0:
            print(f"{analysis_type}: {i}/{len(results)}")
        
        query_name = row["query"][:4].lower()
        target_name = row["target"][:4].lower()
        
        if query_name == target_name:
            continue

        if analysis_type != "DvD":
            if target_name in excluded_pdbs:
                continue

        try:
            query_release = datetime.date.fromisoformat(data_dict[query_name])
            target_release = datetime.date.fromisoformat(pdb_release_dict.get(target_name, "1900-01-01"))
        except KeyError as e:
            print(f"Error at query: {query_name}. Missing release date for target: {target_name}")
            continue

        if analysis_type != "DvD":
            if query_release < target_release:
                continue
        
        similarity = row[metric]
        
        if similarity >= threshold:
            # Check if query_name is already in metric_dict
            if query_name not in metric_dict:
                # Add new entry for query_name
                metric_dict[query_name] = [{"sim": similarity, "partner": target_name}]
            else:
                # Check if target_name already exists
                existing_entry = next((entry for entry in metric_dict[query_name] if entry["partner"] == target_name), None)
                
                if existing_entry:
                    # Compare and keep the higher similarity
                    if similarity > existing_entry["sim"]:
                        existing_entry["sim"] = similarity
                else:
                    # Add the new target_name with its similarity
                    metric_dict[query_name].append({"sim": similarity, "partner": target_name})

    del chunk
    gc.collect()

# Save the results as JSON
with open(output_file+".json", "w") as outfile:
    json.dump(metric_dict, outfile)

print("")
print("Output saved to: ", output_file+".json")

# Calculate statistics
lengths = [len(entry) for entry in metric_dict.values()]
max_length = max(lengths)
min_length = min(lengths)
mean_length = sum(lengths) / len(lengths)
median_length = statistics.median(lengths)

# Print statistics
print("")
print(f"Max: {max(lengths)}, min: {min(lengths)}")
print(f"Mean: {round(sum(lengths) / len(lengths))}, median: {round(statistics.median(lengths))}")

# Sort lengths and count the top and bottom values
lengths_dict = {}
for v in metric_dict.values():
    key = str(len(v))
    if key not in lengths_dict:
        lengths_dict[key] = 1
    else:
        lengths_dict[key] += 1

sorted_lengths = sorted(lengths, reverse=True)

sorted_dict = sorted(lengths_dict, key=lengths_dict.get, reverse=False)

print("")
for key in sorted_dict[:5]:
    print(f"{lengths_dict[key]} designs have {key} related structures")
print("")
for key in sorted_dict[-5:]:
    print(f"{lengths_dict[key]} designs have {key} related structures")

# Draw distribution graph
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt

bins_range = 150
bins = range(0, bins_range, 1)
plt.rcParams["font.family"] = "monospace"
fig = plt.figure(figsize=(12, 3))
plt.title("Distribution of number of related structure of de novo designed chains", fontsize=14)
plt.hist(lengths, bins=bins, range=(0, bins_range))
plt.grid()
plt.xlabel("Number of related structures", fontsize=14)
plt.ylabel("Number of designs", fontsize=14)
plt.xticks(range(0, bins_range+5, 5), rotation=90, fontsize=14)
plt.yticks(fontsize=14)
plt.xlim(0, bins_range)
plt.savefig(output_file+".svg", bbox_inches='tight')