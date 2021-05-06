#!/usr/bin/env bash

if [ $# -gt 0 ]; then
  cd $1
fi

echo "-------------------------------------"
echo "[Korali] Beginning Stat Test 006"
exit_code=$?

constraints=(
"None"
"Inactive"
"Active at Max 1"
"Active at Max 2"
"Inactive at Max 1"
"Inactive at Max 1"
"Mixed"
"Stress"
)

for c in "${constraints[@]}"
do

  echo "-------------------------------------"
  echo "Testing Constraints: ${c}"
  echo "Running File: run-ccmaes.py"

  python3 ./run-ccmaes.py --constraint "${c}"
  exit_code=$(( $exit_code || $? ))

  echo "[Korali] Removing results..."
  rm -rf "_korali_result"
  exit_code=$(( $exit_code || $? ))

  echo "-------------------------------------"

done

exit $exit_code