
## Oredering
 benchmark directory contains annotation of exons from ENSEMBL, including .fasta files and output of ThorAxe, includinf assigned s-exons.
 RNASeqInfos folder contains file with information about experiments and libraries.
 analysis directory contains all outputs of my work for each protein. Plots subdirectory contains all images and rnaseq subdirectoey contains tabular files. 
 code directory includes all used scripts

## Scripts
* chr_table.sh runs chromosomes.py which adds chromosome number ro ENSEMBL annotation of exons from fasta files. 
* merge1_all.py step 2.2.1.1    Combining Ensembl annotation with SJ information from RNA-Seq.
* merge2.py  step 2.2.1.2    Assigning of orthologous exon IDs to exon-SJ pairs, mergtissuee.sh runs it .
* filter_sj.py step  Specification of normalised expression level. Computes total normalised number of uniquely mapped reads per SJ.
* count_hist.R plot histogram of all normalised SJ
* tissue.py calculates normalised number of uniquely mapped counts per experiment per tissue.
* gmls.sh runs write_gml.py and write_both_gmls.py, which convert table of SJ with assigned orthologous s-exons to gml gile to further plot it with Cytoscape.
* plot_splice_graph.R files are automatisation files for Cytoscape to plot splice graph for all set of genes at once.
* AS_events.py was needed, as we rerun ThorAxe at some point and IDs of s-exons have change relative to the last version. That is list of conserved ASE in assigned data must have been renewed as well. this code does it.(assigns new s-exons IDs to events.)
* number_species_pro_path.py reads list of conserved ASE,finds ASEs on that exon and checks which and how many transcripts express such events, also checks how many species also express an ASE in experimental data.
* Check_node.py does similar job as the above one, but it checks every s-exon expressed in RNA-Seq data, if it a first s-exon to start a chain of ASE. Then also calculates number of species, ASE and its' paths are expressed in, then checks if ASE was annotated, if yes, checks in which transcripts. Also calculates value of each present path, by averaging  normalised mapped count of all  SJs in path.
* psi_path.py calculates tissue-specific values of normalised mapped counts of all SJs in terms of PSI and plots heatmap. Outputs 
