#!/usr/bin/env python

import glob
import os
import sys
import re
import subprocess

from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy as np


def get_version():
    ver = 'unknown'
    if os.path.isfile("pympit/_version.py"):
        f = open("pympit/_version.py", "r")
        for line in f.readlines():
            mo = re.match("__version__ = '(.*)'", line)
            if mo:
                ver = mo.group(1)
        f.close()
    return ver

current_version = get_version()



# extensions to build

extshdet = Extension ( 'py.shdet',
    extra_compile_args = [ '-std=c11', '-fno-stack-protector-strong' ],
    include_dirs = [ np.get_include(), 'shdet/include' ],
    sources = [ 
        'shdet/src/cooler_4k_pwr_vct_f.c',
        'shdet/src/dsn_sgnl_f.c',
        'shdet/src/get_prm_lst_f.c',
        'shdet/src/input_arrays_f.c',
        'shdet/src/input_parameters_f.c',
        'shdet/src/input_variables_f.c',
        'shdet/src/mdl_pwr_vct_f.c',
        'shdet/src/opt_pwr_spr_fst_vct_f.c',
        'shdet/src/opt_pwr_vct_f.c',
        'shdet/src/read_ascii_shdet_f.c',
        'shdet/src/rplc_prmtr_f.c',
        'shdet/src/shdet_f.c',
        'shdet/src/shdet_smltn_f.c',
        'shdet/src/t_0_vct_f.c',
        'shdet/src/time_eval.c',
        'shdet/src/trimwhitespace.c',
    ]
)

extensions = cythonize ( [ extshdet ] )


setup (
    name = 'pympit',
    provides = 'pympit',
    version = current_version,
    description = 'Python MPI Tests',
    author = 'Theodore Kisner',
    author_email = 'mail@theodorekisner.com',
    url = 'https://github.com/tskisner/pympit',
    ext_modules = extensions,
    packages = [ 'pympit' ],
    scripts = [ 'bin/run_pympit.py' ],
    license = 'None',
    requires = ['Python (>2.7.0)', ]
)


# extra cleanup of cython generated sources

if "clean" in sys.argv:
    print "Deleting cython files..."
    # Just in case the build directory was created by accident,
    # note that shell=True should be OK here because the command is constant.
    subprocess.Popen("rm -rf build", shell=True, executable="/bin/bash")
    subprocess.Popen("rm -rf pympit/*.c", shell=True, executable="/bin/bash")
    subprocess.Popen("rm -rf pympit/*.so", shell=True, executable="/bin/bash")
    subprocess.Popen("rm -rf pympit/*.pyc", shell=True, executable="/bin/bash")

