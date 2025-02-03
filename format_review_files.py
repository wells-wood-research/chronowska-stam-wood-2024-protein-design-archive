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
    data = pd.Series(content.split(','))  # Split by commas
else:
    data = pd.read_csv(args.filepath, header=None, squeeze=True)  # Read as a column

# Convert to lowercase and remove duplicates
data = data.str.lower().drop_duplicates()

# Save to file with each entry on a new line
data.to_csv(args.filepath, index=False, header=False)