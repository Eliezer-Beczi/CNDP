import networkx as nx
import utils.connectivity_metrics as connectivity_metric
from platypus import NSGAII, EpsMOEA, NSGAIII, EpsNSGAII, Problem, Dominance, Subset, TournamentSelector, \
    HypervolumeFitnessEvaluator, Archive
import statistics
import multiprocessing as mp

G = nx.read_adjlist("input/Ventresca/BarabasiAlbert_n500m1.txt")
k = 1
num_of_tests = 1


def get_pairwise_connectivity(exclude=None):
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
        solution.objectives[0] = get_pairwise_connectivity(solution.variables[0])


class NashDominance(Dominance):
    def __init__(self):
        super(NashDominance, self).__init__()

    def compare(self, x, y):
        k1 = 0
        k2 = 0

        nodes_x = x.variables[0][:]
        nodes_y = y.variables[0][:]

        metric_x = x.objectives[0]
        metric_y = y.objectives[0]

        for i in range(k):
            tmp = nodes_x[i]
            nodes_x[i] = nodes_y[i]

            if get_pairwise_connectivity(nodes_x) < metric_x:
                k1 += 1

            nodes_x[i] = tmp

        for i in range(k):
            tmp = nodes_y[i]
            nodes_y[i] = nodes_x[i]

            if get_pairwise_connectivity(nodes_y) < metric_y:
                k2 += 1

            nodes_y[i] = tmp

        if k1 < k2:
            return -1
        elif k1 > k2:
            return 1
        else:
            return 0


class NashArchive(Archive):
    def __init__(self):
        super(NashArchive, self).__init__(dominance=NashDominance())


def get_critical_nodes():
    algorithm = NSGAII(CNDP(), selector=TournamentSelector(dominance=NashDominance()), archive=NashArchive())
    algorithm.run(1000)

    fitness = algorithm.result[0].objectives[0]
    print(fitness)

    return fitness


if __name__ == '__main__':
    pool = mp.Pool(mp.cpu_count())
    samples = pool.starmap_async(get_critical_nodes, [() for _ in range(num_of_tests)]).get()
    pool.close()

    avg = sum(samples) / len(samples)
    stdev = statistics.stdev(samples)

    print(f"Average: {avg}")
    print(f"Standard Deviation: {stdev}")
