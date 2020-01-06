#!/bin/bash

#call from /TranscriptAnnptation/analysis

for D in *; do
	if [[ ! -f "$D/rnaseq/merge_homologs_norm_counts.tsv" ]]; then
		echo "no merged exons"
	elif [[ ! -f "$D/../../benchmark/$D/thoraxe/splice_graph.gml" ]]; then
		echo "no gml file"
	else
		echo "$D"
		python3 /home/sofya/Documents/TranscriptAnnotation/rnaseq/code/write_gml.py "$D/rnaseq/merge_homologs_norm_counts.tsv" "$D/rnaseq/rnaseq_splice_graph.gml" "$D"
		python3 /home/sofya/Documents/TranscriptAnnotation/rnaseq/code/write_both_gmls.py "$D/rnaseq/merge_homologs_norm_counts.tsv" "$D/../../benchmark/$D/thoraxe/splice_graph.gml" "$D" "$D/rnaseq/both_splice_graphs.gml"
	
	fi
done
