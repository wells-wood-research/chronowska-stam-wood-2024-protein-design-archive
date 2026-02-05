#!/bin/bash

# Default values
next_date=""
all_mode=false

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --all) all_mode=true ;;
        *) next_date="$1" ;; # Assume any non-flag argument is the date
    esac
    shift
done

# Check if date was provided
if [ -z "$next_date" ]; then
    echo "Error: next_date is required."
    exit 1
fi

# Determine which file to copy based on the flag
if [ "$all_mode" = true ]; then
    EXTENSION="_pdb_codes_total.txt"
else
    EXTENSION="_pdb_codes_new_download.txt"
fi

# Define the types of analysis
analysis_type=("DvD" "DvP")

# Start a persistent SSH connection
ssh -Nf mchrnwsk@cysteine.bio.ed.ac.uk

# Create temporary directory on remote server
ssh mchrnwsk@cysteine.bio.ed.ac.uk "mkdir -p /home/mchrnwsk/pda/foldseek/$next_date/tmp"

# Copy all files to temporary directory at once

scp -r \
       /home/mchrnwsk/pda-destress-analysis/data/"${next_date}"_data_scraped.json \
       /home/mchrnwsk/pda-destress-analysis/data/pdb_files \
       /home/mchrnwsk/pda-destress-analysis/data/all_pdb_release_dates.csv \
       /home/mchrnwsk/pda-destress-analysis/similarity_analysis_foldseek.py \
       /home/mchrnwsk/chronowska-stam-wood-2024-protein-design-archive/Foldseek/foldseek_search_dvd.sh \
       /home/mchrnwsk/chronowska-stam-wood-2024-protein-design-archive/Foldseek/foldseek_search_dvp.sh \
       /home/mchrnwsk/pda-destress-analysis/extract_designed_chains_from_pdb.py \
       /home/mchrnwsk/pda-destress-analysis/data/${next_date}_${EXTENSION} \
       mchrnwsk@cysteine.bio.ed.ac.uk:/home/mchrnwsk/pda/foldseek/"$next_date"/tmp

# Loop through each analysis type and create directories, then copy from temp
for type in "${analysis_type[@]}"; do
    # Create local directory
    mkdir -p /home/mchrnwsk/pda-destress-analysis/similarity/foldseek/$next_date/$type/
    
    # Create remote directories and copy files from temp
    ssh mchrnwsk@cysteine.bio.ed.ac.uk "
        mkdir -p /home/mchrnwsk/pda/foldseek/$next_date/pdb_files_chains &&
        cp -r /home/mchrnwsk/pda/foldseek/$next_date/tmp/pdb_files/ \
            /home/mchrnwsk/pda/foldseek/$next_date/ &&
        cp /home/mchrnwsk/pda/foldseek/$next_date/tmp/extract_designed_chains_from_pdb.py \
            /home/mchrnwsk/pda/foldseek/$next_date/extract_designed_chains_from_pdb.py &&
        cp /home/mchrnwsk/pda/foldseek/$next_date/tmp/"$next_date""$EXTENSION" /home/mchrnwsk/pda/foldseek/$next_date/pdb_codes.txt &&
        mkdir -p /home/mchrnwsk/pda/foldseek/$next_date/$type/{analysis,data,output} &&
        cp /home/mchrnwsk/pda/foldseek/$next_date/tmp/${next_date}_data_scraped.json \
           /home/mchrnwsk/pda/foldseek/$next_date/tmp/all_pdb_release_dates.csv \
           /home/mchrnwsk/pda/foldseek/$next_date/$type/analysis/ &&
        cp /home/mchrnwsk/pda/foldseek/$next_date/tmp/similarity_analysis_foldseek.py \
            cp /home/mchrnwsk/pda/foldseek/$next_date/tmp/${next_date}_data_scraped.json \
           /home/mchrnwsk/pda/foldseek/$next_date/ &&
        cp /home/mchrnwsk/pda/foldseek/$next_date/tmp/foldseek_search_${type,,}.sh \
           /home/mchrnwsk/pda/foldseek/$next_date/$type/
    "
done

# Clean up temporary directory
ssh mchrnwsk@cysteine.bio.ed.ac.uk "rm -rf /home/mchrnwsk/pda/foldseek/$next_date/tmp"