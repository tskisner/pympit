
from mpi4py import MPI

import numpy as np
import scipy as sc

from astropy.io import fits

import argparse

import pympit


parser = argparse.ArgumentParser( description='Run an MPI test in python' )
parser.add_argument( '--fftlen', required=False, default=1048576, help='FFT length for math test' )
args = parser.parse_args()

comm = MPI.COMM_WORLD

start = MPI.Wtime()
mt = pympit.work.Math ( seed=comm.rank )
stop = MPI.Wtime()

comm.Barrier()

elapsed = stop - start

for p in range ( comm.size ):
    if p == comm.rank:
        print ( 'Proc {}:  took {:.4f} s'.format( comm.rank, elapsed ), file=sys.stderr )
    comm.Barrier()



