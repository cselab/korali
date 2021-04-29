#!/usr/bin/env python3
from pathlib import Path
import codeBuilders.auxiliar as aux
import os
import build
import build_variables_header
import argparse

class Args:
  def __init__(self, input, config=None, output=None):
    self.input = input
    self.config = config
    self.output = output


def makeTestPath( destination, codeFilePath ):
  p = Path( codeFilePath )
  p = p.resolve()
  r = aux.pathSplitAtDir( p, 'source' )
  r = p.relative_to(r)
  t = Path(destination).joinpath(r)
  suffix = t.suffix.replace('_','')
  t = t.with_suffix(suffix)
  return str(t)


def buildAllSource(source, destination):
  # Build modules source
  configFileList = []
  headerFileList = []
  sourceFileList = []
  outHeaderFileList = []
  outSourceFileList = []
  modulesDir = source + '/modules'
  for moduleDir, relDir, fileNames in os.walk( modulesDir ):
    for fileName in fileNames:
      if '.config' in fileName:
        _name = os.path.splitext(fileName)[0]
        configFileList.append(os.path.abspath(os.path.join(moduleDir,_name+'.config')))
  
        _file = os.path.abspath(os.path.join(moduleDir,_name+'._hpp'))
        headerFileList.append(_file)
        outHeaderFileList.append( makeTestPath(destination, _file) )
  
        _file = os.path.abspath(os.path.join(moduleDir,_name+'._cpp'))
        sourceFileList.append(_file)
        outSourceFileList.append( makeTestPath(destination, _file) )
  
  for config, inHeader, inSource, outHeader, outSource in \
    zip(configFileList, headerFileList, sourceFileList, outHeaderFileList, outSourceFileList):
      print( [inHeader,inSource], config, [outHeader,outSource] )
      args = Args( [inHeader,inSource], config, [outHeader,outSource] )
      build.main(args)
  
  
  # Build variables header
  variableHeaderTemplateFile = source + '/variable/variable._hpp'
  configFileList = []
  modulesDir = source + '/modules/'
  for moduleDir, relDir, fileNames in os.walk( modulesDir ):
    for fileName in fileNames:
      if '.config' in fileName:
        _name = os.path.splitext(fileName)[0]
        configFileList.append(os.path.join(moduleDir,_name+'.config'))
  
  outHeader = makeTestPath(destination, variableHeaderTemplateFile)
  args = Args( [variableHeaderTemplateFile] + configFileList, output=outHeader )
  
  build_variables_header.main(args)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--destination", help="Save the generated files in this folder")
  parser.add_argument("--source", help="Read source files from this folder")
  args = parser.parse_args()

  buildAllSource(args.source, args.destination) 
