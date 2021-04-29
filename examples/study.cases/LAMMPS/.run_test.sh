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

sed 's/k.run(/k["Dry Run"] = True; k.run(/g' run-cmaes.py > __test-cmaes.py
exit_code=$(( $exit_code || $? ))
sed 's/k.run(/k["Dry Run"] = True; k.run(/g' run-tmcmc.py > __test-tmcmc.py
exit_code=$(( $exit_code || $? ))

##### Running Tests

echo "  + Running test files..."

python3 ./__test-cmaes.py
exit_code=$(( $exit_code || $? ))

python3 ./__test-tmcmc.py
exit_code=$(( $exit_code || $? ))

##### Deleting Tests

echo "  + Removing test files..."
rm __test*


exit $exit_code