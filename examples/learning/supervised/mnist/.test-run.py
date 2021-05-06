#! /usr/bin/env python3
from subprocess import call

r = call(["bash", "get_data.sh"])
if r!=0:
  exit(r)

r = call(["python3", "run-mnist.py", "--test"])
if r!=0:
  exit(r)

exit(0)
