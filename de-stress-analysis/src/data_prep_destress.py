# 0. Importing packages-------------------------------------------
import json
import pandas as pd

# from data_prep_tools import *

# 1. Defining variables-------------------------------------------

# Defining a file path for design_data
design_data_path = "de-stress-analysis/data/raw_data/design_meta_data_20240827.json"

# Defining the file path for the DE-STRESS data
destress_data_path = "de-stress-analysis/data/raw_data/destress_data_designs_082024.csv"

# Defining the file path for the PDB DE-STRESS data
pdb_destress_data_path = "de-stress-analysis/data/raw_data/destress_data_pdb_082024.csv"

# Defining a path for the processed data
processed_data_path = "de-stress-analysis/data/processed_data/"

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

# 2. Reading in data----------------------------------------------

# Reading in design data
design_data = pd.read_json(design_data_path)

# Reading in DE-STRESS data
destress_data = pd.read_csv(destress_data_path)

# Reading in PDB DE-STRESS data
pdb_destress_data = pd.read_csv(pdb_destress_data_path)

# Adding new fields
design_data["release_date"] = pd.to_datetime(design_data["release_date"])
design_data["release_year"] = design_data["release_date"].dt.year
design_data["pdb"] = design_data["pdb"].str.lower()

# 3. Extracting amino acid and secondary atructure composition from DE-STRESS data---------------------------

# Dropping some features because they have loads of missing values
destress_data.drop(
    [
        "budeff_total",
        "budeff_steric",
        "budeff_desolvation",
        "budeff_charge",
        "dfire2_total",
    ],
    inplace=True,
    axis=1,
)
pdb_destress_data.drop(
    [
        "budeff_total",
        "budeff_steric",
        "budeff_desolvation",
        "budeff_charge",
        "dfire2_total",
    ],
    inplace=True,
    axis=1,
)

# Merging design data data sets
design_destress_data = pd.merge(
    destress_data,
    design_data[["pdb", "release_year"]],
    left_on="design_name",
    right_on="pdb",
    how="left",
)

# Dropping rows that have any NAs
design_destress_data = design_destress_data.dropna(axis=0).reset_index(drop=True)
pdb_destress_data = pdb_destress_data.dropna(axis=0).reset_index(drop=True)

# Defining the column
column_to_multiply = "num_residues"

# Selecting every other column to multiply
columns_to_multiply = list(design_destress_data.filter(regex="composition")) + list(
    design_destress_data.filter(regex="ss_prop")
)

# Multiplying selected columns by the specified column
design_destress_data[columns_to_multiply] = design_destress_data[
    columns_to_multiply
].mul(design_destress_data[column_to_multiply], axis=0)
pdb_destress_data[columns_to_multiply] = pdb_destress_data[columns_to_multiply].mul(
    pdb_destress_data[column_to_multiply], axis=0
)


# Processing data to be similar to the design data
for col in list(design_destress_data.filter(regex="ss_prop")):
    design_destress_data.rename(
        columns={col: col.split("ss_prop_")[1].replace("_", " ")}, inplace=True
    )
    pdb_destress_data.rename(
        columns={col: col.split("ss_prop_")[1].replace("_", " ")}, inplace=True
    )


# Extracting ss composition
ss_comp_df = design_destress_data[
    ["design_name", "release_year", "num_residues"] + secondary_structure_types
]
pdb_ss_comp_df = pdb_destress_data[
    ["design_name", "num_residues"] + secondary_structure_types
]
ss_comp_df.to_csv(processed_data_path + "ss_comp.csv", index=False)
pdb_ss_comp_df.to_csv(processed_data_path + "pdb_ss_comp.csv", index=False)

# Extracting other de-stress metrics
selected_features_df = design_destress_data.drop(secondary_structure_types, axis=1)
pdb_selected_features_df = pdb_destress_data.drop(secondary_structure_types, axis=1)
for col in ["evoef2_total", "rosetta_total", "hydrophobic_fitness"]:
    selected_features_df[col] = (
        selected_features_df[col] / selected_features_df["num_residues"]
    )
    pdb_selected_features_df[col] = (
        pdb_selected_features_df[col] / pdb_selected_features_df["num_residues"]
    )

selected_features_df.to_csv(
    processed_data_path + "selected_destress_features.csv", index=False
)
pdb_selected_features_df.to_csv(
    processed_data_path + "pdb_selected_destress_features.csv", index=False
)
