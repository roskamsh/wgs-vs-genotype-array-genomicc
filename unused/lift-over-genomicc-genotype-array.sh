#!/bin/sh
# Grid Engine options (lines prefixed with #$)
#$ -N liftover
#$ -cwd 
#$ -l h_rt=24:00:00
#$ -l h_vmem=155G
#$ -e logs/lift.over.$SGE_TASK_ID.err
#$ -o logs/lift.over.$SGE_TASK_ID.out
#  These options are:
#  job name: -N
#  use the current working directory: -cwd
#  runtime limit of 10 minutes: -l h_rt
#  memory limit of 10 Gbyte: -l h_vmem

. /etc/profile.d/modules.sh
module load igmm/apps/picard/2.25.4

i=$SGE_TASK_ID
INPUTDIR=vcf_b37
OUTPUTDIR=vcf_b38

picard LiftoverVcf I=${INPUTDIR}/GenOMICC-b37-no-indels-chr$i\.vcf  O=${OUTPUTDIR}/GenOMICC-b38-chr$i\.vcf CHAIN=GRCh37_to_GRCh38.chain.gz REJECT=${OUTPUTDIR}/rejected_variants/rejected_variants$i\.vcf R=GRCh38/Homo_sapiens.GRCh38.dna.toplevel.fa WARN_ON_MISSING_CONTIG=true MAX_RECORDS_IN_RAM=25000 TMP_DIR=./tmpvcf
