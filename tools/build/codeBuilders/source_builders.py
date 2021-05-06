from . import variables as vr
from . import auxiliar as aux
import json
import sys

def checkSourceTemplateString( moduleConfig, templateFilePath, moduleTemplate ):
  """These keywords shouls appear only once"""
  aux.checkNamespaceKeys(moduleConfig, templateFilePath, moduleTemplate)


def consumeValue(base, moduleName, path, varName, varType, isMandatory, options):
  # We ignore variable types, as they are managed by the modules themselves
  if ('std::vector<korali::Variable' in varType): return ''

  # Flag to indicate a Korali module was detected
  detectedKoraliType = False

  # Checking whether its defined
  cString = ' if (isDefined(' + base + ', ' + path.replace('][', ", ").replace('[', '').replace(']', '') + '))\n'
  cString += ' {\n'

  if ('korali::Sample' in varType and not detectedKoraliType):
    cString += ' ' + varName + '._js.getJson() = ' + base + path + ';\n'
    detectedKoraliType = True

  if ('std::vector<korali::' in varType and not detectedKoraliType):
    baseType = varType.replace('std::vector<', '').replace('>', '')
    cString += ' ' + varName + '.resize(' + base + path + '.size());\n'
    cString += ' for(size_t i = 0; i < ' + base + path + '.size(); i++)'
    cString += ' {\n'
    cString += '   ' + varName + '[i] = (' + baseType + ') korali::Module::getModule(' + base + path + '[i], _k);\n'
    if (not 'Experiment' in varType):
     cString += '   ' + varName + '[i]->applyVariableDefaults();\n'
     cString += '   ' + varName + '[i]->applyModuleDefaults(' + base + path + '[i]);\n'
     cString += '   ' + varName + '[i]->setConfiguration(' + base + path + '[i]);\n'
    cString += ' }\n'
    detectedKoraliType = True

  if ('korali::' in varType and not detectedKoraliType):
    rhs = 'dynamic_cast<' + varType + '>(korali::Module::getModule(' + base + path + ', _k));\n'
    if ('Solver' in varType):
      cString += '  if (_k->_isInitialized == false) ' + varName + ' = ' + rhs
    else:
      cString += ' ' + varName + ' = ' + rhs
    if (not 'Experiment' in varType):
     cString += ' ' + varName + '->applyVariableDefaults();\n'
     cString += ' ' + varName + '->applyModuleDefaults(' + base + path + ');\n'
     cString += ' ' + varName + '->setConfiguration(' + base + path + ');\n'
    detectedKoraliType = True

  if (not detectedKoraliType):
    rhs = base + path + '.get<' + varType + '>();\n'
    if ('gsl_rng*' in varType): rhs = 'setRange(' + base + path + '.get<std::string>());\n'

    cString += ' try { ' + varName + ' = ' + rhs + '} catch (const std::exception& e)\n'
    cString += ' { KORALI_LOG_ERROR(" + Object: [ ' + moduleName + ' ] \\n + Key:    ' + path.replace('"', "'") + '\\n%s", e.what()); } \n'
    if (options):
      cString += '{\n'
      validVarName = 'validOption'
      cString += ' bool ' + validVarName + ' = false; \n'
      for v in options:  cString += ' if (' + varName + ' == "' + v + '") ' + validVarName + ' = true; \n'
      cString += ' if (' + validVarName + ' == false) KORALI_LOG_ERROR(" + Unrecognized value (%s) provided for mandatory setting: ' + path.replace('"', "'") + ' required by ' + moduleName + '.\\n", ' + varName + '.c_str()); \n'
      cString += '}\n'

  cString += '   eraseValue(' + base + ', ' + path.replace('][', ", ").replace('[', '').replace(']', '') + ');\n'
  cString += ' }\n'

  if (isMandatory):
    cString += '  else '
    cString += '  KORALI_LOG_ERROR(" + No value provided for mandatory setting: ' + path.replace('"', "'") + ' required by ' + moduleName + '.\\n"); \n'

  cString += '\n'
  return cString


def saveValue(base, path, varName, varType):

  if ('korali::Sample' in varType):
    sString = '   ' + base + path + ' = ' + varName + '._js.getJson();\n'
    return sString

  if ('gsl_rng*' in varType):
    sString = '   ' + base + path + ' = getRange(' + varName + ');\n'
    return sString

  if ('korali::Variable' in varType):
    sString = ''
    return sString

  if ('std::vector<korali::' in varType):
    sString = ' for(size_t i = 0; i < ' + varName + '.size(); i++) ' + varName + '[i]->getConfiguration(' + base + path + '[i]);\n'
    return sString

  if ('korali::' in varType):
    sString = ' if(' + varName + ' != NULL) ' + varName + '->getConfiguration(' + base + path + ');\n'
    return sString

  sString = '   ' + base + path + ' = ' + varName + ';\n'
  return sString


def createSetConfiguration(module):
  codeString = 'void ' + module["Class Name"] + '::setConfiguration(knlohmann::json& js) \n{\n'

  codeString += ' if (isDefined(js, "Results"))  eraseValue(js, "Results");\n\n'

  # Consume Internal Settings
  if 'Internal Settings' in module:
    for v in module["Internal Settings"]:
      codeString += consumeValue('js', module["Name"], vr.getVariablePath(v),
                                 vr.getCXXVariableName(v["Name"]),
                                 vr.getVariableType(v), False,
                                 vr.getVariableOptions(v))

  # Consume Configuration Settings
  if 'Configuration Settings' in module:
    for v in module["Configuration Settings"]:
      codeString += consumeValue('js', module["Name"], vr.getVariablePath(v),
                                 vr.getCXXVariableName(v["Name"]),
                                 vr.getVariableType(v), True,
                                 vr.getVariableOptions(v))

  if 'Termination Criteria' in module:
    for v in module["Termination Criteria"]:
      codeString += consumeValue(
          'js', module["Name"], '["Termination Criteria"]' + vr.getVariablePath(v),
          vr.getCXXVariableName(v["Name"]), vr.getVariableType(v), True,
          vr.getVariableOptions(v))

  if 'Variables Configuration' in module:
    codeString += ' if (isDefined(_k->_js.getJson(), "Variables"))\n'
    codeString += ' for (size_t i = 0; i < _k->_js["Variables"].size(); i++) { \n'
    for v in module["Variables Configuration"]:
      codeString += consumeValue(
          '_k->_js["Variables"][i]', module["Name"], vr.getVariablePath(v),
          '_k->_variables[i]->' + vr.getCXXVariableName(v["Name"]),
          vr.getVariableType(v), True, vr.getVariableOptions(v))
    codeString += ' } \n'

  if 'Conditional Variables' in module:
    codeString += '  _hasConditionalVariables = false; \n'
    for v in module["Conditional Variables"]:
      codeString += ' if(js' + vr.getVariablePath(v) + '.is_number()) ' + vr.getCXXVariableName(v["Name"]) + ' = js' + vr.getVariablePath(v) + ';\n'
      codeString += ' if(js' + vr.getVariablePath(
          v
      ) + '.is_string()) { _hasConditionalVariables = true; ' + vr.getCXXVariableName(
          v["Name"]) + 'Conditional = js' + vr.getVariablePath(v) + '; } \n'
      codeString += ' eraseValue(js, ' + vr.getVariablePath(v).replace(
          '][', ", ").replace('[', '').replace(']', '') + ');\n\n'

  if 'Compatible Solvers' in module:
    codeString += '  bool detectedCompatibleSolver = false; \n'
    codeString += '  std::string solverName = toLower(_k->_js["Solver"]["Type"]); \n'
    codeString += '  std::string candidateSolverName; \n'
    codeString += '  solverName.erase(remove_if(solverName.begin(), solverName.end(), isspace), solverName.end()); \n'
    for v in module["Compatible Solvers"]:
      codeString += '   candidateSolverName = toLower("' + v + '"); \n'
      codeString += '   candidateSolverName.erase(remove_if(candidateSolverName.begin(), candidateSolverName.end(), isspace), candidateSolverName.end()); \n'
      codeString += '   if (solverName.rfind(candidateSolverName, 0) == 0) detectedCompatibleSolver = true;\n'
    codeString += '  if (detectedCompatibleSolver == false) KORALI_LOG_ERROR(" + Specified solver (%s) is not compatible with problem of type: ' + module[
        "Name"] + '\\n",  _k->_js["Solver"]["Type"].dump(1).c_str()); \n\n'

  codeString += ' ' + module["Parent Class Name"] + '::setConfiguration(js);\n'

  codeString += ' _type = "' + module["Module Type"] + '";\n'
  codeString += ' if(isDefined(js, "Type")) eraseValue(js, "Type");\n'
  codeString += ' if(isEmpty(js) == false) KORALI_LOG_ERROR(" + Unrecognized settings for Korali module: ' + module[
      "Name"] + ': \\n%s\\n", js.dump(2).c_str());\n'
  codeString += '} \n\n'

  return codeString


def createGetConfiguration(module):
  codeString = 'void ' + module["Class Name"] + '::getConfiguration(knlohmann::json& js) \n{\n\n'

  codeString += ' js["Type"] = _type;\n'

  if 'Configuration Settings' in module:
    for v in module["Configuration Settings"]:
      codeString += saveValue('js', vr.getVariablePath(v),
                              vr.getCXXVariableName(v["Name"]), vr.getVariableType(v))

  if 'Termination Criteria' in module:
    for v in module["Termination Criteria"]:
      codeString += saveValue('js',
                              '["Termination Criteria"]' + vr.getVariablePath(v),
                              vr.getCXXVariableName(v["Name"]), vr.getVariableType(v))

  if 'Internal Settings' in module:
    for v in module["Internal Settings"]:
      codeString += saveValue('js', vr.getVariablePath(v),
                              vr.getCXXVariableName(v["Name"]), vr.getVariableType(v))

  if 'Variables Configuration' in module:
    codeString += ' for (size_t i = 0; i <  _k->_variables.size(); i++) { \n'
    for v in module["Variables Configuration"]:
      codeString += saveValue(
          '_k->_js["Variables"][i]', vr.getVariablePath(v),
          '_k->_variables[i]->' + vr.getCXXVariableName(v["Name"]),
          vr.getVariableType(v))
    codeString += ' } \n'

  if 'Conditional Variables' in module:
    for v in module["Conditional Variables"]:
      codeString += ' if(' + vr.getCXXVariableName(
          v["Name"]) + 'Conditional == "") js' + vr.getVariablePath(v) + ' = ' + vr.getCXXVariableName(v["Name"]) + ';\n'
      codeString += ' if(' + vr.getCXXVariableName(
          v["Name"]) + 'Conditional != "") js' + vr.getVariablePath(v) + ' = ' + vr.getCXXVariableName(v["Name"]) + 'Conditional; \n'

  codeString += ' ' + module["Parent Class Name"] + '::getConfiguration(js);\n'

  if 'Experiment' == module['Name']:
     codeString += ' if (isDefined(_js.getJson(), "Variables"))\n'
     codeString += '   js["Variables"] = _js["Variables"];\n'

  codeString += '} \n\n'

  return codeString


def createApplyModuleDefaults(module):
  codeString = 'void ' + module["Class Name"] + '::applyModuleDefaults(knlohmann::json& js) \n{\n\n'

  if 'Module Defaults' in module:
    codeString += ' std::string defaultString = "' + json.dumps(module["Module Defaults"]).replace('"', '\\"') + '";\n'
    codeString += ' knlohmann::json defaultJs = knlohmann::json::parse(defaultString);\n'
    codeString += ' mergeJson(js, defaultJs); \n'

  codeString += ' ' + module["Parent Class Name"] + '::applyModuleDefaults(js);\n'

  codeString += '} \n\n'

  return codeString


def createApplyVariableDefaults(module):
  codeString = 'void ' + module["Class Name"] + '::applyVariableDefaults() \n{\n\n'

  if 'Variable Defaults' in module:
    codeString += ' std::string defaultString = "' + json.dumps(module["Variable Defaults"]).replace('"', '\\"') + '";\n'
    codeString += ' knlohmann::json defaultJs = knlohmann::json::parse(defaultString);\n'
    codeString += ' if (isDefined(_k->_js.getJson(), "Variables"))\n'
    codeString += '  for (size_t i = 0; i < _k->_js["Variables"].size(); i++) \n'
    codeString += '   mergeJson(_k->_js["Variables"][i], defaultJs); \n'

  codeString += ' ' + module["Parent Class Name"] + '::applyVariableDefaults();\n'
  codeString += '} \n\n'

  return codeString


def createCheckTermination(module):
  codeString = 'bool ' + module["Class Name"] + '::checkTermination()\n'
  codeString += '{\n'
  codeString += ' bool hasFinished = false;\n\n'

  if 'Termination Criteria' in module:
    for v in module["Termination Criteria"]:
      codeString += ' if (' + v["Criteria"] + ')\n'
      codeString += ' {\n'
      codeString += '  _terminationCriteria.push_back("' + module["Name"] + vr.getVariablePath(v).replace('"', "'") + ' = " + std::to_string(' + vr.getCXXVariableName(v["Name"]) + ') + ".");\n'
      codeString += '  hasFinished = true;\n'
      codeString += ' }\n\n'

  codeString += ' hasFinished = hasFinished || ' + module["Parent Class Name"] + '::checkTermination();\n'
  codeString += ' return hasFinished;\n'
  codeString += '}\n\n'

  return codeString


def createRunOperation(module):
  codeString = 'bool ' + module["Class Name"] + '::runOperation(std::string operation, korali::Sample& sample)\n'
  codeString += '{\n'
  codeString += ' bool operationDetected = false;\n\n'

  for v in module["Available Operations"]:
    codeString += ' if (operation == "' + v["Name"] + '")\n'
    codeString += ' {\n'
    codeString += '  ' + v["Function"] + '(sample);\n'
    codeString += '  return true;\n'
    codeString += ' }\n\n'

  codeString += ' operationDetected = operationDetected || ' + module["Parent Class Name"] + '::runOperation(operation, sample);\n'
  codeString += ' if (operationDetected == false) KORALI_LOG_ERROR(" + Operation %s not recognized for problem ' + module["Class Name"] + '.\\n", operation.c_str());\n'
  codeString += ' return operationDetected;\n'
  codeString += '}\n\n'

  return codeString


def createGetPropertyPointer(module):
  codeString = 'double* ' + module["Class Name"] + '::getPropertyPointer(const std::string& property)\n'
  codeString += '{\n'

  for v in module["Conditional Variables"]:
    codeString += ' if (property == "' + v["Name"][0] + '") return &' + vr.getCXXVariableName(v["Name"]) + ';\n'

  codeString += ' KORALI_LOG_ERROR(" + Property %s not recognized for distribution ' + module["Class Name"] + '.\\n", property.c_str());\n'
  codeString += ' return NULL;\n'
  codeString += '}\n\n'

  return codeString