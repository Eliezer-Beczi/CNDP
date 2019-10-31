# system imports
import copy

# local imports
from .vertex_cover import greedy_vertex_cover


def greedy_cnp(G, k):
    S0 = greedy_vertex_cover(G)
    MIS = copy.deepcopy(G)

    for node in S0:
        MIS.removeNodeFromGraph(node)
