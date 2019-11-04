# system imports
import copy
import random
import functools

# local imports
from .vertex_cover import greedy_vertex_cover
import utils.objective_functions as objective_functions
import utils.connectivity_metrics as connectivity_metrics


def greedy_cnp(G, k):
    S0 = greedy_vertex_cover(G)
    MIS = copy.deepcopy(G)

    for node in S0:
        MIS.removeNode(node)

    while len(S0) > k:
        B = objective_functions.minimize_pairwise_connectivity(G, MIS, S0)
        i = random.choice(B)
        S0.remove(i)
        MIS.addEdge(i, list(set(G.dict[i]) - set(S0)))

    return S0


def genetic_algorithm(G, k, N, pi_min=5, pi_max=50, delta_pi=5, alpha=0.2, tmax=1000):
    """
    ================
    helper functions
    ================
    """

    def _fitness_function(S):
        new_G = _truncate_graph(G, S)
        metric = connectivity_metrics.pairwise_connectivity(new_G)
        commonalities = list(set(S).intersection(set(best_S)))

        return metric + gamma * len(commonalities)

    def my_cmp(a, b):
        return _fitness_function(a) - _fitness_function(b)

    """
    =========
    variables
    =========
    """

    t = 0
    pi = pi_min
    my_key = functools.cmp_to_key(my_cmp)

    """
    =========
    algorithm
    =========
    """

    P = []  # population

    # fill half of the population with random solutions
    for i in range(N // 2):
        P.append(greedy_cnp(G, k))

    # fill the other half with greedy generated ones
    while len(P) < N:
        P.append(_generate_random_solution(G, k))

    best_S = P[0].copy()  # best solution
    gamma = _update(G, best_S, P, alpha)
    best_S_fitness = _fitness_function(best_S)  # fitness of the best solution

    while t < tmax:
        new_P = _new_generation(G, k, N, P)
        _mutation(G, k, N, new_P, pi)

        P.extend(new_P)
        P.sort(key=my_key)
        P = P[:N]

        # keep track of best solution
        curr_S = P[0]
        curr_S_fitness = _fitness_function(curr_S)

        if best_S_fitness < curr_S_fitness:
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


def _truncate_graph(G, S):
    new_G = copy.deepcopy(G)

    for node in S:
        new_G.removeNode(node)

    return new_G


def _generate_random_solution(G, k):
    S = [*G.dict]

    while len(S) > k:
        S.pop(random.randrange(len(S)))

    return S


def _new_generation(G, k, N, P):
    new_P = []

    for i in range(N):
        r1 = random.randrange(N)
        r2 = random.randrange(N)

        while r1 == r2:
            r2 = random.randrange(N)

        new_S = list(set(P[r1] + P[r2]))
        MIS = copy.deepcopy(G)

        for node in new_S:
            MIS.removeNode(node)

        while len(new_S) > k:
            B = objective_functions.minimize_pairwise_connectivity(
                G, MIS, new_S)
            u = random.choice(B)
            new_S.remove(u)
            MIS.addEdge(u, list(set(G.dict[u]) - set(new_S)))

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

            MIS = copy.deepcopy(G)

            for node in new_S:
                MIS.removeNode(node)

            while len(new_S) < k:
                B = objective_functions.maximize_disconnected_pairs(MIS, k)
                u = random.choice(B)
                new_S.append(u)
                MIS.removeNode(u)


def _update(G, best_S, P, alpha):
    new_G = _truncate_graph(G, best_S)
    metric = connectivity_metrics.pairwise_connectivity(new_G)
    avg = 0

    for S in P:
        avg += len(list(set(S).intersection(set(best_S))))

    avg /= len(P)

    if avg == 0:
        return alpha * metric
    else:
        return (alpha * metric) / avg
