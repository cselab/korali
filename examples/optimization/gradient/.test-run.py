#! /usr/bin/env python3
from subprocess import call

r = call(["python3", "run-adam.py"])
if r!=0:
  exit(r)

r = call(["python3", "run-rprop.py"])
if r!=0:
  exit(r)

# FIXME AdaBelief fails

exit(0)
