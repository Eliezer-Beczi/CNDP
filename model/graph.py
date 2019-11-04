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
                self.dict[src] = []

                for dest in arr[1].split():
                    self.dict[src].append(dest)

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
                self.dict[node] = []

    def removeNode(self, node):
        try:
            del self.dict[node]
        except:
            raise Exception("Node is not present!")

        for val in self.dict.values():
            try:
                val.remove(node)
            except:
                pass

        return True

    def addEdge(self, u, v):
        if u not in self.dict:
            self.dict[u] = v
        else:
            for node in v:
                if node not in self.dict[u]:
                    self.dict[u].append(node)

        for node in v:
            if node not in self.dict:
                self.dict[node] = [u]
            else:
                if u not in self.dict[node]:
                    self.dict[node].append(u)

    def removeEdge(self, u, v):
        if u in self.dict:
            try:
                self.dict[u].remove(v)
            except:
                pass

        if v in self.dict:
            try:
                self.dict[v].remove(u)
            except:
                pass

    def printToFile(self, fileName="output.txt"):
        f = open(fileName, 'w')

        for src, val in self.dict.items():
            for dest in val:
                f.write(f"{src} {dest}\n")
                f.write(f"{dest} {src}\n")

        f.close()

    def __str__(self):
        string = ""

        for u, nbrs in self.dict.items():
            string += f"{u} => [ "

            for i in range(len(nbrs) - 1):
                string += f"{nbrs[i]}, "

            if len(nbrs) > 0:
                string += f"{nbrs[-1]}"

            string += " ]\n"

        return string
