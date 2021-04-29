#!/usr/bin/env python3
import sys
import os
import json
import shutil
import copy
import argparse


def getVariableName(v):
  cVarName = v["Name"].replace(" ", "")
  cVarName = '_' + cVarName[0].lower() + cVarName[1:]
  return cVarName


def getDataType(v):
  if (not "Type" in v):
    return '*real number*'
  cVarType = v["Type"]
  cVarType = cVarType.replace('*', '')
  cVarType = cVarType.replace('>', '')
  cVarType = cVarType.replace('int', '*integer*')
  cVarType = cVarType.replace('size_t', '*unsigned integer*')
  cVarType = cVarType.replace('double', '*real number*')
  cVarType = cVarType.replace('std::string', '*string*')
  cVarType = cVarType.replace('std::function<void(korali::Sample&)',
                              ':ref:`Computational Model <korali-model>`')
  cVarType = cVarType.replace('korali::Sample', ':ref:`Sample <korali-sample>`')
  cVarType = cVarType.replace('std::vector<std::vector<', 'List of Lists of ')
  cVarType = cVarType.replace('std::vector<', 'List of ')
  cVarType = cVarType.replace('bool', '*True/False*')
  cVarType = cVarType.replace('korali::Variable',
                              ':ref:`Variable <korali-variable>`')
  if ('korali::' in cVarType):
    classList = cVarType.replace('*', '').split('::')
    moduleLink = 'module-' + classList[1].lower()
    cVarType = upcase_first_letter(classList[1])
    for c in classList[2:]:
      cVarType += '/' + upcase_first_letter(c)
      moduleLink += '-' + c.lower()
    cVarType = classList[0].replace(
        'korali', '') + ':ref:`' + cVarType + ' <' + moduleLink + '>`'
  return cVarType


def getJsonPath(path):
  nameString = ''
  for item in path:
    nameString += '\\["' + item + '"\\]'
  return nameString


def recursiveUpdate(dest, defaults):
  if (isinstance(defaults, dict)):
    for k, x in defaults.items():
      if (not k in dest):
        dest[k] = copy.deepcopy(defaults[k])
      else:
        recursiveUpdate(dest[k], defaults[k])
  if (isinstance(defaults, list)):
    for k in range(len(defaults)):
      if (not k in dest):
        dest.append(copy.deepcopy(defaults[k]))
      else:
        recursiveUpdate(dest[k], defaults[k])


def createVariableDescription(rootPath, relPath, v):
  moduleTypePath = ''
  if ("problem" in relPath):
    moduleTypePath = '["Problem"]'
  if ("solver" in relPath):
    moduleTypePath = '["Solver"]'
  if ("conduit" in relPath):
    moduleTypePath = '["Conduit"]'
  if ("Variable" in rootPath):
    moduleTypePath = ''
  if ("Results" in rootPath):
    moduleTypePath = ''

  desc = '\n'
  desc += getJsonPath(v["Name"]).replace('"', '').replace('[', '').replace(
      ']', '').replace('\\\\', ' / ') + '\n'
  desc += ' - **Usage**: ' + rootPath + moduleTypePath + getJsonPath(
      v["Name"]).replace('\\', '') + ' = ' + getDataType(v) + '\n'
  desc += ' - **Description**: ' + v["Description"] + '\n'
  if ('Criteria' in v):
    desc += ' - **Criteria**: :code:`' + v["Criteria"] + '`\n'
  if ('Options' in v):
    desc += ' - **Options**: \n\n'
    for o in v["Options"]:
      desc += '      - "*' + o["Value"] + '*": ' + o["Description"] + '\n'
  if ('Produced By' in v):
    desc += ' - **Produced By**: \n\n'
    for s in v['Produced By']:
      desc += '    - :ref:`' + s + ' <module-solver-' + s.replace('/',
                                                                  '-') + '>`\n'
    desc += '\n'
  desc += '\n'
  return desc


def upcase_first_letter(s):
  return s[0].upper() + s[1:]


def processModule(parentModuleConfig, source, destination, moduleRelPath, moduleName):
  modulePath = os.path.join(source, moduleRelPath)
  moduleReadmeFile = modulePath + '/README.rst'
  moduleConfigFile = modulePath + '/' + moduleName + '.config'
  moduleOutputDir = destination + moduleRelPath

  print('Processing file: ' + moduleConfigFile)

  moduleReadmeString = '.. _module-' + moduleRelPath.lower().replace(
      '/', '-').replace(' ', '') + ':\n\n'

  # Loading configuration and readme files
  with open(moduleConfigFile, 'r') as file:
    moduleConfigString = file.read()
  with open(moduleReadmeFile, 'r') as file:
    moduleReadmeString += file.read()

  # Loading Module's Configuration
  moduleConfig = json.loads(moduleConfigString)
  recursiveUpdate(moduleConfig, parentModuleConfig)

  # Creating module's folder, if not exists
  if not os.path.exists(moduleOutputDir):
    os.mkdir(moduleOutputDir)

  # Creating subfolder list
  subFolderList = []
  list_dir = os.listdir(modulePath)
  for f in list_dir:
    fullPath = os.path.join(modulePath, f)
    if not os.path.isfile(fullPath):
      if (not '.o/' in fullPath and not '.d/' in fullPath):
       subModuleSourceFilePath = os.path.join(fullPath, f + '._cpp')
       if (os.path.exists(subModuleSourceFilePath)):
        subFolderList.append(f)

  # Determining if its a parent or leaf module
  isParentModule = True
  if (subFolderList == []):
    isParentModule = False

  # If its parent, construct children modules
  if (isParentModule == True):
    moduleReadmeString += '\n**Sub-Categories:**\n\n'
    moduleReadmeString += '.. toctree::\n'
    moduleReadmeString += '   :titlesonly:\n\n'

    for f in subFolderList:
      subModuleFullPath = os.path.join(modulePath, f)
      moduleSourceFile = modulePath + '/' + moduleName + '._cpp'
      moduleReadmeString += '   ' + f + '/' + f + '\n'
      subPath = os.path.join(moduleRelPath, f)
      processModule(moduleConfig, source, destination, subPath, f)

  # If its leaf, build configuration
  if (isParentModule == False):

    moduleReadmeString += '\n\nUsage\n'
    moduleReadmeString += '----------------------------------\n\n'
    moduleUsageBase = 'e'
    if ("problem" in moduleRelPath):
      moduleUsageBase = 'e["Problem"]["Type"] = "'
    if ("solver" in moduleRelPath):
      moduleUsageBase = 'e["Solver"]["Type"] = "'
    if ("conduit" in moduleRelPath):
      moduleUsageBase = 'k["Conduit"]["Type"] = "'
    if ("distribution" in moduleRelPath):
      moduleUsageBase = 'e["Distribution"][*index*]["Type"] = "'
    if ("engine" in moduleRelPath):
      moduleUsageBase = 'k = korali.Engine()'
    if ("experiment" in moduleRelPath):
      moduleUsageBase = 'k = korali.Experiment()'
    moduleReadmeString += ':code:`' + moduleUsageBase

    classList = moduleRelPath.split('/')
    if (len(classList) > 1):
      moduleReadmeString += upcase_first_letter(classList[1])
      for c in moduleRelPath.split('/')[2:]:
        moduleReadmeString += '/' + upcase_first_letter(c)
      moduleReadmeString += '"'

    moduleReadmeString += '`\n\n'

    if ('Compatible Solvers' in moduleConfig):
      moduleReadmeString += '\n.. _module-' + moduleRelPath.lower().replace(
          '/', '-') + '-compat:\n\n'
      moduleReadmeString += '\nCompatible Solvers\n'
      moduleReadmeString += '----------------------------------\n\n'
      moduleReadmeString += 'This problem can be solved using the following modules: \n\n'
      for v in moduleConfig["Compatible Solvers"]:
        moduleReadmeString += '   - :ref:`' + v + ' <module-solver-' + v.lower(
        ).replace('/', '-').replace(' ', '') + '>`\n'

    if ('Results' in moduleConfig):
      moduleReadmeString += '\n.. _module-' + moduleRelPath.lower().replace(
          '/', '-') + '-results:\n\n'
      moduleReadmeString += '\nResults\n'
      moduleReadmeString += '----------------------------------\n\n'
      moduleReadmeString += 'These are the results produced by this solver: \n\n'
      for v in moduleConfig["Results"]:
        moduleReadmeString += createVariableDescription('e["Results"]',
                                                        moduleRelPath, v)

    if ('Variables Configuration' in moduleConfig):
      moduleReadmeString += '\n.. _module-' + moduleRelPath.lower().replace(
          '/', '-') + '-varsettings:\n\n'
      moduleReadmeString += '\nVariable-Specific Settings\n'
      moduleReadmeString += '----------------------------------\n\n'
      moduleReadmeString += 'These are settings required by this module that are added to each of the experiment\'s variables when this module is selected.\n\n'
      for v in moduleConfig["Variables Configuration"]:
        moduleReadmeString += createVariableDescription(
            'e["Variables"][*index*]', moduleRelPath, v)

    if ('Conditional Variables' in moduleConfig):
      moduleReadmeString += '\n.. _module-' + moduleRelPath.lower().replace(
          '/', '-') + '-distr-config:\n\n'
      moduleReadmeString += '\nDistribution Configuration\n'
      moduleReadmeString += '-----------------------------\n'
      moduleReadmeString += 'These are settings required by this distribution.\n\n'
      if ('Configuration Settings' in moduleConfig):
        for v in moduleConfig["Conditional Variables"]:
          moduleReadmeString += createVariableDescription('e', moduleRelPath, v)
      else:
        moduleReadmeString += '\n*None*\n'

    moduleReadmeString += '\n.. _module-' + moduleRelPath.lower().replace(
        '/', '-') + '-config:\n\n'
    moduleReadmeString += '\nConfiguration\n'
    moduleReadmeString += '-----------------------------\n'
    moduleReadmeString += 'These are settings required by this module.\n\n'
    if ('Configuration Settings' in moduleConfig):
      for v in moduleConfig["Configuration Settings"]:
        moduleReadmeString += createVariableDescription('e', moduleRelPath, v)
    else:
      moduleReadmeString += '\n*None*\n'

    if ('Termination Criteria' in moduleConfig):
      moduleReadmeString += '\n.. _module-' + moduleRelPath.lower().replace(
          '/', '-') + '-criteria:\n\n'
      moduleReadmeString += '\nTermination Criteria\n'
      moduleReadmeString += '----------------------------------\n\n'
      moduleReadmeString += 'These are the customizable criteria that indicates whether the solver should continue or finish execution. Korali will stop when at least one of these conditions are met. The criteria is expressed in C++ since it is compiled and evaluated as seen here in the engine. \n\n'
      for v in moduleConfig["Termination Criteria"]:
        moduleReadmeString += createVariableDescription('e', moduleRelPath, v)

    #if ('Internal Settings' in moduleConfig):
    # moduleReadmeString += '\n.. _module-' + moduleRelPath.lower().replace('/','-') + '-internals:\n\n'
    # moduleReadmeString += '\nInternal Settings *[For Developers]*\n'
    # moduleReadmeString += '--------------------------------------------------\n\n'
    # moduleReadmeString += 'The following are settings that store the internal state of the module. The information below is only interesting for developers and the user does not need to set them up. \n\n'
    # for v in moduleConfig["Internal Settings"]:
    #  moduleReadmeString += createVariableDescription('e', moduleRelPath, v)

    if ('Module Defaults' in moduleConfig):
      moduleReadmeString += '\n.. _module-' + moduleRelPath.lower().replace(
          '/', '-') + '-defaults:\n\n'
      moduleReadmeString += '\nDefault Configuration\n'
      moduleReadmeString += '----------------------------------\n\n'
      moduleReadmeString += 'These following configuration will be assigned by default. Any settings defined by the user will override the given settings specified in these defaults.\n\n'
      moduleReadmeString += '  .. code-block:: python\n\n'
      moduleReadmeString += '    ' + json.dumps(
          moduleConfig['Module Defaults'], sort_keys=True, indent=4).replace(
              '}', '    }')

    if ('Variable Defaults' in moduleConfig):
      moduleReadmeString += '\n\n.. _module-' + moduleRelPath.lower().replace(
          '/', '-') + '-var-defaults:\n\n'
      moduleReadmeString += '\nVariable Defaults\n'
      moduleReadmeString += '----------------------------------\n\n'
      moduleReadmeString += 'These following configuration will be assigned to each of the experiment variables by default. Any settings defined by the user will override the given settings specified in these defaults.\n\n'
      moduleReadmeString += '  .. code-block:: python\n\n'
      moduleReadmeString += '    ' + json.dumps(
          moduleConfig['Variable Defaults'], sort_keys=True, indent=4).replace(
              '}', '    }')

  # Saving Module's readme file
  moduleReadmeString += '\n\n'
  with open(moduleOutputDir + '/' + moduleName + '.rst', 'w') as file:
    file.write(moduleReadmeString)


def build_modules(source, destination):
  shutil.rmtree(destination, ignore_errors=True, onerror=None)
  os.makedirs(destination)
  
  list_dir = os.listdir(source)
  for f in list_dir:
    fullPath = os.path.join(source, f)
    if not os.path.isfile(fullPath):
      if (not '.o/' in fullPath and not '.d/' in fullPath and not 'engine' in fullPath):
        processModule({}, source, destination, f, f)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--destination", help="Save the generated files in this folder")
  parser.add_argument("--source", help="Read files from this folder")
  args = parser.parse_args()

  build_modules(args.source, args.destination) 
