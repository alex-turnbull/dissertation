#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq
import sys
# import predict as mlp
import numpy as np
import argparse
import threading

# parser = argparse.ArgumentParser(description='Runs a server for communicating data between Unity and ML')
# parser.add_argument('--delay_time', type=float, default=0.5, help='adds a delay between data communication, default 0.5')
# parser.add_argument('--model_directory', type=str, default='TrainedModel5.npy', help='the directory of the trained model, default TrainedModel5')
# parser.add_argument('--server_port', type=str, help='port the server should run on')

# args = parser.parse_args()

delayTime = float(0.5)
modelDir = 'TrainedModel5.npy'
# model = np.load(modelDir)


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

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while True:
            message = self.socket.recv()
            print("Received request: %s" % message, "On port:", self.port)

            msgFormat = str(message)
            msgFormat = msgFormat[2:]
            msgFormat = msgFormat[:-1]
            msgFormat = msgFormat.split(";")
            command = msgFormat[0]
            # print("Format Msg: %s" % msgFormat)

            self.mostRecentLookData = [msgFormat[1], msgFormat[2], msgFormat[3], msgFormat[4], msgFormat[5], msgFormat[6],
                             msgFormat[7], msgFormat[8], msgFormat[9], msgFormat[10]]

            if msgFormat[11] == "False":
                self.dead = True
            else:
                self.dead = False

            self.currentScore = float(msgFormat[12])

            # print("server on port", self.port, "RUNNING")
            self.outputString = ""

            for item in self.mostRecentOutData:
                self.outputString = self.outputString + str(item) + ";"

            self.outputString = self.outputString[:-1]

            self.outputString = bytes(self.outputString, 'utf-8')

            #  Send reply back to client
            #  In the real world usage, after you finish your work, send your output here

            self.outputMsg = b"" + self.outputString

            # print("Sending Output: %s" % self.outputString)
            self.socket.send(self.outputMsg)

    def getData(self):
        return self.mostRecentLookData

    def sendData(self, outData):
        pass

    def getFinalScore(self):
        self.context.destroy()
        self.socket.close()
        # print("Server on port", self.port, "CLOSING")
        return self.currentScore

