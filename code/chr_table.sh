#!/bin/bash

#call from rnaseq

for D in *; do
	if [[ ! -f "$D/Ensembl/sequences.fasta" ]]; then
		echo "no sequences.fasta"
	elif [[ ! -f "$D/Ensembl/exonstable.tsv" ]]; then
		echo "no exonstable.tsv"
	else
		echo "$D"
		python3 /home/sofya/Documents/TranscriptAnnotation/rnaseq/code/chromosomes.py "$D/Ensembl/sequences.fasta" "$D" "$D/Ensembl/exonstable.tsv"
	fi
done
