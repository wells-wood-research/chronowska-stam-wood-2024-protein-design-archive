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
    ## Step 1: Review designs. Create file in official github repo for tracking home/mchrnwsk/chronowska-stam-wood-2024-protein-design-archive/data/{next_date}_pdb_codes.csv with new entries.
    #run_command(
    #        f"nano /home/mchrnwsk/chronowska-stam-wood-2024-protein-design-archive/data/{next_date}_pdb_codes.csv" ,
    #        f"Create empty file to save {next_date}_pdb_codes.csv to"
    #    )
    #wait_for_user(f"Add reviewed designs to add in the {next_date} update to /home/mchrnwsk/chronowska-stam-wood-2024-protein-design-archive/data/{next_date}_pdb_codes.csv")
    #wait_for_user(f"Add codes to exclude in the {next_date} update to /home/mchrnwsk/chronowska-stam-wood-2024-protein-design-archive/entries_to_manually_exclude.csv")
###
    ## Step 2: Create /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes.txt with entries not found in exclude, and found in manually include
    #if all_option:
    #    run_command(
    #        f"nano /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes_total.txt" ,
    #        f"Create empty file to save {next_date}_pdb_codes_total.txt to"
    #    )
    #    ## Print codes to add: new codes, excluding ones to exclude
    #    run_command(
    #        f"python /home/mchrnwsk/pda-destress-analysis/print_pdb_codes_string.py --file ../chronowska-stam-wood-2024-protein-design-archive/data/{next_date}_pdb_codes.csv --exclude ../chronowska-stam-wood-2024-protein-design-archive/entries_to_manually_exclude.csv --uppercase" ,
    #        "Running /home/mchrnwsk/pda-destress-analysis/print_pdb_codes_string.py with new_pdb_codes - entries_to_manually_exclude"
    #    ) 
    #    ## Print codes to add: those to manually include, which haven't been added in previous update
    #    run_command(
    #        f"python /home/mchrnwsk/pda-destress-analysis/print_pdb_codes_string.py --file ../chronowska-stam-wood-2024-protein-design-archive/entries_to_manually_include.csv --exclude data/{prev_date}_data_curated.json --uppercase" ,
    #        "Running /home/mchrnwsk/pda-destress-analysis/print_pdb_codes_string.py with entries_to_manually_include - old_pdb_codes"
    #    )
    #    ## Print codes to add: those from previous update, excluding ones to exclude
    #    run_command(
    #        f"python /home/mchrnwsk/pda-destress-analysis/print_pdb_codes_string.py --file data/{prev_date}_data_curated.json --exclude ../chronowska-stam-wood-2024-protein-design-archive/entries_to_manually_exclude.csv --uppercase" ,
    #        "Running /home/mchrnwsk/pda-destress-analysis/print_pdb_codes_string.py with old_pdb_codes - entries_to_manually_exclude"
    #    )
    #    wait_for_user(f"Add the above printed codes to /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes_total.txt")
    #else:
    #    run_command(
    #        f"nano /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes_new_download.txt" ,
    #        f"Create empty file to save {next_date}_pdb_codes_new_download.txt to"
    #    )
    #    ## Print codes to add: new codes, excluding ones to exclude
    #    run_command(
    #        f"python /home/mchrnwsk/pda-destress-analysis/print_pdb_codes_string.py --file ../chronowska-stam-wood-2024-protein-design-archive/data/{next_date}_pdb_codes.csv --exclude ../chronowska-stam-wood-2024-protein-design-archive/entries_to_manually_exclude.csv --uppercase" ,
    #        "Running /home/mchrnwsk/pda-destress-analysis/print_pdb_codes_string.py with new_pdb_codes - entries_to_manually_exclude"
    #    ) 
    #    ## Print codes to add: those to manually include, which haven't been added in previous update
    #    run_command(
    #        f"python /home/mchrnwsk/pda-destress-analysis/print_pdb_codes_string.py --file ../chronowska-stam-wood-2024-protein-design-archive/entries_to_manually_include.csv --exclude data/{prev_date}_data_curated.json --uppercase" ,
    #        "Running /home/mchrnwsk/pda-destress-analysis/print_pdb_codes_string.py with entries_to_manually_include - old_pdb_codes"
    #    )
    #    wait_for_user(f"Add the above printed codes to /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes_new_download.txt")
###
    ## Step 3: Download CIF files
    #os.makedirs("/home/mchrnwsk/pda-destress-analysis/data/cif_files", exist_ok=True)
    #if all_option:
    #    run_command(
    #        f"bash /home/mchrnwsk/pda-destress-analysis/data/download_pdbs.sh -f /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes_total.txt -o /home/mchrnwsk/pda-destress-analysis/data/cif_files -c",
    #        "Downloading CIF files"
    #    )
    #else:
    #    run_command(
    #        f"bash /home/mchrnwsk/pda-destress-analysis/data/download_pdbs.sh -f /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes_new_download.txt -o /home/mchrnwsk/pda-destress-analysis/data/cif_files -c",
    #        "Downloading CIF files"
    #    )
###
    ## Step 4: Download PDB files, .pdb and .pdb1
    #os.makedirs("/home/mchrnwsk/pda-destress-analysis/data/pdb_files", exist_ok=True)
    #if all_option:
    #    run_command(
    #        f"bash /home/mchrnwsk/pda-destress-analysis/data/download_pdbs.sh -f /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes_total.txt -o /home/mchrnwsk/pda-destress-analysis/data/pdb_files -p",
    #        "Downloading PDB files"
    #    )
    #    run_command(
    #        f"bash /home/mchrnwsk/pda-destress-analysis/data/download_pdbs.sh -f /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes_total.txt -o /home/mchrnwsk/pda-destress-analysis/data/pdb_files -a",
    #        "Downloading PDB files"
    #    )
    #else:
    #    run_command(
    #        f"bash /home/mchrnwsk/pda-destress-analysis/data/download_pdbs.sh -f /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes_new_download.txt -o /home/mchrnwsk/pda-destress-analysis/data/pdb_files -p",
    #        "Downloading PDB files"
    #    )
    #    run_command(
    #        f"bash /home/mchrnwsk/pda-destress-analysis/data/download_pdbs.sh -f /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes_new_download.txt -o /home/mchrnwsk/pda-destress-analysis/data/pdb_files -a",
    #        "Downloading PDB files"
    #    )
    #run_command(
    #        f"cp -r /home/mchrnwsk/pda-destress-analysis/data/pdb_files /home/mchrnwsk/pda-destress-analysis/data/pdb_files_backup",
    #        "Copy PDB for safety backup"
    #    )
    #run_command(
    #        f"cp -r /home/mchrnwsk/pda-destress-analysis/data/cif_files /home/mchrnwsk/pda-destress-analysis/data/cif_files_backup",
    #        "Copy CIF for safety backup"
    #    )
###
    ## Step 5: Unzip all files
    #gz_cif_files = [f for f in os.listdir("/home/mchrnwsk/pda-destress-analysis/data/cif_files/") if f.endswith('.gz')]
    #if gz_cif_files:
    #    run_command(
    #        "gunzip -f /home/mchrnwsk/pda-destress-analysis/data/cif_files/*.gz 2>/dev/null || echo 'No .gz files found or decompression failed.'",
    #        "Unzipping CIF files"
    #    )
    #gz_pdb_files = [f for f in os.listdir("/home/mchrnwsk/pda-destress-analysis/data/pdb_files/") if f.endswith('.gz')]
    #if gz_pdb_files:
    #    run_command(
    #        "gunzip -f /home/mchrnwsk/pda-destress-analysis//data/pdb_files/*.gz 2>/dev/null || echo 'No .gz files found or decompression failed.'",
    #        "Unzipping PDB files"
    #    )
#
    # Step 7: Run DE-STRESS
    wait_for_user(f"""In another terminal on this machine run the following command:
                  python /home/mchrnwsk/pda-destress-analysis/run_destress.py
                  """)
###
    ## Step 6: Run scrape_data.py
    #if all_option:
    #    run_command(
    #        f"python /home/mchrnwsk/pda-destress-analysis/scrape_data.py --next {next_date} --prev {prev_date} --all",
    #        "Running scrape_data.py"
    #    )
    #else:
    #    run_command(
    #        f"python /home/mchrnwsk/pda-destress-analysis/scrape_data.py --next {next_date} --prev {prev_date}",
    #        "Running scrape_data.py"
    #    )
###
    ## Step 7: Obtain release dates of all PDB
    #run_command(
    #    f"python /home/mchrnwsk/pda-destress-analysis/release_dates_of_all_PDB.py --prev {prev_date} --next {next_date}",
    #    "Updating PDB release dates automatically"
    #)
###
    ## Step 8: Save fasta for natural proteins
    #run_command(
    #    "python /home/mchrnwsk/pda-destress-analysis/download_pdb_fasta.py",
    #    "Downloading and extracting pdb_seqres.txt"
    #)
    #
    ### Save fasta for designed proteins
    ### Create an empty file to then manually add codes into
    #run_command(
    #    f"nano /home/mchrnwsk/pda-destress-analysis/data/{next_date}_designed_sequences.fasta" ,
    #    f"Create empty file to save {next_date}_designed_sequences.fasta to"
    #)
    #if all_option:
    #    run_command(
    #    f"python /home/mchrnwsk/pda-destress-analysis/print_pdb_codes_string.py --file /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes_total.txt -n 1000" ,
    #    f"Print {next_date}_pdb_codes_total.txt"
    #    )
    #else:
    #    run_command(
    #    f"python /home/mchrnwsk/pda-destress-analysis/print_pdb_codes_string.py --file /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes_new_download.txt" ,
    #    f"Print {next_date}_pdb_codes_new_download.txt to"
    #    )
    #wait_for_user(f"""Designed FASTA sequences:
    #              3. download and save to /home/mchrnwsk/pda-destress-analysis/data/{next_date}_designed_sequences.fasta
    #Need all PDB codes for analysis! See print above ^^^
    #              """)
    #
    ## Step 9: extract_designed_chains_from_fasta.py
    #run_command(
    #    f"python /home/mchrnwsk/pda-destress-analysis/extract_designed_chains_from_fasta.py --next {next_date}",
    #    "Running /home/mchrnwsk/pda-destress-analysis/extract_designed_chains_from_fasta.py"
    #)
###
    #wait_for_user(f"""Next step deletes""")
    ## Step 10: Delete structure files if not found in dataset (take up space and can mess up Foldseek analysis)
    #run_command(
    #        f"python /home/mchrnwsk/pda-destress-analysis/delete_file_if_not_in_dataset.py --next {next_date} --dir /home/mchrnwsk/pda-destress-analysis/data/pdb_files",
    #        "Delete PDB files not found in dataset"
    #    )
    #run_command(
    #        f"python /home/mchrnwsk/pda-destress-analysis/delete_file_if_not_in_dataset.py --next {next_date} --dir /home/mchrnwsk/pda-destress-analysis/data/cif_files",
    #        "Delete CIF files not found in dataset"
    #    )
    #wait_for_user("Check that PDB and CIF files have been deleted correctly. If not, restore from backup and debug.")
    #run_command(
    #    "rm -rf /home/mchrnwsk/pda-destress-analysis/data/pdb_files_backup",
    #    "Remove PDB backup"
    #)
    #run_command(
    #    "rm -rf /home/mchrnwsk/pda-destress-analysis/data/cif_files_backup",
    #    "Remove CIF backup"
    #)
###
    ## Step 11: Run MMseqs2
    #run_command(
    #    f"python /home/mchrnwsk/pda-destress-analysis/prepare_mmseqs2_input.py --next {next_date}",
    #    "Preparing MMseqs2 input")
    #wait_for_user("Run MMseqs2 DvD and DvP commands manually on PC.")
###
    ## Step 12: Analyse MMseqs2
    #run_command(
    #    f"python /home/mchrnwsk/pda-destress-analysis/similarity_analysis_mmseq.py -d {next_date} -a max -p DvD -m bits -t 50",
    #    "Analysing MMseqs2 output, DvD max")
    #run_command(
    #    f"python /home/mchrnwsk/pda-destress-analysis/similarity_analysis_mmseq.py -d {next_date} -a thr -p DvD -m bits -t 50",
    #    "Analysing MMseqs2 output, DvD thr")
    #run_command(
    #    f"python /home/mchrnwsk/pda-destress-analysis/similarity_analysis_mmseq.py -d {next_date} -a max -p DvP -m bits -t 50",
    #    "Analysing MMseqs2 output, DvP max")
    #run_command(
    #    f"python /home/mchrnwsk/pda-destress-analysis/similarity_analysis_mmseq.py -d {next_date} -a thr -p DvP -m bits -t 50",
    #    "Analysing MMseqs2 output, DvP thr")
###
    ## Step 13: Send files to workstation
    #wait_for_user("For the next step, make sure you are connected to the UoE VPN.")
    #if all_option:
    #    run_command(
    #        f"bash /home/mchrnwsk/pda-destress-analysis/prepare_workstation_input.sh {next_date} --all",
    #        "Running workstation (Foldseek and Merizo) setup for all entries"
    #    )
    #else:
    #    run_command(
    #        f"bash /home/mchrnwsk/pda-destress-analysis/prepare_workstation_input.sh {next_date}",
    #        "Running workstation (Foldseek and Merizo) setup for new entries"
    #    )
###
    ## Step 14: Extract designed PDBs
    #wait_for_user(f"""To make PDBs with extracted designed chains, run the following command manually on cysteine:""")
    #if all_option:
    #    wait_for_user(f"""
    #conda activate pdbUtils
    #python /home/mchrnwsk/pda/foldseek/{next_date}/extract_designed_chains_from_pdb.py --next {next_date}
    #conda deactivate
    #cp -r /home/mchrnwsk/pda/foldseek/{next_date}/pdb_files_chains /home/mchrnwsk/pda/foldseek/{next_date}/DvD/
    #cp -r /home/mchrnwsk/pda/foldseek/{next_date}/pdb_files_chains /home/mchrnwsk/pda/foldseek/{next_date}/DvP/
    #                  """)
    #else:
    #    wait_for_user(f"""
    #conda activate pdbUtils
    #python /home/mchrnwsk/pda/foldseek/{next_date}/extract_designed_chains_from_pdb.py --next {next_date}
    #conda deactivate
    #cp -r /home/mchrnwsk/pda/foldseek/{next_date}/pdb_files_chains /home/mchrnwsk/pda/foldseek/{next_date}/DvD/
    #cp -r /home/mchrnwsk/pda/foldseek/{next_date}/pdb_files_chains /home/mchrnwsk/pda/foldseek/{next_date}/DvP/
    #                  """)
###
    ## Step 15: Run Foldseek
    #wait_for_user(f"""To run Foldseek DvD and DvP, run the following command manually on cysteine:
    #tmux
    #conda activate foldseek
    #    cd /home/mchrnwsk/pda/foldseek/{next_date}/DvD/
    #    bash foldseek_search_dvd.sh
    #OR
    #    cd /home/mchrnwsk/pda/foldseek/{next_date}/DvP/
    #    bash foldseek_search_dvp.sh
    #ctrl+b then d
    #              """)
    #
    ## Step 16: Analyse Foldseek
    #wait_for_user(f"""To analyse Foldseek analysis, run the following command manually on cysteine (still in tmux):
    #python /home/mchrnwsk/pda/foldseek/{next_date}/similarity_analysis_foldseek.py -d {next_date} -a max -p DvD -m lddt -t 0.95
    #    AND
    #python /home/mchrnwsk/pda/foldseek/{next_date}/similarity_analysis_foldseek.py -d {next_date} -a max -p DvP -m lddt -t 0.95
    #    AND
    #python /home/mchrnwsk/pda/foldseek/{next_date}/similarity_analysis_foldseek.py -d {next_date} -a thr -p DvD -m lddt -t 0.95
    #    AND
    #python /home/mchrnwsk/pda/foldseek/{next_date}/similarity_analysis_foldseek.py -d {next_date} -a thr -p DvP -m lddt -t 0.95
    #              """)
    #
    ## Step 17: Run Merizo search
    ## In the future: try to use newly downloaded cath database:
    ## bash /home/mchrnwsk/pda/merizo_search/download_dbs.sh cath /home/mchrnwsk/pda/merizo_search/database
    #wait_for_user(f"""To run Merizo-search, run the following command manually on cysteine (still in tmux):
    #conda deactivate
    #conda activate merizo_search
#
    #cd /home/mchrnwsk/pda/merizo_search
    #
    #            
    #wget -P /home/mchrnwsk/pda/merizo_search/database ftp://orengoftp.biochem.ucl.ac.uk/cath/releases/daily-release/newest/cath-b-newest-names.gz
    #gunzip /home/mchrnwsk/pda/merizo_search/database/cath-b-newest-names.gz
#
    #python /home/mchrnwsk/pda/merizo_search/run_merizo_incremental.py --next {next_date} --prev {prev_date}
    #"""
    #)
#
    #wait_for_user(f"""Run command manually on cysteine to add Merizo-search results:
#
    #python /home/mchrnwsk/pda/merizo_search/merizo_to_json.py --json /home/mchrnwsk/pda/foldseek/{next_date}/{next_date}_data_scraped.json --tsv /home/mchrnwsk/pda/foldseek/{next_date}/cath_results_search.tsv --out /home/mchrnwsk/pda/foldseek/{next_date}/{next_date}_data_merizo.json
    #"""
    #)
#
    ## Step 18: Free up space and copy over output
    #run_command(
    #    f"bash /home/mchrnwsk/pda-destress-analysis/process_workstation_output.sh {next_date}",
    #    "Tidying up after Foldseek analysis"
    #)

    # Step 19: Add MMseqs2 and Foldseek analysis results to the dataset
    run_command(
        f"python /home/mchrnwsk/pda-destress-analysis/similarity_analysis_add_results.py --next {next_date}",
        f"Adding MMseqs2 and Foldseek analysis results to the dataset (see output at /home/mchrnwsk/pda-destress-analysis/data/{next_date}_data_similarity.json)"
    )

    # Step 19: Add DE-STRESS analysis results to the dataset
    run_command(
        f"python /home/mchrnwsk/pda-destress-analysis/structure_analysis_add_results.py --next {next_date}",
        f"Adding DE-STRESS analysis results to the dataset (see output at /home/mchrnwsk/pda-destress-analysis/data/{next_date}_data_destress.json)"
    )

    # Step 20: Tidy up: remove manually excluded entries, recalculate previous and next designs, and manually curate data
    run_command(
            f"python /home/mchrnwsk/pda-destress-analysis/remove_manually_excluded_entries.py --next {next_date} --input destress --output reordered",
            "Remove manually excluded entries"
        )
    run_command(
            f"python /home/mchrnwsk/pda-destress-analysis/manual_data_curation.py --next {next_date} --input reordered --output curated",
            "Manually curating data"
        )
    print(f"Complete. Your output can be found at /home/mchrnwsk/pda-destress-analysis/data/{next_date}_data_curated.json")
    
    # Step 21: Move output to github and elm app directory
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

    # Step 22: Celebrate!
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