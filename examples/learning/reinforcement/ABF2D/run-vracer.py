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
 
setResultsDir('_result_vracer')

### Defining Korali Problem

e["Problem"]["Type"] = "Reinforcement Learning / Continuous"
e["Problem"]["Environment Function"] = env
e["Problem"]["Training Reward Threshold"] = 50.0
e["Problem"]["Policy Testing Episodes"] = 20

### Defining state variables

e["Variables"][0]["Name"] = "Swimmer 1 - Pos X"
e["Variables"][1]["Name"] = "Swimmer 1 - Pos Y"
e["Variables"][2]["Name"] = "Swimmer 2 - Pos X"
e["Variables"][3]["Name"] = "Swimmer 2 - Pos Y"

### Defining action variables

e["Variables"][4]["Name"] = "Magnet Rotation X"
e["Variables"][4]["Type"] = "Action"
e["Variables"][4]["Initial Exploration Noise"] = 0.45

e["Variables"][5]["Name"] = "Magnet Rotation Y"
e["Variables"][5]["Type"] = "Action"
e["Variables"][5]["Initial Exploration Noise"] = 0.45

e["Variables"][6]["Name"] = "Magnet Intensity"
e["Variables"][6]["Type"] = "Action"
e["Variables"][6]["Initial Exploration Noise"] = 0.45

### Defining Agent Configuration 

e["Solver"]["Type"] = "Agent / Continuous / VRACER"
e["Solver"]["Mode"] = "Training"
e["Solver"]["Experiences Between Policy Updates"] = 1
e["Solver"]["Episodes Per Generation"] = 50 
e["Solver"]["Learning Rate"] = 1e-5
e["Solver"]["Mini Batch"]["Size"] = 128
e["Solver"]["Policy"]["Distribution"] = "Normal"
e["Solver"]["Experience Replay"]["Start Size"] = 32768
e["Solver"]["Experience Replay"]["Maximum Size"] = 131072


### Configuring the neural network and its hidden layers

e["Solver"]["Neural Network"]["Engine"] = "OneDNN"
e["Solver"]["Neural Network"]["Optimizer"] = "Adam"

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

### Setting file output configuration

e["Solver"]["Experience Replay"]["Serialize"] = True
e["Console Output"]["Verbosity"] = "Detailed"
e["File Output"]["Enabled"] = True
e["File Output"]["Frequency"] = 300
e["File Output"]["Path"] = "_result_vracer"

### Running Experiment

k.run(e)
