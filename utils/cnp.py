# system imports
import random
import functools

# local imports
from .vertex_cover import greedy_vertex_cover
import utils.objective_functions as objective_functions
import utils.connectivity_metrics as connectivity_metrics
import utils.subgraph_store as subgraph_store


def greedy_cnp(G, k):
    S0 = greedy_vertex_cover(G)

    try:
        MIS = subgraph_store.retrieve_from_store(S0)
    except:
        MIS = subgraph_store.add_to_store(G, S0)

    while len(S0) > k:
        B = objective_functions.minimize_pairwise_connectivity(G, MIS, S0)
        i = random.choice(B)
        S0.remove(i)

        try:
            MIS = subgraph_store.retrieve_from_store(S0)
        except:
            MIS = subgraph_store.add_to_store(G, S0)

    return S0


def genetic_algorithm(G, k, N, pi_min=5, pi_max=50, delta_pi=5, alpha=0.2, tmax=100):
    def _fitness_function(S):
        try:
            subgraph = subgraph_store.retrieve_from_store(S)
        except:
            subgraph = subgraph_store.add_to_store(G, S)

        metric = connectivity_metrics.pairwise_connectivity(subgraph)
        commonalities = list(set(S).intersection(set(best_S)))

        return metric + gamma * len(commonalities)

    def my_cmp(a, b):
        return _fitness_function(a) - _fitness_function(b)

    my_key = functools.cmp_to_key(my_cmp)

    t = 0
    pi = pi_min
    P = []

    for _ in range(N):
        P.append(_generate_random_solution(G, k))

    best_S = P[0].copy()
    gamma = _update(G, best_S, P, alpha)
    best_S_fitness = _fitness_function(best_S)

    print(best_S_fitness)

    while t < tmax:
        print(f"Generation: {t + 1}")

        new_P = _new_generation(k, N, P)
        _mutation(G, k, N, new_P, pi)

        P.extend(new_P)
        P.sort(key=my_key)
        P = P[:N]

        curr_S = P[0]
        curr_S_fitness = _fitness_function(curr_S)

        if best_S_fitness > curr_S_fitness:
            best_S = curr_S.copy()
            best_S_fitness = curr_S_fitness
            pi = pi_min

            print(best_S_fitness)
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
    S = [*G.dict]

    while len(S) > k:
        S.pop(random.randrange(len(S)))

    return S


def _new_generation(k, N, P):
    new_P = []

    for i in range(N):
        r1 = random.randrange(N)
        r2 = random.randrange(N)

        while r1 == r2:
            r2 = random.randrange(N)

        new_S = list(set(P[r1] + P[r2]))
        random.shuffle(new_S)

        if len(new_S) > k:
            new_S = new_S[:k]

        new_P.append(new_S)

    return new_P


def _mutation(G, k, N, new_P, pi):
    for i in range(N):
        r = random.randint(1, 100)

        if r <= pi:
            new_S = new_P[i]
            ng = random.randint(0, k)

            for j in range(ng):
                new_S.pop(random.randrange(len(new_S)))

            nodes = G.dict.keys() - set(new_S)

            while len(new_S) < k:
                u = random.choice(tuple(nodes))
                new_S.append(u)
                nodes.discard(u)


def _update(G, best_S, P, alpha):
    try:
        subgraph = subgraph_store.retrieve_from_store(best_S)
    except:
        subgraph = subgraph_store.add_to_store(G, best_S)

    avg = 0
    metric = connectivity_metrics.pairwise_connectivity(subgraph)

    for S in P:
        avg += len(list(set(S).intersection(set(best_S))))

    avg /= len(P)

    if avg == 0:
        return alpha * metric
    else:
        return (alpha * metric) / avg
