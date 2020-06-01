from . import AdjacencyMatrix

class UnweightedIndirectionAdjacencyMatrix(AdjacencyMatrix):
    def __init__(self, verticesList = None):
        super().__init__(verticesList, False)

    def addPath(self, startNode, endNode):
        super().addPath(startNode, endNode, 1)

class WeightedIndirectionAdjacencyMatrix(AdjacencyMatrix):
    def __init__(self, verticesList = None):
        super().__init__(verticesList, False)

    def addPath(self, startNode, endNode, value):
        super().addPath(startNode, endNode, value)