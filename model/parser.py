import os
from .nodes import Node
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


class TxtParser:
    def __init__(self, filePath: str):
        self.__filePath = filePath

    def readLine(self) -> Generator[str, None, None]:
        with open(self.__filePath, "r") as fp:
            for line in fp:
                yield line.strip("\n")

    def readLines(self) -> List:
        return list(self.readLine())

    def writeLine(self, buffer: str):
        with open(self.__filePath, "a") as fp:
            fp.writelines(buffer + "\n")

    def writeLines(self, buffers: List[str]):
        if os.path.exists(self.__filePath):
            print(
                "WARNING: {} is exists and the method will replace this file".format(
                    self.__filePath
                )
            )
        with open(self.__filePath, "w") as fp:
            for buff in buffers:
                fp.writelines(buff + "\n")

    def __str__(self):
        info = os.stat(self.__filePath)
        return "{}".format(info)


class ModelParser(TxtParser):
    def __init__(self, filePath: str) -> None:
        super().__init__(filePath)
        self.__numOfNodes: int = 0
        self.__nodes: Dict[str, Node] = dict()

    def getNumberOfNodes(self) -> int:
        return self.__numOfNodes

    def parse(self) -> None:
        lines = self.readLines()
        self.__numOfNodes = int(lines[0])
        if self.__numOfNodes < 2 or self.__numOfNodes > 999:
            raise Exception(
                "Don't support number of nodes: {}".format(self.__numOfNodes)
            )
        if self.__numOfNodes != len(lines[1:]):
            raise Exception(
                "numofnode: {} != len(line): {}".format(
                    self.__numOfNodes, len(lines[1:])
                )
            )
        for line in lines[1:]:
            node: Node = Node.fromTxt(line)
            self.__nodes[node.name] = node

    def getNodes(self) -> Dict[str, Node]:
        return self.__nodes
