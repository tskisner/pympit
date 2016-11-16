#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals, with_statement

from mpi4py import MPI

import sys
import os
import numpy as np
import scipy as sc

import argparse

import subprocess as sp

import pympit as pt


parser = argparse.ArgumentParser(description='Run an MPI test in python with subprocess forking')
args = parser.parse_args()

comm = MPI.COMM_WORLD
rank = comm.rank
nproc = comm.size

startup = pt.work.since_start(MPI.COMM_WORLD)
if comm.rank == 0:
    print("Startup time = {} seconds".format(startup))

ngroup = int(nproc / 4)
group = int(rank / ngroup)
group_rank = rank % ngroup
            
comm_group = comm.Split(color=group, key=group_rank)
comm_rank = comm.Split(color=group_rank, key=group)

start = MPI.Wtime()

if group_rank == 0:
    print("Group {} of {} has {} processes".format(group+1, ngroup, comm_group.size))

comm_group.barrier()
comm_rank.barrier()
comm.barrier()

local_out = []

proc = sp.Popen(['pympit_worker.py'], stdout=sp.PIPE, stderr=sp.PIPE)
outs, errs = proc.communicate()
proc.wait()

local_out.append(outs)

stop = MPI.Wtime()
elapsed = stop - start

comm.barrier()

for p in range(comm.size):
    if p == comm.rank:
        print("proc {:02d} {:.3f}s:".format(p, elapsed))
        for line in local_out:
            print("  {}".format(line.rstrip()))
    comm.barrier()


