#! /usr/bin/env python3
from subprocess import call

# FIXME test takes too long
r = call(["python3", "run-mocmaes.py"])
if r!=0:
  exit(r)

exit(0)
