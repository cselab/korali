#! /usr/bin/env python3
from subprocess import call

r = call(["python3", "run-mcmc-exponential.py"])
if r!=0:
  exit(r)

r = call(["python3", "run-mcmc-gaussian.py"])
if r!=0:
  exit(r)

r = call(["python3", "run-mcmc-gaussian5d.py"])
if r!=0:
  exit(r)

r = call(["python3", "run-mcmc-laplace.py"])
if r!=0:
  exit(r)

r = call(["python3", "run-multinest-gaussian5d.py"])
if r!=0:
  exit(r)

r = call(["python3", "run-nested-exponential.py"])
if r!=0:
  exit(r)

r = call(["python3", "run-nested-gaussian.py"])
if r!=0:
  exit(r)

r = call(["python3", "run-nested-gaussian5d.py"])
if r!=0:
  exit(r)

r = call(["python3", "run-nested-laplace.py"])
if r!=0:
  exit(r)

r = call(["python3", "run-tmcmc-exponential.py"])
if r!=0:
  exit(r)

r = call(["python3", "run-tmcmc-gaussian.py"])
if r!=0:
  exit(r)

r = call(["python3", "run-tmcmc-gaussian5d.py"])
if r!=0:
  exit(r)

r = call(["python3", "run-tmcmc-laplace.py"])
if r!=0:
  exit(r)

exit(0)
