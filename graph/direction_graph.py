from . import AdjacencyMatrix

class UnweightedDirectionAdjacencyMatrix(AdjacencyMatrix):
    def __init__(self, verticesList = None):
        super().__init__(verticesList, True)

    def addPath(self, startNode, endNode):
        super().addPath(startNode, endNode, 1)

class WeightedDirectionAdjacencyMatrix(AdjacencyMatrix):
    def __init__(self, verticesList = None):
        super().__init__(verticesList, True)

    def addPath(self, startNode, endNode, value):
        super().addPath(startNode, endNode, value)
