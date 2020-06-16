#!/usr/bin/env python3

# Importing computational model
import sys
sys.path.append('./model')
sys.path.append('./helpers')

from model import *
from helpers import *

lg5 = lambda x: lgaussianxdCustom(x, 5)

# Starting Korali's Engine
import korali
k = korali.Engine()
e = korali.Experiment()

# Setting up custom likelihood for the Bayesian Problem
e["Problem"]["Type"] = "Bayesian/Custom"
e["Problem"]["Likelihood Model"] = lg5

# Configuring Nested Sampling parameters
e["Solver"]["Type"] = "Sampler/Nested"
e["Solver"]["Number Live Points"] = 1500
e["Solver"]["Batch Size"] = 1
e["Solver"]["Add Live Points"] = True
e["Solver"]["Resampling Method"] = "Ellipse"

# Configuring the problem's random distributions
for i in range(5):
  e["Distributions"][i]["Name"] = "Uniform " + str(i)
  e["Distributions"][i]["Type"] = "Univariate/Uniform"
  e["Distributions"][i]["Minimum"] = -5.0
  e["Distributions"][i]["Maximum"] = +5.0

  # Configuring the problem's variables and their prior distributions
  e["Variables"][i]["Name"] = "a" + str(i)
  e["Variables"][i]["Prior Distribution"] = "Uniform 0"

e["File Output"]["Enabled"] = False
e["Console Output"]["Frequency"] = 1000
e["Solver"]["Termination Criteria"]["Max Generations"] = 50000
e["Solver"]["Termination Criteria"]["Max Gain Factor"] = 1e-9
e["Solver"]["Termination Criteria"]["Max Effective Sample Size"] = 50000

e["Random Seed"] = 1337

# Running Korali
k.run(e)

verifyMean(e["Results"]["Sample Database"], [0.0, 0.0, 0.0, 0.0, 0.0], 0.05)
verifyStd(e["Results"]["Sample Database"], [1.0, 1.0, 1.0, 1.0, 1.0], 0.05)
