from graph import UnweightedDirectionAdjacencyMatrix, TopoSortAlgorithm
from copy import deepcopy
from .nodes import Node
from common import timeExecute, ThreadPool
from .generator import GenerateRandomProbability
from multiprocessing import cpu_count
from functools import partial
from random import seed
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
    def __init__(self, initializedSamples: int):
        super().__init__(None)
        self._generator: GenerateRandomProbability = GenerateRandomProbability()
        self._initSamples: int = initializedSamples
        self._nodeTable: Dict[str, V] = dict()
        self._topoNodes: Optional[List[Node]] = None

    @classmethod
    def factory(cls, algorithm: str, initializedSamples: int = 1000000) -> Any:
        if algorithm == "forward":
            return ForwardBayesianNetwork(initializedSamples)
        elif algorithm == "likelihood":
            return LikelihoodBayesianNetwork(initializedSamples)
        raise Exception("cannot create {} Bayesian netword!")

    def addNewNode(self, node: Node) -> None:
        if not isinstance(node, Node):
            raise Exception("input object is not a Node")
        if node is None:
            raise Exception("cannot add None node")
        super().addNewNode(node)
        self._nodeTable[node.name] = node

    def batchQuery(self,
        paramList: List[Tuple[Dict[str, str], Optional[Dict[str, str]]]],
        steps: int = -1
    ) -> List[float]:
        pass

    def _prepare(self) -> None:
        if len(self.vertexSet()) == 0:
            raise Exception("Graph haven't been initialized!")
        if self._topoNodes is None:
            topo: TopoSortAlgorithm = TopoSortAlgorithm(self)
            self._topoNodes = [node for node in topo.bfs()]

    def _generateSample(self, originalState: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        state: Optional[Dict[str, str]] = originalState
        if state is None:
            state = dict()
        else:
            state = deepcopy(originalState)
        for node in self._topoNodes:
            if node.name in state:
                continue
            state[node.name] = node.generateSample(state)
        return state

    def _generateSamples(self,
        nSamples: int,
        originalState: Optional[Dict[str, str]] = None
    ) -> List[Dict[str, str]]:
        if nSamples < 1:
            raise Exception("number of samples cannot < 1")
        samples = []
        for _ in range(nSamples):
            samples.append(self._generateSample(originalState))
        return samples

    def _filterSample(self, prob: Dict[str, str], record: Dict[str, str]) -> bool:
        for name, feature in prob.items():
            if name not in record:
                raise Exception("Failed to get item {} in the record".format(name))
            if feature != record[name]:
                return False
        return True

    def _filterSamples(
        self, samples: List[Dict[str, str]], filters: Dict[str, str]
    ) -> Generator[Dict[str, str], None, None]:
        for result in filter(partial(self._filterSample, filters), samples):
            yield result

    def _noneConditionStatsSample(
        self, prob: Dict[str, str], samples: List[Dict[str, str]]
    ) -> Tuple[int, int]:
        if len(samples) == 0:
            raise Exception("input no sample!")
        cnt: int = 0
        for _ in self._filterSamples(samples, prob):
            cnt += 1
        return (cnt, len(samples))

    def _noneConditionStats(
        self, prob: Dict[str, str], samples: List[Dict[str, str]]
    ) -> float:
        cnt, total = self._noneConditionStatsSample(prob, samples)
        return cnt/total

    def _statsCheck(self, prob: Dict[str, str], conditions: Optional[Dict[str, str]]):
        if prob is None:
            raise Exception("input None prob!!!")
        if conditions is None:
            return
        for name in prob:
            if name in conditions:
                raise Exception(
                    "Invalid input, name {} duplicate in prob and conditions".format(
                        name
                    )
                )

class ForwardBayesianNetwork(BayesianNetwork):
    def __generateAndQuery(self,
        steps: int,
        paramList: List[Tuple[Dict[str, str], Optional[Dict[str, str]]]],
        index: int
    ) -> List[Tuple[int, int]]:
        seed(index)
        result: List[Tuple[int, int]] = list()
        samples: List[Dict[str, str]] = self._generateSamples(steps)
        for prob, conditions in paramList:
            self._statsCheck(prob, conditions)
            if conditions is None:
                result.append(self._noneConditionStatsSample(prob, samples))
            else:
                result.append(self._noneConditionStatsSample(
                    prob,
                    [item for item in self._filterSamples(samples, conditions)],
                ))
        return result

    def __convertBatchJobResults(self,
        batchJobResults: List[List[Tuple[int, int]]]
    ) -> List[float]:
        if batchJobResults is None or len(batchJobResults) < 1:
            raise Exception("invalid batch job results")
        result: List[float] = [0.0 for _ in range(len(batchJobResults[0]))]
        for i in range(len(result)):
            total: int = 0
            filtered: int = 0
            for lst in batchJobResults:
                filtered += lst[i][0]
                total += lst[i][1]
            result[i] = filtered/total if total != 0 else 0.0
        return result

    def batchQuery(self,
        paramList: List[Tuple[Dict[str, str], Optional[Dict[str, str]]]],
        steps: int = -1
    ) -> List[float]:
        if paramList is None or len(paramList) < 1:
            raise Exception("invalid query params")
        self._prepare()
        if steps <= 0:
            steps = self._initSamples

        poolSize: int = cpu_count() - 1
        taskList: List[Callable[[], Optional[Any]]] = [
            partial(self.__generateAndQuery, int(steps/poolSize) + 1, paramList, i)
        for i in range(poolSize)]

        pool: ThreadPool = ThreadPool(taskList, poolSize)
        pool.startAndWait()

        return self.__convertBatchJobResults(pool.result)

class LikelihoodBayesianNetwork(BayesianNetwork):
    def __buildConditionalKey(self, condition: Optional[Dict[str, str]]) -> str:
        if condition is None:
            return "standard"
        keyList: List[str] = sorted(condition.keys())
        conditionKey: List[str] = list()
        for k in keyList:
            conditionKey.append(k + ':' + condition[k])
        return ';'.join(conditionKey)

    def __doParamListIndexing(self,
        paramList: List[Tuple[Dict[str, str], Optional[Dict[str, str]]]]
    ) -> Dict[str, List[int]]:
        index: Dict[str, List[int]] = dict()
        for i, param in enumerate(paramList):
            key: str = self.__buildConditionalKey(param[1])
            if key not in index:
                index[key] = [i]
            else:
                index[key].append(i)
        return index

    def __likelihoodSampleWeight(
        self, condition: Dict[str, str], sample: Dict[str, str]
    ):
        w: float = 1.0
        for conditionName, conditionValue in condition.items():
            w *= self._nodeTable[conditionName].getProbability(sample, conditionValue)
        return sample, w

    def __calculateLikelihoodProbability(self,
        condition: Dict[str, str],
        prob: Dict[str, str],
        samples: List[Dict[str, str]]
    ) -> float:
        if prob is None:
            raise Exception("input None condition or prob")
        if samples is None or len(samples) <= 1:
            raise Exception("no input sample found")
        if condition is None:
            return self._noneConditionStats(prob, samples)
        totalw: float = 0.0
        condw: float = 0.0
        for sample, w in map(partial(self.__likelihoodSampleWeight, condition), samples):
            totalw += w
            if self._filterSample(prob, sample):
                condw += w
        return condw/totalw if totalw != 0.0 else 0.0

    def __generateAndQuery(self,
        nSamples: int,
        conditionList: List[Optional[Dict[str, str]]],
        probList: List[Dict[str, str]],
        indexList: List[int]
    ) -> List[float]:
        seed(indexList[0])
        result: List[float] = [0.0 for _ in range(len(probList))]
        condition = conditionList[indexList[0]]
        samples: List[Dict[str, str]] = self._generateSamples(nSamples, condition)
        for i in indexList:
            prob: Dict[str, str] = probList[i]
            self._statsCheck(prob, condition)
            result[i] = self.__calculateLikelihoodProbability(condition, prob, samples)
        return result

    def __convertBatchJobResults(self, batchJobResults: List[List[float]]) -> List[float]:
        result: List[float] = [0.0 for _ in range(len(batchJobResults[0]))]
        for i in range(len(result)):
            for subresult in batchJobResults:
                result[i] += subresult[i]
        return result

    def batchQuery(self,
        paramList: List[Tuple[Dict[str, str], Optional[Dict[str, str]]]],
        steps: int = -1
    ) -> List[float]:
        self._prepare()
        if steps <= 0:
            steps = self._initSamples

        indexTable: Dict[str, List[int]] = self.__doParamListIndexing(paramList)
        probList: List[Dict[str, str]] = [
            param[0] for param in paramList
        ]
        conditionList: List[Optional[Dict[str, str]]] = [
            param[1] for param in paramList
        ]

        poolSize: int = cpu_count() - 1
        taskList: List[Callable[[], Optional[Any]]] = [
            partial(self.__generateAndQuery, steps, conditionList, probList, indexList)
        for _, indexList in indexTable.items()]
        pool: ThreadPool = ThreadPool(taskList, poolSize)
        pool.startAndWait()

        return self.__convertBatchJobResults(pool.result)
