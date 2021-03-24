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

### Loading previous run (if exist)

found = e.loadState('_result_sin/latest')

# If not found, we run first 5 generations.
if (found == False):
  print('------------------------------------------------------')
  print('Running first 5 generations...')
  print('------------------------------------------------------')
  e["Solver"]["Termination Criteria"]["Max Generations"] = 5

# If found, we continue with the next 5 generations.
if (found == True):
  print('------------------------------------------------------')
  print('Running last 10 generations...')
  print('------------------------------------------------------')
  e["Solver"]["Termination Criteria"]["Max Generations"] = 10

### Configuring problem
 
e["Problem"]["Type"] = "Supervised Learning"
e["Problem"]["Inputs"] = trainingInputSet
e["Problem"]["Solution"] = trainingSolutionSet

### Using a neural network solver (deep learning) for inference

e["Solver"]["Type"] = "Learner/DeepSupervisor"
e["Solver"]["Loss Function"] = "Mean Squared Error"
e["Solver"]["Steps Per Generation"] = 5
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
e["Random Seed"] = 0xC0FFEE

### Setting file output configuration

e["File Output"]["Path"] = "_result_sin"
e["File Output"]["Enabled"] = True
e["File Output"]["Frequency"] = 1
 
k.run(e)