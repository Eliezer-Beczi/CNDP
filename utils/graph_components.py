# local imports
from .graph_traversals import DFS


def connected_components(G):
    visited = {}
    components = []

    for node in G.dict:
        visited[node] = False

    for node in G.dict:
        if not visited[node]:
            temp = DFS(G, node)
            component = []

            for x, val in temp.items():
                if not val:
                    continue

                visited[x] = True
                component.append(x)

            components.append(component)

    return components
