# local imports
from .connectivity_metrics import pairwise_connectivity
import utils.subgraph_store as subgraph_store

# third party imports
from scipy.special import comb


def minimize_pairwise_connectivity(G, MIS, S0):
    if not S0:
        raise Exception("S0 list is empty!")

    vertices = []
    minimum = -1
    ok = False

    nodes = set(S0)

    for i in S0:
        nodes.discard(i)

        try:
            subgraph = subgraph_store.retrieve_from_store(nodes)
        except:
            subgraph = subgraph_store.add_to_store(G, nodes)

        connectivity = pairwise_connectivity(subgraph)

        if connectivity < minimum or not ok:
            vertices.clear()
            vertices.append(i)
            minimum = connectivity
            ok = True
        elif connectivity == minimum:
            vertices.append(i)

        nodes.add(i)

    return vertices


def maximize_disconnected_pairs(G, MIS, k):
    vertices = []
    maximum = -1
    ok = False

    nodes_in_MIS = set(MIS.dict.keys())

    for i in MIS.dict:
        nodes_in_MIS.discard(i)

        try:
            subgraph = subgraph_store.retrieve_from_store(nodes_in_MIS)
        except:
            subgraph = subgraph_store.add_to_store(G, nodes_in_MIS)

        metric = pairwise_connectivity(subgraph)
        connectivity = comb(len(nodes_in_MIS), k, exact=True) - metric

        if connectivity > maximum or not ok:
            vertices.clear()
            vertices.append(i)
            maximum = connectivity
            ok = True
        elif connectivity == maximum:
            vertices.append(i)

        nodes_in_MIS.add(i)

    return vertices
