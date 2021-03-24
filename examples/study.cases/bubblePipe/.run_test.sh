#!/usr/bin/env bash

if [ $# -gt 0 ]; then
  cd $1
fi

##### Deleting Previous Results

echo "  + Deleting previous results..."
rm -rf _result*
exit_code=$?

# FIXME: [garampat@mavt.ethz.ch; 2021-03-23]
###### If this is macOS, C++ linking may not be automatic: do not run test
arch="$(uname -s)"
if [ "$arch" == "Darwin" ]; then
 echo "[Korali] MacOS (Darwin) System Detected, aborting test."
 exit 0
fi

##### Running Tests

#./run-korali
# exit_code=$(( $exit_code || $? ))


exit $exit_code
