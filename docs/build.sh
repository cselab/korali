#!/bin/bash

function check()
{
 if [ ! $? -eq 0 ]
 then
  echo "[Korali] Error building site."
  exit -1
 fi
}

# FIXME @george why do we need to build the code here?
# Building Korali source
# pushd ../source
# check
#
# python3 ./build.py
# check
#
# popd
# check

# Installing shpinx, mkdocs, and materials theme
python3 -m pip install sphinx --user
check

python3 -m pip install sphinx_rtd_theme --user
check

python3 -m pip install Pygments --user
check


# Building User Manual
pushd manual
check

pushd builder
check

python3 ./buildExamples.py
check

python3 ./buildFeatures.py
check

python3 ./buildTests.py
check

python3 ./buildModules.py
check

python3 ./buildTools.py
check

popd
check

make html
check

popd

# Inserting user manual into website

mkdir -p web/docs
check

cp -r manual/.build/html/* web/docs
check

# FIXME: [fabianw@mavt.ethz.ch; 2021-02-17] refactor doxygen into sphinx
doxygenBin=$(command -v doxygen >/dev/null)
if [ ! $? -eq 0 ]; then
    echo "[Korali] Error: please install doxygen on your system."
    exit -1
fi

# Running Doxygen
echo "Using $doxygenBin for C++ documentation..."
$doxygenBin doxygen.config 2>&1 | grep -E 'warning|error'
if [ $? -eq 0 ]; then
 echo "[Korali] Error running doxygen."
 echo "[Korali] Hint: Check if there is any missing variable/function documentation."
 exit -1
fi

echo "[Korali] Webpage Build complete."
