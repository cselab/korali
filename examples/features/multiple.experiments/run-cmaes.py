#!/usr/bin/env python3

## In this example, we demonstrate how Korali finds values for the
## variables that maximize the objective function, given by a
## user-provided computational model.

# Importing computational model
import sys
sys.path.append('./_model')
from model import *

# Starting Korali's Engine
import korali
k = korali.Engine()

# Configuring Multiple Experiments.
eList = []

for i in range(8):
  e = korali.Experiment()
  e["Problem"]["Type"] = "Bayesian/Reference"
  e["Problem"]["Likelihood Model"] = "Normal"
  e["Problem"]["Reference Data"] = getReferenceData()
  e["Problem"]["Computational Model"] = lambda sampleData: model(
      sampleData, getReferencePoints())

  # Configuring CMA-ES parameters
  e["Solver"]["Type"] = "Optimizer/CMAES"
  e["Solver"]["Population Size"] = 24
  e["Solver"]["Termination Criteria"]["Max Generations"] = 100

  # Configuring the problem's random distributions
  e["Distributions"][0]["Name"] = "Uniform 0"
  e["Distributions"][0]["Type"] = "Univariate/Uniform"
  e["Distributions"][0]["Minimum"] = -5.0
  e["Distributions"][0]["Maximum"] = +5.0

  e["Distributions"][1]["Name"] = "Uniform 1"
  e["Distributions"][1]["Type"] = "Univariate/Uniform"
  e["Distributions"][1]["Minimum"] = -5.0
  e["Distributions"][1]["Maximum"] = +5.0

  e["Distributions"][2]["Name"] = "Uniform 2"
  e["Distributions"][2]["Type"] = "Univariate/Uniform"
  e["Distributions"][2]["Minimum"] = 0.0
  e["Distributions"][2]["Maximum"] = +5.0

  # Configuring the problem's variables
  e["Variables"][0]["Name"] = "a"
  e["Variables"][0]["Prior Distribution"] = "Uniform 0"
  e["Variables"][0]["Initial Value"] = +0.0
  e["Variables"][0]["Initial Standard Deviation"] = +1.0

  e["Variables"][1]["Name"] = "b"
  e["Variables"][1]["Prior Distribution"] = "Uniform 1"
  e["Variables"][1]["Initial Value"] = +0.0
  e["Variables"][1]["Initial Standard Deviation"] = +1.0

  e["Variables"][2]["Name"] = "[Sigma]"
  e["Variables"][2]["Prior Distribution"] = "Uniform 2"
  e["Variables"][2]["Initial Value"] = +2.5
  e["Variables"][2]["Initial Standard Deviation"] = +0.5

  # Setting distinct experiment paths
  e["File Output"]["Path"] = '_korali_multiple/exp' + str(i)
  e["Store Sample Information"] = True

  # Adding Experiment to vector
  eList.append(e)

#k["Conduit"]["Type"] = "Concurrent"
#k["Conduit"]["Concurrent Jobs"] = 4
#k["Profiling"]["Detail"] = "Full"
#k["Profiling"]["Frequency"] = 0.5

# Running first 100 generations
k.run(eList)

# Running next 100 generations
for e in eList:
  e["Solver"]["Termination Criteria"]["Max Generations"] = 150
k.run(eList)
