#!/usr/bin/env bash
if [[ ! -z "${_clean_LD_LIBRARY_PATH}" ]]; then
    export LD_LIBRARY_PATH=${_clean_LD_LIBRARY_PATH}
fi
if [[ ! -z "${_clean_PYTHONPATH}" ]]; then
    export PYTHONPATH=${_clean_PYTHONPATH}
fi
