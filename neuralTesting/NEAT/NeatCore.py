import Population as Population
import Player as Player
import argparse

nextConnectionNo = 1000
pop = None
speed = 60

showBest = True
runBest = False
humanPlaying = False

humanPlayer = None

runThroughSpecies = False
upToSpecies = 0
speciesChamp = False

showBrain = False

showBestEachGen = False
upToGen = 0
genPlayerTemp = None

showNothing = False


def setup(population):
    # Game Setup, I mean most is done in Unity so gotta craft this into
    # my convoluted shit show of a project lmao

    # Run the server and send some sort of command to call a setup function in Unity??

    # Server might have to be jacked up to receive EVERY car, unless there's
    # a different server for each car :think:

    pop = Population.Population(population)
    humanPlayer = Player.Player()


parser = argparse.ArgumentParser(description='The main shit')
parser.add_argument('--population_size', type=int, default='100', help='Number of agents to generate')

args = parser.parse_args()

setup(args.population_size)
