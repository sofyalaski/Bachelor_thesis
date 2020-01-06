import pandas as pd
import numpy as np
import itertools
import math
from collections import defaultdict 

def main():
    ase = pd.read_csv('/home/sofya/Documents/TranscriptAnnotation/analysis/ase_list_new.txt',sep = '\t',index_col=0)

    def insertion(s_exon_name, gene):
        print(gene,s_exon_name)
        exonstable = pd.read_csv('/home/sofya/Documents/TranscriptAnnotation/analysis/'+gene+'/rnaseq/merge_homologs_norm_counts.tsv',sep = '\t')
        exonstable =exonstable[exonstable.n_total_uq>1e-07]  
        homologs  = pd.read_csv('/home/sofya/Documents/TranscriptAnnotation/benchmark/'+gene+'/thoraxe/s_exon_table.csv',sep = ',', index_col = 0)  
       

        def find_ancestral_exons(row):
            rank_now = row.ExonRank
            found_s_exons = homologs[(homologs.TranscriptIDCluster == row.TranscriptIDCluster)&(homologs.ExonRank==rank_now-1)]
            if not found_s_exons[~found_s_exons.ExonRank.duplicated(keep = 'last')].S_exonID.empty:
                return found_s_exons[~found_s_exons.ExonRank.duplicated(keep = 'last')].S_exonID.iloc[0]
            else:
                return 'start'

        def find_descendent_exons(row):
            rank_now = row.ExonRank
            found_s_exons = homologs[(homologs.TranscriptIDCluster == row.TranscriptIDCluster)&(homologs.ExonRank==rank_now+1)]
            if not found_s_exons[~found_s_exons.ExonRank.duplicated(keep = 'first')].S_exonID.empty:
                return found_s_exons[~found_s_exons.ExonRank.duplicated(keep = 'first')].S_exonID.iloc[0]
            else:
                return 'end'

        def check_old(row):
            val = False
            anc = homologs[(homologs.Species == row.Species)&(homologs.S_exonID==row.ancestors)]
            for tr in range(len(anc)):
                if (homologs[(homologs.Species == row.Species)&(homologs.S_exonID==row.descendants)&(homologs.TranscriptIDCluster==anc.iloc[tr].TranscriptIDCluster)].ExonRank-1==anc.iloc[tr].ExonRank).any():
                    val = True
                    break
            return val
        
        def check_new(row):
            val = False
            for i in range(len(row.S_exonID_5p)):
                for j in range(len(row.S_exonID_3p)):
                    if  not exonstable[(exonstable.Species==row.name)&(exonstable.S_exonID_5p==row.S_exonID_5p[i])&(exonstable.S_exonID_3p==row.S_exonID_3p[j])].empty:
                        val = True
                        break
            return val

        indexes = homologs[homologs.S_exonID == s_exon_name].index
        temp = homologs.loc[indexes]
        temp = temp.assign(ancestors = homologs.loc[indexes].apply(find_ancestral_exons,axis=1))
        temp = temp.assign(descendants = homologs.loc[indexes].apply(find_descendent_exons,axis=1))
        temp = temp[(temp.ancestors!='start')&(temp.descendants!='end')][['Species','ancestors','descendants']]    
        if not temp.empty:
            temp = temp[~temp.duplicated()]
            temp= temp.assign(check = temp.apply(check_old,axis=1))
            list_old_species = temp[temp.check==True].Species.tolist()
        else:
            print(" List of annotated exon doesn't define this exon as an Insertion anymore, as it the next junctioned exon is from the same cluster")
            list_old_species = []
        
        parent = exonstable[(exonstable.S_exonID_3p==s_exon_name)& pd.notnull(exonstable.S_exonID_5p)][['Species','S_exonID_5p','S_exonID_3p']]      
        child = exonstable[(exonstable.S_exonID_5p==s_exon_name)& pd.notnull(exonstable.S_exonID_3p)][['Species','S_exonID_5p','S_exonID_3p']]      
        parent = parent[~parent.duplicated()]
        child = child[~child.duplicated()]
        parent = parent.groupby('Species')['S_exonID_5p'].apply(lambda x: list(x))  
        child = child.groupby('Species')['S_exonID_3p'].apply(lambda x: list(x))  
        junctions = pd.concat([parent,child],axis=1,sort = False)        
        junctions = junctions[pd.notnull(junctions.S_exonID_5p)&pd.notnull(junctions.S_exonID_3p)]

        junctions = junctions.apply(check_new,axis=1)
        list_new_species = junctions[junctions==True].index.tolist()  
        return(list_old_species,list_new_species)

    def mutually_exclusive(s_exon_name,gene):
        if (gene =='SNAP-25')&(s_exon_name =='3_1+3_2'):
            return([],[])

        
        print(gene,s_exon_name)
        exonstable = pd.read_csv('/home/sofya/Documents/TranscriptAnnotation/analysis/'+gene+'/rnaseq/merge_homologs_norm_counts.tsv',sep = '\t')
        exonstable =exonstable[exonstable.n_total_uq>1e-07]  
        homologs  = pd.read_csv('/home/sofya/Documents/TranscriptAnnotation/benchmark/'+gene+'/thoraxe/s_exon_table.csv',sep = ',', index_col = 0)  

        exon_clusters = homologs[['TranscriptIDCluster','S_exonID','ExonRank']].groupby(['TranscriptIDCluster','ExonRank'])['S_exonID'].apply(lambda x: list(x)) 
        exon_clusters = [i for i in exon_clusters if len(i)>1]   
        exon_clusters.sort()
        exon_clusters = list(exon_clusters for exon_clusters,_ in itertools.groupby(exon_clusters))    


        def merge_common(lists): 
            neigh = defaultdict(set) 
            visited = set() 
            for each in lists: 
                for item in each: 
                    neigh[item].update(each) 
            def comp(node, neigh = neigh, visited = visited, vis = visited.add): 
                nodes = set([node]) 
                next_node = nodes.pop 
                while nodes: 
                    node = next_node() 
                    vis(node) 
                    nodes |= neigh[node] - visited 
                    yield node 
            for node in neigh: 
                if node not in visited: 
                    yield sorted(comp(node)) 

        exon_clusters = list(merge_common(exon_clusters)) 
      
        def find_ancestral_exons(row):
            rank_now = row.ExonRank
            found_s_exons = homologs[(homologs.TranscriptIDCluster == row.TranscriptIDCluster)&(homologs.ExonRank==rank_now-1)]
            if not found_s_exons[~found_s_exons.ExonRank.duplicated(keep = 'last')].S_exonID.empty:
                return found_s_exons[~found_s_exons.ExonRank.duplicated(keep = 'last')].S_exonID.iloc[0]
            else:
                return 'start'

        def find_descendent_exons(row):
            rank_now = row.ExonRank
            found_s_exons = homologs[(homologs.TranscriptIDCluster == row.TranscriptIDCluster)&(homologs.ExonRank==rank_now+1)]
            if not found_s_exons[~found_s_exons.ExonRank.duplicated(keep = 'first')].S_exonID.empty:
                return found_s_exons[~found_s_exons.ExonRank.duplicated(keep = 'first')].S_exonID.iloc[0]
            else:
                return 'end'

        def check_old(row):
            val = False
            anc = homologs[(homologs.Species == row.Species)&(homologs.S_exonID==row.ancestors)]
            for tr in range(len(anc)):
                alt_s_exon = homologs[(homologs.Species == row.Species)&(homologs.TranscriptIDCluster==anc.iloc[tr].TranscriptIDCluster)&(homologs.ExonRank ==anc.iloc[tr].ExonRank+1)].S_exonID.tolist()
                if row.s_exon not in alt_s_exon:#the first part of alt s_exon is found, check second part
                    if (homologs[(homologs.Species == row.Species)&(homologs.S_exonID==row.descendants)&(homologs.TranscriptIDCluster==anc.iloc[tr].TranscriptIDCluster)].ExonRank-2==anc.iloc[tr].ExonRank).any():
                        val = True
                        break
            return val
        
        def check_new(row):
            val = False
            for i in range(len(row.S_exonID_5p)):
                for j in range(len(row.S_exonID_3p)):
                    par = exonstable[(exonstable.Species==row.name)&(exonstable.S_exonID_5p==row.S_exonID_5p[i])&(exonstable.S_exonID_3p!=row.s_exon)][['S_exonID_5p','S_exonID_3p']]   
                    ch = exonstable[(exonstable.Species==row.name)&(exonstable.S_exonID_3p==row.S_exonID_3p[j])&(exonstable.S_exonID_5p!=row.s_exon)][['S_exonID_5p','S_exonID_3p']]   
                    par = par[~par.duplicated()] 
                    ch = ch[~ch.duplicated()]
                    for nter in par.S_exonID_3p:
                        for cter in ch.S_exonID_5p:
                             if (True in [(nter in i)&(cter in i) for i in exon_clusters]) |(nter == cter) :
                                 val = True
                                 break
            return val


        indexes = homologs[homologs.S_exonID == s_exon_name].index
        temp = homologs.loc[indexes]
        temp = temp.assign(ancestors = homologs.loc[indexes].apply(find_ancestral_exons,axis=1))
        temp['s_exon'] = s_exon_name  
        temp = temp.assign(descendants = homologs.loc[indexes].apply(find_descendent_exons,axis=1))
        temp = temp[(temp.ancestors!='start')&(temp.descendants!='end')][['Species','ancestors','s_exon','descendants']]    
        if not temp.empty:
            temp = temp[~temp.duplicated()]
            temp= temp.assign(check = temp.apply(check_old,axis=1))
            list_old_species = temp[temp.check==True].Species.tolist()
        else:
            print(" List of annotated exon doesn't define this exon as an Insertion anymore, as it the next junctioned exon is from the same cluster")
            list_old_species = []
        

        parent = exonstable[(exonstable.S_exonID_3p==s_exon_name)& pd.notnull(exonstable.S_exonID_5p)][['Species','S_exonID_5p','S_exonID_3p']]      
        child = exonstable[(exonstable.S_exonID_5p==s_exon_name)& pd.notnull(exonstable.S_exonID_3p)][['Species','S_exonID_5p','S_exonID_3p']]      
        parent = parent[~parent.duplicated()]
        child = child[~child.duplicated()]
        parent = parent.groupby('Species')['S_exonID_5p'].apply(lambda x: list(x))  
        child = child.groupby('Species')['S_exonID_3p'].apply(lambda x: list(x))  
        junctions = pd.concat([parent,child],axis=1,sort = False)        
        junctions = junctions[pd.notnull(junctions.S_exonID_5p)&pd.notnull(junctions.S_exonID_3p)]
        junctions['s_exon']=s_exon_name

        junctions = junctions.apply(check_new,axis=1)
        list_new_species = junctions[junctions==True].index.tolist()  
        return(list_old_species,list_new_species)

    insertions = ase[ase.type=='I']
    s_exons = insertions.idE_s_exon.str.split(',')  
    s_exons = [s_exons.iloc[i][0] for i in range(len(s_exons))]
    genes = insertions.idE.str.split('_')  
    genes = [genes.iloc[i][0] for i in range(len(genes))]  
    insert_pairs = [(gene,exon) for gene,exon in zip(genes,s_exons)]
    species_output = [insertion(pair[1],pair[0]) for pair in insert_pairs]
    insertions = insertions.assign(Ensembl = [species_output[i][0] for i in range(len(species_output))])
    insertions = insertions.assign(rnaseq = [species_output[i][1] for i in range(len(species_output))])

    m_exclusive = ase[ase.type=='E']
    s_exons = m_exclusive.idE_s_exon.str.split(',')  
    s_exons = [s_exons.iloc[i][0] for i in range(len(s_exons))]
    genes = m_exclusive.idE.str.split('_')  
    genes = [genes.iloc[i][0] for i in range(len(genes))]  
    insert_pairs = [(gene,exon) for gene,exon in zip(genes,s_exons)]
    
    species_output = [mutually_exclusive(pair[1],pair[0]) for pair in insert_pairs]
    m_exclusive = m_exclusive.assign(Ensembl = [species_output[i][0] for i in range(len(species_output))])
    m_exclusive = m_exclusive.assign(rnaseq = [species_output[i][1] for i in range(len(species_output))])

    output = insertions.append(m_exclusive, sort = False)     
    output.to_csv('/home/sofya/Documents/TranscriptAnnotation/analysis/ase_list_counted.txt', index = False, sep = '\t')

    output[[(len(output.Ensembl.iloc[i])>len(output.rnaseq.iloc[i])) for i in range(len(output))]]  # Ensembl annotation has more species than found with rnaseq

