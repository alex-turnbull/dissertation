"""

Handles the population of agents undergoing the NEAT process

"""

import math

import Globals as globals
import Player as Player
import Species as Species
import EventServer as servers
import Server as Server


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

    server = None
    serverPort = "6020"

    serverList = []

    def __init__(self, size):
        self.server = servers.EventServer(self.serverPort)  # create event server
        for i in range(0, size):
            # create given number of players and servers
            self.pop.append(Player.Player())
            port = str(globals.currentPort)
            globals.currentPort += 1
            self.pop[i].server = Server.CarServer(port)
            self.serverList.append(self.pop[i].server)
            self.pop[i].brain.generateNetwork()
            self.pop[i].brain.mutate(self.innovationHistory)

    # perform the update loop for those still alive
    def updateAlive(self):
        for i in range(0,len(self.pop)):
            if not self.pop[i].dead:
                self.pop[i].look()
                self.pop[i].think()
                self.pop[i].update()

    # checks if entire population is dead / ready for evolution
    def done(self):
        for i in range(0, len(self.pop)):
            if not self.pop[i].dead:
                return False

        return True

    # sets the best player in the population for reference
    def setBestPlayer(self):
        tempBest = self.species[0].players[0]
        tempBest.gen = self.gen

        if tempBest.score > self.bestScore:
            self.genPlayers.append(tempBest.cloneForReplay())
            print("old best:", self.bestScore)
            print("new best:", tempBest.score)
            self.bestScore = tempBest.score
            self.bestPlayer = tempBest.cloneForReplay()

    # Handle the population and produces a new generation
    def naturalSelection(self):
        self.calculateFitness()  # calculate fitness for all
        self.speciate()  # separate population into species
        self.sortSpecies()  # sort species into fitness rank order
        if self.massExtinctionEvent:
            self.massExtinction()
            self.massExtinctionEvent = False

        self.cullSpecies()  # remove bottom half of species
        self.setBestPlayer()
        self.killStaleSpecies()  # remove species not improving
        self.killBadSpecies()  # remove bad species

        print("Generation", self.gen, "Number of mutations", len(self.innovationHistory), "Species " + str(len(self.species)), "<<<<<<<<<<<<<<<<<<<<<<<<<<")

        averageSum = self.getAvgFitnessSum()
        children = []
        print("Species:")
        for j in range(0, len(self.species)):
            print("best unadjusted fitness: ", self.species[j].bestFitness)
            for i in range(0, len(self.species[j].players)):
                print("player " + str(i), "fitness: " + str(self.species[j].players[i].fitness), "score " + str(self.species[j].players[i].score), ' ')
            print(" ")
            # children.append(self.species[j].champ.cloneForReplay())

            # calculate the number of children required
            NoOfChildren = math.floor(self.species[j].averageFitness/averageSum * len(self.pop)) - 1
            for i in range(0, NoOfChildren):
                children.append(self.species[j].produceChild(self.innovationHistory))

        while len(children) < len(self.pop):
            children.append(self.species[0].produceChild(self.innovationHistory))

        self.pop.clear()
        self.pop = children
        self.gen += 1

        # Assign the server for the cars to communicate on with NEAT
        for i in range(0, len(self.pop)):
            self.pop[i].brain.generateNetwork()
            self.pop[i].server = self.serverList[i]

        # Reactivate Unity Cars
        self.server.getData()
        self.server.sendData("respawn")

    # separate population into species
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

    # calculate fitness of all players
    def calculateFitness(self):
        for i in range(0, len(self.pop)):
            self.pop[i].calculateFitness()

    # sort species by fitness
    def sortSpecies(self):
        for s in self.species:
            s.sortSpecies()

        temp = []

        i  = 0 - 1
        while i+1 < len(self.species):
            i += 1
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

    # remove species not improving
    def killStaleSpecies(self):
        i = 2 - 1
        while i+1 <= len(self.species):
            i += 1
            if self.species[i].staleness >= 15:
                self.species.remove(i)
                i -= 1

    # remove bad species
    def killBadSpecies(self):
        averageSum = self.getAvgFitnessSum()

        i = 1 - 1
        while i+1 < len(self.species):
            i += 1
            if self.species[i].averageFitness/averageSum * len(self.pop) < 1:
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
        i = 5 - 1
        while i+1 <= len(self.species):
            i += 1
            self.species.pop(i)
            i -= 1
