import numpy as np
import sys
import csv
import json as js
import time
import datetime
import argparse


def sigmoid(z):
    return 1.0 / (1 + np.exp(-z))


def sigmoid_derivative(z):
    return sigmoid(z) * (1.0 - sigmoid(z))


def timer(start,end):
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))


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
    # print(modelOut)
    if output == "y":
        if len(args.output_file) >= 1:
            finalOutputFile = args.output_file
        else:
            finalOutputFile = 'output' + datetime.datetime.now().strftime("%d-%m-%Y %H.%M.%S")

        np.save(finalOutputFile + '.npy', modelOut)

        print("Saved data to file: ", finalOutputFile + '.npy')


        # f = open("TrainedModel.txt", "w")
        # f.writelines(str(modelOut))
        # f.close()
    elapsed_time = time.time() - start_time
    print("Runtime: ", str(datetime.timedelta(seconds=elapsed_time)))
    return modelOut


parser = argparse.ArgumentParser(description='trains and outputs a neural network given training data')
parser.add_argument('--training_data', type=str, default='TrainingData5.csv', help='csv file containing training data')
parser.add_argument('--iteration_count', type=int, default=10000, help='number of training cycles')
parser.add_argument('--output_file', type=str, default='', help='the name of the output file (will auto-generate if left blank)')
parser.add_argument('--hidden_layers', type=int, default=20, help='number of hidden layers to train on')
parser.add_argument('--learning_rate', type=float, default=0.1, help='learning rate')

args = parser.parse_args()

X = []
y = []

dir = args.training_data

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
        # print(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
        # print(row[10], row[11], row[12], row[13])

X = np.array(X, dtype=float)
y = np.array(y, dtype=float)

print(X)

n_hidden = args.hidden_layers
learning_rate = args.learning_rate
n_iter = args.iteration_count

start_time = time.time()

output = input("Output TrainedModel? (y/n) ")
model = train(X, y, n_hidden, learning_rate, n_iter)
