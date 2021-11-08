import networkx as nx
import pandas as pd
from tqdm import tqdm

data = pd.read_csv('indonesianLinksDATASET.csv')

edges = pd.DataFrame({'source': data['Source'].tolist(),
                      'target': data['Target'].tolist(),
                      'weight': data['Weight'].tolist()})
        
g = nx.from_pandas_edgelist(edges, 'source', 'target', True, nx.DiGraph())

results_data = pd.read_csv("indonesianResultsDATASET.csv")
results_data = results_data.sort_values(by="Label")

for i,row in results_data.iterrows():
    if row["Degree"] == 0:
        g.add_node(row["Label"])

G = nx.DiGraph()
G.add_nodes_from(sorted(g.nodes(data=True)))
G.add_edges_from(g.edges(data=True))
g = G

degrees = g.degree()

weighted_degrees = g.degree(weight='weight')

paths_len = {}

for node1 in g.nodes():
    paths_len[node1] = []
    for node2 in g.nodes():
        try:
            path = list(nx.algorithms.shortest_paths.generic.all_shortest_paths(g,node1,node2))
            paths_len[node1].append(len(path[0])-1)
        except:
            continue

print("Density:",nx.classes.function.density(g))
print("Average Clustering Coefficient:",nx.algorithms.cluster.average_clustering(g))

average_path_len = 0
counter = 0
for node in paths_len:
    average_path_len += sum(paths_len[node])
    counter += len(paths_len[node])

average_path_len /= counter
print("Average Path Length:",average_path_len)

print("Average Degree:",sum(dict(degrees).values())/len(dict(degrees))/2)
print("Average Weight Degree:",sum(dict(weighted_degrees).values())/len(dict(weighted_degrees))/2)

diameter = 0
for node in paths_len:
    diameter = max(diameter,max(paths_len[node]))

print("Network Diameter:",diameter)
