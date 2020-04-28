import random
import numpy


class ConnectionGene:
    fromNode = None
    toNode = None
    weight = None
    enabled = True
    innovationNo = None

    def __init__(self, fromNode, toNode, w, inno):
        self.fromNode = fromNode
        self.toNode = toNode
        self.weight = w
        self.innovationNo = inno

    def mutateWeight(self):
        rand2 = random.uniform(0, 1)
        if rand2 < 0.1:
            self.weight = random.uniform(-1, 1)
        else:
            self.weight += numpy.random.normal()/50
            if self.weight > 1:
                self.weight = 1
            if self.weight < -1:
                self.weight = -1

    def clone(self, fromNode, toNode):
        clone = ConnectionGene(fromNode, toNode, self.weight, self.innovationNo)
        clone.enabled = self.enabled
        return clone
