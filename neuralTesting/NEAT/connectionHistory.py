
fromNode = None
toNode = None
innovationNumber = None

innovationNumbers = []

class connectionHistory:
    def __init__(self, fromNode, to, inno, innovationNos):
        self.fromNode = fromNode
        self.toNode = to
        self.innovationNumber = inno
        self.innovationNumbers = list(innovationNos.clone())

    def matches(self, genome, fromN, to):
        if genome.genes.count() == len(self.innovationNumbers):
            if fromN.number == self.fromNode and to.number == self.toNode:
                for i in range(0, genome.genes.count()):
                    if not self.innovationNumbers.__contains__(genome.genes.get(i).innovationNo):
                        return False

                return True
            return False
