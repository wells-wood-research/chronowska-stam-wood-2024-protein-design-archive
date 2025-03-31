import argparse
import pandas as pd

parser = argparse.ArgumentParser(description="Formats file based on input format")
parser.add_argument("filepath")
args = parser.parse_args()

# Read file
with open(args.filepath, 'r') as file:
    content = file.read().strip()

# Determine format (comma-separated or newline-separated)
if ',' in content:
    data = pd.Series(content.split(','), name="pdb")  # Split by commas
else:
    data = pd.read_csv(args.filepath, header=None, names=["pdb"])["pdb"]  # Read as a column

# Convert to lowercase and remove duplicates
data = data.str.lower().drop_duplicates().sort_values()

# Save back to file in the original format
data.to_csv(args.filepath, index=False, header=False, sep='\n')
