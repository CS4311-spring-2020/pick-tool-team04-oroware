import networkx
import netgraph
import numpy as np
total_nodes = 20
weights = np.random.randn(total_nodes, total_nodes)
connection_probability = 0.2
is_connected = np.random.rand(total_nodes, total_nodes) <= connection_probability
graph = np.zeros((total_nodes, total_nodes))
graph[is_connected] = weights[is_connected]
counter = 0
for row in graph:
    row[counter] = 0
    counter += 1
g = networkx.from_numpy_array(graph, networkx.DiGraph)
netgraph.draw(g)