#!/usr/bin/env python3
import os
import sys
sys.path.append('./_model')
from env import *

import korali
k = korali.Engine()
e = korali.Experiment()

outdir = '_korali_result_rescale'
found = e.loadState(outdir+'/latest')
if (found == True):
  print('Continuing execution from latest...')
 
### Defining Korali Problem

e["Problem"]["Type"] = "Reinforcement Learning / Continuous"
e["Problem"]["Environment Function"] = env
e["Problem"]["Training Reward Threshold"] = 80.
e["Problem"]["Policy Testing Episodes"] = 10
e["Problem"]["Actions Between Policy Updates"] = 200

### Defining state variables

e["Variables"][0]["Name"] = "State 0"
e["Variables"][1]["Name"] = "State 1"
e["Variables"][2]["Name"] = "State 2"
e["Variables"][3]["Name"] = "State 3"
e["Variables"][4]["Name"] = "State 4"
e["Variables"][5]["Name"] = "State 5"
e["Variables"][6]["Name"] = "State 6"
e["Variables"][7]["Name"] = "State 7"


### Defining action variables

e["Variables"][8]["Name"] = "Rotation Joint 1"
e["Variables"][8]["Type"] = "Action"
e["Variables"][8]["Lower Bound"] = -1.0
e["Variables"][8]["Upper Bound"] = +1.0
e["Variables"][8]["Initial Exploration Noise"] = 0.5

e["Variables"][9]["Name"] = "Rotation Joint 2"
e["Variables"][9]["Type"] = "Action"
e["Variables"][9]["Lower Bound"] = -1.0
e["Variables"][9]["Upper Bound"] = +1.0
e["Variables"][9]["Initial Exploration Noise"] = 0.5

### Defining Agent Configuration 

e["Solver"]["Type"] = "Agent / Continuous / VRACER"
e["Solver"]["Mode"] = "Training"
e["Solver"]["Experiences Between Policy Updates"] = 1
e["Solver"]["Cache Persistence"] = 1000
e["Solver"]["Episodes Per Generation"] = 5
e["Solver"]["Policy Distribution"] = "Normal"
e["Solver"]["Discount Factor"] = 0.995
e["Solver"]["Learning Rate"] = 1e-4
#e["Solver"]["L2 Regularization"] = 1e-4
e["Solver"]["Mini Batch Size"] = 256

### Defining the configuration of replay memory

e["Solver"]["Experience Replay"]["Start Size"] = 32768
e["Solver"]["Experience Replay"]["Maximum Size"] = 262144

### Configuring the Remember-and-Forget Experience Replay algorithm

e["Solver"]["Experience Replay"]["REFER"]["Enabled"] = True
e["Solver"]["Experience Replay"]["REFER"]["Cutoff Scale"] = 4.0
e["Solver"]["Experience Replay"]["REFER"]["Target"] = 0.1
e["Solver"]["Experience Replay"]["REFER"]["Initial Beta"] = 0.3
e["Solver"]["Experience Replay"]["REFER"]["Annealing Rate"] = 5e-7

### Configuring the neural network and its hidden layers

e["Solver"]["Neural Network"]["Engine"] = "OneDNN"

e["Solver"]["Neural Network"]["Hidden Layers"][0]["Type"] = "Layer/Linear"
e["Solver"]["Neural Network"]["Hidden Layers"][0]["Output Channels"] = 128

e["Solver"]["Neural Network"]["Hidden Layers"][1]["Type"] = "Layer/Activation"
e["Solver"]["Neural Network"]["Hidden Layers"][1]["Function"] = "Elementwise/Tanh"

e["Solver"]["Neural Network"]["Hidden Layers"][2]["Type"] = "Layer/Linear"
e["Solver"]["Neural Network"]["Hidden Layers"][2]["Output Channels"] = 128

e["Solver"]["Neural Network"]["Hidden Layers"][3]["Type"] = "Layer/Activation"
e["Solver"]["Neural Network"]["Hidden Layers"][3]["Function"] = "Elementwise/Tanh"

### Defining Termination Criteria

e["Solver"]["Termination Criteria"]["Testing"]["Target Average Reward"] = 250.
e["Solver"]["Termination Criteria"]["Max Generations"] = 47000.

### Setting file output configuration

e["Solver"]["Experience Replay"]["Serialize"] = True
e["Console Output"]["Verbosity"] = "Detailed"
e["File Output"]["Enabled"] = True
e["File Output"]["Frequency"] = 500
e["File Output"]["Path"] = outdir

### Running Experiment

k.run(e)