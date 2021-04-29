#!/usr/bin/env python3
import sys
import os
import argparse
from builders import *


parser = argparse.ArgumentParser()
parser.add_argument('--dir', '-d', default='./', help='Korali root directory')
args = parser.parse_args()

koraliDir = os.path.abspath(args.dir)
modulesDir = os.path.join( koraliDir, 'source', 'modules' )

if not os.path.exists(modulesDir):
  sys.exit("[Korali] Error:  source/modules/ not founde in ", koraliDir)


cnt = 0
for moduleDir, relDir, fileNames in os.walk( modulesDir ):
    for fileName in fileNames:
        if '.config' in fileName:
            _name = os.path.splitext(fileName)[0]
            print( os.path.join(moduleDir,_name+'._hpp'),
                   os.path.join(moduleDir,_name+'._cpp'),
                   os.path.join(moduleDir,_name+'.config'))
            cnt += 1

print(cnt)