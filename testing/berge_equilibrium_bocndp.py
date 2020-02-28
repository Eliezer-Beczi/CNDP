import multiprocessing as mp
import statistics

import networkx as nx
from platypus import NSGAII, Problem, Subset, Dominance, TournamentSelector

G = nx.read_adjlist("input/Ventresca/BarabasiAlbert_n500m1.txt")
k = 50
num_of_tests = 10


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


class BergeDominance(Dominance):
    def __init__(self):
        super(BergeDominance, self).__init__()

    def compare(self, x, y):
        k1 = 0
        k2 = 0

        nodes_x = x.variables[0][:]
        nodes_y = y.variables[0][:]

        D_x = x.objectives[0]
        D_y = y.objectives[0]

        var_D_x = x.objectives[1]
        var_D_y = y.objectives[1]

        for i in range(k):
            tmp = nodes_y[i]
            nodes_y[i] = nodes_x[i]

            if connected_components(nodes_y) > D_x:
                k1 += 1

            if cardinality_variance(nodes_y) < var_D_x:
                k1 += 1

            nodes_y[i] = tmp

        for i in range(k):
            tmp = nodes_x[i]
            nodes_x[i] = nodes_y[i]

            if connected_components(nodes_x) > D_y:
                k2 += 1

            if cardinality_variance(nodes_x) < var_D_y:
                k2 += 1

            nodes_x[i] = tmp

        if k1 < k2:
            return -1
        elif k1 > k2:
            return 1
        else:
            return 0


def get_critical_nodes():
    algorithm = NSGAII(BOCNDP(), selector=TournamentSelector(dominance=BergeDominance()))
    algorithm.run(500)

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
