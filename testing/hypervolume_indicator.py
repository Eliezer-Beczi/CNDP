import multiprocessing as mp
import random
from operator import itemgetter

import networkx as nx
from platypus import NSGAII, Problem, Subset, Generator, Solution, SPEA2, EpsMOEA, IBEA, PAES, EpsNSGAII

G = nx.read_adjlist("input/Ventresca/WattsStrogatz_n250.txt")
k = 70


class DfsGenerator(Generator):
    def __init__(self):
        super(DfsGenerator, self).__init__()
        self.step_size = G.number_of_nodes() // k

    def generate(self, problem):
        solution = Solution(problem)
        solution.variables[0] = list(nx.dfs_preorder_nodes(G, source=random.choice(list(G))))[::self.step_size]
        return solution


# x - number of nodes with highest degree
def degree_random(x):
    solution = degree_random.nodes_sorted_degree[:x]

    while len(solution) < k:
        node = random.choice(degree_random.nodes_sorted_degree)

        if node not in solution:
            solution.append(node)

    random.shuffle(solution)
    return solution


degree_random.nodes_sorted_degree = [arr[0] for arr in
                                     sorted(list(G.degree()), key=itemgetter(1), reverse=True)]  # static variable


class DegreeGenerator(Generator):
    def __init__(self):
        super(DegreeGenerator, self).__init__()

    def generate(self, problem):
        solution = Solution(problem)
        solution.variables[0] = degree_random(random.randint(k // 3, (k * 2) // 3))
        return solution


def random_walk(steps=10000, restart_prob=0.2):
    visited = {}

    while True:
        core = random.choice(list(G))
        current = core

        for _ in range(steps + 1):
            if current in visited:
                visited[current] += 1
            else:
                visited[current] = 1

            restart = random.random()

            if restart < restart_prob:
                current = core
            else:
                neighbors = list(G[current])
                current = random.choice(neighbors)

        if len(visited) >= k:
            break
        else:
            visited = {}

    most_visited = sorted(visited, key=visited.get, reverse=True)
    return most_visited[:k]


class RandomWalkGenerator(Generator):
    def __init__(self):
        super(RandomWalkGenerator, self).__init__()

    def generate(self, problem):
        solution = Solution(problem)
        solution.variables[0] = random_walk()
        return solution


def connected_components(exclude=None):
    if exclude is None:
        exclude = {}

    S = set(exclude)
    subgraph = nx.subgraph_view(G, filter_node=lambda n: n not in S)
    return nx.number_connected_components(subgraph)


def cardinality_variance(exclude=None):
    if exclude is None:
        exclude = {}

    S = set(exclude)
    subgraph = nx.subgraph_view(G, filter_node=lambda n: n not in S)
    components = list(nx.connected_components(subgraph))

    num_of_components = len(components)
    num_of_nodes = subgraph.number_of_nodes()
    variance = 0

    for component in components:
        cardinality = len(component)
        variance += (cardinality - num_of_nodes / num_of_components) ** 2

    variance /= num_of_components
    return variance


class BOCNDP(Problem):
    def __init__(self):
        super(BOCNDP, self).__init__(1, 2)
        self.types[:] = Subset(list(G), k)
        self.directions[0] = Problem.MAXIMIZE
        self.directions[1] = Problem.MINIMIZE

    def evaluate(self, solution):
        x = solution.variables[0]
        solution.objectives[0] = connected_components(x)
        solution.objectives[1] = cardinality_variance(x)


def get_critical_nodes(algorithm, max_iter=1):
    algorithm.run(max_iter)
    return algorithm.result


def write2file(results):
    with open("results.txt", "w") as file:
        for result in results:
            for solution in result:
                file.write(f"{solution.objectives[0] * (-1)} {solution.objectives[1]}\n")

            file.write('\n')


# NSGAII with smart init
# algorithms = [
#     NSGAII(problem=BOCNDP(), generator=DfsGenerator()),
#     NSGAII(problem=BOCNDP(), generator=DegreeGenerator()),
#     NSGAII(problem=BOCNDP(), generator=RandomWalkGenerator())
# ]

# Pareto dominance
algorithms = [
    NSGAII(BOCNDP()),
    EpsMOEA(BOCNDP(), epsilons=[0.05]),
    SPEA2(BOCNDP()),
    IBEA(BOCNDP()),
    PAES(BOCNDP()),
    EpsNSGAII(BOCNDP(), epsilons=[0.05])
]

pool = mp.Pool(mp.cpu_count())
samples = pool.starmap(get_critical_nodes, [(algorithm, 10000) for algorithm in algorithms])
pool.close()

write2file(samples)
