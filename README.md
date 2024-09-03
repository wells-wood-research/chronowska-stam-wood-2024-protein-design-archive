# chronowska-stam-wood-2024-protein-design-archive
Code supporting the Protein Design Archive (PDA) database publication

Welcome to the Protein Design Archive (PDA) Database, an up-to-date, complete, online resource for the protein design community and beyond. Here is a description of what can be found in each directory.

## Data_collection_and_processing

Data has been scraped from the RCSB PDB database using the Jupyter notebook ```Prepare_PDA_data.ipynb```.

It relies on having a list of PDB codes to scrape data for, cif files to scrape information from, and in-house rules for assigning suggested classification for the protein designs.

This base dataset is supplemented using chain labels from each chain's description in FASTA file and ```Extract_auth_chain_labels.ipynb``` notebook.

To download PDB files for Foldseek and DE-STRESS analysis, run the following commands:

```chmod +x download_pdbs.sh```
```bash download_pdbs.sh -f pdb_codes.csv -o ./output/pdb_files -a```

Analysis of similarity measures relies on checking whether the target that the query has matched with has an earlier release date than the query. To do this, ```all_pdb_release_dates.csv``` file is used, which is prepared with the ```Dates_of_release_of_all_PDB.ipynb``` Jupyter notebook.

The most up-to-date dataset of designed proteins can be found in the file ```20240827_data.json```.

## MMseqs2

Jupyter notebook ```Concatenate_chain_sequences.ipynb``` contains the code used to extract only designed chains from original FASTA files. ```designed_single_sequences_1450.fasta``` is the single designed chains input for analysis. DvD and DvP directories each contain chain and struct directories, to reflect their type of searches (Designs vs Designs, or Designs vs Natural Proteins; per single designed chains or per concatenated designed chains). Each directory contains the script used to run the software analysis (```search_{dvd-or-dvp}.sh```), and .json outputs of the highest scores and highest scoring partners for every design, and every metric. .json analysis outputs were prepared using ```Similarity_analysis.ipynb``` Jupyter notebook, which can be found within MMseqs2 directory, and which also provides the overall similarity analysis and graph plotting.

## Foldseek

Jupyter notebook ```Extract_designed_chains_in_pdb_files.ipynb``` contains the code used to extract only designed chains from original PDB files. DvD and DvP directories each contain chain and struct directories, to reflect their type of searches (Designs vs Designs, or Designs vs Natural Proteins; per single designed chains or per concatenated designed chains). Each directory contains the script used to run the software analysis (```foldseek_search_{dvd-or-dvp}_{single_chain-or-concatenated}.sh```) a python file to analyse the results and extract the highest scoring partner and value for each metric (e.g. ```foldseek_all_metrics_above_threshold.py```), and .json outputs of the highest scores and highest scoring partners for every design, and every metric.

## DE-STRESS

## Graphs

Code for plotting protein designs' growth curve.
