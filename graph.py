from graphviz import Digraph
from collections import deque


class Graph():
    def __init__(self, filePath):
        with open(filePath) as f:
            self.dict = {}

            for line in f:
                arr = line.split()
                print(arr)

                src = arr[0]
                dest = arr[1]

                if src in self.dict:
                    self.dict[src].append(dest)
                else:
                    self.dict[src] = [dest]

                if dest in self.dict:
                    self.dict[dest].append(src)
                else:
                    self.dict[dest] = [src]

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

    def removeNodeFromGraph(self, node):
        try:
            del self.dict[node]
        except:
            print("Node is not present!")
            return False

        for val in self.dict.values():
            try:
                val.remove(node)
            except:
                pass

        return True

    def printToFile(self, fileName="output.txt"):
        f = open(fileName, 'w')

        for src, val in self.dict.items():
            for dest in val:
                f.write(f"{src} {dest}\n")
                f.write(f"{dest} {src}\n")

        f.close()
