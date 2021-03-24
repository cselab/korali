#!/usr/bin/env python3

# In this example, we demonstrate how a Korali experiment can
# be resumed from previous file-saved results. This is a useful feature
# for continuing jobs after an error, or to fragment big jobs into
# smaller ones that can better fit a supercomputer queue.

# First, we run a simple Korali experiment.

import sys
import os
sys.path.append('_model')
from model import *
import korali

k = korali.Engine()
e = korali.Experiment()

# Loading previous run (if exist)
e["File Output"]["Path"] = "_result_cmaes"
found = e.loadState('_result_cmaes/latest')

# If not found, we run first 5 generations.
if (found == False):
  print('------------------------------------------------------')
  print('Running first 5 generations...')
  print('------------------------------------------------------')
  e["Solver"]["Termination Criteria"]["Max Generations"] = 5

# If found, we continue with the next 5 generations.
if (found == True):
  print('------------------------------------------------------')
  print('Running next 5 generations...')
  print('------------------------------------------------------')
  e["Solver"]["Termination Criteria"]["Max Generations"] = e["Current Generation"] + 5
 
# Defining experiment

e["Problem"]["Type"] = "Optimization"

e["Solver"]["Type"] = "Optimizer/CMAES"
e["Solver"]["Population Size"] = 5

e["Variables"][0]["Name"] = "X"
e["Variables"][0]["Lower Bound"] = -10.0
e["Variables"][0]["Upper Bound"] = +10.0

# Setting computational model
e["Problem"]["Objective Function"] = model

k.run(e)
