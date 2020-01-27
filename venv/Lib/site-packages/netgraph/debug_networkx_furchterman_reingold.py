#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt; plt.ion()
import networkx as nx

from _layout import _fruchterman_reingold
from _main import InteractiveGraph, _get_random_weight_matrix, _edge_list_to_adjacency


if __name__ == '__main__':

    # # 1) K-graph
    # total_nodes = 8
    # adjacency = np.ones((total_nodes, total_nodes)) - np.diag(np.ones((total_nodes)))
    # edge_list = nx.from_numpy_matrix(adjacency).edges()
    # k = 1./np.sqrt(total_nodes)

    # 2) unbalanced tree
    edge_list = [
        (0, 1),
        (0, 2),
        (0, 3),
        (0, 4),
        (0, 5),
        (2, 6),
        (3, 7),
        (3, 8),
        (4, 9),
        (4, 10),
        (4, 11),
        (5, 12),
        (5, 13),
        (5, 14),
        (5, 15)
    ]

    adjacency = _edge_list_to_adjacency(edge_list)
    total_nodes = np.max(edge_list)+1
    k = 0.1

    # initial node positions
    node_positions = {ii : np.random.rand(2) for ii in range(total_nodes)}

    # networkx layout
    nxg = nx.Graph()
    nxg.add_edges_from(edge_list)

    fig, ax = plt.subplots(1,1)
    nx_node_positions = nx.spring_layout(nxg, pos=node_positions, iterations=50)
    nx.draw_networkx(nxg, pos=nx_node_positions, k=k, ax=ax)
    plt.show()

    # my layout
    fig, ax = plt.subplots(1,1)
    g = InteractiveGraph(edge_list,
                         node_positions=node_positions,
                         ax=ax)

    total_iterations = 50
    x = np.linspace(0, 1, total_iterations) + 1e-4
    temperatures = 0.1 * (x - 1)**2

    for ii, temperature in enumerate(temperatures):
        g.node_positions = _fruchterman_reingold(adjacency, g.node_positions,
                                                 origin=np.zeros((2)),
                                                 scale=np.array((1, 1)),
                                                 temperature=temperature,
                                                 k=k,
        )
        g._update_nodes(g.node_positions.keys())
        g._update_edges(g.node_positions.keys())
        g._update_view()
        fig.canvas.draw()

    input("Press any key to close figure...")
