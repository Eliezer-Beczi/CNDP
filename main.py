# local imports
from model.graph import Graph
import utils.cnp as cnp


def main():
    G = Graph("input.txt")
    dot = G.genDOTSrcCode()
    dot.render("original.gv", view=True)

    N = 10
    cnp.genetic_algorithm(G, 3, N)


main()
