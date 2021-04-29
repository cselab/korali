#!/usr/bin/env python3
import os
import sys
import json
import korali

sys.path.append('./helpers')
from helpers import *

#################################################
#  Prepare Expected Values
#################################################

gen = 1
currentBurnIn = [0, 0, 10, 7, 5, 5, 5, 5, 5, 5, 5, 5]

eps = 1e-12
prevRho = 0.0
minRhoUpdate = 1e-3
maxRhoUpdate = 0.2

#################################################
# Set Up  TMCMC run
#################################################

print("[Korali] Prepare TMCMC run")

e = korali.Experiment()
e["Problem"]["Type"] = "Bayesian/Custom"
e["Problem"]["Likelihood Model"] = evaluateLogLikelihood

e["Distributions"][0]["Name"] = "Uniform 0"
e["Distributions"][0]["Type"] = "Univariate/Uniform"
e["Distributions"][0]["Minimum"] = -10.0
e["Distributions"][0]["Maximum"] = +10.0

e["Variables"][0]["Name"] = "X"
e["Variables"][0]["Prior Distribution"] = "Uniform 0"

e["Solver"]["Type"] = "Sampler/TMCMC"
e["Solver"]["Population Size"] = 5000
e["Solver"]["Covariance Scaling"] = 0.001

e["Solver"]["Default Burn In"] = 5
e["Solver"]["Per Generation Burn In"] = [10, 7]
e["Solver"]["Max Chain Length"] = 1
e["Solver"]["Target Coefficient Of Variation"] = 0.5
e["Solver"]["Min Annealing Exponent Update"] = minRhoUpdate
e["Solver"]["Max Annealing Exponent Update"] = maxRhoUpdate

e["Random Seed"] = 314

#################################################
#  Run TMCMC
#################################################

# Starting Korali's Engine
k = korali.Engine()
print("[Korali] Running TMCMC...")
k.run(e)

#################################################
# Read Result Files
#################################################

print("[Korali] Read & Evaluate Output..")

src = "_korali_result"
resultfiles = [
    f for f in os.listdir(src) if os.path.isfile(os.path.join(src, f))
]
auxList = resultfiles
resultfiles = []
for f in auxList:
  if (f.startswith('gen')):
    resultfiles.append(f)
resultfiles = sorted(resultfiles)

for filename in resultfiles:
  path = '{0}/{1}'.format(src, filename)

  with open(path) as f:
    dataString = f.read()
    dataString = dataString.replace('+INFINITY', '1.0e+300').replace(
        '-INFINITY', '-1.0e+300').replace('NaN', '-1.0e+300')
    data = json.loads(dataString)

    #################################################
    # Test Result
    #################################################

    print("[Korali] Checking generation {0} inside file {1} ..".format(
        gen, path))

    # Testing Burn In Assignments
    assert_value(data['Solver']['Default Burn In'], 5)
    #assert_value( data['Solver']['Current Burn In'], currentBurnIn[gen] )

    # Testing Correctness of (min/max) Rho Update
    assert_value(data['Solver']['Min Annealing Exponent Update'], minRhoUpdate)
    assert_value(data['Solver']['Max Annealing Exponent Update'], maxRhoUpdate)
    rho = data['Solver']['Annealing Exponent']

    # Updates
    prevRho = rho
    gen = gen + 1