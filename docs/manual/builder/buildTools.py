#!/usr/bin/env python3

import sys
import os
import json
import shutil
import copy
import glob

toolsSrcDir = '../../../tools'
toolsDstDir = '../using/tools'

shutil.rmtree(toolsDstDir, ignore_errors=True, onerror=None)
os.makedirs(toolsDstDir)

shutil.copyfile(toolsSrcDir + '/plotter/README.rst',
                toolsDstDir + '/plotter.rst')

for file in glob.glob(r'' + toolsSrcDir + '/plotter/*.png'):
  shutil.copy(file, toolsDstDir)

shutil.copyfile(toolsSrcDir + '/profiler/README.rst',
                toolsDstDir + '/profiler.rst')

for file in glob.glob(r'' + toolsSrcDir + '/profiler/examples/*.png'):
  shutil.copy(file, toolsDstDir)

shutil.copyfile(toolsSrcDir + '/rlview/README.rst', toolsDstDir + '/rlview.rst')
