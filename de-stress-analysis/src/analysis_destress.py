# 0. Importing packages and defining custom functions-------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.font_manager as fm


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

ss_comp_data_path = "de-stress-analysis/data/processed_data/ss_comp.csv"
selected_destress_features_path = (
    "de-stress-analysis/data/processed_data/selected_destress_features.csv"
)

pdb_ss_comp_data_path = "de-stress-analysis/data/processed_data/pdb_ss_comp.csv"
pdb_selected_destress_features_path = (
    "de-stress-analysis/data/processed_data/pdb_selected_destress_features.csv"
)

# List of seccondary structure types
secondary_structure_types = [
    "alpha helix",
    "beta bridge",
    "beta strand",
    "3 10 helix",
    "pi helix",
    "hbonded turn",
    "bend",
    "loop",
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

ss_comp_data = pd.read_csv(ss_comp_data_path)
selected_destress_features = pd.read_csv(selected_destress_features_path)

pdb_ss_comp_data = pd.read_csv(pdb_ss_comp_data_path)
pdb_selected_destress_features = pd.read_csv(pdb_selected_destress_features_path)


# 3. Processing ss_comp_data-------------------------------------------------------

# Define the boundaries for the groups
year_groups = pd.cut(
    ss_comp_data["release_year"], bins=range(1990, 2026, 5), right=False
)

# Assign the year groups to a new column in the DataFrame
ss_comp_data["year_group"] = year_groups

# Apply the function to the year_group column
ss_comp_data["year_group"] = (
    ss_comp_data["year_group"].astype(str).apply(convert_year_group_format)
)

# Add a dummy 'year_group' column
pdb_ss_comp_data["year_group"] = "PDB"

# Group by year and aggregate sum of sequence lengths and amino acid counts
ss_comp_grouped_df = (
    ss_comp_data.groupby("year_group")
    .agg({"num_residues": "sum", **{ss: "sum" for ss in secondary_structure_types}})
    .reset_index()
)

# Group by year and aggregate sum of sequence lengths and amino acid counts
pdb_ss_comp_grouped_df = (
    pdb_ss_comp_data.groupby("year_group")
    .agg({"num_residues": "sum", **{ss: "sum" for ss in secondary_structure_types}})
    .reset_index()
)

# Divide each amino acid count column by sequence length column
for ss in secondary_structure_types:
    ss_comp_grouped_df[ss] = ss_comp_grouped_df[ss] / ss_comp_grouped_df["num_residues"]
    pdb_ss_comp_grouped_df[ss] = (
        pdb_ss_comp_grouped_df[ss] / pdb_ss_comp_grouped_df["num_residues"]
    )

ss_comp_grouped_df = ss_comp_grouped_df[["year_group"] + secondary_structure_types]
pdb_ss_comp_grouped_df = pdb_ss_comp_grouped_df[
    ["year_group"] + secondary_structure_types
]

# 4. Processing selected destress features----------------------------------------------------

# Define the boundaries for the groups
year_groups = pd.cut(
    selected_destress_features["release_year"], bins=range(1990, 2026, 5), right=False
)

# Dropping release year
selected_destress_features.drop(["release_year", "pdb"], axis=1, inplace=True)

# Assign the year groups to a new column in the DataFrame
selected_destress_features["year_group"] = year_groups

# Apply the function to the year_group column
selected_destress_features["year_group"] = (
    selected_destress_features["year_group"]
    .astype(str)
    .apply(convert_year_group_format)
)

# Add a dummy 'year_group' column
pdb_selected_destress_features["year_group"] = "PDB"

# Identify numeric columns
numeric_columns = selected_destress_features.select_dtypes(
    include=[np.number]
).columns.tolist()

# Create aggregation dictionary with 'mean' for each numeric column
agg_dict = {col: "mean" for col in numeric_columns}

# Group by 'year_group' and aggregate using the aggregation dictionary
# selected_destress_features_grouped_df = selected_destress_features.groupby('year_group').agg(agg_dict).reset_index()
# pdb_selected_destress_features_grouped_df = pdb_selected_destress_features.groupby('year_group').agg(agg_dict).reset_index()

# 5. Joining data sets------------------------------------------------------------------------

# Joining designs and PDB
ss_comp_grouped_df = pd.concat(
    [ss_comp_grouped_df, pdb_ss_comp_grouped_df], axis=0
).reset_index(drop=True)
selected_destress_features_grouped_df = pd.concat(
    [
        selected_destress_features[["year_group"] + numeric_columns],
        pdb_selected_destress_features[["year_group"] + numeric_columns],
    ],
    axis=0,
).reset_index(drop=True)

# Ensure 'year_group' is a categorical type with the desired order
ss_comp_grouped_df["year_group"] = pd.Categorical(
    ss_comp_grouped_df["year_group"], categories=year_groups_order, ordered=True
)
selected_destress_features_grouped_df["year_group"] = pd.Categorical(
    selected_destress_features_grouped_df["year_group"],
    categories=year_groups_order,
    ordered=True,
)

# Sort the DataFrame by 'year_group' to enforce the order
ss_comp_grouped_df = ss_comp_grouped_df.sort_values("year_group")
selected_destress_features_grouped_df = (
    selected_destress_features_grouped_df.sort_values("year_group")
)


# 6. Plotting ---------------------------------------------------------------------------------

# Setting theme for plots
sns.set_style("whitegrid")

# Set the font family to Arial
plt.rcParams["font.family"] = "monospace"

# Create a colormap object
color_palette = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
    "#17becf",
    "#aec7e8",
    "#ffbb78",
    "#98df8a",
    "#ff9896",
    "#c5b0d5",
    "#c49c94",
    "#f7b6d2",
    "#c7c7c7",
    "#dbdb8d",
    "#9edae5",
    "#f0d6d6",
]
custom_cmap = plt.cm.colors.ListedColormap(color_palette)

# Sorting the amino acid residues by the highest proportions
pdb_row = ss_comp_grouped_df[ss_comp_grouped_df["year_group"] == "PDB"].iloc[0]
sorted_columns = pdb_row.drop("year_group").sort_values(ascending=False).index.tolist()
ss_comp_grouped_df = ss_comp_grouped_df[["year_group"] + sorted_columns]

ss_comp_grouped_df = ss_comp_grouped_df[ss_comp_grouped_df["year_group"] != "90-95"]

ss_comp_grouped_df.to_csv(analysis_path + "ss_proportions_by_year.csv", index=False)

# Convert IntervalIndex to strings
selected_destress_features_grouped_df["year_group"] = (
    selected_destress_features_grouped_df["year_group"].astype(str)
)

columns = [
    "mass",
    "isoelectric_point",
    "charge",
    "num_residues",
    "hydrophobic_fitness",
    "evoef2_total",
    "packing_density",
    "aggrescan3d_avg_value",
    "rosetta_total",
]
titles = [
    "Comparison by mass (Da)",
    "Isoelectric Point",
    "Charge",
    "Number of Residues",
    "Hydrophobic Fitness (Per Residue)",
    "EvoEF2 Total Score (Per Residue)",
    "Comparison by packing quality",
    "Aggrescan3D Average Value",
    "Rosetta Total Score (Per Residue)",
]

selected_destress_features_grouped_df = selected_destress_features_grouped_df[
    selected_destress_features_grouped_df["year_group"] != "90-95"
]

# Loop over the columns to create individual plots
for i in range(len(columns)):
    col = columns[i]

    # Setting theme for plots
    sns.set_style("whitegrid")

    # Set the font family to Arial
    plt.rcParams["font.family"] = "monospace"
    plt.figure(figsize=(8, 6))  # Create a new figure for each plot

    # Use seaborn to create the box plot
    ax = sns.boxplot(
        data=selected_destress_features_grouped_df,
        x="year_group",
        hue="year_group",
        y=col,
        palette="Set2",
    )
    ax.xaxis.grid(True)
    if col == "mass":
        ax.set_yscale("log")
    elif col in ["rosetta_total", "evoef2_total"]:
        ax.set_yscale("symlog", linthresh=0.1)

    # Highlight the PDB bar
    for patch, label in zip(
        ax.artists, selected_destress_features_grouped_df["year_group"].unique()
    ):
        if label == "PDB":
            patch.set_facecolor("red")

    # Customize the plot
    plt.ylabel(titles[i], fontsize=15)
    plt.xlabel("Release year groups vs PDB", fontsize=17)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.title(titles[i], fontsize=17)
    plt.tight_layout()

    # Save the plot
    plt.savefig(
        f"{analysis_path}/destress_features_by_year_{col}.png",
        bbox_inches="tight",
        dpi=600,
    )
    plt.close()  # Close the figure to avoid overlap


# Define the custom colormap
colors = ["blue", "white", "red"]
n_bins = 100  # Number of bins
custom_cmap = LinearSegmentedColormap.from_list(
    "custom_blue_white_red", colors, N=n_bins
)


ss_comp_grouped_df_heatmap = ss_comp_grouped_df

# Setting the 'Year Group' as the index
ss_comp_grouped_df_heatmap.set_index("year_group", inplace=True)

# Transposing data
ss_comp_grouped_df_heatmap = ss_comp_grouped_df_heatmap.transpose()

# Calculate percentage differences from PDB and absolute percentages
pdb_values = ss_comp_grouped_df_heatmap["PDB"]
pdb_values_np = np.array(pdb_values)
absolute_values = ss_comp_grouped_df_heatmap
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
    fmt="",
    cmap=custom_cmap,
    center=0,
    cbar_kws={"label": "Percentage difference from PDB (%)"},
    annot_kws={"size": 17},
    vmin=-100,
    vmax=200,
)
heatmap.set_title(
    "Design secondary structure percentages by year group vs PDB", fontsize=14
)
heatmap.set_xlabel("Release year groups vs PDB", fontsize=16)
heatmap.set_ylabel("Secondary structure type", fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# Set the colorbar label fontsize
cbar = heatmap.collections[0].colorbar
cbar.ax.yaxis.label.set_size(15)
cbar.ax.tick_params(labelsize=14)

# Adjust layout and save the plot
plt.tight_layout()
plt.savefig(
    analysis_path + "ss_proportions_all_pdb_files_heatmap.png",
    bbox_inches="tight",
    dpi=600,
)
