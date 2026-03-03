from Bio import bgzf
import gzip
import os
import numpy as np

"""
This script cleans up genotypes by removing invalid genotypes from raw vcf.

Script should be run from inside the scripts folder.

Example usage:
    python preprocess.py
"""

def process_headers(input: str, output: str):
    headers = []
    print("processing headers")
    # get headers
    with gzip.open(input, 'rt') as f:
        for line in f:
            if line.startswith("##"):
                headers.append(line)
            else:
                break

    # write out to output
    with bgzf.open(output, 'wt') as f:
        for line in headers:
            f.write(line)

    # write out to output (without gz)
    with open(output.replace('.gz',''), 'w',  encoding='utf-8') as f:
        for line in headers:
            f.write(line)

    return

def process_rows(input: str, output: str):
    print(f"processing rows")
    # find all columns where there are two '|' within a single field or no '|'
    del_cols = set()
    with gzip.open(input, 'rt') as f:
        for line in f:
            # skip headers
            if line.startswith("##"):
                continue
            
            if line.startswith("#"):
                headers=line.strip().split('\t')
                continue
            
            cols = line.split('\t')     # break up line into columns
            for idx, col in enumerate(cols):
                if idx < 9: # first 10 columns are not genotype information
                    continue
                if (col.count('|') == 0) or (col.count('|') == 2):
                    del_cols.add(idx)
    print(f"Removing {len(del_cols)} sample columns which are not formated properly for at least 1 SNP")

    lines = []
    with gzip.open(input, 'rt') as f:
        for line in f:
            # skip headers
            if line.startswith("#"):
                continue

            cols = line.strip().split('\t')     # break up line into columns
            new_cols = []
            for idx, col in enumerate(cols):
                if idx not in del_cols:
                    new_cols.append(col)
            lines.append('\t'.join(new_cols) + '\n')

    # write out the sample names that were dropped
    samples = np.array(headers)
    dropped_ids = samples[list(del_cols)]
    with open(output.replace('.gz','.dropped.txt'), 'w', encoding='utf-8') as f:
        for id in dropped_ids:
            f.write(str(id) + '\n')

    new_header = [col for idx, col in enumerate(headers) if idx not in del_cols]

    # write out to output
    with bgzf.open(output, 'at') as f:
        f.write('\t'.join(new_header) + '\n')
        for line in lines:
            f.write(line)

    # write out to output (without compression)
    with open(output.replace('.gz',''), 'at',  encoding='utf-8') as f:
        f.write('\t'.join(new_header) + '\n')
        for line in lines:
            f.write(line)
    return

def main(in_vcf: str, out_vcf: str):
    """
    Parameters:
        in_vcf (str): path to raw vcf
        out_vcf (str): output path for cleaned vcf
    """
    process_headers(in_vcf, out_vcf)
    process_rows(in_vcf, out_vcf)
    os.system(f"tabix -p vcf {OUTPUT}")
    return

if __name__ == "__main__":
    INPUT = "../data/raw/GenRisk_all_CRC_SNPs_perm.vcf.gz"
    OUTPUT = "../data/processed/GenRisk_all_CRC_SNPs_perm.clean.vcf.gz"
    main(INPUT, OUTPUT)