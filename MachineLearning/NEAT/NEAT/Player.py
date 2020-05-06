"""



"""

import Genome as Genome
import Server as server
import Globals as Globals

# Maybe this can store some sort of reference ID, and then can poll unity for
# it's respective reference for the values


class Player:
    fitness = None
    brain = None

    genomeInputs = 10
    genomeOutputs = 4

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

    def show(self):
        pass

    def move(self):
        # Control/ communication with Unity
        pass

    def update(self):
        if self.server.dead:
            self.dead = True

    def look(self):
        data = self.server.getData()
        self.vision = data

    def think(self):
        max = 0
        maxIndex = 0
        decision = self.brain.feedForward(self.vision)

        for i in range(0, len(decision)):
            if decision[i] > max:
                max = decision[i]
                maxIndex = i

        self.server.mostRecentOutData = decision


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

    def calculateFitness(self):
        self.score = self.server.getFinalScore()
        self.fitness = self.score * self.score
        del self.server
        return self.fitness

    def crossover(self, parent2):
        child = Player()
        child.brain = self.brain.crossover(parent2.brain)
        child.brain.generateNetwork()
        return child
