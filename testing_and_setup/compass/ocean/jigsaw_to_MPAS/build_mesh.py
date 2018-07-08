#!/usr/bin/env python
"""
This script performs the first step of initializing the global ocean.  This
includes:
Step 1. Build mesh using JIGSAW
Step 2. Convert triangles from jigsaw format to netcdf
Step 3. Convert from triangles to MPAS mesh
Step 4. (Optional) Create vtk file for visualization
Step 5. (Optional) Cull land cells using topo.msh.  This is a quick cull, not the method for a production mesh.
Step 6. (Optional) Create vtk file for visualization
"""
import os
import os.path
import subprocess
from optparse import OptionParser

def removeFile(fileName):
    try:
        os.remove(fileName)
    except OSError:
        pass

#parser = OptionParser()
#parser.add_option("--with_cavities", action="store_true", dest="with_cavities")
#parser.add_option("--with_critical_passages", action="store_true",
#                  dest="with_critical_passages")
#parser.add_option("-p", "--geom_feat_path", type="string", dest="path",
#                  default="geometric_features",
#                  help="Path to the geometric_features repository.")
#options, args = parser.parse_args()
#
#path = options.path
#
#landCoverage = '{}/natural_earth/region/Land_Coverage/' \
#    'region.geojson'.format(path)
#
#landCoverageMask = '{}/ocean/region/Global_Ocean_90S_to_60S/' \
#    'region.geojson'.format(path)
#
#removeFile('land_coverage.geojson')
## Mask the land coverage to exclude the region below 60S.
#args = ['{}/difference_features.py'.format(path),
#        '-f', landCoverage,
#        '-m', landCoverageMask,
#        '-o', 'land_coverage.geojson']
#print "running", ' '.join(args)
#subprocess.check_call(args, env=os.environ.copy())
#
## Add the appropriate land coverage below 60S (either all ice or grounded ice).
#if options.with_cavities:
#    antarcticLandCoverage = '{}/bedmap2/region/AntarcticGroundedIceCoverage/' \
#        'region.geojson'.format(path)
#else:
#    antarcticLandCoverage = '{}/bedmap2/region/AntarcticIceCoverage/' \
#        'region.geojson'.format(path)
#
#args = ['{}/merge_features.py'.format(path), '-f', antarcticLandCoverage,
#        '-o', 'land_coverage.geojson']
#print "running", ' '.join(args)
#subprocess.check_call(args, env=os.environ.copy())
#
## Create the land mask based on the land coverage, i.e. coastline data.
## Run command is:
## ./MpasMaskCreator.x  base_mesh.nc land_mask.nc -f land_coverage.geojson
#args = ['./MpasMaskCreator.x', 'base_mesh.nc', 'land_mask_1_from_land_coverage.nc',
#        '-f', 'land_coverage.geojson']
#print "running", ' '.join(args)
#subprocess.check_call(args, env=os.environ.copy())
#
## Add land-locked cells to land coverage mask.
#args = ['./add_land_locked_cells_to_mask.py',
#        '-f', 'land_mask_1_from_land_coverage.nc',
#        '-o', 'land_mask_final.nc',
#        '-m', 'base_mesh.nc',
#        '-l', '43.0',
#        '-n', '20']
#print "running", ' '.join(args)
#subprocess.check_call(args, env=os.environ.copy())
#
## create seed points for a flood fill of the ocean
## use all points in the ocean directory, on the assumption that they are, in
## fact, in the ocean
#removeFile('seed_points.geojson')
#args = ['{}/merge_features.py'.format(path),
#        '-d', '{}/ocean/point'.format(path),
#        '-t', 'seed_point',
#        '-o', 'seed_points.geojson']
#print "running", ' '.join(args)
#subprocess.check_call(args, env=os.environ.copy())
#
#if options.with_critical_passages:
#    # merge transects for critical passages into critical_passages.geojson
#    removeFile('critical_passages.geojson')
#    args = ['{}/merge_features.py'.format(path),
#            '-d', '{}/ocean/transect'.format(path),
#            '-t', 'Critical_Passage',
#            '-o', 'critical_passages.geojson']
#    print "running", ' '.join(args)
#    subprocess.check_call(args, env=os.environ.copy())
#
#    # create masks from the transects
#    # Run command is:
#    # ./MpasMaskCreator.x  base_mesh.nc critical_passages_mask.nc
#    # -f critical_passages.geojson
#    args = ['./MpasMaskCreator.x', 'base_mesh.nc', 'critical_passages_mask.nc',
#            '-f', 'critical_passages.geojson']
#    print "running", ' '.join(args)
#    subprocess.check_call(args, env=os.environ.copy())
#
#    # Alter critical passages to be at least two cells wide, to avoid sea ice
#    # blockage.
#    args = ['./widen_transect_edge_masks.py',
#            '-f', 'critical_passages_mask.nc',
#            '-m', 'base_mesh.nc',
#            '-l', '43.0']
#    print "running", ' '.join(args)
#    subprocess.check_call(args, env=os.environ.copy())
#
#    # Cull the mesh based on the land mask while keeping critical passages open
#    # Run command is:
#    # ./MpasCellCuller.x  base_mesh.nc culled_mesh.nc -m land_mask_final.nc
#    # -p critical_passages_mask.nc
#    args = ['./MpasCellCuller.x', 'base_mesh.nc', 'culled_mesh.nc',
#            '-m', 'land_mask_final.nc', '-p', 'critical_passages_mask.nc']
#    print "running", ' '.join(args)
#    subprocess.check_call(args, env=os.environ.copy())
#else:
#
#    # cull the mesh based on the land mask
#    # Run command is:
#    # ./MpasCellCuller.x  base_mesh.nc culled_mesh.nc -m land_mask_final.nc
#    args = ['./MpasCellCuller.x', 'base_mesh.nc', 'culled_mesh.nc',
#            '-m', 'land_mask_final.nc']
#    print "running", ' '.join(args)
#    subprocess.check_call(args, env=os.environ.copy())
#
## create a mask for the flood fill seed points
## Run command is:
## ./MpasMaskCreator.x  culled_mesh.nc seed_mask.nc -s seed_points.geojson
#args = ['./MpasMaskCreator.x', 'culled_mesh.nc', 'seed_mask.nc',
#        '-s', 'seed_points.geojson']
#print "running", ' '.join(args)
#subprocess.check_call(args, env=os.environ.copy())
#
#
## cull the mesh a second time using a flood fill from the seed points
## Run command is:
## ./MpasCellCuller.x  culled_mesh.nc culled_mesh_final.nc -i seed_mask.nc
#args = ['./MpasCellCuller.x', 'culled_mesh.nc', 'culled_mesh_final.nc',
#        '-i', 'seed_mask.nc']
#
#print "running", ' '.join(args)
#subprocess.check_call(args, env=os.environ.copy())
#
#if options.with_critical_passages:
#    # make a new version of the critical passages mask on the culled mesh
#    # Run command is:
#    # ./MpasMaskCreator.x  culled_mesh_final.nc critical_passages_mask_final.nc
#    # -f critical_passages.geojson
#    args = ['./MpasMaskCreator.x', 'culled_mesh_final.nc',
#            'critical_passages_mask_final.nc',
#            '-f', 'critical_passages.geojson']
#    print "running", ' '.join(args)
#    subprocess.check_call(args, env=os.environ.copy())
##!/usr/bin/env bash
## Directs process to build MPAS mesh using JIGSAW
## Mark R Petersen and Phillip J Wolfram, 01/19/2018
## Last updated 4/20/2018
#
## delete soon:
#MPASTOOLS='/usr/projects/climate/mpeterse/repos/MPAS-Tools/jigsaw_to_MPAS'
#JIGSAW='/usr/projects/climate/mpeterse/repos/jigsaw-geo-matlab/master'
## octave command is system specific.  Correct later.
#MATLAB='octave --silent --eval '
#
## delete soon:
#JIGSAW2NETCDF=$MPASTOOLS/grid_gen/triangle_jigsaw_to_netcdf/
#MESHCONVERTER=$MPASTOOLS/grid_gen/mesh_conversion_tools/MpasMeshConverter.x
#CELLCULLER=$MPASTOOLS/grid_gen/mesh_conversion_tools/MpasCellCuller.x
#VTKEXTRACTOR=$MPASTOOLS/python_scripts/paraview_vtk_field_extractor/paraview_vtk_field_extractor.py
#
## First argument to this shell script is the name of the mesh
#MESHNAME='meshName'

print 'Step 1. Build mesh using JIGSAW ...'
args = ["octave","--silent","--eval",
        "driver_jigsaw_to_mpas"]
print "running", ' '.join(args)
subprocess.check_call(args, env=os.environ.copy())

print 'Step 2. Convert triangles from jigsaw format to netcdf...'
args = ['./triangle_jigsaw_to_netcdf.py',
        '-s',
        '-m', 'meshName-MESH.msh',
        '-o', 'meshName_triangles.nc']
print "running", ' '.join(args)
subprocess.check_call(args, env=os.environ.copy())

print 'Step 3. Convert from triangles to MPAS mesh...'
args = ['./MpasMeshConverter.x',
        'meshName_triangles.nc',
        'meshName_base_mesh.nc']
print "running", ' '.join(args)
subprocess.check_call(args, env=os.environ.copy())
print 'Injecting bathymetry ...'
args = ['./inject_bathymetry.py',
        'meshName_base_mesh.nc']
print "running", ' '.join(args)
#subprocess.check_call(args, env=os.environ.copy())

print 'Step 4. (Optional) Create vtk file for visualization'
args = ['./paraview_vtk_field_extractor.py',
        '--ignore_time',
				'-d','maxEdges=0',
        '-v', 'allOnCells',
        '-f', 'meshName_base_mesh.nc',
        '-o', 'meshName_base_mesh_vtk']
print "running", ' '.join(args)
subprocess.check_call(args, env=os.environ.copy())
# "paraview_vtk_field_extractor.py ${MESHNAME}_base_mesh.nc ${MESHNAME}_vtk"
#$VTKEXTRACTOR --ignore_time -d maxEdges=0 -v allOnCells -f  ${MESHNAME}_base_mesh.nc -o ${MESHNAME}_base_mesh_vtk
# 'done'
#
#print 'Step 5. (Optional) Cull land cells using topo.msh.  This is a quick cull, not the method for a production mesh.'
# "MpasCellCuller.x ${MESHNAME}_base_mesh.nc ${MESHNAME}_culled.nc"
#$CELLCULLER ${MESHNAME}_base_mesh.nc ${MESHNAME}_culled.nc
# 'Injecting bathymetry ...'
# "inject_bathymetry.py ${MESHNAME}_culled.nc"
#$JIGSAW2NETCDF/inject_bathymetry.py ${MESHNAME}_culled.nc
#
#print 'Step 6. (Optional) Create vtk file for visualization'
## "paraview_vtk_field_extractor.py ${MESHNAME}_base_mesh.nc ${MESHNAME}_vtk"
##$VTKEXTRACTOR --ignore_time -d maxEdges=0 -v allOnCells -f  ${MESHNAME}_culled.nc -o ${MESHNAME}_culled_vtk
