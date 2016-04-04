#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals, with_statement

from mpi4py import MPI

import sys
import os
import numpy as np
import scipy as sc


from astropy.io import fits

import argparse

import pympit as pt



parser = argparse.ArgumentParser( description='Run an MPI test in python' )
parser.add_argument( '--fftlen', required=False, default=5242880, help='FFT length for math test' )
args = parser.parse_args()

comm = MPI.COMM_WORLD

start = MPI.Wtime()

mt = pt.work.Math ( seed=comm.rank, fftlen=args.fftlen )
data = mt.generate()
mt.ffts( data )

stop = MPI.Wtime()

comm.Barrier()

elapsed = stop - start

if comm.rank == 0:
    print("Work time = {:.4f}s".format(elapsed))

