"""
The main process to run and handle the NEAT evolutionary process.

Written in Python based on a Processing template available at:
https://github.com/Code-Bullet/NEAT_Template/tree/master/TemplateNeat

"""

import Population as Population
import Player as Player
import argparse
import time


def setup(population):
    print("About to start training with population size of", population)
    time.sleep(2)

    pop = Population.Population(population)
    # humanPlayer = Player.Player()
    while True:
        tick(pop)


def tick(pop):
    if not pop.done():
        pop.updateAlive()
    else:
        pop.naturalSelection()


# Main program, this process gets called from command line in Unity
parser = argparse.ArgumentParser(description='The main process to initate NEAT')
parser.add_argument('--population_size', type=int, default='10', help='Number of agents to generate')

args = parser.parse_args()

setup(args.population_size)
