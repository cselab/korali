#!/usr/bin/env python3

## In this example, we demonstrate how a Korali experiment can
## be resumed from any point (generation). This is a useful feature
## for continuing jobs after an error, or to fragment big jobs into
## smaller ones that can better fit a supercomputer queue.

## First, we run a simple Korali experiment.

import sys
sys.path.append('./_model')
from model import *

import korali
k = korali.Engine()
e = korali.Experiment()

e["Problem"]["Type"] = "Optimization"
e["Problem"]["Objective Function"] = model

e["Solver"]["Type"] = "Optimizer/DEA"
e["Solver"]["Population Size"] = 10
e["Solver"]["Termination Criteria"]["Max Generations"] = 50

e["Variables"][0]["Name"] = "X"
e["Variables"][0]["Lower Bound"] = -10.0
e["Variables"][0]["Upper Bound"] = +10.0

e["Console Output"]["Frequency"] = 5
e["File Output"]["Frequency"] = 5

print('------------------------------------------------------')
print('Now running first 50 generations...')
print('------------------------------------------------------')

k.run(e)

print('------------------------------------------------------')
print('Now running last 50 generations...')
print('------------------------------------------------------')

e["Solver"]["Termination Criteria"]["Max Generations"] = 100
k.run(e)
