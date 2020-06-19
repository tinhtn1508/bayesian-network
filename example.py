from model import (
    GenerateRandomProbability,
    DiscreteDistribution,
    ConditionalProbability,
    Node,
    BayesianNetwork,
)
from graph import UnweightedDirectionAdjacencyMatrix, TopoSortAlgorithm

PD = DiscreteDistribution("D", [0.6, 0.4], (1, 2), ["Easy", "Hard"])
nodeP = Node(PD)
PI = DiscreteDistribution("I", [0.7, 0.3], (1, 2), ["Low", "High"])
nodeI = Node(PI)

PS = ConditionalProbability("S", [0.95, 0.05, 0.2, 0.8], (2, 2), ["Low", "High"], ["I"])
PS.conditions = {PI.name: PI.features}
nodeS = Node(PS)

PG = ConditionalProbability(
    "G",
    [0.3, 0.4, 0.3, 0.05, 0.25, 0.7, 0.9, 0.08, 0.02, 0.5, 0.3, 0.2],
    (2, 2, 3),
    ["A", "B", "C"],
    ["D", "I"],
)
PG.conditions = {PI.name: PI.features, PD.name: PD.features}
nodeG = Node(PG)

print(nodeG.getDistribution({"I": "Low", "D": "Hard"}))

PL = ConditionalProbability(
    "L", [0.1, 0.9, 0.4, 0.6, 0.99, 0.01], (3, 2), ["Weak", "High"], ["G"]
)
PL.conditions = {PG.name: PG.features}
nodeL = Node(PL)

print(nodeL.getDistribution({"G": "A"}))

network = BayesianNetwork()
network.addPath(nodeG, nodeL)
network.addPath(nodeI, nodeS)
network.addPath(nodeP, nodeG)
network.addPath(nodeI, nodeG)
samples = network.forward()
print(network.forwardStats({"D": "Easy", "I": "Low", "G": "A", "S": "High", "L": "High"}, None))
print(network.forwardStats({"L": "High"}, {"D": "Easy", "I": "Low", "G": "A", "S": "High"}))
