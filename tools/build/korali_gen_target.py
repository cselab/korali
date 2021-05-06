#!/usr/bin/env python3
import os
import sys
import random
import string
import inspect
import argparse

import argparse


def parse_args(*, partial=False):
    parser = argparse.ArgumentParser()
    # yapf: disable
    parser.add_argument('-n', '--name', type=str, help="Build target name (input basename)")
    parser.add_argument('-r', '--recursive', type=str, help="Regenerate all targets with an associated .config file below the directory `recursive`")
    # yapf: enable
    if partial:
        return parser.parse_known_args()
    else:
        return parser.parse_args()


def generate_build_file(names, *, outpath='.'):
    """
    Generate a meson.build file for the targets contained in `names` in `outpath`.
    """
    chars = string.ascii_letters + string.digits
    with open(os.path.join(outpath, 'meson.build'), 'w') as out:
        out.write(
            inspect.cleandoc(f"""
            # generated with `{sys.argv[0]}`
            # If you modify this file, you likely need to modify all other
            # generated targets as well.  See the generator this file was
            # created with.
            header_install_dir = run_command(header_path, [korali_install_headers, meson.current_source_dir()]).stdout().strip()
            """))
        for name in names:
            target = name + '_' + ''.join(random.choice(chars) for i in range(6))
            out.write('\n\n')
            out.write(
                inspect.cleandoc(f"""
            gen_{target} = custom_target('gen_{target}',
                output: ['{name}.cpp', '{name}.hpp'],
                input: files([
                  '{name}._cpp',
                  '{name}._hpp',
                  '{name}.config',
                ]),
                command: [korali_gen, '--input', '@INPUT0@', '@INPUT1@', '--config', '@INPUT2@', '--output', '@OUTPUT@'],
                install: true,
                install_dir: [false, header_install_dir],
            )
            korali_source += gen_{target}
            korali_source_config += files('{name}.config')\n
            """))


def generate_recursive(args):
    for root, dirs, files in os.walk(args.recursive):
        names = []
        for f in files:
            if f.endswith('.config'):
                names.append(os.path.splitext(f)[0])
        if names:
            generate_build_file(sorted(names), outpath=root)


def main(args):
    if args.recursive is not None:
        generate_recursive(args)
    else:
        name = args.name
        generate_build_file([name])


if __name__ == "__main__":
    args = parse_args()
    main(args)
