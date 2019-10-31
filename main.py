# local imports
from model.graph import Graph
from utils.vertex_cover import greedy_vertex_cover


def main():
    G = Graph("input.txt")
    dot = G.genDOTSrcCode()
    dot.render("original.gv", view=True)


main()
