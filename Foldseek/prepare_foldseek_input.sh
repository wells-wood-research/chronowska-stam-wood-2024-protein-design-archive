#!/bin/bash

# Define the update date
update_date="20240930"

# Define the types of analysis
analysis_type=("DvD" "DvP")

# Start a persistent SSH connection
ssh -Nf mchrnwsk@cysteine.bio.ed.ac.uk

# Loop through each analysis type and create the necessary directories and copy files
for type in "${analysis_type[@]}"; do

    mkdir -p /home/mchrnwsk/pda-destress-analysis/similarity/foldseek/$update_date/$type/

    # Ensure the destination directories exist
    ssh mchrnwsk@cysteine.bio.ed.ac.uk "mkdir -p /home/mchrnwsk/pda/foldseek/$update_date/$type/analysis/"
    ssh mchrnwsk@cysteine.bio.ed.ac.uk "mkdir -p /home/mchrnwsk/pda/foldseek/$update_date/$type/data/"
    ssh mchrnwsk@cysteine.bio.ed.ac.uk "mkdir -p /home/mchrnwsk/pda/foldseek/$update_date/$type/output/"

    # Copy pdb_files_chains directory
    scp -r /home/mchrnwsk/pda-destress-analysis/data/pdb_files_chains \
        mchrnwsk@cysteine.bio.ed.ac.uk:/home/mchrnwsk/pda/foldseek/"$update_date"/"$type"

    # Copy data.json to analysis directory
    scp -r /home/mchrnwsk/pda-destress-analysis/data/"$update_date"_data.json \
        mchrnwsk@cysteine.bio.ed.ac.uk:/home/mchrnwsk/pda/foldseek/"$update_date"/"$type"/analysis

    # Copy all_pdb_release_dates.csv to analysis directory
    scp -r /home/mchrnwsk/pda-destress-analysis/data/all_pdb_release_dates.csv \
        mchrnwsk@cysteine.bio.ed.ac.uk:/home/mchrnwsk/pda/foldseek/"$update_date"/"$type"/analysis
done

scp -r /home/mchrnwsk/chronowska-stam-wood-2024-protein-design-archive/Foldseek/foldseek_search_dvd.sh \
    mchrnwsk@cysteine.bio.ed.ac.uk:/home/mchrnwsk/pda/foldseek/"$update_date"/DvD

# Copy foldseek_search_dvp.sh to the appropriate type directory
scp -r /home/mchrnwsk/chronowska-stam-wood-2024-protein-design-archive/Foldseek/foldseek_search_dvp.sh \
    mchrnwsk@cysteine.bio.ed.ac.uk:/home/mchrnwsk/pda/foldseek/"$update_date"/DvP