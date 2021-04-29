#!/usr/bin/env bash

if [ $# -gt 0 ]; then
  cd $1
fi

###### Checking if MPI available ##########

if [[ $MPICXX == "" ]]
then
 echo "[Korali] MPI not installed, skipping test."
 exit 0
fi

##### Deleting Previous Results

echo "  + Deleting previous results..."
rm -rf _korali_result*
exit_code=$?

##### Recompiling C++

make clean
exit_code=$(( $exit_code || $? ))

make -j4
exit_code=$(( $exit_code || $? ))

###### If this is macOS, C++ linking may not be automatic: do not run test
arch="$(uname -s)"
if [ "$arch" == "Darwin" ]; then
 echo "[Korali] MacOS (Darwin) System Detected, aborting test."
 exit 0
fi

##### Running Tests
mpirun -n 9 ./run-cmaes
exit_code=$(( $exit_code || $? ))

mpirun -n 9 ./run-tmcmc
exit_code=$(( $exit_code || $? ))


retun $exit_code