import networkx as nx
import random
from graphviz import Source
from networkx.algorithms.approximation import vertex_cover
from networkx.algorithms.components import connected


def pairwise_connectivity(G):
    components = connected.connected_components(G)
    result = 0

    for component in components:
        n = len(component)
        result += (n * (n - 1)) // 2

    return result


def minimize_pairwise_connectivity(G, S0):
    if not S0:
        raise Exception("S0 list is empty!")

    tmp = S0.copy()

    node = next(iter(tmp))
    tmp.discard(node)

    subgraph = nx.subgraph_view(G, filter_node=lambda n: n not in tmp)
    connectivity = pairwise_connectivity(subgraph)

    vertices = [node]
    minimum = connectivity

    while tmp:
        node = next(iter(tmp))
        tmp.discard(node)

        subgraph = nx.subgraph_view(G, filter_node=lambda n: n not in S0 - {node})
        connectivity = pairwise_connectivity(subgraph)

        if connectivity < minimum:
            vertices = [node]
            minimum = connectivity
        elif connectivity == minimum:
            vertices.append(node)

    return vertices


def greedy_cnp(G, k):
    S0 = vertex_cover.min_weighted_vertex_cover(G)

    while len(S0) > k:
        B = minimize_pairwise_connectivity(G, S0)
        i = random.choice(B)
        S0.discard(i)

    return S0


def main():
    G = nx.read_adjlist("input/Ventresca/BarabasiAlbert_n500m1.txt")
    src = Source(nx.nx_pydot.to_pydot(G))
    src.render("graph.gv", view=True)

    print(greedy_cnp(G, 50))


main()
