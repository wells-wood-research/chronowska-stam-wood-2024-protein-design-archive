import os
import subprocess
import sys
from datetime import datetime

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

def parse_arguments():
    next_date = None
    prev_date = None
    argv = sys.argv[1:]

    for i in range(len(argv)):
        if argv[i] == '--next' and i + 1 < len(argv):
            next_date = argv[i + 1]
        elif argv[i] == '--prev' and i + 1 < len(argv):
            prev_date = argv[i + 1]

    if not next_date or not prev_date:
        print("Usage: script.py --next NEXT_DATE --prev PREV_DATE")
        sys.exit(1)

    return next_date, prev_date

def main():
    next_date, prev_date = parse_arguments()

    # Step 1: Review designs. Create file in official github repo for tracking home/mchrnwsk/chronowska-stam-wood-2024-protein-design-archive/data/{next_date}_pdb_codes.csv with new entries.
    wait_for_user(f"Add reviewed designs to add in the {next_date} update to home/mchrnwsk/chronowska-stam-wood-2024-protein-design-archive/data/{next_date}_pdb_codes.csv")
    
    # Step 2: Create /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes.txt with entries not found in exclude, and found in manually include
    run_command(
        f"nano /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes_new_download.txt" ,
        f"Create empty file to save {next_date}_pdb_codes_new_download.txt to"
    )
    ## Print codes to add: new codes, excluding ones to exclude
    run_command(
        f"python print_pdb_codes_string.py --file ../chronowska-stam-wood-2024-protein-design-archive/data/{next_date}_pdb_codes.csv --exclude ../chronowska-stam-wood-2024-protein-design-archive/entries_to_manually_exclude.csv --uppercase" ,
        "Running print_pdb_codes_string.py with new_pdb_codes - entires_to_manually_exclude"
    ) 
    ## Print codes to add: those to manually include, which haven't been added in previous update
    run_command(
        f"python print_pdb_codes_string.py --file ../chronowska-stam-wood-2024-protein-design-archive/entries_to_manually_include.csv --exclude data/{prev_date}_data_curated.json --uppercase" ,
        "Running print_pdb_codes_string.py with entires_to_manually_include - old_pdb_codes"
    )
    wait_for_user(f"Add the above printed codes to /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes_new_download.txt")

    # Step 3: Download CIF files
    run_command(
        f"bash /home/mchrnwsk/pda-destress-analysis/data/download_pdbs.sh -f /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes.txt -o /home/mchrnwsk/pda-destress-analysis/data/cif_files -c",
        "Downloading CIF files"
    )
    run_command(
        "gunzip -f /home/mchrnwsk/pda-destress-analysis/data/cif_files/*.gz",
        "Unzipping CIF files"
    )

    # Step 4: Run scrape_data.py
    run_command(
        f"python scrape_data.py --next {next_date} --prev {prev_date}",
        "Running scrape_data.py"
    )

    # Step 5: Manual download instructions
    wait_for_user("""Release dates of all PDBs:
                  1. Download custom report from the following URL:
                  https://www.rcsb.org/search?request=%7B%22query%22%3A%7B%22type%22%3A%22group%22%2C%22nodes%22%3A%5B%7B%22type%22%3A%22group%22%2C%22nodes%22%3A%5B%7B%22type%22%3A%22group%22%2C%22nodes%22%3A%5B%7B%22type%22%3A%22terminal%22%2C%22service%22%3A%22text%22%2C%22parameters%22%3A%7B%22attribute%22%3A%22rcsb_entry_info.structure_determination_methodology%22%2C%22operator%22%3A%22exact_match%22%2C%22value%22%3A%22experimental%22%7D%7D%5D%2C%22logical_operator%22%3A%22and%22%7D%5D%2C%22logical_operator%22%3A%22and%22%2C%22label%22%3A%22text%22%7D%5D%2C%22logical_operator%22%3A%22and%22%7D%2C%22return_type%22%3A%22entry%22%2C%22request_options%22%3A%7B%22scoring_strategy%22%3A%22combined%22%2C%22results_content_type%22%3A%5B%22experimental%22%5D%2C%22paginate%22%3A%7B%22start%22%3A0%2C%22rows%22%3A25%7D%2C%22sort%22%3A%5B%7B%22sort_by%22%3A%22score%22%2C%22direction%22%3A%22desc%22%7D%5D%7D%2C%22request_info%22%3A%7B%22query_id%22%3A%22e0fff76e6009d1aefc3970505b66f430%22%7D%7D
                  2. select \"Create Custom Report\" instead of \"Tabular Report\", run report, then select \"Release Date\" checkbox and download CSV file
                  3. download only the most recent file as save to /home/mchrnwsk/pda-destress-analysis/data/pdb_release_dates - last download up to 227'111
                  4. change the value above for future reference.""")

    # Step 6: release_dates_of_all_PDB.py
    run_command(
        "python release_dates_of_all_PDB.py",
        "Running release_dates_of_all_PDB.py"
    )

    # Step 7: Manual download instructions
    ## Create an empty file to then manually add codes into
    run_command(
        f"nano /home/mchrnwsk/pda-destress-analysis/data/{next_date}_designed_sequences.fasta" ,
        f"Create empty file to save {next_date}_designed_sequences.fasta to"
    )
    wait_for_user(f"""FASTA sequences:
                  1. Go to https://www.rcsb.org/downloads/fasta
                  2. Download FASTA for all PDBs by clicking the \"Download a file containing sequences in FASTA format for all entries in the PDB archive\" hyperlink under the title
                  extract and save as pdb_seqres.txt to /home/mchrnwsk/pda-destress-analysis/data/pdb_seqres.txt
                  3. download and save to /home/mchrnwsk/pda-destress-analysis/data/{next_date}_designed_sequences.fasta
                  by pasting in the code list obtained by print_pdb_codes_string.py or found in /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes.txt
                  """)

    # Step 8: extract_designed_chains_from_fasta.py
    run_command(
        f"python extract_designed_chains_from_fasta.py --next {next_date}",
        "Running extract_designed_chains_from_fasta.py"
    )

    # Step 9: Download PDB files, .pdb and .pdb1
    run_command(
        f"bash data/download_pdbs.sh -f /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes.txt -o /home/mchrnwsk/pda-destress-analysis/data/pdb_files -p",
        "Downloading PDB files"
    )
    run_command(
        f"bash data/download_pdbs.sh -f /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes.txt -o /home/mchrnwsk/pda-destress-analysis/data/pdb_files -a",
        "Downloading PDB files"
    )
    run_command(
        "gunzip -f ./data/pdb_files/*.gz",
        "Unzipping PDB files"
    )

    # Step 10: Delete structure files if not found in dataset (take up space and can mess up Foldseek analysis)
    run_command(
            f"python delete_file_if_not_in_dataset.py --next {next_date} --dir /home/mchrnwsk/pda-destress-analysis/data/pdb_files",
            "Delete PDB files not found in dataset"
        )
    run_command(
            f"python delete_file_if_not_in_dataset.py --next {next_date} --dir /home/mchrnwsk/pda-destress-analysis/data/cif_files",
            "Delete CIF files not found in dataset"
        )

    # Step 11: extract_designed_chains_from_pdb.py
    os.makedirs("/home/mchrnwsk/pda-destress-analysis/data/pdb_files_chains", exist_ok=True)
    run_command(
        f"python extract_designed_chains_from_pdb.py --next {next_date}",
        "Running extract_designed_chains_from_pdb.py"
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

    # Step 14: Run Foldseek
    wait_for_user("For the next step, make sure you are connected to the UoE VPN.")
    run_command(
        f"bash /home/mchrnwsk/pda-destress-analysis/prepare_foldseek_input.sh {next_date}",
        "Running Foldseek setup"
    )
    wait_for_user(f"""Run Foldseek DvD and DvP manually on cysteine
                  by running the following commands:
                    tmux
                    conda activate foldseek
                        cd foldseek/{next_date}/DvD/
                        bash foldseek_search_dvd.sh
                    OR
                        cd foldseek/{next_date}/DvP/
                        bash foldseek_search_dvd.sh
                    ctrl+b then d
                  """)
    
    # Step 15: Analyse Foldseek
    wait_for_user(f"""Run Foldseek analysis manually on cysteine
                  by running the following commands (still in tmux):
                        python /home/mchrnwsk/pda/foldseek/{next_date}/similarity_analysis_foldeek.py -d {next_date} -a max -p DvD -m lddt -t 0.95
                    AND
                        python /home/mchrnwsk/pda/foldseek/{next_date}/similarity_analysis_foldeek.py -d {next_date} -a max -p DvP -m lddt -t 0.95
                    AND
                        python /home/mchrnwsk/pda/foldseek/{next_date}/similarity_analysis_foldeek.py -d {next_date} -a thr -p DvD -m lddt -t 0.95
                    AND
                        python /home/mchrnwsk/pda/foldseek/{next_date}/similarity_analysis_foldeek.py -d {next_date} -a thr -p DvP -m lddt -t 0.95
                  """)
    
    # Step 16: Free up space and copy over output
    run_command(
        f"bash /home/mchrnwsk/pda-destress-analysis/process_foldseek_output.sh {next_date}",
        "Tidying up after Foldseek analysis"
    )

    # Step 17: Add MMseqs2 and Foldseek analysis results to the dataset
    run_command(
        f"python /home/mchrnwsk/pda-destress-analysis/similarity_analysis_add_results.py --next {next_date}",
        "Adding MMseqs2 and Foldseek analysis results to the dataset"
    )

    # Step 18: Tidy up: remove manually excluded entries, recalculate previous and next designs, and manually curate data
    run_command(
            f"python remove_manually_excluded_entries.py --next {next_date} --input similarity --output reordered",
            "Adding MMseqs2 and Foldseek analysis results to the dataset"
        )
    run_command(
            f"python manual_data_curation.py --next {next_date} --input reordered --output curated",
            "Manually curating data"
        )
    print(f"Complete. Your output can be found at /home/mchrnwsk/pda-destress-analysis/data/{next_date}_data_curated.json")
    
    # Step 19: Move output to elm app directory
    run_command(f"cp /home/mchrnwsk/pda-destress-analysis/data/{next_date}_data_curated.json /home/mchrnwsk/protein-design-archive/backend/scripts/",
                "Copying dataset to elm app backend"
    )
    run_command(f"python print_pdb_codes_string.py --file /home/mchrnwsk/pda-destress-analysis/data/{next_date}_data_curated.json --exclude /home/mchrnwsk/pda-destress-analysis/data/{prev_date}_data_curated.json --uppercase --output /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes_new_download.txt",
                "Saving PDB codes txt file for download"
    )
    run_command(f"cp /home/mchrnwsk/pda-destress-analysis/data/{next_date}_pdb_codes_new_download.txt /home/mchrnwsk/protein-design-archive/backend/scripts/{next_date}_pdb_codes.txt",
                "Copying PDB codes txt file to elm app backend for download"
    )

    # Step 20: Complete
    print("""
          Dataset update complete!
          ⚝⭒٭⋆⚝⭒٭⋆⚝⭒٭⋆⚝⭒٭⋆⚝⭒٭⋆⚝⭒٭⋆
          """)

if __name__ == "__main__":
    main()