
class connectionHistory:
    def __init__(self, fromInt, to, inno, innovationNos):
        self.fromNode = fromInt
        self.toNode = to
        self.innovationNumber = inno
        self.innovationNumbers = list(innovationNos.clone())

    def matches(self, genome, fromN, to):
        if genome.genes.count() == self.innovationNumbers.count():
            if fromN.number == self.fromNode and to.number == self.toNode:
                for i in range(0, genome.genes.count()):
                    if not self.innovationNumbers.__contains__(genome.genes.get(i).innovationNo):
                        return False

                return True
            return False
