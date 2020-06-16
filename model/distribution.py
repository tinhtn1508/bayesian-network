import numpy as np
from functools import reduce
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


class Probability:
    def __init__(
        self,
        name: str,
        table: List[float],
        shape: Tuple[int],
        features: List[str],
        conditions: List[str],
    ):
        self._name = name
        self._features = {val: index for index, val in enumerate(features)}
        if len(table) != reduce((lambda x, y: x * y), shape):
            raise Exception(
                "Don't match between length of table and shape, length: {}, shape: {}".format(
                    len(table), shape
                )
            )
        self._table = np.array(table).reshape(shape)
        sumProb = np.sum(self._table, axis=len(self._table.shape) - 1)
        if sumProb.mean() != 1.0:
            raise Exception("Incorrect probability")

    def getFeatures(self) -> List[str]:
        return list(self._features.keys())

    def getName(self) -> str:
        return self._name

    def getConditions(self) -> List[str]:
        raise NotImplementedError

    def getProbability(self, mNodes: Hashable) -> np.array:
        raise NotImplementedError

    def setConditionalFeatures(self, condFeatures: Hashable) -> None:
        raise NotImplementedError

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
        self.__conditions = {val: index for index, val in enumerate(conditions)}
        self.__conditionalFeatures = dict()

    def getConditions(self) -> List[str]:
        return list(self.__conditions.keys())

    def setConditionalFeatures(self, condFeatures: Hashable) -> None:
        for condition, features in condFeatures.items():
            if condition not in self.__conditions:
                raise Exception("Invalid condition")
            self.__conditionalFeatures[condition] = {
                val: index for index, val in enumerate(features)
            }

    def getProbabilities(self, features: List[str]) -> np.array:
        # TODO
        pass

    def getProbability(self, mNodes: Hashable) -> np.array:
        index = []
        for node, feature in mNodes.items():
            index.append(self.__conditionalFeatures[node][feature])

        out = self._table
        for i in index:
            out = out[i]
        return out


class UnconditionalProbability(Probability):
    def __init__(
        self, name: str, table: List[float], shape: Tuple[int], features: List[str],
    ):
        super().__init__(name, table, shape, features, None)

    def getProbability(self, mNodes: Hashable = None) -> np.array:
        return self._table[0]
