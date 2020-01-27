#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""

import matplotlib.pyplot as plt
import netgraph
import networkx as nx
n = 5
G = nx.DiGraph()
G.add_nodes_from(range(n))
G.add_edges_from([(i, (i+1)%n) for i in range(n)]) # directed cycle
plt.subplots(1,1)
netgraph.draw(G, directed=True) # doesn't draw arrows
# netgraph.draw(G, draw_arrows=True)
plt.show()
