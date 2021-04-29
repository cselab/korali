#! /usr/bin/env python3

import json
import numpy as np
import matplotlib.pyplot as plt
from korali.plotter.helpers import hlsColors, drawMulticoloredLine


# Plot DEA results (read from .json files)
def plot(genList, **kwargs):
  firstKey = next(iter(genList))
  fig, ax = plt.subplots(2, 2, num='Korali Results', figsize=(8, 8))

  numdim = len(genList[firstKey]['Variables'])
  numgens = len(genList)

  lastGen = 0
  for i in genList:
    if genList[i]['Current Generation'] > lastGen:
      lastGen = genList[i]['Current Generation']

  cond = [0.0] * numgens
  fval = [0.0] * numgens
  dfval = [0.0] * numgens
  genIds = [0.0] * numgens
  width = [None] * numdim
  means = [None] * numdim
  objVec = [None] * numdim

  for i in range(numdim):
    objVec[i] = [0.0] * numgens
    width[i] = [0.0] * numgens
    means[i] = [0.0] * numgens

  curPos = 0
  for gen in genList:
    genIds[curPos] = genList[gen]['Current Generation']
    fval[curPos] = genList[gen]['Solver']['Current Best Value']
    dfval[curPos] = abs(genList[gen]['Solver']['Current Best Value'] -
                        genList[gen]['Solver']['Best Ever Value'])

    for i in range(numdim):
      means[i][curPos] = genList[gen]['Solver']['Current Mean'][i]
      width[i][curPos] = genList[gen]['Solver']['Max Distances'][i]
      objVec[i][curPos] = genList[gen]['Solver']['Current Best Variables'][i]
    curPos = curPos + 1

  plt.suptitle('DEA Diagnostics', fontweight='bold', fontsize=12)

  names = [genList[firstKey]['Variables'][i]['Name'] for i in range(numdim)]
  colors = hlsColors(numdim)

  # Upper Left Plot
  ax[0, 0].grid(True)
  ax[0, 0].set_yscale('log')
  drawMulticoloredLine(ax[0, 0], genIds, fval, 0.0, 'r', 'b', '$| F |$')
  ax[0, 0].plot(genIds, dfval, 'x', color='#34495e', label='$| F - F_{best} |$')
  #if ( (idx == 2) or (updateLegend == False) ):
  ax[0, 0].legend(
      bbox_to_anchor=(0, 1.00, 1, 0.2),
      loc="lower left",
      mode="expand",
      ncol=3,
      handlelength=1,
      fontsize=8)

  # Upper Right Plot
  ax[0, 1].set_title('Objective Variables')
  ax[0, 1].grid(True)
  for i in range(numdim):
    ax[0, 1].plot(genIds, objVec[i], color=colors[i], label=names[i])
  #if ( (idx == 2) or (updateLegend == False) ):
  ax[0, 1].legend(
      bbox_to_anchor=(1.04, 0.5),
      loc="center left",
      borderaxespad=0,
      handlelength=1)

  # Lower Right Plot
  ax[1, 0].set_title('Width Population')
  ax[1, 0].grid(True)
  for i in range(numdim):
    ax[1, 0].plot(genIds, width[i], color=colors[i])

  # Lower Left Plot
  ax[1, 1].set_title('Mean Population')
  ax[1, 1].grid(True)
  for i in range(numdim):
    ax[1, 1].plot(genIds, means[i], color=colors[i], label=names[i])
  #if ( (idx == 2) or (updateLegend == False) ):
  ax[1, 1].legend(
      bbox_to_anchor=(1.04, 0.5),
      loc="center left",
      borderaxespad=0,
      handlelength=1)
