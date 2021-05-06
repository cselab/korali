#! /usr/bin/env python3
from subprocess import call

r = call(["python3", "run-cmaes.py"])
if r!=0:
  exit(r)

r = call(["python3", "run-cmaes.py"])
if r!=0:
  exit(r)

# FIXME the following scripts fail
# r = call(["python3", "run-gfpt.py"])
# if r!=0:
#   exit(r)
#
# r = call(["python3", "run-gfpt.py"])
# if r!=0:
#   exit(r)
#
#
# r = call(["python3", "run-sin.py"])
# if r!=0:
#   exit(r)
#
# r = call(["python3", "run-sin.py"])
# if r!=0:
#   exit(r)

exit(0)
