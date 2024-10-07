#!/bin/sh
# Grid Engine options (lines prefixed with #$)
#$ -N snpstats
#$ -cwd 
#$ -l h_rt=24:00:00
#$ -l h_vmem=64G
#$ -e logs/snpstats.$TASK_ID.err
#$ -o logs/snpstats.$TASK_ID.out
#  These options are:
#  job name: -N
#  use the current working directory: -cwd
#  runtime limit of 10 minutes: -l h_rt
#  memory limit of 10 Gbyte: -l h_vmem

QCTOOL=/exports/igmm/eddie/ponting-lab/breeshey/bin/qctool/qctool_v2.0.8
PATH=$PATH:$HOME/.local/bin:$HOME/bin:$BIN:$QCTOOL

INPUTDIR=/exports/igmm/eddie/ponting-lab/breeshey/data/genomicc/imputed/genomic-isaric
OUTPUTDIR=snpstats/genomicc-genotype-array

qctool -g ${INPUTDIR}/GenOMICC_ISARIC_chr${SGE_TASK_ID}.bgen -s ${INPUTDIR}/GenOMICC_ISARIC_chr${SGE_TASK_ID}.sample -snp-stats -osnp ${OUTPUTDIR}/chr${SGE_TASK_ID}.snpstats
