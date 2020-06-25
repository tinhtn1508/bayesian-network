from graph import UnweightedDirectionAdjacencyMatrix, TopoSortAlgorithm
from copy import deepcopy
from .nodes import Node
from common import timeExecute, ThreadPool
from .generator import GenerateRandomProbability
from multiprocessing import cpu_count
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
    Callable,
)


class BayesianNetwork(UnweightedDirectionAdjacencyMatrix):
    def __init__(self, initializedSamples: int = 1000000):
        super().__init__(None)
        self.__generator: GenerateRandomProbability = GenerateRandomProbability()
        self.__initSamples: int = initializedSamples
        self.__nodeTable: Dict[str, V] = dict()
        self.__topoNodes: Optional[List[Node]] = None
        self.__samples: Optional[List[Dict[str, str]]] = None

    def addNewNode(self, node: Node) -> None:
        if not isinstance(node, Node):
            raise Exception("input object is not a Node")
        super().addNewNode(node)
        self.__nodeTable[node.name] = node

    # @timeExecute
    def __generateSample(self, nSamples: int) -> Dict[str, str]:
        samples = []
        for _ in range(nSamples):
            state: Dict[str, str] = dict()
            for node in self.__topoNodes:
                sample = node.generateSample(state)
                state[node.name] = sample
            samples.append(state)
        return samples

    # @timeExecute
    def generateSamples(self, steps=-1) -> List[Dict[str, str]]:
        if len(self.vertexSet()) == 0:
            raise Exception("Graph haven't been initialized!")
        if self.__topoNodes is None:
            topo: TopoSortAlgorithm = TopoSortAlgorithm(self)
            self.__topoNodes = [node for node in topo.bfs()]
        samples: List[Dict[str, str]] = []
        if steps < 0:
            steps = self.__initSamples

        poolSize: int = cpu_count()
        taskList: List[Callable[[], Optional[Any]]] = [
            partial(self.__generateSample, int(steps / poolSize) + 1)
            for _ in range(poolSize)
        ]

        pool: ThreadPool = ThreadPool(taskList, poolSize)
        pool.startAndWait()
        outputs: List[List[Dict[str, str]]] = pool.result
        for output in outputs:
            samples.extend(output)
        self.__samples = samples

    def __filterSample(self, prob: Dict[str, str], record: Dict[str, str]) -> bool:
        for name, feature in prob.items():
            if name not in record:
                raise Exception("Failed to get item {} in the record".format(name))
            if feature != record[name]:
                return False
        return True

    def __samplesFiltering(
        self, samples: List[Dict[str, str]], filters: Dict[str, str]
    ) -> Generator[Dict[str, str], None, None]:
        for result in filter(partial(self.__filterSample, filters), samples):
            yield result

    def __noneConditionStats(
        self, prob: Dict[str, str], samples: List[Dict[str, str]]
    ) -> float:
        cnt: int = 0
        for _ in self.__samplesFiltering(samples, prob):
            cnt += 1
        return cnt / len(samples)

    def __statsCheck(self, prob: Dict[str, str], conditions: Optional[Dict[str, str]]):
        if prob is None:
            raise Exception("No prob is required!!!")
        if self.__samples is None or len(self.__samples) == 0:
            raise Exception(
                "No sample has been generated, call generateSamples() first"
            )
        if conditions is None:
            return
        for name in prob:
            if name in conditions:
                raise Exception(
                    "Invalid input, name {} duplicate in prob and conditions".format(
                        name
                    )
                )

    def forwardStats(
        self, prob: Dict[str, str], conditions: Optional[Dict[str, str]]
    ) -> float:
        self.__statsCheck(prob, conditions)
        if conditions is None:
            return self.__noneConditionStats(prob, self.__samples)
        return self.__noneConditionStats(
            prob,
            [item for item in self.__samplesFiltering(self.__samples, conditions)],
        )

    def __likelihoodSampleWeight(
        self, conditions: Dict[str, str], sample: Dict[str, str]
    ):
        w: float = 1.0
        for conditionName, conditionValue in conditions.items():
            w *= self.__nodeTable[conditionName].getProbability(sample, conditionValue)
        return sample, w

    def likelihoodStats(
        self, prob: Dict[str, str], conditions: Optional[Dict[str, str]]
    ) -> float:
        self.__statsCheck(prob, conditions)
        if conditions is None:
            return self.__noneConditionStats(prob, self.__samples)

        totalw: float = 0.0
        conditionw: float = 0.0
        for sample, w in map(
            partial(self.__likelihoodSampleWeight, conditions),
            self.__samplesFiltering(self.__samples, conditions),
        ):
            totalw += w
            if self.__filterSample(prob, sample):
                conditionw += w
        if totalw == 0.0:
            return 0.0
        return conditionw / totalw

    def __statsBatch(
        self,
        paramList: List[Tuple[Dict[str, str], Dict[str, str]]],
        statsFunc: Callable[[Dict[str, str], Optional[Dict[str, str]]], float],
    ) -> List[float]:
        taskList: List[Callable[[], Optional[Any]]] = [
            partial(statsFunc, prob, conditions) for prob, conditions in paramList
        ]

        pool: ThreadPool = ThreadPool(taskList, cpu_count())
        pool.startAndWait()
        return pool.result

    # @timeExecute
    def forwardStatsBatch(
        self, paramList: List[Tuple[Dict[str, str], Dict[str, str]]],
    ) -> List[float]:
        return self.__statsBatch(paramList, self.forwardStats)

    # @timeExecute
    def likelihoodStatsBatch(
        self, paramList: List[Tuple[Dict[str, str], Dict[str, str]]]
    ) -> List[float]:
        return self.__statsBatch(paramList, self.likelihoodStats)
