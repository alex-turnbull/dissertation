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

#parser = argparse.ArgumentParser(description='Runs a server for communicating data between Unity and ML')
#parser.add_argument('--delay_time', type=float, default=0.5, help='adds a delay between data communication, default 0.5')
#parser.add_argument('--model_directory', type=str, default='TrainedModel5.npy', help='the directory of the trained model, default TrainedModel5')
#parser.add_argument('--server_port', type=str, help='port the server should run on')

#args = parser.parse_args()

delayTime = float(0.5)
modelDir = 'TrainedModel5.npy'
# model = np.load(modelDir)

class carServer:
    def __init__(self, port):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        binder = "tcp://*:"
        self.port = port
        binder += port
        self.socket.bind(binder)

        self.lookData = [0] * 6
        self.outData = [0] * 4
        self.readyToSend = False
        self.send = False
        self.outputString = ""
        self.outputMsg = None


        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        print("server on port", self.port, "RUNNING")
        while True:
            #  Wait for next request from client
            message = self.socket.recv()
            print("Received request: %s" % message, "On port:", self.port)

            #  Do some 'work'.
            time.sleep(delayTime/2)

            msgFormat = str(message)
            msgFormat = msgFormat[2:]
            msgFormat = msgFormat[:-1]
            msgFormat = msgFormat.split(";")
            #print("Format Msg: %s" % msgFormat)

            self.lookData = [msgFormat[0], msgFormat[1], msgFormat[2], msgFormat[3], msgFormat[4], msgFormat[5]]
            """
            X = [
                [msgFormat[0], msgFormat[1], msgFormat[2], msgFormat[3], msgFormat[4], msgFormat[5], msgFormat[6], msgFormat[7],
                 msgFormat[8], msgFormat[9]]
                ]
            X = np.array(X, dtype=float)

            
            predictOutput = mlp.predict(X, model)
            """
            outputString = ""
            # a = predictOutput.reshape(1, 4)
            # for x in np.nditer(a):
                # outputString = outputString + str(x) + ";"

            while not self.readyToSend:
                if self.send:
                    print("Sending Output: %s" % self.outputString)
                    self.socket.send(self.outputMsg)
                    self.send = False
                    time.sleep(delayTime / 2)
                    break

    def getData(self):
        return self.lookData

    def sendData(self, outData):
        self.outputString = ""

        for item in outData:
            self.outputString = self.outputString + str(item) + ";"

        self.outputString = self.outputString[:-1]
        self.outputString = bytes(self.outputString, 'utf-8')

        #  Send reply back to client
        #  In the real world usage, after you finish your work, send your output here

        self.outputMsg = b"" + self.outputString

        self.send = True

