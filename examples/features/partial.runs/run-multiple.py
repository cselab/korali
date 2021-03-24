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

# Creating experiment list
eList = []

for i in range(8):
  e = korali.Experiment()

  e["Problem"]["Type"] = "Optimization"
  e["Problem"]["Objective Function"] = model

  e["Solver"]["Type"] = "Optimizer/CMAES"
  e["Solver"]["Population Size"] = 5
  e["Solver"]["Termination Criteria"]["Max Generations"] = 25

  e["Variables"][0]["Name"] = "X"
  e["Variables"][0]["Lower Bound"] = -10.0
  e["Variables"][0]["Upper Bound"] = +10.0

  e["File Output"]["Path"] = '_result_run-multiple/exp' + str(i)
  e["Console Output"]["Frequency"] = 10
  eList.append(e)

print('------------------------------------------------------')
print('Now running first 25 generations...')
print('------------------------------------------------------')

k.run(eList)

print('------------------------------------------------------')
print('Now running last 25 generations...')
print('------------------------------------------------------')

for e in eList:
  e["Solver"]["Termination Criteria"]["Max Generations"] = 50
k.run(eList)
