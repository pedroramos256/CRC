import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

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

paths = {}
paths_len = {}

for node1 in g.nodes():
    paths[node1] = []
    paths_len[node1] = []
    for node2 in g.nodes():
        try:
            paths[node1].append(list(nx.algorithms.shortest_paths.generic.all_shortest_paths(g,node1,node2)))
        except:
            continue


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

betweenness = list(ratio_paths_through_v.values())
min_b = min(betweenness)
max_b = max(betweenness)
print("Minimum betweenness:",min_b)
print("Maximum betweenness:",max_b)

weighted_degrees = list(map(lambda x: x[1]*7,g.degree(weight='weight')))
min_w = min(weighted_degrees)
max_w = max(weighted_degrees)
print("Minimum weighted degree:",min_w)
print("Maximum weighted degree:",max_w)

options = {
    'node_color': 'green',
    'node_size': 50,
    'width': 0.1,
    'arrowstyle': '->',
    'node_size': weighted_degrees,
    'node_color': betweenness
}


plt.figure(figsize=(25,25))
nx.draw_kamada_kawai(g, **options)
plt.show()