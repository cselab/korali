#!/usr/bin/env python3

import sys
sys.path.append('./_model')
from model import *
from tutorial_samplers import *

import numpy as np  # we use numpy for random initializations
#import mpi4py
#from mpi4py import MPI
import korali


def main():

  # Initialize the distribution
  distrib1 = ExampleDistribution1()

  distrib1_S = lambda s: distrib1.S(s)
  distrib1_zeta = lambda s: distrib1.zeta(s)
  distrib1_phi = lambda s: distrib1.phi(s)

  d1_numberLatentVars = distrib1._p.nDimensions
  d1_numberHyperparams = 1

  initialSigma = 4
  d1_initialLatentValues = np.random.normal(0, 0.5, (d1_numberLatentVars,))
  d1_initialHyperparams = np.array([initialSigma])

  gaussian_sampler_obj = MCMCLatentSampler(d1_numberLatentVars,
                                           d1_numberHyperparams,
                                           d1_initialLatentValues,
                                           d1_initialHyperparams, distrib1_zeta,
                                           distrib1_S, distrib1_phi)

  k = korali.Engine()
  e = korali.Experiment()

  e["Problem"]["Type"] = "Bayesian/Latent/ExponentialLatent"
  e["Problem"]["S Of Likelihood Model"] = distrib1_S
  e["Problem"]["Zeta Of Likelihood Model"] = distrib1_zeta
  e["Problem"]["Phi Of Likelihood Model"] = distrib1_phi
  e["Problem"]["S Dimension"] = 1
  e["Problem"]["Latent Variable Sampler"] = lambda sample: gaussian_sampler_obj.sampleLatent(sample)

  e["Solver"]["Type"] = "SAEM"
  e["Solver"]["Number Samples Per Step"] = 10
  e["Solver"]["Termination Criteria"]["Max Generations"] = 40

  e["Variables"][0]["Name"] = "sigma"
  e["Variables"][0]["Bayesian Type"] = "Hyperparameter"
  e["Variables"][0]["Prior Distribution"] = "Uniform 0"
  e["Variables"][0]["Initial Value"] = 5.0  # Initial hyperparameter value
  e["Variables"][0]["Upper Bound"] = 15
  e["Variables"][0]["Lower Bound"] = 0

  # define a variable for each coordinate of mu
  for i in range(distrib1._p.nDimensions):
    e["Variables"][1 + i]["Name"] = "mu" + str(i)
    e["Variables"][1 + i]["Bayesian Type"] = "Latent"
    e["Variables"][1 + i]["Prior Distribution"] = "Uniform 1"
    e["Variables"][1 + i]["Initial Value"] = 0

  e["Distributions"][0]["Name"] = "Uniform 0"
  e["Distributions"][0]["Type"] = "Univariate/Uniform"
  e["Distributions"][0]["Minimum"] = 0
  e["Distributions"][0]["Maximum"] = 5

  e["Distributions"][1]["Name"] = "Uniform 1"
  e["Distributions"][1]["Type"] = "Univariate/Uniform"
  e["Distributions"][1]["Minimum"] = -5
  e["Distributions"][1]["Maximum"] = 5

  # Configuring results path
  e["File Output"]["Path"] = '_korali_result_saem'
  e["Random Seed"] = 0xC0FFEE

  #k["Conduit"]["Type"] = "Concurrent"
  #k["Conduit"]["Concurrent Jobs"] = 4
  #k["Conduit"]["Type"] = "Distributed"

  k.run(e)


if __name__ == '__main__':
  main()
