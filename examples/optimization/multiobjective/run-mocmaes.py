#!/usr/bin/env python3

## In this example, we demonstrate how Korali finds values for the
## variables that maximize the objective functions, given by a
## user-provided computational model.

# Importing computational model
import sys
sys.path.append('./_model')
from model import *

# Starting Korali's Engine
import korali
k = korali.Engine()

# Creating new experiment
e = korali.Experiment()

# Configuring Problem
e["Random Seed"] = 0xC0F33
e["Problem"]["Type"] = "Optimization"
e["Problem"]["Objective Function"] = negative_rosenbrock_and_sphere
e["Problem"]["Num Objectives"] = 2

dim = 2

# Defining the problem's variables.
for i in range(dim):
    e["Variables"][i]["Name"] = "X" + str(i)
    e["Variables"][i]["Lower Bound"] = -25.0
    e["Variables"][i]["Upper Bound"] = +25.0
    e["Variables"][i]["Initial Standard Deviation"] = 3.0

# Configuring CMA-ES parameters
e["Solver"]["Type"] = "Optimizer/MOCMAES"
e["Solver"]["Population Size"] = 32
e["Solver"]["Mu Value"] = 16
e["Solver"]["Termination Criteria"]["Min Value Difference Threshold"] = 1e-8
e["Solver"]["Termination Criteria"]["Min Variable Difference Threshold"] = 1e-8
e["Solver"]["Termination Criteria"]["Max Generations"] = 500

# Configuring results path
e["File Output"]["Path"] = '_korali_result_mocmaes'
e["File Output"]["Frequency"] = 1

# Running Korali
k.run(e)
