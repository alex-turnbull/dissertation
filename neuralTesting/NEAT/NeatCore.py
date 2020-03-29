import NEAT.Population as Population
import NEAT.Player as Player

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

def setup():
    # Game Setup, I mean most is done in Unity so gotta craft this into
    # my convoluted shit show of a project lmao

    # Run the server and send some sort of command to call a setup function in Unity??

    # Server might have to be jacked up to receive EVERY car, unless there's
    # a different server for each car :think:

    pop = Population.Population(500)
    humanPlayer = Player.Player()
