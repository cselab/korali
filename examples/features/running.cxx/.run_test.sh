#!/usr/bin/env bash

if [ $# -gt 0 ]; then
  cd $1
fi

##### Deleting Previous Results

echo "  + Deleting previous results..."
rm -rf _korali_result*

##### Recompiling C++

make clean
exit_code=$?

make -j4
exit_code=$(( $exit_code || $? ))

###### If this is macOS, C++ linking may not be automatic: do not run test
arch="$(uname -s)"
if [ "$arch" == "Darwin" ]; then
 echo "[Korali] MacOS (Darwin) System Detected, aborting test."
 exit 0
fi

##### Running Tests

./run-cmaes
exit_code=$(( $exit_code || $? ))

./run-cmaes-direct
exit_code=$(( $exit_code || $? ))

./run-lmcma
exit_code=$(( $exit_code || $? ))

./run-lmcma-direct
exit_code=$(( $exit_code || $? ))

./run-tmcmc
exit_code=$(( $exit_code || $? ))


retun $exit_code