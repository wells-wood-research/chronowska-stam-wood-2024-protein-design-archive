import pandas as pd
import glob
import os

# Download by going to:
# 1. https://www.rcsb.org/search?request=%7B%22query%22%3A%7B%22type%22%3A%22group%22%2C%22nodes%22%3A%5B%7B%22type%22%3A%22group%22%2C%22nodes%22%3A%5B%7B%22type%22%3A%22group%22%2C%22nodes%22%3A%5B%7B%22type%22%3A%22terminal%22%2C%22service%22%3A%22text%22%2C%22parameters%22%3A%7B%22attribute%22%3A%22rcsb_entry_info.structure_determination_methodology%22%2C%22operator%22%3A%22exact_match%22%2C%22value%22%3A%22experimental%22%7D%7D%5D%2C%22logical_operator%22%3A%22and%22%7D%5D%2C%22logical_operator%22%3A%22and%22%2C%22label%22%3A%22text%22%7D%5D%2C%22logical_operator%22%3A%22and%22%7D%2C%22return_type%22%3A%22entry%22%2C%22request_options%22%3A%7B%22scoring_strategy%22%3A%22combined%22%2C%22results_content_type%22%3A%5B%22experimental%22%5D%2C%22paginate%22%3A%7B%22start%22%3A0%2C%22rows%22%3A25%7D%2C%22sort%22%3A%5B%7B%22sort_by%22%3A%22score%22%2C%22direction%22%3A%22desc%22%7D%5D%7D%2C%22request_info%22%3A%7B%22query_id%22%3A%22e0fff76e6009d1aefc3970505b66f430%22%7D%7D
# 2. selecting "Create Custom Report" instead of "Tabular Report"
# 3. download only the most recent file - last download up to 225'681

# Specify the directory containing the CSV files
directory = "/home/mchrnwsk/pda-destress-analysis/data/pdb_release_dates"
# Use glob to get all the CSV file paths
all_files = glob.glob(os.path.join(directory, "*.csv"))

# Create an empty list to hold the DataFrames
dfs = []

# Loop over the file paths and read each file
for file in all_files:
    df = pd.read_csv(file, header=1)  # read the CSV file
    dfs.append(df)          # append the DataFrame to the list

# Concatenate all the DataFrames into one
combined_df = pd.concat(dfs, ignore_index=True)

combined_df["Entry ID"] = combined_df["Entry ID"].str.lower()

combined_df.to_csv("/home/mchrnwsk/pda-destress-analysis/data/all_pdb_release_dates.csv", sep=",", index=False)