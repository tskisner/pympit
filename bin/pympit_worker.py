#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals, with_statement

import sys
import os
import numpy as np
import scipy as sc

import socket


from astropy.io import fits

import argparse

parser = argparse.ArgumentParser(description='Small serial code to run in a subprocess')
args = parser.parse_args()

thishost = socket.gethostname()

print("running on {}".format(thishost))

