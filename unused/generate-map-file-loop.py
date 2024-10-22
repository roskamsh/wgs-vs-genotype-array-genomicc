import pandas as pd
import os
import glob 

# Pull cohort information
cohorts = os.listdir("data/snpstats")
outdir = "data/map-id-file"

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
        snpstats.position = snpstats.position.astype(int)
        # Get old ID information
        oldids = snpstats.iloc[:, :6]
        oldids = oldids.drop(oldids.index[-1])
        # Create new ID information
        newrsids = list(oldids.chromosome + ":" + oldids.position.astype(int).astype(str) + ":" + oldids.alleleA + ":" + oldids.alleleB)
        newidcols = pd.DataFrame({'alternate_ids': newrsids, 'rsid': newrsids})

        newids = pd.concat([newidcols, oldids.iloc[:, 2:]], axis = 1)
        final = pd.concat([oldids,newids], axis = 1)

        # Write imputed snps to file
        final.to_csv(f"{outdir}/{cohort}/{chrom}.mapid", sep = " ", index = False)

