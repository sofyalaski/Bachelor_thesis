import pandas as pd
import numpy as np
import sys
import os


def modificate_exons(collapsed_list,exonstable): 
    """For each exon value in merge_SJ_exons.tsv change value to collapsed exons if they are collapsed in homologous_exon_tavle.tsv. Pass set of collapsed exons as a list and dataframe to change."""
    for i in range(len(collapsed_list)): 
        temp = collapsed_list[i].split('/') 
        for ex in range(len(temp)):
            exonstable = exonstable.assign(ExonID_5p=pd.Series([collapsed_list[i] if val==temp[ex] else(val) for val in exonstable.ExonID_5p])) 
            exonstable = exonstable.assign(ExonID_3p=pd.Series([collapsed_list[i] if val==temp[ex] else(val) for val in exonstable.ExonID_3p])) 
    return exonstable 



def main():
    #file1 = '/home/sofya/Documents/TranscriptAnnotation/benchmark/SRC/Ensembl/merge_SJ_all.tsv'
    #file2 = '/home/sofya/Documents/TranscriptAnnotation/benchmark/SRC/thoraxe/s_exon_table.csv'
    file1 = sys.argv[1]
    file2 = sys.argv[2]

    

    exonstable = pd.read_csv(file1, sep='\t',dtype = {0:'object',1:'object',2:'object',3:'object',4:'float64',5:'object',6:'float64',7:'float64',8:'float64',
    9:'float64',10:'float64',11:'float64',12:'float64',13:'float64',14:'float64',15:'float64',16:'float64',17:'float64',18:'float64',19:'float64',20:'float64',
    21:'float64',22:'float64',23:'object',24:'object',25:'object',26:'object',27:'object',28:'object',29:'float64',30:'object',31:'float64',32:'float64',
    33:'float64',34:'float64',35:'float64',36:'float64',37:'float64',38:'float64',39:'float64',40:'object'})
        
    homologs = pd.read_csv(file2, sep=',', index_col=0)
    collapsed_exons = list(set([i for i in homologs.ExonIDCluster if '/' in i]))  
    exonstable = modificate_exons(collapsed_exons, exonstable)

    output = pd.DataFrame(index= [])
    grouped = exonstable.groupby(['Species'])
    for name, data in grouped:
        #data = data.append(exonstable[(exonstable.GeneID_5p.isnull())&(exonstable.GeneID_3p==name)],sort = False )
        data = data.drop(columns = 'Species')

        strand = data.strand.iloc[0]
        intersect = homologs[homologs.Species==name]
        if strand ==1:
            data1 = data.rename(columns={'GeneID_5p':'GeneID','ExonID_5p':'ExonIDCluster','GenomicCodingEnd_5p':'S_exon_CodingEnd','EndPhase_5p':'S_exon_EndPhase'})
            data1 =data1[pd.notnull(data1['S_exon_CodingEnd'])]   
            temp1 = intersect.join(data1.set_index(['GeneID','ExonIDCluster','S_exon_CodingEnd','S_exon_EndPhase']),how = 'inner',sort=False,on = ['GeneID','ExonIDCluster','S_exon_CodingEnd','S_exon_EndPhase'])  
            #data1 = data1.rename(columns={'GeneID':'GeneID_5p','ExonIDCluster':'ExonID_5p','S_exon_CodingEnd':'GenomicCodingEnd_5p','S_exon_EndPhase':'EndPhase_5p'})

            data2 = data.rename(columns={'GeneID_3p':'GeneID','ExonID_3p':'ExonIDCluster','GenomicCodingStart_3p':'S_exon_CodingStart','StartPhase_3p':'S_exon_StartPhase'})
            data2 =data2[pd.notnull(data2['S_exon_CodingStart'])]   
            temp2 = intersect.join(data2.set_index(['GeneID','ExonIDCluster','S_exon_CodingStart','S_exon_StartPhase']),how = 'inner',sort=False,on = ['GeneID','ExonIDCluster','S_exon_CodingStart','S_exon_StartPhase'])  
            #data2 = data2.rename(columns={'GeneID':'GeneID_3p','ExonIDCluster':'ExonID_3p','S_exon_CodingStart':'GenomicCodingStart_3p','S_exon_StartPhase':'StartPhase_3p'})
        else:
            data1 = data.rename(columns={'GeneID_5p':'GeneID','ExonID_5p':'ExonIDCluster','GenomicCodingEnd_5p':'S_exon_CodingStart','StartPhase_5p':'S_exon_StartPhase'})
            data1 =data1[pd.notnull(data1['S_exon_CodingStart'])]   
            temp1 = intersect.join(data1.set_index(['GeneID','ExonIDCluster','S_exon_CodingStart','S_exon_StartPhase']),how = 'inner',sort=False,on = ['GeneID','ExonIDCluster','S_exon_CodingStart','S_exon_StartPhase'])  
            #data1 = data1.rename(columns={'GeneID':'GeneID_5p','ExonIDCluster':'ExonID_5p','S_exon_CodingEnd':'GenomicCodingEnd_5p','S_exon_EndPhase':'EndPhase_5p'})

            data2 = data.rename(columns={'GeneID_3p':'GeneID','ExonID_3p':'ExonIDCluster','GenomicCodingStart_3p':'S_exon_CodingEnd','EndPhase_3p':'S_exon_EndPhase'})
            data2 =data2[pd.notnull(data2['S_exon_CodingEnd'])]   
            temp2 = intersect.join(data2.set_index(['GeneID','ExonIDCluster','S_exon_CodingEnd','S_exon_EndPhase']),how = 'inner',sort=False,on = ['GeneID','ExonIDCluster','S_exon_CodingEnd','S_exon_EndPhase'])  
            #data2 = data2.rename(columns={'GeneID':'GeneID_3p','ExonIDCluster':'ExonID_3p','S_exon_CodingStart':'GenomicCodingStart_3p','S_exon_StartPhase':'StartPhase_3p'})
        


        introns_only = data[(pd.isnull(data.GeneID_5p))&(pd.isnull(data.GeneID_3p))]
        introns_only = introns_only[['start', 'end', 'strand', 'motif', 'total_uq', 'total_mm', 'ave_uq', 'num_exp', 'name_exp', 'uq_per_exp', 'mm_per_exp']]   
        introns_only = introns_only.assign(Species = name) 
        temp1 = temp1[['Species','GeneID','TranscriptIDCluster','ExonIDCluster','SubexonIDCluster','S_exonID','S_exon_CodingStart','S_exon_CodingEnd','chr', 'start', 'end', 'strand', 'motif', 'total_uq',
       'total_mm', 'ave_uq', 'num_exp', 'name_exp', 'uq_per_exp', 'mm_per_exp']]
        temp2 = temp2[['Species','GeneID','TranscriptIDCluster','ExonIDCluster','SubexonIDCluster','S_exonID','S_exon_CodingStart','S_exon_CodingEnd','chr', 'start', 'end', 'strand', 'motif', 'total_uq',
       'total_mm', 'ave_uq', 'num_exp', 'name_exp', 'uq_per_exp', 'mm_per_exp']]         
        ## as I cut out a lot of columns that were different, now there are duplicated columns. Get rid of them

        temp1 = temp1[~temp1.duplicated(keep = 'first')]
        temp2 = temp2[~temp2.duplicated(keep = 'first')]

        '''if (temp1.empty)&(temp2.empty):
            print('NO INTERSECT', name)
            continue
        elif temp2.empty:
            temp1 = temp1.rename(columns = dict([(i, i+'_5p') for i in temp1.columns[0:8]]))   
            print('temp2 EMPTY')
            end = temp1
        elif temp1.empty:
            temp2 = temp2.rename(columns = dict([(i, i+'_right') for i in temp1.columns[0:8]]))
            print('TEM2 EMPTY')
            end = temp2
        else:'''
        temp1_na = temp1[pd.isnull(temp1.start)]
        temp1 = temp1[~pd.isnull(temp1.start)]
        temp2_na = temp2[pd.isnull(temp2.start)]
        temp2 = temp2[~pd.isnull(temp2.start)]
        
        temp1_na = temp1_na.rename(columns = dict([(i, i+'_5p') for i in temp1.columns[1:8]]))  
        temp2_na = temp2_na.rename(columns = dict([(i, i+'_3p') for i in temp1.columns[1:8]]))

        end = temp1.join(temp2.set_index(['Species','chr','start','end','strand','motif','total_uq','total_mm','ave_uq','num_exp','name_exp','uq_per_exp','mm_per_exp']),on = ['Species','chr','start','end','strand','motif','total_uq','total_mm','ave_uq','num_exp','name_exp','uq_per_exp','mm_per_exp'], how = 'outer',sort = False,lsuffix = '_5p',rsuffix = '_3p')            
        end = end.append([temp1_na,temp2_na],sort=False) 
        end=end.append(introns_only,sort = False)  
        floatcols = [end.columns[col] for col in range(len(end.columns)) if (end.dtypes[col] == 'float64') & (end.columns[col] != 'ave_uq')]
        end[floatcols] = end[floatcols].astype('Int64')
        output = output.append(end, sort=False)

    if not output.empty:
        #output = output[pd.notnull(output['num_exp'])]   #get rid of lines where to exons are not connected by any SJ
        output = output.reset_index(drop = True)  
        output = output.assign(GeneID = pd.Series([output.GeneID_5p.iloc[i] if not pd.isnull(output.GeneID_5p.iloc[i]) else(output.GeneID_3p.iloc[i]) for i in range(len(output))]))      
        output = output.drop(columns = ['GeneID_5p','GeneID_3p'])   
        output = output[np.concatenate((output.columns[0],output.columns[-1],output.columns[1:-1]),axis = None)]
        
        temp = output[output.strand==2]
        output = output.drop(temp.index) 
        
        temp = temp[output.columns.tolist()[0:2]+output.columns.tolist()[20:]+output.columns.tolist()[8:20]+output.columns.tolist()[2:8]]
        temp.columns = output.columns   
        output= output.append(temp,sort = False)

        #to_file = file1[0:-18]+'merge_homologs_all.tsv' #if calling for merge_SJ_exons
        to_file = file1[0:-16]+'merge_homologs_all.tsv' #of calling for mege_SJ_all
        output.to_csv(to_file, sep='\t', index = False, header = True)


if __name__ == '__main__':
    main()

#output[['HomologousExon_5p','SubexonCodingStart_5p','SubexonCodingEnd_5p','start','end','HomologousExon_3p','SubexonCodingStart_3p', 'SubexonCodingEnd_3p']]