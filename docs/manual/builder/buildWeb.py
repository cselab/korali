#!/usr/bin/env python3

import os
import json
import sys

koraliDir = os.path.abspath(
    os.path.dirname(os.path.realpath(__file__)) + '/../..')

from buildModules import *
from buildTests import *
from buildTutorials import *

# Processing Modules
buildModules(koraliDir + '/source')

# Processing Tutorials
buildTutorials(koraliDir)

# Processing Tests
buildTests(koraliDir)
