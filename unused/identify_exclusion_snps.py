import pandas as pd
import numpy as np
import os

cleaned_ids = pd.read_csv("cleanedids.csv")
genotyped_snps = pd.read_csv("/exports/igmm/eddie/ponting-lab/breeshey/data/genomicc/geno/wp5-gwas-r9-genomicc-isaric4c-nodupl-phenoind.bim", 
                                           delim_whitespace=True, header = None)

# Identify match for either genome assembly position
genotyped_snps.columns = ['chr','Illumina_ID','pos_morgans','pos_basepairs','alleleA','alleleB']

# for each CHR, POS, identify whether either allele matches
# Step 1: Merge on chromosome and base pair position
merged_df = pd.merge(cleaned_ids, genotyped_snps, left_on=['CHROM', 'POS'], right_on=['chr', 'pos_basepairs'], how='left')

# Step 2: Create a function to check if alleles match
def alleles_match(row):
    # Check if the alleles are matching (ignoring the order)
    ref_alt_set = {row['REF'], row['ALT']}
    allele_a_b_set = {row['alleleA'], row['alleleB']}
    return ref_alt_set == allele_a_b_set

# Step 3: Apply the function and create a new column 'match'
merged_df['match'] = merged_df.apply(alleles_match, axis=1)
cleaned_genotyped = merged_df[merged_df.match].copy()

# Read in chr snp stats for these
dir = "snpstats/genomicc-genotype-array"
files = os.listdir(dir)
df_list = []
for file in files:
    print(f"Reading in file {file}...")
    chrstats = pd.read_csv(os.path.join(dir, file), delim_whitespace=True, skiprows = 9)
    df_list.append(chrstats)

    # identify exclusion snps
    chr = file.replace(".snpstats","")
    exclusion_snps = chrstats[~chrstats['alternate_ids'].isin(cleaned_genotyped['chrid(38)'])].rsid.tolist()
    rsids = " ".join(exclusion_snps)

    # Write rsids
    with open(f"non-genotyped-snps/{chr}_rsids2exclude.txt", "w") as text_file:
        text_file.write(rsids) 

all_snp_stats = pd.concat(df_list, ignore_index=True)

# Now identify which chrstats are in merged_df filtered
all_snp_stats['in_genotyped_set'] = all_snp_stats['alternate_ids'].isin(cleaned_genotyped['chrid(38)'])
all_snp_stats.to_csv("all_snp_stats.csv", index=False)
