from . import AdjacencyMatrix


def reverseGraph(adjMatrix):
    if adjMatrix is None:
        raise Exception("Invalid input")

    rMatrix = AdjacencyMatrix(digraph=adjMatrix.isDigraph())
    for s, e, w in adjMatrix.allEdges():
        rMatrix.addPath(e, s, w)
    return rMatrix
