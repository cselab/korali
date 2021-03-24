#!/usr/bin/env python3

# In this example, we demonstrate how Korali samples the posterior
# distribution of the coastline distance 'alpha' and distance from shore 'beta'
# of the lighthouse.


# Importing computational model
import sys
sys.path.append('./models')
from models import *

# Creating Synthetic Data
data = getReferenceData(N=512)

# Starting Korali's Engine
import korali
k = korali.Engine()
e = korali.Experiment()

# Configuring problem
e["Problem"]["Type"] = "Bayesian/Custom"
e["Problem"]["Likelihood Model"] = lambda x: model2(x, data)

e["Distributions"][0]["Name"] = "Uniform 0"
e["Distributions"][0]["Type"] = "Univariate/Uniform"
e["Distributions"][0]["Minimum"] = -100.0
e["Distributions"][0]["Maximum"] = +100.0

e["Distributions"][1]["Name"] = "Uniform 1"
e["Distributions"][1]["Type"] = "Univariate/Uniform"
e["Distributions"][1]["Minimum"] = 0.0
e["Distributions"][1]["Maximum"] = +100.0

# Defining problem's variables and prior distribution for TMCMC
e["Variables"][0]["Name"] = "Alpha"
e["Variables"][0]["Prior Distribution"] = "Uniform 0"

e["Variables"][1]["Name"] = "Beta"
e["Variables"][1]["Prior Distribution"] = "Uniform 1"

# Configuring the TMCMC sampler parameters
e["Solver"]["Type"] = "Sampler/TMCMC"
e["Solver"]["Population Size"] = 2000
e["Solver"]["Target Coefficient Of Variation"] = 2.0

# General settings
e["File Output"]["Path"] = "_results_example2" 

# Running Korali
k.run(e)
