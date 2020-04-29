import networkx as nx
from graphviz import Source
import statistics
import multiprocessing as mp

import utils.cnp as cnp
import utils.connectivity_metrics as connectivity_metrics


def get_critical_nodes_ga(G, k):
    S, _ = cnp.genetic_algorithm(G, k)
    subgraph = nx.subgraph_view(G, filter_node=lambda n: n not in S)

    fitness = connectivity_metrics.pairwise_connectivity(subgraph)
    print(fitness)

    return fitness


def get_critical_nodes_greedy(G, k):
    S = cnp.greedy_cnp(G, k)
    subgraph = nx.subgraph_view(G, filter_node=lambda n: n not in S)

    fitness = connectivity_metrics.pairwise_connectivity(subgraph)
    print(fitness)

    return fitness


if __name__ == '__main__':
    G = nx.read_adjlist("input/Ventresca/BarabasiAlbert_n500m1.txt")
    # src = Source(nx.nx_pydot.to_pydot(G))
    # src.render("graph.gv", view=True)

    k = 50
    num_of_tests = 10

    pool = mp.Pool(mp.cpu_count())
    samples = pool.starmap_async(get_critical_nodes_ga, [(G, k) for _ in range(num_of_tests)]).get()
    # samples = pool.starmap_async(get_critical_nodes_greedy, [(G, k) for _ in range(num_of_tests)]).get()
    pool.close()

    avg = sum(samples) / len(samples)
    stdev = statistics.stdev(samples)

    print(f"Average: {avg}")
    print(f"Standard Deviation: {stdev}")
