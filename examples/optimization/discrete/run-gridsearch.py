#!/usr/bin/env python3

## In this example, we demonstrate how Korali finds values for the
## variables that maximize the objective function, given by a
## user-provided computational model.

# Importing computational model
import sys
sys.path.append('./_model')
from model import *
import numpy as np

# Starting Korali's Engine
import korali
k = korali.Engine()

# Creating new experiment
e = korali.Experiment()

# Configuring Problem
e["Random Seed"] = 0xC0FEE
e["Problem"]["Type"] = "Optimization"
e["Problem"]["Objective Function"] = modelGrid

# Defining the problem's variables.
e["Variables"][0]["Name"] = "X"
e["Variables"][0]["Values"] = np.linspace(-1, 1, 1000).tolist()

# Chosing Grid Search solver
e["Solver"]["Type"] = "Optimizer/GridSearch"

# Running Korali
k.run(e)
