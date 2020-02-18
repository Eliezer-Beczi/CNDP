import multiprocessing as mp
import statistics

import networkx as nx
from platypus import NSGAII, Problem, Subset

G = nx.read_adjlist("input/Ventresca/BarabasiAlbert_n500m1.txt")
k = 50
num_of_tests = 10


def connectedComponents(exclude=None):
    if exclude is None:
        exclude = {}

    S = set(exclude)
    subgraph = nx.subgraph_view(G, filter_node=lambda n: n not in S)
    return nx.connected_components(subgraph)


def cardinalityVariance(exclude=None):
    if exclude is None:
        exclude = {}

    S = set(exclude)
    subgraph = nx.subgraph_view(G, filter_node=lambda n: n not in S)
    components = nx.connected_components(subgraph)

    num_of_components = len(list(components))
    num_of_nodes = subgraph.number_of_nodes()
    variance = 0

    for component in components:
        cardinality = len(component)
        variance += (cardinality - num_of_nodes / num_of_components) ** 2

    variance /= num_of_components
    return variance


class CNDP(Problem):
    def __init__(self):
        super(CNDP, self).__init__(1, 2)
        self.types[:] = Subset(list(G), k)
        self.directions[0] = Problem.MAXIMIZE
        self.directions[1] = Problem.MINIMIZE

    def evaluate(self, solution):
        x = solution.variables[0]
        solution.objectives[0] = connectedComponents(x)
        solution.objectives[1] = cardinalityVariance(x)


def get_critical_nodes():
    algorithm = NSGAII(CNDP())
    # algorithm = EpsMOEA(CNDP(), epsilons=[0.05], selector=TournamentSelector(dominance=NashDominance()))
    # algorithm = NSGAIII(CNDP(), divisions_outer=12, selector=TournamentSelector(dominance=NashDominance()))
    # algorithm = EpsNSGAII(CNDP(), epsilons=[0.05], selector=TournamentSelector(dominance=NashDominance()))
    algorithm.run(500)

    fitness = algorithm.result[0].objectives[0]
    print(fitness)

    return fitness


pool = mp.Pool(mp.cpu_count())
samples = pool.starmap_async(get_critical_nodes, [() for _ in range(num_of_tests)]).get()
pool.close()

avg = sum(samples) / len(samples)
stdev = statistics.stdev(samples)

print(f"Average: {avg}")
print(f"Standard Deviation: {stdev}")
