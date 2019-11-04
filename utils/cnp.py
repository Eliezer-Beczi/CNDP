# system imports
import copy
import random

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


def genetic_algorithm(G, k, N, pi_min=0.3, alpha=0.5, tmax=1000):
    t = 0  # iteration counter
    P = []  # population
    best_S = []  # best solution
    pi = pi_min

    """
    helper functions
    """

    def truncate_graph(S):
        new_G = copy.deepcopy(G)

        for node in S:
            new_G.removeNode(node)

        return new_G

    """
    initialization
    """

    def fitness_function(S, gamma):
        new_G = truncate_graph(S)
        metric = connectivity_metrics.pairwise_connectivity(new_G)
        commonalities = list(set(S).intersection(set(best_S)))

        return metric + gamma * len(commonalities)

    def generate_random_solution():
        S = [*G.dict]

        while len(S) > k:
            S.pop(random.randrange(len(S)))

        return S

    # fill half of the population with random solutions
    for i in range(N // 2):
        P.append(generate_random_solution())

    # fill the other half with greedy generated ones
    while len(P) < N:
        P.append(greedy_cnp(G, k))

    """
    reproduction
    """

    def new_generation():
        new_P = []

        for i in range(N):
            i1 = random.randrange(N)
            i2 = random.randrange(N)

            while i1 == i2:
                i2 = random.randrange(N)

            new_S = list(set(P[i1] + P[i2]))
            MIS = copy.deepcopy(G)

            for node in new_S:
                MIS.removeNode(node)

            while len(new_S) > k:
                B = objective_functions.minimize_pairwise_connectivity(
                    G, MIS, new_S)
                i = random.choice(B)
                new_S.remove(i)
                MIS.addEdge(i, list(set(G.dict[i]) - set(new_S)))

            new_P.append(new_S)

        return new_P

    """
    mutation
    """

    def mutation():
        for i in range(N):
            new_S = new_P[i]
            r = random.randint(1, 100)

            if r <= pi:
                ng = random.randint(0, k)

                for j in range(ng):
                    new_S.pop(random.randrange(len(new_S)))

                MIS = copy.deepcopy(G)

                for node in new_S:
                    MIS.removeNode(node)

                while len(new_S) < k:
                    B = objective_functions.maximize_disconnected_pairs(
                        G, MIS, k)
                    i = random.choice(B)
                    new_S.append(i)
                    MIS.removeNode(i)

    """
    ordering and selection
    """

    def update():
        new_G = truncate_graph(best_S)
        metric = connectivity_metrics.pairwise_connectivity(new_G)
        avg = 0

        for S in P:
            avg += len(list(set(S).intersection(set(best_S))))

        avg /= len(P)

        return (alpha * metric) / avg

    while t < tmax:
        new_P = new_generation()
        t += 1
