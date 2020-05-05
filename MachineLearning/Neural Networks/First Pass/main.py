"""
First pass Neural Network development

With supporting content taken from:
https://towardsdatascience.com/how-to-build-your-own-neural-network-from-scratch-in-python-68998a08e4f6

"""


import numpy as np
import argparse

#X = np.array(([0, 0, 1], [0, 1, 1], [1, 0, 1], [1, 1, 1]), dtype=float)
#y = np.array(([0], [1], [1], [1]), dtype=float)

import sys
import csv

X = []
y = []

# File parser to read all of the training data
dir = str(sys.argv[1])

with open(dir) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    for row in readCSV:
        X.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]])
        # Convert booleans to int for clarity
        if row[10] == "True":
            row[10] = 1
        else:
            row[10] = 0
        if row[11] == "True":
            row[11] = 1
        else:
            row[11] = 0
        if row[12] == "True":
            row[12] = 1
        else:
            row[12] = 0
        if row[13] == "True":
            row[13] = 1
        else:
            row[13] = 0
        y.append([row[10], row[11], row[12], row[13]])
        #print(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
        #print(row[10], row[11], row[12], row[13])

# Create NumPy array for the use of the Neural Network
X = np.array(X, dtype=float)
y = np.array(y, dtype=float)

# Supporting functions
def sigmoid(t):
    return 1 / (1 + np.exp(-t))


def sigmoid_derivative(p):
    return p * (1 - p)


class NeuralNetwork:
    def __init__(self, x, y):
        self.input = x
        self.weights1 = np.random.rand(self.input.shape[1], 10)
        self.weights2 = np.random.rand(10, 4)
        self.y = y
        self.output = np.zeros(y.shape)

    def feedforward(self):
        self.layer1 = sigmoid(np.dot(self.input, self.weights1))
        self.layer2 = sigmoid(np.dot(self.layer1, self.weights2))
        return self.layer2

    def backprop(self):
        d_weights2 = np.dot(self.layer1.T, 2 * (self.y - self.output) * sigmoid_derivative(self.output))
        d_weights1 = np.dot(self.input.T, np.dot(2 * (self.y - self.output) * sigmoid_derivative(self.output), self.weights2.T) * sigmoid_derivative(self.layer1))

        self.weights1 += d_weights1
        self.weights2 += d_weights2

    def train(self, X, y):
        self.output = self.feedforward()
        self.backprop()


# Main Program, runs the Network based on the given data for a set time
NN = NeuralNetwork(X, y)
for i in range(int(sys.argv[2])):
    if i % 100 == 0:
        print("for iteration # " + str(i) + "\n")
        print("Input : \n" + str(X))
        print("Actual Output: \n" + str(y))
        print("Predicted Output: \n" + str(NN.feedforward()))
        print("Loss: \n" + str(np.mean(np.square(y - NN.feedforward()))))
        print("\n")

    NN.train(X, y)
