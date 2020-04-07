import Genome as Genome
import server as server
import tempGlobals as Globals

# I think I've somehow got to create a connection between this
# and an entity in unity :think:
# YIKES

# Maybe this can store some sort of reference ID, and then can poll unity for
# it's respective reference for the values

class Player:
    fitness = None
    brain = None

    vision = [0] * 10  # ALL inputs from Unity
    decision = [0] * 4  # Output buttons
    unadjustedFitness = None
    lifespan = 0
    dead = False
    score = None
    gen = 0

    genomeInputs = 10
    genomeOutputs = 4

    server = None
    port = None

    def __init__(self):
        self.brain = Genome.Genome(self.genomeInputs, self.genomeOutputs)
        self.port = str(Globals.currentPort)
        Globals.currentPort += 1
        self.server = server.carServer(self.port)

    def show(self):
        pass

    def move(self):
        # Control/ communication with Unity
        pass

    def update(self):
        pass

    def look(self):
        # UNITY?!?????????
        data = self.server.getData()
        if data == "kill":
            self.dead = True
        else:
            self.vision = data

    def think(self):
        max = 0
        maxIndex = 0
        decision = self.brain.feedForward(self.vision)

        for i in range(0, len(decision)):
            if decision[i] > max:
                max = decision[i]
                maxIndex = i

        self.server.sendData(decision)


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
        return self.fitness

    def crossover(self, parent2):
        child = Player()
        child.brain = self.brain.crossover(parent2.brain)
        child.brain.generateNetwork()
        return child
