#!/bin/bash

# Define the update date
next_date="$1"

# Define the types of analysis
analysis_type=("DvD" "DvP")

# Start a persistent SSH connection
ssh -Nf mchrnwsk@cysteine.bio.ed.ac.uk

# Loop through each analysis type and create the necessary directories and copy files
for type in "${analysis_type[@]}"; do

    # Remove large unnecessary files
    ssh mchrnwsk@cysteine.bio.ed.ac.uk "rm -r /home/mchrnwsk/pda/foldseek/$next_date/$type/pdb_files_chains/"
#    ssh mchrnwsk@cysteine.bio.ed.ac.uk "rm -r /home/mchrnwsk/pda/foldseek/$next_date/$type/output"
    ssh mchrnwsk@cysteine.bio.ed.ac.uk "rm -r /home/mchrnwsk/pda/foldseek/$next_date/$type/data"

    scp -r mchrnwsk@cysteine.bio.ed.ac.uk:/home/mchrnwsk/pda/foldseek/$next_date/"$type"_max_related_structure_lddt_95.json /home/mchrnwsk/pda-destress-analysis/similarity/foldseek/$next_date

    scp -r mchrnwsk@cysteine.bio.ed.ac.uk:/home/mchrnwsk/pda/foldseek/$next_date/"$type"_thr_related_structure_lddt_95.json /home/mchrnwsk/pda-destress-analysis/similarity/foldseek/$next_date

done