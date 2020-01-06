import pandas as pd
import numpy as np

def main():
    f = open('/home/sofya/Documents/BA/summary_byASE.txt')
    ase = f.read()
    f.close()

    rows = ase.split('\n')     
    colnames = rows[0].split(' ')
    rows = [i.split('"')[:-1] for i in rows[1:-1]]
    rows = [i[0][:-1].split(' ')+[i[1]] for i in rows]
    ase = pd.DataFrame(rows,columns = colnames)  

    '''
    id: identifier of the event
    idE: identifier of the s-exon
    type: Insertions, alternative Nter, alternative Cter or mutually Exclusive
    n: number of amino acids (rough estimation)
    structure: type of structure found
    hmmer: was a hit found when querying the s-exon with hmmer? (0: search failed, 1: search completed but we mostly found the protein itself, 2: another protein could be found
    documented: is the event documented in the literature?
    function: implication of the event from a functional point of view'''

    new_s_exons = []
    for i in range(len(ase)): 
        protein = ase.iloc[i].idE.split('_')[0] 
        s_exon = '_'.join(ase.iloc[i].idE.split('_')[1:] )
        file_old = '/home/sofya/Documents/TranscriptAnnotation-BeforeThorAxe04/benchmark/'+protein+'/thoraxe/homologous_exon_table.csv'
        file_new = '/home/sofya/Documents/TranscriptAnnotation/benchmark/'+protein+'/thoraxe/s_exon_table.csv'
        s_exons_old = pd.read_csv(file_old, sep = ',', index_col=0)
        s_exons_new = pd.read_csv(file_new, sep = ',', index_col=0)

        s_exon_sequences = list(set(s_exons_old[s_exons_old.HomologousExon==s_exon].HomologousExonSequence))
        s_exons_set = []
        for j in s_exon_sequences:
            if len(j)>10:
                s_exons_set = s_exons_set + list(set(s_exons_new[s_exons_new.S_exon_Sequence.str.contains(j[:-1],na=False)].S_exonID))
            else:
                s_exons_set = s_exons_set+ list(set(s_exons_new[(s_exons_new.S_exon_Sequence == j)|(s_exons_new.S_exon_Sequence == j[1:])|(s_exons_new.S_exon_Sequence == j[:-1])].S_exonID))
        if s_exons_set:
            s_exons_set = set(s_exons_set)
        new_s_exons.append(s_exons_set)
        
    ase = ase.assign(idE_s_exon = new_s_exons)
    ase = ase.assign(idE_s_exon = pd.Series([','.join(list(i)) for i in ase.idE_s_exon],index = ase.index)) 
    ase.to_csv('/home/sofya/Documents/TranscriptAnnotation/analysis/ase_list_new.txt',sep = '\t')  















if __name__=='__main__':
    main()