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

    @property
    def conditions(self) -> List[str]:
        return self.__probTable.conditions

    def setConditionalFeatures(self, condFeatures: Dict[str, List[str]]) -> None:
        self.__probTable.setConditionalFeatures(condFeatures)

    def getDistribution(
        self, param: Optional[Dict[str, str]] = None
    ) -> Dict[str, float]:
        return self.__probTable.getProbability(param)

    def isCondition(self):
        return isinstance(self.__probTable, ConditionalProbability)

    def __str__(self) -> str:
        return self.name

    @classmethod
    def fromTxt(cls, lineFormat: str):
        format = lineFormat.split(";")
        if len(format) != 5:
            raise Exception("Incorrect format line txt")
        name = format[0]
        conditions = None if not format[1] else format[1].split(",")

        features = format[2].split(",")
        if len(format[3]) == 1:
            shape = (1, int(format[3][0]))
        else:
            shape = tuple([int(v) for v in format[3].split(",")])
        probList = [float(v) for v in format[4].split(",")]
        if conditions is None:
            prob = DiscreteDistribution(name, probList, shape, features)
        else:
            prob = ConditionalProbability(name, probList, shape, features, conditions)
        return cls(prob)

    @classmethod
    def fromSample(cls, sample: Probability):
        return cls(sample)
