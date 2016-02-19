#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals, with_statement

from mpi4py import MPI

import sys
import os
import numpy as np

import pympit as pt


world = MPI.COMM_WORLD
rank = world.rank
procs = world.size

# Split the communicator into 2 groups

ngroups = 2
groupsize = int(procs / ngroups)
if groupsize == 0:
    groupsize = 1
group = int(rank / groupsize)
grank = rank % groupsize

if group >= ngroups:
    group = MPI.UNDEFINED
    grank = MPI.UNDEFINED

gcomm = world.Split(group, grank)
rcomm = world.Split(grank, group)

# make a fake message

nmsg = 100000
local_data = np.ones(nmsg, dtype=np.int64)

# do some operations.  use the lower-case functions as a worst case.

start = MPI.Wtime()

world_reduce = world.allreduce(local_data, op=MPI.SUM)

chksum = np.sum(world_reduce)
if chksum != (nmsg * procs):
    print("process {}:  world comm allreduce = {} instead of {}".format(rank, chksum, (nmsg*procs)))

group_reduce = gcomm.allreduce(local_data, op=MPI.SUM)

chksum = np.sum(group_reduce)
if chksum != (nmsg * groupsize):
    print("process {} of group {}:  group comm allreduce = {} instead of {}".format(grank, group, chksum, (nmsg*groupsize)))

rank_reduce = rcomm.allreduce(group_reduce, op=MPI.SUM)

chksum = np.sum(rank_reduce)
if chksum != (nmsg * procs):
    print("process {} of group {}:  rank comm allreduce = {} instead of {}".format(grank, group, chksum, (nmsg*procs)))

stop = MPI.Wtime()

world.Barrier()

elapsed = stop - start

if rank == 0:
    print("Communication time = {:.4f}s".format(elapsed))

