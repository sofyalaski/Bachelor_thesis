import pandas as pd
import numpy as np
import sys
import os
#usage  ipython /home/sofya/Documents/TranscriptAnnotation/rnaseq/code/tissue.py /home/sofya/Documents/TranscriptAnnotation/benchmark table_with_experiments table_with_libraries




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

    def read_index(st):
        return table2[table2.Run_IDs.str.contains(st)].index[0]


    #get rid of columns that are not important at thos stage
    table2 = table2[['Species','Experiment_ID','Library_ID','Anatomical_entity_name','Mapped_read_count','Run_IDs']]  
    tissue_specific_counts = list(set(table2.Anatomical_entity_name))
    tissue_specific_counts.sort()  
    for gene in genes:
        print(gene, genes.index(gene)+1,'/',len(genes))
        file = '/home/sofya/Documents/TranscriptAnnotation/analysis/'+gene+'/rnaseq/merge_homologs_norm_counts.tsv'
        to_file = file[:-30]+'tissue_counts_all.tsv'
        to_file_m = file[:-30]+'tissue_counts_multiple.tsv'
        if os.path.isfile(file):# add not to only produce tables for missing files
            exonstable = pd.read_csv(file, sep = '\t',dtype = {"Species": 'object',"GeneID": 'object',"TranscriptIDCluster": 'object',"ExonIDCluster": 'object',
                "SubexonIDCluster": 'object',"S_exonID": 'object',"S_exon_CodingStart": 'int64',"S_exon_CodingEnd": 'int64',"chr": 'object',"start": 'object',
                "end": 'object',"strand":'object',"motif": 'object',"total_uq": 'object',"total_mm": 'object',"ave_uq": 'float64',"num_exp": 'object',"name_exp": 'object',"uq_per_exp": 'object',"mm_per_exp": 'object'})
        

            #exonstable = pd.read_csv('/home/sofya/Documents/TranscriptAnnotation/benchmark/SRC/Ensembl/merge_homologs_all.tsv',sep = '\t')
            #columns of interest
            exonstable = exonstable[['Species','TranscriptIDCluster_5p', 'ExonIDCluster_5p','S_exonID_5p','TranscriptIDCluster_3p', 'ExonIDCluster_3p','S_exonID_3p','start', 'end', 'strand', 'motif', 'total_uq', 'total_mm', 'ave_uq', 'num_exp', 'name_exp', 'uq_per_exp', 'mm_per_exp']]     

            exonstable = exonstable.assign(name_exp = pd.Series([[] if pd.isnull(exonstable.name_exp.iloc[i]) else (exonstable.name_exp.iloc[i].split(',')) for i in range(len(exonstable))])) 
            exonstable = exonstable.assign(uq_per_exp = pd.Series([[] if pd.isnull(exonstable.uq_per_exp.iloc[i]) else (exonstable.uq_per_exp.iloc[i].split(',')) for i in range(len(exonstable))]))
            exonstable = exonstable.assign(mm_per_exp = pd.Series([[] if pd.isnull(exonstable.mm_per_exp.iloc[i]) else (exonstable.mm_per_exp.iloc[i].split(',')) for i in range(len(exonstable))]))

            output_unique = pd.DataFrame(columns = ['TranscriptIDCluster_5p', 'ExonIDCluster_5p','S_exonID_5p','TranscriptIDCluster_3p', 'ExonIDCluster_3p','S_exonID_3p','Species','n_lib','Experiment_ID']+tissue_specific_counts,index= [])
            output_multiple = pd.DataFrame(columns = ['TranscriptIDCluster_5p', 'ExonIDCluster_5p','S_exonID_5p','TranscriptIDCluster_3p', 'ExonIDCluster_3p','S_exonID_3p','Species','n_lib','Experiment_ID']+tissue_specific_counts,index= [])
            
            for junction in range(len(exonstable)):
                if  pd.isnull(exonstable.total_uq.iloc[junction]):#exclude annotated exons that have no rna-seq evidence that binds them on either end
                    continue
                else:
                    name_j = exonstable.name_exp.iloc[junction]
                    uq_j = [int(val) for val in exonstable.uq_per_exp.iloc[junction]]
                    mm_j = [int(val) for val in exonstable.mm_per_exp.iloc[junction]]
                    one_j = pd.DataFrame(dict({'Run_IDs':name_j,'uq_per_exp':uq_j,'mm_per_exp':mm_j}), index = range(len(name_j))) 
                
                    table2_index = one_j.Run_IDs.apply(read_index).tolist()

                    to_concat = table2.iloc[table2_index][table2.columns[0:-1]].reset_index(drop = True)
                    intersect = pd.concat([one_j,to_concat],axis = 1,sort = False)  
                    intersect = intersect.assign(n_uq = intersect.uq_per_exp/intersect.Mapped_read_count, n_mm = intersect.mm_per_exp/intersect.Mapped_read_count)  

                    n_lib = len(set([i for i in intersect.Library_ID if not pd.isnull(i)]))  
                    n_exp = len(set([i for i in intersect.Experiment_ID if not pd.isnull(i)]))  

                    #norm_counts = intersect.groupby('Anatomical_entity_name').sum()   
                    norm_counts = intersect.groupby(['Experiment_ID','Anatomical_entity_name']).mean()

                    #norm_counts_table = pd.Series(norm_counts.uq_per_exp.div(norm_counts.Mapped_read_count))#normalize
                    #norm_counts_table.index.get_level_values(level=1) 
                    #norm_counts_table = pd.Series(norm_counts_table.tolist(), index= new_index)  
                    experiments =list(set(norm_counts.index.get_level_values(level=0))) 
                    for i in experiments:
                        info_add = pd.Series(dict({'TranscriptIDCluster_5p':exonstable.iloc[junction].TranscriptIDCluster_5p, 
                                                    'ExonIDCluster_5p':exonstable.iloc[junction].ExonIDCluster_5p,
                                                    'S_exonID_5p':exonstable.iloc[junction].S_exonID_5p,
                                                    'TranscriptIDCluster_3p':exonstable.iloc[junction].TranscriptIDCluster_3p,
                                                    'ExonIDCluster_3p':exonstable.iloc[junction].ExonIDCluster_3p,
                                                    'S_exonID_3p':exonstable.iloc[junction].S_exonID_3p,
                                                    'Species':exonstable.iloc[junction].Species,
                                                    'n_lib':n_lib,
                                                    'Experiment_ID':i}))     
                        output_unique = output_unique.append(info_add.append(norm_counts.n_uq.loc[i]),sort = False, ignore_index = True) 
                        output_multiple = output_multiple.append(info_add.append(norm_counts.n_mm.loc[i]),sort = False, ignore_index = True) 
            output_unique.to_csv(to_file, sep='\t', index = False, header = True)
            output_multiple.to_csv(to_file_m, sep='\t', index = False, header = True)



if __name__=='__main__':
    main()
