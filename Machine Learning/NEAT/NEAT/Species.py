import random


class Species:
    players = []
    bestFitness = 0
    champ = None
    averageFitness = 0
    staleness = 0
    rep = None

    excessCoeff = 1
    weightDiffCoeff = 0.5
    combatbilityThreshold = 3

    def __init__(self, p):
        self.players.append(p)

        self.bestFitness = p.fitness
        self.rep = p.brain.clone()
        self.champ = p.cloneForReplay()

    def sameSpecies(self, g):
        compatibility = 0
        excessAndDisjoint = self.getExcessDisjoint(g, self.rep)
        averageWeightDiff = self.averageWeightDiff(g, self.rep)

        largeGenomeNormaliser = len(g.genes) - 20
        if largeGenomeNormaliser < 1:
            largeGenomeNormaliser = 1

        compatibility = (self.excessCoeff * excessAndDisjoint/largeGenomeNormaliser) + (self.weightDiffCoeff * averageWeightDiff)
        return self.combatbilityThreshold > compatibility

    def addToSpecies(self, p):
        self.players.append(p)

    def getExcessDisjoint(self, brain1, brain2):
        matching = 0
        for i in range(0, len(brain1.genes)):
            for j in range(0, len(brain2.genes)):
                if brain1.genes[i].innovationNo == brain2.genes[j].innovationNo:
                    matching += 1
                    break

        return len(brain1.genes) + len(brain2.genes) - 2*matching

    def averageWeightDiff(self, brain1, brain2):
        if len(brain1.genes) == 0 or len(brain2.genes) == 0:
            return 0

        matching = 0
        totalDiff = 0
        for i in range(0, len(brain1.genes)):
            for j in range(0, len(brain2.genes)):
                if brain1.genes[i].innovationNo == brain2.genes[j].innovationNo:
                    matching += 1
                    totalDiff += abs(brain1.genes[i].weight - brain2.genes[j].weight)
                    break

        if matching == 0:
            return 100

        return totalDiff/matching

    def sortSpecies(self):
        temp = []

        i = 0 - 1
        while len(self.players) > 0:
            i += 1
            max = 0
            maxIndex = 0
            for j in range(0, len(self.players)):
                if self.players[j].fitness > max:
                    max = self.players[j].fitness
                    maxIndex = j
            temp.append(self.players[maxIndex])
            self.players.pop(maxIndex)
            i -= 1

        self.players = temp
        if len(self.players) == 0:
            print("Fucking")
            self.staleness = 200
            return

        if self.players[0].fitness > self.bestFitness:
            self.staleness = 0
            self.bestFitness = self.players[0].fitness
            self.rep = self.players[0].brain.clone()
            self.champ = self.players[0].cloneForReplay()
        else:
            self.staleness += 1

    def setAverage(self):
        sum = 0
        for i in range(0,len(self.players)):
            sum += self.players[i].fitness

        self.averageFitness = sum/len(self.players)

    def giveMeBaby(self, innovationHistory):
        baby = None
        if random.uniform(0, 1) < 0.25:
            baby = self.selectPlayer().clone()
        else:
            parent1 = self.selectPlayer()
            parent2 = self.selectPlayer()

            if parent1.fitness < parent2.fitness:
                baby = parent2.crossover(parent1)
            else:
                baby = parent1.crossover(parent2)

        baby.brain.mutate(innovationHistory)
        return baby

    def selectPlayer(self):
        fitnessSum = 0
        for i in range(0,len(self.players)):
            fitnessSum += self.players[i].fitness

        rand = random.uniform(0, fitnessSum)
        runningSum = 0

        for i in range(0,len(self.players)):
            runningSum += self.players[i].fitness
            if runningSum > rand:
                return self.players[i]

        return self.players[0]

    def cull(self):
        if len(self.players) > 2:
            i = int((len(self.players)/2) - 1)
            while i <= len(self.players):
                i += 1
                if i == len(self.players):
                    break
                # for i in range(int(len(self.players)/2), len(self.players)):
                self.players.pop(i)
                i -= 1

    def fitnessSharing(self):
        for i in range(0, len(self.players)):
            self.players[i].fitness /= len(self.players)