from pathlib import Path
import json
import re

from . import header_builders as hb


def pathSplitAtDir( path, dir ):
  ''' Return the path in the `path` variable up to the dir folder.
      e.g. if path=Path('/a/b/c/d') and dir='c', returns Path('a/b/c')

      Parameters
      ----------
      path : pathlib.Path object

      dir : string
  '''
  p = Path('/')
  for i in path.parts:
    p = p.joinpath(i)
    if i==dir: break
  return p


def loadModuleConfiguration( configFilePath, templateFilePath ):

  moduleConfig = json.loads( configFilePath.read_text() )
  modulesPath = pathSplitAtDir(configFilePath,'modules')

  moduleConfig['Name'] = str( configFilePath.parent.parts[-1] )
  moduleConfig['Class Name'] = moduleConfig['Module Data']['Class Name']
  moduleConfig['Parent Class Name'] = moduleConfig['Module Data']['Parent Class Name']
  moduleConfig['Namespace'] = moduleConfig['Module Data']['Namespace']
  moduleConfig['Module Type'] = str( Path(*configFilePath.relative_to(modulesPath).parts[1:-1]) )
  moduleConfig['Relative Path'] = str( configFilePath.parent.relative_to(modulesPath) )

  guard = '_'.join(moduleConfig['Namespace'])
  guard = '_' + guard.upper() + '_' + moduleConfig['Class Name'].upper() + '_'
  moduleConfig['Include Guard'] = guard

  return moduleConfig


def checkNamespaceKeys(moduleConfig, templateFilePath, moduleTemplate):
  namespaceCount = len(moduleConfig["Module Data"]["Namespace"])
  numStr = [''] + list(range(namespaceCount))

  for n in numStr:
    startStr = rf"startNamespace{n}"
    regex = re.compile(rf"@\b{startStr}\b")
    findStart = regex.findall(moduleTemplate, re.MULTILINE)
    endStr = rf"endNamespace{n}"
    regex = re.compile(rf"@\b{endStr}\b")
    findEnd = regex.findall(moduleTemplate, re.MULTILINE)

    if len(findStart)!=len(findEnd):
      sys.exit(f'[Korali] Error: the number of occurrences of {startStr} ({len(findStart)}) is not equal to {endStr}({len(findEnd)}) in file: {templateFilePath}')
    if len(findStart)>1 or len(findEnd)>1:
      sys.exit(f'[Korali] Error: the number of occurrences of {startStr} or {endStr} should be 0 or 1 in file: {templateFilePath}')


def replaceKeys( moduleConfig, codeString ):
  codeString = codeString.replace( '@startIncludeGuard', hb.startIncludeGuard(moduleConfig) )
  codeString = codeString.replace( '@endIncludeGuard', hb.endIncludeGuard(moduleConfig) )

  codeString = codeString.replace( '@className', moduleConfig['Class Name'] )
  codeString = codeString.replace( '@parentClassName', moduleConfig['Parent Class Name'] )

  regex = re.compile(r"@\bstartNamespace\b")
  codeString = regex.sub(hb.startNamespace(moduleConfig), codeString, re.MULTILINE)
  regex = re.compile(r"@\bendNamespace\b")
  codeString = regex.sub(hb.endNamespace(moduleConfig), codeString, re.MULTILINE)

  namespaceCount = len(moduleConfig["Module Data"]["Namespace"])

  for n in range(namespaceCount):
    regex = re.compile(rf"@\bstartNamespace{n}\b")
    rep_str = "namespace " + moduleConfig["Module Data"]["Namespace"][n] + "\n{\n"
    codeString = regex.sub(rep_str, codeString, re.MULTILINE)

    regex = re.compile(rf"@\bendNamespace{n}\b")
    rep_str = "} /* " + moduleConfig["Module Data"]["Namespace"][n] + " */ "
    codeString = regex.sub(rep_str, codeString, re.MULTILINE)

  return codeString