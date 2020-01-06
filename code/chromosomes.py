import pandas as pd
import numpy as np
import sys
import re


def main():
    file = sys.argv[1]
    prot = sys.argv[2]
    exonstable_f = sys.argv[3]

    exonstable = pd.read_csv(exonstable_f, sep = '\t')

    #sort exons by rank for each transcript
    for value,GeneID in enumerate(set(exonstable.GeneID),1): 
        tmp = exonstable[exonstable.GeneID == GeneID]  
        for TranscriptID in set(tmp.TranscriptID):
            tmp2 = tmp[tmp.TranscriptID == TranscriptID]  

            if tmp2.Strand.iloc[0] ==-1:
                tmp2 = tmp2.sort_values(by = 'ExonRank',ascending=False)
            else:
                tmp2 = tmp2.sort_values(by = 'ExonRank')
            t = exonstable[(exonstable.GeneID == GeneID)&(exonstable.TranscriptID == TranscriptID)].index  
            for colname in exonstable:
                exonstable.loc[t,colname] = tmp2[colname].values
    
    f = open(file)
    content = f.read()
    profile = []
    for entry in content.split(">"):
        pos = entry.find("\n")
        name = entry[0:pos]
        if name != "":
            profile.append(name)
    f.close()

    #species = ['danio_rerio','homo_sapiens','xenopus_tropicalis','mus_musculus','gorilla_gorilla','macaca_mulatta','monodelphis_domestica', 'rattus_norvegicus','gallus_gallus','bos_taurus','sus_scrofa','ornithorhynchus_anatinus','caenorhabditis_elegans']
    
    
    table = []
    for i in profile:
        table.append(re.split(' |:',i))
    inf = pd.DataFrame(table,columns = ['specie','G/T/P','ExonID','molecule','version','chr','start','end','strand'])
    
    species = list(set(inf.specie))
    inf['protein'] = prot
    species_dict = dict([[y,x] for x,y in zip(inf.specie,inf.ExonID.str.slice(0,6))])
    species_dict['ENSG']=species_dict.pop('ENSE00')
    inf = inf[inf.specie.isin(species)]#filter out species of interest from fasta file

    #k = inf[[len(inf.chr.iloc[i])<=2 for i in range(len(t))]]
    dic = []
    for i in set(inf.specie):
            dic.append((i,inf[inf.specie == i].chr.iloc[0]))
    dic = dict(dic)
    
    exonstable['chr'] = [dic[species_dict[exonstable.GeneID.iloc[i][0:6]]] if exonstable.GeneID.iloc[i][0:6] in species_dict.keys() else (dic[species_dict['ENSG']]) for i in range(len(exonstable))] 
   
    floatcols= [exonstable.columns[col] for col in range(len(exonstable.columns)) if exonstable.dtypes[col]=='float64']
    exonstable[floatcols]=exonstable[floatcols].astype('Int64')    
    to_file = sys.argv[3][0:-4]+'_chr.tsv'
    exonstable.to_csv(to_file, index = False, header =True,sep = '\t')

    
    

if __name__ == '__main__':
    main()