#!/usr/bin/env python3

# In this example, we demonstrate how Korali finds values for the
# variables that maximize the objective function, given by a
# user-provided computational model, subject to a set of
# constraints.

# Importing the computational model and constraints
import sys
sys.path.append('_model')
from model import *
from constraints import *

# Creating new experiment
import korali
e = korali.Experiment()

# Selecting problem type
e["Problem"]["Type"] = "Optimization"
e["Problem"]["Objective Function"] = model
e["Problem"]["Constraints"] = [g1, g2, g3, g4]

# Creating 7 variables and setting their CCMA-ES bounds
for i in range(7):
  e["Variables"][i]["Name"] = "X" + str(i)
  e["Variables"][i]["Lower Bound"] = -10.0
  e["Variables"][i]["Upper Bound"] = +10.0

# Configuring the constrained optimizer CCMA-ES
e["Solver"]["Type"] = "Optimizer/CMAES"
e["Solver"]["Is Sigma Bounded"] = True
e["Solver"]["Population Size"] = 32
e["Solver"]["Viability Population Size"] = 4
e["Solver"]["Termination Criteria"]["Max Value"] = -680.630057374402 - 1e-4
e["Solver"]["Termination Criteria"]["Max Generations"] = 500

# Starting Korali's Engine and running experiment
k = korali.Engine()
k.run(e)
