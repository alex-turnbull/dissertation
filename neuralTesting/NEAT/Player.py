import Genome as Genome

# I think I've somehow got to create a connection between this
# and an entity in unity :think:
# YIKES

# Maybe this can store some sort of reference ID, and then can poll unity for
# it's respective reference for the values

class Player:
    fitness = None
    brain = None
    vision = [None]*8  # ALL inputs from Unity
    decision = [None]*4  # Output buttons
    unadjustedFitness = None
    lifespan = 0
    bestscore = 0
    dead = None
    score = None
    gen = 0

    genomeInputs = 13
    genomeOutputs = 4

    def __init__(self):
        brain = Genome.Genome(self.genomeInputs, self.genomeOutputs)

    def show(self):
        pass

    def move(self):
        # Control/ communication with Unity
        pass

    def update(self):
        # Unity????????
        pass

    def look(self):
        # UNITY?!?????????
        pass

    def think(self):
        max = 0
        maxIndex = 0
        decision = self.brain.feedForward(self.vision)

        for i in range(0, len(decision)):
            if decision[i] > max:
                max = decision[i]
                maxIndex = i

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
        pass

    def crossover(self, parent2):
        child = Player()
        child.brain = self.brain.crossover(parent2.brain)
        child.brain.generateNetwork()
        return child
