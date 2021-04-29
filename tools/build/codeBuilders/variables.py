
def getVariableType(v):
  """ Replacing bools with ints for Python compatibility """
  vType = v['Type']
  vType = vType.replace('bool', 'int')
  vType = vType.replace('std::function<void(korali::Sample&)>', 'std::uint64_t')
  return vType

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