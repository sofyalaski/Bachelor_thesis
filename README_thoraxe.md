# Transcript Annotation  

This repo has two main folders: `benchmark` and `analysis`:  

## Benchmark folder  

The `benchmark` folder has the raw output of *ThorAxe* for each protein in
the benchmark set. Inside `benchmark` there is a folder for each protein,
e.g. `PAX6`:

```
PAX6
├── Ensembl
│   ├── exonstable.tsv
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
    ├── homologous_exon_table.csv
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

For each protein, the `Ensembl` folder has the data downloaded from Ensembl
with `transcript_query`. The `thoraxe` folder as the raw output from `thoraxe`.

### thoraxe

The `homologous_exon_table.csv` file has the tidy (denormalized) output data for
homologous exons. Each row is an observation of a homologous exon in a
particular transcript. Rows are in order, following the homologous exon rank.
That means that the concatenation of the homologous exon sequence for each
transcript gives the protein isoform sequence.  

The `splice_graph.gml` is the splice graph of homologous exons in all the
transcripts/species using the human-readable Graph Modelling Language (GML)
format. Each node and edge has conservation information, where conservation
means the fraction of species showing that particular node (homologous exon) or
connection.

The `msa` folder has a multiple sequence alignment for each homologous exon, e.g.
`msa_homologous_exon_10_0.fasta`. This MSAs can be easily used as a seed to
look for homologous sequences in different databases by using
[hmmsearch](https://www.ebi.ac.uk/Tools/hmmer/search/hmmsearch).

#### phylosofs

The `phylosofs` folder has the needed inputs for the structural and mollecular
modelling pipelines of *PhyloSofS*. In particular, these files use a single
unicode character to represent each homologous exon. The mapping between the id
for *PhyloSofS* and the one of *ThorAxe* (*ExonCluster*_*ChimericBlock*) is in
the `homologous_exons.tsv` file.  

The `transcripts.pir` has the annotated sequence using the PIR format.

The list of transcripts for each gene is in `transcripts.txt`

#### Intermediate outputs

The `_intermediate` folder has intermediate files and states from the *ThorAxe*
pipeline. In particular, `cluster_plots.html` has the interactive plots of the
chimeric alignments, with the possibility to show the `constitutive` value
calculated for each subexon as described in previous issues of this repo.

### How to run the benchmark?

The are two main scripts to run *ThorAxe* in the benchmark set of proteins.
They were written to use the multiple cores of the new machine running windows
by exploiting the fact that the benchmark dataset is a fixed list of genes
stored in `benchmark_list.txt`.

`benchmark/download_data.jl` runs sequentially because it is not possible to
download data from Ensembl in parallel.

Once the data is downloaded, you can run `benchmark/throw_thoraxe.jl` in
parallel, e.g. to use 4 cores:

 ```bash
 julia -p 4 throw_thoraxe.jl
 ```

The script uses `-a 'wsl clustalo'` to run *clustalo* (it runs in parallel)
using the Windows Subsystem for Linux.  

Both scripts save `stderr` and `stdout` in files inside `benchmark/logfiles`.

Deleting previous data (protein folders and files inside logfiles) before
running the full benchmarks again could be a safe option to avoid residual
files that are no longer needed and avoid confusions. Checking for errors in
the logfiles is recommended.

### To add a particular protein?

To add or update information about a particular protein, you can use
`benchmark/run_single_protein_benchmark.jl`
You should also add the protein into the `benchmark_list.txt` to not lose it
in following updates.

## Analysis folder

The `analysis` folder uses the raw `thoraxe` outputs to generate other outputs
that can help us in the analysis of each protein. There is also a folder for
each protein in the benchmark set, e.g. PAX6:

```
PAX6
├── 02_Transcript_clustering.html
├── 02_Transcript_clustering.ipynb
├── 03_Stats.html
├── 03_Stats.ipynb
├── CytoscapeSession.cys
├── seqlogos
│   ├── msa_homologous_exon_10_0_logo.eps
│   ⋮
│   └── msa_homologous_exon_9_0_logo.eps
└── splice_graph.pdf
```

`splice_graph.pdf` has an automated visualization of the splice graph using the
*Cytoscape* style `default_0` defined in `benchmark/styles.xml`. The session
used to save the *PDF* file is in `CytoscapeSession.cys`. You can use that
session to play with the graph on *Cytoscape* and apply the *yFiles* hierarchical
layout if you want (because *yFiles* layouts are not accessible from the
programmatic interface).

The `seqlogos` folder has a sequence logo in `eps` format for each homologous exon MSA.  

The `.ipynb` files have the jupyter notebooks with the code to execute using
`Jupyter` and `Julia`. The `.html` files are static sites, with the same content
that the jupyter files, that you can visualize in the web browser:

 - `02_Transcript_clustering.html` has a heatmap of transcripts vs homologous exons. Also, it has a clustering of transcripts.  
 - `03_Stats.html` has basic statistics about the number of transcripts, homologous exons, etc.

### How to run the analysis for the benchmark?

Recommendations about cleaning up the protein and `logfiles` folders are
similar to the ones given before for running the benchmark.

At the moment, we have 3 Julia scripts, to generate the sequence logos and the
Jupyter notebooks, and 1 R script, to plot the splice graph using Cytoscape.
`analysis/run_seqlogo.jl` should run before the others. Then you can run  
`analysis/run_transcript_cluster.jl`, `analysis/run_stats.jl` and
`analysis/SpliceGraph.R`.

### To run the Julia scripts for a particular protein.

You can run `analysis/run_single_protein_analysis.jl` using `julia`.
