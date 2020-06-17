import unittest
import numpy as np
from model import GenerateRandomProbability


class GenerateRandomProbabilityTest(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def testGenerate1(self) -> None:
        radom = GenerateRandomProbability()
        distribution = {"A1": 0.3, "A2": 0.7}
        radom.fit(distribution)
        res = list(radom.generate())
        self.assertTrue(res[0] in distribution.keys())
        N: int = 100000
        res = []
        for _ in range(N):
            res.append(list(radom.generate())[0])
        resNumpy = np.array(res)
        isA1 = resNumpy == "A1"
        numOfA1 = resNumpy[isA1]
        delta = 0.3 - len(numOfA1) / N
        self.assertTrue(abs(delta) < 1e-2)

    def testGenerate2(self) -> None:
        radom = GenerateRandomProbability()
        distribution = {"wqQWD": 0.05, "fsfs": 0.15, "gthttrh": 0.17, "gwrwer": 0.13, "gvsds": 0.3, "wetwf": 0.2}
        radom.fit(distribution)
        res = list(radom.generate())
        self.assertTrue(res[0] in distribution.keys())
        N: int = 100000
        res = []
        for _ in range(N):
            res.append(list(radom.generate())[0])
        resNumpy = np.array(res)
        isA1 = resNumpy == "gthttrh"
        numOfA1 = resNumpy[isA1]
        delta = 0.17 - len(numOfA1) / N
        self.assertTrue(abs(delta) < 1e-2)

    def testGenerateAbnormal(self) -> None:
        radom = GenerateRandomProbability()
        with self.assertRaises(Exception):
            list(radom.generate())

    def testGenerateIncorrectDistribution1(self) -> None:
        radom = GenerateRandomProbability()
        distribution = [0.1, 0.9]
        with self.assertRaises(Exception):
            radom.fit()

    def testGenerateIncorrectDistribution2(self) -> None:
        radom = GenerateRandomProbability()
        distribution = {"A1": 0.3, "A2": 0.8}
        with self.assertRaises(Exception):
            radom.fit()

    def testGenerateIncorrectGenerator(self) -> None:
        radom = GenerateRandomProbability("normal")
        distribution = {"A1": 0.3, "A2": 0.7}
        with self.assertRaises(Exception):
            radom.fit()
            list(radom.generate())


def GeneratorTestSuite() -> unittest.TestSuite:
    suite = unittest.TestSuite()
    suite.addTest(GenerateRandomProbabilityTest("testGenerate1"))
    suite.addTest(GenerateRandomProbabilityTest("testGenerate2"))
    suite.addTest(GenerateRandomProbabilityTest("testGenerateAbnormal"))
    suite.addTest(GenerateRandomProbabilityTest("testGenerateIncorrectDistribution1"))
    suite.addTest(GenerateRandomProbabilityTest("testGenerateIncorrectDistribution2"))
    suite.addTest(GenerateRandomProbabilityTest("testGenerateIncorrectGenerator"))
    return suite
