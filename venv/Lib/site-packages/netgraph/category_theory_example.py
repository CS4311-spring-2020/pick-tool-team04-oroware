#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
https://www.reddit.com/r/math/comments/83w8m7/netgraph_a_python_module_for_plotting_directed/dvm4va7/
"""

import matplotlib.pyplot as plt;
from netgraph import InteractiveGraph

node_labels = {
    0 : r'$(A \otimes B) \otimes C$',
    1 : r'$A \otimes (B \otimes C)$',
    2 : r'$(B \otimes C) \otimes A$',
    3 : r'$B \otimes (C \otimes A)$',
    4 : r'$(B \otimes A) \otimes C$',
    5 : r'$B \otimes (A \otimes C)$',
}

# optional
node_positions = {0 : (0,  0),
                  1 : (1,  1),
                  2 : (2,  1),
                  3 : (3,  0),
                  4 : (1, -1),
                  5 : (2, -1)
}

edge_labels = {
    (0, 1) : r'$\alpha$',
    (1, 2) : r'$\gamma$',
    (2, 3) : r'$\alpha$',
    (0, 4) : r'$\gamma \otimes 1$',
    (4, 5) : r'$\alpha$',
    (5, 3) : r'$\gamma \otimes 1$',
}

g = InteractiveGraph(edge_labels.keys(), # i.e. an edge_list
                     node_positions=node_positions,
                     node_labels=node_labels,
                     edge_labels=edge_labels,
                     draw_arrows=True,
                     node_size=25.,
                     node_edge_alpha=0.,
                     edge_width=5.,
                     edge_alpha=0.3,
)

plt.show()
