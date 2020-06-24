import numpy as np
from functools import reduce, lru_cache
from common import cacheDict
from .generator import generateOneSample
from typing import (
    Dict,
    Optional,
    Generic,
    Generator,
    TypeVar,
    List,
    Set,
    Tuple,
    Hashable,
    Any,
    Union,
)


def totuple(a):
    try:
        return tuple(totuple(i) for i in a)
    except TypeError:
        return a


class Probability:
    def __init__(
        self,
        name: str,
        table: List[float],
        shape: Tuple[int],
        features: List[str],
        conditions: Optional[List[str]],
    ):
        self._name: str = name
        self._features: Dict[str, int] = {
            val: index for index, val in enumerate(features)
        }
        self._featuresArray: List[str] = features
        if len(table) != reduce((lambda x, y: x * y), shape):
            raise Exception(
                "Don't match between length of table and shape, length: {}, shape: {}".format(
                    len(table), shape
                )
            )
        self._table: np.array = np.array(table).reshape(shape)
        self._cdfTable = np.cumsum(self._table, axis=len(self._table.shape) - 1)
        sumProb: np.array = np.sum(self._table, axis=len(self._table.shape) - 1)
        if sumProb.mean() != 1.0:
            raise Exception("Incorrect probability")

    @property
    def features(self) -> List[str]:
        return list(self._featuresArray)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def conditions(self) -> List[str]:
        raise NotImplementedError

    def getDistribution(self, mNodes: Optional[Dict[str, str]]) -> Dict[str, float]:
        raise NotImplementedError

    @conditions.setter
    def conditions(self, condFeatures: Dict[str, List[str]]) -> None:
        raise NotImplementedError

    @cacheDict
    def _produceDistributionOutput(self, arr: np.array) -> Dict[str, float]:
        if len(arr) != len(self.features):
            raise Exception(
                "number of probs ({}) != number of features ({})".format(
                    len(arr), len(self.features)
                )
            )
        result: Dict[str, float] = dict()
        for feature, prob in zip(self.features, arr):
            result[feature] = prob
        return result

    def __str__(self) -> str:
        # TODO
        return "{}".format(self._table)


class ConditionalProbability(Probability):
    def __init__(
        self,
        name: str,
        table: List[float],
        shape: Tuple[int],
        features: List[str],
        conditions: List[str],
    ):
        super().__init__(name, table, shape, features, conditions)
        self.__conditions: Dict[str, int] = {
            val: index for index, val in enumerate(conditions)
        }
        self.__conditionalFeatures: Dict[str, Dict[str, int]] = dict()

    @property
    def conditions(self) -> List[str]:
        return list(self.__conditions.keys())

    def setConditionalFeatures(self, condFeatures: Dict[str, List[str]]) -> None:
        for condition, features in condFeatures.items():
            if condition not in self.__conditions:
                raise Exception("Invalid condition")
            self.__conditionalFeatures[condition] = {
                val: index for index, val in enumerate(features)
            }

    def getConditionalFeatures(self):
        return self.__conditionalFeatures

    def getProbabilities(self, features: List[str]) -> np.array:
        # TODO
        pass

    # @timeExecute
    def getDistribution(self, mNodes: Optional[Dict[str, str]]) -> Dict[str, float]:
        if mNodes is None:
            raise Exception("input None node")
        index: List[int] = []
        for node, feature in mNodes.items():
            if node not in self.__conditionalFeatures:
                continue
            index.append(self.__conditionalFeatures[node][feature])

        out: np.array = self._cdfTable
        for i in index:
            out = out[i]
        return self._produceDistributionOutput(out)

    def getProbability(self, mNodes: Optional[Dict[str, str]], feature: str) -> float:
        if mNodes is None:
            raise Exception("input None node")
        index: List[int] = []
        for node, feature in mNodes.items():
            if node not in self.__conditionalFeatures:
                continue
            index.append(self.__conditionalFeatures[node][feature])

        out: np.array = self._cdfTable
        for i in index:
            out = out[i]
        return out[self._features[feature]]

    def generateSample(self, mNodes: Optional[Dict[str, str]]) -> Dict[str, float]:
        if mNodes is None:
            raise Exception("input None node")
        index: List[int] = []
        for node, feature in mNodes.items():
            if node not in self.__conditionalFeatures:
                continue
            index.append(self.__conditionalFeatures[node][feature])
        out: np.array = self._cdfTable
        for i in index:
            out = out[i]
        iSample = generateOneSample(out)
        return self._featuresArray[iSample]


class DiscreteDistribution(Probability):
    def __init__(
        self, name: str, table: List[float], shape: Tuple[int], features: List[str],
    ) -> None:
        super().__init__(name, table, shape, features, None)

    def getDistribution(
        self, mNodes: Optional[Dict[str, str]] = None
    ) -> Dict[str, float]:
        probs: np.array = self._table[0]
        if len(probs) != len(self._featuresArray):
            raise Exception(
                "number of probs ({}) != number of features ({})".format(
                    len(probs), len(self._featuresArray)
                )
            )
        return self._produceDistributionOutput(probs)

    def getProbability(self, mNodes: Optional[Dict[str, str]], feature: str) -> float:
        probs: np.array = self._table[0]
        if len(probs) != len(self._featuresArray):
            raise Exception(
                "number of probs ({}) != number of features ({})".format(
                    len(probs), len(self._featuresArray)
                )
            )
        return probs[self._features[feature]]

    def generateSample(self, mNodes: Optional[Dict[str, str]]) -> Dict[str, float]:
        iSample = generateOneSample(self._cdfTable[0])
        return self._featuresArray[iSample]
