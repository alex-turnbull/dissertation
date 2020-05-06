"""

players are grouped into species based on similar brains

"""

import random


class Species:
    players = []
    bestFitness = 0
    champ = None
    averageFitness = 0
    staleness = 0
    rep = None

    # compatibility testing coefficients
    excessCoeff = 1
    weightDiffCoeff = 0.5
    combatbilityThreshold = 3

    def __init__(self, p):
        self.players.append(p)

        self.bestFitness = p.fitness
        self.rep = p.brain.clone()
        self.champ = p.cloneForReplay()

    # returns whether the parameter genome is in this species
    def sameSpecies(self, g):
        excessAndDisjoint = self.getExcessDisjoint(g, self.rep)
        averageWeightDiff = self.averageWeightDiff(g, self.rep)

        largeGenomeNormaliser = len(g.genes) - 20
        if largeGenomeNormaliser < 1:
            largeGenomeNormaliser = 1

        compatibility = (self.excessCoeff * excessAndDisjoint/largeGenomeNormaliser) + (self.weightDiffCoeff * averageWeightDiff)
        return self.combatbilityThreshold > compatibility

    # add a player to this group of species
    def addToSpecies(self, p):
        self.players.append(p)

    # returns the number of genes that don't match
    def getExcessDisjoint(self, brain1, brain2):
        matching = 0
        for i in range(0, len(brain1.genes)):
            for j in range(0, len(brain2.genes)):
                if brain1.genes[i].innovationNo == brain2.genes[j].innovationNo:
                    matching += 1
                    break

        return len(brain1.genes) + len(brain2.genes) - 2*matching

    # returns the average weight difference between matching genes in the input genomes
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

    # organises players in species internally based on fitness
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

    # produce a child from players in this species
    def produceChild(self, innovationHistory):
        if random.uniform(0, 1) < 0.25:
            child = self.selectPlayer().clone()
        else:
            parent1 = self.selectPlayer()
            parent2 = self.selectPlayer()

            if parent1.fitness < parent2.fitness:
                child = parent2.crossover(parent1)
            else:
                child = parent1.crossover(parent2)

        child.brain.mutate(innovationHistory)
        return child

    # selects a player bases on its fitness
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

    # kill bottom half of species
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
