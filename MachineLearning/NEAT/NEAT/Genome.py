"""

"""

import math
import random

import Globals as globals
import Node as Node
import ConnectionGene as connectionGene
import ConnectionHistory as connectionHistory


class Genome:
    genes = []
    nodes = []
    network = []
    layers = 2
    nextNode = 0
    biasnode = None
    inputs = None
    outputs = None

    # def __init__(self, inNum, out, crossover):
    #    self.inputs = inNum
    #    self.outputs = out

    def __init__(self, inNum, out, crossover=None):
        self.inputs = inNum
        self.outputs = out

        if crossover is None:
            for i in range(0, self.inputs):
                self.nodes.append(Node.Node(i))
                self.nextNode += 1
                self.nodes[i].layer = 0

            for i in range(0, self.outputs):
                self.nodes.append(Node.Node(i+self.inputs))
                self.nodes[i+self.inputs].layer = 1
                self.nextNode += 1

            self.nodes.append(Node.Node(self.nextNode))
            self.biasnode = self.nextNode
            self.nextNode += 1
            self.nodes[self.biasnode].layer = 0

    def getNode(self, nodeNumber):
        for i in range(0, len(self.nodes)):
            if self.nodes[i].number == nodeNumber:
                return self.nodes[i]

        return None

    def connectNodes(self):
        for i in range(0, len(self.nodes)):
            self.nodes[i].outputConnections.clear()

        for i in range(0, len(self.genes)):
            self.genes[i].fromNode.outputConnections.append(self.genes[i])

    def feedForward(self, inputValues):
        for i in range(0, self.inputs):
            self.nodes[i].outputValue = inputValues[i]

        self.nodes[self.biasnode].outputValue = 1

        for i in range(0, len(self.network)):
            self.network[i].engage()

        outs = [0] * self.outputs
        for i in range(0, self.outputs):
            outs[i] = self.nodes[self.inputs + i].outputValue

        for i in range(0, len(self.nodes)):
            self.nodes[i].inputSum = 0

        return outs

    def generateNetwork(self):
        self.connectNodes()
        self.network = []

        for i in range(0, self.layers):
            for x in range(0, len(self.nodes)):
                if self.nodes[x].layer == i:
                    self.network.append(self.nodes[x])

    def addNode(self, innovationHistory):
        if len(self.genes) == 0:
            self.addConnection(innovationHistory)
            return

        randomConnection = math.floor(random.uniform(0, len(self.genes)))

        while self.genes[randomConnection].fromNode == self.nodes[self.biasnode] and len(self.genes) != 1:
            randomConnection = math.floor(random.uniform(0, len(self.genes)))

        self.genes[randomConnection].enabled = False

        newNodeNo = self.nextNode
        self.nodes.append(Node.Node(newNodeNo))
        self.nextNode += 1

        connectionInnovationNumber = self.getInnovationNumber(innovationHistory, self.genes[randomConnection].fromNode, self.getNode(newNodeNo))
        self.genes.append(connectionGene.ConnectionGene(self.genes[randomConnection].fromNode, self.getNode(newNodeNo), 1, connectionInnovationNumber))

        connectionInnovationNumber = self.getInnovationNumber(innovationHistory, self.getNode(newNodeNo), self.genes[randomConnection].toNode)

        self.genes.append(connectionGene.ConnectionGene(self.getNode(newNodeNo), self.genes[randomConnection].toNode, self.genes[randomConnection].weight, connectionInnovationNumber))
        self.getNode(newNodeNo).layer = self.genes[randomConnection].fromNode.layer + 1

        connectionInnovationNumber = self.getInnovationNumber(innovationHistory, self.nodes[self.biasnode], self.getNode(newNodeNo))

        self.genes.append(connectionGene.ConnectionGene(self.nodes[self.biasnode], self.getNode(newNodeNo), 0, connectionInnovationNumber))

        if self.getNode(newNodeNo).layer == self.genes[randomConnection].toNode.layer:
            for i in range(0, len(self.nodes)):
                if self.nodes[i].layer >= self.getNode(newNodeNo).layer:
                    self.nodes[i].layer += 1

            self.layers += 1

        self.connectNodes()


    def addConnection(self, innovationHistory):
        if self.fullyConnected():
            print("connetion failed lmao")
            return

        randomNode1 = math.floor(random.uniform(0, len(self.nodes)))
        randomNode2 = math.floor(random.uniform(0, len(self.nodes)))
        while self.randomConnectionNodesHandler(randomNode1, randomNode2):
            randomNode1 = math.floor(random.uniform(0, len(self.nodes)))
            randomNode2 = math.floor(random.uniform(0, len(self.nodes)))

        if self.nodes[randomNode1].layer > self.nodes[randomNode2].layer:
            temp = randomNode2
            randomNode2 = randomNode1
            randomNode1 = temp

        connectionInnovationNumber = self.getInnovationNumber(innovationHistory, self.nodes[randomNode1], self.nodes[randomNode2])

        self.genes.append(connectionGene.ConnectionGene(self.nodes[randomNode1], self.nodes[randomNode2], random.uniform(-1, 1), connectionInnovationNumber))
        self.connectNodes()

    def randomConnectionNodesHandler(self, r1, r2):
        if self.nodes[r1].layer == self.nodes[r2].layer:
            return True
        if self.nodes[r1].isConnectedTo(self.nodes[r2]):
            return True

        return False

    def getInnovationNumber(self, innovationHistory, nodeFrom, nodeTo):
        isNew = True
        connectionInnovationNumber = globals.nextConnectionNo

        for i in range(0, len(innovationHistory)):
            if innovationHistory[i].matches(self, nodeFrom, nodeTo):
                isNew = False
                connectionInnovationNumber = innovationHistory[i].innovationNumber
                break

        if isNew:
            innoNumbers = []
            for i in range(0, len(self.genes)):
                innoNumbers.append(self.genes[i].innovationNo)

            innovationHistory.append(connectionHistory.ConnectionHistory(nodeFrom.number, nodeTo.number, connectionInnovationNumber, innoNumbers))
            globals.nextConnectionNo += 1

        return connectionInnovationNumber

    def fullyConnected(self):
        maxConnections = 0
        nodesInLayers = [0] * self.layers

        for i in range(0, len(self.nodes)):
            nodesInLayers[self.nodes[i].layer] += 1

        for i in range(0, self.layers-1):
            nodesInFront = 0
            for j in range(i+1, self.layers):
                nodesInFront += nodesInLayers[j]

            maxConnections += nodesInLayers[i] * nodesInFront

        if maxConnections == len(self.genes):
            return True
        return False

    def mutate(self, innovationHistory):
        if len(self.genes) == 0:
            self.addConnection(innovationHistory)

        rand1 = random.uniform(0, 1)
        if rand1 < 0.8:
            for i in range(len(self.genes)):
                self.genes[i].mutateWeight()

        rand2 = random.uniform(0, 1)
        if rand2 < 0.08:
            self.addConnection(innovationHistory)

        rand3 = random.uniform(0, 1)
        if rand3 < 0.02:
            self.addNode(innovationHistory)

    def crossover(self, parent2):
        child = Genome(self.inputs, self.outputs, True)
        child.genes.clear()
        child.nodes.clear()
        child.layers = self.layers
        child.nextNode = self.nextNode
        child.biasnode = self.biasnode
        childGenes = []
        isEnabled = []

        for i in range(0, len(self.genes)):
            setEnabled = True

            parent2Gene = self.matchingGene(parent2, self.genes[i].innovationNo)
            if parent2Gene != -1:
                if not self.genes[i].enabled or not parent2.genes[parent2Gene].enabled:
                    if random.uniform(0, 1) < 0.75:
                        setEnabled = False
                rand = random.uniform(0, 1)
                if rand <= 0.5:
                    childGenes.append(self.genes[i])
                else:
                    childGenes.append(parent2.genes[parent2Gene])
            else:
                childGenes.append(parent2.genes[parent2Gene])
                setEnabled = self.genes[i].enabled

            isEnabled.append(setEnabled)

        for i in range(0,len(self.nodes)):
            child.nodes.append(self.nodes[i].clone())

        for i in range(len(childGenes)):
            child.genes.append(childGenes[i].clone(child.getNode(childGenes[i].fromNode.number), child.getNode(childGenes[i].toNode.Number)))
            child.genes[i].enabled = isEnabled[i]

        child.connectNodes()
        return child

    def matchingGene(self, parent2, innovationNumber):
        for i in range(0,len(parent2.genes)):
            if parent2.genes[i].innovationNo == innovationNumber:
                return i

        return -1

    def printGenome(self):
        print("Print genome   layers:", self.layers)
        print("Bias Node: " + self.biasnode)
        print("nodes")
        for i in range(0, len(self.nodes)):
            print(self.nodes[i].number + ",")
        print("Genes")
        for i in range(0, len(self.genes)):
            print ("gene " + self.genes[i].innovationNo, "From Node " + self.genes[i].fromNode.number, "To node " + self.genes[i].toNode.number, "Is enabled " + self.genes[i].enabled, "From layer " + self.genes[i].fromNode.layer, "To layer " + self.genes[i].toNode.layer, "Weight " + self.genes[i].weight)

        print(" ")

    def clone(self):
        clone = Genome(self.inputs, self.outputs, True)
        for i in range(0, len(self.nodes)):
            clone.nodes.append(self.nodes[i].clone())

        for i in range(0, len(self.genes)):
            clone.genes.append(self.genes[i].clone(clone.getNode(self.genes[i].fromNode.number), clone.getNode(self.genes[i].toNode.number)))

        clone.layers = self.layers
        clone.nextNode = self.nextNode
        clone.biasnode = self.biasnode
        clone.connectNodes()

        return clone
