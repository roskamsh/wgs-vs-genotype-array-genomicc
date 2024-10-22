#!/bin/bash
#SBATCH --job-name=snpstats
#SBATCH --output=logs/bgen2vcf.%A.%a.out
#SBATCH --error=logs/bgen2vcf.%A.%a.err
#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH --mem=64G
#SBATCH --array=1-22

export PATH=$PATH:/home/u036/u036/shared/bin

## Options for wgs
# BGENDIR /home/u036/u036-genomicc/shared/workspace/roskamsh/data/wgs-genomicc-imputed/bgen
# COHORT wgs-genomicc
# PREFIX wgs-genomicc-chr

## Options for genotype-array
# BGENDIR /home/u036/u036-genomicc/shared/workspace/roskamsh/data/genomicc-genotype-array/imputed/genomic-isaric 
# COHORT genomicc-genotype-array
# PREFIX GenOMICC_ISARIC_chr 

BGENDIR=$1
COHORT=$2
PREFIX=$3
OUTPUTDIR=data/vcf/${COHORT}

# Make output directory
mkdir -p ${OUTPUTDIR}

qctool_v2.2.0 -g ${BGENDIR}/${PREFIX}${SLURM_ARRAY_TASK_ID}.bgen -s ${BGENDIR}/${PREFIX}${SLURM_ARRAY_TASK_ID}.sample -og ${OUTPUTDIR}/genomicc_chr${SLURM_ARRAY_TASK_ID}.vcf
