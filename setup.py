#!/usr/bin/env python

import glob
import os
import sys
import re
import subprocess
import shutil

from setuptools import find_packages, setup, Extension
#from Cython.Build import cythonize

from setuptools.command.install import install


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


class FreezeInstall(install):
    def run(self):
        install.run(self)
        # see if we have pyinstaller available
        print("DEBUG:  {}".format(self.prefix))
        for dir in os.getenv("PATH").split(':'):                                           
            if (os.path.exists(os.path.join(dir, "pyinstaller"))):
                proc = subprocess.Popen(["pyinstaller", "pympit.spec"])
                proc.wait()
                shutil.copy2(os.path.join("dist", "run_pympit"), os.path.join(self.prefix, "bin", "run_pympit"))




# extensions to build
#extensions = cythonize([])
extensions = []

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
    requires = ['Python (>2.7.0)', ],
    cmdclass = {'install': FreezeInstall}
)


# extra cleanup of cython generated sources

if "clean" in sys.argv:
    # Just in case the build directory was created by accident,
    # note that shell=True should be OK here because the command is constant.
    subprocess.Popen("rm -rf build", shell=True, executable="/bin/bash")
    subprocess.Popen("rm -rf dist", shell=True, executable="/bin/bash")
    subprocess.Popen("rm -rf pympit/*.c", shell=True, executable="/bin/bash")
    subprocess.Popen("rm -rf pympit/*.so", shell=True, executable="/bin/bash")
    subprocess.Popen("rm -rf pympit/*.pyc", shell=True, executable="/bin/bash")

