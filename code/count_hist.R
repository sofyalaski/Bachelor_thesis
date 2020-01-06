library(ggplot2)
library(tidyr)
library(dplyr)
library(data.table)

main<- function(file_name,dff){
  file <-file_name #'/home/sofya/Documents/TranscriptAnnotation/benchmark/BCL2L1/Ensembl/tissue_counts_all.tsv'
  to_file <- paste(substr(file,1,nchar(file)-21),"plots/histogram_",sep = '')
  tissue_counts <- fread(file,header=TRUE,col.names = c('TranscriptIDCluster_5p', 'ExonIDCluster_5p', 'HomologousExon_5p', 'TranscriptIDCluster_3p', 'ExonIDCluster_3p', 'HomologousExon_3p', 'Species','n_lib','Experiment_ID', "Ammon's_horn", 'CD4-positive_helper_T_cell', 'adipose_tissue', 'adrenal_gland', 'adrenal_tissue', 'adult_mammalian_kidney', 'adult_organism', 'blastula', 'bone_marrow', 'bone_marrow_macrophage', 'bone_tissue', 'brain', 'brown_adipose_tissue', 'cerebellum', 'cerebral_cortex', 'colon', 'corpus_callosum', 'egg_cell', 'embryo', 'embryonic_stem_cell', 'eye', 'female_gonad', 'female_reproductive_system', 'fibroblast', 'frontal_cortex', 'gastrula', 'head', 'head_kidney', 'heart', 'heart_left_ventricle', 'intestine', 'kidney', 'larva', 'leukocyte', 'liver', 'lung', 'lymph_node', 'male_reproductive_system', 'mature_ovarian_follicle', 'mesonephros', 'multi-cellular_organism', 'multi-tissue_structure', 'muscle_of_leg', 'muscle_tissue', 'peripheral_blood_mononuclear_cell', 'pharyngeal_gill', 'pharyngeal_muscle_cell_(C_elegans)', 'placenta', 'prefrontal_cortex', 'prostate_gland', 'rectum', 'skeletal_muscle_tissue', 'spleen', 'stomach', 'tail', 'temporal_lobe', 'testis', 'thoracic_mammary_gland', 'thymus', 'thyroid_gland', 'zone_of_skin'))

  tissue_counts <- data.frame(tissue_counts, check.names = TRUE)
  
  species <- unique(tissue_counts$Species)
  tissue_counts_int <- tissue_counts[7:dim(tissue_counts)[2]]
  tissue_counts_int = subset(tissue_counts_int, select = -c(n_lib) )
  tissue_counts_int = subset(tissue_counts_int, select = -c(multi.cellular_organism,multi.tissue_structure) )
  
    for (i in species){
    print(i)
    specie_counts <- tissue_counts_int[which (tissue_counts_int$Species==i), names(tissue_counts_int) %in% c(names(tissue_counts_int)[2:length(names(tissue_counts_int))])]
    count_nans_columns <- sapply(specie_counts, function(x) sum(is.na(x)))
    expressed_tissues <-names(count_nans_columns[count_nans_columns !=dim(specie_counts)[1]])
    expressed_tissues <- expressed_tissues[2:length(expressed_tissues)]
    df <-(specie_counts[expressed_tissues])

    # if (ncol(df)>2){
    #   ggplot(gather(df[2:dim(df)[2]]), aes(value)) + 
    #     geom_histogram(bins = 10) + 
    #     facet_wrap(~key)+labs(x='normalized tissue counts',y = 'frequency')+ggtitle(paste('Histogram of normalized counts in tissues in ',i,sep = ' '))
    #   ggsave(paste(to_file,i,"tissues",".pdf",sep = ''),width=16,height =9)
    # 
    df_long <- specie_counts[expressed_tissues] %>% gather(tissue, value, expressed_tissues[1:length(expressed_tissues)])
    #   ggplot(df_long, aes(x = value, fill = tissue)) + geom_histogram() + scale_x_log10()+
    #     ggtitle(paste('Histogram of normalized counts in tissues in ',i,sep = ' '))
    #   ggsave(paste(to_file,i,".pdf",sep=''),width=16,height =9)}
    dff<-rbind(dff,df_long)
    }
  return(dff)
}

path <-'/home/sofya/Documents/TranscriptAnnotation/analysis/'
setwd(path)
all_files<- list.files()
dff <- data.frame(tissue=character(),delta_psi  = numeric(0))
for(gene in all_files){
  filepath <- paste(path,gene,'/rnaseq/',sep='')
  if (file.exists(paste(filepath,'tissue_counts_all.tsv',sep =''))){
    dir.create(file.path(paste(filepath, 'plots',sep='')), showWarnings = FALSE)
    filename <- paste(filepath,'tissue_counts_all.tsv',sep='')
    print(filename) 
    dff <- main(filename,dff)
  }
}

ggplot(dff, aes(x = value, fill = tissue)) + geom_histogram() + scale_x_log10(breaks = c(1e-08, 1e-07, 1e-06,1e-05,1e-04,1e-03,1e-02,1e-01))+
   geom_vline(xintercept = 1e-07)+theme(axis.title.x=element_blank(), axis.title.y = element_blank(),legend.title=element_blank(), axis.text = element_text(size=18),legend.text=element_text(size=12))#+ggtitle('Histogram of relative expression in tissues')       
ggsave(paste(path,"ra_histogram.pdf",sep=''),width=16,height =9)

