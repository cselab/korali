#!/usr/bin/env bash
usage() {
    echo "Usage: source ${0} <path to build directory> [<path to source directory>]"
}

if [[ $# -lt 1 ]]; then
    usage
    exit 1
fi

# clean environment if this is not the first invocation in the current shell
if [[ ! -z "${_clean_LD_LIBRARY_PATH}" ]]; then
    export LD_LIBRARY_PATH=${_clean_LD_LIBRARY_PATH}
fi
if [[ ! -z "${_clean_DYLD_LIBRARY_PATH}" ]]; then
    export DYLD_LIBRARY_PATH=${_clean_DYLD_LIBRARY_PATH}
fi
if [[ ! -z "${_clean_PYTHONPATH}" ]]; then
    export PYTHONPATH=${_clean_PYTHONPATH}
fi
export _clean_LD_LIBRARY_PATH=${LD_LIBRARY_PATH}
export _clean_DYLD_LIBRARY_PATH=${DYLD_LIBRARY_PATH}
export _clean_PYTHONPATH=${PYTHONPATH}

# build paths
# using python3 because realpath/readlink do not work reliable on OSX
BUILD_DIR=$(python3 -c "import os; print(os.path.abspath('${1}'))"); shift
SOURCE_DIR=$(pwd -P)
if [[ $# -gt 0 ]]; then
    SOURCE_DIR=$(python3 -c "import os; print(os.path.abspath('${1}'))"); shift
fi
SUBPROJECTS_DIR="${BUILD_DIR}/subprojects"
if [[ -d ${SUBPROJECTS_DIR} ]]; then
    # add shared libraries from subprojects to LD_LIBRARY_PATH
    # FIXME: [fabianw@mavt.ethz.ch; 2021-02-04]
    # Is OSX DYLD_LIBRARY_PATH and '*.dylib'?
    _SUBPROJECT_SO=''
    for so in $(find -L ${SUBPROJECTS_DIR} -type f \( -name "*.so" -o -name "*.dylib" \)); do
        if [[ "${so}" == *"subprojects/"*"/build/"* ]]; then
            # never use something that is below a `build` directory within
            # subprojects.
            continue
        fi
        _SO_DIR="$(dirname ${so})"
        if [[ ! "${_SUBPROJECT_SO}" == *"${_SO_DIR}"* ]]; then
            _SUBPROJECT_SO="${_SO_DIR}:${_SUBPROJECT_SO}"
        fi
    done
    export LD_LIBRARY_PATH="${_SUBPROJECT_SO}${LD_LIBRARY_PATH}"
    export DYLD_LIBRARY_PATH="${_SUBPROJECT_SO}${DYLD_LIBRARY_PATH}"
fi
export LD_LIBRARY_PATH=${BUILD_DIR}/source:${LD_LIBRARY_PATH}
export DYLD_LIBRARY_PATH=${BUILD_DIR}/source:${DYLD_LIBRARY_PATH}
export PYTHONPATH=${SOURCE_DIR}/python:${BUILD_DIR}/source:${PYTHONPATH}
