# Create query database (designed proteins, designed chains concatenated into one structure)
foldseek createdb 1450_designed_structures ./data/queryDB --input-format 1  --chain-name-mode 0

# Create target database (all of pdb)
foldseek databases PDB ./data/targetDB-uncomp tmp

# Perform search of structural similarity between target and query 
foldseek easy-search ./data/queryDB ./data/targetDB-uncomp ./output/resultDB tmp/ -s 7.5 --exhaustive-search 1 --format-output query,qlen,target,tlen,prob,lddt,pident,cigar,qcov,tcov,alntmscore,lddt,evalue,bits
