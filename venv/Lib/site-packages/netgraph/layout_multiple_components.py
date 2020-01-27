#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import networkx
import rpack # pip install rectangle-packer


def layout_multiple_components(graph,
                               component_layout_func=networkx.layout.spring_layout,
                               pad_x=1., pad_y=1.):
    """
    Arguments:
    ----------
    graph: networkx.Graph object
        The graph to plot.

    component_layout_func: function (default networkx.layout.spring_layout)
        Function used to layout individual components.
        You can parameterize the layout function by partially evaluating the
        function first. For example:

        from functools import partial
        my_layout_func = partial(networkx.layout.spring_layout, k=10.)
        pos = layout_many_components(graph, my_layout_func)

    pad_x, pad_y: float
        Padding between subgraphs in the x and y dimension.

    Returns:
    --------
    pos : dict node : (float x, float y)
        The layout of the graph.

    """

    components = _get_components_sorted_by_size(graph)
    component_sizes = [len(component) for component in components]
    bboxes = _get_component_bboxes(component_sizes, pad_x, pad_y)

    pos = dict()
    for component, bbox in zip(components, bboxes):
        component_pos = _layout_component(component, bbox, component_layout_func)
        pos.update(component_pos)

    return pos


def _get_components_sorted_by_size(g):
    subgraphs = list(networkx.connected_component_subgraphs(g))
    return sorted(subgraphs, key=len)


# def _get_component_bboxes(component_sizes, pad_x=1., pad_y=1.):
#     bboxes = []
#     x, y = (0, 0)
#     current_n = 1
#     for n in component_sizes:
#         width, height = _get_bbox_dimensions(n, power=0.8)

#         if not n == current_n: # create a "new line"
#             x = 0 # reset x
#             y += height + pad_y # shift y up
#             current_n = n

#         bbox = x, y, width, height
#         bboxes.append(bbox)
#         x += width + pad_x # shift x down the line
#     return bboxes


def _get_component_bboxes(component_sizes, pad_x=1., pad_y=1.):
    dimensions = [_get_bbox_dimensions(n, power=0.8) for n in component_sizes]
    # rpack only works on integers
    dimensions = [(int(width + pad_x), int(height + pad_y)) for (width, height) in dimensions]
    # rpack works best if the heights are in descending order
    dimensions = dimensions[::-1]
    origins = rpack.pack(dimensions)
    bboxes = [(x, y, width-pad_x, height-pad_y) for (x,y), (width, height) in zip(origins, dimensions)]
    # reverse order to match order of components
    bboxes = bboxes[::-1]
    return bboxes


def _get_bbox_dimensions(n, power=0.5):
    return (n**power, n**power)


def test():
    from itertools import combinations

    g = networkx.Graph()

    # add 100 unconnected nodes
    g.add_nodes_from(range(100))

    # add 50 2-node components
    g.add_edges_from([(ii, ii+1) for ii in range(100, 200, 2)])

    # add 33 3-node components
    for ii in range(200, 300, 3):
        g.add_edges_from([(ii, ii+1), (ii, ii+2), (ii+1, ii+2)])

    # add a couple of larger components
    n = 300
    for ii in np.random.randint(3, 30, size=10):
        g.add_edges_from(combinations(range(n, n+ii), 2))
        n += ii

    pos = layout_many_components(g, component_layout_func=networkx.layout.circular_layout)

    networkx.draw(g, pos, node_size=100)

    plt.show()


if __name__ == '__main__':
    test()
