#! /usr/bin/env python3
import os
import sys
from korali.cxx.cflags import getcflags
from korali.cxx.libs import getlibs
from korali.cxx.compiler import getcompiler


def main():
  koraliDir = os.path.abspath(
      os.path.dirname(os.path.realpath(__file__)) + '/../')

  if (len(sys.argv) != 2):
    print(
        '[Korali] Syntax error on call to korali.cxx module: Exactly one argument is required (--cflags, --libs, or --compiler).'
    )
    exit(-1)

  makeFlags = dict()
  lineList = [line.rstrip('\n') for line in open(koraliDir + '/Makefile.conf')]
  for line in lineList:
    item = [i.strip() for i in line.split('=', 1)]
    makeFlags[item[0]] = item[1]

  if (sys.argv[1] == '--cflags'):
    correctSyntax = True
    getcflags(koraliDir, makeFlags)
    exit(0)

  if (sys.argv[1] == '--libs'):
    correctSyntax = True
    getlibs(koraliDir, makeFlags)
    exit(0)

  if (sys.argv[1] == '--compiler'):
    correctSyntax = True
    getcompiler(koraliDir, makeFlags)
    exit(0)

  print(
      '[Korali] Syntax error on call to korali.cxx module: Argument \'{0}\' not recognized (--cflags, --libs, or --compiler).'
      .format(sys.argv[1]))
  exit(-1)


if __name__ == '__main__':
  main()
