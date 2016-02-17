
from __future__ import absolute_import, division, print_function, unicode_literals, with_statement

from mpi4py import MPI

import sys
import os
import numpy as np

import pympit as pt


world = MPI.COMM_WORLD
rank = world.rank
np = world.size

# Split the communicator into 2 groups

ngroups = 2
groupsize = int(np / ngroups)
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

world_reduce = np.zeros_like(local_data)
world.allreduce(sendobj=local_data, recvobj=world_data, op=MPI.SUM)

chksum = np.sum(world_reduce)
if chksum != (nmsg * np):
    print("process {}:  world comm allreduce = {} instead of {}".format(rank, chksum, (nmsg*np)))

group_reduce = np.zeros_like(local_data)
gcomm.allreduce(sendobj=local_data, recvobj=group_reduce, op=MPI.SUM)

chksum = np.sum(group_reduce)
if chksum != (nmsg * groupsize):
    print("process {} of group {}:  group comm allreduce = {} instead of {}".format(grank, group, chksum, (nmsg*groupsize)))

rank_reduce = np.zeros_like(local_data)
rcomm.allreduce(sendobj=group_reduce, recvobj=rank_reduce, op=MPI.SUM)

chksum = np.sum(rank_reduce)
if chksum != (nmsg * np):
    print("process {} of group {}:  rank comm allreduce = {} instead of {}".format(grank, group, chksum, (nmsg*np)))

stop = MPI.Wtime()

comm.Barrier()

elapsed = stop - start

if comm.rank == 0:
    print("Communication time = {:.4f}s".format(elapsed))

