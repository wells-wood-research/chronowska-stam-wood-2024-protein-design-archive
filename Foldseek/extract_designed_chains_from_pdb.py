import re
import pandas as pd
from pdbUtils import pdbUtils
import os

data = pd.read_json("/home/mchrnwsk/pda-destress-analysis/data/20240930_data_curated.json")
base_dir = "/home/mchrnwsk/pda-destress-analysis/data/pdb_files"
chain_dir = base_dir+"_chains"

standard_amino_acids = {
    "ALA": "A",
    "CYS": "C",
    "ASP": "D",
    "GLU": "E",
    "PHE": "F",
    "GLY": "G",
    "HIS": "H",
    "ILE": "I",
    "LYS": "K",
    "LEU": "L",
    "MET": "M",
    "ASN": "N",
    "PRO": "P",
    "GLN": "Q",
    "ARG": "R",
    "SER": "S",
    "THR": "T",
    "VAL": "V",
    "TRP": "W",
    "TYR": "Y",
}

def extract_designed_chains(pdb_file):

    # Open the PDB file
    with open(pdb_file, 'r') as file:
        lines = file.readlines()

    species = {}
    molecule_counter = 0
    chain_not_finished = False

    # Parse through the file
    for line in lines:
        # Check for COMPND lines
        if line.startswith("COMPND"):

            # Find the MOL_ID
            if chain_not_finished:
                chain_match = re.search(r"COMPND\s*\d*(s*[A-Za-z\d, ]+)", line)
                if chain_match:
                    if re.search(r"COMPND\s*\d*(s*[A-Za-z\d, ]+);", line):
                        chain_not_finished = False
                        species[molecule_counter]["chains"] += " " + chain_match.group(1).strip()
                        continue
                    else:
                        species[molecule_counter]["chains"] += " " + chain_match.group(1).strip()
                        continue

                species[molecule_counter]["chains"] += (chain_match.group(1).strip())
                if line.endswith(";"):
                    chain_not_finished = False
                continue

            mol_id_match = re.search(r"MOL_ID:\s*(\d+);", line)
            if mol_id_match:
                molecule_counter = mol_id_match.group(1)
                species[molecule_counter] = {"chains":"", "source":""}
                continue

            chain_match = re.search(r"CHAIN:\s*([A-Za-z\d, ]+)", line)
            if chain_match:
                if re.search(r"CHAIN:\s*([A-Za-z\d, ]+);", line):
                    species[molecule_counter]["chains"] = chain_match.group(1).strip()
                    continue
                else:
                    chain_not_finished = True
                    species[molecule_counter]["chains"] = chain_match.group(1).strip()
                    continue

        # Check for SOURCE lines
        elif line.startswith("SOURCE"):
            mol_id_match = re.search(r"MOL_ID:\s*(\d+);", line)
            if mol_id_match:
                molecule_counter = mol_id_match.group(1)
                continue

            # Find ORGANISM_TAXID
            taxid_match = re.search(r"ORGANISM_TAXID:\s*(\d+)", line)
            if taxid_match:
                if taxid_match.group(1) == "32630":
                    species[molecule_counter]["source"] = "designed"
                    continue
                else:
                    species[molecule_counter]["source"] = "natural"
                    continue
        
        if line.startswith("KEYWDS"):
            break

    return species

def set_chains_manually(pdb, designed_chains):
    pdb_file_assembly = base_dir+"/"+pdb.lower() + ".pdb1"
    df = pdbUtils.pdb2df(pdb_file_assembly)
    designed_chains_only_df = pd.DataFrame(columns = df.columns)
    
    for chain_label in designed_chains:
        outfile = chain_dir+"/"+pdb+"_"+chain_label+".pdb"
        
        try:
            designed_chains_only_df = df[df["CHAIN_ID"] == chain_label]
            pdbUtils.df2pdb(designed_chains_only_df, outfile)
        except Exception as e:
            if not set(designed_chains).intersection(df["CHAIN_ID"].unique().tolist()):
                print(pdb, " exception", e)
                print("All chain labels in PDB: ", df["CHAIN_ID"].unique().tolist())
                print("All designed chain labels: ", designed_chains)
                print("\n")

for i, row in data.iterrows():
    pdb = row["pdb"]

    if pdb == "1mey":
        set_chains_manually(pdb, ["C", "F", "G"])
        continue
    elif pdb == "2lq4":
        set_chains_manually(pdb, ["p"])
        continue
    elif pdb == "8ub3":
        set_chains_manually(pdb, ["A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "Q", "U", "c", "k", "s", "w", "4", "Z"])
        continue
    else:
        try:
            pdb_file_assembly = base_dir+"/"+pdb.lower() + ".pdb1"
            pdb_file = base_dir+"/"+pdb.lower() + ".pdb"
            current_pdb_chain_sources = extract_designed_chains(pdb_file)
            df = pdbUtils.pdb2df(pdb_file_assembly)
        except:
            print(pdb + " file not found.")
            continue
        
        designed_chains = []
        for key in current_pdb_chain_sources:
            if current_pdb_chain_sources[key]["source"] == "designed" or not current_pdb_chain_sources[key]["source"]:
                designed_chains += current_pdb_chain_sources[key]["chains"].split(", ")

        designed_chains_only_df = pd.DataFrame(columns = df.columns)
        
        for chain_label in designed_chains:
            outfile = chain_dir+"/"+pdb+"_"+chain_label+".pdb"
            try:
                designed_chains_only_df = df[df["CHAIN_ID"] == chain_label]
                pdbUtils.df2pdb(designed_chains_only_df, outfile)
            except Exception as e:
                if not set(designed_chains).intersection(df["CHAIN_ID"].unique().tolist()):
                    print(pdb, " exception", e)
                    print("All chain labels in PDB: ", df["CHAIN_ID"].unique().tolist())
                    print("All designed chain labels: ", designed_chains)
                    print("\n")