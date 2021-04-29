#!/usr/bin/env python3
import os
import re
import argparse

from codeBuilders import builders

def parse_args():
    parser = argparse.ArgumentParser()
    # yapf: disable
    parser.add_argument('--input', nargs=2, type=str, help='Input files', required=True)
    parser.add_argument('--config', type=str, help='Config file', required=True)
    parser.add_argument('--output', nargs=2, type=str, help='Output files')
    # yapf: enable
    return parser.parse_known_args()


def get_output_list(files):
    out = []
    for f in files:
        suffix = os.path.splitext(f)[1].replace('_', '')
        out.append(re.sub(r'\._(hpp|cpp)\s*$', suffix, f))
    return out


def main(args):
    if args.output is None:
        args.output = get_output_list(args.input)

    for src, dst in zip(args.input, args.output):
        builders.buildCodeFromTemplate( args.config, src,  dst   )

if __name__ == "__main__":
    args, _ = parse_args()
    main( args )