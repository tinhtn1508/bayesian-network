import os
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
