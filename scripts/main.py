import os
import subprocess
import sys
from datetime import datetime
import argparse

# Run in /home/mchrnwsk/pda-destress-analysis directory

# Run in "jupyter" environment; packages required:
# pandas
# numpy
# Bio
# pdbUtils
# nltk
# BeautifulSoup

def run_command(command, description):
    print(f"Starting: {description}")
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, check=True)
    print(f"Completed: {description}\n")
    return result

def wait_for_user(prompt):
    input(f"{prompt} \nPress ENTER to continue...")

def main(next_date, prev_date, all_option=False):
    # Step 1: Review designs. Create file in official github repo for tracking home/mchrnwsk/chronowska-stam-wood-2024-protein-design-archive/data/{next_date}_pdb_codes.csv with new entries.
    run_command(
            f"nano /home/mchrnwsk/chronowska-stam-wood-2024-protein-design-archive/data/{next_date}_pdb_codes.csv" ,
            f"Create empty file to save {next_date}_pdb_codes.csv to"
        )
    wait_for_user(f"Add reviewed designs to add in the {next_date} update to /home/mchrnwsk/chronowska-stam-wood-2024-protein-design-archive/data/{next_date}_pdb_codes.csv")
    wait_for_user(f"Add codes to exclude in the {next_date} update to /home/mchrnwsk/chronowska-stam-wood-2024-protein-design-archive/entries_to_manually_exclude.csv")

    # Step 2: Create /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes.txt with entries not found in exclude, and found in manually include
    if all_option:
        run_command(
            f"nano /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes_total.txt" ,
            f"Create empty file to save {next_date}_pdb_codes_total.txt to"
        )
        ## Print codes to add: new codes, excluding ones to exclude
        run_command(
            f"python print_pdb_codes_string.py --file ../chronowska-stam-wood-2024-protein-design-archive/data/{next_date}_pdb_codes.csv --exclude ../chronowska-stam-wood-2024-protein-design-archive/entries_to_manually_exclude.csv --uppercase" ,
            "Running print_pdb_codes_string.py with new_pdb_codes - entries_to_manually_exclude"
        ) 
        ## Print codes to add: those to manually include, which haven't been added in previous update
        run_command(
            f"python print_pdb_codes_string.py --file ../chronowska-stam-wood-2024-protein-design-archive/entries_to_manually_include.csv --exclude data/{prev_date}_data_curated.json --uppercase" ,
            "Running print_pdb_codes_string.py with entries_to_manually_include - old_pdb_codes"
        )
        ## Print codes to add: those from previous update, excluding ones to exclude
        run_command(
            f"python print_pdb_codes_string.py --file data/{prev_date}_data_curated.json --exclude ../chronowska-stam-wood-2024-protein-design-archive/entries_to_manually_exclude.csv --uppercase" ,
            "Running print_pdb_codes_string.py with old_pdb_codes - entries_to_manually_exclude"
        )
        wait_for_user(f"Add the above printed codes to /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes_total.txt")
    else:
        run_command(
            f"nano /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes_new_download.txt" ,
            f"Create empty file to save {next_date}_pdb_codes_new_download.txt to"
        )
        ## Print codes to add: new codes, excluding ones to exclude
        run_command(
            f"python print_pdb_codes_string.py --file ../chronowska-stam-wood-2024-protein-design-archive/data/{next_date}_pdb_codes.csv --exclude ../chronowska-stam-wood-2024-protein-design-archive/entries_to_manually_exclude.csv --uppercase" ,
            "Running print_pdb_codes_string.py with new_pdb_codes - entries_to_manually_exclude"
        ) 
        ## Print codes to add: those to manually include, which haven't been added in previous update
        run_command(
            f"python print_pdb_codes_string.py --file ../chronowska-stam-wood-2024-protein-design-archive/entries_to_manually_include.csv --exclude data/{prev_date}_data_curated.json --uppercase" ,
            "Running print_pdb_codes_string.py with entries_to_manually_include - old_pdb_codes"
        )
        wait_for_user(f"Add the above printed codes to /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes_new_download.txt")

    # Step 3: Download CIF files
    os.makedirs("/home/mchrnwsk/pda-destress-analysis/data/cif_files", exist_ok=True)
    if all_option:
        run_command(
            f"bash /home/mchrnwsk/pda-destress-analysis/data/download_pdbs.sh -f /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes_total.txt -o /home/mchrnwsk/pda-destress-analysis/data/cif_files -c",
            "Downloading CIF files"
        )
    else:
        run_command(
            f"bash /home/mchrnwsk/pda-destress-analysis/data/download_pdbs.sh -f /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes_new_download.txt -o /home/mchrnwsk/pda-destress-analysis/data/cif_files -c",
            "Downloading CIF files"
        )

    # Step 4: Download PDB files, .pdb and .pdb1
    os.makedirs("/home/mchrnwsk/pda-destress-analysis/data/pdb_files", exist_ok=True)
    if all_option:
        run_command(
            f"bash data/download_pdbs.sh -f /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes_total.txt -o /home/mchrnwsk/pda-destress-analysis/data/pdb_files -p",
            "Downloading PDB files"
        )
        run_command(
            f"bash data/download_pdbs.sh -f /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes_total.txt -o /home/mchrnwsk/pda-destress-analysis/data/pdb_files -a",
            "Downloading PDB files"
        )
    else:
        run_command(
            f"bash data/download_pdbs.sh -f /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes_new_download.txt -o /home/mchrnwsk/pda-destress-analysis/data/pdb_files -p",
            "Downloading PDB files"
        )
        run_command(
            f"bash data/download_pdbs.sh -f /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes_new_download.txt -o /home/mchrnwsk/pda-destress-analysis/data/pdb_files -a",
            "Downloading PDB files"
        )
    run_command(
            f"cp -r /home/mchrnwsk/pda-destress-analysis/data/pdb_files /home/mchrnwsk/pda-destress-analysis/data/pdb_files_backup",
            "Copy PDB for safety backup"
        )
    run_command(
            f"cp -r /home/mchrnwsk/pda-destress-analysis/data/cif_files /home/mchrnwsk/pda-destress-analysis/data/cif_files_backup",
            "Copy CIF for safety backup"
        )

    # Step 5: Unzip all files
    gz_cif_files = [f for f in os.listdir("/home/mchrnwsk/pda-destress-analysis/data/cif_files/") if f.endswith('.gz')]
    if gz_cif_files:
        run_command(
            "gunzip -f /home/mchrnwsk/pda-destress-analysis/data/cif_files/*.gz 2>/dev/null || echo 'No .gz files found or decompression failed.'",
            "Unzipping CIF files"
        )
    gz_pdb_files = [f for f in os.listdir("/home/mchrnwsk/pda-destress-analysis/data/pdb_files/") if f.endswith('.gz')]
    if gz_pdb_files:
        run_command(
            "gunzip -f ./data/pdb_files/*.gz 2>/dev/null || echo 'No .gz files found or decompression failed.'",
            "Unzipping PDB files"
        )

    # Step 6: Run scrape_data.py
    if all_option:
        run_command(
            f"python scrape_data.py --next {next_date} --prev {prev_date} --all",
            "Running scrape_data.py"
        )
    else:
        run_command(
            f"python scrape_data.py --next {next_date} --prev {prev_date}",
            "Running scrape_data.py"
        )

    # Step 7: Manual download instructions
    wait_for_user("""Release dates of all PDBs:
                  1. Download custom report from the following URL:
                  https://www.rcsb.org/search?request=%7B%22query%22%3A%7B%22type%22%3A%22group%22%2C%22nodes%22%3A%5B%7B%22type%22%3A%22group%22%2C%22nodes%22%3A%5B%7B%22type%22%3A%22group%22%2C%22nodes%22%3A%5B%7B%22type%22%3A%22terminal%22%2C%22service%22%3A%22text%22%2C%22parameters%22%3A%7B%22attribute%22%3A%22rcsb_entry_info.structure_determination_methodology%22%2C%22operator%22%3A%22exact_match%22%2C%22value%22%3A%22experimental%22%7D%7D%5D%2C%22logical_operator%22%3A%22and%22%7D%5D%2C%22logical_operator%22%3A%22and%22%2C%22label%22%3A%22text%22%7D%5D%2C%22logical_operator%22%3A%22and%22%7D%2C%22return_type%22%3A%22entry%22%2C%22request_options%22%3A%7B%22scoring_strategy%22%3A%22combined%22%2C%22results_content_type%22%3A%5B%22experimental%22%5D%2C%22paginate%22%3A%7B%22start%22%3A0%2C%22rows%22%3A25%7D%2C%22sort%22%3A%5B%7B%22sort_by%22%3A%22score%22%2C%22direction%22%3A%22desc%22%7D%5D%7D%2C%22request_info%22%3A%7B%22query_id%22%3A%22e0fff76e6009d1aefc3970505b66f430%22%7D%7D
                  2. click on the right \"Tabular Report\", then on the left \"Create/Modify Custom Report\" instead of \"Tabular Report\", select \"Release Date\" checkbox, then run report and download CSV file
                  3. download only the most recent file as save to /home/mchrnwsk/pda-destress-analysis/data/pdb_release_dates - last download up to 248'335
                  4. change the value above for future reference.""")

    # Step 8: release_dates_of_all_PDB.py
    run_command(
        "python release_dates_of_all_PDB.py",
        "Running release_dates_of_all_PDB.py"
    )

    # Step 9: Manual download instructions
    ## Save fasta for natural proteins
    wait_for_user(f"""PDB FASTA sequences:
                  1. Go to https://www.rcsb.org/downloads/fasta
                  2. Download FASTA for all PDBs by clicking the \"Download a file containing sequences in FASTA format for all entries in the PDB archive\" hyperlink under the title
                  extract and save as pdb_seqres.txt to /home/mchrnwsk/pda-destress-analysis/data/pdb_seqres.txt
                  """)
    
    ## Save fasta for designed proteins
    ## Create an empty file to then manually add codes into
    run_command(
        f"nano /home/mchrnwsk/pda-destress-analysis/data/{next_date}_designed_sequences.fasta" ,
        f"Create empty file to save {next_date}_designed_sequences.fasta to"
    )
    if all_option:
        run_command(
        f"python print_pdb_codes_string.py --file /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes_total.txt -n 1000" ,
        f"Print {next_date}_pdb_codes_total.txt"
        )
    else:
        run_command(
        f"python print_pdb_codes_string.py --file /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes_new_download.txt" ,
        f"Print {next_date}_pdb_codes_new_download.txt to"
        )
    wait_for_user(f"""Designed FASTA sequences:
                  3. download and save to /home/mchrnwsk/pda-destress-analysis/data/{next_date}_designed_sequences.fasta
    Need all PDB codes for analysis! See print above ^^^
                  """)
    
    # Step 10: extract_designed_chains_from_fasta.py
    run_command(
        f"python extract_designed_chains_from_fasta.py --next {next_date}",
        "Running extract_designed_chains_from_fasta.py"
    )

    wait_for_user(f"""Next step deletes""")
    # Step 11: Delete structure files if not found in dataset (take up space and can mess up Foldseek analysis)
    run_command(
            f"python delete_file_if_not_in_dataset.py --next {next_date} --dir /home/mchrnwsk/pda-destress-analysis/data/pdb_files",
            "Delete PDB files not found in dataset"
        )
    run_command(
            f"python delete_file_if_not_in_dataset.py --next {next_date} --dir /home/mchrnwsk/pda-destress-analysis/data/cif_files",
            "Delete CIF files not found in dataset"
        )
    wait_for_user("Check that PDB and CIF files have been deleted correctly. If not, restore from backup and debug.")
    run_command(
        "rm -rf /home/mchrnwsk/pda-destress-analysis/data/pdb_files_backup",
        "Remove PDB backup"
    )
    run_command(
        "rm -rf /home/mchrnwsk/pda-destress-analysis/data/cif_files_backup",
        "Remove CIF backup"
    )

    # Step 12: Run MMseqs2
    run_command(
        f"python prepare_mmseqs2_input.py --next {next_date}",
        "Preparing MMseqs2 input")
    wait_for_user("Run MMseqs2 DvD and DvP commands manually on PC.")

    # Step 13: Analyse MMseqs2
    run_command(
        f"python /home/mchrnwsk/pda-destress-analysis/similarity_analysis_mmseq.py -d {next_date} -a max -p DvD -m bits -t 50",
        "Analysing MMseqs2 output, DvD max")
    run_command(
        f"python /home/mchrnwsk/pda-destress-analysis/similarity_analysis_mmseq.py -d {next_date} -a thr -p DvD -m bits -t 50",
        "Analysing MMseqs2 output, DvD thr")
    run_command(
        f"python /home/mchrnwsk/pda-destress-analysis/similarity_analysis_mmseq.py -d {next_date} -a max -p DvP -m bits -t 50",
        "Analysing MMseqs2 output, DvP max")
    run_command(
        f"python /home/mchrnwsk/pda-destress-analysis/similarity_analysis_mmseq.py -d {next_date} -a thr -p DvP -m bits -t 50",
        "Analysing MMseqs2 output, DvP thr")

    # Step 14: Send files to workstation
    wait_for_user("For the next step, make sure you are connected to the UoE VPN.")
    if all_option:
        run_command(
            f"bash /home/mchrnwsk/pda-destress-analysis/prepare_workstation_input.sh {next_date} --all",
            "Running workstation (Foldseek and Merizo) setup for all entries"
        )
    else:
        run_command(
            f"bash /home/mchrnwsk/pda-destress-analysis/prepare_workstation_input.sh {next_date}",
            "Running workstation (Foldseek and Merizo) setup for new entries"
        )

    # Step 15: Extract designed PDBs
    wait_for_user(f"""To make PDBs with extracted designed chains, run the following command manually on cysteine:""")
    if all_option:
        wait_for_user(f"""
    conda activate pdbUtils
    python /home/mchrnwsk/pda/foldseek/{next_date}/extract_designed_chains_from_pdb.py --next {next_date}
    conda deactivate
    cp -r /home/mchrnwsk/pda/foldseek/{next_date}/pdb_files_chains /home/mchrnwsk/pda/foldseek/{next_date}/DvD/
    cp -r /home/mchrnwsk/pda/foldseek/{next_date}/pdb_files_chains /home/mchrnwsk/pda/foldseek/{next_date}/DvP/
                      """)
    else:
        wait_for_user(f"""
    conda activate pdbUtils
    python /home/mchrnwsk/pda/foldseek/{next_date}/extract_designed_chains_from_pdb.py --next {next_date}
    conda deactivate
    cp -r /home/mchrnwsk/pda/foldseek/{next_date}/pdb_files_chains /home/mchrnwsk/pda/foldseek/{next_date}/DvD/
    cp -r /home/mchrnwsk/pda/foldseek/{next_date}/pdb_files_chains /home/mchrnwsk/pda/foldseek/{next_date}/DvP/
                      """)

    # Step 16: Run Foldseek
    wait_for_user(f"""To run Foldseek DvD and DvP, run the following command manually on cysteine:
    tmux
    conda activate foldseek
        cd /home/mchrnwsk/pda/foldseek/{next_date}/DvD/
        bash foldseek_search_dvd.sh
    OR
        cd /home/mchrnwsk/pda/foldseek/{next_date}/DvP/
        bash foldseek_search_dvp.sh
    ctrl+b then d
                  """)
    
    # Step 17: Analyse Foldseek
    wait_for_user(f"""To analyse Foldseek analysis, run the following command manually on cysteine (still in tmux):
    python /home/mchrnwsk/pda/foldseek/{next_date}/similarity_analysis_foldseek.py -d {next_date} -a max -p DvD -m lddt -t 0.95
        AND
    python /home/mchrnwsk/pda/foldseek/{next_date}/similarity_analysis_foldseek.py -d {next_date} -a max -p DvP -m lddt -t 0.95
        AND
    python /home/mchrnwsk/pda/foldseek/{next_date}/similarity_analysis_foldseek.py -d {next_date} -a thr -p DvD -m lddt -t 0.95
        AND
    python /home/mchrnwsk/pda/foldseek/{next_date}/similarity_analysis_foldseek.py -d {next_date} -a thr -p DvP -m lddt -t 0.95
                  """)
    
    # Step 18: Run Merizo search
    # In the future: try to use newly downloaded cath database:
    # bash /home/mchrnwsk/pda/merizo_search/download_dbs.sh cath /home/mchrnwsk/pda/merizo_search/database
    wait_for_user(f"""To run Merizo-search, run the following command manually on cysteine (still in tmux):
    conda deactivate
    conda activate merizo_search

    wget -P /home/mchrnwsk/pda/merizo_search/database ftp://orengoftp.biochem.ucl.ac.uk/cath/releases/daily-release/newest/cath-b-newest-names.gz
    gunzip /home/mchrnwsk/pda/merizo_search/database/cath-b-newest-names.gz

    python /home/mchrnwsk/pda/merizo_search/merizo_search/merizo.py easy-search /home/mchrnwsk/pda/foldseek/{next_date}/pdb_files_chains/*.pdb /home/mchrnwsk/pda/merizo_search/examples/database/cath /home/mchrnwsk/pda/foldseek/{next_date}/cath_results /home/mchrnwsk/pda/foldseek/{next_date}/tmp --multi_domain_search -k 100 --iterate 2>&1 | tee /home/mchrnwsk/pda/log.txt
    """)
    wait_for_user(f"""To add merizo-search results to the dataset, run the following command manually on cysteine (still in tmux):
    python /home/mchrnwsk/pda/merizo_to_json.py --json /home/mchrnwsk/pda/foldseek/{next_date}/{next_date}_data_scraped.json --tsv /home/mchrnwsk/pda/foldseek/{next_date}/cath_results_search.tsv --out /home/mchrnwsk/pda/foldseek/{next_date}/{next_date}_data_merizo.json
    """)

    # Step 19: Free up space and copy over output
    run_command(
        f"bash /home/mchrnwsk/pda-destress-analysis/process_workstation_output.sh {next_date}",
        "Tidying up after Foldseek analysis"
    )

    # Step 20: Add MMseqs2 and Foldseek analysis results to the dataset
    run_command(
        f"python /home/mchrnwsk/pda-destress-analysis/similarity_analysis_add_results.py --next {next_date}",
        "Adding MMseqs2 and Foldseek analysis results to the dataset"
    )

    # Step 21: Tidy up: remove manually excluded entries, recalculate previous and next designs, and manually curate data
    run_command(
            f"python remove_manually_excluded_entries.py --next {next_date} --input similarity --output reordered",
            "Adding MMseqs2 and Foldseek analysis results to the dataset"
        )
    run_command(
            f"python manual_data_curation.py --next {next_date} --input reordered --output curated",
            "Manually curating data"
        )
    print(f"Complete. Your output can be found at /home/mchrnwsk/pda-destress-analysis/data/{next_date}_data_curated.json")
    
    # Step 22: Move output to github and elm app directory
    run_command(f"cp /home/mchrnwsk/pda-destress-analysis/data/{next_date}_data_curated.json /home/mchrnwsk/chronowska-stam-wood-2024-protein-design-archive/data/",
                "Copying dataset to public repository"
    )
    run_command(f"cp /home/mchrnwsk/pda-destress-analysis/data/{next_date}_data_curated.json /home/mchrnwsk/protein-design-archive/backend/scripts/",
                "Copying dataset to elm app backend"
    )
    run_command(f"python print_pdb_codes_string.py --file /home/mchrnwsk/pda-destress-analysis/data/{next_date}_data_curated.json --exclude /home/mchrnwsk/pda-destress-analysis/data/{prev_date}_data_curated.json --uppercase --output /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes_new_download.txt",
                "Saving PDB codes txt file for download"
    )
    run_command(f"cp /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes_new_download.txt /home/mchrnwsk/protein-design-archive/backend/scripts/{next_date}_pdb_codes.txt",
                "Copying PDB codes txt file to elm app backend for download"
    )

    # Step 23: Celebrate!
    print("""
          Dataset update complete!
          ⚝⭒٭⋆⚝⭒٭⋆⚝⭒٭⋆⚝⭒٭⋆⚝⭒٭⋆⚝⭒٭⋆
          """)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape PDB data')
    parser.add_argument('--next', required=True, help='Next date (e.g., 20240930)')
    parser.add_argument('--prev', required=True, help='Prev date (e.g., 20240827)')
    parser.add_argument('--all', action='store_true', help='Processing for the whole dataset, not just new codes.')
    args = parser.parse_args()
    
    next_date = args.next
    prev_date = args.prev
    all_option = args.all

    main(next_date, prev_date, all_option)