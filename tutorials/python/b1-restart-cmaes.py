#!/usr/bin/env python3

## In this example, we demonstrate how a Korali experiment can
## be resumed from any point (generation). This is a useful feature
## for continuing jobs after an error, or to fragment big jobs into
## smaller ones that can better fit a supercomputer queue. 

## First, we run a simple Korali experiment.

import sys
sys.path.append('./model')
from directModel import *

import korali
k = korali.initialize()
k.setModel(evaluateModel)

k["Problem"] = "Direct Evaluation"
k["Solver"]  = "CMA-ES" 
k["Variables"][0]["Name"] = "X"
k["Variables"][0]["CMA-ES"]["Lower Bound"] = -10.0
k["Variables"][0]["CMA-ES"]["Upper Bound"] = +10.0
k["CMA-ES"]["Objective"] = "Maximize"
k["CMA-ES"]["Termination Criteria"]["Max Generations"]["Value"] = 500
k["CMA-ES"]["Sample Count"] = 5

# Setting output directory
k["Result Directory"] = "_b1_restart_cmaes"

k.run()

# Reducing Output
k["CMA-ES"]["Result Output Frequency"]  = 100

# Now we loadState() to resume the same experiment from generation 5.
k.loadState("_b1_restart_cmaes/s00400.json")

k.run()
