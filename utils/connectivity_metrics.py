# local imports
from .graph_components import connected_components


def pairwise_connectivity(G):
    components = connected_components(G)
    result = 0

    for component in components:
        n = len(component)
        result += (n * (n - 1)) // 2

    return result
