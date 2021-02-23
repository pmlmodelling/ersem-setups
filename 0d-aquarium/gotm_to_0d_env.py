#!/usr/bin/env python

"""
gotm_to_0d_env.py: Extracts and converts environmental forcing from a GOTM
simulation formatted for the 0d FABM driver

Adapted from
https://github.com/fabm-model/fabm/blob/master/testcases/0d/gotm_to_0d_env.py
"""

import numpy as np
from netCDF4 import Dataset
from netCDF4 import num2date

import argparse


parser = argparse.ArgumentParser(description='Extract environmental forcing for the 0d FABM driver from a GOTM simulation.')
parser.add_argument("filename",help="GOTM NetCDF file name")
parser.add_argument('--lvl', dest='lvl', default=0, type=int,
                   help='vertical level to extract - default surface')
parser.add_argument('--output', help="Output filename",
                    default="env_annual.dat")

args = parser.parse_args()
fn  = args.filename
lvl = args.lvl
data_file = args.output

data = Dataset(fn)
time = data.variables['time']
swr  = data.variables['light_parEIR']
temp = data.variables['temp']
salt = data.variables['salt']
lvl = temp.shape[1] - lvl

valid_times = num2date(time[:], time.units)
with open(data_file, "w") as f:
    for i, t in enumerate(valid_times):
        input_str = t.strftime('%Y-%m-%d %H:00:00') + \
                "{:8.1f} {:8.2f} {:8.2f}\n".format(
                        np.average(swr[i, lvl:, 0, 0]),
                        np.average(temp[i, lvl:, 0, 0]),
                        np.average(salt[i, lvl:, 0 ,0]))
        f.write(input_str)
