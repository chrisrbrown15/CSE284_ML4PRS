#!/bin/bash

# This script checks integrity of a vcf file
#
# Parameters: 
#   1: path to bcftools
#   2: path to vcf file
#
# Example usage:
#   bash scripts/check_genotypes.sh ./tools/bcftools/bin/bcftools data/processed/GenRisk_all_CRC_SNPs_perm.clean.vcf

bcftool=$1
file=$2

$1 view $2 > /dev/null