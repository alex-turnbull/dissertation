
class Genome:
    def __init__(self, inNum, out):
        self.inputs = inNum
        self.inputs = out
        self.layers = 2
        self.nextNode = 0

        for i in range(0,self.inputs):
            self.nodes