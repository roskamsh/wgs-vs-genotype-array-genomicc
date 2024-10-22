import pandas as pd
import os
import glob 
import sys

# Pull cohort information
outdir = "data/map-id-file"
chr = sys.argv[1]
cohort = sys.argv[2]

os.makedirs(f"{outdir}/{cohort}",exist_ok = True)
file_path = os.path.join("data", "snpstats", cohort, f"chr{chr}.snpstats")
filename = file_path.split('/')[3]
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
final.to_csv(f"{outdir}/{cohort}/chr{chr}.mapid", sep = " ", index = False)

