
## Bachelor Thesis folder

####The structure of benchmark folder on the example of TPM1
```
TPM1
├── Ensembl
│   ├── exonstable.tsv
│   ├── exonstable_chr.tsv
│   ├── sequences.fasta
│   ├── tree.nh
│   └── tsl.csv
└── thoraxe
    ├── _intermediate
    │   ├── chimeric_alignment_1.fasta
    │   ⋮
    │   ├── cluster_data.js
    │   ├── cluster_plots.html
    │   ├── gene_ids_1.txt
    │   ⋮
    │   ├── msa_matrix_1.txt
    │   ⋮
    │   ├── subexon_table.csv
    │   ├── subexon_table_1.csv
    │   ⋮
    │   └── transcript_table.csv
    ├── s_exon_table.csv
    ├── msa
    │   ├── msa_homologous_exon_10_0.fasta
    │   ⋮
    │   └── msa_homologous_exon_9_0.fasta
    ├── phylosofs
    │   ├── homologous_exons.tsv
    │   ├── transcripts.pir
    │   ├── transcripts.txt
    │   └── tree.nh
    └── splice_graph.gml
```

####The structure of analysis folder on the example of TPM1
```
TPM1
├── rnaseq
│   ├── ase_rnaseq.tsv
│   ├── ase_rissue.tsv
│   ├── ase_rissue_groupped.tsv
|   ├── both_CytoscapeSession.cys
|   ├── both_splice_graphs.gml
|   ├── merge_homologs_all.tsv
|   ├── merge_homologs_norm_counts.tsv
|   ├── merge_SJ_all.tsv
|   ├── rnaseq_CytoscapeSession.cys
|   ├── rnaseq_splice_graph.gml
|   ├── tissue_counts_all.tsv
│   └── tissue_counts_multiple.tsv
├── plots
│   ├── both_splice_graphs.pdf
│   ├── rnaseq_splice_graph.pdf
│   ├── splice_graph.pdf
│   ├── heatmap_both.pdf
├── seqlogos
│   ├── msa_homologous_s_exon_1_0.eps
│   ⋮
│   └── msa_homologous_s_exon_17_0.eps
├── struct(if present)
    └── annotated.pdf
├── ase_list_new.txt
├── ase_list_detailed.txt
├── psi_histogram.pdf
└── ra_histogram.pdf

  
```

* *benchmark* directory contains annotation of exons from ENSEMBL, including .fasta files and output of ThorAxe, includinf assigned s-exons.
* *RNASeqInfos* folder contains file with information about experiments and libraries.
* *analysis* directory contains all outputs of my work for each protein. Plots subdirectory contains all images and rnaseq subdirectoey contains tabular files. 
* *code* directory includes all used scripts

## Scripts
* chr_table.sh runs chromosomes.py:  Adds chromosome number ro ENSEMBL annotation of exons from fasta files. 
  * outputs exonstable_chr.tsv*
* merge1_all.py (step 2.2.1.1):    Combining Ensembl annotation with SJ information from RNA-Seq.
  * outputs merge_SJ_all.tsv
* merge2.py  (step 2.2.1.2):    Assigning of orthologous exon IDs to exon-SJ pairs, mergtissuee.sh runs it .
  * outputs merhe_homologs_all.tsv
* filter_sj.py (step 2.2.1.3): Computes total normalised number of uniquely mapped reads per SJ.
  * outputs merge_homologs_norm_counts.tsv
* count_hist.R : Plot histogram of all normalised SJ
  * outputs ra_histogram.pdf
* tissue.py calculates normalised number of uniquely mapped counts per experiment per tissue.
  * outputs tissue_counts_all.tsv
* gmls.sh runs write_gml.py and write_both_gmls.py, which convert table of SJ with assigned orthologous s-exons to gml gile to further plot it with Cytoscape
  * outputs both_splice_graphs.gml and rnaseq_splice_graph.pdf
* plot_splice_graph.R files: Automatisation files for Cytoscape to plot splice graph for all set of genes at once.
  * outputs both_splice_graphs.pdf, rnaseq_splice_graph.pdf, both_CytoscapeSession.cys and rnaseq_CytoscapeSession.cys
* AS_events.py was needed, as we rerun ThorAxe at some point and IDs of s-exons have change relative to the last version. That is list of conserved ASE in assigned data must have been renewed as well. this code does it.(assigns new s-exons IDs to events).
  * outputs ase_list_new.txt
* number_species_pro_path.py reads list of conserved ASE,finds ASEs on that exon and checks which and how many transcripts express such events, also checks how many species also express an ASE in experimental data.
  * outputs ase_list_detailed.tsv
* Check_node.py does similar job as the above one, but it checks every s-exon expressed in RNA-Seq data, if it a first s-exon to start a chain of ASE. Then also calculates number of species, ASE and its' paths are expressed in, then checks if ASE was annotated, if yes, checks in which transcripts. Also calculates value of each present path, by averaging  normalised mapped count of all  SJs in path.
  outputs ase_rnaseq.tsv
* psi_path.py calculates tissue-specific values of normalised mapped counts of all SJs in terms of PSI and plots heatmap. 
  * outputs ase_tissue_groupped.tsv and heatmaps
