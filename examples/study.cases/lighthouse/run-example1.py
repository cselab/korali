#!/usr/bin/env python3

# In this example, we demonstrate how Korali samples the posterior
# distribution of the estimated coastline distance 'alpha' of the lighthouse 
# problem with KNOWN distance from shore 'beta'.

# Importing computational model
import sys
sys.path.append('./models')
from models import *

# Creating Synthetic Data
data = getReferenceData(N=1)

# Starting Korali's Engine
import korali
k = korali.Engine()
e = korali.Experiment()

# Configuring problem
e["Problem"]["Type"] = "Bayesian/Custom"
e["Problem"]["Likelihood Model"] = lambda x: model1(x, data)

e["Distributions"][0]["Name"] = "Uniform 0"
e["Distributions"][0]["Type"] = "Univariate/Uniform"
e["Distributions"][0]["Minimum"] = -100.0
e["Distributions"][0]["Maximum"] = +100.0

# Defining problem's variables and prior distribution for TMCMC
e["Variables"][0]["Name"] = "Alpha"
e["Variables"][0]["Prior Distribution"] = "Uniform 0"

# Configuring the TMCMC sampler parameters
e["Solver"]["Type"] = "Sampler/TMCMC"
e["Solver"]["Population Size"] = 5000
#e["Solver"]["Default Burn In"] = 1
e["Solver"]["Target Coefficient Of Variation"] = 0.2

# Gener settings 
e["File Output"]["Path"] = "_results_example1"

# Running Korali
k.run(e)
