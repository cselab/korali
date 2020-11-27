#!/usr/bin/env python3
import os
from setuptools import *

baseDir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
sourceDir = 'source'
toolsDir = 'tools'

print('[Korali] Building installation setup...')
with open(baseDir + '/VERSION') as f:
  koraliVer = f.read()

koraliFiles = ['libkorali.so', 'Makefile.conf']
for dirpath, subdirs, files in os.walk(sourceDir):
  for x in files:
    if (x.endswith(".hpp") or (x.endswith(".h")) or (x.endswith(".config")) or  x.endswith(".py")):
      relDir = os.path.relpath(dirpath, sourceDir)
      relFile = os.path.join(relDir, x)
      koraliFiles.append(relFile)

setup(
    name='Korali',
    version=koraliVer,
    author='G. Arampatzis, S. Martin, D. Waelchli',
    author_email='martiser@ethz.ch',
    description='High Performance Framework for Uncertainty Quantification and Optimization',
    url='Webpage: https://www.cse-lab.ethz.ch/korali/',
    packages=[ 'korali', 'korali.plotter', 'korali.profiler', 'korali.cxx'  ],
    package_dir={
        'korali': sourceDir,
        'korali.plotter': toolsDir + '/plotter',
        'korali.profiler': toolsDir + '/profiler',
        'korali.cxx': toolsDir + '/cxx'
    },
    include_package_data=True,
    package_data={ 'korali': koraliFiles },
    install_requires=['pybind11', 'numpy', 'matplotlib'],
    license='GNU General Public License v3.0')
