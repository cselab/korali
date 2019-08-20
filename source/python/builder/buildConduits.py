import sys
import os
import json
from buildAux import *

def buildConduits(koraliDir):
 # Processing Conduits
 curdir = koraliDir + '/conduits' 
 
 # Conduits List
 conduitDetectionList = ''
 
 # Detecting Conduits
 conduitPaths  = [x[0] for x in os.walk(curdir)][1:]
 for conduitPath in conduitPaths:
  conduitName = conduitPath.replace(curdir + '/', '')
 
  # Loading JSON Configuration
  conduitJsonFile = conduitPath + '/' + conduitName + '.json'
  if (not os.path.isfile(conduitJsonFile)): continue 
  with open(conduitJsonFile, 'r') as file: conduitJsonString = file.read()
  conduitConfig = json.loads(conduitJsonString)

  ###### Adding Conduit to list
  conduitDetectionList += '  if(conduitType == "' + conduitConfig["Alias"] + '") conduit = new Korali::Conduit::' + conduitConfig["C++ Class"] + '();\n'
  
  ###### Producing conduit code

  conduitHeaderString = createHeaderDeclarations(conduitConfig)
  conduitCodeString = createSetConfiguration(conduitConfig)
  conduitCodeString += createGetConfiguration(conduitConfig)
  conduitCodeString += createCheckTermination(conduitConfig)

  ####### Producing header file
  
  # Loading template header .hpp file
  conduitTemplateHeaderFile = conduitPath + '/' + conduitName + '._hpp'
  with open(conduitTemplateHeaderFile, 'r') as file: conduitTemplateHeaderString = file.read()
  newHeaderString = conduitTemplateHeaderString.replace('private:', 'private: \n' + conduitHeaderString + '\n')
  
  # Saving new header .hpp file
  conduitNewHeaderFile = conduitPath + '/' + conduitName + '.hpp'
  print('[Korali] Creating: ' + conduitNewHeaderFile + '...')
  with open(conduitNewHeaderFile, 'w') as file: file.write(newHeaderString)
  
  ###### Creating code file
  
  conduitBaseFileName = conduitPath + '/' + conduitName + '._cpp'
  conduitNewCodeFile = conduitPath + '/' + conduitName + '.cpp'
  baseFileTime = os.path.getmtime(conduitBaseFileName)
  newFileTime = baseFileTime
  if (os.path.exists(conduitNewCodeFile)): newFileTime = os.path.getmtime(conduitNewCodeFile)
  
  if (baseFileTime >= newFileTime):
   with open(conduitBaseFileName, 'r') as file: conduitBaseCodeString = file.read()
   conduitBaseCodeString += '\n\n' + conduitCodeString
   print('[Korali] Creating: ' + conduitNewCodeFile + '...')
   with open(conduitNewCodeFile, 'w') as file: file.write(conduitBaseCodeString)

 ###### Creating base configuration file

 conduitBaseFileName = curdir + '/base._cpp'
 conduitNewCodeFile = curdir + '/base.cpp'
 baseFileTime = os.path.getmtime(conduitBaseFileName)
 newFileTime = baseFileTime
 if (os.path.exists(conduitNewCodeFile)): newFileTime = os.path.getmtime(conduitNewCodeFile)

 if (baseFileTime >= newFileTime):
   with open(conduitBaseFileName, 'r') as file: conduitBaseCodeString = file.read()
   newBaseString = conduitBaseCodeString.replace(' // Conduit list', conduitDetectionList)
   with open(conduitNewCodeFile, 'w') as file: file.write(newBaseString)

 ###### Creating base header file
 with open(curdir + '/base._hpp', 'r') as file: conduitBaseHeaderString = file.read()
 newBaseString = conduitBaseHeaderString
 with open(curdir + '/base.hpp', 'w+') as file: file.write(newBaseString)