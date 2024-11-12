import pandas as pd
import json
import argparse

def main(next_date):
    seq_sim = "bits"
    seq_threshold = 50
    seq_threshold_str = str(round(seq_threshold))
    struct_sim = "lddt"
    struct_threshold = 0.95
    struct_threshold_str = str(round(struct_threshold*100))

    base_dir = "/home/mchrnwsk/pda-destress-analysis"
    base_dir_analysis = f"{base_dir}/similarity"
    base_dir_data = f"{base_dir}/data"

    data = pd.read_json(f"{base_dir_data}/{next_date}_data.json")

    seq_max_sim_dvd = f"{base_dir_analysis}/mmseq/{next_date}/DvD_max_related_sequence_{seq_sim}_{seq_threshold_str}.json"
    seq_max_sim_dvp = f"{base_dir_analysis}/mmseq/{next_date}/DvP_max_related_sequence_{seq_sim}_{seq_threshold_str}.json"
    seq_thr_sim_dvd = f"{base_dir_analysis}/mmseq/{next_date}/DvD_thr_related_sequence_{seq_sim}_{seq_threshold_str}.json"
    seq_thr_sim_dvp = f"{base_dir_analysis}/mmseq/{next_date}/DvP_thr_related_sequence_{seq_sim}_{seq_threshold_str}.json"
    struct_max_sim_dvd = f"{base_dir_analysis}/foldseek/{next_date}/DvD_max_related_structure_{struct_sim}_{struct_threshold_str}.json"
    struct_max_sim_dvp = f"{base_dir_analysis}/foldseek/{next_date}/DvP_max_related_structure_{struct_sim}_{struct_threshold_str}.json"
    struct_thr_sim_dvd = f"{base_dir_analysis}/foldseek/{next_date}/DvD_thr_related_structure_{struct_sim}_{struct_threshold_str}.json"
    struct_thr_sim_dvp = f"{base_dir_analysis}/foldseek/{next_date}/DvP_thr_related_structure_{struct_sim}_{struct_threshold_str}.json"

    with open(seq_max_sim_dvd, "r") as f:
        seq_max_sim_designed = json.load(f)
    with open(seq_max_sim_dvp, "r") as f:
        seq_max_sim_natural = json.load(f)
    with open(seq_thr_sim_dvd, "r") as f:
        seq_thr_sim_designed = json.load(f)
    with open(seq_thr_sim_dvp, "r") as f:
        seq_thr_sim_natural = json.load(f)
    with open(struct_max_sim_dvd, "r") as f:
        struct_max_sim_designed = json.load(f)
    with open(struct_max_sim_dvp, "r") as f:
        struct_max_sim_natural = json.load(f)
    with open(struct_thr_sim_dvd, "r") as f:
        struct_thr_sim_designed = json.load(f)
    with open(struct_thr_sim_dvp, "r") as f:
        struct_thr_sim_natural = json.load(f)

    def get_similarity_data(pdb_code, similarity_dict):
        return similarity_dict.get(pdb_code, [])

    data["seq_thr_sim_designed"] = data["pdb"].apply(lambda x: get_similarity_data(x, seq_thr_sim_designed))
    data["seq_thr_sim_natural"] = data["pdb"].apply(lambda x: get_similarity_data(x, seq_thr_sim_natural))
    data["struct_thr_sim_designed"] = data["pdb"].apply(lambda x: get_similarity_data(x, struct_thr_sim_designed))
    data["struct_thr_sim_natural"] = data["pdb"].apply(lambda x: get_similarity_data(x, struct_thr_sim_natural))

    data["seq_max_sim_designed"] = data["pdb"].apply(lambda x: get_similarity_data(x, seq_max_sim_designed))
    data["seq_max_sim_natural"] = data["pdb"].apply(lambda x: get_similarity_data(x, seq_max_sim_natural))
    data["struct_max_sim_designed"] = data["pdb"].apply(lambda x: get_similarity_data(x, struct_max_sim_designed))
    data["struct_max_sim_natural"] = data["pdb"].apply(lambda x: get_similarity_data(x, struct_max_sim_natural))

    data_result = data.to_json(f"{base_dir_data}/{next_date}_data_similarity.json", orient="records", indent=4)

if __name__ == "__main__":
   # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Add results of MMseqs2 and Foldseek analysis to the dataset')
    parser.add_argument('--next', required=True, help='Next date (e.g., 20240930)')
    args = parser.parse_args()
    
    next_date = args.next

    main(next_date)