#!/usr/bin/env python

def _edge_list_to_adjacency_list(edge_list):
    adjacency = dict()
    for source, target in edge_list:
        if source in adjacency:
            adjacency[source] |= set([target])
        else:
            adjacency[source] = set([target])
    return adjacency


def test_edge_list_to_adjacency_list():
    adjacency_list = {'A': set(['B', 'C']),
             'B': set(['A', 'D', 'E']),
             'C': set(['A', 'F']),
             'D': set(['B']),
             'E': set(['B', 'F']),
             'F': set(['C', 'E']),
    }

    edge_list = [
        ('A', 'B'), ('A', 'C'),
        ('B', 'A'), ('B', 'D'), ('B', 'E'),
        ('C', 'A'), ('C', 'F'),
        ('D', 'B'),
        ('E', 'B'), ('E', 'F'),
        ('F', 'C'), ('F', 'E')
    ]

    output = _edge_list_to_adjacency_list(edge_list)

    # print(adjacency_list)
    # print(output)
    assert output == adjacency_list



def dfs(adjacency_list, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    for node in adjacency_list[start] - visited:
        dfs(adjacency_list, node, visited)
    return visited


def test_dfs():
    graph = {'A': set(['B', 'C']),
             'B': set(['A', 'D', 'E']),
             'C': set(['A', 'F']),
             'D': set(['B']),
             'E': set(['B', 'F']),
             'F': set(['C', 'E']),
             'G': set()
    }

    assert dfs(graph, 'C') == {'C', 'B', 'F', 'D', 'E', 'A'}
    assert dfs(graph, 'G') == {'G'}


def get_connected_components(adjacency_list):
    not_visited = set(list(adjacency_list.keys()))
    components = []
    while not_visited:
        start = not_visited.pop()
        component = dfs(adjacency_list, start)
        components.append(component)
        for node in component:
            if node != start:
                not_visited.remove(node)
    return components


def test_get_connected_components():
    graph = {'A': set(['B', 'C']),
             'B': set(['A', 'D', 'E']),
             'C': set(['A', 'F']),
             'D': set(['B']),
             'E': set(['B', 'F']),
             'F': set(['C', 'E']),
             'G': set(),
    }
    assert get_connected_components(graph) == [{'D', 'E', 'C', 'A', 'F', 'B'}, {'G'}]


def is_bipartite(edge_list):
    pass


if __name__ == '__main__':
    test_edge_list_to_adjacency_list()
    test_dfs()
    test_get_connected_components()
    pass
