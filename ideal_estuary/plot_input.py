import os
import numpy as np
from netCDF4 import Dataset, num2date
from PyFVCOM.read import MFileReader
import matplotlib.pylab as plt

# simple grid
dir_path = os.path.dirname(os.path.realpath(__file__))
estuary_path = os.path.join('model',
                            'estuary')
figure_path = os.path.join(estuary_path,
                           "figures")
fvcom_files = os.path.join(estuary_path,
                           'output',
                           'estuary_avg_0001.nc')


if not os.path.isdir(figure_path):
    os.makedirs(figure_path)

print("Plotting mesh")
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111)
dims = {'siglay': [0]}
fvcom = MFileReader(fvcom_files, dims=dims)
DATA = fvcom.grid.h
p1 = ax.tripcolor(fvcom.grid.x, fvcom.grid.y,
                  fvcom.grid.triangles, DATA, shading='flat', edgecolors='k')
plt.colorbar(p1)
ax.set_aspect('equal', 'box')
name = os.path.join(figure_path, 'bathymetry')
fig.savefig(name, bbox_inches='tight', pad_inches=0.2, dpi=300)
plt.close()

print("Plotting wind forcing")
# check forcing
idtime = 100
fvcom_files = os.path.join(estuary_path,
                           'input',
                           '2D_forcing_50_years_20180927_new_grd.nc')
fvcom_frc = MFileReader(fvcom_files, variables=['uwind_speed',
                                                'vwind_speed',
                                                'short_wave',
                                                'net_heat_flux'])
uwind = np.squeeze(fvcom_frc.data.uwind_speed[idtime, :])
vwind = np.squeeze(fvcom_frc.data.vwind_speed[idtime, :])

# wind speed
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111)
scale = 75
p1 = ax.quiver(fvcom.grid.xc[0:-1:2],
               fvcom.grid.yc[0:-1:2],
               uwind[0:-1:2],
               vwind[0:-1:2],
               scale=scale,
               headlength=8,
               headaxislength=8,
               width=0.0015)

arrow_legend = 2
plt.text(5e4, 6e4, '{} m/s'.format(str(arrow_legend)), fontsize=10)
q = ax.quiver(5e4, 5e4, arrow_legend, 0, scale=scale,
              headlength=8, headaxislength=8, width=0.0015)
ax.set_aspect('equal', 'box')
name = os.path.join(figure_path, 'wind_forcing')
fig.savefig(name, bbox_inches='tight', pad_inches=0.2, dpi=300)
plt.close()

print("Plotting short wave")
# short wave
fvcom = fvcom_frc
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111)
idnode = 500
shortwave = getattr(fvcom_frc.data, 'short_wave')
ax.plot(fvcom.time.datetime[0:8*365*1], shortwave[0:8*365*1, idnode])
ax.set_xlabel('Time (DD-MM HH)', fontsize='x-large')
ax.set_ylabel('W/m2')
name = os.path.join(figure_path, 'short_wave')
fig.savefig(name, bbox_inches='tight', pad_inches=0.2, dpi=300)
plt.close()


print("Plotting net heat flux")
# net heat flux
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111)
idnode = 500
netheat = getattr(fvcom_frc.data, 'net_heat_flux')
ax.plot(fvcom.time.datetime, netheat[:, idnode])
ax.set_xlabel('Time (year)', fontsize='x-large')
ax.set_ylabel('W/m2')
name = os.path.join(figure_path, 'net_heat_flux')
fig.savefig(name, bbox_inches='tight', pad_inches=0.2, dpi=300)
plt.close()

print("Plotting OBC ts")
# OBC T S
obc_node = 40
fvcom_files = os.path.join(estuary_path,
                           'output',
                           'estuary_avg_0001.nc')
fvcom = MFileReader(fvcom_files, dims={'time': range(1)})
fvcom_files_obc = os.path.join(estuary_path,
                               'input',
                               '2D_obc_ts_forcing.nc')
nc = Dataset(fvcom_files_obc).variables
fig = plt.figure(figsize=(10, 5))

ax = fig.add_subplot(121)
month = np.arange(1, 5)
for month in month:
    obc_temp = nc['obc_temp'][month+12*0, :, obc_node]
    depth = fvcom.grid.siglay_z[:, obc_node]
    if month in np.arange(1, 7):
        ax.plot(obc_temp, -depth, label=month)
    else:
        ax.plot(obc_temp, -depth, '--', label=month)
    ax.legend(loc='upper right')
    ax.set_xlim(4.5, 33)
    ax.set_xlabel('Temp (degC)')
    ax.set_ylabel('Depth (m)')
    ax.set_title('obc node {}'.format(str(obc_node)))

ax = fig.add_subplot(122)
month = np.arange(1, 5)
for month in month:
    obc_salt = nc['obc_salinity'][month+12*0, :, obc_node]
    depth = fvcom.grid.siglay_z[:, obc_node]
    if month in np.arange(1, 7):
        ax.plot(obc_salt, -depth, label=month)
    else:
        ax.plot(obc_salt, -depth, '--', label=month)
    ax.legend(loc='upper right')
    ax.set_xlim(28, 37)
    ax.set_xlabel('Salinity (psu)')
    ax.set_ylabel('Depth (m)')
    ax.set_title('obc node {}'.format(str(obc_node)))
name = os.path.join(figure_path, 'obc_TS_node_{}'.format(str(obc_node)))
fig.savefig(name, bbox_inches='tight', pad_inches=0.2, dpi=300)
plt.close()

print("Plotting river forcing")
# River forcing
tracer_f = "2D_bio_River_50_years_20180821_monthly_river_2_tracers_T1T2.nc"
fvcom_file_river = \
    os.path.join(estuary_path,
                 'input',
                 tracer_f)
nc = Dataset(fvcom_file_river)
nc.variables.keys()
varlist = ['river_flux', 'river_temp', 'river_salt', 'river_sed',
           'N4_n', 'N3_n']
fig = plt.figure(figsize=(12, 8))
time_var = nc['time']
dtime = num2date(time_var[:], time_var.units)
for var, num in zip(varlist, np.arange(1, 3)):
    ax = fig.add_subplot(3, 2, num)
    if var in ('river_flux'):
        river_var = np.sum(nc[var][:, :], 1)
    else:
        river_var = nc[var][:, 0]
    ax.plot(dtime, river_var)
    ax.set_title('{} ({})'.format(nc[var].long_name, nc[var].units))
    ax.set_xlabel('Time (month)')
    plt.tight_layout()
name = os.path.join(figure_path, 'river_flux1')
fig.savefig(name, bbox_inches='tight', pad_inches=0.2, dpi=300)
plt.close()

varlist = ['N1_p', 'N5_s', 'O3_c', 'O3_TA', 'O3_bioalk', 'O2_o']
fig = plt.figure(figsize=(12, 8))
for var, num in zip(varlist, np.arange(1, 3)):
    ax = fig.add_subplot(3, 2, num)
    river_var = nc[var][:, 0]
    ax.plot(dtime, river_var)
    ax.set_title('{} ({})'.format(nc[var].long_name, nc[var].units))
    ax.set_xlabel('Time (month)')
    plt.tight_layout()
name = os.path.join(figure_path, 'river_flux2')
fig.savefig(name, bbox_inches='tight', pad_inches=0.2, dpi=300)
plt.close()
