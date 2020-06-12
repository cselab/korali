#!/usr/bin/env python3

import sys
sys.path.append('./_model')
from model import *
from tutorial_samplers import *

import numpy as np
import korali


def main():
  # Initialize the distribution
  distrib2 = ExampleDistribution2()

  distrib2_S = lambda s: distrib2.S(s)
  distrib2_zeta = lambda s: distrib2.zeta(s)
  distrib2_phi = lambda s: distrib2.phi(s)

  d2_numberLatentVars = distrib2._p.nPoints  # one for each datapoint
  d2_numberHyperparams = distrib2._p.nDimensions * distrib2._p.nClusters + 1

  d2_initialLatentValues = np.random.normal(0.5, 0.5, (d2_numberLatentVars))
  d2_initialHyperparams = np.random.normal(0, 1, (d2_numberHyperparams))

  gaussian_sampler_obj = MultimodalGaussianSampler(distrib2._p.points, distrib2._p.nDimensions, distrib2._p.nClusters)

  multimodal_gaussian_sampler = lambda s: gaussian_sampler_obj.sampleLatent(s)

  k = korali.Engine()
  e = korali.Experiment()

  e["Problem"]["Type"] = "Bayesian/Latent/ExponentialLatent"
  e["Problem"]["S Of Likelihood Model"] = distrib2_S
  e["Problem"]["Zeta Of Likelihood Model"] = distrib2_zeta
  e["Problem"]["Phi Of Likelihood Model"] = distrib2_phi
  e["Problem"]["S Dimension"] = distrib2.sufficientStatisticsDimension
  e["Problem"]["Latent Variable Sampler"] = multimodal_gaussian_sampler

  e["Solver"]["Type"] = "SAEM"
  e["Solver"]["Number Samples Per Step"] = 100
  e["Solver"]["Termination Criteria"]["Max Generations"] = 50

  e["Distributions"][0]["Name"] = "Uniform 0"
  e["Distributions"][0]["Type"] = "Univariate/Uniform"
  e["Distributions"][0]["Minimum"] = 0
  e["Distributions"][0]["Maximum"] = 5

  e["Distributions"][1]["Name"] = "Uniform 1"
  e["Distributions"][1]["Type"] = "Univariate/Uniform"
  e["Distributions"][1]["Minimum"] = -5
  e["Distributions"][1]["Maximum"] = 5

  e["Distributions"][2]["Name"] = "Multinomial 2"
  e["Distributions"][2]["Type"] = "Specific/Multinomial"


    # * Define which hyperparameters we use (all mu, and sigma)
  variable_counter = 0
  for cluster_idx in range(distrib2._p.nClusters):
    for dim in range(distrib2._p.nDimensions):
      e["Variables"][variable_counter]["Name"] = "mu_" + str(cluster_idx) + "_" + str(dim)
      e["Variables"][variable_counter]["Bayesian Type"] = "Hyperparameter"
      e["Variables"][variable_counter]["Prior Distribution"] = "Uniform 1"  # not used (?) but required
      e["Variables"][variable_counter]["Initial Value"] = d2_initialHyperparams[variable_counter]
      e["Variables"][variable_counter]["Upper Bound"] = e["Distributions"][1]["Maximum"]
      e["Variables"][variable_counter]["Lower Bound"] = e["Distributions"][1]["Minimum"]

      variable_counter += 1

  e["Variables"][variable_counter]["Name"] = "sigma"
  e["Variables"][variable_counter]["Bayesian Type"] = "Hyperparameter"
  e["Variables"][variable_counter]["Prior Distribution"] = "Uniform 0"  # We probably don't need a prior distribution for any variable -- Edit: yes, seems korali demands one
  e["Variables"][variable_counter]["Initial Value"] = 2.0
  e["Variables"][variable_counter]["Upper Bound"] = 5
  e["Variables"][variable_counter]["Lower Bound"] = 0
  variable_counter += 1

  # * Latent variables
  latent_counter = 0
  for cluster_idx in range(distrib2._p.nPoints):
    e["Variables"][variable_counter]["Name"] = "cluster_assignment_" + str(latent_counter)
    e["Variables"][variable_counter]["Bayesian Type"] = "Latent"
    e["Variables"][variable_counter]["Prior Distribution"] = "Multinomial 2"
    e["Variables"][variable_counter]["Initial Value"] = d2_initialLatentValues[latent_counter]

    variable_counter += 1
    latent_counter += 1

  # Configuring results path
  e["File Output"]["Path"] = '_korali_result_saem-mixture'
  e["File Output"]["Frequency"] = 50
  e["Console Output"]["Frequency"] = 10
  e["Console Output"]["Verbosity"] = "Detailed"
  e["Random Seed"] = 0xC0FFEE

  #k["Conduit"]["Type"] = "Concurrent"
  #k["Conduit"]["Concurrent Jobs"] = 4
  k.run(e)


if __name__ == '__main__':
  # ** For debugging, try this: **
  # import sys, trace
  # sys.stdout = sys.stderr
  # tracer = trace.Trace(trace=1, count=0, ignoredirs=["/usr", sys.prefix])
  # tracer.runfunc(main)
  # ** Else: **
  main()
