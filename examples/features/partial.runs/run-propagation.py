#!/usr/bin/env python3
import os
import sys
sys.path.append('./_model/')
from model import *
import numpy as np

Ns = 100
means = [-5, 5, 10, 15, 20]
variances = [1, 1, 1, 1, 1]
fileName = '_propagation_output/samplesOut.dat'
prepareFile(fileName)

import korali
k = korali.Engine()
e = korali.Experiment()

e["Problem"]["Type"] = "Propagation"
e["Problem"]["Execution Model"] = lambda modelData: put_normal_rnds(
    modelData, Ns, fileName)

e["Variables"][0]["Name"] = "Mean"
e["Variables"][0]["Precomputed Values"] = means
e["Variables"][1]["Name"] = "Variance"
e["Variables"][1]["Precomputed Values"] = variances

e["Solver"]["Type"] = "Executor"
e["Solver"]["Executions Per Generation"] = 1
e["Solver"]["Termination Criteria"]["Max Generations"] = 2

print("\n-------------------------------------------------------------")
print("Now running first 2 samples.")
print("-------------------------------------------------------------\n")

k.run(e)

print('------------------------------------------------------')
print("Now running another 2 samples.")
print('------------------------------------------------------')

e["Solver"]["Termination Criteria"]["Max Generations"] = 4
k.run(e)

print('------------------------------------------------------')
print("Now running last sample(s).")
print('------------------------------------------------------')

e["Solver"]["Termination Criteria"]["Max Generations"] = 100
k.run(e)
