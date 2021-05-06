#! /usr/bin/env python3
import sys
import os
import json
import shutil
import copy
import glob
import argparse

def processExample(source, destination, exampleRelPath, exampleName):
  examplePath = os.path.join(source, exampleRelPath)
  exampleReadmeFile = examplePath + '/README.rst'
  exampleOutputDir = os.path.abspath(os.path.join( destination + exampleRelPath, os.pardir))

  print('Processing file: ' + exampleReadmeFile)

  exampleReadmeString = '.. _example_' + exampleRelPath.lower().replace('./', '').replace('/', '-').replace(' ', '') + ':\n\n'

  # Creating subfolder list
  subFolderList = []
  list_dir = os.listdir(examplePath)
  for f in list_dir:
    fullPath = os.path.join(examplePath, f)
    if not os.path.isfile(fullPath):
      if (not '.o/' in fullPath and not '.d/' in fullPath and not '/_' in fullPath):
        subFolderList.append(f)

  # Creating example's folder, if not exists
  if not os.path.exists(exampleOutputDir):
    os.mkdir(exampleOutputDir)

  # Determining if its a parent or leaf example
  isParentExample = True
  if subFolderList == []:
    isParentExample = False

  # If there is a test script, do not proceed further
  if os.path.isfile(examplePath + '/.run_test.sh'):
    isParentExample = False

  # If its leaf, link to source code
  if (isParentExample == False):
    exampleReadmeString += '.. hint::\n\n'
    exampleReadmeString += '   Example code: `https://github.com/cselab/korali/tree/master/examples/' + exampleRelPath.replace(
        './', ''
    ) + '/ <https://github.com/cselab/korali/tree/master/examples/' + exampleRelPath.replace(
        './', '') + '/>`_\n\n'

  # Copying any images in the source folder
  for file in glob.glob(r'' + examplePath + '/*.png'):
    shutil.copy(file, exampleOutputDir)

  # Reading original rst
  with open(exampleReadmeFile, 'r') as file:
    exampleReadmeString += file.read() + '\n\n'

  # If its parent, construct children examples
  if (isParentExample == True):
    exampleReadmeString += '**Sub-Categories**\n\n'
    exampleReadmeString += '.. toctree::\n'
    exampleReadmeString += '   :titlesonly:\n\n'

    for f in subFolderList:
      subExampleFullPath = os.path.join(examplePath, f)
      if (not '/_' in subExampleFullPath):
        exampleReadmeString += '   ' + exampleName + '/' + f + '\n'
        subPath = os.path.join(exampleRelPath, f)
        processExample(source, destination, subPath, f)

  # Saving Example's readme file
  exampleReadmeString += '\n\n'
  with open(exampleOutputDir + '/' + exampleName + '.rst', 'w') as file:
    file.write(exampleReadmeString)


def build_examples(source, destination):
  shutil.rmtree(destination, ignore_errors=True, onerror=None)
  os.makedirs(destination)
  
  list_dir = os.listdir(source)
  for f in list_dir:
    fullPath = os.path.join(source, f)
    if not os.path.isfile(fullPath):
      if (not '.o/' in fullPath and not '.d/' in fullPath and not '/_' in fullPath and not 'features' in fullPath):
        processExample(source, destination, f, f)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--destination", help="Save the generated files in this folder")
  parser.add_argument("--source", help="Read files from this folder")
  args = parser.parse_args()

  build_examples(args.source, args.destination) 
