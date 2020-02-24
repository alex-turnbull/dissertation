import numpy as np
import sklearn
from sklearn import datasets as ds
import sys
import csv
import json as js
import time
from datetime import timedelta


def sigmoid(z):
    return 1.0 / (1 + np.exp(-z))


def sigmoid_derivative(z):
    return sigmoid(z) * (1.0 - sigmoid(z))


def timer(start,end):
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))


def train(X, y, n_hidden, learning_rate, n_iter):
    m, n_input = X.shape
    weight1 = np.random.randn(n_input, n_hidden)
    b1 = np.zeros((1, n_hidden))
    weight2 = np.random.randn(n_hidden, 4)
    b2 = np.zeros((1, 1))
    for i in range(1, n_iter+1):
        Z2 = np.matmul(X, weight1) + b1
        A2 = sigmoid(Z2)
        Z3 = np.matmul(A2, weight2) + b2
        A3 = Z3
        dZ3 = A3 - y
        dW2 = np.matmul(A2.T, dZ3)
        db2 = np.sum(dZ3, axis=0, keepdims=True)
        dZ2 = np.matmul(dZ3, weight2.T) * sigmoid_derivative(Z2)
        dW1 = np.matmul(X.T, dZ2)
        db1 = np.sum(dZ2, axis=0)
        weight2 = weight2 - learning_rate * dW2 / m
        b2 = b2 - learning_rate * db2 / m
        weight1 = weight1 - learning_rate * dW1 / m
        b1 = b1 - learning_rate * db1 / m
        if i % 100 == 0:
            cost = np.mean((y-A3) ** 2)
            print("Input : \n" + str(X))
            print("Actual Output: \n" + str(y))
            print("Predicted Output: \n" + str(A3))
            print('Iteration %i, training loss: %f, Accuracy: %f' % (i, cost, (100-(cost*100))))
    np.set_printoptions(threshold=sys.maxsize)
    modelOut = {'weight1': weight1, 'b1': b1, 'weight2': weight2, 'b2': b2}
    #print(modelOut)
    if output == "y":
        np.save('TrainedModel5.npy', modelOut)
        #f = open("TrainedModel.txt", "w")
        #f.writelines(str(modelOut))
        #f.close()
    elapsed_time = time.time() - start_time
    print("Runtime: ", str(timedelta(seconds=elapsed_time)))
    return modelOut

X = []
y = []

dir = str(sys.argv[1])

with open(dir) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    for row in readCSV:
        X.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]])
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

X = np.array(X, dtype=float)
y = np.array(y, dtype=float)

print(X)

n_hidden = 3
learning_rate = 0.05
n_iter = int(sys.argv[2])

start_time = time.time()

output = input("Output TrainedModel? (y/n) ")
model = train(X, y, n_hidden, learning_rate, n_iter)

def predict(x, model):
    W1 = model['weight1']
    b1 = model['b1']
    W2 = model['weight2']
    b2 = model['b2']
    A2 = sigmoid(np.matmul(x, W1) + b1)
    A3 = np.matmul(A2, W2) + b2
    return A3

x =[]
x.append([0.9845487, 270.8687, 1.0, 0.0, 2.940531, 0.5767461, 0.5667362, 5.482859, 0.6581876, 0.646764])
x = np.array(x, dtype=float)