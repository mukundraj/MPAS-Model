function driver_jigsaw_to_mpas
%-----------------------------------------------------------
%   Mark Petersen (mpetersen@lanl.gov)
%   Phillip Wolfram (pwolfram@lanl.gov)
%   04/01/2018
%-----------------------------------------------------------

   makePlots = false;
	 pathToJigsaw = 'jigsaw-geo-matlab'
   
   addpath('mesh_definition_tools/latitude_1D_grids')
   addpath('mesh_definition_tools/spherical_tools')
   addpath(pathToJigsaw)
   addpath([pathToJigsaw '/dual-mesh'])
   addpath([pathToJigsaw '/jigsaw'])
   addpath([pathToJigsaw '/mesh-util'])
   
	 % temporary name
	 meshName = 'meshName'
   %------------------------------------ setup files for JIGSAW
   
   opts.geom_file = [ meshName '.msh'];      % GEOM file
   opts.jcfg_file = [ meshName '.jig'];      % JCFG file
   opts.mesh_file = [ meshName '-MESH.msh']; % MESH file
   opts.hfun_file = [ meshName '-HFUN.msh']; % HFUN file
           
   %------------------------------------ compute HFUN over GEOM
   [cellWidthGlobal,lon,lat] = feval(meshName);
   
   if (makePlots)
       figure('color','w');
       surf(lon,lat,cellWidthGlobal) ;
       view(2); axis image; hold on ;
       shading interp;
       title('JIGSAW HFUN data') ;
   end
   
   %------------------------------------ save HFUN data to file
   
       %cellWidthGlobal = ...
       %    cellWidthGlobal * 2./sqrt(3.);        %%!! it seems that we need this?
   
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
   
   %------------------------------------ draw mesh/cost outputs
   
   ang2 = triang2( ...                 % calc. tri-angles
       mesh.point.coord(:,1:3), ...
       mesh.tria3.index(:,1:3)) ;
   
   t_90 = max(ang2,[],2) > 90.0 ;
   t_95 = max(ang2,[],2) > 95.0 ;
   
   if (makePlots)
       figure;
       patch ('faces',mesh.tria3.index(:,1:3), ...
           'vertices',mesh.point.coord(:,1:3), ...
           'facecolor','w', ...
           'edgecolor',[.2,.2,.2]) ;
       hold on; axis image off;
       patch ('faces',mesh.tria3.index(t_90,1:3), ...
           'vertices',mesh.point.coord(:,1:3), ...
           'facecolor','y', ...
           'edgecolor',[.2,.2,.2]) ;
       patch ('faces',mesh.tria3.index(t_95,1:3), ...
           'vertices',mesh.point.coord(:,1:3), ...
           'facecolor','r', ...
           'edgecolor',[.2,.2,.2]) ;
       set(gca,'clipping','off') ;
       title('JIGSAW TRIA mesh') ;
   
       drawscr(mesh.point.coord (:,1:3), ...
               [], ...
               mesh.tria3.index (:,1:3)  ...
               ) ;
   
       drawnow ;
       set(figure(1),'units','normalized', ...
           'position',[.35,.55,.30,.35]) ;
       set(figure(2),'units','normalized', ...
           'position',[.05,.55,.30,.35]) ;
       set(figure(3),'units','normalized', ...
           'position',[.05,.10,.30,.35]) ;
       drawnow ;
     end
   
   end
   
   
