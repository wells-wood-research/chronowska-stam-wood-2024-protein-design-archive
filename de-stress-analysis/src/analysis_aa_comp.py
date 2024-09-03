# 0. Importing packages and defining custom functions-------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from matplotlib.colors import LinearSegmentedColormap


# Function to convert year_group format
def convert_year_group_format(year_group):

    # Remove the first two characters
    year_group = year_group[3:]

    # Replace ',' with '-'
    year_group = year_group.replace(", ", "-")

    # Use regular expression to remove the first two characters after '-'
    year_group = re.sub(r"-(..)", "-", year_group)

    # Remove the trailing character ')'
    year_group = year_group[:-1]

    return year_group


# 1. Defining variables--------------------------------------------------

aa_comp_data_path = "de-stress-analysis/data/processed_data/aa_comp.csv"

# Defining a file path for the PDB aa composition
pdb_aa_comp_path = "de-stress-analysis/data/processed_data/pdb_aa_comp.csv"

# List of amino acid one letter codes
amino_acids_one_letter = [
    "A",
    "R",
    "N",
    "D",
    "C",
    "Q",
    "E",
    "G",
    "H",
    "I",
    "L",
    "K",
    "M",
    "F",
    "P",
    "S",
    "T",
    "W",
    "Y",
    "V",
    "X",
]

# Defining analysis path
analysis_path = "de-stress-analysis/analysis/"

# Defining year group order
year_groups_order = [
    "90-95",
    "95-00",
    "00-05",
    "05-10",
    "10-15",
    "15-20",
    "20-25",
    "PDB",
]

# 2. Reading in data------------------------------------------------------

aa_comp_data = pd.read_csv(aa_comp_data_path)

# Reading in PDB aa comp data
pdb_aa_comp_df = pd.read_csv(pdb_aa_comp_path)

# 3. Processing aa_comp_data-------------------------------------------------------

# Define the boundaries for the groups
year_groups = pd.cut(
    aa_comp_data["release_year"], bins=range(1990, 2026, 5), right=False
)

# Assign the year groups to a new column in the DataFrame
aa_comp_data["year_group"] = year_groups

# Apply the function to the year_group column
aa_comp_data["year_group"] = (
    aa_comp_data["year_group"].astype(str).apply(convert_year_group_format)
)

# Extracting seq length
aa_comp_data["seq_len"] = aa_comp_data["seq"].str.len()

# Group by year and aggregate sum of sequence lengths and amino acid counts
aa_comp_grouped_df = (
    aa_comp_data.groupby("year_group")
    .agg({"seq_len": "sum", **{aa: "sum" for aa in amino_acids_one_letter}})
    .reset_index()
)

# Divide each amino acid count column by sequence length column
for amino_acid in amino_acids_one_letter:
    aa_comp_grouped_df[amino_acid] = (
        aa_comp_grouped_df[amino_acid] / aa_comp_grouped_df["seq_len"]
    )

aa_comp_grouped_df = aa_comp_grouped_df[["year_group"] + amino_acids_one_letter]

# Creating release year flag for PDB data
pdb_aa_comp_df["year_group"] = "PDB"

# Extracting seq length
pdb_aa_comp_df["seq_len"] = pdb_aa_comp_df["seq"].str.len()

# Group by year and aggregate sum of sequence lengths and amino acid counts
pdb_aa_comp_grouped_df = (
    pdb_aa_comp_df.groupby("year_group")
    .agg({"seq_len": "sum", **{aa: "sum" for aa in amino_acids_one_letter}})
    .reset_index()
)

# Divide each amino acid count column by sequence length column
for amino_acid in amino_acids_one_letter:
    pdb_aa_comp_grouped_df[amino_acid] = (
        pdb_aa_comp_grouped_df[amino_acid] / pdb_aa_comp_grouped_df["seq_len"]
    )

pdb_aa_comp_grouped_df.drop(["seq_len"], inplace=True, axis=1)

# Joining data
aa_comp_grouped_df = pd.concat(
    [aa_comp_grouped_df, pdb_aa_comp_grouped_df], axis=0
).reset_index(drop=True)

# Sort the DataFrame by 'year_group' to enforce the order
aa_comp_grouped_df["year_group"] = pd.Categorical(
    aa_comp_grouped_df["year_group"], categories=year_groups_order, ordered=True
)
aa_comp_grouped_df = aa_comp_grouped_df.sort_values("year_group").reset_index(drop=True)

aa_comp_grouped_df = aa_comp_grouped_df[aa_comp_grouped_df["year_group"] != "90-95"]

# Sorting the amino acid residues by the highest proportions
pdb_row = aa_comp_grouped_df[aa_comp_grouped_df["year_group"] == "PDB"].iloc[0]
sorted_columns = pdb_row.drop("year_group").sort_values(ascending=False).index.tolist()
aa_comp_grouped_df = aa_comp_grouped_df[["year_group"] + sorted_columns]


aa_comp_grouped_df.to_csv(analysis_path + "aa_proportions_by_year.csv", index=False)


# 4. Plotting ---------------------------------------------------------------------------------

# Define the custom colormap
colors = ["blue", "white", "red"]
n_bins = 100  # Number of bins
custom_cmap = LinearSegmentedColormap.from_list(
    "custom_blue_white_red", colors, N=n_bins
)


aa_comp_grouped_df_heatmap = aa_comp_grouped_df

# Setting the 'Year Group' as the index
aa_comp_grouped_df_heatmap.set_index("year_group", inplace=True)

# Transposing data
aa_comp_grouped_df_heatmap = aa_comp_grouped_df_heatmap.transpose()

# Calculate percentage differences from PDB and absolute percentages
pdb_values = aa_comp_grouped_df_heatmap["PDB"]
pdb_values_np = np.array(pdb_values)
absolute_values = aa_comp_grouped_df_heatmap
df_percentage_diff = (
    ((absolute_values - pdb_values_np[:, None]) / pdb_values_np[:, None])
    .mul(100)
    .round(0)
)
annot_labels = absolute_values.mul(100).round(1).astype(str)

# Set the font family to Arial
plt.rcParams["font.family"] = "monospace"

# Plot the heat map using seaborn
plt.figure(figsize=(9, 6))
heatmap = sns.heatmap(
    df_percentage_diff,
    annot=annot_labels,
    center=0,
    fmt="",
    cmap=custom_cmap,
    cbar_kws={"label": "Percentage difference from PDB (%)"},
    annot_kws={"size": 17},
    vmin=-100,
    vmax=200,
)
heatmap.set_title("Design amino acid percentages by year group vs PDB", fontsize=14)
heatmap.set_xlabel("Release year groups vs PDB", fontsize=16)
heatmap.set_ylabel("Amino acids", fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14, rotation=0)

# Set the colorbar label fontsize
cbar = heatmap.collections[0].colorbar
cbar.ax.yaxis.label.set_size(15)
cbar.ax.tick_params(labelsize=14)

# Adjust layout and save the plot
plt.tight_layout()
plt.savefig(
    analysis_path + "aa_proportions_heatmap.png",
    bbox_inches="tight",
    dpi=600,
)
