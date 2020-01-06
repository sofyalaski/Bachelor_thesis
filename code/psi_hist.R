library(ggplot2)
library(tidyr)
library(dplyr)
library(data.table)

main<- function(file_name,df){
  file <-file_name #'/home/sofya/Documents/TranscriptAnnotation/analysis/TPM1/rnaseq/ase_delta_psi.tsv'
  psi_counts <- fread(file,header=TRUE,drop = 'V1')
  
  psi_counts <- data.frame(psi_counts, check.names = TRUE)
  psi_counts <- subset(psi_counts, select = -c(path_1,path_2,group))
  psi_counts$gene = strsplit(file_name,split='/', fixed=TRUE)[[1]][7]
  #psi_counts <- subset(psi_counts, select = -c(Specie))
  df<-rbind(df,psi_counts)
  return (df)
}


path <-'/home/sofya/Documents/TranscriptAnnotation/analysis/'
setwd(path)
all_files<- list.files()
df <- data.frame(tissue=character(),delta_psi  = numeric(0))
for(gene in all_files){
  filepath <- paste(path,gene,'/rnaseq/',sep='')
  if (file.exists(paste(filepath,'ase_delta_psi.tsv',sep =''))){
    filename <- paste(filepath,'ase_delta_psi.tsv',sep='')
    print(filename)
    df <- main(filename,df)
  }
}
ggplot(df, aes(x = abs(delta_psi), fill = tissue,position = "dodge"))+ geom_histogram() +
  scale_x_continuous(breaks = scales::pretty_breaks(n = 10))+
  #ggtitle('Histogram of all delta PSI in tissues')+ geom_vline(xintercept = 0.2)+
  theme(legend.position = c(.87, 1),legend.justification = c("right", "top"), legend.box.just = "right",legend.title=element_blank(),
        legend.box.margin = margin(6, 6, 6, 6),axis.title.x=element_blank(), axis.title.y = element_blank(),axis.text = element_text(size=18),legend.text=element_text(size=18))
ggsave(paste(path,"psi_histogram.pdf",sep=''),width=16,height = 9)
