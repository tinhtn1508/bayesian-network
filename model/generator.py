import numpy as np
from typing import Any, TypeVar, Generator


class GenerateRandomProbability:
    def __init__(self, generator: str = "uniform", ranges: tuple = (0, 1)):
        self.__generatorType = generator
        self.__nSamples = 0
        self.__cdfDistribution = None
        self.__ranges = ranges

    def fit(self, distribution: map, nSamples: int = 1) -> None:
        if not isinstance(distribution, dict):
            raise Exception(
                "Don't support distribution type: {}".format(type(distribution))
            )
        if sum(distribution.values()) != 1.0:
            raise Exception("Incorrect distribution")

        self.__nSamples = nSamples
        self.__cumulativeDistributionFunction(distribution)

    def __cumulativeDistributionFunction(self, distribution: map):
        self.__cdfDistribution = dict(sorted(distribution.items(), key=lambda x: x[1]))
        sumProb = 0
        for key, prob in self.__cdfDistribution.items():
            self.__cdfDistribution[key] = prob + sumProb
            sumProb += prob

    def generate(self) -> Generator:
        if self.__cdfDistribution is None:
            raise Exception("Please use the fit method before generating")
        for sample_pro in self.__samples():
            for feature, pro in self.__cdfDistribution.items():
                if sample_pro <= pro:
                    yield feature
                    break

    def __samples(self) -> np.array:
        if self.__generatorType == "uniform":
            return np.random.uniform(
                self.__ranges[0], self.__ranges[1], self.__nSamples
            )
        else:
            raise Exception(
                "Do not support generator type: {}".format(self.__generatorType)
            )

    def __str__(self):
        output = "Generator type: {}\nNumber of samples: {}\nRanges: {}\ncdf: {}".format(
            self.__generatorType, self.__nSamples, self.__ranges, self.__cdfDistribution
        )
        return output
