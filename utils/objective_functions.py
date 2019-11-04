# system imports
import copy
import random

# local imports
from .connectivity_metrics import pairwise_connectivity

# third party imports
from scipy.special import comb


def minimize_pairwise_connectivity(G, MIS, S0):
    if not S0:
        raise Exception("S0 list is empty!")

    vertices = []
    minimum = -1
    ok = False

    for i in S0:
        temp = copy.deepcopy(MIS)
        temp.addEdge(i, list(set(G.dict[i]) - set(S0)))

        connectivity = pairwise_connectivity(temp)

        if connectivity < minimum or not ok:
            vertices.clear()
            vertices.append(i)
            minimum = connectivity
            ok = True
        elif connectivity == minimum:
            vertices.append(i)

    return vertices


def maximize_disconnected_pairs(G, MIS, k):
    vertices = []
    maximum = -1
    ok = False

    S0 = [*MIS.dict]

    for i in S0:
        temp = copy.deepcopy(MIS)
        temp.removeNode(i)
        metric = pairwise_connectivity(temp)

        connectivity = comb(len(temp), k, exact=True) - metric

        if connectivity > maximum or not ok:
            vertices.clear()
            vertices.append(i)
            maximum = connectivity
            ok = True
        elif connectivity == maximum:
            vertices.append(i)

    return vertices
