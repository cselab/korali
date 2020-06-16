#!/usr/bin/env python3

import korali
import numpy as np

def create_train_data(n=20, L=2):
  """ create synthetic data to train on """
  x = np.linspace(-L/2, L/2, n)
  y = x**2
  return x, y

k = korali.Engine()
e = korali.Experiment()

e['Random Seed'] = 0xC0FFEE
e['Problem']['Type'] = 'Supervised Learning'

xtrain, ytrain = create_train_data()

e['Variables'][0]['Name'] = 'X'
e['Variables'][0]['Type'] = 'Input'
e['Variables'][0]['Training Data'] = xtrain.tolist()

e['Variables'][1]['Name'] = 'Y'
e['Variables'][1]['Type'] = 'Output'
e['Variables'][1]['Training Data'] = ytrain.tolist()

e['Solver']['Type'] = 'Gaussian Process'
e['Solver']['Covariance Function'] = 'CovSEiso'

e['Solver']['Optimizer']['Type'] = 'Optimizer/Rprop'
e['Solver']['Optimizer']['Termination Criteria']['Max Generations'] = 1000
e['Solver']['Optimizer']['Termination Criteria']['Parameter Relative Tolerance'] = 1e-8

e['Console Output']['Verbosity'] = 'Normal'
e['Console Output']['Frequency'] = 10
e['File Output']['Frequency'] = 100
e["File Output"]["Path"] = "_korali_result_surrogate"

k.run(e)

show_figure = False

if show_figure:
  xtest = np.linspace(-1, 1, 100)
  xtest = xtest.reshape((len(xtest), 1))
  ytest = np.array(e.evaluate(xtest.tolist()))

  import matplotlib.pyplot as plt

  fig = plt.figure(0)
  ax = fig.subplots()

  ax.plot(xtrain, ytrain, 'ob')
  ax.plot(xtest.flatten(), ytest[:,0], '-r')
  plt.show()
