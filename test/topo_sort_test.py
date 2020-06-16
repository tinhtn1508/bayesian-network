import unittest
from graph import TopoSortAlgorithm, UnweightedDirectionAdjacencyMatrix


class TopoSortTest(unittest.TestCase):
    def setUp(self) -> None:
        adj: UnweightedDirectionAdjacencyMatrix = UnweightedDirectionAdjacencyMatrix(
            verticesList=["a", "b", "c", "d", "e", "f"]
        )
        adj.addPath("a", "b")
        adj.addPath("a", "c")
        adj.addPath("b", "d")
        adj.addPath("b", "e")
        adj.addPath("d", "f")
        self.__adj = adj
        self.__topo = TopoSortAlgorithm(adj)

    def testVertexNone(self):
        with self.assertRaises(Exception):
            _ = [v for v in self.__topo.dfsFromVertex(None)]
        with self.assertRaises(Exception):
            _ = [v for v in self.__topo.bfsFromVertex(None)]

    def testVertexNotExistInGraph(self):
        with self.assertRaises(Exception):
            _ = [v for v in self.__topo.dfsFromVertex("None")]
        with self.assertRaises(Exception):
            _ = [v for v in self.__topo.bfsFromVertex("None")]

    def testTopoSortFromB(self):
        expected = ["b", "e", "d", "f"]
        actual = [v for v in self.__topo.dfsFromVertex("b")]
        self.assertEqual(expected, actual)
        expected = ["b", "d", "e", "f"]
        actual = [v for v in self.__topo.bfsFromVertex("b")]
        self.assertEqual(expected, actual)

    def testTopoSortFromF(self):
        expected = ["f"]
        actual = [v for v in self.__topo.dfsFromVertex("f")]
        self.assertEqual(expected, actual)
        actual = [v for v in self.__topo.bfsFromVertex("f")]
        self.assertEqual(expected, actual)

    def testTopoSortAll(self):
        actual = [v for v in self.__topo.dfs()]
        expected = ["a", "c", "b", "e", "d", "f"]
        self.assertEqual(expected, actual)
        actual = [v for v in self.__topo.bfs()]
        expected = ["a", "b", "c", "d", "e", "f"]
        self.assertEqual(expected, actual)


def TopoSortTestSuite() -> unittest.TestSuite:
    suite = unittest.TestSuite()
    suite.addTest(TopoSortTest("testVertexNone"))
    suite.addTest(TopoSortTest("testVertexNotExistInGraph"))
    suite.addTest(TopoSortTest("testTopoSortFromB"))
    suite.addTest(TopoSortTest("testTopoSortFromF"))
    suite.addTest(TopoSortTest("testTopoSortAll"))
    return suite
