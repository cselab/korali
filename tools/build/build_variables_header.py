#!/usr/bin/env python3
import os
import re
import argparse

from codeBuilders import builders


def parse_args():
    parser = argparse.ArgumentParser()
    # yapf: disable
    parser.add_argument('--input', nargs='+', type=str, help='Input file(s)', required=True)
    parser.add_argument('--output', type=str, help='Output file')
    # yapf: enable
    return parser.parse_known_args()


def translate(src, dst, configFileList):

    builders.buildVariablesHeader(configFileList, src, dst)

    # print the file path for each config file
    # print(f"Have {len(configFileList)} .config files:")
    # for p in configFileList:
    #     print(f"\t{p}")


def main(args):
    # because of unknown number of input files, convention is that the first
    # (required) file in `input` is the `variable._hpp` template.  The rest are
    # .config files
    template = args.input[0]
    config_files = args.input[1:]

    if args.output is None:
        args.output = os.path.splitext(template)[0] + '.hpp'

    translate(template, args.output, config_files)


if __name__ == "__main__":
    args, _ = parse_args()
    main(args)