#!/usr/bin/env python3

# In this example, we demonstrate how Korali samples the posterior distribution
# in a bayesian problem where the likelihood is calculated by providing
# reference data points and their objective values.

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

# Configuring TMCMC parameters
e["Solver"]["Type"] = "Sampler/TMCMC"
e["Solver"]["Population Size"] = 5000
e["Solver"]["Target Coefficient Of Variation"] = 0.8
e["Solver"]["Covariance Scaling"] = 0.04

# Configuring the problem's random distributions
e["Distributions"][0]["Name"] = "Uniform 0"
e["Distributions"][0]["Type"] = "Univariate/Uniform"
e["Distributions"][0]["Minimum"] = 0.0
e["Distributions"][0]["Maximum"] = +5.0

e["Distributions"][1]["Name"] = "Uniform 1"
e["Distributions"][1]["Type"] = "Univariate/Uniform"
e["Distributions"][1]["Minimum"] = 0.0
e["Distributions"][1]["Maximum"] = +5.0

e["Distributions"][2]["Name"] = "Uniform 2"
e["Distributions"][2]["Type"] = "Univariate/Uniform"
e["Distributions"][2]["Minimum"] = 0.0
e["Distributions"][2]["Maximum"] = +5.0

# Configuring the problem's variables and their prior distributions
e["Variables"][0]["Name"] = "a"
e["Variables"][0]["Prior Distribution"] = "Uniform 0"

e["Variables"][1]["Name"] = "b"
e["Variables"][1]["Prior Distribution"] = "Uniform 1"

e["Variables"][2]["Name"] = "[Sigma]"
e["Variables"][2]["Prior Distribution"] = "Uniform 2"

e["Store Sample Information"] = True

# Configuring output settings
e["File Output"]["Path"] = '_korali_result_tmcmc'

# Starting Korali's Engine and running experiment
e["Console Output"]["Verbosity"] = "Detailed"
k = korali.Engine()
k.run(e)
