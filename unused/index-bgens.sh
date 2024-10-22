#!/bin/bash
#SBATCH --job-name=index
#SBATCH --output=logs/index.%A.%a.out
#SBATCH --error=logs/index.%A.%a.err
#SBATCH --time=1:00:00
#SBATCH --ntasks=1
#SBATCH --mem=25G
#SBATCH --array=1-22

export PATH=$PATH:/home/u036/u036/shared/bin

## Options for wgs
# BGENDIR /home/u036/u036-genomicc/shared/workspace/roskamsh/data/wgs-genomicc-imputed/bgen
# COHORT genomicc-wgs
# PREFIX wgs-genomicc-chr

## Options for genotype-array
# BGENDIR /home/u036/u036-genomicc/shared/workspace/roskamsh/data/genomicc-genotype-array/imputed/genomic-isaric 
# COHORT genomicc-genotype-array
# PREFIX GenOMICC_ISARIC_chr 

BGENDIR=$1
COHORT=$2
PREFIX=$3
OUTPUTDIR=data/bgen-recoded/${COHORT}

cp ${BGENDIR}/${PREFIX}${SLURM_ARRAY_TASK_ID}.sample ${OUTPUTDIR}/${COHORT}-chr${SLURM_ARRAY_TASK_ID}.sample

bgenix -g ${OUTPUTDIR}/${COHORT}-chr${SLURM_ARRAY_TASK_ID}.bgen -index

