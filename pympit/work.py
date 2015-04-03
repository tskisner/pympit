
from mpi4py import MPI

import unittest

import numpy as np
import scipy as sc

#import work_helper



class Math ( object ):
    '''
    Do some FFTs of random data
    '''


    def __init__ ( self, seed=0, rms=100.0, fftlen=1048576 ):
        '''
        seed = random number seed (default 0)
        rms = scaling (default 100.00)
        fftlen = length of the FFT (default 1048576)
        ''' 
        self.seed = seed
        self.fftlen = fftlen
        self.rms = rms


    def generate ( self ):
        np.random.seed( self.seed )
        data = np.random.normal ( loc=0.0, scale=self.rms, size=(self.fftlen,) )
        return data


    def ffts ( self, data ):
        fdata = np.fft.rfft ( data, axis=0 )
        check = np.fft.irfft ( fdata )
        return



class WorkTest ( unittest.TestCase ):


    def setUp ( self ):
        # setup tasks here
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.rank


    def test_math ( self ):
        start = MPI.Wtime()
        mt = Math( seed=self.rank )
        data = mt.generate()
        mt.ffts( data )
        stop = MPI.Wtime()
        elapsed = stop - start
        print 'Proc {}:  test took {:.4f} s'.format( self.rank, elapsed )


if __name__ == "__main__":
    unittest.main()

