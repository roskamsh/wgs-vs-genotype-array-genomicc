import pandas as pd
import os
import glob 

# Pull cohort information
cohorts = os.listdir("data/snpstats")
outdir = "data/snpstats-updated-id"

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
        snpstats.rsid = snpstats.chromosome + ":" + snpstats.position.astype(int).astype(str) + ":" + snpstats.alleleA + ":" + snpstats.alleleB

        # Write imputed snps to file
        snpstats.to_csv(f"{outdir}/{cohort}/{chrom}.snpstats", index = False)

