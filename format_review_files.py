import argparse
import pandas as pd

parser = argparse.ArgumentParser(description = "Formats file to remove duplicates and convert entries to lowercase")
parser.add_argument("filepath")
args = parser.parse_args()

data = pd.read_csv(args.filepath, header=None)
data[0] = data[0].str.lower()
data.drop_duplicates(inplace=True)
data.sort_values(by=data.columns[0], inplace=True)
data.to_csv(args.filepath, index=False, header=False)