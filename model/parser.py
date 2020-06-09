import json
from typing import Dict, Optional, Generic, Generator, TypeVar, List, Set, Tuple, Hashable, Any, Union

MODEL_NAME = "BayesianModel"
CONNECTION = "Connections"
FEATURE = "Features"

class Parser():
    def __init__(self):
        self.root = dict()
        self.nameNodes = list()

    def load(self, filename: str) -> dict:
        if filename is None:
            raise Exception("filename is None")
        try:
            with open(filename, 'r') as f:
                self.root = json.load(f)
                self.__checkStyle();
                self.nameNodes = self.getNameNodes()
        except Exception as e:
            raise e

    def __checkStyle(self) -> None:
        for key in self.root.keys():
            if key != MODEL_NAME:
                raise Exception("Incorrect root keys: {}".format(key))

    def checkValues(self) -> None:
        pass

    def __checkValue(self, fromNode: str) -> None:
        pass

    def checkConnections(self) -> None:
        for nameNode in self.nameNodes:
            self.__checkConnection(nameNode)

    def __checkConnection(self, fromNode) -> None:
        connectToNode: List[str] = self.getConnections(fromNode)
        if connectToNode is None:
            return
        for connect in connectToNode:
            if connect not in self.nameNodes:
                raise Exception("Connection not exist: {}".format(connect))

    def getNameNodes(self) -> List[str]:
        return list(self.root[MODEL_NAME].keys())

    def getConnections(self, fromNode: str) -> List[str]:
        return self.root[MODEL_NAME][fromNode][CONNECTION]

    def getFeatures(self, fromNode) -> List[str]:
        return list(self.root[MODEL_NAME][fromNode][FEATURE].keys())

    def getValues(self, fromNode) -> Hashable:
        return self.root[MODEL_NAME][fromNode][FEATURE]

# parser = Parser()
# parser.load("model_tmp.json")
# print(parser.root["BayesianModel"]["Grade"]["Features"])
# print(parser.checkConnections())
# print(parser.getConnections("Grade"))
# print(parser.getFeatures("Grade"))
# print(parser.getValues("Grade"))
