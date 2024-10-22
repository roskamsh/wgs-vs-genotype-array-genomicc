#!/bin/bash
#SBATCH --job-name=findimputed
#SBATCH --output=logs/findimputed.%A.%a.out
#SBATCH --error=logs/findimputed.%A.%a.err
#SBATCH --time=1:00:00
#SBATCH --ntasks=1
#SBATCH --mem=20G
#SBATCH --array=1-22

export PATH=$PATH:/home/u036/u036/shared/bin

# Activate /home/u036/u036-genomicc/shared/workspace/roskamsh/envs/bgen_env before submission

## Options for wgs
# COHORT genomicc-wgs

## Options for genotype-array
# COHORT genomicc-genotype-array

COHORT=$1
OUTPUTDIR=data/imputed-snps/${COHORT}

# Make output directory
mkdir -p ${OUTPUTDIR}

# Run python script
python identify-imputed-snps.py ${SLURM_ARRAY_TASK_ID} ${COHORT}

