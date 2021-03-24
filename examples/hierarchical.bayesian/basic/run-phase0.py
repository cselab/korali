#!/usr/bin/env python3
import sys
sys.path.append('_setup/model')
from model import *
import numpy as np

# N : number of datasets
N = 5

# Ns: number os samples in each dataset
Ns = 100

# Creating new experiment
import korali
e = korali.Experiment()

e["Problem"]["Type"] = "Propagation"
e["Problem"]["Execution Model"] = lambda modelData: normal_rnds(modelData, Ns)

e["Variables"][0]["Name"] = "V1"
e["Variables"][1]["Name"] = "V2"
e["Variables"][0]["Precomputed Values"] = np.random.normal(10, 4, N).tolist()
e["Variables"][1]["Precomputed Values"] = np.random.lognormal(0, 1, N).tolist()

e["Solver"]["Type"] = "Executor"
e["Solver"]["Executions Per Generation"] = 1

e["Random Seed"] = 0xC0FFEE
e["File Output"]["Path"] = "_setup/results_phase_0/"
e["Console Output"]["Verbosity"] = "Detailed"

# Starting Korali's Engine and running experiment
k = korali.Engine()
k.run(e)
