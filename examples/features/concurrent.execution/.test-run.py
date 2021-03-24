#! /usr/bin/env python3
from subprocess import call

for k in [1, 2, 4, 8]:
  r = call(["python3", "run.py", str(k)])
  if r!=0:
    exit(r)

exit(0)
