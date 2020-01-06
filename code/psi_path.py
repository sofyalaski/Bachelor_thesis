import pandas as pd
import numpy as np
import os 
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import gridspec
sns.set(rc={'axes.facecolor':'lightgray', 'figure.facecolor':'white'})  
cmap = sns.cm.rocket_r

def main():
    f = open('/home/sofya/Documents/BA/Bachelor_thesis/benchmark_list.txt','r')    
    genes = f.read()
    f.close()
    genes =genes.split('\n')  
    genes = [i for i in genes if i!=''] 
    tissues_groups = pd.read_csv('/home/sofya/Documents/tissues_commented.tsv',sep = '\t') 
    tissue_order = tissues_groups[['tissue','category']].sort_values(by = 'category').tissue.tolist()    


    for gene in genes:        
        print(gene, genes.index(gene)+1,'/',len(genes))
        file1 = '/home/sofya/Documents/BA/Bachelor_thesis/analysis/'+gene+'/rnaseq/merge_homologs_norm_counts.tsv'
        file2 ='/home/sofya/Documents/BA/Bachelor_thesis/analysis/'+gene+'/rnaseq/tissue_counts_all.tsv'
        file3 = '/home/sofya/Documents/BA/Bachelor_thesis/analysis/'+gene+'/rnaseq/ase_rnaseq.tsv'
        if (os.path.isfile(file1))&(os.path.isfile(file2))&(os.path.isfile(file3)):
            exonstable = pd.read_csv(file1,sep = '\t')
            tissue_counts = pd.read_csv(file2,sep = '\t')
            ase = pd.read_csv(file3, sep = '\t')

            ase = ase[['gene','idE','paths','alt_paths','path_species','alt_path_species']]  

            group_ind = pd.Series(index = range(len(ase)))
            groups = dict()
            node_start = ase.iloc[0].alt_paths.split(',')[0]#list(set(ase.iloc[0].paths.split(',')+ase.iloc[0].alt_paths.split(','))) 
            node_end = ase.iloc[0].alt_paths.split(',')[-1]
            groups['1'] = dict()
            groups['1']['start'] = [node_start] 
            groups['1']['end'] = [node_end] 
            group_ind.iloc[0] = 1
            for i in range(1,len(ase)):
                node_start = ase.iloc[i].alt_paths.split(',')[0]
                node_end = ase.iloc[i].alt_paths.split(',')[-1]
                #nodes = list(set(ase.iloc[i].paths.split(',')+ase.iloc[i].alt_paths.split(','))) 
                val = False
                for key in list(groups.keys()):
                    if node_start in groups[key]['start'] or node_end in groups[key]['end']:
                        group_ind.iloc[i] = int(key)
                        if node_start not in groups[key]['start']:
                            groups[key]['start'] = groups[key]['start']+[node_start]
                        if node_end not in groups[key]['end']:
                            groups[key]['end'] = groups[key]['end']+[node_end]
                        val = True
                if val ==False:
                    new_key = str(int(list(groups.keys())[-1])+1)
                    groups[new_key] = dict()
                    groups[new_key]['start'] = [node_start]
                    groups[new_key]['end'] = [node_end]
                    group_ind.iloc[i] = int(key)+1

            ase = ase.assign(group = group_ind) 
            

            def pathcost(path,specie):
                path = path.split(',')
                path_value = pd.DataFrame()
                for junction in range(len(path)-1):
                    donor = path[junction]
                    acceptor = path[junction+1]
                    a = tissue_counts[(tissue_counts.Species==specie)&(tissue_counts.S_exonID_5p == donor)&(tissue_counts.S_exonID_3p==acceptor)].dropna(how = 'all',axis =1)  
                    if a.empty:#experiments = ','.join(a.Experiment_ID.tolist())     
                        continue
                    a = a.drop(columns = ['TranscriptIDCluster_5p', 'ExonIDCluster_5p', 'S_exonID_5p','TranscriptIDCluster_3p', 'ExonIDCluster_3p', 'S_exonID_3p', 'Species','Experiment_ID','n_lib'])   
                    a = a.mean().to_frame().T   
                    path_value = path_value.append(a, sort = False)
                path_value = path_value.mean(skipna=False).to_frame().T.dropna(axis=1).assign(path = ','.join(path))
                return path_value

            
            def delete_subpath(paths):
                paths.sort(key = len)
                paths = [path.split(',') for path in paths]
                to_remove = []
                for i in range(len(paths)):
                    for j in range(i+1,len(paths)):
                        ind = []
                        for elem in paths[i]:
                            if elem in paths[j]:
                                ind.append(paths[j].index(elem))
                            else:
                                break
                        
                        if ind:
                            if ind == list(range(ind[0],ind[0]+len(paths[i]))):
                                to_remove.append(i)
                to_remove = list(set(to_remove))
                to_remove.reverse()
                for j in to_remove:
                    del paths[j]
                paths = [','.join(path) for path in paths]
                return paths

            '''def find_edges(paths):
                paths = [i.split(',') for i in paths]
                edges = []
                for i in range(len(paths)):
                    for j in range(len(paths[i])-1):
                        edges.append(paths[i][j]+','+paths[i][j+1])
                edges = list(set(edges))
                return edges'''



            def find_full_path(unfull_path, paths_df):
                paths_df = paths_df.drop(paths_df[paths_df.path == unfull_path].index)
                start = paths_df.groupby('f').size().idxmax()# where most of paths start
                if start !=unfull_path.split(',')[0]:
                    print('start node is not included in this path')
                    path_start = [i for i in paths if (start in i.split(','))&(unfull_path.split(',')[0] in i.split(','))]  
                    path_start = [','.join(i.split(',')[0:i.split(',').index(unfull_path.split(',')[0])]) for i in path_start]   
                    path_start = list(set(path_start))
                    new_paths =  [','.join([i]+[unfull_path]) for i in path_start]
                else:
                    print('end node is not included in this path')
                    end = max(paths_df.groupby('l').size().tolist())
                    end = (paths_df.groupby('l').size()==end).index.tolist() 
                    for i in range(len(paths_df)): 
                        if len(list(set(paths_df.iloc[i].path.split(','))&set(end)))==len(end): 
                            #print(paths_df.iloc[i].path) 
                            #print(min([paths_df.iloc[i].path.split(',').index(j) for j in end])) 
                            end = paths_df.iloc[i].path.split(',')[min([paths_df.iloc[i].path.split(',').index(j) for j in end])]
                            break 
                    path_end = [i for i in paths if (end in i.split(','))&(unfull_path.split(',')[-1] in i.split(','))]  
                    path_end = [','.join(i.split(',')[i.split(',').index(unfull_path.split(',')[-1])+1 :i.split(',').index(end)+1]) for i in path_end]   
                    path_end = list(set(path_end))
                    new_paths =  [','.join([unfull_path]+[i]) for i in path_end]
                for new_path in new_paths:
                    if new_path[-1]==',':
                        new_path = new_path[:-1]
                    if new_path[0]==',':
                        new_path = new_path[1:]
                    if new_path not in paths_df.path.tolist():
                        paths_df = paths_df.append(pd.Series({'path':new_path,'f':new_path.split(',')[0],'l':new_path.split(',')[-1]}), sort = False, ignore_index = True)
                return paths_df


            output = pd.DataFrame()
            for group,data in ase.groupby('group'):
                #divide into groups that show events including equal nodes
                group = int(group)
                all_species = list(set([item for sublist in (data.path_species.str.split(',').tolist()+data.alt_path_species.str.split(',').tolist()) for item in sublist]))  
                all_data = pd.DataFrame()
                
                for specie in all_species:
                    #paths which are exclusive in path/alt_path?
                    paths = data[data.path_species.str.contains(specie)].paths.tolist()+data[data.alt_path_species.str.contains(specie)].alt_paths.tolist()    
                    # delete paths which are in reality subpaths of some other path
                    paths = delete_subpath(paths)      
                    if paths:
                        # divide into subgroups having equal start and end nodes, so that PSI not biased
                        paths_df =  pd.DataFrame({'path':paths,'f' : [i.split(',')[0] for i in paths],'l':[i.split(',')[-1] for i in paths]}) 
                        if len(paths_df)>1:
                            path_not_full = paths_df.groupby(['f','l'])['path'].apply(lambda x: list(x)).tolist() 
                            path_not_full = [i for i in path_not_full if len(i)==1] 

                            for unfull_path in path_not_full:
                                #print(specie, unfull_path[0])
                                paths_df = find_full_path(unfull_path[0],paths_df)
                        #new
                        lasts = list(set(paths_df.l)) 
                        for last in range(len(lasts)):
                            temp = paths_df.iloc[list(set([i for i in range(len(paths_df)) if lasts[last] in paths_df.iloc[i].path.split(',')]) & set(paths_df[paths_df.l!=lasts[last]].index.tolist()))]  
                            if not temp.empty:
                                paths_not_full = paths_df[paths_df.l==lasts[last]].path.tolist()  
                                paths_df = paths_df.drop(paths_df[paths_df.l == lasts[last]].index)  
                                next_exons = list(set([','.join(temp.path.iloc[i].split(',')[temp.path.iloc[i].split(',').index(lasts[last]) +1:]) for i in range(len(temp))]))
                                for i in range(len(paths_not_full)):
                                    new_path = ','.join([paths_not_full[i]]+next_exons)
                                    if new_path not in paths_df.path.tolist():
                                        paths_df = paths_df.append(pd.Series({'path': new_path,'f': new_path.split(',')[0],'l':new_path.split(',')[-1]}), sort = False, ignore_index = True)
                        firsts = list(set(paths_df.f)) 
                        for first in range(len(firsts)):
                            temp = paths_df.iloc[list(set([i for i in range(len(paths_df)) if firsts[first] in paths_df.iloc[i].path.split(',')]) & set(paths_df[paths_df.f!=firsts[first]].index.tolist()))]  
                            if not temp.empty:
                                paths_not_full = paths_df[paths_df.f==firsts[first]].path.tolist()  
                                paths_df = paths_df.drop(paths_df[paths_df.f == firsts[first]].index)  
                                first_exons = list(set([','.join(temp.path.iloc[i].split(',')[:temp.path.iloc[i].split(',').index(firsts[first])]) for i in range(len(temp))]    ))
                                for i in range(len(paths_not_full)):
                                    new_path = ','.join(first_exons+[paths_not_full[i]])
                                    if new_path not in paths_df.path.tolist():
                                        paths_df = paths_df.append(pd.Series({'path': new_path,'f': new_path.split(',')[0],'l':new_path.split(',')[-1]}), sort = False, ignore_index = True)
                        

                        for name, subgroup in paths_df.groupby(['f','l']):
                            #if len(subgroup)<2:
                            #    continue
                            path_values = pd.DataFrame()
                            for path in subgroup.path.tolist():
                                path_values = path_values.append(pathcost(path,specie),sort = False)
                            path_values = path_values.set_index('path')
                            path_values = path_values.append(pd.Series(path_values.apply(lambda x: x.sum()),name = 'col_sum'))
                            cols = path_values.columns.tolist()

                            path_values = path_values.iloc[0:-1].apply(lambda x: x/path_values.iloc[-1],axis =1).assign(Species = specie)  
                            all_data = all_data.append(path_values,sort = False)
                            path_values = path_values.reset_index()


                all_data = all_data.reset_index().sort_values(by = 'Species')
                output = output.append(all_data, sort = False, ignore_index = True)

                paths = list(set(all_data.path.tolist()))  
                paths_df =  pd.DataFrame({'path':paths,'f' : [i.split(',')[0] for i in paths],'l':[i.split(',')[-1] for i in paths]}).sort_values(by = ['f','l'])       
                paths = paths_df.path.tolist()
                path_dict = {paths[i]:'path '+str(i+1) for i in range(len(paths))} 
                all_data = all_data.assign(path = [path_dict[i] for i in all_data.path.tolist()])   
                all_data = all_data.assign(Species = all_data.Species.str.capitalize().str.slice(0,1)+'_'+all_data.Species.str.split('_').str[1].str.slice(0,1)).sort_values(by = ['Species','path']).set_index(['Species','path'])    
                all_data = all_data[[i for i in tissue_order if i in all_data.columns.tolist()]]
                col_dict= {'embryonic stem cell': 'ESC',
                            'prefrontal cortex': 'PFC',
                            'brown adipose tissue': 'BAT',
                            'thoracic mammary gland': 'mammary gland',
                            'bone marrow macrophage': 'BMM',
                            'heart left ventricle': 'left ventricle',
                            'skeletal muscle tissue': 'skeletal muscle',
                            'adult mammalian kidney': 'adult_kidney',
                            'multi-cellular organism': 'multi-cellular'}

                all_data.columns = [i if i not in list(col_dict.keys()) else (col_dict[i]) for i in all_data.columns.tolist()]

                if not all_data.empty:

                    fig, axn = plt.subplots(1, 2, figsize = (16,9))
                    fig.text(0.02,0.02, '\n'.join([i[1]+' : '+i[0] for i in list(path_dict.items())]), fontsize =12)    
                    cbar_kws = dict(use_gridspec=False, orientation='horizontal')
                    cbar_ax = fig.add_axes([.25, .1, .5, .04])

                    for i, ax in enumerate(axn.flat):
                        sns.heatmap(ax=ax, data=all_data, xticklabels=True, cbar=i == 0, cbar_kws=None if i else cbar_kws, cbar_ax=None if i else cbar_ax, yticklabels=True,square = True,cmap = cmap)
                        ax.hlines(all_data.index.get_level_values(level = i).value_counts().sort_index().cumsum().tolist()[:-1], *ax.get_xlim(),color = 'maroon')
                        ax.set_ylabel('')    
                        ax.set_xlabel('')
                        ylims = ax.get_ylim()
                        ylims = (ylims[0]+0.5,ylims[1]-0.5) 
                        ax.set_ylim(ylims)
                        ax.set_xticklabels(ax.get_xticklabels())
                        all_data = all_data.sort_index(level =1)#first plot was sorted by species, second will be sorted by path
                    fig.suptitle('Heatmap of ASE psi values in '+ gene+ ' in event '+ str(group), fontsize=15)
                    fig.subplots_adjust(wspace = 0.3, left = .125, right = .975)

                    #plt.savefig(file3[0:-21]+'plots/heatmap_both_'+str(group)+'.pdf')
                    plt.close()

                    
            output.to_csv(file3[:-10]+'tissue_grouped.tsv')



if __name__ == '__main__':
    main()
                        

