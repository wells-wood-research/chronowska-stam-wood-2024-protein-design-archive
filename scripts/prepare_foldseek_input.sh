#!/bin/bash

# Define the update date
next_date="$1"

# Define the types of analysis
analysis_type=("DvD" "DvP")

# Start a persistent SSH connection
ssh -Nf mchrnwsk@glycine.bio.ed.ac.uk

# Loop through each analysis type and create the necessary directories and copy files
for type in "${analysis_type[@]}"; do

    mkdir -p /home/mchrnwsk/pda-destress-analysis/similarity/foldseek/$next_date/$type/
    # Ensure the destination directories exist
    ssh mchrnwsk@glycine.bio.ed.ac.uk "mkdir -p /home/mchrnwsk/pda/foldseek/$next_date/$type/analysis/"
    ssh mchrnwsk@glycine.bio.ed.ac.uk "mkdir -p /home/mchrnwsk/pda/foldseek/$next_date/$type/data/"
    ssh mchrnwsk@glycine.bio.ed.ac.uk "mkdir -p /home/mchrnwsk/pda/foldseek/$next_date/$type/output/"
    # Copy pdb_files_chains directory
    scp -r /home/mchrnwsk/pda-destress-analysis/data/pdb_files_chains \
        mchrnwsk@glycine.bio.ed.ac.uk:/home/mchrnwsk/pda/foldseek/"$next_date"/"$type"

    # Copy data.json to analysis directory
    scp -r /home/mchrnwsk/pda-destress-analysis/data/"$next_date"_data_scraped.json \
        mchrnwsk@glycine.bio.ed.ac.uk:/home/mchrnwsk/pda/foldseek/"$next_date"/"$type"/analysis

    # Copy all_pdb_release_dates.csv to analysis directory
    scp -r /home/mchrnwsk/pda-destress-analysis/data/all_pdb_release_dates.csv \
        mchrnwsk@glycine.bio.ed.ac.uk:/home/mchrnwsk/pda/foldseek/"$next_date"/"$type"/analysis

done

# Copy analysis script to analysis directory
scp -r /home/mchrnwsk/pda-destress-analysis/similarity_analysis_foldseek.py \
    mchrnwsk@glycine.bio.ed.ac.uk:/home/mchrnwsk/pda/foldseek/"$next_date"

# Copy Foldseek scripts
scp -r /home/mchrnwsk/chronowska-stam-wood-2024-protein-design-archive/Foldseek/foldseek_search_dvd.sh \
    mchrnwsk@glycine.bio.ed.ac.uk:/home/mchrnwsk/pda/foldseek/"$next_date"/DvD

scp -r /home/mchrnwsk/chronowska-stam-wood-2024-protein-design-archive/Foldseek/foldseek_search_dvp.sh \
    mchrnwsk@glycine.bio.ed.ac.uk:/home/mchrnwsk/pda/foldseek/"$next_date"/DvP
