#! /usr/bin/env python3
from subprocess import call

r = call(["python3", "run-ffn.py"])
if r!=0:
  exit(r)

r = call(["python3", "run-rnn.py"])
if r!=0:
  exit(r)

exit(0)
