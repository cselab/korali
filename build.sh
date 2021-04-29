#!/usr/bin/env bash

rm -rf build
rm -rf test_install
CXX=clang++ CC=clang meson setup build --buildtype release --prefix $(pwd -P)/test_install  
# --force-fallback-for=gsl
# meson compile -C build
# meson test -C build
# meson install -C build
