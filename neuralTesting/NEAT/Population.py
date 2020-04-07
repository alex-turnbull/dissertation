import math

import tempGlobals as globals
import Player as Player
import Species as Species


class Population:
    pop = []
    bestPlayer = None
    bestScore = 0
    gen = 0
    innovationHistory = []
    genPlayers = []
    species = []

    massExtinctionEvent = False
    newStage = False

    def __init__(self, size):
        for i in range(0, size):
            self.pop.append(Player.Player())
            self.pop[i].brain.generateNetwork()
            self.pop[i].brain.mutate(self.innovationHistory)

    def updateAlive(self):
        for i in range(0,len(self.pop)):
            if not self.pop[i].dead:
                self.pop[i].look()
                self.pop[i].think()
                self.pop[i].update()
                if not globals.showNothing and (not globals.showBest or i == 0):
                    self.pop[i].show()


    def done(self):
        for i in range(0, len(self.pop)):
            if not self.pop[i].dead:
                return False

        return True

    def setBestPlayer(self):
        tempBest = self.species[0].players[0]
        tempBest.gen = self.gen

        if tempBest.score > self.bestScore:
            self.genPlayers.append(tempBest.cloneForReplay())
            print("old best:", self.bestScore)
            print("new best:", tempBest.score)
            self.bestScore = tempBest.score
            self.bestPlayer = tempBest.cloneForReplay()

    def naturalSelection(self):
        self.calculateFitness()
        self.speciate()
        self.sortSpecies()
        if self.massExtinctionEvent:
            self.massExtinction()
            self.massExtinctionEvent = False

        self.cullSpecies()
        self.setBestPlayer()
        self.killStaleSpecies()
        self.killBadSpecies()

        print("Generation", self.gen, "Number of mutations", len(self.innovationHistory), "Species " + str(len(self.species)), "<<<<<<<<<<<<<<<<<<<<<<<<<<")

        averageSum = self.getAvgFitnessSum()
        children = []
        print("Species:")
        for j in range(0, len(self.species)):
            print("best unadjusted fitness: ", self.species[j].bestFitness)
            for i in range(0, len(self.species[j].players)):
                print("player " + str(i), "fitness: " + str(self.species[j].players[i].fitness), "score " + str(self.species[j].players[i].score), ' ')
            print(" ")
            children.append(self.species[j].champ.cloneForReplay())

            NoOfChildren = math.floor(self.species[j].averageFitness/averageSum * len(self.pop))
            for i in range(0, NoOfChildren):
                children.append(self.species[j].giveMeBaby(self.innovationHistory))

        while len(children) < len(self.pop):
            children.append(self.species[0].giveMeBaby(self.innovationHistory))

        self.pop.clear()
        self.pop = children
        self.gen += 1
        for i in range(0, len(self.pop)):
            self.pop[i].brain.generateNetwork()

    def speciate(self):
        for s in self.species:
            s.players.clear()

        for i in range(0, len(self.pop)):
            speciesFound = False
            for s in self.species:
                if s.sameSpecies(self.pop[i].brain):
                    s.addToSpecies(self.pop[i])
                    speciesFound = True
                    break

            if not speciesFound:
                self.species.append(Species.Species(self.pop[i]))

    def calculateFitness(self):
        for i in range(0, len(self.pop)):
            self.pop[i].calculateFitness()


    def sortSpecies(self):
        for s in self.species:
            s.sortSpecies()

        temp = []
        for i in range(0, len(self.species)):
            max = 0
            maxIndex = 0
            for j in range(0, len(self.species)):
                if self.species[j].bestFitness > max:
                    max = self.species[j].bestFitness
                    maxIndex = j

            temp.append(self.species[maxIndex])
            self.species.pop(maxIndex)
            i -= 1

        self.species = temp

    def killStaleSpecies(self):
        for i in range(2, len(self.species)):
            if self.species[i].staleness >= 15:
                self.species.remove(i)
                i -= 1

    def killBadSpecies(self):
        averageSum = self.getAvgFitnessSum()

        for i in range(1, len(self.species)):
            if self.species[i].averageFitness/averageSum* len(self.pop) < 1:
                self.species.remove(i)
                i -= 1

    def getAvgFitnessSum(self):
        averageSum = 0
        for s in self.species:
            averageSum += s.averageFitness

        return averageSum

    def cullSpecies(self):
        for s in self.species:
            s.cull()
            s.fitnessSharing()
            s.setAverage()

    def massExtinction(self):
        for i in range(5, len(self.species)):
            self.species.pop(i)
            i -= 1
