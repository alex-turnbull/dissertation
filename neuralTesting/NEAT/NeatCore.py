import Population as Population
import Player as Player
import argparse
import time


def setup(population):
    # Game Setup, I mean most is done in Unity so gotta craft this into
    # my convoluted shit show of a project lmao

    # Run the server and send some sort of command to call a setup function in Unity??

    # Server might have to be jacked up to receive EVERY car, unless there's
    # a different server for each car :think:

    print("About to start training with population size of", population)
    time.sleep(2)

    pop = Population.Population(population)
    # humanPlayer = Player.Player()
    while True:
        tick(pop)

def tick(pop):
    pop.updateAlive()


parser = argparse.ArgumentParser(description='The main shit')
parser.add_argument('--population_size', type=int, default='10', help='Number of agents to generate')

args = parser.parse_args()

setup(args.population_size)
