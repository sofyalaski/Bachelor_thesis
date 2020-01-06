import pandas as pd 
import itertools
import sys


def conservation(exonstable, cluster):
    #n_tr = list(set(exonstable.TranscriptIDCluster_5p.tolist()+exonstable.TranscriptIDCluster_3p.tolist()))     
    #n_tr = len([i for i in n_tr if ~ pd.isnull(i)])
    #cons = len(list(set(exonstable[exonstable.S_exonID_5p==cluster].TranscriptIDCluster_5p.tolist()+ exonstable[exonstable.S_exonID_3p==cluster].TranscriptIDCluster_3p.tolist())))/n_tr*100
    cons = round(len(set(exonstable[(exonstable.S_exonID_5p==cluster)|(exonstable.S_exonID_3p==cluster)].Species))/9*10)#12/10, if taking all species into account
    return cons

def main():
    #f = open('/home/sofya/Documents/TranscriptAnnotation/benchmark/FMR1/thoraxe/splice_graph.gml','r')
    #exonstable = pd.read_csv('/home/sofya/Documents/TranscriptAnnotation/rnaseq/FMR1/Ensembl/merge_homologs_norm_counts.tsv',sep = '\t')
    exonstable = pd.read_csv(sys.argv[1],sep = '\t')
    exonstable =exonstable[exonstable.n_total_uq>1e-07]  
    if exonstable.start.count()==0:
        return 0 
    else:
        f = open(sys.argv[2], 'r')
        old_info = f.read()
        f.close()

    

        old_info = old_info.split('[\n                    ')[1:]#the 0th element ist graph information(irrelevant)
        old_info_lists = [i.split('                    ') for i in old_info]
        old_info_lists = [[i[0].split('\n')[0],i[1].split('\n')[0],i[2].split('\n')[0] ]for i in old_info_lists]   
        df = pd.DataFrame(old_info_lists)   

        nodes = df[df[0].str.slice(0,2)=='id']
        nodes = nodes.assign(id = nodes[0].str[3:],label = nodes[1].str[7:-1], conservation_old =nodes[2].str[13:].astype('float64'), in_old = True)
        nodes = nodes[['id','label','conservation_old','in_old']] 

        edges = df[df[0].str.slice(0,6)=='source']  
        edges = edges.assign(source = edges[0].str[7:],target = edges[1].str[7:], conservation_old =edges[2].str[13:].astype('float64'),in_old = True)
        edges = edges[['source','target','conservation_old','in_old']] 

        exon_clusters = list(set(exonstable.S_exonID_5p.tolist()+exonstable.S_exonID_3p.tolist())) 
        exon_clusters = [i for i in exon_clusters if not pd.isnull(i)]  

        nodes = nodes.assign(in_new = nodes.label.isin(exon_clusters))
        nodes = nodes.assign(conservation_rnaseq = pd.Series([conservation(exonstable,i)  for i in nodes.label]))# if the label not in new conservation then len of its' set equals to 0
        
        #nodes = nodes.append(pd.Series({'id':str(int(nodes.iloc[-1].id)+1),'label':'5_p','conservation_old':0,'in_old':False,'in_new':True,'conservation_rnaseq': 10.0}),sort = False, ignore_index  = True) 
        #nodes = nodes.append(pd.Series({'id':str(int(nodes.iloc[-1].id)+1),'label':'3_p','conservation_old':0,'in_old':False,'in_new':True,'conservation_rnaseq': 10.0}),sort = False, ignore_index  = True)
                
        unique_edges = list(set(list(zip(exonstable.S_exonID_5p,exonstable.S_exonID_3p))))  
        unique_edges = pd.DataFrame(unique_edges,columns =['S_exonID_5p','S_exonID_3p'])  
        unique_edges = unique_edges[pd.notnull(unique_edges.S_exonID_5p)&pd.notnull(unique_edges.S_exonID_3p)].reset_index(drop = True)

        label_dict=pd.Series(nodes.id.values,index=nodes.label.values).to_dict() 
        edges['in_new'] = ''        
        edges['conservation_rnaseq']=0
        for i in range(len(unique_edges)):
            source = unique_edges.loc[i].S_exonID_5p   
            target = unique_edges.loc[i].S_exonID_3p  
            if pd.isnull(source):
                edges=edges.append(pd.Series({'source':str(int(nodes[nodes.label=='5_p'].id)) ,'target':label_dict[target],'conservation_old':0,'in_old':False,'in_new':True,'conservation_rnaseq':int(nodes[nodes.id==label_dict[target]].conservation_rnaseq)}),sort = False, ignore_index  = True) 
            elif pd.isnull(target):
                edges=edges.append(pd.Series({'source':label_dict[source],'target':str(int(nodes[nodes.label=='3_p'].id)),'conservation_old':0,'in_old':False,'in_new':True,'conservation_rnaseq':int(nodes[nodes.id==label_dict[source]].conservation_rnaseq)}),sort = False, ignore_index  = True) 
            else:
                if edges[(edges.source==label_dict[source])&(edges.target==label_dict[target])].empty:
                    edges = edges.append(pd.Series({'source':label_dict[source],'target':label_dict[target],'conservation_old':0,'in_old':False,'in_new':True,
                    'conservation_rnaseq': len(list(set(exonstable[(exonstable.S_exonID_5p==source)&(exonstable.S_exonID_3p==target)].Species)))/9*10}),sort = False, ignore_index  = True) 
                else:
                    edges.loc[(edges.source==label_dict[source])&(edges.target==label_dict[target]),'in_new'] = True
                    edges.loc[(edges.source==label_dict[source])&(edges.target==label_dict[target]),'conservation_rnaseq'] = len(list(set(exonstable[(exonstable.S_exonID_5p==source)&(exonstable.S_exonID_3p==target)].Species)))/9*10 
        edges.loc[edges.in_new=='','in_new'] = False
        edges = edges.assign(in_cluster=0)

            #add edges between s-exons of one cluster, as they are not connected by intron, but still have a connection to eeach other. Get those s-exons from s-exon_table of thoraxe output
        
        homologs  = pd.read_csv('/home/sofya/Documents/TranscriptAnnotation/benchmark/'+sys.argv[3]+'/thoraxe/s_exon_table.csv',sep = ',', index_col = 0)  
        s_exon_clusters = homologs[['TranscriptIDCluster','S_exonID','ExonRank']].groupby(['TranscriptIDCluster','ExonRank'])['S_exonID'].apply(lambda x: list(x)) 
        s_exon_clusters = [i for i in s_exon_clusters if len(i)>1]   
        s_exon_clusters.sort()
        s_exon_clusters = list(s_exon_clusters for s_exon_clusters,_ in itertools.groupby(s_exon_clusters))    

        for s_exon_cluster in s_exon_clusters:
            for j in range(len(s_exon_cluster)-1):
                source = label_dict[s_exon_cluster[j]]
                target = label_dict[s_exon_cluster[j+1]]
                edges.loc[edges[(edges.source==source)&(edges.target == target)].index,'in_new'] = True
                edges.loc[edges[(edges.source==source)&(edges.target == target)].index,'conservation_rnaseq'] = min(nodes[nodes.id==source].conservation_rnaseq.iloc[0],nodes[nodes.id==target].conservation_rnaseq.iloc[0])
                edges.loc[edges[(edges.source==source)&(edges.target == target)].index,'in_cluster'] =1

        nodes = nodes.assign(state= pd.Series([0 if (nodes.in_new.iloc[i]==True) & (nodes.in_old.iloc[i]==True) else( 100 if (nodes.in_new.iloc[i]==True)&(nodes.in_old.iloc[i]==False ) else( 50)) for i in range(len(nodes))],index = nodes.index))   
        #edges = edges.assign(state= pd.Series([100 if (edges.in_new.iloc[i]==True) & (edges.in_old.iloc[i]==True) else( 50 if (edges.in_new.iloc[i]==True)&(edges.in_old.iloc[i]==False ) else( 0)) for i in range(len(edges))],index = edges.index))   
        nodes = nodes.assign(conservation= pd.Series([[int(round(nodes.conservation_old.iloc[i]/10))]+[int(nodes.conservation_rnaseq.iloc[i])] for i in range(len(nodes))],index = nodes.index))   
        edges = edges.assign(conservation= pd.Series([[int(round(edges.conservation_old.iloc[i]/10))]+[int(edges.conservation_rnaseq.iloc[i])] for i in range(len(edges))],index = edges.index))   
        '''edges = edges.assign(new = pd.Series([100 if (edges.conservation.iloc[i][0]==0)&(not(edges.source.iloc[i]==nodes.id.iloc[-1])|
                            (edges.source.iloc[i]==nodes.id.iloc[-2])|(edges.target.iloc[i]==nodes.id.iloc[-1])|(edges.target.iloc[i]==nodes.id.iloc[-2]))
                            else(50 if ((edges.source.iloc[i]==nodes.id.iloc[-1])|
                            (edges.source.iloc[i]==nodes.id.iloc[-2])|(edges.target.iloc[i]==nodes.id.iloc[-1])|(edges.target.iloc[i]==nodes.id.iloc[-2])) else(0)) for i in range(len(edges))],index = edges.index))   '''  
        edges = edges.assign(new = pd.Series([100 if (edges.conservation.iloc[i][0]==0)&(edges.conservation.iloc[i][1]!=0) else 
            (50 if (edges.conservation.iloc[i][0]!=0)&(edges.conservation.iloc[i][1]==0) else(0)) for i in range(len(edges))], index = edges.index)) # 100 if new 50 if only old 0 if both
        nodes = nodes[['id','label','conservation','state']]     
        edges = edges[['source','target','conservation_rnaseq','conservation','new','in_cluster']]     

        '''
        # not showing 3p/5p  endings as the graph is too noisy otherwise
        f1 = open(sys.argv[3], 'w') 
        f1.write('\n\tgraph [\n\t\tdirected 1\n\t\tid 42\n\t\tlabel "splice graph of orthologous exon groups"\n')
        for i in range(len(nodes)):
            f1.write('\n\t\t\tnode [\n\t\t\t\tid {id}\n\t\t\t\tlabel "{label}"\n\t\t\t\tstate {state}\n\t\t\t\tconservation "'.format(id = nodes.iloc[i].id,label = nodes.label.iloc[i],state = nodes.state.iloc[i]))#,cons = nodes.conservation.iloc[i]))
            for item in nodes.conservation.iloc[i]:
                f1.write("%s " % item)
            f1.write('"\n\t\t\t]\n')
        for i in range(len(edges)):
            f1.write('\n\t\t\tedge [\n\t\t\t\tsource {source}\n\t\t\t\ttarget {target}\n\t\t\t\tstate {state}\n\t\t\t\tconservation "'.format(source = edges.iloc[i].source,target = edges.target.iloc[i],state = edges.new.iloc[i]))#,cons = edges.conservation.iloc[i]))
            for item in edges.conservation.iloc[i]:
                f1.write("%s " % item)
            f1.write('"\n\t\t\t]\n')
        f1.write('\n\t]\n')
        f1.close()'''


        #edges = (edges[(edges.source!=nodes.id.iloc[-1])&(edges.target !=nodes.id.iloc[-1])&(edges.source!=nodes.id.iloc[-2])&(edges.target!=nodes.id.iloc[-2])])    
        #nodes = nodes[0:-2]


        f2 = open(sys.argv[4], 'w') 
        f2.write('\n\tgraph [\n\t\tdirected 1\n\t\tid 42\n\t\tlabel "splice graph of orthologous exon groups"\n')
        for i in range(len(nodes)):
            f2.write('\n\t\t\tnode [\n\t\t\t\tid {id}\n\t\t\t\tlabel "{label}"\n\t\t\t\tstate {state}\n\t\t\t\tconservation "'.format(id = nodes.iloc[i].id,label = nodes.label.iloc[i],state = nodes.state.iloc[i]))#,cons = nodes.conservation.iloc[i]))
            for item in nodes.conservation.iloc[i]:
                f2.write("%s " % item)
            f2.write('"\n\t\t\t]\n')
        for i in range(len(edges)):
            f2.write('\n\t\t\tedge [\n\t\t\t\tsource {source}\n\t\t\t\ttarget {target}\n\t\t\t\tstate {state}\n\t\t\t\tin_cluster {in_cluster}\n\t\t\t\tconservation_rnaseq {rnaseq}\n\t\t\t\tconservation "'.format(source = edges.iloc[i].source,target = edges.target.iloc[i],state = edges.new.iloc[i],in_cluster = edges.in_cluster.iloc[i],rnaseq = edges.conservation_rnaseq.iloc[i]))#cons = edges.conservation.iloc[i]))
            for item in edges.conservation.iloc[i]:
                f2.write("%s " % item)
            f2.write('"\n\t\t\t]\n')
        f2.write('\n\t]\n')
        f2.close()


if __name__=='__main__':
    main()
