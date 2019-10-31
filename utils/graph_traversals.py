# system imports
from collections import deque


def DFS(G, v):
    stack = [v]
    visited = {}

    for node in G.dict.keys():
        visited[node] = False

    visited[v] = True

    while stack:
        w = stack.pop()

        for x in G.dict[w]:
            if not visited[x]:
                visited[x] = True
                stack.append(x)

    return visited


def BFS(G, v):
    queue = deque(v)
    visited = {}

    for node in G.dict.keys():
        visited[node] = False

    visited[v] = True

    while queue:
        w = queue.popleft()

        for x in G.dict[w]:
            if not visited[x]:
                visited[x] = True
                queue.append(x)

    return visited
