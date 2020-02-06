import networkx as nx
import utils.connectivity_metrics as connectivity_metric
from platypus import NSGAII, EpsMOEA, NSGAIII, EpsNSGAII, Problem, Dominance, Subset, TournamentSelector, \
    HypervolumeFitnessEvaluator
import statistics
import multiprocessing as mp

G = nx.read_adjlist("input/Ventresca/BarabasiAlbert_n500m1.txt")
k = 50
num_of_tests = 10


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


class BergeDominance(Dominance):
    def __init__(self):
        super(BergeDominance, self).__init__()

    def compare(self, x, y):
        k1 = 0
        k2 = 0

        nodes_x = x.variables[0][:]
        nodes_y = y.variables[0][:]

        metric_x = getPairwiseConnectivity(nodes_x)
        metric_y = getPairwiseConnectivity(nodes_y)

        for i in range(k):
            tmp = nodes_y[i]
            nodes_y[i] = nodes_x[i]

            if getPairwiseConnectivity(nodes_y) < metric_x:
                k1 += 1

            nodes_y[i] = tmp

        for i in range(k):
            tmp = nodes_x[i]
            nodes_x[i] = nodes_y[i]

            if getPairwiseConnectivity(nodes_x) < metric_y:
                k2 += 1

            nodes_x[i] = tmp

        if k1 < k2:
            return -1
        elif k1 > k2:
            return 1
        else:
            return 0


def get_critical_nodes():
    algorithm = NSGAII(CNDP(), selector=TournamentSelector(dominance=BergeDominance()))
    # algorithm = EpsMOEA(CNDP(), epsilons=[0.05], selector=TournamentSelector(dominance=BergeDominance()))
    # algorithm = NSGAIII(CNDP(), divisions_outer=12, selector=TournamentSelector(dominance=BergeDominance()))
    # algorithm = EpsNSGAII(CNDP(), epsilons=[0.05], selector=TournamentSelector(dominance=BergeDominance()))
    algorithm.run(1)

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
