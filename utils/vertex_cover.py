def greedy_vertex_cover(G):
    visited = {}

    for node in G.dict:
        visited[node] = False

    for u, nbrs in G.dict.items():
        if not visited[u]:
            for v in nbrs:
                if not visited[v]:
                    visited[u] = True
                    visited[v] = True

                    break

    return [x for x, val in visited.items() if val]
