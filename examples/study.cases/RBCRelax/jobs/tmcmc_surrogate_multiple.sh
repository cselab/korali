#!/bin/bash -l
set -eu

date
cd ..
echo "Running Korali+Mirheo ..."
./run-tmcmc-surrogate-multiple.py --pop 10000
date