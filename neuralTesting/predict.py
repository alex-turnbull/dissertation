import numpy as np
import sys
import ast


def sigmoid(t):
    return 1 / (1 + np.exp(-t))


def sigmoid_derivative(p):
    return p * (1 - p)


def predict(x, model):
    W1 = model[()]['weight1']
    b1 = model[()]['b1']
    W2 = model[()]['weight2']
    b2 = model[()]['b2']
    A2 = sigmoid(np.matmul(x, W1) + b1)
    A3 = np.matmul(A2, W2) + b2
    return A3


"""
# modelDir = "TrainedModel.npy"
# modelDir = sys.argv[1]
# model = np.load(modelDir)
# X = []
# X.append([0.9845487, 270.8687, 1.0, 0.0, 2.940531, 0.5767461, 0.5667362, 5.482859, 0.6581876, 0.646764])
# X = np.array(X, dtype=float)
# print(X)
# print(model)
# print("Prediction: ",predict(X, model))
"""
