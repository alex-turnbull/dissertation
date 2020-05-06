"""

Represents a neuron in the brain

"""

import math


class Node:
    number = None
    inputSum = 0  # current sum before activation
    outputValue = 0  # after activation function is applied
    outputConnections = []
    layer = 0

    def __init__(self, no):
        self.number = no

    def sigmoid(self, x):
        y = 1 / (1 + pow(math.e, -4.9*x))
        return y

    # function to send its output value into the inputs of connected nodes
    def engage(self):
        if self.layer != 0:
            self.outputValue = self.sigmoid(self.inputSum)

        for i in range(0, len(self.outputConnections)):
            if self.outputConnections[i].enabled:
                self.outputConnections[i].toNode.inputSum += self.outputConnections[i].weight * float(self.outputValue)

    def isConnectedTo(self, node):
        if node.layer == self.layer:
            return False

        if node.layer < self.layer:
            for i in range(0, len(node.outputConnections)):
                if node.outputConnections[i].toNode == self:
                    return True

        else:
            for i in range(0, len(self.outputConnections)):
                if self.outputConnections[i].toNode == node:
                    return True

        return False

    def clone(self):
        clone = Node(self.number)
        clone.layer = self.layer
        return clone
