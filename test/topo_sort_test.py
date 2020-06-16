import unittest
from graph import TopoSortAlgorithm, UnweightedDirectionAdjacencyMatrix


class TopoSortTest1(unittest.TestCase):
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


class TopoSortTest2(unittest.TestCase):
    def setUp(self) -> None:
        adj: UnweightedDirectionAdjacencyMatrix = UnweightedDirectionAdjacencyMatrix(
            verticesList=["D", "I", "G", "S", "L"]
        )
        adj.addPath("D", "G")
        adj.addPath("G", "L")
        adj.addPath("I", "G")
        adj.addPath("I", "S")
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

    def testTopoSortFromD(self):
        expected = ["D", "G", "L"]
        actual = [v for v in self.__topo.dfsFromVertex("D")]
        self.assertEqual(expected, actual)
        actual = [v for v in self.__topo.bfsFromVertex("D")]
        self.assertEqual(expected, actual)

    def testTopoSortFromI(self):
        expected = ["I", "S", "G", "L"]
        actual = [v for v in self.__topo.dfsFromVertex("I")]
        self.assertEqual(expected, actual)
        expected = ["I", "G", "S", "L"]
        actual = [v for v in self.__topo.bfsFromVertex("I")]
        self.assertEqual(expected, actual)

    def testTopoSortAll(self):
        actual = [v for v in self.__topo.dfs()]
        expected = ["D", "G", "L", "I", "S"]
        self.assertEqual(expected, actual)
        actual = [v for v in self.__topo.bfs()]
        expected = ["D", "I", "G", "S", "L"]
        self.assertEqual(expected, actual)



def TopoSortTestSuite() -> unittest.TestSuite:
    suite = unittest.TestSuite()
    suite.addTest(TopoSortTest1("testVertexNone"))
    suite.addTest(TopoSortTest1("testVertexNotExistInGraph"))
    suite.addTest(TopoSortTest1("testTopoSortFromB"))
    suite.addTest(TopoSortTest1("testTopoSortFromF"))
    suite.addTest(TopoSortTest1("testTopoSortAll"))

    suite.addTest(TopoSortTest2("testVertexNone"))
    suite.addTest(TopoSortTest2("testVertexNotExistInGraph"))
    suite.addTest(TopoSortTest2("testTopoSortFromD"))
    suite.addTest(TopoSortTest2("testTopoSortFromI"))
    suite.addTest(TopoSortTest2("testTopoSortAll"))
    return suite
