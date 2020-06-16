from . import AdjacencyMatrix
from common import Stack, Queue
from typing_extensions import Protocol
from typing import (
    Dict,
    Optional,
    Generic,
    Generator,
    TypeVar,
    List,
    Set,
    Tuple,
    Hashable,
    Any,
    Union,
)

C = TypeVar("C", bound="Comparable")


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


V = TypeVar("V", bound=Union[Hashable, Comparable])


class TopoSortAlgorithm:
    def __init__(self, adjacencyMatrix: AdjacencyMatrix):
        if not adjacencyMatrix:
            raise Exception("Invalid input param")
        self.__adjacencyMatrix = adjacencyMatrix

    def __dfsFromVertex(self, vertex: V, visited: Set[V], stack: Stack) -> None:
        if vertex is None or visited is None or stack is None:
            raise Exception(
                "Invalid input: vertex: {}, visited: {}, stack: {}".format(
                    vertex, visited, stack
                )
            )
        for neighbor, _ in self.__adjacencyMatrix.allSuccessors(vertex):
            if neighbor in visited:
                continue
            visited.add(neighbor)
            self.__dfsFromVertex(neighbor, visited, stack)
        stack.push(vertex)

    def dfsFromVertex(
        self, vertex: V, visited: Set[V] = None
    ) -> Generator[V, None, None]:
        if vertex is None:
            raise Exception("Vertex is None")
        if self.__adjacencyMatrix.checkVertexExist(vertex) is None:
            raise Exception("Node not exist in graph")
        if visited is None:
            visited = set()
        stack: Stack = Stack()
        visited.add(vertex)
        self.__dfsFromVertex(vertex, visited, stack)
        while len(stack) > 0:
            v, _ = stack.pop()
            yield v

    def dfs(self) -> Generator[V, None, None]:
        visited = set()
        stack: Stack = Stack()
        if self.__adjacencyMatrix.isDigraph():
            for vertex in self.__adjacencyMatrix.zeroInDegreeVertexes():
                if vertex in visited:
                    continue
                self.__dfsFromVertex(vertex, visited, stack)
                while(len(stack) > 0):
                    v, _ = stack.pop()
                    yield v
        else:
            raise Exception("This is not a Digraph")

    def __bfsImpl(self, visited: Set[V], queue: Queue):
        while len(queue) > 0:
            v, _ = queue.dequeue()
            for neighbor, _ in self.__adjacencyMatrix.allSuccessors(v):
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                queue.enqueue(neighbor)
            yield v

    def bfsFromVertex(
        self, vertex: V, visited: Set[V] = None
    ) -> Generator[V, None, None]:
        if vertex is None:
            raise Exception("Vertex is None")
        if self.__adjacencyMatrix.checkVertexExist(vertex) is None:
            raise Exception("Vertex: {} not exist in graph".format(vertex))
        if visited is None:
            visited = set()
        queue: Queue = Queue()
        queue.enqueue(vertex)
        visited.add(vertex)
        for v in self.__bfsImpl(visited, queue):
            yield v

    def bfs(self) -> Generator[V, None, None]:
        visited = set()
        queue: Queue = Queue()
        if self.__adjacencyMatrix.isDigraph():
            for v in self.__adjacencyMatrix.zeroInDegreeVertexes():
                visited.add(v)
                queue.enqueue(v)
            for v in self.__bfsImpl(visited, queue):
                yield v
        else:
            raise Exception("This is not a Digraph")
