#!/usr/bin/env bash

if [ $# -gt 0 ]; then
  cd $1
fi

##### Deleting Previous Results

echo "  + Deleting previous results..."
rm -rf _korali_result*
exit_code=$?

##### Creating test files

echo "  + Creating test files..."

rm -rf __test-*
exit_code=$(( $exit_code || $? ))

for file in *.py
do
  sed -e 's%Defining Termination Criteria%Defining Termination Criteria\ne["Solver"]["Termination Criteria"]["Max Generations"] = 20\n%g' \
        ${file} > __test-${file}
  exit_code=$(( $exit_code || $? ))
done

##### Running Test

for file in __test-*.py
do
  echo "Running ${file} ..."
  OMP_NUM_THREADS=4 python3 ${file}
  exit_code=$(( $exit_code || $? ))
done

##### Deleting Tests

rm -rf __test-*
exit_code=$(( $exit_code || $? ))


exit $exit_code