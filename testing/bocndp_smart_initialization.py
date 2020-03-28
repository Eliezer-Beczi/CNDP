import multiprocessing as mp
import random
import statistics

import networkx as nx
from platypus import NSGAII, Problem, Subset, Generator, Solution
from operator import itemgetter

G = nx.read_adjlist("input/Ventresca/WattsStrogatz_n250.txt")
k = 70
num_of_tests = 10


class DfsGenerator(Generator):
    def __init__(self):
        super(DfsGenerator, self).__init__()
        self.step_size = G.number_of_nodes() // k

    def generate(self, problem):
        solution = Solution(problem)
        solution.variables[0] = list(nx.dfs_preorder_nodes(G, source=random.choice(list(G))))[::self.step_size]
        return solution


class DegreeGenerator(Generator):
    def __init__(self):
        super(DegreeGenerator, self).__init__()

    def generate(self, problem):
        solution = Solution(problem)
        data = sorted(list(G.degree()), key=itemgetter(1), reverse=True)
        solution.variables[0] = [arr[0] for arr in data][:k]
        return solution


def random_walk_restart(steps=10000, restart_prob=0.2):
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
        solution.variables[0] = random_walk_restart()
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


def get_critical_nodes():
    # algorithm = NSGAII(problem=BOCNDP(), generator=DfsGenerator())
    # algorithm = NSGAII(problem=BOCNDP(), generator=DegreeGenerator())
    algorithm = NSGAII(problem=BOCNDP(), generator=RandomWalkGenerator())
    algorithm.run(10000)

    print(algorithm.result[0].objectives)
    return algorithm.result[0].objectives


pool = mp.Pool(mp.cpu_count())
samples = pool.starmap_async(get_critical_nodes, [() for _ in range(num_of_tests)]).get()
pool.close()

D, var_D = list(zip(*samples))

avg_D = sum(D) / len(samples)
avg_var_D = sum(var_D) / len(samples)

stdev_D = statistics.stdev(D)
stdev_var_D = statistics.stdev(var_D)

print(f"Average D: {avg_D}")
print(f"Average var_D: {avg_var_D}")

print(f"Standard Deviation D: {stdev_D}")
print(f"Standard Deviation var_D: {stdev_var_D}")
