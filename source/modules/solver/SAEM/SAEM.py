#! /usr/bin/env python3

import json
import numpy as np
import matplotlib.pyplot as plt
from korali.plotter.helpers import hlsColors, drawMulticoloredLine
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


def plotVariables(genList):
  numgens = len(genList)

  lastGen = 0
  generations = []
  for i in genList:
    generations.append(genList[i]["Current Generation"])
    if genList[i]['Current Generation'] > lastGen:
      lastGen = genList[i]['Current Generation']

  some_gen = list(genList.keys())[0]
  numLatent = genList[some_gen]["Solver"]["Number Latent"]
  numHyper = genList[some_gen]["Solver"]["Number Hyperparameters"]
  numSamples = genList[some_gen]["Solver"]["Number Samples Per Step"]
  sample_means = np.zeros((len(genList), numLatent))
  sample_sdevs = np.zeros((len(genList), numLatent))
  hyperparams = np.zeros((len(genList), numHyper))
  gammas = np.zeros((len(genList)))

  # determine which are latent, vs. hyperparameters
  latentVars = []
  hyperVars = []
  for var_dict in genList[some_gen]["Variables"]:
    if var_dict["Bayesian Type"] == "Hyperparameter":
      hyperVars.append(var_dict)
    else:
      latentVars.append(var_dict)

  for idx, i in enumerate(genList):
    sample_means[idx, ...] = genList[i]["Solver"]["Current Sample Means"]
    sample_sdevs[
        idx, ...] = genList[i]["Solver"]["Current Sample Standard Deviations"]
    hyperparams[idx, ...] = genList[i]["Solver"]["Current Hyperparameters"]
    gammas[idx] = genList[i]["Solver"]["Gamma"]

  # Create an "outer" subplot for the two column titles
  fig, ax0 = plt.subplots(nrows=1, ncols=2, figsize=(8, 20), dpi=60)
  ax0[0].set_title("Latent Variables", y=1.03, fontdict={'fontweight': 8, 'fontsize': 20})
  ax0[1].set_title("Hyperparameters", y=1.03, fontdict={'fontweight': 8, 'fontsize': 20})

  # Make outer plot invisible
  ax0[0].tick_params(labelcolor=(1., 1., 1., 0.0), top='off', bottom='off', left='off', right='off')
  ax0[0]._frameon = False
  ax0[1].tick_params(labelcolor=(1., 1., 1., 0.0), top='off', bottom='off', left='off', right='off')
  ax0[1]._frameon = False
  ax0[0].tick_params(
      axis='both',  # changes apply to the x-axis
      which='both',  # both major and minor ticks are affected
      bottom=False,  # ticks along the bottom edge are off
      top=False,  # ticks along the top edge are off
      labelbottom=False)
  ax0[1].tick_params(
      axis='both',
      which='both',
      bottom=False,
      top=False,
      labelbottom=False)

  fig.subplots_adjust(hspace=.8)

  # suptitle?
  plt.suptitle(
      'SAEM Plotter - \nNumber of Samples: {0}\n'.format(str(numSamples)),
      fontweight='bold',
      fontsize=20)
  for latentIdx in range(numLatent):
    ax = fig.add_subplot(max(numLatent, numHyper) + 1, 2, 2 * latentIdx + 1)
    ax.errorbar(x=generations, y=sample_means[:, latentIdx], yerr=sample_sdevs[:, latentIdx])
    ax.set_title(latentVars[latentIdx]["Name"])
  # fig, ax = plt.subplots(nrows=max(numLatent, numHyper) + 1, ncols=1, figsize=(15,8))
  for hyperIdx in range(numHyper):
    ax = fig.add_subplot(max(numLatent, numHyper) + 1, 2, 2 * hyperIdx + 2)
    ax.plot(generations, hyperparams[:, hyperIdx])
    ax.set_title(hyperVars[hyperIdx]["Name"])
  ax = fig.add_subplot(max(numLatent, numHyper) + 1, 2, 2 * max(numLatent, numHyper) + 1)
  ax.plot(generations, gammas)
  ax.set_title("gamma")

  return fig, ax


def plot(genList, args):

  fig, ax = plotVariables(genList)
