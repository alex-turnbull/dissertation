"""

A modified instance of a server that also runs, provides commands to Unity to handle certain events.
Currenetly just handling activation of the cars once the evolution has happened.

"""

import time
import zmq
import sys
# import predict as mlp
import numpy as np
import argparse
import threading


class EventServer:
    def __init__(self, port):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        binder = "tcp://*:"
        self.port = port
        binder += port
        self.socket.bind(binder)

        self.outputString = ""
        self.outputMsg = None

        # puts the server on a seperate thread
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        print("server on port", self.port, "RUNNING")
        pass

    # when required, get data from client, always empty/none
    def getData(self):
        message = self.socket.recv()

        return None

    # send the data when the Python wants to call an event to the Unity client
    def sendData(self, outData):
        self.outputString = ""

        self.outputString += outData

        self.outputString = bytes(self.outputString, 'utf-8')

        self.outputMsg = b"" + self.outputString
        self.socket.send(self.outputMsg)

