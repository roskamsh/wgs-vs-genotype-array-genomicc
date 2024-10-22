#!/bin/bash
#SBATCH --job-name=bgen2bed
#SBATCH --output=logs/bgen2bed.%A.%a.out
#SBATCH --error=logs/bgen2bed.%A.%a.err
#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH --mem=64G
#SBATCH --array=1-22

export PATH=$PATH:/home/u036/u036/shared/bin

## Options for wgs
# COHORT genomicc-wgs

## Options for genotype-array
# COHORT genomicc-genotype-array

COHORT=$1
IMPUTED_SNPS_DIR=data/imputed-snps/${COHORT}
BGENDIR=data/bgen-recoded/${COHORT}
OUTPUTDIR=data/bedfiles/${COHORT}

# Make output directory
mkdir -p ${OUTPUTDIR}

qctool_v2.2.0  -g ${BGENDIR}/${COHORT}-chr${SLURM_ARRAY_TASK_ID}.bgen \
	       -s ${BGENDIR}/${COHORT}-chr${SLURM_ARRAY_TASK_ID}.sample \
	       -excl-rsids ${IMPUTED_SNPS_DIR}/chr${SLURM_ARRAY_TASK_ID}_imputed_rsids.txt \
               -og "${OUTPUTDIR}/genomicc_chr${SLURM_ARRAY_TASK_ID}.bed"
