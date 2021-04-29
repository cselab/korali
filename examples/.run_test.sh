#! /usr/bin/env bash

if [ $# -gt 0 ]; then
  cd $1
fi

### Testing examples

exampleDirs=`find . -type d -not -path "*/_*" -not -path "*/study.cases/*" -not -name "study.cases" | sort | awk '$0 !~ last "/" {print last} {last=$0} END {print last}'`
exit_code=$?


for dir in $exampleDirs
do
  echo "----------------------------------------------"
  echo " + Entering Folder: $dir"
  echo "----------------------------------------------"
  pushd $dir > /dev/null
  exit_code=$(( $exit_code || $? ))

  ./.run_test.sh
  exit_code=$(( $exit_code || $? ))

  popd > /dev/null
  exit_code=$(( $exit_code || $? ))
done

### Testing Study Cases

exampleDirs=`ls -d study.cases/*/`

for dir in $exampleDirs
do
  echo "----------------------------------------------"
  echo " + Entering Folder: $dir"
  echo "----------------------------------------------"
  pushd $dir > /dev/null
  exit_code=$(( $exit_code || $? ))

  ./.run_test.sh
  exit_code=$(( $exit_code || $? ))

  popd > /dev/null
  exit_code=$(( $exit_code || $? ))
done

exit $exit_code

