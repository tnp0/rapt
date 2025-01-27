#!/usr/bin/env python

from __future__ import print_function
import os
import sys
import subprocess

sofiles = [ ]

for directory in sys.argv[2:]:

    for fn in os.listdir(directory):
        fn = os.path.join(directory, fn)

        if not fn.endswith(".so.o"):
            continue
        if not os.path.exists(fn[:-2] + ".libs"):
            continue

        sofiles.append(fn[:-2])

# The raw argument list.
args = [ ]

for fn in sofiles:
    afn = fn + ".o"
    libsfn = fn + ".libs"

    args.append(afn)
    with open(libsfn) as fd:
        data = fd.read()
        args.extend(data.split(" "))

unique_args = [ ]
while args:
    a = args.pop()
    if a in ('-L', ):
        continue
    if a not in unique_args:
        unique_args.insert(0, a)

print('Biglink create %s library' % sys.argv[1])

args = os.environ['LD'].split() + os.environ["LDFLAGS"].split() + [ '-Wl,-Bsymbolic', '-shared', '-O3', '-o', sys.argv[1] ] + unique_args

for i in args:
    print(i)

rv = subprocess.call(args)
sys.exit(rv)
