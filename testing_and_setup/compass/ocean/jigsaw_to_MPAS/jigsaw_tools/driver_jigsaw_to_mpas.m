function driver_jigsaw_to_mpas
%-----------------------------------------------------------
%   Mark Petersen (mpetersen@lanl.gov)
%   Phillip Wolfram (pwolfram@lanl.gov)
%   04/01/2018
%-----------------------------------------------------------

	 pathToJigsaw = 'jigsaw-geo-matlab'
   
   addpath(pathToJigsaw)
   addpath([pathToJigsaw '/dual-mesh'])
   addpath([pathToJigsaw '/jigsaw'])
   addpath([pathToJigsaw '/mesh-util'])
   
	 % temporary name
	 meshName = 'mesh'
   %------------------------------------ Load cellWidth, lon, lat
   load('cellWidth.mat')
   %------------------------------------ setup files for JIGSAW
   
   opts.geom_file = [ meshName '.msh'];      % GEOM file
   opts.jcfg_file = [ meshName '.jig'];      % JCFG file
   opts.mesh_file = [ meshName '-MESH.msh']; % MESH file
   opts.hfun_file = [ meshName '-HFUN.msh']; % HFUN file
           
   
   %------------------------------------ save HFUN data to file
   
   hmat.mshID = 'ELLIPSOID-GRID';
   hmat.point.coord{1} = lon*pi/180 ;
   hmat.point.coord{2} = lat*pi/180 ;
   hmat.value = cellWidthGlobal ;
   
   savemsh(opts.hfun_file,hmat) ;
   
   %------------------------------------ define JIGSAW geometry
   
   geom.mshID = 'ELLIPSOID-MESH';
   geom.radii = 6371.*ones(3,1) ;
   
   savemsh(opts.geom_file,geom) ;
   
   %------------------------------------ build mesh via JIGSAW!
   
   opts.hfun_scal = 'absolute';
   opts.hfun_hmax = +inf ;
   opts.hfun_hmin = +0.0 ;
   opts.mesh_dims = +2 ;               % 2-dim. simplexes
   opts.optm_qlim = 0.9375 ;
   opts.verbosity = +1 ;
   
   mesh = jigsaw  (opts) ;
