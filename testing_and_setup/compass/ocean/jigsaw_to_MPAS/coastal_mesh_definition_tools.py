import pyflann
from  netCDF4 import Dataset
import matplotlib.pyplot as plt
from skimage import measure
import math
import numpy as np
from scipy import spatial,io
import os
import timeit
from mpl_toolkits.basemap import Basemap
plt.switch_backend('agg')

km = 1000

def CPP_projection(lon,lat,origin):

  R = 6378206.4
  x = R*(lon-origin[0])*np.cos(origin[1])
  y = R*lat

  return x,y

nn_search = "flann"

# Bounding boxes
Delaware_Bay =  np.array([-75.61903,-74.22, 37.767484, 40.312747])
Galveston_Bay = np.array([-95.45,-94.4, 29, 30])
US_Atlantic_Coast = np.array([-98.186645, -59.832744, 7.791301 ,45.942453])
Delware_Region = np.array([-77, -69.8 ,35.5, 41])
Entire_Globe = np.array([-180,180,-90,90])

######################################################################################
######################################################################################

# Path to bathymetry data and name of file
data_path = "/users/sbrus/climate/bathy_data/SRTM15_plus/"
nc_file = "earth_relief_15s.nc"

# Bounding box of coastal refinement region
region_box = Delaware_Bay
origin = (.5*(region_box[0]+region_box[1]), .5*(region_box[2]+region_box[3]))

# Mesh parameters
grd_box = Entire_Globe 
ddeg = .1
dx_min = 1*km
dx_max = 240*km
grade_width = 10000*km

# Bounding box of plotting region
plot_box = US_Atlantic_Coast 

######################################################################################
######################################################################################

# Open NetCDF file and read cooordintes
nc_fid = Dataset(data_path+nc_file,"r")
lon = nc_fid.variables['lon'][:]
lat = nc_fid.variables['lat'][:]

# Find indicies of coordinates inside bounding box
lon_idx, = np.where((lon > region_box[0]) & (lon < region_box[1]))
lat_idx, = np.where((lat > region_box[2]) & (lat < region_box[3]))

# Get region data inside bounding box
lon_region = lon[lon_idx]
lat_region = lat[lat_idx]
z_region = nc_fid.variables['z'][lat_idx,lon_idx]
print lon_region.shape, lat_region.shape
print z_region.shape

# Get coastlines for ploting
m = Basemap(projection='cyl',llcrnrlat=plot_box[2],urcrnrlat=plot_box[3],\
            llcrnrlon=plot_box[0],urcrnrlon=plot_box[1],resolution='c')

# Plot the bathymetry data
plt.figure()
levels = np.linspace(np.amin(z_region),np.amax(z_region),100)
plt.contourf(lon_region,lat_region,z_region,levels=levels)
plt.colorbar()
plt.axis('equal')
plt.savefig('bathy.png',bbox_inches='tight')

# Find coastline contours, filter out small strings
contours = measure.find_contours(z_region,0)
contours.sort(key=len,reverse=True)
coastlines = []
for c in contours[:10]:
  if c.shape[0] > 20:
    coastlines.append(c)

# Plot coastlines
plt.figure()
for c in coastlines:
  plt.plot(c[:,1],c[:,0])
plt.axis('equal')
plt.savefig('coastlines.png',bbox_inches='tight')

# Combine coastlines and map from pixel to lon,lat
coast = np.concatenate(coastlines)
coast_pts = np.copy(coast)
coast_pts[:,0] = (region_box[1]-region_box[0])/float(len(lon_region))*coast[:,1] + region_box[0]
coast_pts[:,1] = (region_box[3]-region_box[2])/float(len(lat_region))*coast[:,0] + region_box[2]
plt.figure()
plt.plot(coast_pts[:,0],coast_pts[:,1])
plt.savefig('coastlines_latlon.png',bbox_inches='tight')

# Convert to x,y and create kd-tree
coast_pts_xy = np.copy(coast_pts)
coast_pts_xy[:,0],coast_pts_xy[:,1] = CPP_projection(coast_pts[:,0],coast_pts[:,1],origin)
if nn_search == "kdtree":
  tree = spatial.KDTree(coast_pts_xy)
elif nn_search == "flann":
  flann = pyflann.FLANN()
  flann.build_index(coast_pts_xy,algorithm='kdtree',target_precision=.9999)

# Create cell width background grid
lat_grd = np.arange(grd_box[2],grd_box[3],ddeg)
lon_grd = np.arange(grd_box[0],grd_box[1],ddeg)
Lon_grd,Lat_grd = np.meshgrid(lon_grd,lat_grd)
X_grd,Y_grd = CPP_projection(Lon_grd,Lat_grd,origin)
ny,nx = Lon_grd.shape
print ny,nx

# Put backgound grid coordinates in a nx x 2 array for kd-tree query
pts = np.vstack([X_grd.ravel(), Y_grd.ravel()]).T

# Find distances of background grid coordinates to the coast
print "Finding distance"
start = timeit.default_timer()
if nn_search == "kdtree":
  d,idx = tree.query(pts)
elif nn_search == "flann":
  idx,d = flann.nn_index(pts,checks=150)
  d = np.sqrt(d)
end = timeit.default_timer()
print "Done"
print end-start, " seconds"

# Make distance array that corresponds with cell_width array
D = np.reshape(d,(ny,nx))

# Find indicies of coordinates inside bounding box
lon_idx, = np.where((lon_grd > plot_box[0]) & (lon_grd < plot_box[1]))
lat_idx, = np.where((lat_grd > plot_box[2]) & (lat_grd < plot_box[3]))

lon_grd_plot = lon_grd[lon_idx]
lat_grd_plot = lat_grd[lat_idx]
D_plot = D[np.ix_(lat_idx,lon_idx)] # numpy 2d array indexing is pretty dumb
print D_plot.shape,D.shape

# Plot distance to coast
plt.figure()
levels = np.linspace(np.amin(D_plot),np.amax(D_plot),100)
plt.contourf(lon_grd_plot,lat_grd_plot,D_plot,levels=levels)
#plt.plot(Lon_grd,Lat_grd,'k-',lw=0.5,alpha=0.5)
#plt.plot(Lon_grd.T,Lat_grd.T,'k-',lw=0.5,alpha=0.5)
plt.colorbar()
plt.axis('equal')
plt.savefig('distance.png',bbox_inches='tight')

# Assign background grid cell width values
cell_width = dx_max*np.ones(D.shape)

# Compute cell width based on distance
cell_width_dist = dx_max*np.tanh(1.0/(2*grade_width)*D)+dx_min
cell_width = np.minimum(cell_width_dist,cell_width)/km
cell_width_plot = cell_width[np.ix_(lat_idx,lon_idx)]

# Save matfile
io.savemat('cellWidthVsLatLon.mat',mdict={'cellWidth':cell_width,'lon':lon_grd,'lat':lat_grd})

plt.figure()
plt.contourf(lon_grd_plot,lat_grd_plot,cell_width_plot)
m.drawcoastlines()
plt.colorbar()
plt.axis('equal')
plt.savefig('cell_width.png',bbox_inches='tight')

# Show figures and wait to exit
#plt.show()
#plt.show(block=False)
#raw_input(' exit?: ')
#plt.close()


