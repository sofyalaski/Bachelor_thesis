#!/bin/bash

#call from benchmark

for D in *; do
	if [[ ! -f "$D/Ensembl/merge_SJ_all.tsv" ]]; then
		echo "no merged exons"
	elif [[ ! -f "$D/thoraxe/s_exon_table.csv" ]]; then
		echo "no s-exon table!"
	else
		echo "$D"
		ipython /home/sofya/Documents/TranscriptAnnotation/rnaseq/code/merge2.py "$D/Ensembl/merge_SJ_all.tsv" "$D/thoraxe/s_exon_table.csv"
	fi
done
