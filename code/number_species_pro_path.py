import pandas as pd
import numpy as np
import itertools
import math
from collections import defaultdict 

ase = pd.read_csv('/home/sofya/Documents/TranscriptAnnotation/analysis/ase_list_new.txt',sep = '\t',index_col=0)


def event(s_exon_name, gene,event_type,event_id):
    print(gene,s_exon_name)
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
    

    def find_ancestral_exons(row):
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
        return homologs[(homologs.TranscriptIDCluster == row.TranscriptIDCluster)&(homologs.S_exon_Rank.isin(ranks_array))].S_exonID.tolist()

    def check_cluster(s_exon,Specie):
        """Find a following s_exon that is inside of the same cluster for given Specie. Searches in s_exons_table."""
        if s_exon in [s_exon for clst in exon_clusters[exon_clusters.Species==Specie].S_exonID for s_exon in clst]:
            for i in range(len(exon_clusters[exon_clusters.Species==Specie])): 
                if s_exon in exon_clusters[exon_clusters.Species==Specie].S_exonID.iloc[i]: 
                    new_ind = exon_clusters[exon_clusters.Species==Specie].iloc[i].S_exonID.index(s_exon)+1 
                    if new_ind == len(exon_clusters[exon_clusters.Species==Specie].S_exonID.iloc[i]):
                        return 0 #last inside one cluster
                    else:
                        return exon_clusters[exon_clusters.Species==Specie].iloc[i].S_exonID[new_ind]
                        break 
        else:
            return 0

        def check_cluster_down(s_exon,Specie):
            """Find a following s_exon that is inside of the same cluster for given Specie. Searches in s_exons_table."""
            if s_exon in [s_exon for clst in exon_clusters[exon_clusters.Species==Specie].S_exonID for s_exon in clst]:
                for i in range(len(exon_clusters[exon_clusters.Species==Specie])): 
                    if s_exon in exon_clusters[exon_clusters.Species==Specie].S_exonID.iloc[i]: 
                        new_ind = exon_clusters[exon_clusters.Species==Specie].iloc[i].S_exonID.index(s_exon)-1 
                        if new_ind == len(exon_clusters[exon_clusters.Species==Specie].S_exonID.iloc[i]):
                            return 0 #last inside one cluster
                        else:
                            return exon_clusters[exon_clusters.Species==Specie].iloc[i].S_exonID[new_ind]
                            break 
            else:
                return 0

    def check_next_exonstable(row):
        further_exons_df = pd.DataFrame(row.S_exonID_3p,index= [0],columns = [0])    
        next_exon = list(set(exonstable[(exonstable.Species==row.Species)&(exonstable.S_exonID_5p ==row.S_exonID_3p)&(pd.notnull(exonstable.S_exonID_3p))].S_exonID_3p))
        next_exon.append(check_cluster(further_exons_df.iloc[0][0],row.Species))
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
                    next_exon.append(check_cluster(further_exons_df[i-1].iloc[j],row.Species))
                    next_exon = [val for val in next_exon if val!=0]
                    if next_exon:
                        dupl = pd.concat([further_exons_df.iloc[[j]]]*len(next_exon),ignore_index = True)
                        dupl[i] = next_exon 
                        further_exons_df = further_exons_df.drop(j)
                        further_exons_df = pd.concat([further_exons_df,dupl],ignore_index = True)
        return further_exons_df
    

    def check_exon_skipping(alt_s_exon_s_exon,row):### rewrite into insertion?
        if alt_s_exon_s_exon in row.descendants:
            order = pd.Series([row.s_exon]+row.descendants[:row.descendants.index(alt_s_exon_s_exon)])
            if True in  [order.isin(i).all() for i in exon_clusters[exon_clusters.Species==row.Species].S_exonID]:
                return True
            else:
                return False
        else:
            return False

    def shortest_alternative_path(mask_row):
        return mask_row.tolist().index(True)    

    def transcript_with_path_in_homologs(indexes_possible_path, path):
        """Find index in s-exon_table file where the given path begins. Takes indexes where the s_exons of path show uup as well as path itself."""
        path_transcripts = []
        if path[0] == 'start':
            path = path[1:]
            path_starts = homologs.loc[indexes_possible_path][(homologs.loc[indexes_possible_path].S_exon_Rank ==1)&(homologs.loc[indexes_possible_path].S_exonID==path[0])] 
            for path_start in range(len(path_starts)):
                val = 0
                for j in range(len(path[1:])): 
                    if homologs.loc[path_starts.iloc[path_start].name+j+1].S_exonID==path[1:][j]:
                        val+=1
                if val == len(path)-1:
                    path_transcripts.append(path_starts.iloc[path_start].TranscriptIDCluster) 
        elif path[-1] =='end':
            print('end!')
        else:
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


    def check_old_insertion(row,alternative_paths):
        if row.ancestors=='start':
            descendants_in = list(set(homologs[(homologs.S_exonID.isin(row.descendants))&(homologs.S_exon_Rank ==1)].S_exonID))   
            if descendants_in:
                skippings = [descendants_in[[row.descendants.index(i) for i in descendants_in].index(min([row.descendants.index(i) for i in descendants_in]))]]
            else: 
                skippings = []
        else:
            #anc = homologs[(homologs.Species == row.Species)&(homologs.S_exonID==row.ancestors)]
            anc = homologs[homologs.S_exonID==row.ancestors]
            skippings = []
            for tr in range(len(anc)):
                descendants_in = homologs[(homologs.S_exonID.isin(row.descendants))&(homologs.TranscriptIDCluster==anc.iloc[tr].TranscriptIDCluster)]
                skippings += descendants_in[descendants_in.S_exon_Rank-1==anc.iloc[tr].S_exon_Rank].S_exonID.tolist()
        if skippings:    
            skippings = list(set(skippings))
            for j in skippings:
                path =  [row.ancestors]+[s_exon_name]+row.descendants[:row.descendants.index(j) + 1]
                path_transcripts = []
                alt_path = [row.ancestors]+[j]
                if (','.join(path) in alternative_paths.paths.tolist()) & (','.join(alt_path) in alternative_paths.alt_paths.tolist()):
                    continue
                alt_path_transcripts = []
                indexes_possible_path = homologs[homologs.S_exonID.isin(path)].index.tolist()
                indexes_possible_alt_path = homologs[homologs.S_exonID.isin(alt_path)].index.tolist()
                transcripts_path = transcript_with_path_in_homologs(indexes_possible_path, path)
                transcripts_alt_path = transcript_with_path_in_homologs(indexes_possible_alt_path, alt_path)
                transcripts_path.sort()
                transcripts_alt_path.sort()
                alternative_paths = alternative_paths.append(pd.Series({'paths': ','.join(path), 'alt_paths': ','.join(alt_path),
                                    'tr_path':','.join(transcripts_path), 'tr_alt_path':','.join(transcripts_alt_path)}),sort = False, ignore_index = True)
        return alternative_paths

    def check_old_m_exclusive(row,alternative_paths):
        #anc = homologs[(homologs.Species == row.Species)&(homologs.S_exonID==row.ancestors)][['Species','TranscriptIDCluster','S_exonID', 'S_exon_Rank']]
        anc = homologs[homologs.S_exonID==row.ancestors][['Species','TranscriptIDCluster','S_exonID', 'S_exon_Rank']]

        for tr in range(len(anc)):
            alt_s_exon = homologs[(homologs.TranscriptIDCluster==anc.iloc[tr].TranscriptIDCluster)&(homologs.S_exon_Rank ==anc.iloc[tr].S_exon_Rank+1)][['Species','TranscriptIDCluster','S_exonID', 'S_exon_Rank']]
            alt_s_exon = alt_s_exon.drop(alt_s_exon[alt_s_exon.S_exonID==row.s_exon].index)
            not_insertions = alt_s_exon.apply(lambda x: check_exon_skipping(x.S_exonID, row),axis=1)  
            alt_s_exon = alt_s_exon[~not_insertions]
            if not alt_s_exon.empty:#the first part of alt s_exon is found, check second part
                for alt_exon in range(len(alt_s_exon)):
                    max_rank_for_transcript = max(homologs[homologs.TranscriptIDCluster == alt_s_exon.iloc[alt_exon].TranscriptIDCluster].S_exon_Rank)
                    if alt_s_exon.iloc[alt_exon].S_exon_Rank + 10 > max_rank_for_transcript:
                        ranks_array = list(range(alt_s_exon.iloc[alt_exon].S_exon_Rank+1,max_rank_for_transcript+1))
                    else:
                        ranks_array = list(range(alt_s_exon.iloc[alt_exon].S_exon_Rank+1, alt_s_exon.iloc[alt_exon].S_exon_Rank+11))#check up to ten next exons
                    following_alt_s_exon = homologs[(homologs.TranscriptIDCluster==alt_s_exon.iloc[alt_exon].TranscriptIDCluster)&(homologs.S_exon_Rank.isin(ranks_array))].S_exonID.tolist()       
                    a = homologs[(homologs.S_exonID.isin(following_alt_s_exon))&(homologs.TranscriptIDCluster==alt_s_exon.iloc[alt_exon].TranscriptIDCluster)][['TranscriptIDCluster','S_exonID','S_exon_Rank']]    
                    b = homologs[(homologs.S_exonID.isin(row.descendants))&(homologs.TranscriptIDCluster==alt_s_exon.iloc[alt_exon].TranscriptIDCluster)][['TranscriptIDCluster','S_exonID','S_exon_Rank']]     
                    a = a.assign(S_exon_Rank = a.S_exon_Rank+1)
                    if (a.empty)|(b.empty):
                        continue
                    elif a.empty:
                        cons = b.set_index(['TranscriptIDCluster','S_exon_Rank']).rename(columns={'S_exonID':'S_exonID_acceptor'}).sort_values(by = ['TranscriptIDCluster','S_exon_Rank']).assign(S_exonID_donor = np.nan)
                    else:
                        cons = a.join(b.set_index(['TranscriptIDCluster','S_exon_Rank']), how = 'inner', on = ['TranscriptIDCluster','S_exon_Rank'], lsuffix = '_donor',rsuffix = '_acceptor').sort_values(by = ['TranscriptIDCluster','S_exon_Rank'])  
                    if cons.empty:
                        continue
                    chain_following_s_exons = following_alt_s_exon[0:following_alt_s_exon.index(cons.iloc[0].S_exonID_donor)]
                    if row.s_exon in [alt_s_exon.iloc[alt_exon].S_exonID]+chain_following_s_exons+[cons.iloc[0].S_exonID_donor]+[cons.iloc[0].S_exonID_acceptor]:
                        continue
                    else: 
                        if cons.S_exonID_donor.iloc[0] in row.descendants:
                            if following_alt_s_exon.index(cons.S_exonID_acceptor.iloc[0]) - following_alt_s_exon.index(cons.S_exonID_donor.iloc[0]) == row.descendants.index(cons.S_exonID_acceptor.iloc[0]) - row.descendants.index(cons.S_exonID_donor.iloc[0]):
                                alt_path = [row.ancestors]+[alt_s_exon.iloc[alt_exon].S_exonID]+chain_following_s_exons+[cons.iloc[0].S_exonID_donor]
                                path = [row.ancestors]+[row.s_exon]+row.descendants[:row.descendants.index(cons.iloc[0].S_exonID_donor)+1]
                            else:    
                                alt_path = [row.ancestors]+[alt_s_exon.iloc[alt_exon].S_exonID]+chain_following_s_exons+[cons.iloc[0].S_exonID_donor]+[cons.iloc[0].S_exonID_acceptor]
                                path = [row.ancestors]+[row.s_exon]+row.descendants[:row.descendants.index(cons.iloc[0].S_exonID_acceptor)+1]
                        else:
                                alt_path = [row.ancestors]+[alt_s_exon.iloc[alt_exon].S_exonID]+chain_following_s_exons+[cons.iloc[0].S_exonID_donor]+[cons.iloc[0].S_exonID_acceptor]
                                path = [row.ancestors]+[row.s_exon]+row.descendants[:row.descendants.index(cons.iloc[0].S_exonID_acceptor)+1]
                        if (','.join(path) in alternative_paths.paths.tolist()) & (','.join(alt_path) in alternative_paths.alt_paths.tolist()):
                            continue
                        else:
                            indexes_possible_path = homologs[homologs.S_exonID.isin(path)].index.tolist()
                            indexes_possible_alt_path = homologs[homologs.S_exonID.isin(alt_path)].index.tolist()
                            transcripts_path = transcript_with_path_in_homologs(indexes_possible_path, path)
                            transcripts_alt_path = transcript_with_path_in_homologs(indexes_possible_alt_path, alt_path)
                            transcripts_path.sort()
                            transcripts_alt_path.sort()
        
                    alternative_paths = alternative_paths.append(pd.Series({'paths':','.join(path),'alt_paths':','.join(alt_path),'tr_path':','.join(transcripts_path),'tr_alt_path':','.join(transcripts_alt_path)}),sort = False, ignore_index = True)
        return alternative_paths

    def check_path_in_species(path):
        species = []
        for node in range(len(path)-1):
            from_junctions = list(set(exonstable[(exonstable.S_exonID_5p==path[node])&(exonstable.S_exonID_3p==path[node+1])].Species))
            from_junctions+=[i  for i in Species if check_cluster(path[node], i)!=0 ]     # add the links connected via intercluster junctions
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

                path_values = calculate_path_value(paths,species_path,'I')     
                alt_path_values = calculate_path_value(alt_paths,species_alt_path,'I') 
                ordering = ordering.append(pd.DataFrame({'paths': [','.join(j)for j in paths] ,'alt_paths': [','.join(j)for j in alt_paths],
                        'path_species':[','.join(sorted(j))for j in species_path],'alt_path_species':[','.join(sorted(j))for j in species_alt_path],
                        'path_values':path_values,'alt_path_values':alt_path_values}),sort = False)
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

                                path_values = calculate_path_value(path,species_path,'E')
                                alt_path_values = calculate_path_value(alt_path,species_alt_path,'E')
                                alternative_paths_rnaseq = alternative_paths_rnaseq.append(pd.Series({'paths': ','.join(path),'alt_paths': ','.join(alt_path),
                                'path_species':','.join(sorted(species_path)),'alt_path_species':','.join(sorted(species_alt_path)),
                                'path_values':path_values,'alt_path_values':alt_path_values}),sort = False,ignore_index = True)
        return alternative_paths_rnaseq

    indexes = homologs[homologs.S_exonID == s_exon_name].index
    temp = homologs.loc[indexes]
    temp = temp.assign(ancestors = homologs.loc[indexes].apply(find_ancestral_exons,axis=1))
    temp['s_exon'] = s_exon_name  
    temp = temp.assign(descendants = homologs.loc[indexes].apply(find_descendent_exons,axis=1))
    temp = temp[['Species','ancestors','s_exon','descendants']]#[(temp.ancestors!='start')&(temp.descendants!='end')]   
    temp = temp[pd.notnull(temp.ancestors)]
    alternative_paths = pd.DataFrame(columns = ['paths','alt_paths','tr_path','tr_alt_path'], index =[])
    if not temp.empty:
        if event_type == 'I':
            for row in range(len(temp)):
                alternative_paths = check_old_insertion(temp.iloc[row],alternative_paths)
        else:
            for row in range(len(temp)):
                alternative_paths = check_old_m_exclusive(temp.iloc[row],alternative_paths)
        if not alternative_paths.empty:
            alternative_paths = alternative_paths[~alternative_paths.duplicated()]   
        
    Species = ['homo_sapiens','xenopus_tropicalis','mus_musculus','danio_rerio','bos_taurus','gorilla_gorilla','macaca_mulatta','monodelphis_domestica', 'ornithorhynchus_anatinus', 'rattus_norvegicus','sus_scrofa']
    parent = exonstable[(exonstable.S_exonID_3p==s_exon_name)& pd.notnull(exonstable.S_exonID_5p)][['Species','S_exonID_5p','S_exonID_3p']]      
    child = exonstable[(exonstable.S_exonID_5p==s_exon_name)& pd.notnull(exonstable.S_exonID_3p)][['Species','S_exonID_5p','S_exonID_3p']]      
    for i in Species:
        child = child.append(pd.Series({'Species':i, 'S_exonID_5p':s_exon_name,'S_exonID_3p':check_cluster(s_exon_name,i)}),ignore_index=True, sort= False)
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
       

    if (alternative_paths.empty) & (alternative_paths_rnaseq.empty):
        print('empty')        
        output = pd.DataFrame(columns = ['id','gene','s_exonID','type','paths', 'alt_paths', 'tr_path', 'tr_alt_path', 'path_species','alt_path_species', 'path_values', 'alt_path_values'], index =[])
    elif alternative_paths_rnaseq.empty:
        output = alternative_paths.assign(event_id=event_id, gene = gene, s_exonID=s_exon_name,type = event_type,path_species = np.nan,alt_path_species = np.nan, path_values = np.nan, alt_path_values= np.nan)
    elif alternative_paths.empty:
        output = alternative_paths_rnaseq.assign(event_id=event_id, gene = gene, s_exonID=s_exon_name,type = event_type,tr_path = np.nan, tr_alt_path = np.nan)
    else:
        output = alternative_paths.join(alternative_paths_rnaseq.set_index(['paths','alt_paths']), how = 'outer', on = ['paths','alt_paths'])
        output = output.assign(event_id=event_id, gene=gene,s_exonID=s_exon_name,type = event_type)
    if not output.empty:
        output = output[['event_id','gene','s_exonID','type','paths', 'alt_paths', 'tr_path', 'tr_alt_path', 'path_species','alt_path_species', 'path_values', 'alt_path_values']]
        output = output.assign(id = event_id, Ec_path = [len(list(set([i[0:6] for i in output.tr_path.iloc[row].split(',') if (i[3:6]!='MMU' and i[3:6]!='DAR')]))) if pd.notnull(output.tr_path.iloc[row]) else(0) for row in range(len(output))],
                                Ec_alt_path = [len(list(set([i[0:6] for i in output.tr_alt_path.iloc[row].split(',') if (i[3:6]!='MMU' and i[3:6]!='DAR')]))) if pd.notnull(output.tr_alt_path.iloc[row]) else(0) for row in range(len(output))],
                                Rc_path =  [len(output.iloc[row].path_species.split(','))  if pd.notnull(output.path_species.iloc[row]) else(0) for row in range(len(output))],
                                Rc_alt_path =  [len(output.iloc[row].alt_path_species.split(','))  if pd.notnull(output.alt_path_species.iloc[row]) else(0) for row in range(len(output))])    
        species_in_gene =  len(list(set(homologs.Species)))//2
        output = output[((output.Ec_path>=species_in_gene)&(output.Ec_alt_path>=species_in_gene))|((output.Rc_path>1)&(output.Rc_alt_path>1))] # with at least two species for each path
    return output

output = pd.DataFrame()
events = ase[(ase.type=='I')|(ase.type=='E')]
s_exons = events.idE_s_exon.str.split(',')  
s_exons = [s_exons.iloc[i][0] for i in range(len(s_exons))]
genes = events.idE.str.split('_')  
genes = [genes.iloc[i][0] for i in range(len(genes))]  
ids = events.id.tolist()
insert_pairs = [(gene,exon,event_type,event_id) for gene,exon,event_type,event_id in zip(genes,s_exons,events.type.tolist(),ids)]
output = output.append([event(pair[1],pair[0], pair[2],pair[3]) for pair in insert_pairs], sort = False)


output = output.reset_index(drop = True) 
species_name = {'ENST00':'homo_sapiens','ENSXET':'xenopus_tropicalis','ENSMUS':'mus_musculus','ENSDAR':'danio_rerio','ENSBTA':'bos_taurus',
                    'WBGene':'caenorhabditis_elegans', 'ENSGAL':'gallus_gallus','ENSGGO':'gorilla_gorilla','ENSMMU':'macaca_mulatta','ENSMOD':'monodelphis_domestica', 
                    'ENSOAN':'ornithorhynchus_anatinus', 'ENSRNO' : 'rattus_norvegicus','ENSSSC':'sus_scrofa'}
output = output.assign(E_path_species =  [','.join(sorted([species_name[name] for name in list(set([t[0:6] for t in i.split(',') if(t[3:6]!='MMU' and t[3:6]!='DAR')]))]))if pd.notnull(i) else(np.nan) for i in output.tr_path.tolist() ],
                       E_alt_path_species =  [','.join(sorted([species_name[name] for name in list(set([t[0:6] for t in i.split(',') if(t[3:6]!='MMU' and t[3:6]!='DAR')]))])) if pd.notnull(i) else(np.nan) for i in output.tr_alt_path.tolist() ]  )

output =output.assign(diff_path = output.Rc_path-output.Ec_path,diff_alt_path = output.Rc_alt_path-output.Ec_alt_path)  
#no_rna_support = output[pd.isnull(output.Species_rnaseq)].Species_Ensembl.str.split(',')  

output =output[['event_id','gene','s_exonID','type','paths', 'alt_paths', 'tr_path', 'tr_alt_path','E_path_species' ,'E_alt_path_species','path_species','alt_path_species', 'path_values', 'alt_path_values', 'Ec_path','Ec_alt_path','Rc_path', 'Rc_alt_path','diff_path','diff_alt_path']] 
output.to_csv('/home/sofya/Documents/TranscriptAnnotation/analysis/ase_list_detailed.tsv', index = False, sep = '\t')    



