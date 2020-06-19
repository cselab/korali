#!/usr/bin/env python3

# Importing computational model
import sys
import os
import korali

# Creating hierarchical Bayesian problem from previous two problems
e = korali.Experiment()

e["Problem"]["Type"] = "Hierarchical/Psi"

for i in range(5):
  subProblem = korali.Experiment()
  subProblem.loadState('_setup/results_phase_1/' + str(i).zfill(3) + '/latest')
  e["Problem"]["Sub Experiments"][i] = subProblem

# Add probability of theta given psi, one per subproblem variable.

e["Variables"][0]["Name"] = "Psi 1"
e["Variables"][1]["Name"] = "Psi 2"
e["Variables"][2]["Name"] = "Psi 3"
e["Variables"][3]["Name"] = "Psi 4"

e["Variables"][0]["Prior Distribution"] = "Uniform 0"
e["Variables"][1]["Prior Distribution"] = "Uniform 1"
e["Variables"][2]["Prior Distribution"] = "Uniform 2"
e["Variables"][3]["Prior Distribution"] = "Uniform 3"

e["Problem"]["Conditional Priors"] = ["Conditional 0", "Conditional 1"]

# Configuring the problem's random distributions
e["Distributions"][0]["Name"] = "Conditional 0"
e["Distributions"][0]["Type"] = "Univariate/Normal"
e["Distributions"][0]["Mean"] = "Psi 1"
e["Distributions"][0]["Standard Deviation"] = "Psi 2"

e["Distributions"][1]["Name"] = "Conditional 1"
e["Distributions"][1]["Type"] = "Univariate/LogNormal"
e["Distributions"][1]["Mu"] = "Psi 3"
e["Distributions"][1]["Sigma"] = "Psi 4"

e["Distributions"][2]["Name"] = "Uniform 0"
e["Distributions"][2]["Type"] = "Univariate/Uniform"
e["Distributions"][2]["Minimum"] = 0.0
e["Distributions"][2]["Maximum"] = 20.0

e["Distributions"][3]["Name"] = "Uniform 1"
e["Distributions"][3]["Type"] = "Univariate/Uniform"
e["Distributions"][3]["Minimum"] = 0.0
e["Distributions"][3]["Maximum"] = 20.0

e["Distributions"][4]["Name"] = "Uniform 2"
e["Distributions"][4]["Type"] = "Univariate/Uniform"
e["Distributions"][4]["Minimum"] = -2.0
e["Distributions"][4]["Maximum"] = +2.0

e["Distributions"][5]["Name"] = "Uniform 3"
e["Distributions"][5]["Type"] = "Univariate/Uniform"
e["Distributions"][5]["Minimum"] = 0.0
e["Distributions"][5]["Maximum"] = 5.0

e["Solver"]["Type"] = "Sampler/TMCMC"
e["Solver"]["Population Size"] = 2000
e["Solver"]["Default Burn In"] = 1
e["Solver"]["Target Coefficient Of Variation"] = 0.6
e["Solver"]["Covariance Scaling"] = 0.1

e["Console Output"]["Verbosity"] = "Detailed"
e["File Output"]["Path"] = "_setup/results_phase_2/"
e["Random Seed"] = 0xC0FFEE

# Starting Korali's Engine and running experiment
k = korali.Engine()
#k["Conduit"]["Type"] = "Concurrent"
#k["Conduit"]["Concurrent Jobs"] = 4
k.run(e)
