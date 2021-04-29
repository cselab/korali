#!/usr/bin/env python3
import pathlib
import sys
import os


def main():
    argv = sys.argv
    if len(argv) != 3:
        raise RuntimeError(
            f"Usage: {argv[0]} <header install directory> <absolute path of current header directory>"
        )
    anchor = 'source'  # should this name ever change, this code will be broken
    # all source code with headers must be below `anchor`
    install_base = os.path.join(
        *[x for x in pathlib.PurePath(argv[1].strip()).parts])
    path = pathlib.PurePath(argv[2].strip())
    subpath = []
    append = False
    for part in path.parts:
        if part == anchor:
            append = True
            continue
        if append:
            subpath.append(part)
    print(os.path.join(install_base, *subpath))  # stripped directory name


if __name__ == "__main__":
    main()
