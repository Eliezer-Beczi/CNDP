from networkx.algorithms.components import connected


def pairwise_connectivity(G):
    components = connected.connected_components(G)
    result = 0

    for component in components:
        n = len(component)
        result += (n * (n - 1)) // 2

    return result
