#!/usr/bin/env python


def subModel(p, x):
  y = p["Parameters"][0]
  p["F(x)"] = -0.5 * y * x


def model(p):
  x = p["Parameters"][0]
  # Starting Model's Korali Engine
  import korali
  k = korali.Engine()

  # Creating new experiment
  e = korali.Experiment()

  # Configuring Problem
  e["Random Seed"] = 0xC0FEE
  e["Problem"]["Type"] = "Optimization"
  e["Problem"]["Objective Function"] = lambda sampleData: subModel(sampleData, x)

  # Defining the problem's variables
  e["Variables"][0]["Name"] = "Y"
  e["Variables"][0]["Lower Bound"] = -10.0
  e["Variables"][0]["Upper Bound"] = +10.0

  # Configuring CMA-ES parameters
  e["Solver"]["Type"] = "Optimizer/CMAES"
  e["Solver"]["Population Size"] = 4
  e["Solver"]["Termination Criteria"]["Min Value Difference Threshold"] = 1e-15
  e["Solver"]["Termination Criteria"]["Max Generations"] = 100

  e["Console Output"]["Verbosity"] = "Silent"
  e["File Output"]["Enabled"] = False

  # Running Korali
  k.run(e)

  # Storing the best Y as result of evaluation
  p["F(x)"] = e["Results"]["Best Sample"]["F(x)"]
