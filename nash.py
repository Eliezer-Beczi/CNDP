import networkx as nx
import utils.connectivity_metrics as connectivity_metric
from platypus import NSGAII, Problem, Subset

k = 50
G = nx.read_adjlist("input/Ventresca/BarabasiAlbert_n500m1.txt")


class CNDP(Problem):
    def __init__(self):
        super(CNDP, self).__init__(1, 1)
        self.types[:] = Subset(list(G), k)

    def evaluate(self, solution):
        S = set(solution.variables[0])
        subgraph = nx.subgraph_view(G, filter_node=lambda n: n not in S)
        metric = connectivity_metric.pairwise_connectivity(subgraph)
        solution.objectives[0] = metric


algorithm = NSGAII(CNDP())
algorithm.run(10000)

for s in algorithm.result:
    print(f"{s.variables[0]} => {s.objectives[0]}")
