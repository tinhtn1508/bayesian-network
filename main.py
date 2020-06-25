import graph
import argparse
import os
from common import timeExecute
from model import (
    Node,
    ModelParser,
    TestParser,
    TxtParser,
    BayesianNetwork,
)
from typing import (
    List,
    Dict,
    Optional,
    Tuple,
)


class BayesianNetworkRunner:
    def __init__(
        self, modelFile: str, testFile: str, algorithm: str, output: str
    ) -> None:
        err: Optional[str] = self.__checkArguments(
            modelFile, testFile, algorithm, output
        )
        if err is not None:
            raise Exception(err)
        self.__network: BayesianNetwork = self.__produceNetwork(modelFile)
        self.__queries: List[
            Tuple[Dict[str, str], Dict[str, str]]
        ] = self.__produceQuery(testFile)
        self.__statsFunc: Callable[
            [List[Tuple[Dict[str, str], Dict[str, str]]]], List[float]
        ] = self.__network.forwardStatsBatch
        if algorithm == "likelihood":
            self.__statsFunc = self.__network.likelihoodStatsBatch
        elif algorithm == "gibbs":
            pass
            # TODO
        self.__output = TxtParser(output)

    def __checkArguments(
        self, model: str, test: str, algorithm: str, output: str
    ) -> Optional[str]:
        if not os.path.exists(model):
            return "[ERROR] The file {} does not exist.\n".format(model)
        if not os.path.exists(test):
            return "[ERROR] The file {} does not exist.\n".format(test)
        if algorithm not in ["forward", "likelihood", "gibbs"]:
            return "[ERROR] Invalid algorithm: {}\n".format(algorithm)
        if len(output) == 0:
            return "[ERROR] Invalid output path: {}".format(output)
        return None

    def __produceNetwork(self, model: str) -> BayesianNetwork:
        parser: ModelParser = ModelParser(model)
        parser.parse()

        nodes: Dict[str, Node] = parser.getNodes()
        network: BayesianNetwork = BayesianNetwork()
        for name, node in nodes.items():
            if not node.isCondition():
                continue
            node.setConditionalFeatures(
                {
                    nodes[condition].name: nodes[condition].features
                    for condition in node.conditions
                }
            )
            for condition in node.conditions:
                network.addPath(nodes[condition], node)
        return network

    def __produceQuery(self, test) -> List[Tuple[Dict[str, str], Dict[str, str]]]:
        parser: TestParser = TestParser(test)
        parser.parse()
        return parser.getQueriesTable()

    def run(self):
        self.__network.generateSamples()
        result: List[float] = self.__statsFunc(self.__queries)
        self.__output.writeLines([s for s in map(str, result)])


# @timeExecute
def main() -> None:
    parser: ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", help="path file to model")
    parser.add_argument("-t", "--test", help="path file to queries")
    parser.add_argument(
        "-o", "--output", default="output.txt", help="path file to output"
    )
    parser.add_argument(
        "-a", "--algorithm", default="forward", help="forward | likelihood | gibbs"
    )
    args = parser.parse_args()
    if args.model is None or args.test is None or args.algorithm is None:
        warning = "\nThe agruments [--model, --test, --algorithm] can not be empty\n"
        warning += "For more details, you can use the command [main.py -h]\n"
        print(warning)
        exit()

    try:
        BayesianNetworkRunner(args.model, args.test, args.algorithm, args.output).run()
    except Exception as e:
        print("Failed: {}".format(e))
    else:
        print("The inference procedure is successful !!!!!!!")
        print("Please check output at here: {}".format(os.path.abspath(args.output)))


if __name__ == "__main__":
    main()
