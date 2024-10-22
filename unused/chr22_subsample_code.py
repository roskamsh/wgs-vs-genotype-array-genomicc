import pandas as pd

vcf_sub = pd.read_csv("chr22_subsample.recode.vcf", skiprows = 2, delim_whitespace = True)
full_samples = pd.read_csv("GenOMICC_ISARIC_chr22.sample", delim_whitespace = True)

subset = list(vcf_sub.columns[9:])
subset_samples = full_samples[full_samples.ID_1.isin(subset)].copy()

# Need to add first line back in (all zeros)
header = full_samples[:1]
out = pd.concat([header,subset_samples], axis=0, ignore_index=True)
out.to_csv("chr22_subsample.sample")


