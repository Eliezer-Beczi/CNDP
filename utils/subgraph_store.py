import copy

graphs = {}


def add_to_store(G, S):
    key = _hash_list(S)

    if key not in graphs:
        new_G = _truncate_graph(G, S)
        graphs[key] = new_G

    return graphs[key]


def retrieve_from_store(S):
    key = _hash_list(S)

    if key in graphs:
        return graphs[key]
    else:
        raise Exception("No such graph in store!")


"""
=================
PRIVATE FUNCTIONS
=================
"""


def _truncate_graph(G, S):
    subgraph = copy.deepcopy(G)

    for node in S:
        subgraph.removeNode(node)

    return subgraph


def _hash_list(S):
    return tuple(sorted(S))
