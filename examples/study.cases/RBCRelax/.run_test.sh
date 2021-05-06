#!/usr/bin/env bash

if [ $# -gt 0 ]; then
  cd $1
fi

##### Creating test files

echo "  + Creating test files..."

rm -f _*
exit_code=$?

fileList=`ls *.py`

for file in $fileList
do
  sed -e 's/k.run(/k["Dry Run"] = True; k.run(/g' $file > _$file
  exit_code=$(( $exit_code || $? ))
done

##### Running Tests
echo "  + Running test files..."

for file in $fileList
do
  python3  _$file
  exit_code=$(( $exit_code || $? ))
done

##### Deleting Tests

echo "  + Removing test files..."
rm -f _run*
exit_code=$(( $exit_code || $? ))


exit $exit_code