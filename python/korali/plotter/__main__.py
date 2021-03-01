#! /usr/bin/env python3
import os
import sys
import signal
import json
import argparse
import matplotlib
import importlib

curdir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

# Check if name has .png ending
def validateOutput(output):
  if not output.endswith(".png"):
    print(
        "[Korali] Error: Outputfile '{0}' must end with '.png' suffix.".format(
            output))
    sys.exit(-1)


def main(path, check, test, output, plotAll=False):

  if (check == True):
    print("[Korali] Plotter correctly installed.")
    exit(0)

  if test or output:
    matplotlib.use('Agg')

  if output:
    validateOutput(output)

  # This import has to be after matplotlib.use('Agg').
  import matplotlib.pyplot as plt

  signal.signal(signal.SIGINT, lambda x, y: exit(0))

  configFile = path + '/gen00000000.json'
  if (not os.path.isfile(configFile)):
    print(
        "[Korali] Error: Did not find any results in the {0} folder...".format(
            path))
    exit(-1)

  with open(configFile) as f:
    js = json.load(f)
  configRunId = js['Run ID']

  resultFiles = [
      f for f in os.listdir(path)
      if os.path.isfile(os.path.join(path, f)) and f.startswith('gen')
  ]
  resultFiles = sorted(resultFiles)

  genList = {}

  for file in resultFiles:
    with open(path + '/' + file) as f:
      genJs = json.load(f)
      solverRunId = genJs['Run ID']

      if (configRunId == solverRunId):
        curGen = genJs['Current Generation']
        genList[curGen] = genJs

  del genList[0]

  solverName = js['Solver']['Type'].lower()
  solverDir = ""
  moduleName = ""

  if ("cmaes" in solverName):
   solverDir = curdir + '/CMAES'
   moduleName = '.CMAES'

  if ("dea" in solverName):
   solverDir = curdir + '/DEA'
   moduleName = '.DEA'

  if ("lmcmaes" in solverName):
   solverDir = curdir + '/LMCMAES'
   moduleName = '.LMCMAES'

  if ("mocmaes" in solverName):
   solverDir = curdir + '/MOCMAES'
   moduleName = '.MOCMAES'

  if ("mcmc" in solverName):
   solverDir = curdir + '/MCMC'
   moduleName = '.MCMC'

  if ("nested" in solverName):
   solverDir = curdir + '/Nested'
   moduleName = '.Nested'

  if ("tmcmc" in solverName):
   solverDir = curdir + '/TMCMC'
   moduleName = '.TMCMC'

  if (solverDir == ""):
   print("[Korali] Solver '{0}' does not provide support for plotting.".format(solverName))
   exit(0)

  sys.path.append(solverDir)
  solverLib = importlib.import_module(moduleName, package="plotter")
  solverLib.plot(genList, plotAll=plotAll )

  if not output:
    plt.show()
  else:
    plt.savefig(output)

  return 0

if __name__ == '__main__':
  parser = argparse.ArgumentParser(
      prog='korali.plotter',
      description='Plot the results of a Korali execution.')
  parser.add_argument(
      '--dir',
      help='directory of result files',
      default='_korali_result',
      required=False)
  parser.add_argument(
      '--check',
      help='verifies that korali.plotter is available',
      action='store_true',
      required=False)
  parser.add_argument(
      '--test',
      help='run without graphics (for testing purpose)',
      action='store_true',
      required=False)
  parser.add_argument(
      '--output', help='save figure to file', type=str, default="")
  parser.add_argument(
      '--all', help='plot all generations', action='store_true', required=False)
  args = parser.parse_args()

  main(args.dir, args.check, args.test, args.output, args.all)