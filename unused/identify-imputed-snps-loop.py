import pandas as pd
import numpy as np
import os
import glob 

def alleles_match(row):
    ref_alt_set = {row['REF'], row['ALT']}
    allele_a_b_set = {row['alleleA'], row['alleleB']}
    return ref_alt_set == allele_a_b_set

# genotyped SNP IDs
genotyped_ids = pd.read_csv("data/genotyped-snps-hg38.txt", sep = " ", header = None)
genotyped_ids.columns = ["SNP","CHR","POS","REF","ALT"]

# Do so for each cohort
cohorts = os.listdir("data/snpstats")
outdir = "data/imputed-snps"

for cohort in cohorts:
    file_pattern = os.path.join("data", "snpstats", cohort, 'chr*.snpstats')
    files = glob.glob(file_pattern)
    os.makedirs(f"{outdir}/{cohort}",exist_ok = True)

    # For each file, read in snpstats, determine which are not in genotyped snps list & write exclusion snps
    for file_path in files:
        print(f"Reading in file: {file_path}")
        filename = file_path.split('/')[3]
        chrom = filename.replace('.snpstats','')
        snpstats = pd.read_csv(file_path, delimiter="\t", skiprows=9)
        snpstats = snpstats.dropna(subset=['chromosome']) 
        snpstats['chromosome_int'] = snpstats['chromosome'].str.replace('^chr', '', regex=True).astype(int)
        snpstats['position'] = snpstats['position'].astype(int)

        # Check for SNPs found in genotyped list & BGEN file
        merged_df = pd.merge(snpstats, genotyped_ids, left_on=['chromosome_int', 'position'], right_on=['CHR', 'POS'], how='left')
        merged_df['is_genotyped'] = merged_df.apply(alleles_match, axis=1)
        imputed_df = merged_df[~merged_df.is_genotyped].copy()

        # Print some summary statistics about genotyped/imputed snps
        n_genotyped = sum(merged_df.is_genotyped)
        n_imputed = imputed_df.shape[0]
        print(f"Number of genotyped SNPs for {chrom}: {n_genotyped}")
        print(f"Number of imputed SNPs for {chrom}: {n_imputed}")

        # Write imputed snps to file
        imputed_snps = list(imputed_df.rsid.unique())
        rsids = " ".join(imputed_snps)
        with open(f"{outdir}/{cohort}/{chrom}_imputed_rsids.txt", "w") as text_file:
            text_file.write(rsids) 

