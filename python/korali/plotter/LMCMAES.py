#! /usr/bin/env python3

import json
import numpy as np
import matplotlib.pyplot as plt
from korali.plotter.helpers import hlsColors, drawMulticoloredLine


# Plot CMAES results (read from .json files)
def plot(genList, **kwargs):
  firstKey = next(iter(genList))
  fig, ax = plt.subplots(2, 2, num='Korali Results', figsize=(8, 8))

  numdim = len(genList[firstKey]['Variables'])
  numgens = len(genList)

  lastGen = 0
  for i in genList:
    if genList[i]['Current Generation'] > lastGen:
      lastGen = genList[i]['Current Generation']

  fval = [0.0] * numgens
  dfval = [0.0] * numgens
  genIds = [0.0] * numgens
  sigma = [0.0] * numgens
  psL2 = [0.0] * numgens
  objVec = [None] * numdim

  for i in range(numdim):
    objVec[i] = [None] * numgens

  curPos = 0
  for gen in genList:
    genIds[curPos] = genList[gen]['Current Generation']
    fval[curPos] = genList[gen]['Solver']['Current Best Value']
    dfval[curPos] = abs(genList[gen]['Solver']['Current Best Value'] -
                        genList[gen]['Solver']['Best Ever Value'])
    sigma[curPos] = genList[gen]['Solver']['Sigma']
    psL2[curPos] = genList[gen]['Solver']['Conjugate Evolution Path L2 Norm']
    for i in range(numdim):
      objVec[i][curPos] = genList[gen]['Solver']['Current Best Variables'][i]
    curPos = curPos + 1

  plt.suptitle('CMAES Diagnostics', fontweight='bold', fontsize=12)

  names = [genList[firstKey]['Variables'][i]['Name'] for i in range(numdim)]

  # Upper Left Plot
  ax[0, 0].grid(True)
  ax[0, 0].set_yscale('log')
  #drawMulticoloredLine(ax[0,0], genIds, fval, 0.0, 'r', 'b', '$| F |$')
  ax[0, 0].plot(genIds, fval, color='r', label='$| F |$')
  ax[0, 0].plot(genIds, dfval, 'x', color='#34495e', label='$| F - F_{best} |$')
  ax[0, 0].plot(genIds, sigma, color='#F8D030', label='$\sigma$')
  ax[0, 0].plot(genIds, psL2, color='k', label='$|| \mathbf{p}_{\sigma} ||$')

  ax[0, 0].legend(
      bbox_to_anchor=(0, 1.00, 1, 0.2),
      loc="lower left",
      mode="expand",
      ncol=3,
      handlelength=1,
      fontsize=8)

  colors = hlsColors(numdim)

  # Upper Right Plot
  ax[0, 1].set_title('Objective Variables')
  ax[0, 1].grid(True)
  for i in range(numdim):
    ax[0, 1].plot(genIds, objVec[i], color=colors[i], label=names[i])
  ax[0, 1].legend(
      bbox_to_anchor=(1.04, 0.5),
      loc="center left",
      borderaxespad=0,
      handlelength=1)

  # Lower Right Plot
  ax[1, 0].set_title('Square Root of Eigenvalues of $\mathbf{C}$')
  ax[1, 0].grid(True)
  ax[1, 0].set_yscale('log')

  # Lower Left Plot
  ax[1, 1].set_title('$\sigma \sqrt{diag(\mathbf{C})}$')
  ax[1, 1].grid(True)
  ax[1, 1].set_yscale('log')
