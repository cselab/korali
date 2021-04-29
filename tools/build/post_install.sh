#!/usr/bin/env bash
install_base="$1"; shift
lib_base="$1"; shift

cd ${install_base}
lib_suffix="$(basename ${lib_base}*)"
suffix="${lib_suffix##*.}"
lib_short="${lib_base}.${suffix}"
ln -sf ${lib_suffix} ${lib_short}
exit 0
