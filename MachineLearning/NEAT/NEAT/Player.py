"""

the definition for an agent in NEAT

"""

import Genome as Genome
import Server as server
import Globals as Globals

# Maybe this can store some sort of reference ID, and then can poll unity for
# it's respective reference for the values


class Player:
    fitness = None
    brain = None

    genomeInputs = 10  # number of sensors
    genomeOutputs = 4  # number of buttons to press

    vision = [0] * genomeInputs  # ALL inputs from Unity
    decision = [0] * genomeOutputs  # Output buttons
    unadjustedFitness = None
    lifespan = 0
    dead = False
    score = None
    gen = 0

    server = None
    port = None

    id = ""

    def __init__(self):
        self.brain = Genome.Genome(self.genomeInputs, self.genomeOutputs)

        self.id = "g" + str(self.gen) + ":n" + str(Globals.count)
        Globals.count += 1

    def move(self):
        # Control/ communication with Unity
        pass

    # performs the look - think - update every tick
    def update(self):
        if self.server.dead:
            self.dead = True

    # retrieve latest vision data from the server
    def look(self):
        data = self.server.getData()
        self.vision = data

    # makes the prediction based on inputs and sends the output
    def think(self):
        max = 0
        maxIndex = 0
        decision = self.brain.feedForward(self.vision)

        for i in range(0, len(decision)):
            if decision[i] > max:
                max = decision[i]
                maxIndex = i

        self.server.mostRecentOutData = decision

    # return a copy of this player
    def clone(self):
        clone = Player()
        clone.brain = self.brain.clone()
        clone.fitness = self.fitness
        clone.brain.generateNetwork()
        clone.gen = self.gen
        clone.bestscore = self.score
        return clone

    def cloneForReplay(self):
        clone = Player()
        clone.brain = self.brain.clone()
        clone.fitness = self.fitness
        clone.brain.generateNetwork()
        clone.gen = self.gen
        clone.bestscore = self.score

        return clone

    # calculate fitness
    def calculateFitness(self):
        self.score = self.server.getFinalScore()
        self.fitness = self.score * self.score
        return self.fitness

    def crossover(self, parent2):
        child = Player()
        child.brain = self.brain.crossover(parent2.brain)
        child.brain.generateNetwork()
        return child
