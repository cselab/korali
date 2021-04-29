#! /usr/bin/env python3
from subprocess import call

r = call(["python3", "run-execution.py"])
if r!=0:
  exit(r)

r = call(["python3", "run-uncertainty-propagation.py"])
if r!=0:
  exit(r)

exit(0)
