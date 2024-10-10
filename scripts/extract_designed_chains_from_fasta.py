import pandas as pd
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

date = "20240930"
filename_data = "/home/mchrnwsk/pda-destress-analysis/data/"+date+"_data_curated.json"
filename_fasta_input = "/home/mchrnwsk/pda-destress-analysis/data/designed_sequences_"+date+".fasta"
filename_fasta_output = "/home/mchrnwsk/pda-destress-analysis/data/designed_chains_"+date+".fasta"

data = pd.read_json(filename_data)
records_iterable = SeqIO.to_dict(SeqIO.parse(filename_fasta_input, "fasta"))
records_designed = SeqIO.to_dict(SeqIO.parse(filename_fasta_input, "fasta"))

designed_single_sequences = {}

# Iterate through the records and group them by PDB code
for record_id, record in records_iterable.items():
    pdb_code = record_id[:4].lower()  # Extract the first four characters (PDB code)

    if data["pdb"].str.contains(pdb_code).any() != True:
        records_designed.pop(record_id, None)
    if "32630" not in record.description.split("|")[-1]:
        records_designed.pop(record_id, None)

print(f"Total number of chains: {len(records_iterable)}")
print(f"Number of designed chains: {len(records_designed)}")

designed_chains_record = []
for pdb_code, sequence in records_designed.items():
    designed_seq = ''.join(sequence)  # Concatenate all sequences in the group
    record = SeqRecord(Seq(designed_seq), id=pdb_code, description=f"designed single sequences for {pdb_code}")
    designed_chains_record.append(record)

with open(filename_fasta_output, "w") as output_handle:
    SeqIO.write(designed_chains_record, output_handle, "fasta")