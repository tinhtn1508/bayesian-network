from typing_extensions import Protocol
from typing import Dict, Optional, Generic, Generator, TypeVar, List, Set, Tuple, Hashable, Any, Union

C = TypeVar('C', bound = 'Comparable')

class Comparable(Protocol):
    def __eq__(self, other: Any) -> bool:
        ...

    def __lt__(self: C, other: C) -> bool:
        ...

    def __gt__(self: C, other: C) -> bool:
        return (not self < other) and (self != other)

    def __le__(self: C, other: C) -> bool:
        return (self < other) or (self == other)

    def __ge__(self: C, other: C) -> bool:
        return not self < other

V = TypeVar('V', bound = Union[Hashable, Comparable])
W = TypeVar('W', float, int)

class AdjacencyMatrix(Generic[V, W]):
    def __init__(self, verticesList: Optional[List[V]] = None,
                    digraph: bool = False) -> None:
        self.__digraph: bool                            = digraph
        self.__map: Dict[V, Dict[V, Optional[W]]]       = dict()
        self.__inDegreeMap: Dict[V, int]                = dict()
        self.__outDegreeMap: Dict[V, int]               = dict()
        self.__edgesSet: Set[Tuple[V, V]]               = set()

        if verticesList is not None:
            for v in verticesList:
                self.__map[v] = dict()
                for _v in verticesList:
                    self.__map[v][_v] = None
                self.__inDegreeMap[v] = 0
                self.__outDegreeMap[v] = 0

    def addNewNode(self, node: Optional[V]) -> None:
        if node is None: raise Exception("input None node")
        if node in self.__map: return
        self.__map[node] = dict()
        for v in self.__map.keys():
            self.__map[v][node] = None
            self.__map[node][v] = None

    def addPath(self, startNode: V, endNode: V, value: W) -> None:
        if startNode is None or endNode is None: raise Exception("input None node")
        if value is None: raise Exception("input None value")
        if startNode not in self.__map: self.addNewNode(startNode)
        if endNode not in self.__map: self.addNewNode(endNode)
        isNewPath: bool = self.__map[startNode][endNode] is None

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

    def getPath(self, startNode: V, endNode: V) -> Optional[W]:
        if startNode is None or endNode is None: raise Exception("input None node")
        if startNode not in self.__map: raise Exception("cannot found start node in map")
        if endNode not in self.__map[startNode]: raise Exception("cannot found end node in map")
        return self.__map[startNode][endNode]

    def deletePath(self, startNode: V, endNode: V) -> None:
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

    def allSuccessors(self, v: V) -> Generator[Tuple[V, Optional[W]], None, None]:
        if v is None: raise Exception("input None vertex")
        if v not in self.__map: raise Exception(f"input vertex not in graph ({v})")
        adj: Dict[V, Optional[W]] = self.__map[v]
        for k in adj.keys():
            if adj[k] is not None: yield (k, adj[k])

    def allInorderedSuccessors(self, v: V) -> Generator[Tuple[V, Optional[W]], None, None]:
        if v is None: raise Exception("input None vertex")
        if v not in self.__map: raise Exception(f"input vertex not in graph ({v})")
        adj: Dict[V, Optional[W]] = self.__map[v]
        for k in sorted(adj.keys()):
            if adj[k] is not None: yield (k, adj[k])

    def allPredecessors(self, v: V) -> Generator[Tuple[V, Optional[W]], None, None]:
        if v is None: raise Exception("input None vertex")
        if v not in self.__map: raise Exception("input vertex not in graph")
        keys: List[V] = self.vertexSet()
        for k in keys:
            if self.__map[k][v] is not None: yield (k, self.__map[k][v])

    def allInorderedPredecessors(self, v: V) -> Generator[Tuple[V, Optional[W]], None, None]:
        if v is None: raise Exception("input None vertex")
        if v not in self.__map: raise Exception("input vertex not in graph")
        keys: List[V] = self.vertexSet()
        for k in sorted(keys):
            if self.__map[k][v] is not None: yield (k, self.__map[k][v])

    def vertexSet(self) -> List[V]:
        return list(self.__map.keys())

    def allVertexes(self) -> Generator[V, None, None]:
        for k in self.__map.keys(): yield k

    def allInorderedVertexes(self) -> Generator[V, None, None]:
        for k in sorted(self.__map.keys()): yield k

    def checkVertexExist(self, v: V) -> bool:
        if v is None: raise Exception("input None vertex")
        return v in self.__map

    def zeroInDegreeVertexes(self) -> Generator[V, None, None]:
        for v in self.__inDegreeMap.keys():
            if self.__inDegreeMap[v] == 0: yield v

    def zeroOutDegreeVertexes(self) -> Generator[V, None, None]:
        for v in self.__outDegreeMap.keys():
            if self.__outDegreeMap[v] == 0: yield v

    def isDigraph(self) -> bool:
        return self.__digraph

    def allEdges(self) -> Generator[Tuple[V, V, Optional[W]], None, None]:
        for s, e in self.__edgesSet:
            yield (s, e, self.__map[s][e])

    def __str__(self) -> str:
        if not self.__map: raise Exception('Map is empty')
        keys: List[V] = sorted(self.__map.keys())
        result: str = "vertices: " + str(keys) + '\n' + "Matrix: " + '\n'
        for kstart in keys:
            for kend in keys:
                result += "{:<10}".format(str(self.__map[kstart][kend])) + ' '
            result += '\n'
        return result
