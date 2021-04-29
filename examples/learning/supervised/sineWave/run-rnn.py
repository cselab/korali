#!/usr/bin/env python3
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.patches as mpatch
from random import randrange
import time
import korali
k = korali.Engine()

# Setting random seed for reproducibility
np.random.seed(0xC0FFEE)

# Input parameters
Arch = "FNN"
#Arch = "RNN"
tf = 2.0 # Total Time
dt = 0.4 # Time Differential
B = 500 # Training Batch Size
s = 1.0  # Parameter for peak separation
w = np.pi # Parameter for wave speed
a = 1.0 # Scaling

# Transformation Function
def y(x, t): return np.sin(x * s +  w * t)  

X = np.random.uniform(0, np.pi*2, B)
T = np.arange(0, tf, dt)

# Providing inputs batches with varying timesequence lengths
trainingInputSetX = [ ]
trainingInputSetT = [ ]
for j, x in enumerate(X):
 trainingInputSetX.append([ ])
 trainingInputSetT.append([ ])
 for t in range(randrange(len(T)) + 1):
  trainingInputSetX[j].append([x])
  trainingInputSetT[j].append([T[t]])

# Giving the solution for the last time step of each batch sequence
trainingSolutionSet = [ ]
for j, x in enumerate(X):
 t = trainingInputSetT[j][-1][0]
 trainingSolutionSet.append([ y(x, t) ]) 

### Defining a learning problem to infer values of sin(x,t)

e = korali.Experiment()
e["Problem"]["Type"] = "Supervised Learning"
e["Problem"]["Max Timesteps"] = len(T)
e["Problem"]["Training Batch Size"] = B
e["Problem"]["Inference Batch Size"] = B
e["Problem"]["Input"]["Data"] = trainingInputSetX
e["Problem"]["Input"]["Size"] = 1
e["Problem"]["Solution"]["Data"] = trainingSolutionSet
e["Problem"]["Solution"]["Size"] = 1
 
### Using a neural network solver (deep learning) for inference

e["Solver"]["Type"] = "Learner/DeepSupervisor"
e["Solver"]["Loss Function"] = "Mean Squared Error"
e["Solver"]["Steps Per Generation"] = 20
e["Solver"]["Optimizer"] = "AdaBelief"
e["Solver"]["Learning Rate"] = 0.0001

### Defining the shape of the neural network

e["Solver"]["Neural Network"]["Engine"] = "OneDNN"

e["Solver"]["Neural Network"]["Hidden Layers"][0]["Type"] = "Layer/Recurrent/GRU"
e["Solver"]["Neural Network"]["Hidden Layers"][0]["Depth"] = 1
e["Solver"]["Neural Network"]["Hidden Layers"][0]["Output Channels"] = 32

### Configuring output 

e["Console Output"]["Frequency"] = 1
e["File Output"]["Enabled"] = False

### Training the neural network

e["Solver"]["Termination Criteria"]["Max Generations"] = 100
e["Random Seed"] = 0xC0FFEE
k.run(e)

### Obtaining inferred results from the NN and comparing them to the actual solution

X = np.random.uniform(0, np.pi*2, B)

# Providing inputs batches with varying timesequence lengths
testInputSetX = [ ]
testInputSetT = [ ]
for j, x in enumerate(X):
 testInputSetX.append([ ])
 testInputSetT.append([ ])
 for t in range(randrange(len(T)) + 1):
  testInputSetX[j].append([x])
  testInputSetT[j].append([T[t]])

# Giving the solution for the last time step of each batch sequence
testSolutionSet = [ ]
for j, x in enumerate(X):
 t = testInputSetT[j][-1][0]
 testSolutionSet.append([ y(x, t) ]) 
testInferredSet = e.getEvaluation(testInputSetX) 

### Calc MSE on test set

mse = np.mean((np.array(testInferredSet) - np.array(testSolutionSet))**2)
print("MSE on test set: {}".format(mse))

### Plotting inferred result
cmap = cm.get_cmap(name='Set1')
xAxis = [ x[-1][0] for x in testInputSetX ]

for i, x in enumerate(testInputSetX):
 t = len(x)-1  
 plt.plot(xAxis[i], testSolutionSet[i], "o", color=cmap(t))
 plt.plot(xAxis[i], testInferredSet[i], "x", color=cmap(t))
 
labelPatches = [ ] 
for i, t in enumerate(T):
 labelPatches.append(mpatch.Patch(color=cmap(i), label='Seq Length: ' + str(i+1)))
plt.legend(handles=labelPatches, loc='lower right')

### Plotting Results

plt.show()
