# Subset for small region & samples
vcftools --vcf data/vcf/genomicc-genotype-array/genomicc_chr22.vcf 
	 --chr chr22 
	 --from-bp 15000000
	 --to-bp 17000000 
	 --max-indv 10
	 --recode
	 --out chr22_subsample


