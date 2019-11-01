# local imports
from model.graph import Graph
from utils.cnp import greedy_cnp


def main():
    G = Graph("input.txt")
    dot = G.genDOTSrcCode()
    dot.render("original.gv", view=True)

    print(greedy_cnp(G, 4))


main()
