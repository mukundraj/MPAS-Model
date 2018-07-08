#!/usr/bin/env python
"""
This script performs the first step of initializing the global ocean.  This
includes:
Step 1. Build mesh using JIGSAW
Step 2. Convert triangles from jigsaw format to netcdf
Step 3. Convert from triangles to MPAS mesh
Step 4. Create vtk file for visualization
"""
import os
import subprocess

def removeFile(fileName):
    try:
        os.remove(fileName)
    except OSError:
        pass

print 'Step 1. Build mesh using JIGSAW' 
args = ["octave","--silent","--eval",
        "driver_jigsaw_to_mpas"]
print "running", ' '.join(args)
subprocess.check_call(args, env=os.environ.copy())

print 'Step 2. Convert triangles from jigsaw format to netcdf'
args = ['./triangle_jigsaw_to_netcdf.py',
        '-s',
        '-m', 'mesh-MESH.msh',
        '-o', 'mesh_triangles.nc']
print "running", ' '.join(args)
subprocess.check_call(args, env=os.environ.copy())

print 'Step 3. Convert from triangles to MPAS mesh'
args = ['./MpasMeshConverter.x',
        'mesh_triangles.nc',
        'base_mesh.nc']
print "running", ' '.join(args)
subprocess.check_call(args, env=os.environ.copy())
print 'Injecting bathymetry'
args = ['./inject_bathymetry.py',
        'base_mesh.nc']
print "running", ' '.join(args)
subprocess.check_call(args, env=os.environ.copy())

print 'Step 4. Create vtk file for visualization'
args = ['./paraview_vtk_field_extractor.py',
        '--ignore_time',
				'-d','maxEdges=0',
        '-v', 'allOnCells',
        '-f', 'base_mesh.nc',
        '-o', 'base_mesh_vtk']
print "running", ' '.join(args)
subprocess.check_call(args, env=os.environ.copy())
