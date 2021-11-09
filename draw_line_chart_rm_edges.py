import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import random

data = pd.read_csv('indonesianLinksDATASET.csv')

edges = pd.DataFrame({'source': data['Source'].tolist(),
                      'target': data['Target'].tolist(),
                      'weight': data['Weight'].tolist()})
        
g0 = nx.from_pandas_edgelist(edges, 'source', 'target', True, nx.DiGraph())

results_data = pd.read_csv("indonesianResultsDATASET.csv")
results_data = results_data.sort_values(by="Label")

for i,row in results_data.iterrows():
    if row["Degree"] == 0:
        g0.add_node(row["Label"])

G = nx.DiGraph()
G.add_nodes_from(sorted(g0.nodes(data=True)))
G.add_edges_from(g0.edges(data=True))
g0 = G

gR = g0.copy()
g1 = g0.copy()
g2 = g0.copy()
g3 = g0.copy()

line_R = []
line_ID = []
line_RD = []
line_IB = []
line_RB = []


def get_paths(g,old_paths):
    paths = {}
    paths_len = {}
    paths_removed = []

    for node1 in g.nodes():
        paths[node1] = {}
        paths_len[node1] = {}
        for node2 in g.nodes():
            if old_paths == {}:
                try:
                    paths[node1][node2] = list(nx.algorithms.shortest_paths.generic.all_shortest_paths(g,node1,node2))
                    paths_len[node1][node2] = len(paths[node1][node2][0])-1
                except:
                    continue
            elif node2 in old_paths[node1].keys():
                for path in old_paths[node1][node2]:
                    flag = True
                    for i in range(len(path)-1):
                        if not g.has_edge(path[i],path[i+1]): 
                            flag = False
                            paths_removed.append(path)
                            old_paths[node1][node2].remove(path)
                            break
                if flag:
                    paths[node1][node2] = old_paths[node1][node2]
                    paths_len[node1][node2] = len(old_paths[node1][node2][0])-1

                else:     
                
                    try:
                        paths[node1][node2] = list(nx.algorithms.shortest_paths.generic.all_shortest_paths(g,node1,node2))
                        paths_len[node1][node2] = len(paths[node1][node2][0])-1
                    except:
                        continue

    return paths,paths_len,paths_removed

def get_inverse_geodesic_length(g,old_paths):
    inverse_geodesic_length = 0
    paths,paths_len,_ = get_paths(g,old_paths)
    for node in paths_len:
        for l in paths_len[node].values():
            if l != 0:
                inverse_geodesic_length += 1/l

    if (len(g.nodes())*(len(g.nodes())-1)) != 0:
        return inverse_geodesic_length/(len(g.nodes())*(len(g.nodes())-1)),paths
    return 0,paths

def get_scc_size(g,old_paths):
    return len(sorted(nx.strongly_connected_components(g),key=len,reverse=True)[0]),old_paths

def get_clustering(g,old_paths):
    clustering = dict(nx.clustering(g))
    return sum(clustering.values())/len(clustering),old_paths

def get_betweenness(g,old_paths,old_paths_through_e):
    
    paths,_,paths_removed = get_paths(g,old_paths) 

    if old_paths_through_e == {}:
    
        paths_through_e = {}
        for e in tqdm(g.edges()):
            paths_through_e[e] = {}
            for s in paths:
                paths_through_e[e][s] = {}
                for t in paths[s]:
                    if t not in paths_through_e[e][s]:
                        paths_through_e[e][s][t] = []
                    for path in paths[s][t]:
                        for i in range(len(path)-1):
                            if e[0] == path[i] and e[1] == path[i+1] and e[0] != s and e[1] != t:
                                paths_through_e[e][s][t].append(path)
                                break
                        
    else:
        e_removed = None
        for e in old_paths_through_e:
            if not g.has_edge(*e):
                e_removed = e
                break
        for path in paths_removed:
            s = path[0]
            t = path[-1]
            for i in range(1,len(path)-2):
                e = (path[i],path[i+1])
                if path in old_paths_through_e[e][s][t]:
                    old_paths_through_e[e][s][t].remove(path)
                
        
        paths_through_e = old_paths_through_e
        """
        for e in old_paths_through_e:
            if e != e_removed:

                paths_through_e[e] = {}  
                for s in old_paths_through_e[e]:
                    paths_through_e[e][s] = {}
                    for t in old_paths_through_e[e][s]:
                        paths_through_e[e][s][t] = []
                        for path in old_paths_through_e[e][s][t]:
                            flag = True
                            for i in range(len(path)-1):
                                if e_removed == (path[i],path[i+1]):
                                    flag = False
                                    break
                            if flag:
                                paths_through_e[e][s][t].append(path)
        """

    ratio_paths_through_e = {}
    for e in g.edges():
        ratio_paths_through_e[e] = 0
        for s in paths_through_e[e]:
            if s in paths.keys():
                for t in paths_through_e[e][s]:
                    if t in paths[s].keys() and len(paths[s][t]) != 0:
                        ratio_paths_through_e[e] += len(paths_through_e[e][s][t])/len(paths[s][t])

    return sorted(list(ratio_paths_through_e.items()),key=lambda x: x[1],reverse=True),paths,paths_through_e



get_function = get_clustering
function_string = "Clustering"
in_x = list(range(len(g0.edges())))

edges_random = random.sample(list(gR.edges()),len(gR.edges()))
temp_paths = {}
for edge in tqdm(edges_random):
    value,temp_paths = get_function(gR,temp_paths)
    line_R.append(value)
    gR.remove_edge(*edge)

size = len(g0.edges())
temp_paths = {}
for i in tqdm(range(size)):
    degrees = dict(sorted(list(g0.degree()),key=lambda x: x[1],reverse=True))
    max_degree = 0
    max_degree_edge = None
    for edge in g0.edges():
        degree = degrees[edge[0]]*degrees[edge[1]]
        if degree > max_degree:
            max_degree = degree
            max_degree_edge = edge

    value,temp_paths = get_function(g0,temp_paths)
    line_RD.append(value)
    g0.remove_edge(*max_degree_edge)

degrees = dict(sorted(list(g1.degree()),key=lambda x: x[1],reverse=True))
edge_degrees = {}
for edge in g1.edges():
    edge_degrees[edge] = degrees[edge[0]]*degrees[edge[1]]

edge_degrees = sorted(edge_degrees.items(),key=lambda x: x[1],reverse=True)
temp_paths = {}
for t in tqdm(edge_degrees):
    value,temp_paths = get_function(g1,temp_paths)
    line_ID.append(value)
    g1.remove_edge(*t[0])


size = len(g2.edges())
temp_paths = {}
temp_paths_through_e = {}
for i in tqdm(range(size)):
    betweennesses,temp_paths,temp_paths_through_e = get_betweenness(g2,temp_paths,temp_paths_through_e)
    betweenness = betweennesses[0]
    value,temp_paths = get_function(g2,temp_paths)
    line_RB.append(value)
    g2.remove_edge(*betweenness[0])


temp_paths = {}
temp_paths_through_e = {}
betweennesses,temp_paths,temp_paths_through_e = get_betweenness(g3,temp_paths,temp_paths_through_e)
for t in tqdm(betweennesses):
    value,temp_paths = get_function(g3,temp_paths)
    line_IB.append(value)
    g3.remove_edge(*t[0])


df = pd.concat([pd.Series(line_R),pd.Series(line_ID),pd.Series(line_RD),pd.Series(line_IB),pd.Series(line_RB)])
df.to_csv(f"{function_string}.csv")

fig = plt.figure(function_string, figsize=(8, 8))
plt.plot(in_x, line_R,color="grey",label="Random")
plt.plot(in_x, line_ID,color="r",label="ID")
plt.plot(in_x, line_RD,color="g",label="RD")    
plt.plot(in_x, line_IB,color="b",label="IB")
plt.plot(in_x, line_RB,color="y",label="RB")


plt.title(f'{function_string} Evolution')
plt.xlabel('N edges removed')
plt.ylabel(function_string)
plt.legend()
plt.show()


