#!/usr/bin/env python
# Simple script to inject bathymetry onto a mesh
# Phillip Wolfram, 01/19/2018

import matplotlib.pyplot as plt
from open_msh import readmsh
import numpy as np
from scipy import interpolate
import netCDF4 as nc4
import pprint

dtor = np.pi/180.0
rtod = 180.0/np.pi

if __name__ == "__main__":
    import sys


    # Path to bathymetry data and name of file
    data_path = "/users/sbrus/climate/bathy_data/SRTM15_plus/"
    nc_file = "earth_relief_15s.nc"

    # Open NetCDF data file and read cooordintes
    nc_fid = nc4.Dataset(data_path+nc_file,"r")
    lon_data = nc_fid.variables['lon'][:]*dtor
    lat_data = nc_fid.variables['lat'][:]*dtor
    
    # Setup interpolation boxes
    n = 100  
    xbox = np.linspace(-180,180,n)*dtor
    ybox = np.linspace(-90,90,n)*dtor
    dx = xbox[1]-xbox[0]
    dy = ybox[1]-ybox[0]
    boxes = []
    for i in range(n-1):
      for j in range(n-1):
        boxes.append(np.asarray([xbox[i],xbox[i+1],ybox[j],ybox[j+1]]))

    # Get mesh points
    ds = nc4.Dataset(sys.argv[1],'r+')
    lon_mesh = np.mod(ds.variables['lonCell'][:] + np.pi, 2*np.pi)-np.pi
    lat_mesh = ds.variables['latCell'][:]
    mesh_pts = np.vstack((lon_mesh,lat_mesh)).T

    # Initialize bathymetry
    bathymetry = np.zeros(np.shape(lon_mesh))
    bathymetry.fill(np.nan)

    
    for i,box in enumerate(boxes):
      print i,"/",len(boxes)

      # Get data inside box
      overlap = 0.1 
      lon_idx, = np.where((lon_data > box[0]-overlap*dx) & (lon_data < box[1]+overlap*dx))
      lat_idx, = np.where((lat_data > box[2]-overlap*dy) & (lat_data < box[3]+overlap*dy))
      xdata = lon_data[lon_idx]
      ydata = lat_data[lat_idx]
      zdata = nc_fid.variables['z'][lat_idx,lon_idx]

      ## Get mesh points inside box
      #lon_idx, = np.where((lon_mesh > box[0]) & (lon_mesh < box[1]))
      #lat_idx, = np.where((lat_mesh > box[2]) & (lat_mesh < box[3]))
      #idx = np.intersect1d(lon_idx,lat_idx)
      #xmesh = lon_data[idx]
      #ymesh = lat_data[idx]
      #mesh_pts = np.vstack((xmesh,ymesh)).T

      bathy = interpolate.RegularGridInterpolator((xdata,ydata),zdata.T,bounds_error=False,fill_value=np.nan)
      bathy_int = bathy(mesh_pts)
      idx = np.where(np.isfinite(bathy_int))
      bathymetry[idx] = bathy_int[idx] 
      #bathymetry[idx] = bathy_int

    #ds.createVariable('bathymetry','f8',('nCells'))
    #ds.createVariable('cullCell','i',('nCells'))
    ds.variables['bathymetry'][:] = bathymetry 
    ds.variables['cullCell'][:] = ds.variables['bathymetry'][:] > 20.0

    ds.close()


