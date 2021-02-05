#!/usr/bin/env python3
import os
import sys
sys.path.append('./_model')
from env import *

####### Defining Korali Problem

import korali
k = korali.Engine()
e = korali.Experiment()

### Defining the Cartpole problem's configuration

e["Problem"]["Type"] = "Reinforcement Learning / Discrete"
e["Problem"]["Possible Actions"] = [ [ -10.0 ], [ 10.0 ] ]
e["Problem"]["Environment Function"] = env
e["Problem"]["Training Reward Threshold"] = 400
e["Problem"]["Policy Testing Episodes"] = 20
e["Problem"]["Actions Between Policy Updates"] = 5

e["Variables"][0]["Name"] = "Cart Position"
e["Variables"][0]["Type"] = "State"

e["Variables"][1]["Name"] = "Cart Velocity"
e["Variables"][1]["Type"] = "State"

e["Variables"][2]["Name"] = "Pole Angle"
e["Variables"][2]["Type"] = "State"

e["Variables"][3]["Name"] = "Pole Angular Velocity"
e["Variables"][3]["Type"] = "State"

e["Variables"][4]["Name"] = "Force"
e["Variables"][4]["Type"] = "Action"

### Configuring Agent hyperparameters

e["Solver"]["Type"] = "Agent / Discrete / DQN"
e["Solver"]["Mode"] = "Training"
e["Solver"]["Experiences Between Policy Updates"] = 1
e["Solver"]["Cache Persistence"] = 1
e["Solver"]["Episodes Per Generation"] = 1
e["Solver"]["Target Update Frequency"] = 100

### Defining Experience Replay configuration

e["Solver"]["Experience Replay"]["Start Size"] = 5000
e["Solver"]["Experience Replay"]["Maximum Size"] = 10000

### Configuring the Remember-and-Forget Experience Replay algorithm

e["Solver"]["Experience Replay"]["REFER"]["Enabled"] = False
e["Solver"]["Experience Replay"]["REFER"]["Cutoff Scale"] = 4.0
e["Solver"]["Experience Replay"]["REFER"]["Target"] = 1.0
e["Solver"]["Experience Replay"]["REFER"]["Initial Beta"] = 1.0
e["Solver"]["Experience Replay"]["REFER"]["Annealing Rate"] = 5e-7

### Defining probability of taking a random action (epsilon)

e["Solver"]["Random Action Probability"] = 0.05

## Defining Q-Critic and Action-selection (policy) optimizers

#e["Solver"]["Optimizer"] = "GradientDescendent"
e["Solver"]["Optimizer"] = "AdaBelief"
e["Solver"]["Discount Factor"] = 0.99
e["Solver"]["Learning Rate"] = 0.01
e["Solver"]["Mini Batch Size"] = 32

### Configuring the neural network and its hidden layers

e["Solver"]["Neural Network"]["Engine"] = "OneDNN"

e["Solver"]["Neural Network"]["Hidden Layers"][0]["Type"] = "Layer/Linear"
e["Solver"]["Neural Network"]["Hidden Layers"][0]["Output Channels"] = 32

e["Solver"]["Neural Network"]["Hidden Layers"][1]["Type"] = "Layer/Activation"
e["Solver"]["Neural Network"]["Hidden Layers"][1]["Function"] = "Elementwise/Tanh"

e["Solver"]["Neural Network"]["Hidden Layers"][2]["Type"] = "Layer/Linear"
e["Solver"]["Neural Network"]["Hidden Layers"][2]["Output Channels"] = 32

e["Solver"]["Neural Network"]["Hidden Layers"][3]["Type"] = "Layer/Activation"
e["Solver"]["Neural Network"]["Hidden Layers"][3]["Function"] = "Elementwise/Tanh"

### Defining Termination Criteria

e["Solver"]["Termination Criteria"]["Testing"]["Target Average Reward"] = 450

### Setting file output configuration

e["File Output"]["Enabled"] = False

### Running Experiment

k.run(e)