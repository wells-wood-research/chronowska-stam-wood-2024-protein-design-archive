#!/bin/bash

# Path to the current directory
BASE_DIR=$(pwd)

# Easy-search
docker run -it --rm -v ${BASE_DIR}:/data soedinglab/mmseqs2 mmseqs easy-search /data/designed_single_sequences_1450.fasta /data/designed_single_sequences_1450.fasta /data/results.m8 /data/tmp -a 1 --exhaustive-search 1 -s 7.0 --add-self-matches --format-output "query,qlen,target,tlen,bits,pident,raw,cigar,qcov,tcov"