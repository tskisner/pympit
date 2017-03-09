#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals, with_statement

# Attempt to get the time before MPI initialization
import time
prestart = time.time()

from mpi4py import MPI
mpistart = time.time()

import sys
import os
import numpy as np
import scipy as sc

import argparse

import pympit as pt


parser = argparse.ArgumentParser( description='Run an MPI test in python' )
parser.add_argument( '--fftlen', required=False, default=5242880, help='FFT length for math test' )
args = parser.parse_args()

comm = MPI.COMM_WORLD

if comm.rank == 0:
    ts = time.localtime(prestart)
    print("Python interpreter started at {:04d}{:02d}{:02d} {:02d}:{:02d}:{:02d}".format(ts.tm_year, ts.tm_mon, ts.tm_mday, ts.tm_hour, ts.tm_min, ts.tm_sec))
    ts = time.localtime(mpistart)
    print("MPI init finished at {:04d}{:02d}{:02d} {:02d}:{:02d}:{:02d}".format(ts.tm_year, ts.tm_mon, ts.tm_mday, ts.tm_hour, ts.tm_min, ts.tm_sec))

startup = pt.work.since_start(MPI.COMM_WORLD)
if comm.rank == 0:
    print("Total startup time = {} seconds".format(startup))

start = MPI.Wtime()

mt = pt.work.Math ( seed=comm.rank, fftlen=args.fftlen )
data = mt.generate()
mt.ffts( data )

stop = MPI.Wtime()

comm.Barrier()

elapsed = stop - start

if comm.rank == 0:
    print("Work time = {:.4f}s".format(elapsed))

