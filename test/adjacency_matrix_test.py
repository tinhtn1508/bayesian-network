import unittest
from graph import AdjacencyMatrix
from typing import Any, Optional, List


class AdjacencyMatrixTest(unittest.TestCase):
    def setUp(self) -> None:
        adj: AdjacencyMatrix = AdjacencyMatrix(
            verticesList=[
                "a",
                "b",
                "c",
                "d",
                "e",
                "f",
                "g",
                "h",
                "i",
                "j",
                "k",
                "l",
                "x",
                "y",
                "z",
            ],
            digraph=True,
        )
        adj.addPath("a", "b", 1)
        adj.addPath("a", "c", 1)
        adj.addPath("b", "d", 1)
        adj.addPath("b", "e", 1)
        adj.addPath("d", "f", 1)
        adj.addPath("e", "g", 1)
        adj.addPath("e", "h", 1)
        adj.addPath("g", "i", 1)
        adj.addPath("g", "j", 1)
        adj.addPath("h", "k", 1)
        adj.addPath("i", "l", 1)
        adj.addPath("j", "l", 1)
        adj.addPath("y", "z", 1)
        adj.addPath("y", "x", 1)
        self.__adj = adj

    def testAddNode1(self) -> None:
        self.__adj.addNewNode("m")
        self.assertIn("m", self.__adj.vertexSet())

    def testAddNode2(self) -> None:
        with self.assertRaises(Exception):
            self.__adj.addNewNode(None)

    def testAddPath1(self) -> None:
        with self.assertRaises(Exception):
            self.__adj.addPath(None, "a", 1)

    def testAddPath2(self) -> None:
        with self.assertRaises(Exception):
            self.__adj.addPath("b", None, 1)

    def testAddPath3(self) -> None:
        with self.assertRaises(Exception):
            self.__adj.addPath("b", "k", None)

    def testAddPath4(self) -> None:
        self.__adj.addPath("m", "n", 1)
        self.assertTrue("m" in self.__adj.vertexSet())
        self.assertTrue("n" in self.__adj.vertexSet())
        pathweight: Optional[Any] = self.__adj.getPath("m", "n")
        self.assertTrue(pathweight is not None and pathweight == 1)

    def testAddPath5(self) -> None:
        self.__adj.addPath("a", "b", 3.5)
        self.assertTrue("a" in self.__adj.vertexSet())
        self.assertTrue("b" in self.__adj.vertexSet())
        pathweight: Optional[Any] = self.__adj.getPath("a", "b")
        self.assertTrue(pathweight is not None and pathweight == 3.5)

    def testGetPath1(self) -> None:
        self.__adj.getPath("a", "b")
        self.assertTrue("a" in self.__adj.vertexSet())
        self.assertTrue("b" in self.__adj.vertexSet())
        pathweight: Optional[Any] = self.__adj.getPath("a", "b")
        self.assertTrue(pathweight is not None and pathweight == 1)

    def testGetPath2(self) -> None:
        with self.assertRaises(Exception):
            self.__adj.getPath(None, "b")

    def testGetPath3(self) -> None:
        with self.assertRaises(Exception):
            self.__adj.getPath("a", None)

    def testGetPath4(self) -> None:
        with self.assertRaises(Exception):
            self.__adj.getPath("r", "a")

    def testGetPath5(self) -> None:
        with self.assertRaises(Exception):
            self.__adj.getPath("a", "s")

    def testGetPath6(self) -> None:
        self.assertIsNone(self.__adj.getPath("a", "f"))

    def testDeletePath1(self) -> None:
        self.assertIsNotNone(self.__adj.getPath("a", "b"))
        self.__adj.deletePath("a", "b")
        self.assertIsNone(self.__adj.getPath("a", "b"))

    def testDeletePath2(self) -> None:
        with self.assertRaises(Exception):
            self.__adj.deletePath("a", None)

    def testDeletePath3(self) -> None:
        with self.assertRaises(Exception):
            self.__adj.deletePath(None, "b")

    def testDeletePath4(self) -> None:
        with self.assertRaises(Exception):
            self.__adj.deletePath("s", "b")

    def testDeletePath5(self) -> None:
        with self.assertRaises(Exception):
            self.__adj.deletePath("b", "r")

    def testAllSuccessors1(self) -> None:
        expectedresult: List[str] = ["b", "c"]
        result = list(self.__adj.allSuccessors("a"))
        for v, _ in result:
            self.assertIn(v, expectedresult)
        self.assertEqual(len(result), len(expectedresult))

    def testAllSuccessors2(self) -> None:
        with self.assertRaises(Exception):
            list(self.__adj.allSuccessors(None))

    def testAllSuccessors3(self) -> None:
        with self.assertRaises(Exception):
            list(self.__adj.allSuccessors("r"))

    def testAllInorderedSuccessors1(self) -> None:
        expectedresult: List[str] = ["d", "e"]
        result: List[str] = list(self.__adj.allInorderedSuccessors("b"))
        self.assertEqual(len(expectedresult), len(result))
        for i in range(len(result)):
            self.assertEqual(expectedresult[i], result[i][0])

    def testAllInorderedSuccessors2(self) -> None:
        with self.assertRaises(Exception):
            list(self.__adj.allInorderedSuccessors(None))

    def testAllInorderedSuccessors3(self) -> None:
        with self.assertRaises(Exception):
            list(self.__adj.allInorderedSuccessors("r"))

    def testAllPredecessors1(self) -> None:
        expectedresult: List[str] = ["a"]
        result = list(self.__adj.allPredecessors("b"))
        for v, _ in result:
            self.assertIn(v, expectedresult)
        self.assertEqual(len(result), len(expectedresult))

    def testAllPredecessors2(self) -> None:
        with self.assertRaises(Exception):
            list(self.__adj.allPredecessors(None))

    def testAllPredecessors3(self) -> None:
        with self.assertRaises(Exception):
            list(self.__adj.allPredecessors("r"))

    def testAllInorderedPredecessors1(self) -> None:
        expectedresult: List[str] = ["i", "j"]
        result: List[str] = list(self.__adj.allInorderedPredecessors("l"))
        self.assertEqual(len(expectedresult), len(result))
        for i in range(len(result)):
            self.assertEqual(expectedresult[i], result[i][0])

    def testAllInorderedPredecessors2(self) -> None:
        with self.assertRaises(Exception):
            list(self.__adj.allInorderedPredecessors(None))

    def testAllInorderedPredecessors3(self) -> None:
        with self.assertRaises(Exception):
            list(self.__adj.allInorderedPredecessors("r"))

    def testCheckVertexExist(self) -> None:
        with self.assertRaises(Exception):
            self.__adj.checkVertexExist(None)
        self.assertTrue(self.__adj.checkVertexExist("a"))
        self.assertFalse(self.__adj.checkVertexExist("r"))

    def testZeroInDegreeVertexes(self) -> None:
        expectedresult = ["a", "y"]
        result = list(self.__adj.zeroInDegreeVertexes())
        for v in result:
            self.assertIn(v, expectedresult)
        self.assertEqual(len(expectedresult), len(result))

    def testZeroOutDegreeVertexes(self) -> None:
        expectedresult = ["c", "f", "k", "l", "z", "x"]
        result = list(self.__adj.zeroOutDegreeVertexes())
        for v in result:
            self.assertIn(v, expectedresult)
        self.assertEqual(len(expectedresult), len(result))

    def testAllEdges(self):
        result = list(self.__adj.allEdges())
        self.assertEqual(len(result), 14)


def AdjacencyMatrixTestSuite() -> unittest.TestSuite:
    suite = unittest.TestSuite()
    suite.addTest(AdjacencyMatrixTest("testAddNode1"))
    suite.addTest(AdjacencyMatrixTest("testAddNode2"))
    suite.addTest(AdjacencyMatrixTest("testAddPath1"))
    suite.addTest(AdjacencyMatrixTest("testAddPath2"))
    suite.addTest(AdjacencyMatrixTest("testAddPath3"))
    suite.addTest(AdjacencyMatrixTest("testAddPath4"))
    suite.addTest(AdjacencyMatrixTest("testAddPath5"))
    suite.addTest(AdjacencyMatrixTest("testGetPath1"))
    suite.addTest(AdjacencyMatrixTest("testGetPath2"))
    suite.addTest(AdjacencyMatrixTest("testGetPath3"))
    suite.addTest(AdjacencyMatrixTest("testGetPath4"))
    suite.addTest(AdjacencyMatrixTest("testGetPath5"))
    suite.addTest(AdjacencyMatrixTest("testGetPath6"))
    suite.addTest(AdjacencyMatrixTest("testDeletePath1"))
    suite.addTest(AdjacencyMatrixTest("testDeletePath2"))
    suite.addTest(AdjacencyMatrixTest("testDeletePath3"))
    suite.addTest(AdjacencyMatrixTest("testDeletePath4"))
    suite.addTest(AdjacencyMatrixTest("testDeletePath5"))
    suite.addTest(AdjacencyMatrixTest("testAllSuccessors1"))
    suite.addTest(AdjacencyMatrixTest("testAllSuccessors2"))
    suite.addTest(AdjacencyMatrixTest("testAllSuccessors3"))
    suite.addTest(AdjacencyMatrixTest("testAllInorderedSuccessors1"))
    suite.addTest(AdjacencyMatrixTest("testAllInorderedSuccessors2"))
    suite.addTest(AdjacencyMatrixTest("testAllInorderedSuccessors3"))
    suite.addTest(AdjacencyMatrixTest("testAllPredecessors1"))
    suite.addTest(AdjacencyMatrixTest("testAllPredecessors2"))
    suite.addTest(AdjacencyMatrixTest("testAllPredecessors3"))
    suite.addTest(AdjacencyMatrixTest("testAllInorderedPredecessors1"))
    suite.addTest(AdjacencyMatrixTest("testAllInorderedPredecessors2"))
    suite.addTest(AdjacencyMatrixTest("testAllInorderedPredecessors3"))
    suite.addTest(AdjacencyMatrixTest("testCheckVertexExist"))
    suite.addTest(AdjacencyMatrixTest("testZeroInDegreeVertexes"))
    suite.addTest(AdjacencyMatrixTest("testZeroOutDegreeVertexes"))
    suite.addTest(AdjacencyMatrixTest("testAllEdges"))
    return suite
