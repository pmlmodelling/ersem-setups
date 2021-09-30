import os
import glob
import numpy as np

from PyFVCOM.read import MFileReader
from pythontools.visual.utils import colourmap
import PyFVCOM as pf
from PyFVCOM.plot import Plotter, Depth
import matplotlib.pyplot as plt
import matplotlib

project0 = 'estuary'
casename = 'ideal'
base = os.path.join('model', 'estuary')
experiment = ''
suffix = ''
level_label = 'vertical_transect'
level_label2 = 'surface'
fname = 'estuary_avg_0001.nc'
fpath1 = os.path.join(base, 'output', fname)
fvcom_files = sorted(glob.glob(fpath1))

noisy = True
if noisy:
    print(fpath1, flush=True)
    print(fvcom_files, flush=True)

if not fvcom_files:
    raise Exception('Cannot find FVCOM output: {}'.format(fpath1))

MyFile = fvcom_files

plot_map = True  # to plot horizontal map
save_plot = True  # to save the plot

fvcom = MFileReader(MyFile)

varlist = ['total_food', 'GPP', 'temp', 'salinity',
           'P1_Chl', 'O3_c', 'R6_c', 'N1_p', 'N3_n',
           'tracer1_c', 'total_chl']

clims = {
    'temp': [5, 25],
    'O3_c': [1900, 2300],
    'R6_c': [0, 200],
    'salinity': [0, 31]
}

# plot all time series, maybe too much
time_indices = range(0, fvcom.dims.time)
level = 0  # select vertical layer (0: surface, -1: bottom) if plot_map = True

plt.rcParams['axes.facecolor'] = '0.6'
for var in varlist:
    baseDir = os.path.join(base, 'figures', var)
    baseName = os.path.join(baseDir, var)

    if var in ('uv'):
        plotvars = ['u', 'v']
    elif var == 'total_chl':
        plotvars = ['P1_Chl', 'P2_Chl', 'P3_Chl', 'P4_Chl']
    elif var == 'netPP':
        plotvars = ['P1_Chl', 'P2_Chl', 'P3_Chl', 'P4_Chl']
    elif var == 'total_food':
        plotvars = ["P1_c", "P2_c", "P3_c",
                    "P4_c", "Z5_c", "Z5_c",
                    "R8_c", "R6_c", "R4_c"]
    elif var == 'GPP':
        plotvars = ["P1_fO3PIc", "P2_fO3PIc", "P3_fO3PIc", "P4_fO3PIc"]
    else:
        plotvars = [var]

    if noisy:
        print('Loading {} data from netCDF... '.format(var),
              end='',
              flush=True)
        if save_plot:
            print('Saving files to {}'.format(baseDir), flush=True)
            if not os.path.isdir(baseDir):
                os.makedirs(baseDir)
        print('Working on {}...'.format(var), flush=True),

    fvcom = MFileReader(MyFile, variables=plotvars)
    fvcom.grid.lon = fvcom.grid.x
    fvcom.grid.lat = fvcom.grid.y
    positions = np.array(((0, 2e5), (4e5, 2e5)))
    indices, distance = fvcom.horizontal_transect_nodes(positions)
    cmap = colourmap(var)

    if var in ('total_chl'):
        setattr(
            fvcom.data, var, fvcom.data.P1_Chl + fvcom.data.P2_Chl +
            fvcom.data.P3_Chl + fvcom.data.P4_Chl)
        attributes = type('attributes', (object, ), {})()
        setattr(attributes, 'long_name', 'Total chlorophyll')
        setattr(attributes, 'units', fvcom.atts.P1_Chl.units)
        setattr(fvcom.atts, var, attributes)
    elif var in ('total_food'):
        setattr(fvcom.data, var, fvcom.data.P1_c + fvcom.data.P2_c
                + fvcom.data.P3_c + fvcom.data.P4_c + fvcom.data.Z5_c
                + fvcom.data.Z5_c + fvcom.data.R8_c + fvcom.data.R6_c
                + fvcom.data.R4_c)
        attributes = pf.utilities.general.PassiveStore()
        setattr(attributes, 'long_name', 'Total mussel food ')
        setattr(attributes, 'units', fvcom.atts.P1_c.units)
        setattr(fvcom.atts, var, attributes)
        attributes = pf.utilities.general.PassiveStore()
        setattr(fvcom.data, var, getattr(fvcom.data, var) / 1000000)
        setattr(attributes, 'long_name', 'Integrated Total mussel food')
        setattr(attributes, 'units', 'Kg\C')
        setattr(fvcom.atts, var, attributes)
    elif var in ('GPP'):
        setattr(fvcom.data, var, fvcom.data.P1_fO3PIc +
                fvcom.data.P2_fO3PIc + fvcom.data.P3_fO3PIc +
                fvcom.data.P4_fO3PIc)
        attributes = pf.utilities.general.PassiveStore()
        setattr(attributes, 'long_name', 'Gross Primary Productivity')
        setattr(attributes, 'units', fvcom.atts.P1_fO3PIc.units)
        setattr(fvcom.atts, var, attributes)

    if var in clims:
        clim = clims[var]
    else:
        clim = [
            np.nanpercentile(getattr(fvcom.data, var), 3),
            np.nanpercentile(getattr(fvcom.data, var), 97)
        ]
    plot = Plotter(fvcom,
                   figsize=(20, 20),
                   res='i',
                   cb_label='{} ({})'.format(
                       getattr(fvcom.atts, var).long_name,
                       getattr(fvcom.atts, var).units),
                   cmap=cmap,
                   vmin=clim[0],
                   vmax=clim[1],
                   cartesian=True)



    # Plot a temperature transect between two locations.
    depth_plot = Depth(fvcom,
                       figsize=(20, 9),
                       cb_label='{} ({})'.format(
                            getattr(fvcom.atts, var).long_name,
                            getattr(fvcom.atts, var).units),
                       cmap=cmap)
    depth_plot.axes.set_xlabel('Distance (km)')
    depth_plot.axes.set_ylabel('Depth (m)')
    for ntime in time_indices:
        print("Time step index: {}".format(ntime))

        # Make a plot of the surface temperature.
        plot.plot_field(np.squeeze(getattr(fvcom.data, var))[ntime, level, :])
        plot.axes.set_title(
            fvcom.time.datetime[ntime].strftime('%Y-%m-%d %H:%M:%S'))

        if save_plot:
            plot.figure.savefig('{}{}_{}_{}_{:04d}.png'.format(
                baseName, suffix, experiment, level_label2, ntime),
                bbox_inches='tight',
                pad_inches=0.2,
                dpi=120)

        # fill_seabed makes the part of the plot below the seabed grey.
        # plot.plot_slice(distance / 1000,  # to kilometres from metres
        depth_plot.plot_slice(
            fvcom.grid.lon[indices] / 1000,  # to kilometres from metres
            fvcom.grid.siglay_z[:, indices],
            getattr(fvcom.data, var)[ntime, :, indices],
            fill_seabed=True,
            vmin=clim[0],
            vmax=clim[1])
        depth_plot.axes.set_title(
            fvcom.time.datetime[ntime].strftime('%Y-%m-%d %H:%M:%S'))
        depth_plot.axes.set_xlim(
            right=(fvcom.grid.lon[indices] /
                   1000).max())  # set the x-axis to the data range

        if save_plot:
            depth_plot.figure.savefig('{}{}_{}_{}_{:04d}.png'.format(
                baseName, suffix, experiment, level_label, ntime),
                bbox_inches='tight',
                pad_inches=0.2,
                dpi=120)
