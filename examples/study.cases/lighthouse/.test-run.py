#! /usr/bin/env python3
from subprocess import call

r = call(["python3", "run-example1.py"])
if r!=0:
  exit(r)

r = call(["python3", "run-example2.py"])
if r!=0:
  exit(r)

exit(0)
