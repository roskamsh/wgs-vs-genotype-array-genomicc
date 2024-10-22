import pandas as pd

mapfile = pd.read_csv("../../../data/wgs-genomicc-imputed/imputed_wgs_pheno_for_BRH.csv")
sample_file = pd.read_csv("/home/u036/u036-genomicc/shared/workspace/roskamsh/data/wgs-genomicc-imputed/bgen/wgs-genomicc-chr11.sample", sep = " ")

# Identify which sample IDs are in both the phenotype file and the sample_file
common_ids = pd.Series(list(set(mapfile['platekey_id']).intersection(set(sample_file['ID_1']))))

# Only 16,479 common IDs between the two of these... what has happened to these sample IDs that are not in the common_ids?
distinct_values_mapfile = pd.Series(list(set(mapfile['platekey_id']).difference(set(sample_file['ID_1']))))
distinct_values_samplefile  = pd.Series(list(set(sample_file['ID_1']).difference(set(mapfile['platekey_id']))))

# It looks as though the samplefile includes some sample IDs labeled as so: GCC60369_GCC60369
# Do these GCC IDs have corresponding platekeys in the mapfile that might account for this discrepancy?
distinct_values_split = distinct_values_samplefile.str.split('_').str[0]
gcc_ids = distinct_values_split[distinct_values_split.str.startswith('GCC')].tolist()
platekey_ids = distinct_values_samplefile[distinct_values_samplefile.str.startswith('LP')].tolist()

# Do these add up to the expected number?
len(common_ids) + len(gcc_ids) + len(platekey_ids) == sample_file.shape[0] - 1

# Now check if we can map the GCC IDs in gcc_ids to a value in mapfile
subset_mapfile = mapfile[mapfile['genomicc_id'].isin(gcc_ids)].copy()
# they do
missing_platekey_ids = subset_mapfile['platekey_id'].tolist()
# Are these the same as the distinct_values_mapfile?
intersection = pd.Series(list(set(distinct_values_mapfile.tolist()).intersection(set(missing_platekey_ids))))
# This is an exact intersection with the missing_platekey_ids

# Create 1:1 mapping of whatever ID is in the samplefile --> genomicc_id in the mapfile
# 16,479 of these IDs correspond to the platekey_id column
# 5,921 of these are already the GCC id, but have been changed s.t. they are GCCID_GCCID
# 136 of these are not in the mapfile, but are platekey_ids
# create a new column in samplefile, that: (1) checks if the value is in common_ids
# (2) checks if the value starts with GCC
# (3) otherwise is not in mapfile and therefore can be assigned as the original samplefile naming, but write these missing platekey_ids to a separate file
# List to store values that do not match conditions
unmatched_values = []

# Function to apply conditions
def get_genomicc_id(value, common_ids, unmatched_values):
# 1. If value is in common_ids, find corresponding GCC_ID and convert to lowercase
    if value in common_ids.values:
        matching_row = mapfile[mapfile['platekey_id'] == value]
        return matching_row['genomicc_id'].values[0]
    # 2. If value starts with 'GCC', split by "_" to return ID only, and convert to lowercase
    elif value.startswith('GCC'):
        return value.split('_')[0]
    # 3. Otherwise, return the same value and save it to unmatched_values
    else:
        unmatched_values.append(value)
        return value

# Apply the function to the column 'genomicc_id' and create a new column 'processed_id'
sample_file['genomicc_id'] = sample_file['ID_1'].apply(lambda x: get_genomicc_id(x, common_ids, unmatched_values))

new_sample_file = pd.DataFrame({
                    'ID_1': sample_file['genomicc_id'],
                    'ID_2': sample_file['genomicc_id'],
                    'missing': sample_file['missing']
                    })

new_sample_file.to_csv("data/bgen_recoded/genomicc-wgs/wgs-genomicc-chr11.sample", delim = " ", index = False)

# Now add BGEN sample ID that corresponds to each row in the mapfile
# use new information contained in sample_file to match the genomicc IDs between these two
all_match = pd.Series(list(set(sample_file['genomicc_id']).intersection(set(mapfile['genomicc_id']))))
len(all_match) == mapfile.shape[0] # yep

def get_bgen_id(value):
    matching_row = sample_file[sample_file['genomicc_id'] == value]
    return matching_row['ID_1'].values[0]

mapfile['bgen_id'] = mapfile['genomicc_id'].apply(lambda x: get_bgen_id(x))


