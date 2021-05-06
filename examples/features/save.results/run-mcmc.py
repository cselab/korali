#!/usr/bin/env python3

## In this example, we demonstrate how to use Korali to sample
## a computational model, while saving important quantities of
## interest derived from the model

# Importing computational model
import sys
sys.path.append('_model')
from model import *

# Starting Korali's Engine
import korali
k = korali.Engine()
e = korali.Experiment()

# Selecting problem and solver types.
e["Problem"]["Type"] = "Sampling"
e["Problem"]["Probability Function"] = storeResults

# Defining the problem's variables and their bounds.
e["Variables"][0]["Name"] = "Soil pH"
e["Variables"][0]["Initial Mean"] = 6.0
e["Variables"][0]["Initial Standard Deviation"] = 1.0

e["Variables"][1]["Name"] = "Average Temperature (C)"
e["Variables"][1]["Initial Mean"] = +30.0
e["Variables"][1]["Initial Standard Deviation"] = +5.0

# Configuring the TMCMC sampler parameters
e["Solver"]["Type"] = "Sampler/MCMC"
e["Solver"]["Burn In"] = 500
e["Solver"]["Termination Criteria"]["Max Samples"] = 5000

# Configuring output frequency
e["Console Output"]["Frequency"] = 500
e["File Output"]["Frequency"] = 500

# Storing sample information
e["Store Sample Information"] = True

# Running Korali
k.run(e)
