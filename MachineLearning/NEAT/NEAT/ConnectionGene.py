"""

Defines a connection between 2 nodes

"""

import random
import numpy


class ConnectionGene:
    fromNode = None
    toNode = None
    weight = None
    enabled = True
    innovationNo = None
    # each connection is given a number to compare genomes

    def __init__(self, fromNode, toNode, w, inno):
        self.fromNode = fromNode
        self.toNode = toNode
        self.weight = w
        self.innovationNo = inno

    # enhances and changes the weight
    def mutateWeight(self):
        rand2 = random.uniform(0, 1)
        # a random 10% change to completely redefine the weight
        # otherwise slight modify it
        if rand2 < 0.1:
            self.weight = random.uniform(-1, 1)
        else:
            self.weight += numpy.random.normal()/50
            # restrict weight to bounds
            if self.weight > 1:
                self.weight = 1
            if self.weight < -1:
                self.weight = -1

    # returns an exact copy of this connection
    def clone(self, fromNode, toNode):
        clone = ConnectionGene(fromNode, toNode, self.weight, self.innovationNo)
        clone.enabled = self.enabled
        return clone
