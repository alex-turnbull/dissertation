"""

'server' implementation to handle data for a player between Unity and here

"""

import zmq
import threading


class CarServer:
    def __init__(self, port):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        binder = "tcp://*:"
        self.port = port
        binder += port
        self.socket.bind(binder)

        self.mostRecentLookData = [0] * 10
        self.mostRecentOutData = [0] * 4
        self.readyToSend = False
        self.send = False
        self.outputString = ""
        self.outputMsg = None

        self.dead = False

        self.currentScore = 0

        # run on its own thread
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while True:
            # receives the input from the unity client
            message = self.socket.recv()
            print("Received request: %s" % message, "On port:", self.port)

            # formats the message through string manipulation
            msgFormat = str(message)
            msgFormat = msgFormat[2:]
            msgFormat = msgFormat[:-1]
            msgFormat = msgFormat.split(";")
            command = msgFormat[0]
            # print("Format Msg: %s" % msgFormat)

            self.mostRecentLookData = [msgFormat[1], msgFormat[2], msgFormat[3], msgFormat[4], msgFormat[5], msgFormat[6],
                             msgFormat[7], msgFormat[8], msgFormat[9], msgFormat[10]]

            # handle death
            if msgFormat[11] == "False":
                self.dead = True
            else:
                self.dead = False

            # retrieve fitness
            self.currentScore = float(msgFormat[12])

            self.outputString = ""

            # output the data produced by the NEAT system
            for item in self.mostRecentOutData:
                self.outputString = self.outputString + str(item) + ";"

            self.outputString = self.outputString[:-1]

            self.outputString = bytes(self.outputString, 'utf-8')

            #  Send reply back to client
            self.outputMsg = b"" + self.outputString

            # print("Sending Output: %s" % self.outputString)
            self.socket.send(self.outputMsg)

    # function player calls to get latest data
    def getData(self):
        return self.mostRecentLookData

    def sendData(self, outData):
        pass

    def getFinalScore(self):
        # self.context.destroy()
        # self.socket.close()
        # print("Server on port", self.port, "CLOSING")
        return self.currentScore

