#!/usr/bin/env python3

import os
import sys
import json
import signal
import os.path
from os import path
import matplotlib
from matplotlib import cm
import matplotlib.colors as colors
import argparse
import numpy as np

signal.signal(signal.SIGINT, lambda x, y: exit(0))

parser = argparse.ArgumentParser(
    prog='korali.plotter',
    description='Show profiling information of a Korali execution.')
parser.add_argument(
    '--input',
    help='Json files with profiling information to read.',
    default='./profiling.json',
    nargs='+',
    required=False)
parser.add_argument(
    '--test',
    help='Run without graphics (for testing purpose)',
    action='store_true',
    required=False)
parser.add_argument(
    '--tend',
    help='Indicates the maximum time to report in the timeline',
    required=False,
    default='undefined')
parser.add_argument(
    '--output',
    help='Indicates the output file path. If not specified, it prints to screen.',
    required=False)
parser.add_argument(
    '--timeFormat',
    help='Indicates the format to use for the timeline.',
    required=False,
    choices=['Seconds', 'Minutes', 'Hours', 'Days'],
    default='seconds')

args = parser.parse_args()

if (args.test == True):
  print('[Korali] Testing profiler plotter for file: ' + str(args.input) + '...')
  matplotlib.use('Agg')

from matplotlib import pyplot

######################## Creating Time-based figure

#### Reading profiling files

experimentCount = 0
elapsedTime = 0
fullJs = {'Timelines': {}}

for file in args.input:
  if (not path.exists(file)):
    print('[Korali] Error: Could not find profiling information file: ' + file +
          ' ...')
    exit(-1)

  with open(file) as f:
    jsString = f.read()
    js = json.loads(jsString)

    currExperimentCount = js["Experiment Count"]
    if (currExperimentCount > experimentCount):
      experimentCount = currExperimentCount

  fullJs["Timelines"].update(js["Timelines"])
  if (float(js["Elapsed Time"]) > elapsedTime):
    elapsedTime = float(js["Elapsed Time"])
timelines = []
labels = []

if (args.tend == 'undefined'):
  tend = elapsedTime
else:
  tend = float(args.tend)

for x in fullJs["Timelines"]:
  timelines.append(fullJs["Timelines"][x])
  labels.append(x)

#### Preprocessing information

startLists = []
durationLists = []
experimentIdLists = []
for list in timelines:
  currentStartList = []
  currentDurationList = []
  currentSolverIdList = []
  for segment in list:
    currentStartList.append(segment["Start Time"])
    currentDurationList.append(segment["End Time"] - segment["Start Time"])
    currentSolverIdList.append(segment["Solver Id"])
  startLists.append(currentStartList)
  durationLists.append(currentDurationList)
  experimentIdLists.append(currentSolverIdList)

#### Setting Plot Format

height = 8
fig, ax = pyplot.subplots(1, 1, sharex=True, figsize=(25, height))

# Setting Y-axis limits
upperLimit = len(timelines) * 10
ax.set_ylim(0, upperLimit)

# Setting X-axis limits
ax.set_xlim(0, tend)

# Setting ticks on y-axis
yticks = []
for i in range(len(timelines)):
  yticks.append(10 + i * 10)
xticks = np.arange(0, tend + 1, tend / 10)
ax.set_xticks(xticks)
ax.set_yticks([])

xticklabels = []

timescale = 1
if (args.timeFormat == 'Minutes'):
  timescale = 60
if (args.timeFormat == 'Hours'):
  timescale = 3600
if (args.timeFormat == 'Days'):
  timescale = 86400

for tick in xticks:
  xticklabels.append("{:.1f}".format(tick / timescale))
ax.set_xticklabels(xticklabels)

# Setting graph attribute
ax.grid(False)

# Creating Color list
cMap = pyplot.get_cmap('plasma')
cNorm = colors.Normalize(vmin=0, vmax=experimentCount * 3)
scalarMap = cm.ScalarMappable(norm=cNorm, cmap=cMap)
colorMap = [scalarMap.to_rgba(i) for i in range(experimentCount * 3)]

for i in range(len(startLists)):
  colorList = [
      colorMap[experimentIdLists[i][j] * 3] for j in range(0, experimentCount)
  ]
  segList = [(startLists[i][j], durationLists[i][j])
             for j in range(0, len(startLists[i]))]
  ax.broken_barh(segList, (yticks[i] - 5, 9), facecolors=tuple(colorList))

####################### Creating Plot

pyplot.xticks(fontsize=16)
pyplot.yticks(fontsize=16)

yticks = np.linspace(0, upperLimit, num=10, endpoint=True)
ax.set_yticks(yticks)
ytickLabels = []
for tick in yticks:
  ytickLabels.append(str(int(tick / 10)))
ax.set_yticklabels(ytickLabels)

ax.set_ylabel('Worker History', fontsize=18)
ax.set_xlabel('Time (' + args.timeFormat + ')', fontsize=18)

if (args.output is None):
  pyplot.show()
else:
  pyplot.savefig(args.output, bbox_inches='tight')
