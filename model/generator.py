import numpy as np
from typing import (
    Any,
    TypeVar,
    Generator,
    Hashable,
    Dict,
    Tuple,
    Optional,
)

np.random.seed(0)


class GenerateRandomProbability:
    def __init__(self, generator: str = "uniform", ranges: Tuple[int, int] = (0, 1)) -> None:
        self.__generatorType: str                                   = generator
        self.__nSamples: int                                        = 0
        self.__cdfDistribution: Optional[Dict[Hashable, float]]     = None
        self.__ranges: Tuple[int, int]                              = ranges

    def fit(self, distribution: Dict[Hashable, float], nSamples: int = 1) -> None:
        if not isinstance(distribution, dict):
            raise Exception(
                "Don't support distribution type: {}".format(type(distribution))
            )
        sumProb: float = sum(distribution.values())
        if sumProb > 1.0 + 1e-4 or sumProb < 1.0 - 1e-4:
            raise Exception("Incorrect distribution")

        self.__nSamples = nSamples
        self.__cumulativeDistributionFunction(distribution)

    def __cumulativeDistributionFunction(self, distribution: Dict[Hashable, float]) -> None:
        self.__cdfDistribution = distribution
        sumProb: float = 0
        for key, prob in self.__cdfDistribution.items():
            self.__cdfDistribution[key] = prob + sumProb
            sumProb += prob

    def oneSample(self) -> Hashable:
        if self.__cdfDistribution is None:
            raise Exception("Please use the fit method before generating")
        rnd: float = np.random.uniform(self.__ranges[0], self.__ranges[1], 1)[0]
        for feature, pro in self.__cdfDistribution.items():
            if rnd <= pro:
                return feature
        raise Exception("Cannot acquire any return value with random number: {}".format(rnd))

    def generate(self) -> Generator[Hashable, None, None]:
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
        output: str = "Generator type: {}\nNumber of samples: {}\nRanges: {}\ncdf: {}".format(
            self.__generatorType, self.__nSamples, self.__ranges, self.__cdfDistribution
        )
        return output
