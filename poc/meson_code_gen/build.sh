#!/usr/bin/env bash
rm -rf build
rm -rf test_install
meson setup build --buildtype release --prefix $(pwd -P)/test_install
meson compile -C build
meson install -C build
