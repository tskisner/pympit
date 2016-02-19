#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals, with_statement

from mpi4py import MPI

import sys
import os
import numpy as np
import scipy as sc

# Astropy has known problems with pyinstaller.
# See pull requests #4531 and #960
#
#from astropy.io import fits

import argparse

import subprocess as sp

import pympit as pt


parser = argparse.ArgumentParser(description='Run an MPI test in python with subprocess forking')
args = parser.parse_args()

comm = MPI.COMM_WORLD

start = MPI.Wtime()

local_out = []

proc = sp.Popen(['pympit_worker.py'], stdout=sp.PIPE, stderr=sp.PIPE)
outs, errs = proc.communicate()
proc.wait()

local_out.append(outs)

stop = MPI.Wtime()
elapsed = stop - start

comm.Barrier()

for p in range(comm.size):
    if p == comm.rank:
        print("proc {:02d} {:.3f}s:".format(p, elapsed))
        for line in local_out:
            print("  {}".format(line.rstrip()))
    comm.Barrier()


