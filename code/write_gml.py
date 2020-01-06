import pandas as pd 
import sys
import itertools


def main():

    exonstable = pd.read_csv(sys.argv[1],sep = '\t')
    f = open(sys.argv[2], 'w')

    #f = open('/home/sofya/Documents/TranscriptAnnotation/analysis/MAPK10/rnaseq/rnaseq_splice_graph.gml','w')
    #exonstable = pd.read_csv('/home/sofya/Documents/TranscriptAnnotation/rnaseq/MAPK10/Ensembl/merge_homologs.tsv',sep = '\t')
    exonstable =exonstable[exonstable.n_total_uq>1e-07]  

    
    exon_clusters = list(set(exonstable.S_exonID_5p.tolist()+exonstable.S_exonID_3p.tolist())) 
    exon_clusters = [i for i in exon_clusters if not pd.isnull(i)]  

    exon_clusters = pd.DataFrame({'id':list(range(1,len(exon_clusters)+1)),'node':exon_clusters})
    #n_tr = list(set(exonstable.TranscriptIDCluster_5p.tolist()+exonstable.TranscriptIDCluster_3p.tolist()))     
    #n_tr = len([i for i in n_tr if ~ pd.isnull(i)])
    #exon_clusters = exon_clusters.assign(cons = pd.Series([round(len(list(set(exonstable[exonstable.S_exonID_5p==i].TranscriptIDCluster_5p.tolist()+ exonstable[exonstable.S_exonID_3p==i].TranscriptIDCluster_3p.tolist())))/n_tr*100) for i in exon_clusters.node]))
    exon_clusters = exon_clusters.assign(cons = pd.Series([round(len(set(exonstable[(exonstable.S_exonID_5p==i)|(exonstable.S_exonID_3p==i)].Species))/9*10) for i in exon_clusters.node]))#12/10, if taking all species into account
    exon_clusters = exon_clusters.append(pd.DataFrame({'id':len(exon_clusters)+1,'node':'5_p','cons':10},index = [exon_clusters.iloc[-1].name+1]),sort = False, ignore_index = True)
    exon_clusters = exon_clusters.append(pd.DataFrame({'id':len(exon_clusters)+1,'node':'3_p','cons':10},index = [exon_clusters.iloc[-1].name+1]),sort = False, ignore_index = True)

    unique_edges = list(set(list(zip(exonstable.S_exonID_5p,exonstable.S_exonID_3p))))  
    unique_edges=pd.DataFrame(unique_edges,columns =['S_exonID_5p','S_exonID_3p'])  
    unique_edges.S_exonID_5p = unique_edges.S_exonID_5p.fillna('5_p')
    unique_edges.S_exonID_3p = unique_edges.S_exonID_3p.fillna('3_p')
    unique_edges = unique_edges.assign(source = pd.Series([int(exon_clusters[exon_clusters.node==i].id) for i in unique_edges.S_exonID_5p]))
    unique_edges = unique_edges.assign(target = pd.Series([int(exon_clusters[exon_clusters.node==i].id) for i in unique_edges.S_exonID_3p]))
    unique_edges = unique_edges.assign(cons = pd.Series([len(list(set(exonstable[(exonstable.S_exonID_5p==unique_edges.S_exonID_5p.iloc[i])&(exonstable.S_exonID_3p==unique_edges.S_exonID_3p.iloc[i])].Species)))/9*10  for i in range(len(unique_edges))]))#/12*10 if with zebrafish and macaque
    unique_edges = unique_edges.assign(rnaseq = 0)
    #add edges between s-exons of one cluster, as they are not connected by intron, but still have a connection to each other. Get those s-exons from s-exon_table of thoraxe output
    
    homologs  = pd.read_csv('/home/sofya/Documents/TranscriptAnnotation/benchmark/'+sys.argv[3]+'/thoraxe/s_exon_table.csv',sep = ',', index_col = 0)  
    s_exon_clusters = homologs[['TranscriptIDCluster','S_exonID','ExonRank']].groupby(['TranscriptIDCluster','ExonRank'])['S_exonID'].apply(lambda x: list(x)) 
    s_exon_clusters = [i for i in s_exon_clusters if len(i)>1]   
    s_exon_clusters.sort()
    s_exon_clusters = list(s_exon_clusters for s_exon_clusters,_ in itertools.groupby(s_exon_clusters))    

    for s_exon_cluster in s_exon_clusters:
        for j in range(len(s_exon_cluster)-1):
            if exon_clusters[exon_clusters.node==s_exon_cluster[j]].empty:
                continue
            source = exon_clusters[exon_clusters.node==s_exon_cluster[j]].id.iloc[0]  
            if exon_clusters[exon_clusters.node==s_exon_cluster[j+1]].empty:
                continue
            target = exon_clusters[exon_clusters.node==s_exon_cluster[j+1]].id.iloc[0]  
            cons = min(exon_clusters[exon_clusters.node==s_exon_cluster[j]].cons.iloc[0],exon_clusters[exon_clusters.node==s_exon_cluster[j+1]].cons.iloc[0])
            if unique_edges[(unique_edges.S_exonID_5p==s_exon_cluster[j])&(unique_edges.S_exonID_3p==s_exon_cluster[j+1])].empty:
                unique_edges = unique_edges.append(pd.DataFrame({'S_exonID_5p':s_exon_cluster[j],'S_exonID_3p':s_exon_cluster[j+1],'source':source,'target':target,'cons':cons,'rnaseq' : 1}, index = [len(unique_edges)+1]),sort = False)



    f.write('\n\tgraph [\n\t\tdirected 1\n\t\tid 42\n\t\tlabel "splice graph of orthologous exon groups"\n') 

    #get rid of 5p or 3p splice junctions as they only make the picture noisy
    exon_clusters = exon_clusters[(exon_clusters.node!='5_p')&(exon_clusters.node!='3_p')]   
    unique_edges = unique_edges[(unique_edges.S_exonID_5p!='5_p')&(unique_edges.S_exonID_3p!='3_p')]

    for i in range(len(exon_clusters)):
        f.write('\n\t\t\tnode [\n\t\t\t\tid {id}\n\t\t\t\tlabel "{label}"\n\t\t\t\tconservation {conserv}\n\t\t\t]\n'.format(id = exon_clusters.iloc[i].id,label = exon_clusters.iloc[i].node,conserv = exon_clusters.iloc[i].cons))
        
    for i in range(len(unique_edges)):
        f.write('\n\t\t\tedge [\n\t\t\t\tsource {source}\n\t\t\t\ttarget {target}\n\t\t\t\tconservation {cons}\n\t\t\t\tin_cluster {rnaseq}\n\t\t\t]\n'.format(source = unique_edges.iloc[i].source,target = unique_edges.iloc[i].target,cons = unique_edges.iloc[i].cons,rnaseq = unique_edges.rnaseq.iloc[i]))
    f.write('\n\t]\n')
    f.close()






    
if __name__=='__main__':
    main()