#!/usr/bin/env python3
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import time
import korali
k = korali.Engine()

scaling = 5.0
np.random.seed(0xC0FFEE)

# The input set has scaling and a linear element to break symmetry
trainingInputSet = np.random.uniform(0, 2 * np.pi, 500)
trainingSolutionSet = np.tanh(np.exp(np.sin(trainingInputSet))) * scaling 

trainingInputSet = [ [ i ] for i in trainingInputSet.tolist() ]
trainingSolutionSet = [ [ i ] for i in trainingSolutionSet.tolist() ]

### Defining a learning problem to infer values of sin(x)

e = korali.Experiment()
e["Problem"]["Type"] = "Supervised Learning"

e["Problem"]["Inputs"] = trainingInputSet
e["Problem"]["Solution"] = trainingSolutionSet

### Using a neural network solver (deep learning) for inference

e["Solver"]["Type"] = "Learner/DeepSupervisor"
e["Solver"]["Loss Function"] = "Mean Squared Error"
e["Solver"]["Steps Per Generation"] = 200
e["Solver"]["Optimizer"] = "AdaBelief"
e["Solver"]["Learning Rate"] = 0.05

### Defining the shape of the neural network

e["Solver"]["Neural Network"]["Layers"][0]["Type"] = "Layer/Dense"
e["Solver"]["Neural Network"]["Layers"][0]["Node Count"] = 1
e["Solver"]["Neural Network"]["Layers"][0]["Activation Function"]["Type"] = "Elementwise/Linear"

e["Solver"]["Neural Network"]["Layers"][1]["Type"] = "Layer/Dense"
e["Solver"]["Neural Network"]["Layers"][1]["Node Count"] = 32
e["Solver"]["Neural Network"]["Layers"][1]["Activation Function"]["Type"] = "Elementwise/Tanh"

e["Solver"]["Neural Network"]["Layers"][2]["Type"] = "Layer/Dense"
e["Solver"]["Neural Network"]["Layers"][2]["Node Count"] = 32
e["Solver"]["Neural Network"]["Layers"][2]["Activation Function"]["Type"] = "Elementwise/Tanh"

e["Solver"]["Neural Network"]["Layers"][3]["Type"] = "Layer/Dense"
e["Solver"]["Neural Network"]["Layers"][3]["Node Count"] = 1
e["Solver"]["Neural Network"]["Layers"][3]["Activation Function"]["Type"] = "Elementwise/Linear"

e["Console Output"]["Frequency"] = 1
e["File Output"]["Enabled"] = False
e["Random Seed"] = 0xC0FFEE

### Training the neural network

e["Solver"]["Termination Criteria"]["Max Generations"] = 10
k.run(e)

### Obtaining inferred results from the NN and comparing them to the actual solution

testInputSet = np.random.uniform(0, 2 * np.pi, 100)
testInputSet = [[x] for x in testInputSet.tolist()]

testInferredSet = [ e.getEvaluation(x) for x in testInputSet ]
testGradientSet = [ e.getGradients(x) for x in testInferredSet ]
testOutputSet = np.tanh(np.exp(np.sin(testInputSet))) * scaling 


### Calc MSE on test set

mse = np.mean((np.array(testInferredSet) - np.array(testOutputSet))**2)
print("MSE on test set: {}".format(mse))

### Plotting Results

plt.plot(testInputSet, testOutputSet, "o")
plt.plot(testInputSet, testInferredSet, "x")
#plt.plot(testInferredSet, testGradientSet, "*")
plt.show()
