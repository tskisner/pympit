#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals, with_statement

from mpi4py import MPI

import sys
import os
import numpy as np

import multiprocessing


#- Default number of processes to use for multiprocessing
if 'SLURM_CPUS_PER_TASK' in os.environ.keys():
    mproc = int(os.environ['SLURM_CPUS_PER_TASK'])
else:
    mproc = max(1, multiprocessing.cpu_count() // 2)


def compute(seed) :
    std = None
    nsamp = 100
    try :
        np.random.seed(seed)
        data = np.random.random(size=nsamp)
        std = np.std(data)
    except :
        std = 0
    return std


def _func(arg) :
    return compute(**arg)


comm = MPI.COMM_WORLD
rank = comm.rank
nproc = comm.size

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

job_seeds = list(range(rank*100, (rank+1)*100, 1))

pool = multiprocessing.Pool(mproc)
local_std = pool.map(_func, job_seeds)
pool.close()
pool.join()

comm_group.barrier()
comm_rank.barrier()
comm.barrier()

std = comm.gather(local_std, root=0)
if rank == 0:
    np.savetxt('pympit_mp_out.txt', std)

stop = MPI.Wtime()
elapsed = stop - start

comm.barrier()

for p in range(comm.size):
    if p == comm.rank:
        print("proc {:02d} {:.3f}s:".format(p, elapsed))
        for line in local_out:
            print("  {}".format(line.rstrip()))
    comm.barrier()


