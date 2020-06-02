import random
import functools
import networkx as nx
from networkx.algorithms.approximation import vertex_cover

import utils.connectivity_metrics as connectivity_metric
import utils.objective_functions as objective_function


def greedy_cnp(G, k):
    S0 = vertex_cover.min_weighted_vertex_cover(G)

    while len(S0) > k:
        B = objective_function.minimize_pairwise_connectivity(G, S0)
        i = random.choice(B)
        S0.discard(i)

    return S0


def genetic_algorithm(G, k, N=100, pi_min=50, pi_max=90, delta_pi=2.5, alpha=2, tmax=1000):
    def fitness_function(S):
        subgraph = nx.subgraph_view(G, filter_node=lambda n: n not in S)
        metric = connectivity_metric.pairwise_connectivity(subgraph)
        commonalities = S.intersection(best_S)

        return metric + gamma * len(commonalities)

    def my_cmp(a, b):
        return fitness_function(a) - fitness_function(b)

    t = 0
    P = []
    gamma = 1
    pi = pi_min
    my_key = functools.cmp_to_key(my_cmp)

    # for _ in range(N // 10):
    #     P.append(greedy_cnp(G, k))

    while len(P) < N:
        P.append(_generate_random_solution(G, k))

    best_S = P[0].copy()
    best_S_fitness = fitness_function(best_S)

    while t < tmax:
        new_P = _new_generation(k, N, P)
        new_P = _mutation(G, k, N, new_P, pi)

        P.extend(new_P)
        P.sort(key=my_key)
        P = P[:N]

        curr_S = P[0]
        curr_S_fitness = fitness_function(curr_S)

        if curr_S_fitness < best_S_fitness:
            best_S = curr_S.copy()
            best_S_fitness = curr_S_fitness
            pi = pi_min
        else:
            pi = min(pi + delta_pi, pi_max)

        gamma = _update(G, best_S, P, alpha)
        t += 1

    return best_S, best_S_fitness


"""
=================
PRIVATE FUNCTIONS
=================
"""


def _generate_random_solution(G, k):
    S = list(G)

    while len(S) > k:
        S.pop(random.randrange(len(S)))

    return set(S)


def _new_generation(k, N, P):
    new_P = []

    for _ in range(N):
        r1 = random.randrange(N)
        r2 = random.randrange(N)

        while r1 == r2:
            r2 = random.randrange(N)

        new_S = P[r1].union(P[r2])

        if len(new_S) == k:
            new_P.append(new_S)
        else:
            tmp = list(new_S)
            random.shuffle(tmp)
            tmp = tmp[:k]

            new_P.append(set(tmp))

    return new_P


def _mutation(G, k, N, P, pi):
    new_P = []

    for i in range(N):
        r = random.randint(1, 100)

        if r <= pi:
            new_S = list(P[i])
            ng = random.randint(0, k)
            random.shuffle(new_S)

            for _ in range(ng):
                new_S.pop()

            nodes = list(set(G) - set(new_S))
            random.shuffle(nodes)

            while len(new_S) < k:
                u = nodes.pop()
                new_S.append(u)

            new_P.append(set(new_S))
        else:
            S = P[i]
            new_P.append(S)

    return new_P


def _update(G, best_S, P, alpha):
    subgraph = nx.subgraph_view(G, filter_node=lambda n: n not in best_S)
    metric = connectivity_metric.pairwise_connectivity(subgraph)
    avg = 0

    for S in P:
        avg += len(S.intersection(best_S))

    avg /= len(P)

    try:
        gamma = (alpha * metric) / avg
    except:
        gamma = 1

    return gamma
