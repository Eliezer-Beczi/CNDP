# system imports
import copy

# local imports
from .connectivity_metrics import pairwise_connectivity


def minimize_pairwise_connectivity(G, MIS, S0):
    if not S0:
        raise Exception("S0 list is empty!")

    node = -1
    minimum = -1

    for i in S0:
        temp = copy.deepcopy(MIS)
        temp.addEdge(i, G.dict[i])
        connectivity = pairwise_connectivity(temp)

        if minimum == -1 or connectivity < minimum:
            node = i
            minimum = connectivity

    return node
