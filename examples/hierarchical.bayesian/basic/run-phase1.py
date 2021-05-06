#!/usr/bin/env python3
import sys
import os
import shutil
sys.path.append('_setup/model')
from model import *
import korali

# Creating Experiment List
eList = []
for i in range(5):
  e = korali.Experiment()

  data = getReferenceData("_setup/data/", i)
  N = len(data)

  e["Problem"]["Type"] = "Bayesian/Reference"
  e["Problem"]["Likelihood Model"] = "Normal"
  e["Problem"]["Reference Data"] = data
  e["Problem"]["Computational Model"] = lambda d: normal(N,d)


  # Configuring the problem's random distributions
  e["Distributions"][0]["Name"] = "Uniform 0"
  e["Distributions"][0]["Type"] = "Univariate/Uniform"
  e["Distributions"][0]["Minimum"] = 0.0
  e["Distributions"][0]["Maximum"] = 20.0

  e["Distributions"][1]["Name"] = "Uniform 1"
  e["Distributions"][1]["Type"] = "Univariate/Uniform"
  e["Distributions"][1]["Minimum"] = 0.0
  e["Distributions"][1]["Maximum"] = 10.0

  e["Variables"][0]["Name"] = "[Mean]"
  e["Variables"][0]["Prior Distribution"] = "Uniform 0"

  e["Variables"][1]["Name"] = "[Sigma]"
  e["Variables"][1]["Prior Distribution"] = "Uniform 1"

  e["Solver"]["Type"] = "Sampler/TMCMC"
  e["Solver"]["Population Size"] = 1000
  e["Solver"]["Target Coefficient Of Variation"] = 0.6
  e["Solver"]["Covariance Scaling"] = 0.02
  e["Solver"]["Default Burn In"] = 0

  e["Random Seed"] = 0xC0FFEE
  e["File Output"]["Path"] = "_setup/results_phase_1/" + str(i).zfill(3)
  e["Console Output"]["Verbosity"] = "Detailed"
  eList.append(e)

# Starting Korali's Engine and running experiment
k = korali.Engine()
k["Conduit"]["Type"] = "Concurrent"
k["Conduit"]["Concurrent Jobs"] = 4
k.run(eList)
