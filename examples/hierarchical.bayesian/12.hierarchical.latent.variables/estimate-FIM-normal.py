import sys
sys.path.append('./_model/normal')
sys.path.append('./_model')
from model import *
from load_data import *

import korali


def main():

  # * Load the data.
  #   It is stored together with other information such as data dimensions in object "d":
  d = NormalData()

  k = korali.Engine()
  e = korali.Experiment()

  e["Problem"]["Type"] = "Bayesian/Latent/HierarchicalReference"

  e["Problem"]["Likelihood Model"] = "Normal"
  e["Problem"]["Reference Data"] = d.y_values
  # * Next, define the computational models, y, sdev = f(x, theta), g(x, theta)

  ## Warning: The i=i is necessary to capture the current i.
  ## Just writing
  ##   "lambda sample, i: logisticModelFunction(sample, x_vals[i])"
  ## will capture i by reference and thus not do what is intended.

  e["Problem"]["Computational Models"] = [
      lambda sample, i=i: normalModelFunction(sample, d.x_values[i])
      for i in range(d.nIndividuals)
  ]

  # FIM estimation is only supported for diagonal covariance matrices
  e["Problem"]["Diagonal Covariance"] = True

  e["Distributions"][0]["Name"] = "Uniform 0"
  e["Distributions"][0]["Type"] = "Univariate/Uniform"
  e["Distributions"][0]["Minimum"] = -100
  e["Distributions"][0]["Maximum"] = 100

  e["Distributions"][1]["Name"] = "Uniform 1"
  e["Distributions"][1]["Type"] = "Univariate/Uniform"
  e["Distributions"][1]["Minimum"] = 0
  e["Distributions"][1]["Maximum"] = 100

  # * Define the variables:
  #   We only define one prototype latent variable vector for individual 0.
  #   The others will be automatically generated by Korali, as well as all hyperparameters.

  # We define one normal and one lognormal variable.

  e["Variables"][0]["Name"] = "Theta 1"
  e["Variables"][0]["Initial Value"] = 2
  e["Variables"][0]["Latent Variable Distribution Type"] = "Normal"
  e["Variables"][0][
      "Prior Distribution"] = "Uniform 0"  # not used, but required

  e["Variables"][1]["Name"] = "Theta 2"
  e["Variables"][1]["Initial Value"] = 2
  e["Variables"][1]["Latent Variable Distribution Type"] = "Log-Normal"
  e["Variables"][1][
      "Prior Distribution"] = "Uniform 1"  # not used, but required

  e["Solver"]["Type"] = "LatentVariableFIM"
  e["Solver"]["Number Chains"] = 1
  e["Solver"]["MCMC Outer Steps"] = 1000
  e["Solver"]["MCMC Subchain Steps"] = [2, 2, 0]
  e["Solver"]["MCMC Target Acceptance Rate"] = 0.4
  # e["Solver"]["Termination Criteria"]["Max Generations"] = 1

  # Set values for the hyperparameters.
  # Insert the hyperparameter estimates from a run of HSAEM, for example:
  e["Solver"]["Hyperparameters Mean"] = [4.99, 0.95]
  # we can pass the covariance as its diagonal entries:
  e["Solver"]["Hyperparameters Diagonal Covariance"] = [0.0093771, 0.058124]

  # Configure how results will be stored to a file:
  e["File Output"]["Frequency"] = 1
  e["File Output"]["Path"] = "_korali_result_FIM_normal/"
  # We choose a non-default output directory -
  # for plotting results, we can later set the directory with:
  #   python3 -m korali.plotter --dir _korali_result_FIM_normal/.
  # But for FIM estimation, there is currently no plotting available.

  # Configure console output:
  e["Console Output"]["Frequency"] = 1
  e["Console Output"]["Verbosity"] = "Detailed"

  # k["Conduit"]["Type"] = "Sequential"

  k.run(e)


if __name__ == '__main__':
  # # ** For debugging, try this: **
  # import sys, trace
  # sys.stdout = sys.stderr
  # tracer = trace.Trace(trace=1, count=0, ignoredirs=["/usr", sys.prefix])
  # tracer.runfunc(main)
  # # ** Else: **
  main()
