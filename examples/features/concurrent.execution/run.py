#!/usr/bin/env python3
import korali
import sys
sys.path.append("_model")
from runModel import *

k = korali.Engine()

if (len(sys.argv) != 2):
  print(
      'Error: this example requires the number of concurrent jobs passed as numerical argument.\n'
  )
  exit(-1)

e = korali.Experiment()

e["Problem"]["Type"] = "Optimization"
e["Problem"]["Objective Function"] = runModel

e["Solver"]["Type"] = "Optimizer/CMAES"
e["Solver"]["Population Size"] = 12
e["Solver"]["Termination Criteria"]["Max Generations"] = 10

e["Variables"][0]["Name"] = "X0"
e["Variables"][0]["Lower Bound"] = -32.0
e["Variables"][0]["Upper Bound"] = +32.0

e["Variables"][1]["Name"] = "X1"
e["Variables"][1]["Lower Bound"] = -32.0
e["Variables"][1]["Upper Bound"] = +32.0

e["Variables"][2]["Name"] = "X2"
e["Variables"][2]["Lower Bound"] = -32.0
e["Variables"][2]["Upper Bound"] = +32.0

e["Variables"][3]["Name"] = "X3"
e["Variables"][3]["Lower Bound"] = -32.0
e["Variables"][3]["Upper Bound"] = +32.0
e["Random Seed"] = 0xC0FFEE

k["Conduit"]["Type"] = "Concurrent"
k["Conduit"]["Concurrent Jobs"] = int(sys.argv[1])

k.run(e)
