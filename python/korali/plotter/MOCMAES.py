#! /usr/bin/env python3

import json
import numpy as np
import matplotlib.pyplot as plt
from korali.plotter.helpers import hlsColors, drawMulticoloredLine
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

plotSamples = False

#Plot scatter plot in upper triangle of figure
def plot_upper_triangle(ax, theta, f=None):
  dim = theta.shape[1]
  for i in range(dim):
    for j in range(i + 1, dim):
      if f:
        ax[i, j].scatter(
            theta[:, i], theta[:, j], marker='o', s=3, alpha=0.5, c=f)
      else:
        ax[i, j].plot(theta[:, i], theta[:, j], '.', markersize=3)
      ax[i, j].grid(b=True, which='both')
      ax[i, j].set_xlabel("F"+str(i))
      ax[i, j].set_ylabel("F"+str(j))


#Plot scatter plot in lower triangle of figure
def plot_lower_triangle(ax, theta, f=None):
  dim = theta.shape[1]
  for i in range(dim):
    for j in range(0, i):
      if f:
        ax[i, j].scatter(
            theta[:, i], theta[:, j], marker='o', s=3, alpha=0.5, c=f)
      else:
        ax[i, j].plot(theta[:, i], theta[:, j], '.', markersize=3)
      ax[i, j].grid(b=True, which='both')
      ax[i, j].set_xlabel("F"+str(i))
      ax[i, j].set_ylabel("F"+str(j))


def plotGen(genList, idx):
    numgens = len(genList)

    lastGen = 0
    for i in genList:
        if genList[i]['Current Generation'] > lastGen:
            lastGen = genList[i]['Current Generation']

    numObjectives = genList[lastGen]['Problem']['Num Objectives']

    if plotSamples and numObjectives > 1:
          sampleVals = np.array(genList[lastGen]['Solver']['Sample Value Collection'])

          isFinite = [~np.isnan(s - s).any() for s in sampleVals]  # Filter trick
          sampleVals = sampleVals[isFinite]

          numentries = len(sampleVals)

          fig, ax = plt.subplots(numObjectives, numObjectives, figsize=(8, 8))
          samplesTmp = np.reshape(sampleVals, (numentries, numObjectives))
          plt.suptitle(
              'MO-CMA-ES Plotter - \nNumber of Samples {0}'.format(str(numentries)),
              fontweight='bold',
              fontsize=12)

          plot_upper_triangle(ax, samplesTmp)
          plot_lower_triangle(ax, samplesTmp)

          for i in range(numObjectives):
            ax[i, i].set_xticklabels([])
            ax[i, i].set_yticklabels([])

    else:
        fig, ax = plt.subplots(2, 2, num='Korali Results', figsize=(8, 8))
        firstKey = next(iter(genList))
        numdim = len(genList[firstKey]['Variables'])
        populationsize = genList[firstKey]['Solver']['Population Size']
        numgens = len(genList)

        lastGen = 0
        for i in genList:
            if genList[i]['Current Generation'] > lastGen:
                lastGen = genList[i]['Current Generation']

        cond = np.zeros((numgens, numObjectives))
        absfval = np.zeros((numgens, numObjectives))
        dfval = np.zeros((numgens, numObjectives))
        theta = np.zeros((numgens, numdim*numObjectives))
        dtheta = np.zeros((numgens, numObjectives))
        cond = np.zeros((numgens, populationsize))
        minsdev = np.zeros((numgens, populationsize))
        genIds = np.zeros(numgens)
        for idx, gen in enumerate(genList):
            genIds[idx] = genList[gen]['Current Generation']
            absfval[idx] = abs(np.array(genList[gen]['Solver']['Current Best Values']))
            dfval[idx] = abs(np.array(genList[gen]['Solver']['Current Best Value Differences']))
            theta[idx] = np.reshape(np.array(genList[gen]['Solver']['Current Best Variables']), numdim*numObjectives)
            dtheta[idx] = abs(np.array(genList[gen]['Solver']['Current Best Variable Differences']))
            cond[idx] = np.array(genList[gen]['Solver']['Current Max Standard Deviations']) / np.array(genList[gen]['Solver']['Current Min Standard Deviations'])
            minsdev[idx] = np.array(genList[gen]['Solver']['Current Min Standard Deviations'])

        plt.suptitle('MO-CMA-ES Diagnostics', fontweight='bold', fontsize=12)

        names = [genList[firstKey]['Variables'][i]['Name'] for i in range(numdim)]

        # Upper Left Plot
        ax[0, 0].set_title('Best Objective Values and Differences')
        ax[0, 0].set_yscale('log')
        ax[0, 0].plot(genIds, absfval)
        ax[0, 0].plot(genIds, dfval, 'x', color='#34495e')

        # Upper Right Plot
        ax[0, 1].set_title('Best Objective Variables')
        ax[0, 1].plot(genIds, theta)
        #ax[0, 1].plot(genIds, dtheta, 'x', color='#34495e')

        # Lower Left Plot
        ax[1, 0].set_title('Condition')
        ax[1, 0].set_yscale('log')
        ax[1, 0].plot(genIds, cond)

        # Lower Right Plot
        ax[1, 1].set_title('Min Standard Deviations')
        ax[1, 1].set_yscale('log')
        ax[1, 1].plot(genIds, minsdev)

def plot(genList, , **kwargs):
      numgens = len(genList)

      plotAll = kwargs['plotAll']
      if plotAll:
        for idx in genList:
          plotGen(genList, idx)
      else:
        lastGen = 0
        for i in genList:
          if genList[i]['Current Generation'] > lastGen:
            lastGen = genList[i]['Current Generation']
        plotGen(genList, lastGen)
