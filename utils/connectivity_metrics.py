# system imports
import copy

# local imports
from .graph_components import connected_components


def pairwise_connectivity(G):
    components = connected_components(G)
    sum = 0

    for component in components:
        n = len(component)
        sum += (n * (n - 1)) // 2

    return sum
