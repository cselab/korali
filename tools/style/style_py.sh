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
    "$fileDir/../../python"
    "$fileDir/../../tests"
)

function check()
{
 if [ ! $? -eq 0 ]
 then
  echo "[Korali] Error fixing style." 
  exit -1
 fi 
}

function check_syntax()
{
    for d in "${dst[@]}"; do
        src_files=`find $d -type f -not -name "__*"  -name "*.py"`

        diff=`echo $src_files | xargs -n6 -P2 python3 -m yapf --style=yapf -d "$@"`

        if [ ! "$diff" == "" ]; then
            echo "[Korali] Error: Python Code formatting is not normalized:"
            echo $diff | head -n 5
            echo "[Korali] Solution: Please run '$fileDir/style_py.sh fix' to fix it."
            exit -1
        fi
    done
}

function fix_syntax()
{
    for d in "${dst[@]}"; do
        src_files=`find $d -type f -not -name "__*"  -name "*.py"`

        echo $src_files | \
            xargs -n6 -P2 python3 -m yapf --style=yapf -i "$@"

        check
    done
}


##############################################
### Testing Python Code Style
##############################################
PIP_USER=$(python3 -c "import sys; hasattr(sys, 'real_prefix') or print('--user')")

python3 -m yapf --version > /dev/null
if [ $? -ne 0 ]; then
  echo "[Korali] yapf not found, trying to install it automatically."
  python3 -m pip install $PIP_USER yapf; check
fi

if [[ "${task}" == 'check' ]]; then
    check_syntax
else
    fix_syntax
fi

exit 0
