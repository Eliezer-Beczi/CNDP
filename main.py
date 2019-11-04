# local imports
from model.graph import Graph
import utils.cnp as cnp


def main():
    G = Graph("input.txt")
    dot = G.genDOTSrcCode()
    dot.render("original.gv", view=True)

    N = 20
    S, fitness = cnp.genetic_algorithm(G, 50, N)
    print(fitness)


main()
