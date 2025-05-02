import pandas as pd
import json
import datetime
import argparse
import gc
import statistics

# Setup argument parser
parser = argparse.ArgumentParser(description="Process Foldseek analysis")
parser.add_argument("-d", "--date", type=str, required=True, help="Update date in iso format (20240930)")
parser.add_argument("-a", "--thr_or_max", type=str, required=True, help="Find metric values above threshold or highest per design (\"thr\" or \"max\")")
parser.add_argument("-p", "--prot_or_des", type=str, required=True, help="Compare designs against designs or natural proteins (\"DvD\" or \"DvP\")")
parser.add_argument("-m", "--metric", default="lddt", type=str, required=True, help="Metric to use (lddt)")
parser.add_argument("-t", "--threshold", default=0.9, type=float, required=True, help="Threshold for metric similarity (0.9)") # Always required for naming
args = parser.parse_args()

# Assign command-line arguments to variables
update_date = args.date
thr_or_max = args.thr_or_max
prot_or_des = args.prot_or_des
metric = args.metric
threshold = args.threshold

# Define paths for Foldseek output files
base_dir = "/home/mchrnwsk/pda/foldseek"
base_dir_current = base_dir+"/"+update_date
current_dir_foldseek = base_dir_current+"/"+prot_or_des
current_dir_foldseek_analysis = current_dir_foldseek+"/"+"analysis"
output_file = base_dir_current+"/"+prot_or_des+"_"+thr_or_max+"_related_structure"+"_"+str(metric)+"_"+str(round(threshold*100))

# Load data
data = pd.read_json(current_dir_foldseek_analysis+"/"+update_date+"_data_scraped.json")
pdb_release = pd.read_csv(current_dir_foldseek_analysis+"/"+"all_pdb_release_dates.csv")

# Preprocess data into dictionaries for faster lookup
data_dict = dict(zip(data["pdb"].str.lower(), data["release_date"]))
results = pd.read_csv(current_dir_foldseek+"/"+"output/resultDB", sep="\t")
pdb_release_dict = dict(zip(pdb_release["Entry ID"].str.lower(), pdb_release["Release Date"]))
excluded_pdbs = set(data["pdb"].str.lower())
metric_dict = {}

chunksize = 10000
for chunk in pd.read_csv(current_dir_foldseek+"/"+"output/resultDB", sep="\t", header=None, names=[
    "query","qlen","target","tlen","prob","lddt","pident","cigar","qcov","tcov","alntmscore","lddt1","evalue","bits"], chunksize=chunksize, dtype={
        "prob": "float32", "lddt": "float32", "pident": "float32", 
        "alntmscore": "float32", "evalue": "float32", "bits": "float32"}):

    for i, row in chunk.iterrows():
        if i % 1000 == 0:
            print(f"{prot_or_des}: {i}/{len(results)}")
        
        query_name = row["query"][:4].lower() # designed protein
        target_name = row["target"][:4].lower() # designed or natural protein
        
        if prot_or_des != "DvD":
            if target_name in excluded_pdbs:
                continue

        try:
            query_release = datetime.date.fromisoformat(data_dict[query_name])
            target_release = datetime.date.fromisoformat(pdb_release_dict.get(target_name, "1900-01-01"))
        except KeyError as e:
            print(f"Error at query: {query_name}, target: {target_name}. {e} not found.")
            continue

        if prot_or_des != "DvD":
            if query_release < target_release:
                continue
        
        similarity = row[metric]

        if query_name == target_name:
            similarity = 0.0 # self-comparison
        
        if thr_or_max == "thr":
            if similarity >= threshold:
                if query_name not in metric_dict:
                    metric_dict[query_name] = [{"sim": similarity, "partner": target_name}]
                else:
                    existing_entry = next((entry for entry in metric_dict[query_name] if entry["partner"] == target_name), None)
                    
                    if existing_entry:
                        if similarity > existing_entry["sim"]:
                            existing_entry["sim"] = similarity
                    else:
                        metric_dict[query_name].append({"sim": similarity, "partner": target_name})
        else:
            if query_name not in metric_dict:
                metric_dict[query_name] = {"sim": similarity, "partner": target_name}
            else:
                if metric_dict[query_name]["sim"] < similarity:
                    metric_dict[query_name] = {"sim": similarity, "partner": target_name}
                else:
                    continue

    del chunk
    gc.collect()

# Save the results as JSON
with open(output_file+".json", "w") as outfile:
    json.dump(metric_dict, outfile)

print("")
print("Output saved to: ", output_file+".json")

if thr_or_max == "thr":
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
