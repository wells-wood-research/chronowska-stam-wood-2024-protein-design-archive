#!/bin/bash

# Define the update date
next_date="$1"

# Define the types of analysis
analysis_type=("DvD" "DvP")

# Start a persistent SSH connection
ssh -Nf mchrnwsk@glycine.bio.ed.ac.uk

# Create temporary directory on remote server
ssh mchrnwsk@glycine.bio.ed.ac.uk "mkdir -p /home/mchrnwsk/pda/foldseek/$next_date/tmp"

# Copy all files to temporary directory at once
scp -r /home/mchrnwsk/pda-destress-analysis/data/pdb_files_chains \
       /home/mchrnwsk/pda-destress-analysis/data/"${next_date}"_data_scraped.json \
       /home/mchrnwsk/pda-destress-analysis/data/all_pdb_release_dates.csv \
       /home/mchrnwsk/pda-destress-analysis/similarity_analysis_foldseek.py \
       /home/mchrnwsk/chronowska-stam-wood-2024-protein-design-archive/Foldseek/foldseek_search_dvd.sh \
       /home/mchrnwsk/chronowska-stam-wood-2024-protein-design-archive/Foldseek/foldseek_search_dvp.sh \
       mchrnwsk@glycine.bio.ed.ac.uk:/home/mchrnwsk/pda/foldseek/"$next_date"/tmp

# Loop through each analysis type and create directories, then copy from temp
for type in "${analysis_type[@]}"; do
    # Create local directory
    mkdir -p /home/mchrnwsk/pda-destress-analysis/similarity/foldseek/$next_date/$type/
    
    # Create remote directories and copy files from temp
    ssh mchrnwsk@glycine.bio.ed.ac.uk "
        mkdir -p /home/mchrnwsk/pda/foldseek/$next_date/$type/{analysis,data,output} &&
        cp -r /home/mchrnwsk/pda/foldseek/$next_date/tmp/pdb_files_chains \
              /home/mchrnwsk/pda/foldseek/$next_date/$type/ &&
        cp /home/mchrnwsk/pda/foldseek/$next_date/tmp/${next_date}_data_scraped.json \
           /home/mchrnwsk/pda/foldseek/$next_date/tmp/all_pdb_release_dates.csv \
           /home/mchrnwsk/pda/foldseek/$next_date/$type/analysis/ &&
        cp /home/mchrnwsk/pda/foldseek/$next_date/tmp/similarity_analysis_foldseek.py \
           /home/mchrnwsk/pda/foldseek/$next_date/ &&
        cp /home/mchrnwsk/pda/foldseek/$next_date/tmp/foldseek_search_${type,,}.sh \
           /home/mchrnwsk/pda/foldseek/$next_date/$type/
    "
done

# Clean up temporary directory
ssh mchrnwsk@glycine.bio.ed.ac.uk "rm -rf /home/mchrnwsk/pda/foldseek/$next_date/tmp"