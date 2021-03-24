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

sed -e 's%\plt.%#plt.%g' run-sin.py > __test-sin.py
exit_code=$(( $exit_code || $? ))

##### Running Test

OMP_NUM_THREADS=4 python3 ./__test-sin.py
exit_code=$(( $exit_code || $? ))

##### Deleting Tests

#rm -rf __test-*
exit_code=$(( $exit_code || $? ))


exit $exit_code
