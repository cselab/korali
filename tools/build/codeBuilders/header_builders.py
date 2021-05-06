import sys
from . import variables as vr
from . import auxiliar as aux
import re


def checkHeaderTemplateString( moduleConfig, templateFilePath, moduleTemplate ):
  """These keywords shouls appear only once"""

  substrings = ['@startIncludeGuard',
                '@endIncludeGuard',
                '@className',
                '@parentClassName']

  aux.checkNamespaceKeys(moduleConfig, templateFilePath, moduleTemplate)


def startIncludeGuard(moduleConfig):
  """String for the start the header include guard"""

  string = '\n'
  string += '#ifndef ' + moduleConfig['Include Guard'] + '\n'
  string += '#define ' + moduleConfig['Include Guard'] + '\n'
  return string


def endIncludeGuard(moduleConfig):
  """String for the end the header include guard"""

  string = ''
  string += '#endif // ' + moduleConfig['Include Guard'] + '\n'
  return string


def startNamespace(moduleConfig):
  """String for the start the header namespace"""
  string = [ 'namespace ' + s + '\n{\n'  for s in moduleConfig['Namespace'] ]
  string = ''.join(string)
  return string

def endNamespace(moduleConfig):
  """String for the end the header namespace"""
  string = [ '} //' + s + '\n'  for s in reversed(moduleConfig['Namespace']) ]
  string = ''.join(string)
  return string


def createHeaderDeclarations(moduleConfig):
  """String for variable declarations"""

  string = '  '
  if 'Configuration Settings' in moduleConfig:
    for v in moduleConfig["Configuration Settings"]:
      string += '/**\n  '
      string += '* @brief ' + v["Description"] + '\n  '
      string += '*/\n  '
      string += ' ' + vr.getVariableType(v) + ' ' + vr.getCXXVariableName(v["Name"]) + ';\n  '

  if 'Internal Settings' in moduleConfig:
    for v in moduleConfig["Internal Settings"]:
      string += '/**\n  '
      string += '* @brief [Internal Use] ' + v["Description"] + '\n  '
      string += '*/\n  '
      string += ' ' + vr.getVariableType(v) + ' ' + vr.getCXXVariableName(v["Name"]) + ';\n  '

  if 'Termination Criteria' in moduleConfig:
    for v in moduleConfig["Termination Criteria"]:
      string += '/**\n  '
      string += '* @brief [Termination Criteria] ' + v["Description"] + '\n  '
      string += '*/\n  '
      string += ' ' + vr.getVariableType(v) + ' ' + vr.getCXXVariableName(v["Name"]) + ';\n  '

  if 'Conditional Variables' in moduleConfig:
    for v in moduleConfig["Conditional Variables"]:
      string += '/**\n  '
      string += '* @brief [Conditional Variable Value] ' + v["Description"] + '\n  '
      string += '*/\n  '
      string += ' double ' + vr.getCXXVariableName(v["Name"]) + ';\n  '

      string += '/**\n  '
      string += '* @brief [Conditional Variable Reference] ' + v["Description"] + '\n  '
      string += '*/\n  '
      string += ' std::string ' + vr.getCXXVariableName(v["Name"]) + 'Conditional;\n  '

  return string


def createrClassDoxygenString( moduleConfig ):
  """Creates the doxygen string for the class documentation"""
  string = '/**\n'
  string += '* @brief Class declaration for module: ' + moduleConfig['Class Name'] + '.\n'
  string += '*/\n'
  return string


def createHeaderDoxygenString( moduleConfig ):
  """Creates the doxygen string that goes to the top of the header file"""

  string = '/** \\namespace ' + moduleConfig['Namespace'][-1] + '\n'
  string += '* @brief Namespace declaration for modules of type: ' + moduleConfig['Namespace'][-1] + '.\n'
  string += '*/\n\n'

  string += '/** \\file\n'
  string += '* @brief Header file for module: ' + moduleConfig["Class Name"] + '.\n'
  string += '*/\n\n'

  string += '/** \\dir ' + moduleConfig["Relative Path"] + '\n'
  string += '* @brief Contains code, documentation, and scripts for module: ' + moduleConfig["Class Name"] + '.\n'
  string += '*/\n\n'

  return string


def createOverrideFunctionString(moduleConfig):
  """Creates the sting of overridden function declarations"""

  string = '  '
  if 'Termination Criteria' in moduleConfig:
    string += '/**\n  '
    string += '* @brief Determines whether the module can trigger termination of an experiment run.\n  '
    string += '* @return True, if it should trigger termination; false, otherwise.\n  '
    string += '*/\n  '
    string += 'bool checkTermination() override;\n  '

  string += '/**\n  '
  string += '* @brief Obtains the entire current state and configuration of the module.\n  '
  string += '* @param js JSON object onto which to save the serialized state of the module.\n  '
  string += '*/\n  '
  string += 'void getConfiguration(knlohmann::json& js) override;\n  '

  string += '/**\n  '
  string += '* @brief Sets the entire state and configuration of the module, given a JSON object.\n  '
  string += '* @param js JSON object from which to deserialize the state of the module.\n  '
  string += '*/\n  '
  string += 'void setConfiguration(knlohmann::json& js) override;\n  '

  string += '/**\n  '
  string += '* @brief Applies the module\'s default configuration upon its creation.\n  '
  string += '* @param js JSON object containing user configuration. The defaults will not override any currently defined settings.\n  '
  string += '*/\n  '
  string += 'void applyModuleDefaults(knlohmann::json& js) override;\n  '

  string += '/**\n  '
  string += '* @brief Applies the module\'s default variable configuration to each variable in the Experiment upon creation.\n  '
  string += '*/\n  '
  string += 'void applyVariableDefaults() override;\n  '

  if 'Available Operations' in moduleConfig:
    string += '/**\n  '
    string += '* @brief Runs the operation specified on the given sample. It checks recursively whether the function was found by the current module or its parents.\n  '
    string += "* @param sample Sample to operate on. Should contain in the 'Operation' field an operation accepted by this module or its parents.\n  "
    string += '* @param operation Should specify an operation type accepted by this module or its parents.\n  '
    string += '* @return True, if operation found and executed; false, otherwise.\n  '
    string += '*/\n  '
    string += 'bool runOperation(std::string operation, korali::Sample& sample) override;\n  '

  if 'Conditional Variables' in moduleConfig:
    string += '/**\n  '
    string += '* @brief Retrieves the pointer of a conditional value of a distribution property.\n  '
    string += '* @param property Name of the property to find.\n  '
    string += '* @return The pointer to the property..\n  '
    string += '*/\n  '
    string += 'double* getPropertyPointer(const std::string& property) override;\n  '

  return string