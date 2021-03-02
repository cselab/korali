#!/usr/bin/env bash
if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <check|fix>"
    exit 1
fi
task="${1}"; shift
fileDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# check these destinations
dst=(
    "$fileDir/../../examples"
    "$fileDir/../../source"
    "$fileDir/../../tests"
    )

function check()
{
  if [ ! $? -eq 0 ]; then 
    echo "[Korali] Error fixing style."
    exit -1 
  fi
}

function check_syntax()
{
    # If run-clang-format is not installed, clone it
    if [ ! -f  run-clang-format/run-clang-format.py ]; then

      # FIXME: [fabianw@mavt.ethz.ch; 2021-02-17] should this not be a git submodule?
      git clone https://github.com/Sarcasm/run-clang-format.git
      if [ ! $? -eq 0 ]; then
        echo "[Korali] Error installing run-clang-format."
        exit 1
      fi

    fi

    for d in "${dst[@]}"; do
      python3 run-clang-format/run-clang-format.py --recursive ${d} --extensions cpp,hpp,_cpp,_hpp > /dev/null

      if [ ! $? -eq 0 ]; then
        echo "[Korali] Error: C++ Code formatting in file ${d} is not normalized."
        echo "[Korali] Solution: Please run '$fileDir/style_cxx.sh fix' to fix it."
        exit -1
      fi
    done
}

function fix_syntax()
{
    for d in "${dst[@]}"; do
      src_files=`find ${d} -type f -not -name "__*" -name "*.hpp" -name "*.cpp" -name "*._hpp" -name "*._cpp"`

      echo $src_files | xargs -n6 -P2 clang-format -style=file -i "$@"

      check
    done
}

##############################################
### Testing/fixing C++ Code Style
##############################################
command -v clang-format >/dev/null
if [ ! $? -eq 0 ]; then
    echo "[Korali] Error: please install clang-format on your system."
    exit -1
fi
 
if [[ "${task}" == 'check' ]]; then
    check_syntax
else
    fix_syntax
fi

exit 0
