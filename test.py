import test
import unittest


def main():
    runner = unittest.TextTestRunner()

    print("Running unit test for Adjacency matrix class")
    runner.run(test.AdjacencyMatrixTestSuite())

    print("Running unit test for Stack class")
    runner.run(test.StackTestSuite())

    print("Running unit test for Queue class")
    runner.run(test.QueueTestSuite())

    print("Running unit test for Topo Sort Algorithm")
    runner.run(test.TopoSortTestSuite())

    print("Running unit test for Generator")
    runner.run(test.GeneratorTestSuite())


if __name__ == "__main__":
    main()
