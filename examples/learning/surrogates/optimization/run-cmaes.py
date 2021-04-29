#!/usr/bin/env python3

import korali
import numpy as np

# load the surrogate
surrogate = korali.Experiment()
found = surrogate.loadState("_korali_result_surrogate/latest")
assert found

def model(sample):
  x = sample["Parameters"][0]
  y = surrogate.getEvaluation([[[x]]])
  # minus because we maximize
  sample["F(x)"] = -y[0][0]

k = korali.Engine()
e = korali.Experiment()

e['Random Seed'] = 0xC0FFEE
e["Problem"]["Type"] = "Optimization"
e["Problem"]["Objective Function"] = model

e["Variables"][0]["Name"] = "X"
e["Variables"][0]["Lower Bound"] = -1.0
e["Variables"][0]["Upper Bound"] = +1.0

e["Solver"]["Type"] = "Optimizer/CMAES"
e["Solver"]["Population Size"] = 4
e["Solver"]["Termination Criteria"]["Min Value Difference Threshold"] = 1e-15
e["Solver"]["Termination Criteria"]["Max Generations"] = 100

e['Console Output']['Verbosity'] = 'Normal'
e['Console Output']['Frequency'] = 10
e['File Output']['Frequency'] = 100
e["File Output"]["Path"] = "_korali_result_cmaes"

k.run(e)
