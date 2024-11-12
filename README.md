# chronowska-stam-wood-2024-protein-design-archive
Code supporting the Protein Design Archive (PDA) database publication

Welcome to the Protein Design Archive (PDA) Database, an up-to-date, complete, online resource for the protein design community and beyond. Here is a description of what can be found in each directory.

# Data preparation
## Improved method of data preparation as of October 2024
_Edit: code for data preparation used for the monthly updates of the PDA has been much improved since October 2024. In view of much interest in this resource and commitment to maintaining it to the highest standard, updates since October 2024 are performed using the improved method, with accurate designed chain selection; and since October 2024 using semi-automated method, reducing chance of inconsistency and errors that could potentially arise_

Data is now collected using the ```main.py``` script, run with flags --next iso_format_date_of_next(current)_update --prev iso_format_date_of_previous_update e.g. --next 20241031 --prev 20240930 for the October 2024 update which includes entries up to 31st October 2024.
This script relies on other scripts found in scripts directory, but should be self explanatory with the comments and cues printed to the command line.

## Data preparation for paper submission
_Below is described the original method used at the time of submission of manuscript "The Protein Design Archive (PDA): insights from 40 years of protein design" (doi: [](https://doi.org/10.1101/2024.09.05.611465)) on 7th September 2024. This method has been improved since them (see section above)._
### Data_collection_and_processing

Data has been scraped from the RCSB PDB database using the Jupyter notebook ```Prepare_PDA_data.ipynb```.

It relies on having a list of PDB codes to scrape data for, cif files to scrape information from, and in-house rules for assigning suggested classification for the protein designs.

This base dataset is supplemented using chain labels from each chain's description in FASTA file and ```Extract_auth_chain_labels.ipynb``` notebook.

To download PDB files for Foldseek and DE-STRESS analysis, run the following commands:

```chmod +x download_pdbs.sh```
```bash download_pdbs.sh -f pdb_codes.csv -o ./output/pdb_files -a```

Analysis of similarity measures relies on checking whether the target that the query has matched with has an earlier release date than the query. To do this, ```all_pdb_release_dates.csv``` file is used, which is prepared with the ```Dates_of_release_of_all_PDB.ipynb``` Jupyter notebook.

The most up-to-date dataset of designed proteins can be found in the file ```20240827_data.json```.

### MMseqs2

Jupyter notebook ```Concatenate_chain_sequences.ipynb``` contains the code used to extract only designed chains from original FASTA files. ```designed_single_sequences_1450.fasta``` is the single designed chains input for analysis. DvD and DvP directories each contain chain and struct directories, to reflect their type of searches (Designs vs Designs, or Designs vs Natural Proteins; per single designed chains or per concatenated designed chains). Each directory contains the script used to run the software analysis (```search_{dvd-or-dvp}.sh```), and .json outputs of the highest scores and highest scoring partners for every design, and every metric. .json analysis outputs were prepared using ```Similarity_analysis.ipynb``` Jupyter notebook, which can be found within MMseqs2 directory, and which also provides the overall similarity analysis and graph plotting.

### Foldseek

Jupyter notebook ```Extract_designed_chains_in_pdb_files.ipynb``` contains the code used to extract only designed chains from original PDB files. DvD and DvP directories each contain chain and struct directories, to reflect their type of searches (Designs vs Designs, or Designs vs Natural Proteins; per single designed chains or per concatenated designed chains). Each directory contains the script used to run the software analysis (```foldseek_search_{dvd-or-dvp}_{single_chain-or-concatenated}.sh```) a python file to analyse the results and extract the highest scoring partner and value for each metric (e.g. ```foldseek_all_metrics_above_threshold.py```), and .json outputs of the highest scores and highest scoring partners for every design, and every metric.

### DE-STRESS

The `de-stress-analysis/` folder contains all the code needed to produce the amino acid/secondary structure composition heatmaps and box plots of the de-stress metrics that are included in figure 4. 

First, create the conda environment and activate it with the command below.

```bash 
conda env create -f de-stress-analysis/environment.yml
conda activate pda_destress_analysis
```

After this download `destress_data_designs_082024.csv`, `destress_data_pdb_082024.csv`, `design_meta_data_20240827.json`, `designed_chains_pdb_files/` and `pdb_all_files_june_2024/` from the supplementary materials and place them in the `de-stress-analysis/data/raw_data/` folder.

Next, run the `de-stress-analysis/data_prep_destress.py` and `de-stress-analysis/data_prep_aa_comp.py` scripts to prepare the data. 

Finally, run the `de-stress-analysis/analysis_destress.py` and `de-stress-analysis/analysis_aa_comp.py` scripts to produce the plots that were used in the paper and these will be saved in the `de-stress-analysis/analysis/` folder.

## Graphs

Code for plotting protein designs' growth curve.
