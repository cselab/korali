import sys
import os
import json

####################################################################
# Helper Functions
####################################################################


def getVariableType(v):
  # Replacing bools with ints for Python compatibility
  return v['Type'].replace('bool', 'int').replace(
      'std::function<void(korali::Sample&)>', 'std::uint64_t')


def getCXXVariableName(v):
  cVarName = ''
  for name in v:
    cVarName += name
  cVarName = cVarName.replace(" ", "")
  cVarName = cVarName.replace("(", "")
  cVarName = cVarName.replace(")", "")
  cVarName = cVarName.replace("+", "")
  cVarName = cVarName.replace("-", "")
  cVarName = cVarName.replace("[", "")
  cVarName = cVarName.replace("]", "")
  cVarName = '_' + cVarName[0].lower() + cVarName[1:]
  return cVarName


def getVariablePath(v):
  cVarPath = ''
  for name in v["Name"]:
    cVarPath += '["' + name + '"]'
  return cVarPath


def getVariableOptions(v):
  options = []
  if (v.get('Options', '')):
    for item in v["Options"]:
      options.append(item["Value"])
  return options


def getOptionName(path):
  nameList = path.rsplit('/')
  optionName = ''
  for name in nameList[1:-1]:
    optionName += name[0].capitalize() + name[1:] + '/'
  optionName += getModuleName(path)
  return optionName


def getModuleName(path):
  nameList = path.rsplit('/', 1)
  moduleName = nameList[-1]
  moduleName = moduleName[0].capitalize() + moduleName[1:]
  return moduleName


def getClassName(path):
  nameList = path.rsplit('/')
  className = 'korali::'
  for name in nameList[:-1]:
    className += name + '::'
  className += getModuleName(path)
  return className


def getNamespaceName(path):
  nameList = path.rsplit('/')
  namespaceName = 'korali::'
  for name in nameList[:-1]:
    namespaceName += name + '::'
  namespaceName += getModuleName(path)[0].lower() + getModuleName(path)[1:]
  return namespaceName


def getParentClassName(className):
  nameString = className.rsplit('::', 2)
  if (len(nameString) == 2):
    return 'korali::Module'
  parentClass = nameString[0] + '::' + nameString[-2][0].upper(
  ) + nameString[-2][1:]
  return parentClass


def isLeafModule(path):
  list_dir = os.listdir(path)
  for f in list_dir:
    subPath = os.path.join(path, f)
    if not os.path.isfile(subPath):
      return False
  return True


#####################################################################


def consumeValue(base, moduleName, path, varName, varType, isMandatory,
                 options):
  cString = '\n'

  if ('std::function' in varType):
    cString += ' try { ' + varName + ' = ' + base + path + '.get<size_t>(); } catch (const std::exception& e) {\n'
    cString += '   KORALI_LOG_ERROR(" + Object: [ ' + moduleName + ' ] \\n + Key:    ' + path.replace(
        '"', "'") + '\\n%s", e.what());\n'
    cString += ' } \n'
    cString += '   eraseValue(' + base + ', ' + path.replace(
        '][', ", ").replace('[', '').replace(']', '') + ');\n'
    return cString

  if ('std::vector<korali::Variable' in varType):
    return cString

  if ('korali::Sample' in varType):
    cString += ' ' + varName + '._js.getJson() = ' + base + path + ';\n'
    cString += '   eraseValue(' + base + ', ' + path.replace(
        '][', ", ").replace('[', '').replace(']', '') + ');\n'
    return cString

  if ('std::vector<korali::Variable*>' in varType):
    cString += ' eraseValue(' + base + ', ' + path.replace('][', ", ").replace(
        '[', '').replace(']', '') + ');\n\n'
    return cString

  if ('std::vector<korali::' in varType):
    baseType = varType.replace('std::vector<', '').replace('>', '')
    cString += ' for(size_t i = 0; i < ' + base + path + '.size(); i++) ' + varName + '.push_back((' + baseType + ')korali::Module::getModule(' + base + path + '[i], _k));\n'
    cString += ' eraseValue(' + base + ', ' + path.replace('][', ", ").replace(
        '[', '').replace(']', '') + ');\n\n'
    return cString

  rhs = base + path + '.get<' + varType + '>();\n'

  if ('korali::' in varType):
    rhs = 'dynamic_cast<' + varType + '>(korali::Module::getModule(' + base + path + ', _k));\n'

  if ('gsl_rng*' in varType):
    rhs = 'setRange(' + base + path + '.get<std::string>());\n'

  cString += ' if (isDefined(' + base + ', ' + path.replace('][', ", ").replace(
      '[', '').replace(']', '') + '))  \n  { \n'
  cString += ' try {' + varName + ' = ' + rhs + ' } catch (const std::exception& e) {\n'
  cString += '   KORALI_LOG_ERROR(" + Object: [ ' + moduleName + ' ] \\n + Key:    ' + path.replace(
      '"', "'") + '\\n%s", e.what());\n'
  cString += ' } \n'
  cString += '   eraseValue(' + base + ', ' + path.replace('][', ", ").replace(
      '[', '').replace(']', '') + ');\n'
  cString += '  }\n'

  if (isMandatory):
    cString += '  else '
    cString += '  KORALI_LOG_ERROR(" + No value provided for mandatory setting: ' + path.replace(
        '"', "'") + ' required by ' + moduleName + '.\\n"); \n'

  cString += '\n'

  if (options):
    cString += '{\n'
    validVarName = 'validOption'
    cString += ' bool ' + validVarName + ' = false; \n'
    for v in options:
      cString += ' if (' + varName + ' == "' + v + '") ' + validVarName + ' = true; \n'
    cString += ' if (' + validVarName + ' == false) KORALI_LOG_ERROR(" + Unrecognized value provided for mandatory setting: ' + path.replace(
        '"', "'") + ' required by ' + moduleName + '.\\n"); \n'
    cString += '}\n'

  cString += '\n'
  return cString


#####################################################################


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
    sString = ' ' + varName + '->getConfiguration(' + base + path + ');\n'
    return sString

  sString = '   ' + base + path + ' = ' + varName + ';\n'
  return sString


####################################################################


def createSetConfiguration(module):
  codeString = 'void ' + module[
      "Class"] + '::setConfiguration(knlohmann::json& js) \n{\n'

  codeString += ' if (isDefined(js, "Results"))  eraseValue(js, "Results");\n\n'

  # Consume Configuration Settings
  if 'Configuration Settings' in module:
    for v in module["Configuration Settings"]:
      codeString += consumeValue('js', module["Name"], getVariablePath(v),
                                 getCXXVariableName(v["Name"]),
                                 getVariableType(v), True,
                                 getVariableOptions(v))

  if 'Internal Settings' in module:
    for v in module["Internal Settings"]:
      codeString += consumeValue('js', module["Name"], getVariablePath(v),
                                 getCXXVariableName(v["Name"]),
                                 getVariableType(v), False,
                                 getVariableOptions(v))

  if 'Termination Criteria' in module:
    for v in module["Termination Criteria"]:
      codeString += consumeValue(
          'js', module["Name"], '["Termination Criteria"]' + getVariablePath(v),
          getCXXVariableName(v["Name"]), getVariableType(v), True,
          getVariableOptions(v))

  if 'Variables Configuration' in module:
    codeString += ' for (size_t i = 0; i < _k->_js["Variables"].size(); i++) { \n'
    for v in module["Variables Configuration"]:
      codeString += consumeValue(
          '_k->_js["Variables"][i]', module["Name"], getVariablePath(v),
          '_k->_variables[i]->' + getCXXVariableName(v["Name"]),
          getVariableType(v), True, getVariableOptions(v))
    codeString += ' } \n'

  if 'Conditional Variables' in module:
    codeString += '  _hasConditionalVariables = false; \n'
    for v in module["Conditional Variables"]:
      codeString += ' if(js' + getVariablePath(
          v) + '.is_number()) ' + getCXXVariableName(
              v["Name"]) + ' = js' + getVariablePath(v) + ';\n'
      codeString += ' if(js' + getVariablePath(
          v
      ) + '.is_string()) { _hasConditionalVariables = true; ' + getCXXVariableName(
          v["Name"]) + 'Conditional = js' + getVariablePath(v) + '; } \n'
      codeString += ' eraseValue(js, ' + getVariablePath(v).replace(
          '][', ", ").replace('[', '').replace(']', '') + ');\n\n'

  if 'Compatible Solvers' in module:
    codeString += '  bool detectedCompatibleSolver = false; \n'
    codeString += '  std::string solverName = _k->_js["Solver"]["Type"]; \n'
    codeString += '  std::string candidateSolverName; \n'
    codeString += '  solverName.erase(remove_if(solverName.begin(), solverName.end(), isspace), solverName.end()); \n'
    for v in module["Compatible Solvers"]:
      codeString += '   candidateSolverName = "' + v + '"; \n'
      codeString += '   candidateSolverName.erase(remove_if(candidateSolverName.begin(), candidateSolverName.end(), isspace), candidateSolverName.end()); \n'
      codeString += '   if (solverName.rfind(candidateSolverName, 0) == 0) detectedCompatibleSolver = true;\n'
    codeString += '  if (detectedCompatibleSolver == false) KORALI_LOG_ERROR(" + Specified solver (%s) is not compatible with problem of type: ' + module[
        "Name"] + '\\n",  _k->_js["Solver"]["Type"].dump(1).c_str()); \n\n'

  codeString += ' ' + module["Parent Class"] + '::setConfiguration(js);\n'

  codeString += ' _type = "' + module["Option Name"] + '";\n'
  codeString += ' if(isDefined(js, "Type")) eraseValue(js, "Type");\n'
  codeString += ' if(isEmpty(js) == false) KORALI_LOG_ERROR(" + Unrecognized settings for Korali module: ' + module[
      "Name"] + ': \\n%s\\n", js.dump(2).c_str());\n'
  codeString += '} \n\n'

  return codeString


####################################################################


def createGetConfiguration(module):
  codeString = 'void ' + module[
      "Class"] + '::getConfiguration(knlohmann::json& js) \n{\n\n'

  codeString += ' js["Type"] = _type;\n'

  if 'Configuration Settings' in module:
    for v in module["Configuration Settings"]:
      codeString += saveValue('js', getVariablePath(v),
                              getCXXVariableName(v["Name"]), getVariableType(v))

  if 'Termination Criteria' in module:
    for v in module["Termination Criteria"]:
      codeString += saveValue('js',
                              '["Termination Criteria"]' + getVariablePath(v),
                              getCXXVariableName(v["Name"]), getVariableType(v))

  if 'Internal Settings' in module:
    for v in module["Internal Settings"]:
      codeString += saveValue('js', getVariablePath(v),
                              getCXXVariableName(v["Name"]), getVariableType(v))

  if 'Variables Configuration' in module:
    codeString += ' for (size_t i = 0; i <  _k->_variables.size(); i++) { \n'
    for v in module["Variables Configuration"]:
      codeString += saveValue(
          '_k->_js["Variables"][i]', getVariablePath(v),
          '_k->_variables[i]->' + getCXXVariableName(v["Name"]),
          getVariableType(v))
    codeString += ' } \n'

  if 'Conditional Variables' in module:
    for v in module["Conditional Variables"]:
      codeString += ' if(' + getCXXVariableName(
          v["Name"]) + 'Conditional == "") js' + getVariablePath(
              v) + ' = ' + getCXXVariableName(v["Name"]) + ';\n'
      codeString += ' if(' + getCXXVariableName(
          v["Name"]) + 'Conditional != "") js' + getVariablePath(
              v) + ' = ' + getCXXVariableName(v["Name"]) + 'Conditional; \n'

  codeString += ' ' + module["Parent Class"] + '::getConfiguration(js);\n'

  if 'Experiment' == module['Name']:
    codeString += ' js["Variables"] = _js["Variables"];\n'

  codeString += '} \n\n'

  return codeString


####################################################################


def createApplyModuleDefaults(module):
  codeString = 'void ' + module[
      "Class"] + '::applyModuleDefaults(knlohmann::json& js) \n{\n\n'

  if 'Module Defaults' in module:
    codeString += ' std::string defaultString = "' + json.dumps(
        module["Module Defaults"]).replace('"', '\\"') + '";\n'
    codeString += ' knlohmann::json defaultJs = knlohmann::json::parse(defaultString);\n'
    codeString += ' mergeJson(js, defaultJs); \n'

  codeString += ' ' + module["Parent Class"] + '::applyModuleDefaults(js);\n'

  codeString += '} \n\n'

  return codeString


####################################################################


def createApplyVariableDefaults(module):
  codeString = 'void ' + module["Class"] + '::applyVariableDefaults() \n{\n\n'

  if 'Variable Defaults' in module:
    codeString += ' std::string defaultString = "' + json.dumps(
        module["Variable Defaults"]).replace('"', '\\"') + '";\n'
    codeString += ' knlohmann::json defaultJs = knlohmann::json::parse(defaultString);\n'
    codeString += ' for (size_t i = 0; i < _k->_js["Variables"].size(); i++) \n'
    codeString += '  mergeJson(_k->_js["Variables"][i], defaultJs); \n'

  codeString += ' ' + module["Parent Class"] + '::applyVariableDefaults();\n'
  codeString += '} \n\n'

  return codeString


####################################################################


def createCheckTermination(module):
  codeString = 'bool ' + module["Class"] + '::checkTermination()\n'
  codeString += '{\n'
  codeString += ' bool hasFinished = false;\n\n'

  if 'Termination Criteria' in module:
    for v in module["Termination Criteria"]:
      codeString += ' if (' + v["Criteria"] + ')\n'
      codeString += ' {\n'
      codeString += '  _terminationCriteria.push_back("' + module[
          "Name"] + getVariablePath(v).replace(
              '"', "'") + ' = " + std::to_string(' + getCXXVariableName(
                  v["Name"]) + ') + ".");\n'
      codeString += '  hasFinished = true;\n'
      codeString += ' }\n\n'

  codeString += ' hasFinished = hasFinished || ' + module[
      "Parent Class"] + '::checkTermination();\n'
  codeString += ' return hasFinished;\n'
  codeString += '}\n\n'

  return codeString


####################################################################


def createRunOperation(module):
  codeString = 'bool ' + module[
      "Class"] + '::runOperation(std::string operation, korali::Sample& sample)\n'
  codeString += '{\n'
  codeString += ' bool operationDetected = false;\n\n'

  for v in module["Available Operations"]:
    codeString += ' if (operation == "' + v["Name"] + '")\n'
    codeString += ' {\n'
    codeString += '  ' + v["Function"] + '(sample);\n'
    codeString += '  return true;\n'
    codeString += ' }\n\n'

  codeString += ' operationDetected = operationDetected || ' + module[
      "Parent Class"] + '::runOperation(operation, sample);\n'
  codeString += ' if (operationDetected == false) KORALI_LOG_ERROR(" + Operation %s not recognized for problem ' + module[
      "Class"] + '.\\n", operation.c_str());\n'
  codeString += ' return operationDetected;\n'
  codeString += '}\n\n'

  return codeString


####################################################################


def createGetPropertyPointer(module):
  codeString = 'double* ' + module[
      "Class"] + '::getPropertyPointer(const std::string& property)\n'
  codeString += '{\n'

  for v in module["Conditional Variables"]:
    codeString += ' if (property == "' + v["Name"][
        0] + '") return &' + getCXXVariableName(v["Name"]) + ';\n'

  codeString += ' KORALI_LOG_ERROR(" + Property %s not recognized for distribution ' + module[
      "Class"] + '.\\n", property.c_str());\n'
  codeString += ' return NULL;\n'
  codeString += '}\n\n'

  return codeString


####################################################################


def createHeaderDeclarations(module):
  headerString = ''

  if 'Configuration Settings' in module:
    for v in module["Configuration Settings"]:
      headerString += '/**\n'
      headerString += '* @brief ' + v["Description"] + '\n'
      headerString += '*/\n'
      headerString += ' ' + getVariableType(v) + ' ' + getCXXVariableName(
          v["Name"]) + ';\n'

  if 'Internal Settings' in module:
    for v in module["Internal Settings"]:
      headerString += '/**\n'
      headerString += '* @brief [Internal Use] ' + v["Description"] + '\n'
      headerString += '*/\n'
      headerString += ' ' + getVariableType(v) + ' ' + getCXXVariableName(
          v["Name"]) + ';\n'

  if 'Termination Criteria' in module:
    for v in module["Termination Criteria"]:
      headerString += '/**\n'
      headerString += '* @brief [Termination Criteria] ' + v[
          "Description"] + '\n'
      headerString += '*/\n'
      headerString += ' ' + getVariableType(v) + ' ' + getCXXVariableName(
          v["Name"]) + ';\n'

  if 'Conditional Variables' in module:
    for v in module["Conditional Variables"]:
      headerString += '/**\n'
      headerString += '* @brief [Conditional Variable Value] ' + v[
          "Description"] + '\n'
      headerString += '*/\n'
      headerString += ' double ' + getCXXVariableName(v["Name"]) + ';\n'

      headerString += '/**\n'
      headerString += '* @brief [Conditional Variable Reference] ' + v[
          "Description"] + '\n'
      headerString += '*/\n'
      headerString += ' std::string ' + getCXXVariableName(
          v["Name"]) + 'Conditional;\n'

  return headerString


####################################################################


def createVariableDeclarations(module):
  variableDeclarationString = ''

  if 'Variables Configuration' in module:
    for v in module["Variables Configuration"]:
      varName = getCXXVariableName(v["Name"])
      if (not varName in variableDeclarationSet):
        variableDeclarationString += '/**\n'
        variableDeclarationString += '* @brief [Module: ' + module[
            "Class"] + '] ' + v["Description"] + '\n'
        variableDeclarationString += '*/\n'
        variableDeclarationString += '  ' + getVariableType(
            v) + ' ' + varName + ';\n'
        variableDeclarationSet.add(varName)

  return variableDeclarationString


####################################################################


def save_if_different(filename, content):
  try:
    with open(filename) as f:
      existing = f.read()
    if content == existing:
      return
  except FileNotFoundError:
    pass

  with open(filename, 'w') as f:
    print('[Korali] Creating: ' + filename + '...')
    f.write(content)


####################################################################
# Main Parser Routine
####################################################################

print("\n[Korali] Start Parser")

koraliDir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
modulesDir = koraliDir + '/modules/'

# modules List
moduleDetectionList = ''
moduleIncludeList = ''
variableDeclarationList = ''
variableDeclarationSet = set()

# Detecting modules' json file
for moduleDir, relDir, fileNames in os.walk(modulesDir):
  for fileName in fileNames:
    if '.config' in fileName:
      filePath = moduleDir + '/' + fileName
      print('[Korali] Opening: ' + filePath + '...')
      moduleFilename = fileName.replace('.config', '')

      # Loading Json configuration file
      with open(filePath, 'r') as file:
        moduleConfig = json.load(file)

      # Processing Module information
      modulePath = os.path.relpath(moduleDir, modulesDir)
      moduleConfig["Name"] = getModuleName(modulePath)
      moduleConfig["Class"] = getClassName(modulePath)
      moduleConfig["Namespace"] = getNamespaceName(modulePath)
      moduleConfig["Parent Class"] = getParentClassName(moduleConfig["Class"])
      moduleConfig["Option Name"] = getOptionName(modulePath)
      moduleConfig["Is Leaf"] = isLeafModule(moduleDir)

      ####### Adding module to list
      relpath = os.path.relpath(moduleDir, modulesDir)
      if (moduleConfig["Is Leaf"]):
        filepath = os.path.join(relpath, moduleFilename + '.hpp')
        moduleIncludeList += '#include "' + filepath + '" \n'
        moduleDetectionList += '  if(moduleType == "' + moduleConfig[
            "Option Name"] + '") module = new ' + moduleConfig["Class"] + '();\n'

      ###### Producing module code

      moduleCodeString = createSetConfiguration(moduleConfig)
      moduleCodeString += createGetConfiguration(moduleConfig)
      moduleCodeString += createApplyModuleDefaults(moduleConfig)
      moduleCodeString += createApplyVariableDefaults(moduleConfig)

      if 'Termination Criteria' in moduleConfig:
        moduleCodeString += createCheckTermination(moduleConfig)

      if 'Available Operations' in moduleConfig:
        moduleCodeString += createRunOperation(moduleConfig)

      if 'Conditional Variables' in moduleConfig:
        moduleCodeString += createGetPropertyPointer(moduleConfig)

      ####### Producing header file

      # Adding doxygen header
      moduleTemplateHeaderString = '/** \\file\n'
      moduleTemplateHeaderString += '* @brief Header file for module: ' + moduleConfig[
          "Class"] + '.\n'
      moduleTemplateHeaderString += '*/\n\n'

      moduleTemplateHeaderString += '/** \\dir ' + relpath + '\n'
      moduleTemplateHeaderString += '* @brief Contains code, documentation, and scripts for module: ' + moduleConfig[
          "Class"] + '.\n'
      moduleTemplateHeaderString += '*/\n\n'

      # Loading template header .hpp file
      moduleTemplateHeaderFile = moduleDir + '/' + moduleFilename + '._hpp'
      with open(moduleTemplateHeaderFile, 'r') as file:
        moduleTemplateHeaderString += file.read()

      # Adding overridden function declarations
      functionOverrideString = ''

      if 'Termination Criteria' in moduleConfig:
        functionOverrideString += '/**\n'
        functionOverrideString += '* @brief Determines whether the module can trigger termination of an experiment run.\n'
        functionOverrideString += '* @return True, if it should trigger termination; false, otherwise.\n'
        functionOverrideString += '*/\n'
        functionOverrideString += ' bool checkTermination() override;\n'

      functionOverrideString += '/**\n'
      functionOverrideString += '* @brief Obtains the entire current state and configuration of the module.\n'
      functionOverrideString += '* @param js JSON object onto which to save the serialized state of the module.\n'
      functionOverrideString += '*/\n'
      functionOverrideString += ' void getConfiguration(knlohmann::json& js) override;\n'

      functionOverrideString += '/**\n'
      functionOverrideString += '* @brief Sets the entire state and configuration of the module, given a JSON object.\n'
      functionOverrideString += '* @param js JSON object from which to deserialize the state of the module.\n'
      functionOverrideString += '*/\n'
      functionOverrideString += ' void setConfiguration(knlohmann::json& js) override;\n'

      functionOverrideString += '/**\n'
      functionOverrideString += '* @brief Applies the module\'s default configuration upon its creation.\n'
      functionOverrideString += '* @param js JSON object containing user configuration. The defaults will not override any currently defined settings.\n'
      functionOverrideString += '*/\n'
      functionOverrideString += ' void applyModuleDefaults(knlohmann::json& js) override;\n'

      functionOverrideString += '/**\n'
      functionOverrideString += '* @brief Applies the module\'s default variable configuration to each variable in the Experiment upon creation.\n'
      functionOverrideString += '*/\n'
      functionOverrideString += ' void applyVariableDefaults() override;\n'

      if 'Available Operations' in moduleConfig:
        functionOverrideString += '/**\n'
        functionOverrideString += '* @brief Runs the operation specified on the given sample. It checks recursively whether the function was found by the current module or its parents.\n'
        functionOverrideString += '* @param sample Sample to operate on. Should contain in the "Operation" field an operation accepted by this module or its parents.\n'
        functionOverrideString += '* @param operation Should specify an operation type accepted by this module or its parents.\n'
        functionOverrideString += '* @return True, if operation found and executed; false, otherwise.\n'
        functionOverrideString += '*/\n'
        functionOverrideString += ' bool runOperation(std::string operation, korali::Sample& sample) override;\n'

      if 'Conditional Variables' in moduleConfig:
        functionOverrideString += '/**\n'
        functionOverrideString += '* @brief Retrieves the pointer of a conditional value of a distribution property.\n'
        functionOverrideString += '* @param property Name of the property to find.\n'
        functionOverrideString += '* @return The pointer to the property..\n'
        functionOverrideString += '*/\n'
        functionOverrideString += ' double* getPropertyPointer(const std::string& property) override;\n'

      newHeaderString = moduleTemplateHeaderString.replace(
          'public:', 'public: \n' + functionOverrideString + '\n')

      # Adding Doxygen Information

      doxyClassHeader = '/**\n'
      doxyClassHeader += '* @brief Class declaration for module: ' + moduleConfig[
          "Class"] + '.\n'
      doxyClassHeader += '*/\n'
      newHeaderString = newHeaderString.replace('class ',
                                                doxyClassHeader + 'class ')

      if (not moduleConfig["Is Leaf"]):
        doxyNamespaceHeader = '/** \\namespace ' + moduleConfig[
            "Namespace"] + '\n'
        doxyNamespaceHeader += '* @brief Namespace declaration for modules of type: ' + moduleConfig[
            "Namespace"] + '.\n'
        doxyNamespaceHeader += '*/\n\n'
        newHeaderString = doxyNamespaceHeader + newHeaderString

      # Adding declarations
      declarationsString = createHeaderDeclarations(moduleConfig)
      newHeaderString = newHeaderString.replace(
          'public:', 'public: \n' + declarationsString + '\n')

      # Retrieving variable declarations
      variableDeclarationList += createVariableDeclarations(moduleConfig)

      # Saving new header .hpp file
      moduleNewHeaderFile = moduleDir + '/' + moduleFilename + '.hpp'
      save_if_different(moduleNewHeaderFile, newHeaderString)

      ###### Creating code file

      moduleBaseCodeFileName = moduleDir + '/' + moduleFilename + '._cpp'
      moduleNewCodeFile = moduleDir + '/' + moduleFilename + '.cpp'
      baseFileTime = os.path.getmtime(moduleBaseCodeFileName)
      newFileTime = baseFileTime
      if (os.path.exists(moduleNewCodeFile)):
        newFileTime = os.path.getmtime(moduleNewCodeFile)

      if (baseFileTime >= newFileTime):
        with open(moduleBaseCodeFileName, 'r') as file:
          moduleBaseCodeString = file.read()
        moduleBaseCodeString += '\n\n' + moduleCodeString
        save_if_different(moduleNewCodeFile, moduleBaseCodeString)

###### Updating module source file

moduleBaseCodeFileName = modulesDir + '/module._cpp'
moduleNewCodeFile = modulesDir + '/module.cpp'
baseFileTime = os.path.getmtime(moduleBaseCodeFileName)
newFileTime = baseFileTime
if (os.path.exists(moduleNewCodeFile)):
  newFileTime = os.path.getmtime(moduleNewCodeFile)

if (baseFileTime >= newFileTime):
  with open(moduleBaseCodeFileName, 'r') as file:
    moduleBaseCodeString = file.read()
  newBaseString = moduleBaseCodeString.replace('// Module Include List',
                                               moduleIncludeList)
  newBaseString = newBaseString.replace(' // Module Selection List',
                                        moduleDetectionList)
  save_if_different(moduleNewCodeFile, newBaseString)

###### Updating module header file

moduleBaseHeaderFileName = modulesDir + '/module._hpp'
moduleNewHeaderFile = modulesDir + '/module.hpp'
with open(moduleBaseHeaderFileName, 'r') as file:
  moduleBaseHeaderString = file.read()
newBaseString = moduleBaseHeaderString
save_if_different(moduleNewHeaderFile, newBaseString)

###### Updating variable header file

variableBaseHeaderFileName = koraliDir + '/variable/variable._hpp'
variableNewHeaderFile = koraliDir + '/variable/variable.hpp'
with open(variableBaseHeaderFileName, 'r') as file:
  variableBaseHeaderString = file.read()
newBaseString = variableBaseHeaderString
newBaseString = newBaseString.replace(' // Variable Declaration List',
                                      variableDeclarationList)
save_if_different(variableNewHeaderFile, newBaseString)

print("[Korali] End Parser\n")
