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


class TestParser(TxtParser):
    def __init__(self, filePath: str) -> None:
        super().__init__(filePath)
        self.__numOfQueries: int = 0
        self.__queriesTable: List = list()

    def parse(self) -> None:
        lines = self.readLines()
        self.__numOfQueries = int(lines[0])
        if self.__numOfQueries < 1 or self.__numOfQueries > 999:
            raise Exception(
                "Don't support number of query: {}".format(self.__numOfQueries)
            )
        if self.__numOfQueries != len(lines[1:]):
            raise Exception(
                "__numOfQueries: {} != len(line): {}".format(
                    self.__numOfQueries, len(lines[1:])
                )
            )
        for line in lines[1:]:
            format = line.split(";")
            inferFormat = format[0]
            infer = self.__parse(inferFormat)

            if len(format) == 1:
                self.__queriesTable.append((infer, None))
            else:
                proof = self.__parse(format[1])
                self.__queriesTable.append((infer, proof))

    def __parse(self, lineFormat):
        format = lineFormat.split(",")
        output = dict()
        for c in format:
            featureFormat = c.split("=")
            output[featureFormat[0]] = featureFormat[1]
        return output

    def getQueriesTable(self):
        return self.__queriesTable
