import test
import unittest

def main():
    print("Running unit test for Adjacency matrix class")
    runner = unittest.TextTestRunner()
    runner.run(test.AdjacencyMatrixTestSuite())

if __name__ == "__main__":
    main()
