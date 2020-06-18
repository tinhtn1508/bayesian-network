import numpy as np

from .generator import GenerateRandomProbability
from .distribution import DiscreteDistribution, ConditionalProbability, Probability
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


class Node:
    def __init__(self, probTable: Probability):
        self.__probTable = probTable

    def getName(self) -> str:
        return self.__probTable.name

    def getFeatures(self) -> List[str]:
        return self.__probTable.features

    def getDistribution(self, param: Hashable = None):
        return self.__probTable.getProbability(param)

    def __str__(self):
        return self.getName()

    @classmethod
    def fromTxt(cls, lineFormat: str):
        # TODO
        pass

    @classmethod
    def fromSample(cls, sample: Probability, connector: List[str]):
        return cls(sample, connector)
