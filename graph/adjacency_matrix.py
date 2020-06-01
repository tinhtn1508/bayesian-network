
class AdjacencyMatrix(object):
    def __init__(self, verticesList = None, digraph = False):
        self.__digraph = digraph
        self.__map = {}
        self.__inDegreeMap = {}
        self.__outDegreeMap = {}
        self.__edgesSet = set()
        if verticesList is not None:
            for v in verticesList:
                self.__map[v] = {}
                for _v in verticesList:
                    self.__map[v][_v] = None
                self.__inDegreeMap[v] = 0
                self.__outDegreeMap[v] = 0

    def addNewNode(self, node):
        if node in self.__map: return
        self.__map[node] = {}
        for v in self.__map.keys():
            self.__map[v][node] = None
            self.__map[node][v] = None

    def addPath(self, startNode, endNode, value):
        if startNode is None or endNode is None: raise Exception("input None node")
        if value is None: raise Exception("input None value")
        if startNode not in self.__map: self.addNewNode(startNode)
        if endNode not in self.__map: self.addNewNode(endNode)
        isNewPath = self.__map[startNode][endNode] is None
        self.__map[startNode][endNode] = value
        self.__edgesSet.add((startNode, endNode))
        if not self.__digraph:
            self.__map[endNode][startNode] = value
            self.__edgesSet.add((endNode, startNode))
        if startNode not in self.__outDegreeMap: self.__outDegreeMap[startNode] = 0
        if endNode not in self.__outDegreeMap: self.__outDegreeMap[endNode] = 0
        if startNode not in self.__inDegreeMap: self.__inDegreeMap[startNode] = 0
        if endNode not in self.__inDegreeMap: self.__inDegreeMap[endNode] = 0
        if isNewPath:
            self.__outDegreeMap[startNode] += 1
            self.__inDegreeMap[endNode] += 1
            if not self.__digraph:
                self.__outDegreeMap[endNode] += 1
                self.__inDegreeMap[startNode] += 1

    def getPath(self, startNode, endNode):
        if startNode is None or endNode is None: raise Exception("input None node")
        if startNode not in self.__map: raise Exception("cannot found start node in map")
        if endNode not in self.__map[startNode]: raise Exception("cannot found end node in map")
        return self.__map[startNode][endNode]

    def deletePath(self, startNode, endNode):
        if startNode is None or endNode is None: raise Exception("input None node")
        if startNode not in self.__map: raise Exception("cannot found start node in map")
        if endNode not in self.__map[startNode]: raise Exception("cannot found end node in map")
        if self.__map[startNode][endNode] is None: return
        self.__map[startNode][endNode] = None
        self.__outDegreeMap[startNode] -= 1
        self.__inDegreeMap[endNode] -= 1
        self.__edgesSet.remove((startNode, endNode))
        if not self.__digraph:
            self.__edgesSet.remove((endNode, startNode))
            self.__map[endNode][startNode] = None
            self.__outDegreeMap[endNode] -= 1
            self.__inDegreeMap[startNode] -= 1

    def allSuccessors(self, v):
        if v is None: raise Exception("input None vertex")
        if v not in self.__map: raise Exception(f"input vertex not in graph ({v})")
        adj = self.__map[v]
        for k in adj.keys():
            if adj[k] is not None: yield (k, adj[k])

    def allInorderedSuccessors(self, v):
        if v is None: raise Exception("input None vertex")
        if v not in self.__map: raise Exception(f"input vertex not in graph ({v})")
        adj = self.__map[v]
        for k in sorted(adj.keys()):
            if adj[k] is not None: yield (k, adj[k])

    def allPredecessor(self, v):
        if v is None: raise Exception("input None vertex")
        if v not in self.__map: raise Exception("input vertex not in graph")
        keys = self.vertexSet()
        for k in keys:
            if self.__map[k][v] is not None: yield (k, self.__map[k][v])

    def vertexSet(self):
        return self.__map.keys()

    def allVertexes(self):
        for k in self.__map.keys(): yield k

    def allInorderedVertexes(self):
        for k in sorted(self.__map.keys()): yield k

    def checkVertexExist(self, v):
        if v is None: raise Exception("input None vertex")
        return v in self.__map

    def zeroInDegreeVertexes(self):
        for v in self.__inDegreeMap.keys():
            if self.__inDegreeMap[v] == 0: yield v

    def zeroOutDegreeVertexes(self):
        for v in self.__outDegreeMap.keys():
            if self.__outDegreeMap[v] == 0: yield v

    def isDigraph(self):
        return self.__digraph

    def allEdges(self):
        for s, e in self.__edgesSet:
            yield (s, e, self.__map[s][e])

    def __str__(self):
        if not self.__map: raise Exception('Map is empty')
        keys = sorted(self.__map.keys())
        result = "vertices: " + str(keys) + '\n' + "Matrix: " + '\n'
        for kstart in keys:
            for kend in keys:
                result += "{:<10}".format(str(self.__map[kstart][kend])) + ' '
            result += '\n'
        return result
