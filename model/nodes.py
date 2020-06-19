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
    def __init__(self, probTable: Probability) -> None:
        self.__probTable: Probability = probTable

    @property
    def name(self) -> str:
        return self.__probTable.name

    @property
    def features(self) -> List[str]:
        return self.__probTable.features

    def getDistribution(self, param: Optional[Dict[str, str]] = None) -> Dict[str, float]:
        return self.__probTable.getProbability(param)

    def __str__(self) -> str:
        return self.name

    @classmethod
    def fromTxt(cls, lineFormat: str):
        # TODO
        pass

    @classmethod
    def fromSample(cls, sample: Probability, connector: List[str]):
        return cls(sample, connector)
