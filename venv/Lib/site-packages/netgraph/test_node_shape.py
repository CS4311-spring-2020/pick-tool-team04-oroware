import numpy as np
import matplotlib.pyplot as plt; plt.ion()
import netgraph

# Construct sparse, directed, weighted graph
# with positive and negative edges:
total_nodes = 20
weights = np.random.randn(total_nodes, total_nodes)
connection_probability = 0.2
is_connected = np.random.rand(total_nodes, total_nodes) <= connection_probability
graph = np.zeros((total_nodes, total_nodes))
graph[is_connected] = weights[is_connected]

# Make a standard plot:
netgraph.draw(graph, node_shape='^')
