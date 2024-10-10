import pandas as pd
import argparse

update_date = "20240930"

parser = argparse.ArgumentParser(description="Process MMseqs2 analysis")
parser.add_argument("-i", "--input", default="reordered", type=str, required=True, help="Label of data input (just \"reordered\" for \"20240930_data_reordered.json\")")
parser.add_argument("-o", "--output", default="curated", type=str, required=True, help="Label of data output (just \"curated\" for \"20240930_data_curated.json\")")
args = parser.parse_args()

input_type = args.input
output_type = args.output

base_dir_data = "/home/mchrnwsk/pda-destress-analysis/data"
base_dir_git = "/home/mchrnwsk/chronowska-stam-wood-2024-protein-design-archive"
data = pd.read_json(base_dir_data+"/"+update_date+"_data_"+input_type+".json")

data["review_comment"] = pd.Series([[""]] * len(data))

index_7jzl = data.loc[data["pdb"] == "7jzl"].index[0]
chains_7jzl = data[data["pdb"] == "7jzl"]["chains"].values
chains_7jzl[0][1]["chain_source"] = "synthetic construct"
chains_7jzl[0][1]["chain_type"] = "D"
data.loc[data["pdb"] == "7jzl", "chains"] = chains_7jzl
data.at[index_7jzl, "review_comment"] = ["2024-10-06: Confirm chain E,G,F to be de novo designed rather than unknown"]

index_5i9d = data.loc[data["pdb"] == "5i9d"].index[0]
chains_5i9d = data[data["pdb"] == "5i9d"]["chains"].values
chains_5i9d[0][0]["chain_source"] = "synthetic construct"
chains_5i9d[0][0]["chain_type"] = "D"
chains_5i9d[0][1]["chain_source"] = "RNA"
chains_5i9d[0][1]["chain_type"] = "N"
data.loc[data["pdb"] == "5i9d", "chains"] = chains_5i9d
data.at[index_5i9d, "review_comment"] = [["2024-10-06: Confirm chain A to be de novo designed rather than unknown", "2024-10-06: Confirm chain B to be RNA rather than de novo designed"]]

index_1mey = data.loc[data["pdb"] == "1mey"].index[0]
chains_1mey = data[data["pdb"] == "1mey"]["chains"].values
chains_1mey[0][0]["chain_source"] = "DNA"
chains_1mey[0][0]["chain_type"] = "N"
chains_1mey[0][1]["chain_source"] = "DNA"
chains_1mey[0][1]["chain_type"] = "N"
chains_1mey[0][2]["chain_source"] = "synthetic construct"
chains_1mey[0][2]["chain_type"] = "D"
data.loc[data["pdb"] == "1mey", "chains"] = chains_1mey
data.at[index_1mey, "review_comment"] = [["2024-10-07: Confirm chains A, D, B, E to be DNA rather than unknown", "2024-10-07: Confirm chain C, F, G to be de novo designed rather than unknown"]]

data_result = data.to_json(base_dir_data+"/"+update_date+"_data_"+output_type+".json", orient="records", indent=4)