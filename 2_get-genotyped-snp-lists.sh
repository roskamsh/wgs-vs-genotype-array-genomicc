#!/usr/bin/env bash

INPUTDIR=/home/u036/u036-genomicc/shared/workspace/roskamsh/data/wgs-genomicc-imputed/bed-bim-fam
BIMFILE=merged.mild.QCimputation.bim 

cat ${INPUTDIR}/${BIMFILE} | while read line; do chr=$( echo $line | cut -d ' ' -f 1); pos=$( echo $line | cut -d ' ' -f 4 ); alleleA=$( echo $line | cut -d ' ' -f 5 ); alleleB=$( echo $line | cut -d ' ' -f 6 ); echo "$chr:$pos:$alleleA:$alleleB $chr $pos $alleleA $alleleB"; done > data/genotyped-snps-hg38.txt

