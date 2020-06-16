from graph import UnweightedDirectionAdjacencyMatrix, TopoSortAlgorithm
from .nodes import Node
from .generator import GenerateRandomProbability


class BayesianNetwork(UnweightedDirectionAdjacencyMatrix):
    def __init__(self):
        super().__init__(None)
        self.__generator = GenerateRandomProbability()

    def forward(self):
        # TODO
        pass

    def likelihood(self):
        # TODO
        pass
