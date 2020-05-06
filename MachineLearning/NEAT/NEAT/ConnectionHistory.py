"""

stores the history of how previous brains were configured

"""

fromNode = None
toNode = None
innovationNumber = None
innovationNumbers = []


class ConnectionHistory:
    def __init__(self, fromNode, to, inno, innovationNos):
        self.fromNode = fromNode
        self.toNode = to
        self.innovationNumber = inno
        self.innovationNumbers = innovationNos

    # compares whether the genome matches the original genome and the connection is between the same nodes
    def matches(self, genome, fromN, to):
        # if number of connection are different, then genomes aren't the same
        if len(genome.genes) == len(self.innovationNumbers):
            if fromN.number == self.fromNode and to.number == self.toNode:
                # check if all innovation numbers match
                for i in range(0, len(genome.genes)):
                    if not self.innovationNumbers.__contains__(genome.genes.get(i).innovationNo):
                        return False

                return True
            return False
