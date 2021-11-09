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


def get_paths(g):
    paths = {}
    paths_len = {}

    for node1 in g.nodes():
        paths[node1] = []
        paths_len[node1] = []
        for node2 in g.nodes():
            try:
                paths[node1].append(list(nx.algorithms.shortest_paths.generic.all_shortest_paths(g,node1,node2)))
                paths_len[node1].append(len(paths[node1][-1][0])-1)
            except:
                continue

    return paths,paths_len

def get_inverse_geodesic_length(g):
    inverse_geodesic_length = 0
    _,paths_len = get_paths(g)
    for node in paths_len:
        for l in paths_len[node]:
            if l != 0:
                inverse_geodesic_length += 1/l

    if (len(g.nodes())*(len(g.nodes())-1)) != 0:
        return inverse_geodesic_length/(len(g.nodes())*(len(g.nodes())-1))
    return 0

def get_scc_size(g):
    return len(sorted(nx.strongly_connected_components(g),key=len,reverse=True)[0])

def get_clustering(g):
    clustering = dict(nx.clustering(g))
    return sum(clustering.values())/len(clustering)

def get_betweenness(g):
    paths,_ = get_paths(g) 
    
    n_paths_through_v = {}
    for v in g.nodes():
        n_paths_through_v[v] = {}
        for s in g.nodes():
            n_paths_through_v[v][s] = {}
            for paths_s in paths[s]:
                for path in paths_s:
                    if path[-1] not in n_paths_through_v[v][s]:
                        n_paths_through_v[v][s][path[-1]] = []
                    if v in path and v != s and v != path[-1]:
                        n_paths_through_v[v][s][path[-1]].append(1)
                    else:
                        n_paths_through_v[v][s][path[-1]].append(0)

    ratio_paths_through_v = {}
    for v in g.nodes():
        ratio_paths_through_v[v] = 0
        for s in g.nodes():
            for t in n_paths_through_v[v][s]:
                ratio_paths_through_v[v] += sum(n_paths_through_v[v][s][t])/len(n_paths_through_v[v][s][t])

    return sorted(list(ratio_paths_through_v.items()),key=lambda x: x[1],reverse=True)


get_function = get_inverse_geodesic_length
function_string = "Inverse Geodesic Length"
in_x = list(range(len(g0.nodes())))

nodes_random = random.sample(list(gR.nodes()),len(gR.nodes()))
for node in tqdm(nodes_random):
    line_R.append(get_function(gR))
    gR.remove_node(node)

size = len(g0.nodes())
for i in tqdm(range(size)):
    max_degree_node = sorted(list(g0.degree()),key=lambda x: x[1],reverse=True)[0]
    line_RD.append(get_function(g0))
    g0.remove_node(max_degree_node[0])

degrees = sorted(list(g1.degree()),key=lambda x: x[1],reverse=True)

for t in tqdm(degrees):
    line_ID.append(get_function(g1))
    g1.remove_node(t[0])


size = len(g2.nodes())
for i in tqdm(range(size)):
    betweenness = get_betweenness(g2)[0]
    line_RB.append(get_function(g2))
    g2.remove_node(betweenness[0])

degrees = sorted(list(g1.degree()),key=lambda x: x[1],reverse=True)

betweenness = get_betweenness(g3)
for t in tqdm(betweenness):
    line_IB.append(get_function(g3))
    g3.remove_node(t[0])


df = pd.concat([pd.Series(line_R),pd.Series(line_ID),pd.Series(line_RD),pd.Series(line_IB),pd.Series(line_RB)])
df.to_csv(f"{function_string}.csv")

fig = plt.figure(function_string, figsize=(8, 8))
plt.plot(in_x, line_R,color="grey",label="Random")
plt.plot(in_x, line_ID,color="r",label="ID")
plt.plot(in_x, line_RD,color="g",label="RD")
plt.plot(in_x, line_IB,color="b",label="IB")
plt.plot(in_x, line_RB,color="y",label="RB")


plt.title(f'{function_string} Evolution')
plt.xlabel('N nodes removed')
plt.ylabel(function_string)
plt.legend()
plt.show()


