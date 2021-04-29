#!/usr/bin/env python3

# Importing computational model
import korali

# Creating hierarchical Bayesian problem from previous two problems
e = korali.Experiment()

psi = korali.Experiment()
psi.loadState('_setup/results_phase_2/latest')

e["Problem"]["Type"] = "Hierarchical/ThetaNew"
e["Problem"]["Psi Experiment"] = psi

e["Distributions"][0]["Name"] = "Uniform 0"
e["Distributions"][0]["Type"] = "Univariate/Uniform"
e["Distributions"][0]["Minimum"] = 280.0
e["Distributions"][0]["Maximum"] = 320.0

e["Distributions"][1]["Name"] = "Uniform 1"
e["Distributions"][1]["Type"] = "Univariate/Uniform"
e["Distributions"][1]["Minimum"] = 10.0
e["Distributions"][1]["Maximum"] = 70.0

e["Distributions"][2]["Name"] = "Uniform 2"
e["Distributions"][2]["Type"] = "Univariate/Uniform"
e["Distributions"][2]["Minimum"] = 0.0
e["Distributions"][2]["Maximum"] = 5.0

e["Distributions"][3]["Name"] = "Uniform 3"
e["Distributions"][3]["Type"] = "Univariate/Uniform"
e["Distributions"][3]["Minimum"] = 0.0
e["Distributions"][3]["Maximum"] = 20.0

e["Variables"][0]["Name"] = "C1"
e["Variables"][1]["Name"] = "C2"
e["Variables"][2]["Name"] = "C3"
e["Variables"][3]["Name"] = "Sigma"

e["Variables"][0]["Prior Distribution"] = "Uniform 0"
e["Variables"][1]["Prior Distribution"] = "Uniform 1"
e["Variables"][2]["Prior Distribution"] = "Uniform 2"
e["Variables"][3]["Prior Distribution"] = "Uniform 3"

e["Solver"]["Type"] = "Sampler/TMCMC"
e["Solver"]["Population Size"] = 1000
e["Solver"]["Target Coefficient Of Variation"] = 0.6
e["Solver"]["Covariance Scaling"] = 0.02
e["Solver"]["Default Burn In"] = 1
e["Solver"]["Max Chain Length"] = 1

e["Random Seed"] = 0xC0FFEE
e["Console Output"]["Verbosity"] = "Detailed"
e["File Output"]["Path"] = "_setup/results_phase_3a/"

# Starting Korali's Engine and running experiment
k = korali.Engine()
k["Conduit"]["Type"] = "Concurrent"
k["Conduit"]["Concurrent Jobs"] = 4
k.run(e)
