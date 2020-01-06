import pandas as pd
import numpy as np
import itertools
from collections import defaultdict 

def gene_check(gene, output):
    exonstable = pd.read_csv('/home/sofya/Documents/TranscriptAnnotation/analysis/'+gene+'/rnaseq/merge_homologs_norm_counts.tsv',sep = '\t')
    exonstable =exonstable[exonstable.n_total_uq>1e-07]  
    homologs  = pd.read_csv('/home/sofya/Documents/TranscriptAnnotation/benchmark/'+gene+'/thoraxe/s_exon_table.csv',sep = ',', index_col = 0)  
    
    species_name = {'ENSG':'homo_sapiens','ENSXET':'xenopus_tropicalis','ENSMUS':'mus_musculus','ENSDAR':'danio_rerio','ENSBTA':'bos_taurus','ENSGGO':'gorilla_gorilla',
                    'ENSMMU':'macaca_mulatta','ENSMOD':'monodelphis_domestica', 'ENSOAN':'ornithorhynchus_anatinus', 'ENSRNO' : 'rattus_norvegicus','ENSSSC':'sus_scrofa'}
    exon_clusters = homologs[['TranscriptIDCluster','S_exonID','ExonRank']].groupby(['TranscriptIDCluster','ExonRank'])['S_exonID'].apply(lambda x: list(x)) 
    exon_clusters = pd.DataFrame(exon_clusters).reset_index(drop = False)
    exon_clusters = exon_clusters[[len(i)>1 for i in exon_clusters.S_exonID]] 
    exon_clusters = exon_clusters.assign(Species = [species_name[exon_clusters.TranscriptIDCluster.iloc[i][0:6]] if exon_clusters.TranscriptIDCluster.iloc[i][0:6] in species_name.keys() else(species_name['ENSG']) for i in range(len(exon_clusters))])
    exon_clusters = exon_clusters[['Species','S_exonID']]
    exon_clusters = exon_clusters.assign(S_exonID = [','.join(exon_clusters.S_exonID.iloc[i]) for i in range(len(exon_clusters))])
    exon_clusters = exon_clusters[~exon_clusters.duplicated()]
    exon_clusters = exon_clusters.assign(S_exonID = [exon_clusters.S_exonID.iloc[i].split(',') for i in range(len(exon_clusters))])

    #clusters = exon_clusters.S_exonID.apply(pd.Series)
    #exon_clusters = pd.concat([exon_clusters.Species.to_frame(),clusters.rename(columns = lambda x : 'S_exonID_' + str(x))], axis= 1)   
    
    
    def event(gene,s_exon_name,event_type):
        print(gene,s_exon_name,event_type)

        '''def find_ancestral_exons(row):
            """Given a row with an s_exon in some specie, find it's ancestor in that Specie from s_exons_table."""
            rank_now = row.S_exon_Rank
            if rank_now == 1:
                return 'start'
            else:
                found_s_exons = homologs[(homologs.TranscriptIDCluster == row.TranscriptIDCluster)&(homologs.S_exon_Rank==rank_now-1)]
                if not found_s_exons.empty:
                    return found_s_exons.S_exonID.iloc[0]
                else:
                    return np.nan

        def find_descendent_exons(row):
            """Return next ten exons for the given specie in s_exon from s_exons_table."""
            rank_now = row.S_exon_Rank
            #found_s_exons = homologs[(homologs.TranscriptIDCluster == row.TranscriptIDCluster)&(homologs.S_exon_Rank==ranks_array)]
            max_rank_for_transcript = max(homologs[homologs.TranscriptIDCluster == row.TranscriptIDCluster].S_exon_Rank)
            if rank_now+10>max_rank_for_transcript:
                ranks_array = list(range(rank_now+1,max_rank_for_transcript+1))
            else:
                ranks_array = list(range(rank_now+1, rank_now+11))#check up to ten next exons
            return homologs[(homologs.TranscriptIDCluster == row.TranscriptIDCluster)&(homologs.S_exon_Rank.isin(ranks_array))].S_exonID.tolist()'''

        def check_cluster(s_exon,Specie):
            """Find a following s_exon that is inside of the same cluster for given Specie. Searches in s_exons_table."""
            if s_exon in [s_exon for clst in exon_clusters[exon_clusters.Species==Specie].S_exonID for s_exon in clst]:
                t = exon_clusters[exon_clusters.Species == Specie].S_exonID.apply(lambda x: s_exon in x) 
                temp = exon_clusters.loc[t[t==True].index]
                next = temp.apply(lambda x: x.S_exonID[x.S_exonID.index(s_exon)+1] if  x.S_exonID.index(s_exon)+1!=len(x.S_exonID) else np.nan, axis = 1).dropna().tolist() 
                if next:
                    return list(set(next))
                else:
                    return 0 
            else:
                return 0
        

        def check_cluster_down(s_exon,Specie):
            """Find a following s_exon that is inside of the same cluster for given Specie. Searches in s_exons_table."""
            if s_exon in [s_exon for clst in exon_clusters[exon_clusters.Species==Specie].S_exonID for s_exon in clst]:
                t = exon_clusters[exon_clusters.Species == Specie].S_exonID.apply(lambda x: s_exon in x) 
                temp = exon_clusters.loc[t[t==True].index]
                previous = temp.apply(lambda x: x.S_exonID[x.S_exonID.index(s_exon)-1] if  x.S_exonID.index(s_exon)!=0 else np.nan, axis = 1).dropna().tolist() 
                if previous:
                    return list(set(previous))
                else:
                    return 0 
            else:
                return 0

        def check_next_exonstable(row):
            further_exons_df = pd.DataFrame(row.S_exonID_3p,index= [0],columns = [0])    
            next_exon = list(set(exonstable[(exonstable.Species==row.Species)&(exonstable.S_exonID_5p ==row.S_exonID_3p)&(pd.notnull(exonstable.S_exonID_3p))].S_exonID_3p))
            cluster = check_cluster(further_exons_df.iloc[0][0],row.Species)
            if cluster !=0:
                next_exon+=cluster
            next_exon = [val for val in next_exon if val!=0]
            if next_exon:
                further_exons_df = pd.concat([further_exons_df]*len(next_exon),ignore_index = True)
                further_exons_df[1] = next_exon 
                for i  in range(2,10):
                    if further_exons_df.columns[-1] != i-1:
                        break
                    for j in range(len(further_exons_df)):
                        if pd.isnull(further_exons_df[i-1].iloc[j]):
                            continue
                        next_exon = list(set(exonstable[(exonstable.Species==row.Species)&(exonstable.S_exonID_5p ==further_exons_df[i-1].iloc[j])&(pd.notnull(exonstable.S_exonID_3p))].S_exonID_3p))
                        cluster = check_cluster(further_exons_df[i-1].iloc[j],row.Species)
                        if cluster!=0:
                            next_exon+=cluster
                        next_exon = [val for val in next_exon if val!=0]
                        if next_exon:
                            dupl = pd.concat([further_exons_df.iloc[[j]]]*len(next_exon),ignore_index = True)
                            dupl[i] = next_exon 
                            further_exons_df = further_exons_df.drop(j)
                            further_exons_df = pd.concat([further_exons_df,dupl],ignore_index = True)
            return further_exons_df
        
        def shortest_alternative_path(mask_row):
            return mask_row.tolist().index(True)    


        def check_path_in_species(path):
            species = []
            '''nodes = pd.Series(list(zip(path[:-1],path[1:])), index = path[1:]).to_frame().T

            #nodes = pd.DataFrame(index=[], columns = list(zip(path[:-1],path[1:])))  
            from_junctions = nodes.apply(lambda x: list(set(exonstable[(exonstable.S_exonID_5p==x.iloc[0][0])&(exonstable.S_exonID_3p==x.iloc[0][1])].Species)), axis=0)  
            for i in Species:
                nodes = nodes.append(pd.Series( nodes.apply(lambda x: ','.join(check_cluster(x.iloc[0][0], i)) if check_cluster(x.iloc[0][0], i) !=0 else 0,axis=0), name = i), sort = False)
            nodes.
            from_homologs = [i  for i in Species if check_cluster(path[node], i)!=0 ]     

            from_homologs = [i  for i in Species if check_cluster(path[node], i)!=0 ]     
            from_junctions+=[i  for i in from_homologs if path[node+1] in check_cluster(path[node], i) ]     

            '''
            for node in range(len(path)-1):
                from_junctions = list(set(exonstable[(exonstable.S_exonID_5p==path[node])&(exonstable.S_exonID_3p==path[node+1])].Species))
                from_homologs = [i  for i in Species if check_cluster(path[node], i)!=0 ]     
                from_junctions+=[i  for i in from_homologs if path[node+1] in check_cluster(path[node], i) ]     
                species.append(list(set(from_junctions)))
            return list(set.intersection(*map(set,species)))
        
        def calculate_path_value(paths,species_path, event_type):
            path_values = []
            if event_type =='I':
                for path in range(len(paths)):
                    temp= []
                    for specie in species_path[path]:
                        specie_mean = []
                        for node in range(len(paths[path])-1):
                            # if there are multiple junctions connecting two s-exones the take mean of those junctions
                            specie_mean.append(np.mean(exonstable[(exonstable.Species==specie)&(exonstable.S_exonID_5p==paths[path][node])&(exonstable.S_exonID_3p==paths[path][node+1])].n_total_uq))
                        
                        result = [k for k in specie_mean if pd.notnull(k)]
                        if result:
                            temp.append(np.mean(result))
                        else:
                            temp.append(0)
                    path_values.append(temp)
            else:
                for specie in species_path:
                        specie_mean = []
                        for node in range(len(paths)-1):
                            # if there are multiple junctions connecting two s-exones the take mean of those junctions
                            specie_mean.append(np.mean(exonstable[(exonstable.Species==specie)&(exonstable.S_exonID_5p==paths[node])&(exonstable.S_exonID_3p==paths[node+1])].n_total_uq))
                        result = [k for k in specie_mean if pd.notnull(k)]
                        if result:
                            path_values.append(np.mean(result))
                        else:
                            result.append(0) ## means they connected inside one cluster and no true junction connects them
            return path_values    
        
        def path_redundancy_check(paths, alt_paths, ordering):
            true_paths =[]
            for i in range(len(paths)):
                if (','.join(paths[i]) in ordering.paths.tolist()) & (','.join(alt_paths[i]) in ordering.alt_paths.tolist()):
                    true_paths.append(i)
            return true_paths


        def check_new_insertion(row,ordering):
            p3_exons = check_next_exonstable(row)
            for i in range(len(p3_exons)):
                inserts = list(set(exonstable[(exonstable.Species==row.Species)&(exonstable.S_exonID_5p == row.S_exonID_5p)&pd.notnull(exonstable.S_exonID_3p)&pd.notnull(exonstable.name_exp)&(exonstable.S_exonID_3p.isin(p3_exons.iloc[i]))].S_exonID_3p))
                paths = [[row.S_exonID_5p]+[row.s_exon]+p3_exons.iloc[i].tolist()[:p3_exons.iloc[i].tolist().index(insert)+1] for insert in inserts]
                alt_paths = [[row.S_exonID_5p]+[insert] for insert in inserts]  
                paths_described = path_redundancy_check(paths, alt_paths, ordering)
                for index in sorted(paths_described, reverse=True):
                    del paths[index]
                    del alt_paths[index]
                if paths:
                    species_path = [check_path_in_species(path) for path in paths]
                    species_alt_path = [check_path_in_species(path) for path in alt_paths]
                    index_little_species = [i for i in range(len(species_path)) if (len(species_path[i])<2) | (len(species_alt_path[i])<2)]

                    for index in sorted(index_little_species, reverse=True):
                        del paths[index]
                        del alt_paths[index]
                        del species_path[index]
                        del species_alt_path[index]
                    if paths:
                        path_values = calculate_path_value(paths,species_path,'I')     
                        alt_path_values = calculate_path_value(alt_paths,species_alt_path,'I') 
                        ordering = ordering.append(pd.DataFrame({'paths': [','.join(j)for j in paths] ,'alt_paths': [','.join(j)for j in alt_paths],
                                'path_species':[','.join(j)for j in species_path],'alt_path_species':[','.join(j)for j in species_alt_path],
                                'path_values':path_values,'alt_path_values':alt_path_values, 'type':'I','idE':s_exon_name}),sort = False)
            return ordering

        def check_new_m_exclusive(row,alternative_paths_rnaseq):
            p3_exons = check_next_exonstable(row)# exons following the exon on 3p end
            alt_s_exons = exonstable[(exonstable.Species == row.Species)&(exonstable.S_exonID_5p == row.S_exonID_5p)&(exonstable.S_exonID_3p !=row.s_exon)&pd.notnull(exonstable.name_exp)&pd.notnull(exonstable.S_exonID_3p)][['Species','S_exonID_5p','S_exonID_3p','n_total_uq','n_total_mm']]
            alt_s_exons = alt_s_exons[~alt_s_exons.duplicated()]
            for alt_exon in range(len(alt_s_exons)):
                #find exons that follow the starting alterating s-exon
                following_exons = check_next_exonstable(alt_s_exons.iloc[alt_exon])  
                following_exons = following_exons.apply(lambda x: pd.Series([np.nan]*len(x)) if row.s_exon in x.tolist() else x,axis=1).dropna(axis=0, how = 'all') 
                for i in range(len(p3_exons)):
                    mask = following_exons.isin(p3_exons.iloc[i].dropna().tolist())   
                    following_exons_i = following_exons[[True if True in mask.iloc[i].tolist() else(False) for i in range(len(mask))]]
                    if  not following_exons_i.empty:
                        following_exons_i = following_exons_i[~following_exons_i[0].isin(p3_exons.iloc[i].tolist())]# delete those rows, where direct link from one of descendants of s_exon to possible alternative s-exon exsists
                        mask = following_exons_i.isin(p3_exons.iloc[i].dropna().tolist()) 
                        mask = mask.apply(shortest_alternative_path,axis = 1)   
                        #here shouldn't always be the first True # TPM1 9_0 should check first if thers direct link to that first
                        for mask_elem in range(len(mask)):
                            if pd.isnull(following_exons_i.iloc[mask_elem][following_exons_i.columns[0:mask.iloc[mask_elem]+1]][1]):
                                continue
                            else:
                                path_ending = following_exons_i.iloc[mask_elem][following_exons_i.columns[mask.iloc[mask_elem]]]
                                path = [row.S_exonID_5p]+[s_exon_name]+p3_exons.iloc[i].tolist()[:p3_exons.iloc[i].tolist().index(path_ending)+1]
                                alt_path = [row.S_exonID_5p]+following_exons_i.iloc[mask_elem][following_exons_i.columns[0:mask.iloc[mask_elem]+1]].tolist()

                                if (','.join(path) in alternative_paths_rnaseq.paths.tolist()) & (','.join(alt_path) in alternative_paths_rnaseq.alt_paths.tolist()):
                                    continue
                                else:
                                    species_path = check_path_in_species(path)
                                    species_alt_path = check_path_in_species(alt_path) 
                                    #if (len(species_path)>1)&(len(species_alt_path)>1):
                                    path_values = calculate_path_value(path,species_path,'E')
                                    alt_path_values = calculate_path_value(alt_path,species_alt_path,'E')
                                    alternative_paths_rnaseq = alternative_paths_rnaseq.append(pd.Series({'paths': ','.join(path),'alt_paths': ','.join(alt_path),
                                    'path_species':','.join(species_path),'alt_path_species':','.join(species_alt_path),
                                    'path_values':path_values,'alt_path_values':alt_path_values,'type':'E','idE':s_exon_name}),sort = False,ignore_index = True)
            
            return alternative_paths_rnaseq.loc[[alternative_paths_rnaseq.index[i] for i in range(len(alternative_paths_rnaseq)) if (len(alternative_paths_rnaseq.iloc[i].path_species.split(','))>1)&(len(alternative_paths_rnaseq.iloc[i].alt_path_species.split(','))>1)]]   

        Species = ['homo_sapiens','xenopus_tropicalis','mus_musculus','danio_rerio','bos_taurus','gorilla_gorilla','macaca_mulatta','monodelphis_domestica', 'ornithorhynchus_anatinus', 'rattus_norvegicus','sus_scrofa']
        parent = exonstable[(exonstable.S_exonID_3p==s_exon_name)& pd.notnull(exonstable.S_exonID_5p)][['Species','S_exonID_5p','S_exonID_3p']]      
        child = exonstable[(exonstable.S_exonID_5p==s_exon_name)& pd.notnull(exonstable.S_exonID_3p)][['Species','S_exonID_5p','S_exonID_3p']]      
        for i in Species:
            cluster = check_cluster(s_exon_name,i)
            if cluster!=0:
                for sub_exon in cluster:
                    child = child.append(pd.Series({'Species':i, 'S_exonID_5p':s_exon_name,'S_exonID_3p':sub_exon}),ignore_index=True, sort= False)
        for i in Species:
            cluster = check_cluster_down(s_exon_name,i)
            if cluster!=0:
                for sub_exon in cluster:
                    parent = parent.append(pd.Series({'Species':i, 'S_exonID_5p':sub_exon,'S_exonID_3p':s_exon_name}),ignore_index=True, sort= False)
        
        parent = parent[parent.S_exonID_3p!=0]
        parent = parent[~parent.duplicated()]
        child = child[child.S_exonID_3p!=0]
        child = child[~child.duplicated()]
        parent = parent.rename(columns = {'S_exonID_3p':'s_exon'})  
        child = child.rename(columns = {'S_exonID_5p':'s_exon'})  
        junctions = parent.join(child.set_index(['Species','s_exon']), how = 'inner',on = ['Species','s_exon']) 
        alternative_paths_rnaseq = pd.DataFrame(columns = ['paths','alt_paths','path_species','alt_path_species','path_values','alt_path_values'], index =[])
        if not junctions.empty:
            for row in range(len(junctions)):
                if event_type =='I':
                    alternative_paths_rnaseq = check_new_insertion(junctions.iloc[row],alternative_paths_rnaseq)   
                else:
                    alternative_paths_rnaseq = check_new_m_exclusive(junctions.iloc[row],alternative_paths_rnaseq)   
        return alternative_paths_rnaseq


    def path_in_homologs(path):
        path =  path.split(',')
        indexes_possible_path = homologs[homologs.S_exonID.isin(path)].index.tolist()
        path_transcripts = []
        possible_indexes_path = []
        for i in range(len(indexes_possible_path)-(len(path)-1)): 
            val = 0
            for k in range(1,len(path)):
                if indexes_possible_path[i] == indexes_possible_path[i+k]-k:  
                    val+=1
            if val == len(path)-1:
                possible_indexes_path.append(indexes_possible_path[i]) 
        for ind in possible_indexes_path:
            if homologs.loc[ind:ind+len(path)-1].S_exonID.tolist()==path:
                path_transcripts.append(homologs.loc[ind].TranscriptIDCluster)
        return path_transcripts

    exons = list(set(homologs.S_exonID.tolist()))      
    for exon in exons:
        output = output.append(event(gene,exon,'I'),sort = False)
        output = output.append(event(gene,exon,'E'),sort = False)
    if not output.empty:
        output = output.reset_index(drop = True) 
        output = output.assign(gene =gene,tr_path = output.apply(lambda x: ','.join(path_in_homologs(x.paths)),axis =1),
                                tr_alt_path = output.apply(lambda x: ','.join(path_in_homologs(x.alt_paths)),axis =1))   
    return output


def main():
    f = open('/home/sofya/Documents/TranscriptAnnotation/benchmark_list.txt','r')    
    genes = f.read()
    f.close()
    genes =genes.split('\n')  
    genes = [i for i in genes if i!='']
    
    for gene in genes:

        output = pd.DataFrame()
        output = gene_check(gene,output)
        if not output.empty:
            output =output[['gene','idE','type','paths', 'alt_paths', 'path_species', 'alt_path_species', 'path_values','alt_path_values', 'tr_path','tr_alt_path']]     
            #output.to_csv('/home/sofya/Documents/TranscriptAnnotation/analysis/'+gene+'/rnaseq/ase_rnaseq.tsv', index = False, sep = '\t')    

if __name__ == '__main__':
    main()


