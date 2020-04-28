import time
import zmq
import sys
import predict as mlp
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Runs a server for communicating data between Unity and ML')
parser.add_argument('--delay_time', type=float, default=0.5, help='adds a delay between data communication')
parser.add_argument('--model_directory', type=str, default='TrainedModel5.npy', help='the directory of the trained model')

args = parser.parse_args()

delayTime = float(args.delay_time)
modelDir = args.model_directory
model = np.load(modelDir)

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    message = socket.recv()
    print("Received request: %s" % message)

    #  Do some 'work'.
    time.sleep(delayTime/2)

    msgFormat = str(message)
    msgFormat = msgFormat[2:]
    msgFormat = msgFormat[:-1]
    msgFormat = msgFormat.split(";")
    #print("Format Msg: %s" % msgFormat)

    X = [
        [msgFormat[0], msgFormat[1], msgFormat[2], msgFormat[3], msgFormat[4], msgFormat[5], msgFormat[6], msgFormat[7],
         msgFormat[8], msgFormat[9]]
        ]
    X = np.array(X, dtype=float)

    predictOutput = mlp.predict(X, model)

    outputString = ""
    a = predictOutput.reshape(1, 4)
    for x in np.nditer(a):
        outputString = outputString + str(x) + ";"

    outputString = outputString[:-1]
    outputString = bytes(outputString, 'utf-8')
    #  Send reply back to client
    #  In the real world usage, after you finish your work, send your output here
    print("Sending Output: %s" % outputString)
    outputMsg = b"" + outputString
    socket.send(outputMsg)
    time.sleep(delayTime / 2)