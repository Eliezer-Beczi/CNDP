import networkx as nx
from graphviz import Source

import utils.cnp as cnp


def main():
    G = nx.read_adjlist("input/Ventresca/BarabasiAlbert_n500m1.txt")
    src = Source(nx.nx_pydot.to_pydot(G))
    src.render("graph.gv", view=True)

    S, S_fitness = cnp.genetic_algorithm(G, 50, 50)


main()
