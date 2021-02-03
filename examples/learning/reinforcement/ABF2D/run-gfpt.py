#!/usr/bin/env python3
import os
import sys
import argparse
sys.path.append('./_model')
from env import *

import korali
k = korali.Engine()
e = korali.Experiment()

### Setting results dir for ABF2D trajectories
 
setResultsDir('_result_gfpt')

### Defining Korali Problem

e["Problem"]["Type"] = "Reinforcement Learning / Continuous"
e["Problem"]["Environment Function"] = env
e["Problem"]["Training Reward Threshold"] = 50.0
e["Problem"]["Policy Testing Episodes"] = 1
e["Problem"]["Actions Between Policy Updates"] = 200

### Defining state variables

e["Variables"][0]["Name"] = "Swimmer 1 - Pos X"
e["Variables"][1]["Name"] = "Swimmer 1 - Pos Y"
e["Variables"][2]["Name"] = "Swimmer 2 - Pos X"
e["Variables"][3]["Name"] = "Swimmer 2 - Pos Y"

### Defining action variables

e["Variables"][4]["Name"] = "Magnet Rotation X"
e["Variables"][4]["Type"] = "Action"
e["Variables"][4]["Lower Bound"] = -1.0
e["Variables"][4]["Upper Bound"] = +1.0
e["Variables"][4]["Initial Exploration Noise"] = 0.25

e["Variables"][5]["Name"] = "Magnet Rotation Y"
e["Variables"][5]["Type"] = "Action"
e["Variables"][5]["Lower Bound"] = -1.0
e["Variables"][5]["Upper Bound"] = +1.0
e["Variables"][5]["Initial Exploration Noise"] = 0.25

e["Variables"][6]["Name"] = "Magnet Intensity"
e["Variables"][6]["Type"] = "Action"
e["Variables"][6]["Lower Bound"] = +0.0
e["Variables"][6]["Upper Bound"] = +2.0
e["Variables"][6]["Initial Exploration Noise"] = 0.25

### Defining Agent Configuration 

e["Solver"]["Type"] = "Agent / Continuous / GFPT"
e["Solver"]["Mode"] = "Training"
e["Solver"]["Episodes Per Generation"] = 1
e["Solver"]["Experiences Between Policy Updates"] = 1
e["Solver"]["Cache Persistence"] = 200
e["Solver"]["Learning Rate"] = 0.001

### Defining the configuration of replay memory

e["Solver"]["Experience Replay"]["Start Size"] = 4096
e["Solver"]["Experience Replay"]["Maximum Size"] = 65536

### Configuring the Remember-and-Forget Experience Replay algorithm

e["Solver"]["Experience Replay"]["REFER"]["Enabled"] = True
e["Solver"]["Experience Replay"]["REFER"]["Cutoff Scale"] = 4.0
e["Solver"]["Experience Replay"]["REFER"]["Target"] = 1.0
e["Solver"]["Experience Replay"]["REFER"]["Initial Beta"] = 1.0
e["Solver"]["Experience Replay"]["REFER"]["Annealing Rate"] = 5e-7

### Configuring Mini Batch

e["Solver"]["Mini Batch Size"] = 128
e["Solver"]["Mini Batch Strategy"] = "Uniform"

## Defining Critic and Policy Configuration

e["Solver"]["Policy"]["Learning Rate Scale"] = 0.1
e["Solver"]["Policy"]["Target Accuracy"] = 0.000001
e["Solver"]["Policy"]["Optimization Candidates"] = 64
e["Solver"]["Policy"]["Mini Batch Size"] = 4

### Configuring the neural network and its hidden layers

e["Solver"]["Neural Network"]["Engine"] = "OneDNN"

e["Solver"]["Neural Network"]["Hidden Layers"][0]["Type"] = "Layer/Linear"
e["Solver"]["Neural Network"]["Hidden Layers"][0]["Output Channels"] = 64

e["Solver"]["Neural Network"]["Hidden Layers"][1]["Type"] = "Layer/Activation"
e["Solver"]["Neural Network"]["Hidden Layers"][1]["Function"] = "Elementwise/Tanh"

e["Solver"]["Neural Network"]["Hidden Layers"][2]["Type"] = "Layer/Linear"
e["Solver"]["Neural Network"]["Hidden Layers"][2]["Output Channels"] = 64

e["Solver"]["Neural Network"]["Hidden Layers"][3]["Type"] = "Layer/Activation"
e["Solver"]["Neural Network"]["Hidden Layers"][3]["Function"] = "Elementwise/Tanh"

### Defining Termination Criteria

e["Solver"]["Termination Criteria"]["Testing"]["Target Average Reward"] = 50.0

### Setting console/file output configuration

e["Solver"]["Experience Replay"]["Serialize"] = False
e["Console Output"]["Verbosity"] = "Detailed"
e["File Output"]["Enabled"] = True
e["File Output"]["Frequency"] = 1
e["File Output"]["Path"] = "_result_gfpt"

### Running Experiment

k.run(e)