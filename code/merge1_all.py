import pandas as pd
import numpy as np
import sys
import os
#usage  ipython /home/sofya/Documents/TranscriptAnnotation/rnaseq/code/merge1_all.py /home/sofya/Documents/TranscriptAnnotation/benchmark threshold_for_total_unique_reads

def main():

    exon_dir = sys.argv[1]
    subdirs = [x[0] for x in os.walk(exon_dir)]
    exon_files = [x+'/exonstable_chr.tsv' for x in subdirs if x[-7:]=='Ensembl']  
    exon_files = [i  for i in exon_files if os.path.isfile(i)]

    frog = pd.read_csv('/home/sofya/Documents/BA/data/Xenopus_tropicalis_SJ.out.tab.merged.gz' , sep = '\t',compression = 'gzip',header = None, dtype = {0:'object',1:'int64',2:'int64',3:'int64',4:'int64',5:'int64',6:'int64',7:'float',8:'int64'})   
    zebrafish = pd.read_csv('/home/sofya/Documents/BA/data/Danio_rerio_SJ.out.tab.merged.gz' , sep = '\t',compression = 'gzip',header = None,dtype = {0:'object',1:'int64',2:'int64',3:'int64',4:'int64',5:'int64',6:'int64',7:'float',8:'int64'})   
    human = pd.read_csv('/home/sofya/Documents/BA/data/Homo_sapiens_SJ.out.tab.merged.gz', sep = '\t',compression = 'gzip',header = None,dtype = {0:'object',1:'int64',2:'int64',3:'int64',4:'int64',5:'int64',6:'int64',7:'float',8:'int64'})   
    mouse = pd.read_csv('/home/sofya/Documents/BA/data/Mus_musculus_SJ.out.tab.merged.gz', sep = '\t',compression = 'gzip',header = None,dtype = {0:'object',1:'int64',2:'int64',3:'int64',4:'int64',5:'int64',6:'int64',7:'float',8:'int64'})   
    cow = pd.read_csv('/home/sofya/Documents/BA/data/Bos_taurus_SJ.out.tab.merged.gz', sep = '\t',compression = 'gzip',header = None,dtype = {0:'object',1:'int64',2:'int64',3:'int64',4:'int64',5:'int64',6:'int64',7:'float',8:'int64'})   
    c_elegans = pd.read_csv('/home/sofya/Documents/BA/data/Caenorhabditis_elegans_SJ.out.tab.merged.gz', sep = '\t',compression = 'gzip',header = None,dtype = {0:'object',1:'int64',2:'int64',3:'int64',4:'int64',5:'int64',6:'int64',7:'float',8:'int64'})   
    chicken = pd.read_csv('/home/sofya/Documents/BA/data/Gallus_gallus_SJ.out.tab.merged.gz', sep = '\t',compression = 'gzip',header = None,dtype = {0:'object',1:'int64',2:'int64',3:'int64',4:'int64',5:'int64',6:'int64',7:'float',8:'int64'})   
    gorilla = pd.read_csv('/home/sofya/Documents/BA/data/Gorilla_gorilla_SJ.out.tab.merged.gz', sep = '\t',compression = 'gzip',header = None,dtype = {0:'object',1:'int64',2:'int64',3:'int64',4:'int64',5:'int64',6:'int64',7:'float',8:'int64'})   
    macaque = pd.read_csv('/home/sofya/Documents/BA/data/Macaca_mulatta_SJ.out.tab.merged.gz', sep = '\t',compression = 'gzip',header = None,dtype = {0:'object',1:'int64',2:'int64',3:'int64',4:'int64',5:'int64',6:'int64',7:'float',8:'int64'})   
    opossum = pd.read_csv('/home/sofya/Documents/BA/data/Monodelphis_domestica_SJ.out.tab.merged.gz', sep = '\t',compression = 'gzip',header = None,dtype = {0:'object',1:'int64',2:'int64',3:'int64',4:'int64',5:'int64',6:'int64',7:'float',8:'int64'})   
    platypus = pd.read_csv('/home/sofya/Documents/BA/data/Ornithorhynchus_anatinus_SJ.out.tab.merged.gz', sep = '\t',compression = 'gzip',header = None,dtype = {0:'object',1:'int64',2:'int64',3:'int64',4:'int64',5:'int64',6:'int64',7:'float',8:'int64'})   
    rat = pd.read_csv('/home/sofya/Documents/BA/data/Rattus_norvegicus_SJ.out.tab.merged.gz', sep = '\t',compression = 'gzip',header = None,dtype = {0:'object',1:'int64',2:'int64',3:'int64',4:'int64',5:'int64',6:'int64',7:'float',8:'int64'})   
    pig = pd.read_csv('/home/sofya/Documents/BA/data/Sus_scrofa_SJ.out.tab.merged.gz', sep = '\t',compression = 'gzip',header = None,dtype = {0:'object',1:'int64',2:'int64',3:'int64',4:'int64',5:'int64',6:'int64',7:'float',8:'int64'})   
    

    columns = ['chr','start','end','strand','motif','total_uq','total_mm','ave_uq','num_exp', 'name_exp','uq_per_exp','mm_per_exp']   
    CHR = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','MT','X','Y','Z']   
    species_code = {'ENSG': human,'ENSXET':frog,'ENSMUS':mouse,'ENSDAR':zebrafish,'ENSBTA':cow,'WBGene':c_elegans,'ENSGAL':chicken,
                    'ENSGGO':gorilla, 'ENSMMU':macaque, 'ENSMOD':opossum, 'ENSOAN':platypus, 'ENSRNO' : rat,'ENSSSC':pig}   
    species_name = {'ENSG':'homo_sapiens','ENSXET':'xenopus_tropicalis','ENSMUS':'mus_musculus','ENSDAR':'danio_rerio','ENSBTA':'bos_taurus',
                    'WBGene':'caenorhabditis_elegans', 'ENSGAL':'gallus_gallus','ENSGGO':'gorilla_gorilla','ENSMMU':'macaca_mulatta','ENSMOD':'monodelphis_domestica', 
                    'ENSOAN':'ornithorhynchus_anatinus', 'ENSRNO' : 'rattus_norvegicus','ENSSSC':'sus_scrofa'}
    strand_code = {-1: 2,1:1} 
    for i in [zebrafish,human,mouse,frog, cow,c_elegans,chicken,gorilla,macaque,opossum,platypus,rat,pig]:  
        i.columns = columns  

    for file in exon_files:
        print(file, exon_files.index(file)+1,'/',len(exon_files))
        #file = '/home/sofya/Documents/TranscriptAnnotation/benchmark/SRC/Ensembl/exonstable_chr.tsv' 
        exonstable = pd.read_csv(file, sep = '\t', dtype = {0:"object",1:"object",2:"object",3:"int64",4:"object",5:"int64",6:"int64",7:"int64",8:"float64",9:"float64",10:"float64",11:"float64",12:"int64",13:"int64",14:"object"})
        output = pd.DataFrame(index= [])
        
        grouped = exonstable.groupby(['GeneID'])
        for name, data in grouped:
            code = name[0:6]
            if code =='ENSG00':
                code = 'ENSG' 
            elif code[0:4]=='FBgn': # skip drosopjila as no SJ 
                continue               
            chromosome = data.chr.iloc[0] 
            strand = data.Strand.iloc[0]

            min_val = min(data[['ExonRegionStart','ExonRegionEnd']].min())   
            max_val = max(data[['ExonRegionStart','ExonRegionEnd']].max())  

            intersect = species_code[code][(species_code[code].chr == chromosome)&(species_code[code].strand == strand_code[strand])&(species_code[code].end>=min_val)&(species_code[code].end<=max_val)&(species_code[code].start>=min_val)&(species_code[code].end<=max_val)]
            #intersect = intersect[intersect.total_uq> int(sys.argv[2])]

            data = data.assign(key1 = pd.Series(data.ExonRegionStart))
            intersect = intersect.assign(key1 = pd.Series(intersect.end + 1))   
            intersect = intersect.drop(columns = 'chr')
            temp2 = data.join(intersect.set_index('key1'),how = 'outer',on = 'key1',sort = False)

            data = data.drop(columns = 'key1')
            intersect = intersect.drop(columns = 'key1')
            shared = intersect.columns.tolist()

            data = data.assign(key2 = pd.Series(data.ExonRegionEnd))
            intersect = intersect.assign(key2 = pd.Series(intersect.start -1))
            temp1 = data.join(intersect.set_index('key2'),how = 'outer',on = 'key2',sort = False)  

            temp1 = temp1.drop(columns = 'key2')#connects end of exon with intron start
            temp2 = temp2.drop(columns = 'key1')# connects end of intron with start of exon
            temp1 = temp1.reset_index(drop = True)
            temp2 = temp2.reset_index(drop = True)


            temp1_na = temp1[np.isnan(temp1.start)]
            temp1 = temp1[ ~np.isnan(temp1.start)] 
            temp2_na = temp2[np.isnan(temp2.start)]
            temp2 = temp2[ ~np.isnan(temp2.start)] 

            end = temp1.join(temp2.set_index(shared),on = shared,how = 'outer', lsuffix = '_5p',rsuffix = '_3p',sort = False)

            temp1_na = temp1_na.rename(columns = dict([(i, i+'_5p') for i in temp1_na.columns[0:14]])) 
            temp2_na = temp2_na.rename(columns = dict([(i, i+'_3p') for i in temp2_na.columns[0:14]])) 
            end = end.append([temp1_na,temp2_na],sort=False) 

            floatcols= [end.columns[col] for col in range(len(end.columns)) if (end.dtypes[col]=='float64')&(end.columns[col]!='ave_uq')]
            end[floatcols]=end[floatcols].astype('Int64')   
            end = end.drop(columns = ['chr_5p','chr_3p'])
            end = end.assign(chr = chromosome) 
            end = end.assign(Species = species_name[code])
            end = end[np.concatenate((end.columns[-1],end.columns[:-1]),axis = None)] 
            output=output.append(end,sort = False)   
        if not output.empty:
            to_file = file[0:-18]+'merge_SJ_all.tsv'
            output.to_csv(to_file, sep = '\t', index = False, header = True) 

if __name__== '__main__':
    main()
