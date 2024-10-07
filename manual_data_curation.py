import pandas as pd
import numpy as np

filename_dataset = "/home/mchrnwsk/chronowska-stam-wood-2024-protein-design-archive/data/20240930_data"

data = pd.read_json(filename_dataset+".json")

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

data_result = data.to_json(filename_dataset+"_curated.json", orient="records", indent=4)