#!/usr/bin/env python3

# In this example, we demonstrate how a Korali experiment can
# be resumed from any point (generation). This is a useful feature
# for continuing jobs after an error, or to fragment big jobs into
# smaller ones that can better fit a supercomputer queue.

# First, we run a simple Korali experiment.

import sys
sys.path.append('_model')
from model import *

import korali
k = korali.Engine()
e = korali.Experiment()

e["Problem"]["Type"] = "Optimization"
e["Problem"]["Objective Function"] = model_with_gradient

e["Solver"]["Type"] = "Optimizer/Rprop"
e["Solver"]["Termination Criteria"]["Max Generations"] = 25
e["Solver"]["Termination Criteria"]['Parameter Relative Tolerance'] = 1e-8

e["Variables"][0]["Name"] = "X"
e["Variables"][0]["Initial Value"] = -10.

e["Console Output"]["Frequency"] = 10

print("\n-------------------------------------------------------------")
print("Running first 25 generations...")
print("-------------------------------------------------------------\n")

k.run(e)

print("\n-------------------------------------------------------------")
print("Running last 25 generations...")
print("-------------------------------------------------------------\n")

e["Solver"]["Termination Criteria"]["Max Generations"] = 50
k.run(e)
