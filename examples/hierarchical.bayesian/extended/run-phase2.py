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
e["Variables"][4]["Name"] = "Psi 5"
e["Variables"][5]["Name"] = "Psi 6"

e["Variables"][0]["Prior Distribution"] = "Uniform 0"
e["Variables"][1]["Prior Distribution"] = "Uniform 1"
e["Variables"][2]["Prior Distribution"] = "Uniform 2"
e["Variables"][3]["Prior Distribution"] = "Uniform 3"
e["Variables"][4]["Prior Distribution"] = "Uniform 4"
e["Variables"][5]["Prior Distribution"] = "Uniform 5"

e["Problem"]["Conditional Priors"] = [
    "Conditional 0", "Conditional 1", "Conditional 2", "Conditional 3"
]

e["Distributions"][0]["Name"] = "Conditional 0"
e["Distributions"][0]["Type"] = "Univariate/Uniform"
e["Distributions"][0]["Minimum"] = 280
e["Distributions"][0]["Maximum"] = 320

e["Distributions"][1]["Name"] = "Conditional 1"
e["Distributions"][1]["Type"] = "Univariate/Normal"
e["Distributions"][1]["Mean"] = "Psi 1"
e["Distributions"][1]["Standard Deviation"] = "Psi 2"

e["Distributions"][2]["Name"] = "Conditional 2"
e["Distributions"][2]["Type"] = "Univariate/LogNormal"
e["Distributions"][2]["Mu"] = "Psi 3"
e["Distributions"][2]["Sigma"] = "Psi 4"

e["Distributions"][3]["Name"] = "Conditional 3"
e["Distributions"][3]["Type"] = "Univariate/Uniform"
e["Distributions"][3]["Minimum"] = "Psi 5"
e["Distributions"][3]["Maximum"] = "Psi 6"

e["Distributions"][4]["Name"] = "Uniform 0"
e["Distributions"][4]["Type"] = "Univariate/Uniform"
e["Distributions"][4]["Minimum"] = 10.0
e["Distributions"][4]["Maximum"] = 70.0

e["Distributions"][5]["Name"] = "Uniform 1"
e["Distributions"][5]["Type"] = "Univariate/Uniform"
e["Distributions"][5]["Minimum"] = 0.001
e["Distributions"][5]["Maximum"] = 30.0

e["Distributions"][6]["Name"] = "Uniform 2"
e["Distributions"][6]["Type"] = "Univariate/Uniform"
e["Distributions"][6]["Minimum"] = -1.0
e["Distributions"][6]["Maximum"] = +1.0

e["Distributions"][7]["Name"] = "Uniform 3"
e["Distributions"][7]["Type"] = "Univariate/Uniform"
e["Distributions"][7]["Minimum"] = 0.0
e["Distributions"][7]["Maximum"] = 10.0

e["Distributions"][8]["Name"] = "Uniform 4"
e["Distributions"][8]["Type"] = "Univariate/Uniform"
e["Distributions"][8]["Minimum"] = 0.0
e["Distributions"][8]["Maximum"] = 15.0

e["Distributions"][9]["Name"] = "Uniform 5"
e["Distributions"][9]["Type"] = "Univariate/Uniform"
e["Distributions"][9]["Minimum"] = 0.0
e["Distributions"][9]["Maximum"] = 15.0

e["Solver"]["Type"] = "Sampler/TMCMC"
e["Solver"]["Population Size"] = 1000
e["Solver"]["Default Burn In"] = 3
e["Solver"]["Target Coefficient Of Variation"] = 0.6
e["Solver"]["Covariance Scaling"] = 0.01

e["Random Seed"] = 0xC0FFEE
e["Console Output"]["Verbosity"] = "Detailed"
e["File Output"]["Path"] = "_setup/results_phase_2/"

# Starting Korali's Engine and running experiment
k = korali.Engine()
k["Conduit"]["Type"] = "Concurrent"
k["Conduit"]["Concurrent Jobs"] = 4
k.run(e)
