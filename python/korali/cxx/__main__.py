#! /usr/bin/env python3
import os
import sys
import ast
import sysconfig
import os
import subprocess

import libkorali as lk

def main():
  fileDir = os.path.dirname(os.path.realpath(__file__))
  koraliDir = os.path.abspath(fileDir + '/../')

  configFile = open(fileDir + '/flags.in', "r")
  configFileContents = configFile.read()
  configDict = ast.literal_eval(configFileContents)
  configFile.close()

  if (len(sys.argv) != 2):
    print('[Korali] Syntax error on call to korali.cxx module: Exactly one argument is required (--cflags, --libs, or --compiler).')
    exit(-1)
        
  if (sys.argv[1] == '--cflags'):
    correctSyntax = True
    pythonCFlagsCommand = subprocess.Popen("python3-config --includes", shell=True, stdout=subprocess.PIPE)
    pythonCFlags = pythonCFlagsCommand.stdout.read().decode()
    flags = '-std=c++17' + ' -I' + koraliDir + '/include' + ' -I' + sysconfig.get_path("include") + ' -I' + sysconfig.get_path("platinclude") + ' -I' + configDict['PYBIND11_INCLUDES'] + ' ' + pythonCFlags

  if (sys.argv[1] == '--libs'):
    correctSyntax = True
    
    try:
     pythonLibsCommand = subprocess.Popen("python3-config --ldflags --embed", shell=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
     pythonLibsCommand = subprocess.Popen("python3-config --ldflags", shell=True, stdout=subprocess.PIPE)
    pythonLibs = pythonLibsCommand.stdout.read().decode()
    
    # Looking for Korali library
    koraliLib = os.path.realpath(lk.__file__)
    flags = '-L' + koraliDir + ' -L' + koraliDir + '/../../../../lib' + ' -L' + koraliDir + '/../../../../lib64' + ' ' + koraliLib + ' ' + pythonLibs

  if (sys.argv[1] == '--compiler'):
    correctSyntax = True
    flags = configDict['CXX']

  if (correctSyntax == False):
   print('[Korali] Syntax error on call to korali.cxx module: Argument \'{0}\' not recognized (--cflags, --libs, or --compiler).'.format(sys.argv[1]))
   exit(-1)

  print(flags + ' ')

if __name__ == '__main__':
  main()
