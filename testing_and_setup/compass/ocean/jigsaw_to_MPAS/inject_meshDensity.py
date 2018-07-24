#!/usr/bin/env python
# Simple script to inject mesh density onto a mesh
# Mark Petersen, 7/24/2018

import matplotlib.pyplot as plt
from open_msh import readmsh
import numpy as np
from scipy import interpolate
import netCDF4 as nc4
import scipy.io as sio
dtor = np.pi/180.0
rtod = 180.0/np.pi

if __name__ == "__main__":
    import sys

    matData = sio.loadmat('cellWidthVsLatLon.mat')
    cellWidth = matData['cellWidth']
    LonPos = matData['lon'].T*dtor
    LatPos = matData['lat'].T*dtor
    minCellWidth = cellWidth.min()
    meshDensityVsLatLon = ( minCellWidth / cellWidth )**4
    print 'minimum cell width in grid definition:', minCellWidth
    print 'maximum cell width in grid definition:', cellWidth.max()
    print 'cellWidth',cellWidth
    print 'meshDensityVsLatLon',meshDensityVsLatLon

    LON, LAT = np.meshgrid(LonPos, LatPos)

    ds = nc4.Dataset(sys.argv[1],'r+')
    meshDensity = ds.variables["meshDensity"][:]

    print "Preparing interpolation of meshDensity from lat/lon to mesh..."
    meshDensityInterp = interpolate.LinearNDInterpolator(np.vstack((LAT.ravel(), LON.ravel())).T, meshDensityVsLatLon.ravel())

    print "Interpolating and writing meshDensity..."
    ds.variables['meshDensity'][:] = meshDensityInterp(np.vstack((ds.variables['latCell'][:], np.mod(ds.variables['lonCell'][:] + np.pi, 2*np.pi)-np.pi)).T)

    ds.close()
