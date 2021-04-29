#!/usr/bin/env python3
import sys
import os
import json
import shutil
import argparse

testsDir = '../../../tests/'

def build_tests(testsDir, devDir):
  testPageFileSrc = devDir + '/testing.rst.base'
  with open(testPageFileSrc, 'r') as file:
    testPageString = file.read()
  
  unitTestList = ''
  statTestList = ''
  regTestList = ''
  
  # Detecting Tests
  testNames = os.listdir(testsDir)
  for testName in sorted(testNames):
    testPath = testsDir + '/' + testName
    if (os.path.isdir(testPath)):
      testReadmeFile = testsDir + '/' + testName + '/README.rst'
      with open(testReadmeFile, 'r') as file:
        testReadmeString = file.read()
      testTitle = testReadmeString.partition('\n')[0]
  
      if ('REG' in testPath):
        regTestList += '#. `' + testTitle + ' <https://github.com/cselab/korali/tree/master/tests/' + testName + '>`_\n'
      if ('UNIT' in testPath):
        unitTestList += '#. `' + testTitle + ' <https://github.com/cselab/korali/tree/master/tests/' + testName + '>`_\n'
      if ('STAT' in testPath):
        statTestList += '#. `' + testTitle + ' <https://github.com/cselab/korali/tree/master/tests/' + testName + '>`_\n'
  
      testDstPath = testName + '.rst'
  
  testPageString = testPageString.replace('< Regression Tests Go Here >',regTestList)
  testPageString = testPageString.replace('< Unit Tests Go Here >', unitTestList)
  testPageString = testPageString.replace('< Statistical Tests Go Here >',statTestList)
  testPageFileDst = open(devDir + '/testing.rst', 'w')
  testPageFileDst.write(testPageString)
  testPageFileDst.close()


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--destination", help="Save the generated files in this folder")
  parser.add_argument("--source", help="Read files from this folder")
  args = parser.parse_args()

  build_tests(args.source, args.destination) 
