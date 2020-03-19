import networkx as nx
from platypus import NSGAII, default_variator, Problem, Subset

G = nx.read_adjlist("input/Ventresca/BarabasiAlbert_n500m1.txt")
k = 50
num_of_tests = 10


class SmartNSGAII(NSGAII):
    def __init__(self, problem):
        super(SmartNSGAII, self).__init__(problem)

    def initialize(self):
        super(SmartNSGAII, self).initialize()

        # if self.archive is not None:
        #     self.archive += self.population
        #
        # if self.variator is None:
        #     self.variator = default_variator(self.problem)


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


algorithm = SmartNSGAII(BOCNDP())
algorithm.run(10)
