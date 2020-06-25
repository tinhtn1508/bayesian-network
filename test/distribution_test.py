import unittest
import numpy as np
from model import ConditionalProbability, DiscreteDistribution


class DistributionTest(unittest.TestCase):
    def testConditionalProbabilityIncorrect(self) -> None:
        with self.assertRaises(Exception):
            _ = ConditionalProbability(
                "S", [0.95, 0.05, 0.2, 0.8], (2, 3), ["Low", "High"], ["I"]
            )

        with self.assertRaises(Exception):
            _ = ConditionalProbability(
                "S", [0.95, 0.05, 0.2, 0.9], (2, 2), ["Low", "High"], ["I"]
            )

    def testDiscreteDistributionIncorrect(self) -> None:
        with self.assertRaises(Exception):
            _ = DiscreteDistribution("D", [0.6, 0.4], (3, 2), ["Easy", "Hard"])

        with self.assertRaises(Exception):
            _ = DiscreteDistribution("D", [0.6, 0.9], (1, 2), ["Easy", "Hard"])

    def testDiscreteDistributionGet(self) -> None:
        P = DiscreteDistribution("D", [0.6, 0.4], (1, 2), ["Easy", "Hard"])
        actual = P.getDistribution()
        expected = {"Easy": 0.6, "Hard": 0.4}
        self.assertEqual(actual, expected)

    def testConditionalProbabilityGet(self) -> None:
        PL = ConditionalProbability(
            "L", [0.1, 0.9, 0.4, 0.6, 0.99, 0.01], (3, 2), ["Weak", "Strong"], ["G"]
        )
        PL.setConditionalFeatures({"G": ["A", "B", "C"]})

        actual = PL.getDistribution({"G": "A"})
        expected = {"Weak": 0.1, "Strong": 0.9}
        self.assertEqual(actual, expected)
        actual = PL.getDistribution({"G": "B"})
        expected = {"Weak": 0.4, "Strong": 0.6}
        self.assertEqual(actual, expected)
        actual = PL.getDistribution({"G": "C"})
        expected = {"Weak": 0.99, "Strong": 0.01}
        self.assertEqual(actual, expected)


def DistributionTestSuite() -> unittest.TestSuite:
    suite = unittest.TestSuite()
    suite.addTest(DistributionTest("testConditionalProbabilityIncorrect"))
    suite.addTest(DistributionTest("testDiscreteDistributionIncorrect"))
    suite.addTest(DistributionTest("testDiscreteDistributionGet"))
    suite.addTest(DistributionTest("testConditionalProbabilityGet"))
    return suite
