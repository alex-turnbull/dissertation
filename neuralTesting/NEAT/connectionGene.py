import NEAT.Node as Node
import random
import numpy

fromNode = None
toNode = None
weight = None
enabled = True
innovationNo = None

class connectionGene:
    def __init__(self, fromN, to, w, inno):
        self.fromNode = fromN
        self.toNode = to
        self.weight = w
        self.innovationNo = inno

    def mutateWeight(self):
        rand2 = random.randrange(0, 1)
        if rand2 < 0.1:
            self.weight = random.randrange(-1, 1)
        else:
            self.weight += numpy.random.normal()/50
            if self.weight > 1:
                self.weight = 1
            if self.weight < -1:
                self.weight = -1

    def clone(self, fromN, to):
        clone = connectionGene(fromN, to, self.weight, self.innovationNo)
        clone.enabled = self.enabled
        return clone