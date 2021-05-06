#!/usr/bin/env python3

# Importing computational model
import sys
import os
import korali
sys.path.append('_setup/model')
from model import *

# Creating hierarchical Bayesian problem from previous two problems
e = korali.Experiment()
theta = korali.Experiment()
psi = korali.Experiment()

theta.loadState('_setup/results_phase_1/000/latest')
psi.loadState('_setup/results_phase_2/latest')

e["Problem"]["Type"] = "Hierarchical/Theta"
e["Problem"]["Theta Experiment"] = theta
e["Problem"]["Psi Experiment"] = psi

e["Solver"]["Type"] = "Sampler/TMCMC"
e["Solver"]["Population Size"] = 1000
e["Solver"]["Termination Criteria"]["Max Generations"] = 30
e["Solver"]["Default Burn In"] = 1
e["Solver"]["Target Coefficient Of Variation"] = 0.6

e["Random Seed"] = 0xC0FFEE
e["Console Output"]["Verbosity"] = "Detailed"
e["File Output"]["Path"] = "_setup/results_phase_3b/"

# Starting Korali's Engine and running experiment
k = korali.Engine()
k["Conduit"]["Type"] = "Concurrent"
k["Conduit"]["Concurrent Jobs"] = 4
k.run(e)
