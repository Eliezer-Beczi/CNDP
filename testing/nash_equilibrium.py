import networkx as nx
import utils.connectivity_metrics as connectivity_metric
from platypus import NSGAII, Problem, Dominance, Subset, TournamentSelector

k = 50
G = nx.read_adjlist("input/Ventresca/BarabasiAlbert_n500m1.txt")


def getPairwiseConnectivity(exclude=None):
    if exclude is None:
        exclude = {}

    S = set(exclude)
    subgraph = nx.subgraph_view(G, filter_node=lambda n: n not in S)
    return connectivity_metric.pairwise_connectivity(subgraph)


class CNDP(Problem):
    def __init__(self):
        super(CNDP, self).__init__(1, 1)
        self.types[:] = Subset(list(G), k)

    def evaluate(self, solution):
        solution.objectives[0] = getPairwiseConnectivity(solution.variables[0])


class NashDominance(Dominance):
    def __init__(self):
        super(NashDominance, self).__init__()

    def compare(self, x, y):
        k1 = 0
        k2 = 0

        nodes_x = x.variables[0][:]
        nodes_y = y.variables[0][:]

        metric_x = getPairwiseConnectivity(nodes_x)
        metric_y = getPairwiseConnectivity(nodes_y)

        for i in range(k):
            tmp = nodes_x[i]
            nodes_x[i] = nodes_y[i]

            if getPairwiseConnectivity(nodes_x) < metric_x:
                k1 += 1

            nodes_x[i] = tmp

        for i in range(k):
            tmp = nodes_y[i]
            nodes_y[i] = nodes_x[i]

            if getPairwiseConnectivity(nodes_y) < metric_y:
                k2 += 1

            nodes_y[i] = tmp

        if k1 < k2:
            return -1
        elif k1 > k2:
            return 1
        else:
            return 0


algorithm = NSGAII(CNDP(), selector=TournamentSelector(dominance=NashDominance()))
algorithm.run(10000)

for s in algorithm.result:
    print(f"{s.variables[0]} => {s.objectives[0]}")
