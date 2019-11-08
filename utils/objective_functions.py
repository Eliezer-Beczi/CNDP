import networkx as nx
from scipy.special import comb

from utils.connectivity_metrics import pairwise_connectivity


def minimize_pairwise_connectivity(G, S0):
    if not S0:
        raise Exception("S0 list is empty!")

    tmp = S0.copy()
    nodes = tmp.copy()

    node = next(iter(tmp))
    tmp.discard(node)

    subgraph = nx.subgraph_view(G, filter_node=lambda n: n not in tmp)
    connectivity = pairwise_connectivity(subgraph)

    vertices = [node]
    minimum = connectivity

    while tmp:
        node = next(iter(tmp))

        tmp.discard(node)
        nodes.discard(node)

        subgraph = nx.subgraph_view(G, filter_node=lambda n: n not in nodes)
        connectivity = pairwise_connectivity(subgraph)

        if connectivity < minimum:
            vertices = [node]
            minimum = connectivity
        elif connectivity == minimum:
            vertices.append(node)

        nodes.add(node)

    return vertices


def maximize_disconnected_pairs(G, k):
    tmp = set(G)
    nodes = tmp.copy()

    node = next(iter(tmp))
    tmp.discard(node)

    subgraph = nx.subgraph_view(G, filter_node=lambda n: n in tmp)
    connectivity = comb(len(tmp), k) - pairwise_connectivity(subgraph)

    vertices = [node]
    maximum = connectivity

    while tmp:
        node = next(iter(tmp))

        tmp.discard(node)
        nodes.discard(node)

        subgraph = nx.subgraph_view(G, filter_node=lambda n: n in nodes)
        connectivity = comb(len(tmp), k) - pairwise_connectivity(subgraph)

        if connectivity > maximum:
            vertices = [node]
            maximum = connectivity
        elif connectivity == maximum:
            vertices.append(node)

        nodes.add(node)

    return vertices
