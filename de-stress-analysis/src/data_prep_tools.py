import os


def extract_combined_sequence_from_pdb(pdb_file, standard_residue_dict, nonstandard_residue_dict):
    combined_sequence = []
    seen_residues = set()

    with open(pdb_file, 'r') as file:
        for line in file:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                chain_id = line[21]
                res_name = line[17:20].strip()
                res_seq = int(line[22:26].strip())
                residue_id = (chain_id, res_seq)
                
                # Process each residue only once
                if residue_id not in seen_residues:
                    seen_residues.add(residue_id)
                    if res_name in standard_residue_dict.keys():
                        
                        combined_sequence.append(standard_residue_dict.get(res_name))

                    elif res_name in nonstandard_residue_dict.keys():

                        combined_sequence.append(standard_residue_dict.get(nonstandard_residue_dict.get(res_name)))

                    elif res_name == "HOH":

                        combined_sequence.append('')

                    else:

                        combined_sequence.append('X')

    return ''.join(combined_sequence)

def extract_combined_sequences_from_directory(directory, standard_residue_dict, nonstandard_residue_dict):
    pdb_files = [f for f in os.listdir(directory) if f.endswith('.pdb')]
    all_sequences = {}

    for pdb_file in pdb_files:
        file_path = os.path.join(directory, pdb_file)
        sequence = extract_combined_sequence_from_pdb(file_path, standard_residue_dict, nonstandard_residue_dict)
        all_sequences[pdb_file] = sequence

    return all_sequences


def calculate_aa_composition(sequence, standard_amino_acids):
    composition = {aa: 0 for aa in standard_amino_acids}
    # total_count = len(sequence)

    for aa in sequence:
        if aa in composition:
            composition[aa] += 1

    return composition