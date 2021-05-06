#! /usr/bin/env python3
import os
import sys
import pybind11

flags = dict()
flags['CXX'] = sys.argv[1]
flags['PYBIND11_INCLUDES'] =  pybind11.get_include()

with open("flags.in", 'w') as f:
   f.write(str(flags))
   
