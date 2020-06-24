from graph import UnweightedDirectionAdjacencyMatrix, TopoSortAlgorithm
from copy import deepcopy
from .nodes import Node
from common import timeExecute
from .generator import GenerateRandomProbability
from functools import partial
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


class BayesianNetwork(UnweightedDirectionAdjacencyMatrix):
    def __init__(self, initializedSamples: int = 100000):
        super().__init__(None)
        self.__generator: GenerateRandomProbability = GenerateRandomProbability()
        self.__initSamples: int = initializedSamples
        self.__nodeTable: Dict[str, V] = dict()
        self.__topoNodes: Optional[List[Node]] = None
        self.__forwardSamples: Optional[List[Dict[str, str]]] = None
        self.__likelihoodSamples: Optional[List[Dict[str, str]]] = None
        self.__likelihoodOriginalState: Optional[Dict[str, str]] = None

    def addNewNode(self, node: Node) -> None:
        if not isinstance(node, Node):
            raise Exception("input object is not a Node")
        super().addNewNode(node)
        self.__nodeTable[node.name] = node

    def __forwardGenerateSample(self) -> Dict[str, str]:
        state: Dict[str, str] = dict()
        for node in self.__topoNodes:
            sample = node.generateSample(state)
            state[node.name] = sample
        return state

    @timeExecute
    def forward(self, steps=-1) -> List[Dict[str, str]]:
        if len(self.vertexSet()) == 0:
            raise Exception("Graph haven't been initialized!")
        if self.__topoNodes is None:
            topo: TopoSortAlgorithm = TopoSortAlgorithm(self)
            self.__topoNodes = [node for node in topo.bfs()]
        samples: List[Dict[str, str]] = []
        if steps < 0:
            steps = self.__initSamples
        for _ in range(steps):
            samples.append(self.__forwardGenerateSample())
        self.__forwardSamples = samples

    def __filterSample(self, prob: Dict[str, str], record: Dict[str, str]) -> bool:
        for name, feature in prob.items():
            if name not in record:
                raise Exception("Failed to get item {} in the record".format(name))
            if feature != record[name]:
                return False
        return True

    def __forwardSamplesFilter(
        self, samples: List[Dict[str, str]], filters: Dict[str, str]
    ) -> Generator[Dict[str, str], None, None]:
        for result in filter(partial(self.__filterSample, filters), samples):
            yield result

    def __forwardNoneConditionStats(
        self, prob: Dict[str, str], samples: List[Dict[str, str]]
    ) -> float:
        cnt: int = 0
        for _ in self.__forwardSamplesFilter(samples, prob):
            cnt += 1
        return cnt / len(samples)

    def forwardStats(
        self, prob: Dict[str, str], conditions: Optional[Dict[str, str]]
    ) -> float:
        if prob is None:
            raise Exception("No prob is required!!!")
        if self.__forwardSamples is None or len(self.__forwardSamples) == 0:
            raise Exception("forward process haven't been run, call forward() first!")
        if conditions is None:
            return self.__forwardNoneConditionStats(prob, self.__forwardSamples)
        for name in prob:
            if name in conditions:
                raise Exception(
                    "Invalid input, name {} duplicate in prob and conditions".format(
                        name
                    )
                )
        return self.__forwardNoneConditionStats(
            prob,
            [
                item
                for item in self.__forwardSamplesFilter(
                    self.__forwardSamples, conditions
                )
            ],
        )

    def __likelihoodSampleWeight(self, sample: Dict[str, str]):
        w: float= 1.0
        for conditionName, conditionValue in self.__likelihoodOriginalState.items():
            w *= self.__nodeTable[conditionName].getProbability(sample, conditionValue)
        return sample, w

    def likelihoodStats(self, prob: Dict[str, str]) -> float:
        if prob is None:
            raise Exception("No prob is required!!!")
        if self.__likelihoodSamples is None or len(self.__likelihoodSamples) == 0:
            raise Exception("likelihood process haven't been run, call likelihood() first!")
        for name in prob:
            if name in self.__likelihoodOriginalState:
                raise Exception(
                    "Invalid input, name {} duplicate in prob and conditions".format(
                        name
                    )
                )

        totalw: float = 0.0
        conditionw: float = 0.0
        for sample, w in map(self.__likelihoodSampleWeight, self.__likelihoodSamples):
            totalw += w
            if self.__filterSample(prob, sample):
                conditionw += w
        return conditionw/totalw

    def __likelihoodGenerateSample(self, originalState: Dict[str, str]) -> Dict[str, str]:
        state: Dict[str, str] = deepcopy(originalState)
        for node in self.__topoNodes:
            if node.name in state:
                continue
            sample: str = node.generateSample(state)
            state[node.name] = sample
        return state

    @ timeExecute
    def likelihood(self, originalState: Dict[str, str], steps: int = -1):
        if originalState is None:
            raise Exception("expect to have original state!")
        if len(self.vertexSet()) == 0:
            raise Exception("Graph haven't been initialized!")
        if self.__topoNodes is None:
            topo: TopoSortAlgorithm = TopoSortAlgorithm(self)
            self.__topoNodes = [node for node in topo.bfs()]
        self.__likelihoodOriginalState = originalState
        samples: List[Dict[str, str]] = []
        if steps < 0:
            steps = self.__initSamples
        for _ in range(steps):
            samples.append(self.__likelihoodGenerateSample(originalState))
        self.__likelihoodSamples = samples
