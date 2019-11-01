# system imports
import copy

# local imports
from .vertex_cover import greedy_vertex_cover
from .objective_functions import minimize_pairwise_connectivity


def greedy_cnp(G, k):
    S0 = greedy_vertex_cover(G)
    MIS = copy.deepcopy(G)

    for node in S0:
        MIS.removeNode(node)

    while len(S0) > k:
        i = minimize_pairwise_connectivity(G, MIS, S0)
        S0.remove(i)
        MIS.addEdge(i, G.dict[i])

    return S0
