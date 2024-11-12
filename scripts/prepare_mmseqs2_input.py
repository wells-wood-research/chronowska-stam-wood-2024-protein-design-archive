import os
import argparse

def main(next_date):
    base_dir_data = "/home/mchrnwsk/pda-destress-analysis/data/"
    base_dir_analysis = "/home/mchrnwsk/pda-destress-analysis/similarity/mmseq"
    git_dir_mmseqs2 = "/home/mchrnwsk/chronowska-stam-wood-2024-protein-design-archive/MMseqs2"
    current_dir_mmseqs2 = f"{base_dir_analysis}/{next_date}"
    dvd_current_dir_mmseqs2 = f"{current_dir_mmseqs2}/DvD"
    dvp_current_dir_mmseqs2 = f"{current_dir_mmseqs2}/DvP"

    scripts = {
        "dvd": {
            "source": f"{git_dir_mmseqs2}/mmseqs2_search_dvd.sh",
            "destination": dvd_current_dir_mmseqs2
        },
        "dvp": {
            "source": f"{git_dir_mmseqs2}/mmseqs2_search_dvp.sh",
            "destination": dvp_current_dir_mmseqs2
        }
    }

    inputs = {
        "designed": {
            "source": f"{base_dir_data}/{next_date}_designed_chains.fasta",
            "destination_dvd": f"{dvd_current_dir_mmseqs2}/{next_date}_designed_chains.fasta",
            "destination_dvp": f"{dvp_current_dir_mmseqs2}/{next_date}_designed_chains.fasta"
        },
        "natural": {
            "source": f"{base_dir_data}/pdb_seqres.txt",
            "destination_dvd": f"{dvd_current_dir_mmseqs2}/pdb_sequences.fasta",
            "destination_dvp": f"{dvp_current_dir_mmseqs2}/pdb_sequences.fasta"
        }
    }

    # MMseqs2
    # Create folders:
    os.mkdir(current_dir_mmseqs2)
    os.mkdir(dvd_current_dir_mmseqs2)
    os.mkdir(dvp_current_dir_mmseqs2)

    # Put input files:
    # Inputs
    for input_key, input_paths in inputs.items():
        source_file = input_paths["source"]
        destination_file_dvd = input_paths["destination_dvd"]
        destination_file_dvp = input_paths["destination_dvp"]

        with open(source_file, 'r') as file:
            script_content = file.read()
        with open(destination_file_dvd, 'w') as file:
            file.write(script_content)
        with open(destination_file_dvp, 'w') as file:
            file.write(script_content)

    # Scripts
    for script_key, script_paths in scripts.items():
        source_file = script_paths["source"]
        destination_dir = script_paths["destination"]
        destination_file = script_paths["destination"]+f"/search_{script_key}.sh"
        
        # Read the original file content
        with open(source_file, 'r') as file:
            script_content = file.read()

        # Replace the relevant part of the script with the new format
        script_content = script_content.replace(
            "/data/designed_single_sequences_1450.fasta", 
            f"/data/{next_date}_designed_chains.fasta"
        )

        script_content = script_content.replace(
            "$(pwd)", 
            destination_dir
        )

        # Write the modified content to the new file location
        with open(destination_file, 'w') as file:
            file.write(script_content)

    print("")
    print(f"Check {current_dir_mmseqs2} for prepared analysis directory.")
    print("")
    print(f"Run command\nsudo bash {dvd_current_dir_mmseqs2}/search_dvd.sh\nor\nsudo bash {dvp_current_dir_mmseqs2}/search_dvp.sh\nfor analysis.")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Prepare input files for MMSeqs2 analysis')
    parser.add_argument('--next', required=True, help='Next date (e.g., 20240930)')
    args = parser.parse_args()
    
    next_date = args.next

    main(next_date)