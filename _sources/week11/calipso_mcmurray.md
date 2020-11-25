---
anaconda-cloud: {}
jupytext:
  notebook_metadata_filter: all,-language_info,-toc,-latex_envs
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.12
    jupytext_version: 1.6.0
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

### Adding lidar data to the Ft. McMurray fire overpass

+++

#### 1. Read in the cloudsat and calipso groundtracks

See https://www-calipso.larc.nasa.gov/resources/calipso_users_guide/data_summaries/layer/index.php
for the lidar profile data specification

I've added two new functions to a301lib.geolocate:

* [trim_track](https://github.com/a301-teaching/a301_code/blob/5029c180cd8ebeb431069cc28b6699c8b7f4fcfa/a301lib/geolocate.py#L534)
  selects the part of the ground-track that is within a Modis scene
  
* [gc_distance](https://github.com/a301-teaching/a301_code/blob/5029c180cd8ebeb431069cc28b6699c8b7f4fcfa/a301lib/geolocate.py#L582) computes the great circle distance for a lon,lat groundtrack

```{code-cell} ipython3
import h5py
import numpy as np
import datetime as dt
from datetime import timezone as tz
from matplotlib import pyplot as plt
import pyproj
from numpy import ma
from a301utils.a301_readfile import download
from a301lib.cloudsat import get_geo as radar_get_geo
from a301lib.calipso import get_geo as lidar_get_geo
import json
from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap
from a301lib.geolocate import trim_track

modis_file='MYD021KM.A2016136.2015.006.reproject.h5'
cloudsat_file='2016136191427_53456_CS_2B-GEOPROF_GRANULE_P_R04_E06.h5'
calipso_file='CAL_LID_L2_05kmALay-Prov-V3-30.2016-05-15T19-42-56ZD_Subset.h5'
download(modis_file)
download(cloudsat_file)
download(calipso_file)
download('after_stretch.png')  #my png file created by qgis
```

#### get the groundtracks for  cloudsat and calipso

```{code-cell} ipython3
radar_lats,radar_lons,radar_date_times,radar_prof_times,radar_dem_elevation=radar_get_geo(cloudsat_file)
    
lidar_lats,lidar_lons,lidar_date_times,lidar_prof_times,lidar_dem_elevation=lidar_get_geo(calipso_file)
```

#### Read in the modis image for Ft. Mcmurray

```{code-cell} ipython3
with h5py.File(modis_file,'r') as h5_file:
    basemap_string=h5_file.attrs['basemap_args']
    basemap_args=json.loads(basemap_string)
    chan1=h5_file['channels']['1'][...]
    geotiff_string = h5_file.attrs['geotiff_args']
    geotiff_args = json.loads(geotiff_string)
    level1b_file=h5_file.attrs['level1b_file']

transform = geotiff_args['adfgeotransform']
print('basemap_args: \n{}\n'.format(basemap_args))
print('geotiff_args: \n{}\n'.format(geotiff_args))
```

#### Plot the two groundtracks on a 8 bit (256 color) modis image of channel 1

+++

### read in my hand-crafted qgis file which I've converted to png

```{code-cell} ipython3
%matplotlib inline
from matplotlib import cm
from matplotlib.colors import Normalize

cmap=cm.autumn  #see http://wiki.scipy.org/Cookbook/Matplotlib/Show_colormaps
cmap.set_over('w')
cmap.set_under('b',alpha=0.2)
cmap.set_bad('0.75') #75% grey

plt.close('all')
fig,ax = plt.subplots(1,1,figsize=(14,14))
#
# set up the Basemap object
#
basemap_args['ax']=ax
basemap_args['resolution']='c'
bmap = Basemap(**basemap_args)
print(bmap.projparams)
x0,y0=bmap.projparams['x_0'],bmap.projparams['y_0']
#
# transform the ground track lons/lats to x/y
#
radarx,radary=bmap(radar_lons,radar_lats)
lidarx,lidary=bmap(lidar_lons,lidar_lats)

x0,y0 = bmap.projparams['x_0'],bmap.projparams['y_0']
lidar_hit=trim_track(lidarx,lidary,chan1,transform,x0=x0,y0=y0)
lidarx,lidary=lidarx[lidar_hit],lidary[lidar_hit]
lidar_lons,lidar_lats=lidar_lons[lidar_hit],lidar_lats[lidar_hit]

hit=trim_track(radarx,radary,chan1,transform,x0=x0,y0=y0)
radarx,radary=radarx[hit],radary[hit]
radar_lons,radar_lats = radar_lons[hit],radar_lats[hit]

# #
# # plot as blue circles
# #
bmap.plot(radarx,radary,'bo',alpha=0.2)
bmap.plot(lidarx,lidary,'ro')
#
# now plot channel 1
#
num_meridians=180
num_parallels = 90
col = bmap.imshow(chan1, origin='upper',cmap=cmap, vmin=0, vmax=0.1)

lon_sep, lat_sep = 5,5
parallels = np.arange(-90, 90, lat_sep)
meridians = np.arange(0, 360, lon_sep)
bmap.drawparallels(parallels, labels=[1, 0, 0, 0],
                       fontsize=10, latmax=90)
bmap.drawmeridians(meridians, labels=[0, 0, 0, 1],
                       fontsize=10, latmax=90)
bmap.drawcoastlines()
colorbar=fig.colorbar(col, shrink=0.5, pad=0.05,extend='both')
colorbar.set_label('channel1 reflectivity',rotation=-90,verticalalignment='bottom')
_=ax.set(title='Ft. McMurray')
```

#### Write the groundtracks out for future translation to shapefiles with fiona (as in vector_data.ipynb)

```{code-cell} ipython3
groundtrack_name = modis_file.replace('reproject','groundtrack')
print('writing groundtrack to {}'.format(groundtrack_name))
#
# h5 files can't store dates, but they can store floating point
# seconds since 1970, which is called POSIX timestamp
#
radar_timestamps = [item.timestamp() for item in radar_date_times]
radar_timestamps= np.array(radar_timestamps)
lidar_timestamps = [item.timestamp() for item in lidar_date_times]
lidar_timestamps= np.array(lidar_timestamps)
with h5py.File(groundtrack_name,'w') as groundfile:
    groundfile.attrs['cloudsat_filename']=cloudsat_file
    groundfile.attrs['calipso_filename']=calipso_file
    groundfile.attrs['modis_filename']=level1b_file
    groundfile.attrs['reproject_filename']=modis_file
    groundfile.attrs['basemap_args']=basemap_string
    groundfile.attrs['geotiff_args']=geotiff_string
    groundfile.attrs['proj4params']=json.dumps(bmap.projparams,indent=4)
    dset=groundfile.create_dataset('radar_lons',radar_lons.shape,radar_lons.dtype)
    dset[...] = radar_lons[...]
    dset.attrs['long_name']='radar longitude'
    dset.attrs['units']='degrees East'
    dset=groundfile.create_dataset('radar_lats',radar_lats.shape,radar_lats.dtype)
    dset[...] = radar_lats[...]
    dset.attrs['long_name']='radar latitude'
    dset.attrs['units']='degrees North'
    dset= groundfile.create_dataset('radar_times',radar_timestamps.shape,radar_timestamps.dtype)
    dset[...] = radar_timestamps[...]

    dset=groundfile.create_dataset('lidar_lons',lidar_lons.shape,lidar_lons.dtype)
    dset[...] = lidar_lons[...]
    dset.attrs['long_name']='lidar longitude'
    dset.attrs['units']='degrees East'
    dset=groundfile.create_dataset('lidar_lats',lidar_lats.shape,lidar_lats.dtype)
    dset[...] = lidar_lats[...]
    dset.attrs['long_name']='lidar latitude'
    dset.attrs['units']='degrees North'
    dset= groundfile.create_dataset('lidar_times',lidar_timestamps.shape,lidar_timestamps.dtype)
    dset[...] = lidar_timestamps[...]
    dset.attrs['long_name']='lidar UTC datetime timestamp'
    dset.attrs['units']='seconds since Jan. 1, 1970'
```

```{code-cell} ipython3
fig,ax = plt.subplots(1,1,figsize=(14,14))
basemap_args['ax']=ax
basemap_args['resolution']='i'
bmap = Basemap(**basemap_args)
im=plt.imread('after_stretch.png')
bmap.imshow(im,origin='upper')
bmap.plot(radarx,radary,'bo',alpha=0.2)
bmap.plot(lidarx,lidary,'ro')

num_meridians=180
num_parallels = 90
lon_sep, lat_sep = 5,5
parallels = np.arange(-90, 90, lat_sep)
meridians = np.arange(0, 360, lon_sep)
bmap.drawparallels(parallels, labels=[1, 0, 0, 0],
                       fontsize=10, latmax=90)
bmap.drawmeridians(meridians, labels=[0, 0, 0, 1],
                       fontsize=10, latmax=90)
bmap.drawcoastlines()
```

#### Plot the 0.5 micron and the 1.0 micron optical depthts for calipso 

Is the lidar seeing the smoke plumes from the fire?

```{code-cell} ipython3
%matplotlib inline
from a301lib.geolocate import gc_distance
distance=gc_distance(lidar_lons,lidar_lats)
with h5py.File(calipso_file,'r') as infile:
    aer_532=infile['Column_Optical_Depth_Aerosols_532'][...]
    aer_1064=infile['Column_Optical_Depth_Aerosols_1064'][...]
fig,(ax1,ax2)=plt.subplots(2,1,figsize=(14,4))
ax1.plot(lidar_lats,aer_532[lidar_hit])
ax2.set(title='0.5 micron optical depth',ylabel='optical depth',xlabel='latitude (deg N)');
ax2.plot(distance,aer_532[lidar_hit])
ax2.set(ylabel='optical depth',xlabel='distance (km)');
```

```{code-cell} ipython3
fig,(ax1,ax2)=plt.subplots(2,1,figsize=(14,4))
ax1.plot(lidar_lats,aer_1064[lidar_hit])
ax1.set(ylabel='optical depth',xlabel='latitude (deg N)');
ax2.plot(distance,aer_1064[lidar_hit])
ax2.set(title='1 micron optical depth',ylabel='optical depth',xlabel='distance (km)');
```

```{code-cell} ipython3

```
