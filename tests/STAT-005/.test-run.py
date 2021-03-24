#! /usr/bin/env python3
from subprocess import call

r = call(["python3", "run-maxcmaes1.py"])
if r!=0:
  exit(r)

r = call(["python3", "run-maxcmaes2.py"])
if r!=0:
  exit(r)

r = call(["python3", "run-mincmaes1.py"])
if r!=0:
  exit(r)

r = call(["python3", "run-mincmaes2.py"])
if r!=0:
  exit(r)

exit(0)
