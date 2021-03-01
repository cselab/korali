#!/usr/bin/env python3

# In this example, we demonstrate how Korali find the variable values
# that maximize the posterior in a bayesian problem where the likelihood
# is calculated by providing reference data points and their objective values.

# Importing the computational model
import sys
sys.path.append('./_model')
from model import *

# Creating new experiment
import korali
e = korali.Experiment()

# Setting up the reference likelihood for the Bayesian Problem
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

# Configuring output settings
e["File Output"]["Path"] = '_korali_result_cmaes'
e["File Output"]["Frequency"] = 5
e["Console Output"]["Frequency"] = 5

# Starting Korali's Engine and running experiment
k = korali.Engine()
k.run(e)
