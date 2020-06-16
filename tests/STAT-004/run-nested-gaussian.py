#!/usr/bin/env python3

# Importing the computational model
import sys
sys.path.append('./model')
sys.path.append('./helpers')

from model import *
from helpers import *

# Creating new experiment
import korali
e = korali.Experiment()

# Setting up the reference likelihood for the Bayesian Problem
e["Problem"]["Type"] = "Bayesian/Custom"
e["Problem"]["Likelihood Model"] = lgaussianCustom

# Configuring Nested Sampling parameters
e["Solver"]["Type"] = "Sampler/Nested"
e["Solver"]["Number Live Points"] = 1500
e["Solver"]["Batch Size"] = 1
e["Solver"]["Add Live Points"] = True
e["Solver"]["Resampling Method"] = "Box"

# Configuring the problem's random distributions
e["Distributions"][0]["Name"] = "Uniform 0"
e["Distributions"][0]["Type"] = "Univariate/Uniform"
e["Distributions"][0]["Minimum"] = -15.0
e["Distributions"][0]["Maximum"] = +15.0

# Configuring the problem's variables and their prior distributions
e["Variables"][0]["Name"] = "a"
e["Variables"][0]["Prior Distribution"] = "Uniform 0"

e["File Output"]["Enabled"] = False
e["Console Output"]["Frequency"] = 1000
e["Solver"]["Termination Criteria"]["Max Generations"] = 20000
e["Solver"]["Termination Criteria"]["Max Gain Factor"] = 1e-9
e["Solver"]["Termination Criteria"]["Max Effective Sample Size"] = 50000
e["Random Seed"] = 1227

# Starting Korali's Engine and running experiment
k = korali.Engine()
k.run(e)

verifyMean(e["Results"]["Posterior Samples"], [-2.0], 0.1)
verifyStd(e["Results"]["Posterior Samples"], [3.0], 0.1)
