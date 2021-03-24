#!/usr/bin/env bash

if [ $# -gt 0 ]; then
  cd $1
fi

exit_code=0

# Check Code Formatting and documentation

#echo "----------------------------------------------"
#echo "[Korali] Beginning code formatting check..."
#echo "----------------------------------------------"
#
#pushd ../../tools/style/  > /dev/null
#exit_code=$?
#
##FIXME: [garampat@mavt.ethz.ch; 2021-03-23] Style check deactivated until fixed.
#./style_cxx.sh check
#exit_code=$(( $exit_code || $? ))
#
## FIXME: [fabianw@mavt.ethz.ch; 2021-02-17] should python code not also be checked?
#
#popd  > /dev/null
#exit_code=$(( $exit_code || $? ))


echo "----------------------------------------------"
echo "[Korali] Beginning documentation building..."
echo "----------------------------------------------"

pushd ../../docs/  > /dev/null
exit_code=$(( $exit_code || $? ))

./build.sh
exit_code=$(( $exit_code || $? ))

popd  > /dev/null
exit_code=$(( $exit_code || $? ))

exit $exit_code
