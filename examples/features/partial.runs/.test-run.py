#! /usr/bin/env python3
from subprocess import call

r = call(["python3", "run-cmaes.py"])
if r!=0:
  exit(r)

r = call(["python3", "run-dea.py"])
if r!=0:
  exit(r)

r = call(["python3", "run-mcmc.py"])
if r!=0:
  exit(r)

r = call(["python3", "run-multiple.py"])
if r!=0:
  exit(r)

r = call(["python3", "run-propagation.py"])
if r!=0:
  exit(r)

r = call(["python3", "run-rprop.py"])
if r!=0:
  exit(r)

r = call(["python3", "run-tmcmc.py"])
if r!=0:
  exit(r)

exit(0)
