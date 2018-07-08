function predriver_jigsaw_to_mpas
%-----------------------------------------------------------
%   Mark Petersen (mpetersen@lanl.gov)
%   Phillip Wolfram (pwolfram@lanl.gov)
%   04/01/2018
%-----------------------------------------------------------

	 pathToJigsaw = 'jigsaw-geo-matlab'
   
   addpath('mesh_definition_tools/latitude_1D_grids')
   addpath('mesh_definition_tools/spherical_tools')
   
	 % temporary name
	 meshName = 'mesh'
   %------------------------------------ compute HFUN over GEOM
   [cellWidthGlobal,lon,lat] = feval(meshName);
	 save('cellWidth.mat','cellWidthGlobal','lon','lat')
