#!/bin/bash
#SBATCH --job-name=recodesnps
#SBATCH --output=logs/recodesnps.%A.%a.out
#SBATCH --error=logs/recodesnps.%A.%a.err
#SBATCH --time=36:00:00
#SBATCH --ntasks=1
#SBATCH --mem=64G
#SBATCH --array=1-22

export PATH=$PATH:/home/u036/u036/shared/bin

# Activate /home/u036/u036-genomicc/shared/workspace/roskamsh/envs/bgen_env before submission

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

# Make output directory
mkdir -p ${OUTPUTDIR}

python generate-map-file.py ${SLURM_ARRAY_TASK_ID} ${COHORT}

qctool_v2.2.0 -g ${BGENDIR}/${PREFIX}${SLURM_ARRAY_TASK_ID}.bgen -s ${BGENDIR}/${PREFIX}${SLURM_ARRAY_TASK_ID}.sample -map-id-data data/map-id-file/${COHORT}/chr${SLURM_ARRAY_TASK_ID}.mapid -og ${OUTPUTDIR}/${COHORT}-chr${SLURM_ARRAY_TASK_ID}.bgen 

cp ${BGENDIR}/${PREFIX}${SLURM_ARRAY_TASK_ID}.sample ${OUTPUTDIR}/${COHORT}-chr${SLURM_ARRAY_TASK_ID}.sample

bgenix -g ${OUTPUTDIR}/${COHORT}-chr${SLURM_ARRAY_TASK_ID}.bgen -index

