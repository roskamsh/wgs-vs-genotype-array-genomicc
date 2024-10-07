#!/bin/bash
#SBATCH --job-name=snpstats
#SBATCH --output=logs/snpstats.%A.%a.out
#SBATCH --error=logs/snpstats.%A.%a.err
#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH --mem=64G
#SBATCH --array=1-22

QCTOOL=/home/u036/u036-genomicc/shared/workspace/roskamsh/data/wgs-genomicc-imputed/bgen
PATH=$PATH:$HOME/.local/bin:$HOME/bin:$BIN:$QCTOOL

INPUTDIR=
OUTPUTDIR=snpstats/genomicc-wgs

qctool -g ${INPUTDIR}/wgs-genomicc-chr${SLURM_ARRAY_TASK_ID}.bgen -s ${INPUTDIR}/wgs-genomicc-chr${SLURM_ARRAY_TASK_ID}.sample -snp-stats -osnp ${OUTPUTDIR}/chr${SLURM_ARRAY_TASK_ID}.snpstats
