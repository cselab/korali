#! /usr/bin/env python3

import json
import numpy as np
import matplotlib.pyplot as plt
from korali.plotter.helpers import hlsColors, drawMulticoloredLine
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


# Plot histogram of sampes in diagonal
def plot_histogram(ax, theta):
  dim = theta.shape[1]
  num_bins = 50

  for i in range(dim):

    if (dim == 1):
      ax_loc = ax
    else:
      ax_loc = ax[i, i]

    hist, bins, _ = ax_loc.hist(
        theta[:, i], num_bins, density=True, color='lightgreen', ec='black')

    if i == 0:

      # Rescale hist to scale of theta -> get correct axis titles
      widths = np.diff(bins)
      if (dim > 1):
        hist = hist / np.max(hist) * (
            ax_loc.get_xlim()[1] - ax_loc.get_xlim()[0])
        bottom = ax_loc.get_xlim()[0]
        ax_loc.cla()
        ax_loc.bar(
            bins[:-1],
            hist,
            widths,
            color='lightgreen',
            ec='black',
            bottom=bottom)
        ax_loc.set_ylim(ax_loc.get_xlim())
        ax_loc.set_xticklabels([])
      else:
        ax_loc.cla()
        ax_loc.bar(bins[:-1], hist, widths, color='lightgreen', ec='black')

    elif i == theta.shape[1] - 1:
      ax_loc.set_yticklabels([])

    else:
      ax_loc.set_xticklabels([])
      ax_loc.set_yticklabels([])
    ax_loc.tick_params(axis='both', which='both', length=0)


#Plot scatter plot in upper triangle of figure
def plot_upper_triangle(ax, theta, lik=False):
  dim = theta.shape[1]
  if (dim == 1):
    return

  for i in range(dim):
    for j in range(i + 1, dim):
      if lik:
        ax[i, j].scatter(
            theta[:, j], theta[:, i], marker='o', s=10, c=theta, alpha=0.5)
      else:
        ax[i, j].plot(theta[:, j], theta[:, i], '.', markersize=1)
      ax[i, j].set_xticklabels([])
      ax[i, j].set_yticklabels([])
      ax[i, j].grid(b=True, which='both')


#Plot 2d histogram in lower triangle of figure
def plot_lower_triangle(ax, theta):
  dim = theta.shape[1]
  if (dim == 1):
    return

  for i in range(dim):
    for j in range(i):
      # returns bin values, bin edges and bin edges
      H, xe, ye = np.histogram2d(theta[:, j], theta[:, i], 10, density=True)
      # plot and interpolate data
      ax[i, j].imshow(
          H.T,
          aspect="auto",
          interpolation='spline16',
          origin='lower',
          extent=np.hstack((ax[j, j].get_xlim(), ax[i, i].get_xlim())),
          cmap=plt.get_cmap('jet'))

      if i < theta.shape[1] - 1:
        ax[i, j].set_xticklabels([])
      if j > 0:
        ax[i, j].set_yticklabels([])


def plot(genList, **kwargs):
  numgens = len(genList)

  lastGen = 0
  for i in genList:
    if genList[i]['Current Generation'] > lastGen:
      lastGen = genList[i]['Current Generation']

  numdim = len(genList[lastGen]['Variables'])
  samples = genList[lastGen]['Solver']['Sample Database']
  numentries = len(samples)

  fig, ax = plt.subplots(numdim, numdim, figsize=(8, 8))
  samplesTmp = np.reshape(samples, (numentries, numdim))
  plt.suptitle(
      'MCMC Plotter - \nNumber of Samples {0}\n'.format(str(numentries)),
      fontweight='bold',
      fontsize=12)
  plot_histogram(ax, samplesTmp)
  plot_upper_triangle(ax, samplesTmp, False)
  plot_lower_triangle(ax, samplesTmp)
