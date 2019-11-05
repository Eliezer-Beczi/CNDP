# system imports
from collections import deque

# third party imports
from graphviz import Digraph


class Graph():
    def __init__(self, filePath):
        with open(filePath) as f:
            _ = f.readline()  # number of nodes
            self.dict = {}

            for line in f:
                arr = line.split(':')

                src = arr[0]
                self.dict[src] = set()

                for dest in arr[1].split():
                    self.dict[src].add(dest)

    def genDOTSrcCode(self):
        dot = Digraph("G")
        dot.graph_attr["ranksep"] = "0.5"
        dot.graph_attr["nodesep"] = "0.5"
        dot.graph_attr["rankdir"] = "LR"
        dot.graph_attr["fontsize"] = "10"
        dot.graph_attr["compound"] = "true"

        dot.node_attr["shape"] = "circle"
        dot.node_attr["fontsize"] = "10"
        dot.node_attr["style"] = "filled"
        dot.node_attr["fillcolor"] = "yellow"

        dot.edge_attr["dir"] = "none"

        for node in self.dict:
            dot.node(node)

        visited = []

        for src, val in self.dict.items():
            for dest in val:
                if dest not in visited:
                    dot.edge(src, dest)

            visited.append(src)

        return dot

    def addNode(self, *nodes):
        for node in nodes:
            if node not in self.dict:
                self.dict[node] = set()

    def removeNode(self, node):
        try:
            del self.dict[node]
        except:
            raise Exception("Node is not present!")

        for val in self.dict.values():
            val.discard(node)

        return True

    def addEdge(self, u, v):
        if u not in self.dict:
            self.dict[u] = v
        else:
            for node in v:
                if node not in self.dict[u]:
                    self.dict[u].add(node)

        for node in v:
            if node not in self.dict:
                self.dict[node] = set([u])
            else:
                if u not in self.dict[node]:
                    self.dict[node].add(u)

    def removeEdge(self, u, v):
        self.dict[u].discard(v)
        self.dict[v].remove(u)

    def printToFile(self, fileName="output.txt"):
        f = open(fileName, 'w')

        for src, val in self.dict.items():
            f.write(f"{src}: ")

            for dest in val:
                f.write(f"{dest} ")

            f.write("\n")

        f.close()

    def __str__(self):
        string = ""

        for u, nbrs in self.dict.items():
            string += f"{u}: "

            for v in nbrs:
                string += f"{v} "

            string += "\n"

        return string
