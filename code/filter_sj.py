import pandas as pd
import numpy as np
import sys
import os

# ipython /home/sofya/Documents/TranscriptAnnotation/rnaseq/code/filter_sj.py /home/sofya/Documents/TranscriptAnnotation/benchmark /home/sofya/Documents/TranscriptAnnotation/rnaseq/RNAseqInfos/Bgee_RNA-Seq_all_libraries.csv 



def main():
    f = open('/home/sofya/Documents/TranscriptAnnotation/benchmark_list.txt','r')    
    genes = f.read()
    f.close()
    genes =genes.split('\n')  
    genes = [i for i in genes if i!=''] 


    table2 = pd.read_csv(sys.argv[1],sep = ',')
    #table2 = pd.read_csv('/home/sofya/Documents/TranscriptAnnotation/rnaseq/RNAseqInfos/Bgee_RNA-Seq_all_libraries.csv',sep = ',')
    table2=table2.assign(species = pd.Series(table2.species.str.lower()))  
    table2 = table2.rename(columns={'species':'Species','Experiment ID':'Experiment_ID','Library ID':'Library_ID','Anatomical entity name':'Anatomical_entity_name','Mapped read count':'Mapped_read_count','Run IDs':'Run_IDs'})
    table2 = table2[['Species','Experiment_ID','Library_ID','Anatomical_entity_name','Mapped_read_count','Run_IDs']]  

    def read_index(st):
        return table2[table2.Run_IDs.str.contains(st)].index[0]

    def get_norm_uq(row):
        if pd.isnull(row.name_exp):
            return 0
        names = row.name_exp.split(',')
        uqs = list(map(int,row.uq_per_exp.split(',')))
        mapped_counts = [table2.iloc[read_index(i)].Mapped_read_count for i in names]
        normalized = np.divide(uqs,mapped_counts)   
        return sum(normalized)

    def get_norm_mm(row):
        if pd.isnull(row.name_exp):
            return 0
        names = row.name_exp.split(',')
        mms = list(map(int,row.mm_per_exp.split(',')))
        mapped_counts = [table2.iloc[read_index(i)].Mapped_read_count for i in names]
        normalized = np.divide(mms,mapped_counts)   
        return sum(normalized)

    for gene in genes:
        print(gene, genes.index(gene)+1,'/',len(genes))
        homologs  = pd.read_csv('/home/sofya/Documents/TranscriptAnnotation/benchmark/'+gene+'/thoraxe/s_exon_table.csv',sep = ',', index_col = 0)  
        #exonstable = pd.read_csv('/home/sofya/Documents/TranscriptAnnotation/benchmark/'+gene+'/Ensembl/merge_homologs_all.tsv', sep = '\t', dtype = {0:"object",1:"object",2:"object",3:"int64",4:"object",5:"int64",6:"int64",7:"int64",8:"float64",9:"float64",10:"float64",11:"float64",12:"int64",13:"int64",14:"object"})
        file = '/home/sofya/Documents/TranscriptAnnotation/analysis/'+gene+'/rnaseq/junction_exclusions.tsv'
        exonstable = pd.read_csv(file, sep = '\t',dtype = {"Species": 'object',"GeneID": 'object',"TranscriptIDCluster": 'object',"ExonIDCluster": 'object',
                "SubexonIDCluster": 'object',"S_exonID": 'object',"S_exon_CodingStart": 'int64',"S_exon_CodingEnd": 'int64',"chr": 'object',"start": 'object',
                "end": 'object',"strand":'object',"motif": 'object',"total_uq": 'object',"total_mm": 'object',"ave_uq": 'float64',"num_exp": 'object',"name_exp": 'object',"uq_per_exp": 'object',"mm_per_exp": 'object'})
        

        exonstable = exonstable.assign(n_total_uq = pd.Series(exonstable.apply(get_norm_uq,axis=1), index = exonstable.index))
        exonstable = exonstable.assign(n_total_mm = pd.Series(exonstable.apply(get_norm_mm,axis=1), index = exonstable.index))
        #output = exonstable[exonstable.n_total_uq>1.7e-07] 
        to_file = file[:-4] + '_norm_counts.tsv'
        exonstable.to_csv(to_file, sep='\t', index = False, header = True)

if __name__=='__main__':
    main()
