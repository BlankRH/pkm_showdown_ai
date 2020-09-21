import numpy as np
import random

def sigmoid(x):
    return 1.0/(1.0+np.exp(-x))

def sigmoidDerivative(x):
    return sigmoid(x)*(1-sigmoid(x))

class Network(object):

    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = []
        self.weights = []
        for i in len(sizes):
            self.weights.append(np.random.rand(len(sizes), ))

    def feedforward
