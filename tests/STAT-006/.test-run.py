#! /usr/bin/env python3
from subprocess import call

r = call(["python3", "run-ccmaes.py", "--constraint", "None"])
if r!=0:
  exit(r)

r = call(["python3", "run-ccmaes.py", "--constraint", "Inactive"])
if r!=0:
  exit(r)

r = call(["python3", "run-ccmaes.py", "--constraint", "Active at Max 1"])
if r!=0:
  exit(r)

r = call(["python3", "run-ccmaes.py", "--constraint", "Active at Max 2"])
if r!=0:
  exit(r)

r = call(["python3", "run-ccmaes.py", "--constraint", "Inactive at Max 1"])
if r!=0:
  exit(r)

r = call(["python3", "run-ccmaes.py", "--constraint", "Inactive at Max 2"])
if r!=0:
  exit(r)

r = call(["python3", "run-ccmaes.py", "--constraint","Mixed"])
if r!=0:
  exit(r)

r = call(["python3", "run-ccmaes.py", "--constraint", "Stress"])
if r!=0:
  exit(r)

exit(0)
