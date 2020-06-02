import multiprocessing as mp
import statistics

import networkx as nx
from platypus import NSGAII, EpsMOEA, SPEA2, IBEA, PAES, EpsNSGAII, Problem, Subset

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


def get_critical_nodes():
    algorithm = NSGAII(BOCNDP())
    # algorithm = EpsMOEA(BOCNDP(), epsilons=[0.05])
    # algorithm = SPEA2(BOCNDP())
    # algorithm = IBEA(BOCNDP())
    # algorithm = PAES(BOCNDP())
    # algorithm = EpsNSGAII(BOCNDP(), epsilons=[0.05])
    algorithm.run(10000)

    print(algorithm.result[0].objectives)
    return algorithm.result[0].objectives


if __name__ == '__main__':
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
