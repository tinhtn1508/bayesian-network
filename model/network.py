from graph import UnweightedDirectionAdjacencyMatrix, TopoSortAlgorithm
from .nodes import Node
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
        self.__topoNodes: Optional[List[Node]] = None
        self.__forwardSamples: Optional[List[Dict[str, str]]] = None

    def __forwardGenerateSample(self) -> Dict[str, str]:
        state: Dict[str, str] = dict()
        for node in self.__topoNodes:
            distribution: Dict[str, float] = node.getDistribution(state)
            self.__generator.fit(distribution)
            sample = self.__generator.oneSample()
            state[node.name] = sample
        return state

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

    def __forwardSamplesFilter(
        self, samples: List[Dict[str, str]], filters: Dict[str, str]
    ) -> Generator[Dict[str, str], None, None]:
        def filterFn(prob: Dict[str, str], record: Dict[str, str]) -> bool:
            for name, feature in prob.items():
                if name not in record:
                    raise Exception("Failed to get item {} in the record".format(name))
                if feature != record[name]:
                    return False
            return True

        for result in filter(partial(filterFn, filters), samples):
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

    def likelihood(self):
        # TODO
        pass
