#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
https://stackoverflow.com/questions/49137795/manually-sketch-graph-and-import-into-networkx
"""

import numpy as np
import matplotlib.pyplot as plt

from netgraph import InteractivelyConstructDestroyGraph

# initialise figure
fig, ax = plt.subplots()

# set size of axis
ax.set(xlim=[-2, 2], ylim=[-2, 2])

# initialise graph;
# netgraph supports many graph input formats but an empty graph is not one of them;
# hence we pass in a single edge in an edge list format
g = InteractivelyConstructDestroyGraph([(0, 1)], node_size=9., node_edge_width=3., edge_width=3., draw_arrows=True, ax=ax)
plt.show()

# manipulate graph:
#   Pressing 'A' will add a node to the graph.
#   Pressing 'D' will remove a selected node.
#   Pressing 'a' will add edges between all selected nodes.
#   Pressing 'd' will remove edges between all selected nodes.
#   Pressing 'r' will reverse the direction of edges between all selected nodes.
#   Nodes can be selected and moved using the mouse.

# # get current edge list
# edge_list = g.edge_list

# # get current node positions, which is a dict int node : (float x, float y) (same format as in networkx)
# node_positions = g.node_positions

# # create graph in networkx
# import networkx
# G = networkx.Graph()
# G.add_edges_from(edge_list)

# # reproduce plot in networkx
# networkx.draw(G, pos=node_positions)
# plt.show()
