#!/usr/bin/env bash

if [ $# -gt 0 ]; then
  cd $1
fi

echo "[Korali] Checking Pip Installation"
python3 -m pip check korali
exit_code=$?

echo "[Korali] Checking korali.plotter"
python3 -m korali.plotter --check
exit_code=$(( $exit_code || $? ))

# TODO: @Fabian: how should we test for these?
#echo "[Korali] Checking korali.cxx"
#python3 -m korali.cxx --cflags
#exit_code=$(( $exit_code || $? ))
#
#python3 -m korali.cxx --compiler
#exit_code=$(( $exit_code || $? ))
#
#python3 -m korali.cxx --libs
#exit_code=$(( $exit_code || $? ))

exit $exit_code
