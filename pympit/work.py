
from __future__ import absolute_import, division, print_function, unicode_literals, with_statement

from mpi4py import MPI

import unittest
import datetime

import os

import numpy as np
import scipy as sc
import astropy.io.fits as af


def since_start(comm):
    comm.barrier()
    elapsed = 0
    if comm.rank == 0:
        tnow = datetime.datetime.now()
        if "STARTTIME" in os.environ:
            try:
                tstart = datetime.datetime.strptime(os.getenv("STARTTIME"), "%Y%m%d-%H:%M:%S")
                dt = tnow - tstart
                elapsed = dt.seconds
            except ValueError:
                print("unable to parse $STARTTIME={}".format(os.getenv("STARTTIME")))
        else:
            print("elapsed time unknown since $STARTTIME not set")
    elapsed = comm.bcast(elapsed, root=0)
    return elapsed


class Math(object):
    '''
    Do some FFTs of random data
    '''
    def __init__(self, seed=0, rms=100.0, fftlen=1048576):
        '''
        seed = random number seed (default 0)
        rms = scaling (default 100.00)
        fftlen = length of the FFT (default 1048576)
        ''' 
        self.seed = seed
        self.fftlen = fftlen
        self.rms = rms


    def generate(self):
        np.random.seed(self.seed)
        data = np.random.normal(loc=0.0, scale=self.rms, size=(self.fftlen,))
        return data


    def ffts(self, data):
        fdata = np.fft.rfft(data, axis=0)
        check = np.fft.irfft(fdata)
        return


class IOWork(object):
    '''
    Create files and perform read / write operations
    '''
    def __init__(self, comm, dir='.', procs_per_file=1, datasize=100000000):
        self.comm = comm
        self.dir = dir
        self.ppfile = procs_per_file
        self.prefix = "data_"

        self.nfile = int(comm.size / self.ppfile)
        self.myfile = int(comm.rank / self.ppfile)
        self.filerank = comm.rank % self.ppfile

        self.filesize = int(datasize / self.nfile)
        self.filecount = int(self.filesize / 8)
        self.filesize = self.filecount * 8

        self.datasize = self.filesize * self.nfile
        self.filechunk = int(self.filesize / self.ppfile)


    def create_data(self):
        if self.comm.rank == 0:
            for i in range(self.nfile):
                path = os.path.join(self.dir, "{}{:04d}".format(self.prefix, i))
                with open(path, "wb") as f:
                    np.zeros(self.filecount, dtype=np.float64).tofile(f)
        self.comm.barrier()
        return


    def write(self):
        mypath = os.path.join(self.dir, "{}{:04d}".format(self.prefix, self.myfile))
        offset = self.filerank * self.filechunk

        handle = open(mypath, 'wb')
        handle.seek(8 * offset, os.SEEK_SET)

        data = np.random.random(size=self.filechunk)
        data.tofile(handle)

        handle.close()

        self.comm.barrier()
        return


    def read(self):
        mypath = os.path.join(self.dir, "{}{:04d}".format(self.prefix, self.myfile))
        offset = self.filerank * self.filechunk

        handle = open(mypath, 'rb')
        handle.seek(8 * offset, os.SEEK_SET)

        data = np.fromfile(handle, dtype=np.float64, count=self.filechunk)

        handle.close()

        self.comm.barrier()
        return



class WorkTest(unittest.TestCase):


    def setUp(self):
        # setup tasks here
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.rank


    def test_math(self):
        start = MPI.Wtime()
        mt = Math( seed=self.rank )
        data = mt.generate()
        mt.ffts( data )
        stop = MPI.Wtime()
        elapsed = stop - start
        print('Proc {}:  math test took {:.4f} s'.format(self.rank, elapsed))


    def test_io(self):
        io = IOWork(self.comm)
        start = MPI.Wtime()
        io.create_data()
        stop = MPI.Wtime()
        elapsed = stop - start
        print('Proc {}:  create data took {:.4f} s'.format(self.rank, elapsed))
        start = MPI.Wtime()
        io.write()
        stop = MPI.Wtime()
        elapsed = stop - start
        print('Proc {}:  write data took {:.4f} s'.format(self.rank, elapsed))
        start = MPI.Wtime()
        io.read()
        stop = MPI.Wtime()
        elapsed = stop - start
        print('Proc {}:  read data took {:.4f} s'.format(self.rank, elapsed))


if __name__ == "__main__":
    unittest.main()

