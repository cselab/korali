#! /usr/bin/env python3
from subprocess import call

r = call(["python3", "run-phase0.py"])
if r!=0:
  exit(r)

r = call(["python3", "run-phase1.py"])
if r!=0:
  exit(r)

r = call(["python3", "run-phase2.py"])
if r!=0:
  exit(r)

r = call(["python3", "run-phase3a.py"])
if r!=0:
  exit(r)

r = call(["python3", "run-phase3b.py"])
if r!=0:
  exit(r)

exit(0)
